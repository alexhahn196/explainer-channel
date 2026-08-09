#!/usr/bin/env python3
"""
render.py - faehrt die ganze Pipeline fuer ein Video.

    python3 produktion/pipeline/render.py V1
    python3 produktion/pipeline/render.py V3 --ab 4
    python3 produktion/pipeline/render.py V2 --nur 1 2

Jeder Schritt ist einzeln aufrufbar und wiederaufsetzbar. Fertige Chunks
werden nicht neu erzeugt, also kostet ein Abbruch nur den laufenden Schritt.

Voraussetzung fuer Schritt 2: FISH_KEY in der Umgebung.
Schritt 4 nimmt mit --bild ein extern erzeugtes Standbild an; ohne das
Argument erzeugt es selbst einen einfachen Ersatz.
"""
import argparse
import os
import subprocess
import sys
import time

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)

SCHRITTE = [
    (1, "Text",        "schritt1_text.py",  []),
    (2, "TTS",         "schritt2_tts.py",   []),
    (3, "Klangbett",   "schritt3_bett.py",  []),
    (4, "Standbild",   "schritt4_bild.py",  []),
    (5, "Video",       "schritt5_video.py", []),
    (6, "Untertitel",  "schritt6_srt.py",   []),
    (7, "Paket",       "schritt7_paket.py", []),
]
ZUSATZ = [("Aussprache-QA", "qa_namen.py")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video", help="V1 … V8")
    ap.add_argument("--ab", type=int, default=1)
    ap.add_argument("--bis", type=int, default=7)
    ap.add_argument("--nur", type=int, nargs="+")
    ap.add_argument("--bild", help="Standbild für Schritt 4")
    ap.add_argument("--hook", choices=["a", "b"])
    a = ap.parse_args()

    if a.video[0] != "V" or not a.video[1:].isdigit():
        raise SystemExit("Video als V1 … V8 angeben")
    if a.nur:
        gewaehlt = set(a.nur)
    else:
        gewaehlt = {n for n, *_ in SCHRITTE if a.ab <= n <= a.bis}

    if 2 in gewaehlt and not os.environ.get("FISH_KEY"):
        raise SystemExit("FISH_KEY ist nicht gesetzt — Schritt 2 braucht ihn.")

    t0 = time.time()
    zeiten = []
    for nr, name, datei, argumente in SCHRITTE:
        if nr not in gewaehlt:
            continue
        cmd = [sys.executable, os.path.join(HIER, datei), a.video] + argumente
        if nr == 1 and a.hook:
            cmd += ["--hook", a.hook]
        if nr == 4 and a.bild:
            cmd += ["--bild", a.bild]
        print(f"\n{'='*66}\nSCHRITT {nr} — {name}\n{'='*66}", flush=True)
        t = time.time()
        r = subprocess.run(cmd)
        zeiten.append((nr, name, time.time() - t, r.returncode))
        if r.returncode != 0:
            print(f"\nSchritt {nr} ({name}) ist mit Code {r.returncode} "
                  f"abgebrochen. Die Pipeline hält hier an.")
            return r.returncode
        if nr == 6:
            for zname, zdatei in ZUSATZ:
                print(f"\n{'-'*66}\n{zname}\n{'-'*66}", flush=True)
                subprocess.run([sys.executable, os.path.join(HIER, zdatei), a.video])

    print(f"\n{'='*66}\nZEITEN\n{'='*66}")
    for nr, name, s, rc in zeiten:
        print(f"  {nr}  {name:12s} {s/60:6.1f} min")
    print(f"     {'gesamt':12s} {(time.time()-t0)/60:6.1f} min")
    return 0


if __name__ == "__main__":
    sys.exit(main())
