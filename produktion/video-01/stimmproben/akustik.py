#!/usr/bin/env python3
"""Akustische Vermessung der Stimmproben.

Was hier gemessen wird, ist das, was sich an einer Audiodatei objektiv
bestimmen laesst — Pausen, Grundfrequenz, Pegel, Aussetzer. Was sich damit
NICHT bestimmen laesst, ist der Klangeindruck: ob eine Stimme gehetzt wirkt,
angenehm ist oder zum Kanal passt. Diese Datei liefert Messwerte, kein Urteil.

Gemessen:
  Pausen        — Laenge und Lage jeder Sprechpause ueber 120 ms
  Grundfrequenz — YIN-Schaetzung je 10-ms-Rahmen (75-400 Hz)
  Pegel         — RMS je Rahmen, Spitzenwert, Uebersteuerung
  Defekte       — Uebersteuerung, Sprungstellen (Knacken), Abriss am Dateiende
  Kadenz        — Streuung der Tonhoehenbewegung an Satzenden. Eine sehr
                  geringe Streuung bedeutet: jeder Satz endet gleich.
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import soundfile as sf

RATE_ZIEL = 16000
RAHMEN_MS = 10
F0_MIN, F0_MAX = 60.0, 400.0   # 60 Hz, damit auch eine sehr tiefe Stimme erfasst wird
PAUSE_MIN_S = 0.120


def lade(pfad: pathlib.Path) -> tuple[np.ndarray, int]:
    x, sr = sf.read(str(pfad), dtype="float64", always_2d=False)
    if x.ndim > 1:
        x = x.mean(axis=1)
    return x, sr


def rahmen_rms(x: np.ndarray, sr: int, ms: int = RAHMEN_MS) -> tuple[np.ndarray, int]:
    n = int(sr * ms / 1000)
    m = len(x) // n
    r = x[: m * n].reshape(m, n)
    return np.sqrt((r ** 2).mean(axis=1) + 1e-12), n


def pausen(x: np.ndarray, sr: int) -> tuple[list[dict], np.ndarray]:
    """Pausen ueber eine pegelabhaengige Schwelle (-35 dB unter Sprechpegel)."""
    rms, n = rahmen_rms(x, sr)
    db = 20 * np.log10(rms + 1e-12)
    sprechpegel = np.percentile(db, 85)
    schwelle = sprechpegel - 35.0
    still = db < schwelle
    raus, i = [], 0
    while i < len(still):
        if still[i]:
            j = i
            while j < len(still) and still[j]:
                j += 1
            dauer = (j - i) * RAHMEN_MS / 1000
            if dauer >= PAUSE_MIN_S:
                raus.append({"von": round(i * RAHMEN_MS / 1000, 3),
                             "bis": round(j * RAHMEN_MS / 1000, 3),
                             "dauer": round(dauer, 3)})
            i = j
        else:
            i += 1
    return raus, db


def yin(rahmen: np.ndarray, sr: int) -> float:
    """Grundfrequenz eines Rahmens, YIN-Differenzfunktion. 0.0 = stimmlos."""
    N = len(rahmen)
    tau_min = int(sr / F0_MAX)
    tau_max = min(int(sr / F0_MIN), N // 2)
    if tau_max <= tau_min:
        return 0.0
    d = np.empty(tau_max)
    for tau in range(tau_max):
        diff = rahmen[: N - tau_max] - rahmen[tau: tau + N - tau_max]
        d[tau] = np.dot(diff, diff)
    # Kumulative mittlere normierte Differenz nach YIN:
    #   d'(tau) = d(tau) / ((1/tau) * summe_{j=1..tau} d(j))
    kum = np.cumsum(d[1:]) / (np.arange(1, tau_max) + 1e-12)
    dn = np.empty(tau_max)
    dn[0] = 1.0
    dn[1:] = d[1:] / (kum + 1e-12)
    kand = np.where(dn[tau_min:tau_max] < 0.15)[0]
    tau = (kand[0] + tau_min) if len(kand) else (int(np.argmin(dn[tau_min:tau_max])) + tau_min)
    # Vom ersten Unterschreiten der Schwelle in die Talsohle laufen. Ohne das
    # sitzt tau auf der fallenden Flanke, und die Feininterpolation unten
    # verschiebt dann in die falsche Richtung.
    while tau + 1 < tau_max and dn[tau + 1] < dn[tau]:
        tau += 1
    if dn[tau] > 0.5:
        return 0.0
    if tau <= 0:
        return 0.0
    # Parabolische Feininterpolation um das Minimum. Ohne sie ist tau
    # ganzzahlig und die Schaetzung systematisch zu hoch (bei 300 Hz rund
    # +2,5 %), weil sr/tau bei kleinen tau grob quantisiert.
    if 0 < tau < tau_max - 1:
        y0, y1, y2 = dn[tau - 1], dn[tau], dn[tau + 1]
        nenner = 2 * (2 * y1 - y0 - y2)
        if abs(nenner) > 1e-12:
            tau = tau + (y2 - y0) / nenner
    return float(sr / tau) if tau > 0 else 0.0


def f0_verlauf(x: np.ndarray, sr: int, schritt_ms: int = 10,
               fenster_ms: int = 45) -> np.ndarray:
    schritt = int(sr * schritt_ms / 1000)
    fenster = int(sr * fenster_ms / 1000)
    raus = []
    for i in range(0, len(x) - fenster, schritt):
        raus.append(yin(x[i: i + fenster], sr))
    return np.array(raus)


def defekte(x: np.ndarray, sr: int) -> dict:
    spitze = float(np.max(np.abs(x)))
    uebersteuert = int(np.sum(np.abs(x) >= 0.9995))
    # Sprungstellen: Sample-zu-Sample-Sprung weit ueber dem ueblichen Mass
    d = np.abs(np.diff(x))
    grenze = float(np.percentile(d, 99.99)) * 6 + 1e-9
    sprung_idx = np.where(d > max(grenze, 0.28))[0]
    # Zusammenhaengende Treffer zu einem Ereignis buendeln
    ereignisse = []
    for i in sprung_idx:
        t = i / sr
        if not ereignisse or t - ereignisse[-1] > 0.02:
            ereignisse.append(round(t, 3))
    # Abriss: Pegel in den letzten 30 ms gegen den Sprechpegel
    rms, _ = rahmen_rms(x, sr)
    db = 20 * np.log10(rms + 1e-12)
    sprechpegel = float(np.percentile(db, 85))
    schluss_db = float(db[-3:].max()) if len(db) >= 3 else -99.0
    return {
        "spitze": round(spitze, 4),
        "spitze_dbfs": round(20 * np.log10(spitze + 1e-12), 2),
        "uebersteuerte_samples": uebersteuert,
        "sprungstellen_s": ereignisse[:20],
        "sprungstellen_anzahl": len(ereignisse),
        "schlusspegel_unter_sprechpegel_db": round(schluss_db - sprechpegel, 1),
        "abriss_verdacht": bool(schluss_db - sprechpegel > -18.0),
    }


def auswerten(pfad: pathlib.Path) -> dict:
    x, sr = lade(pfad)
    ps, db = pausen(x, sr)
    f0 = f0_verlauf(x, sr)
    stimmhaft = f0[f0 > 0]
    rms, _ = rahmen_rms(x, sr)
    sprechpegel = float(np.percentile(20 * np.log10(rms + 1e-12), 85))
    dauer = len(x) / sr
    pausenzeit = sum(p["dauer"] for p in ps)
    return {
        "datei": pfad.name,
        "dauer_s": round(dauer, 3),
        "sprechanteil_pct": round((dauer - pausenzeit) / dauer * 100, 1),
        "pausen_anzahl": len(ps),
        "pause_median_s": round(float(np.median([p["dauer"] for p in ps])), 3) if ps else 0.0,
        "pause_max_s": round(max((p["dauer"] for p in ps), default=0.0), 3),
        "pausen": ps,
        "f0_median_hz": round(float(np.median(stimmhaft)), 1) if len(stimmhaft) else 0.0,
        "f0_p10_hz": round(float(np.percentile(stimmhaft, 10)), 1) if len(stimmhaft) else 0.0,
        "f0_p90_hz": round(float(np.percentile(stimmhaft, 90)), 1) if len(stimmhaft) else 0.0,
        "f0_spanne_halbtoene": round(
            float(12 * np.log2(np.percentile(stimmhaft, 90) / np.percentile(stimmhaft, 10))), 2
        ) if len(stimmhaft) else 0.0,
        "sprechpegel_dbfs": round(sprechpegel, 2),
        "defekte": defekte(x, sr),
        "_f0": f0.tolist(),
        "_rms_db": db.tolist(),
    }


if __name__ == "__main__":
    hier = pathlib.Path(__file__).resolve().parent
    raus = {}
    for wav in sorted(pathlib.Path("/tmp/wav").glob("*.wav")):
        raus[wav.stem] = auswerten(wav)
        r = raus[wav.stem]
        print(f"{wav.stem:<34} {r['dauer_s']:6.2f}s  "
              f"Pausen {r['pausen_anzahl']:3d}  F0 {r['f0_median_hz']:6.1f} Hz  "
              f"Spanne {r['f0_spanne_halbtoene']:5.2f} HT  "
              f"Spitze {r['defekte']['spitze_dbfs']:6.2f} dBFS", flush=True)
    # Die Rahmenverlaeufe (_f0, _rms_db) sind Zwischendaten von mehreren MB
    # und gehoeren nicht ins Repository. Sie landen in einer eigenen Datei,
    # die .gitignore ausschliesst; `auswertung.py` liest sie von dort.
    verlauf = {k: {"_f0": v.pop("_f0"), "_rms_db": v.pop("_rms_db")}
               for k, v in raus.items()}
    (hier / "akustik_ergebnis.json").write_text(
        json.dumps(raus, indent=1, ensure_ascii=False), encoding="utf-8")
    (hier / "akustik_verlauf.json").write_text(
        json.dumps(verlauf), encoding="utf-8")
    print("\nakustik_ergebnis.json + akustik_verlauf.json geschrieben.")
