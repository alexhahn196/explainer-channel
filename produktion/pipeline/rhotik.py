#!/usr/bin/env python3
"""
rhotik.py - misst die Rhotizitaet einer Stimme ueber den F3-Formanten.

Verfahren identisch zu Stimmtest Runde 2 (stimmtest/akzent_rhotik.json,
stimmtest/screen_r2d.json). Nicht veraendern, sonst sind die Werte nicht
mehr mit den dort veroeffentlichten Referenzen vergleichbar:

  1. faster-whisper "base.en", int8, beam_size=1, mit Wort-Zeitstempeln.
  2. Jedes Vorkommen eines Zielworts wird ausgeschnitten:
     [start - 0.02 s, ende + 0.05 s].
  3. Praat-Burg-Formantanalyse (5 Formanten, Obergrenze 5000 Hz),
     F3 alle 10 ms abgetastet.
  4. Das MINIMUM von F3 ueber das Wort ist der Messwert. Ein gesprochenes
     /r/ senkt F3 stark ab; faellt das Minimum unter 2100 Hz, gilt das
     Token als rhotisch (= amerikanisch/neutral gesprochen).
  5. Ergebnis: "rhotische Tokens / verwertbare Tokens" plus der Median
     aller Minima.

Referenzwerte aus Runde 2 (kurze Probe, John 1):
  Calm (britisch gefaerbt)      F3-Median 2269 Hz   0/5
  Jameson (neutral american)    F3-Median 1638 Hz   5/5

Zielwoerter: Woerter mit /r/ NACH dem Vokal (postvokalisch). Nur dort
unterscheiden sich rhotische und nicht-rhotische Aussprache ueberhaupt.
"word" und "darkness" sind der Satz aus Runde 2; "lord" und "shepherd"
kommen dazu, wenn der Text sie hergibt.

Aufruf:
    python3 produktion/pipeline/rhotik.py DATEI [DATEI ...] [--json AUS]
    python3 produktion/pipeline/rhotik.py DATEI --max-sekunden 900
"""
import argparse, json, os, sys

import numpy as np
import parselmouth
import soundfile as sf
from faster_whisper import WhisperModel

# Runde-2-Satz zuerst - nur diese beiden sind direkt mit den
# veroeffentlichten Referenzwerten vergleichbar.
ZIEL_R2 = {"word", "words", "darkness"}
ZIEL_ERWEITERT = ZIEL_R2 | {"lord", "lord's", "shepherd", "shepherd's"}

GRENZE_HZ = 2100.0          # unterhalb = /r/ gesprochen
VOR_S, NACH_S = 0.02, 0.05  # Randzugabe um das Wort
SCHRITT_S = 0.01            # Abtastung des Formantverlaufs


def _tokens(pfad, modell, ziel, max_s=None):
    """ASR mit Wort-Zeitstempeln, gefiltert auf die Zielwoerter."""
    segs, _ = modell.transcribe(pfad, word_timestamps=True, beam_size=1)
    out = []
    for s in segs:
        if max_s is not None and s.start > max_s:
            break
        for w in (s.words or []):
            t = w.word.strip().lower().strip(".,!?;:“”\"'")
            if t in ziel:
                out.append((t, w.start, w.end))
    return out


def _f3_minimum(daten, sr, a, b):
    """Kleinster F3-Wert ueber das ausgeschnittene Wort, oder None."""
    i0 = max(0, int((a - VOR_S) * sr))
    i1 = min(len(daten), int((b + NACH_S) * sr))
    if i1 - i0 < int(0.03 * sr):
        return None
    schnipsel = daten[i0:i1].astype(np.float64)
    snd = parselmouth.Sound(schnipsel, sampling_frequency=sr)
    try:
        fm = snd.to_formant_burg(max_number_of_formants=5, maximum_formant=5000)
    except Exception:
        return None
    werte = []
    x = 0.01
    while x < snd.duration - 0.01:
        v = fm.get_value_at_time(3, x)
        if v and not np.isnan(v):
            werte.append(v)
        x += SCHRITT_S
    return min(werte) if werte else None


def messen(pfad, modell, ziel=ZIEL_ERWEITERT, max_s=None):
    """Ein Audiofile vermessen. Gibt Kennzahlen und Tokenliste zurueck."""
    daten, sr = sf.read(pfad, dtype="float32", always_2d=True)
    daten = daten.mean(axis=1)
    tok = _tokens(pfad, modell, ziel, max_s)
    treffer = []
    for t, a, b in tok:
        if max_s is not None and a > max_s:
            continue
        f3 = _f3_minimum(daten, sr, a, b)
        if f3 is not None:
            treffer.append({"wort": t, "s": round(a, 2), "f3_min": round(float(f3), 1)})
    if not treffer:
        return {"datei": pfad, "tokens": 0, "quote": "0/0", "f3_median": None,
                "urteil": "keine verwertbaren Tokens", "treffer": []}

    minima = [d["f3_min"] for d in treffer]
    rhot = sum(1 for v in minima if v < GRENZE_HZ)
    r2 = [d for d in treffer if d["wort"] in ZIEL_R2]
    r2_rhot = sum(1 for d in r2 if d["f3_min"] < GRENZE_HZ)
    anteil = rhot / len(minima)
    urteil = ("rhotisch (amerikanisch/neutral)" if anteil >= 0.7 else
              "nicht-rhotisch (britisch gefaerbt)" if anteil <= 0.3 else
              "uneinheitlich")
    return {
        "datei": pfad,
        "tokens": len(minima),
        "quote": f"{rhot}/{len(minima)}",
        "anteil_rhotisch": round(anteil, 3),
        "f3_median": round(float(np.median(minima)), 1),
        "f3_p25": round(float(np.percentile(minima, 25)), 1),
        "f3_p75": round(float(np.percentile(minima, 75)), 1),
        "quote_nur_r2_woerter": f"{r2_rhot}/{len(r2)}" if r2 else "0/0",
        "je_wort": {w: f"{sum(1 for d in treffer if d['wort'] == w and d['f3_min'] < GRENZE_HZ)}"
                       f"/{sum(1 for d in treffer if d['wort'] == w)}"
                    for w in sorted({d["wort"] for d in treffer})},
        "urteil": urteil,
        "treffer": treffer,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dateien", nargs="+")
    ap.add_argument("--json", dest="aus")
    ap.add_argument("--max-sekunden", type=float, default=None,
                    help="nur die ersten N Sekunden auswerten")
    ap.add_argument("--nur-r2-woerter", action="store_true",
                    help="nur 'word'/'darkness' wie in Runde 2")
    a = ap.parse_args()

    ziel = ZIEL_R2 if a.nur_r2_woerter else ZIEL_ERWEITERT
    modell = WhisperModel("base.en", device="cpu", compute_type="int8")
    erg = []
    print(f"{'Datei':34s} {'Tokens':>7} {'rhotisch':>10} {'F3-Median':>10}  Urteil")
    for p in a.dateien:
        if not os.path.exists(p):
            print(f"{os.path.basename(p):34s}  DATEI FEHLT", flush=True)
            continue
        r = messen(p, modell, ziel, a.max_sekunden)
        erg.append(r)
        f3 = r["f3_median"] if r["f3_median"] is not None else "-"
        print(f"{os.path.basename(p):34s} {r['tokens']:>7} {r['quote']:>10} "
              f"{f3:>10}  {r['urteil']}", flush=True)
        if r["treffer"]:
            print(f"{'':34s} je Wort: {r['je_wort']}", flush=True)
    if a.aus:
        json.dump(erg, open(a.aus, "w"), ensure_ascii=False, indent=1)
        print(f"\ngeschrieben: {a.aus}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
