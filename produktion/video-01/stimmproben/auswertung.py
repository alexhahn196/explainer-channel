#!/usr/bin/env python3
"""Verbindet Spracherkennung und Akustikmessung zu den vier Pruefpunkten.

Was diese Auswertung leisten kann und was nicht
-----------------------------------------------
MESSBAR und hier beantwortet:
  * Verstaendlichkeit unter Tempo — als Wortfehlerrate der Erkennung gegen
    den Solltext. Der Erkenner ist ueber alle Proben derselbe, also ist die
    DIFFERENZ zwischen Lauf A und B einer Stimme aussagekraeftig.
  * Satzgrenzen — als Zahl und Laenge der Pausen an Satzenden.
  * Aussprache der Stolperstellen — als das, was ein Erkenner hoert, der den
    Sollwert nicht kennt.
  * Pointe — als Pause davor, Tonhoehenhub und Pegel gegen die eigene Grundlinie.
  * Technische Defekte — Uebersteuerung, Sprungstellen, Abriss.

NICHT MESSBAR und hier bewusst nicht behauptet:
  * ob eine schnelle Fassung "wach" oder "gehetzt" wirkt
  * Alter, Timbre, Register, Sympathie einer Stimme
  * ob eine Aussprache "richtig genug" ist
Das sind Hoereindruecke. Sie stehen in keiner Zeile dieser Datei.
"""
from __future__ import annotations

import json
import pathlib
import re

import numpy as np

HIER = pathlib.Path(__file__).resolve().parent

# Stolperstellen aus aussprache.md, die im Testtext vorkommen, mit der Stelle
# im Solltext (Wortindex, 0-basiert) und der in aussprache.md benannten Fehlform.
STOLPERSTELLEN = [
    ("Dümmer",         "DUEM-uh / Notloesung DEE-mer", "klingt wie *dumber*"),
    ("Campemoor",      "KAHM-puh-mohr",                "engl. *camp-uh-moor* mit /uː/"),
    ("Pr 31",          "P-R thirty-one",               "als Wort statt Buchstaben"),
    ("Widan el-Faras", "wih-DAAN el FA-rass",          "Betonung auf 1. statt 2. Silbe"),
]

POINTE = "The wheel is not the parent of the road. The wheel is a guest on it."


def normalisiere(t: str) -> list[str]:
    t = t.lower().replace("—", " ").replace("’", "'")
    t = re.sub(r"[^a-z0-9'\s]", " ", t)
    return t.split()


def wer(soll: list[str], ist: list[str]) -> dict:
    """Wortfehlerrate ueber Levenshtein-Ausrichtung."""
    n, m = len(soll), len(ist)
    d = np.zeros((n + 1, m + 1), dtype=np.int32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            k = 0 if soll[i - 1] == ist[j - 1] else 1
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + k)
    # Rueckverfolgung fuer die Fehlerarten
    i, j, ers, ein, aus = n, m, 0, 0, 0
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i, j] == d[i-1, j-1] + (0 if soll[i-1] == ist[j-1] else 1):
            if soll[i-1] != ist[j-1]:
                ers += 1
            i, j = i - 1, j - 1
        elif i > 0 and d[i, j] == d[i-1, j] + 1:
            aus += 1
            i -= 1
        else:
            ein += 1
            j -= 1
    return {"wer_pct": round(d[n, m] / max(n, 1) * 100, 2),
            "ersetzt": ers, "eingefuegt": ein, "ausgelassen": aus,
            "soll_woerter": n, "ist_woerter": m}


def finde_folge(woerter: list[dict], muster: list[str],
                ab: int = 0) -> tuple[int, int] | None:
    """Sucht eine Wortfolge in der Erkennung, tolerant gegen einzelne Fehler."""
    norm = [re.sub(r"[^a-z0-9']", "", w["wort"].lower()) for w in woerter]
    L = len(muster)
    bestes, beste_treffer = None, 0
    for i in range(ab, max(ab, len(norm) - L + 1)):
        treffer = sum(1 for a, b in zip(norm[i:i + L], muster) if a == b)
        if treffer > beste_treffer:
            beste_treffer, bestes = treffer, (i, i + L)
    return bestes if beste_treffer >= max(2, L // 2) else None


def umfeld(woerter: list[dict], marker: list[str], breite: int = 3) -> dict | None:
    """Gibt die erkannten Woerter rund um eine Fundstelle samt Zeit zurueck."""
    tr = finde_folge(woerter, marker)
    if not tr:
        return None
    a = max(0, tr[0] - breite)
    b = min(len(woerter), tr[1] + breite)
    return {"erkannt": " ".join(w["wort"] for w in woerter[tr[0]:tr[1]]),
            "umfeld": " ".join(w["wort"] for w in woerter[a:b]),
            "von": woerter[tr[0]]["von"], "bis": woerter[tr[1] - 1]["bis"]}


def pointe_messen(ak: dict, woerter: list[dict]) -> dict | None:
    tr = finde_folge(woerter, ["the", "wheel", "is", "not", "the", "parent"])
    if not tr:
        return None
    start = woerter[tr[0]]["von"]
    ende = woerter[-1]["bis"]
    f0 = np.array(ak["_f0"])
    rms = np.array(ak["_rms_db"])
    t = np.arange(len(f0)) * 0.01
    tr_ = np.arange(len(rms)) * 0.01
    drin = (t >= start) & (t <= ende)
    davor = t < start
    f_drin = f0[drin & (f0 > 0)]
    f_davor = f0[davor & (f0 > 0)]
    # Pegel nur ueber Sprachrahmen vergleichen. Ohne diese Schranke zaehlt die
    # Stille zwischen den Saetzen mit, und ein Abschnitt mit mehr Pause sieht
    # dann faelschlich leiser aus.
    sprechpegel = float(np.percentile(rms, 85))
    laut = rms > (sprechpegel - 25.0)
    r_drin = rms[(tr_ >= start) & (tr_ <= ende) & laut]
    r_davor = rms[(tr_ < start) & laut]
    # Pause unmittelbar vor der Pointe: die letzte Pause, die vor dem ersten
    # Wort endet. Die Wortzeiten der Erkennung haben Schlupf, darum ein
    # grosszuegiges Fenster statt einer engen Punktsuche.
    pause_davor = 0.0
    kandidaten = [p for p in ak["pausen"] if start - 0.9 < p["bis"] < start + 0.6]
    if kandidaten:
        pause_davor = max(p["dauer"] for p in kandidaten)
    if len(f_drin) == 0 or len(f_davor) == 0:
        return None
    return {
        "beginn_s": round(start, 2),
        "pause_davor_s": round(pause_davor, 3),
        "pause_median_sonst_s": ak["pause_median_s"],
        "f0_median_pointe_hz": round(float(np.median(f_drin)), 1),
        "f0_median_davor_hz": round(float(np.median(f_davor)), 1),
        "f0_unterschied_halbtoene": round(
            float(12 * np.log2(np.median(f_drin) / np.median(f_davor))), 2),
        "f0_hub_pointe_halbtoene": round(
            float(12 * np.log2(np.percentile(f_drin, 90) / np.percentile(f_drin, 10))), 2),
        "f0_hub_davor_halbtoene": round(
            float(12 * np.log2(np.percentile(f_davor, 90) / np.percentile(f_davor, 10))), 2),
        "pegel_unterschied_db": round(float(np.median(r_drin) - np.median(r_davor)), 2),
    }


def main() -> None:
    asr = json.loads((HIER / "asr_ergebnis.json").read_text(encoding="utf-8"))
    ak = json.loads((HIER / "akustik_ergebnis.json").read_text(encoding="utf-8"))
    vl = json.loads((HIER / "akustik_verlauf.json").read_text(encoding="utf-8"))
    for k, v in ak.items():
        v.update(vl[k])
    soll_roh = (HIER / "elevenlabs" / "testtext.txt").read_text(encoding="utf-8").strip()
    soll = normalisiere(soll_roh)

    raus = {}
    for stem in sorted(ak):
        e = {"akustik": {k: v for k, v in ak[stem].items() if not k.startswith("_")}}
        for modell in asr:
            if stem not in asr[modell]:
                continue
            w = asr[modell][stem]["woerter"]
            m = {"wer": wer(soll, normalisiere(asr[modell][stem]["text"])),
                 "stolperstellen": {}}
            for name, _soll_sprech, _fehlform in STOLPERSTELLEN:
                marker = {
                    "Dümmer": ["called", "the", "dummer"],
                    "Campemoor": ["called", "the", "campemore"],
                    "Pr 31": ["a", "path", "labeled"],
                    "Widan el-Faras": ["the", "quarry", "is", "called"],
                }[name]
                m["stolperstellen"][name] = umfeld(w, marker)
            m["pointe"] = pointe_messen(ak[stem], w)
            e[modell] = m
        raus[stem] = e

    (HIER / "auswertung.json").write_text(
        json.dumps(raus, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"auswertung.json geschrieben — {len(raus)} Proben")


if __name__ == "__main__":
    main()
