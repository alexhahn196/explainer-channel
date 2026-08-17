#!/usr/bin/env python3
"""Prueft, ob die Neumontage Laufzeit und Verankerung unveraendert laesst.

Die Frage ist nicht, ob das Video ungefaehr gleich lang ist, sondern ob
jede einzelne Einstellung noch an derselben Stelle der Tonspur steht. Bei
159 Einstellungen gegen eine feste Spur summiert sich sonst ein Fehler von
einem Frame je Schnitt zu ueber fuenf Sekunden am Ende.

Geprueft wird an den gerenderten Teilen in _bau/, nicht am Plan - ein Plan
kann stimmen und das Rendern trotzdem danebenliegen.

Aufruf:
    python3 produktion/video-02/pruefe_verankerung.py
    python3 produktion/video-02/pruefe_verankerung.py --video video-02.mp4
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

HIER = pathlib.Path(__file__).resolve().parent
BAU = HIER / "_bau"
FPS = 30
ABSPANN_S = 1.4
FFPROBE = shutil.which("ffprobe") or "ffprobe"


def frames(pfad):
    a = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames,width,height",
         "-of", "default=nw=1:nk=1", str(pfad)],
        capture_output=True, text=True, check=True).stdout.split()
    return int(a[2]), int(a[0]), int(a[1])


def main():
    plan = json.loads((HIER / "schnittplan.json").read_text(encoding="utf-8"))
    soll_gesamt = sum(s["dauer_s"] for s in plan) + ABSPANN_S

    print(f"{'Nr':>4} {'Motiv':6} {'Soll s':>8} {'Ist s':>8} "
          f"{'Abw ms':>7} {'Anker soll':>11} {'Anker ist':>10} {'Drift ms':>9}")
    lauf = 0.0
    schlimmste_dauer = schlimmster_anker = 0.0
    fehler = []
    formate = set()
    for i, s in enumerate(plan):
        teil = BAU / f"{s['nr']:03d}.mp4"
        if not teil.exists():
            fehler.append(f"Einstellung {s['nr']}: Teil fehlt")
            continue
        n, b, h = frames(teil)
        formate.add((b, h))
        soll = s["dauer_s"] + (ABSPANN_S if i == len(plan) - 1 else 0.0)
        ist = n / FPS
        abw = (ist - soll) * 1000
        drift = (lauf - s["start_s"]) * 1000
        schlimmste_dauer = max(schlimmste_dauer, abs(abw))
        schlimmster_anker = max(schlimmster_anker, abs(drift))
        if i < 3 or i >= len(plan) - 3 or abs(drift) > 100:
            print(f"{s['nr']:>4} {s['motiv']:6} {soll:8.3f} {ist:8.3f} "
                  f"{abw:+7.1f} {s['start_s']:11.3f} {lauf:10.3f} {drift:+9.1f}")
        lauf += ist

    print()
    print(f"  Einstellungen                {len(plan)}")
    print(f"  Format                       {formate}")
    print(f"  Laufzeit Soll                {soll_gesamt:.3f} s = "
          f"{int(soll_gesamt//60)}:{soll_gesamt%60:04.1f}")
    print(f"  Laufzeit aus den Teilen      {lauf:.3f} s = "
          f"{int(lauf//60)}:{lauf%60:04.1f}")
    print(f"  Abweichung gesamt            {(lauf-soll_gesamt)*1000:+.1f} ms")
    print(f"  groesste Einzelabweichung    {schlimmste_dauer:.1f} ms "
          f"({schlimmste_dauer/1000*FPS:.2f} Frames)")
    print(f"  groesster Ankerversatz       {schlimmster_anker:.1f} ms "
          f"({schlimmster_anker/1000*FPS:.2f} Frames)")

    if "--video" in sys.argv:
        v = HIER / sys.argv[sys.argv.index("--video") + 1]
        a = subprocess.run(
            [FFPROBE, "-v", "error", "-show_entries",
             "format=duration", "-of", "default=nw=1:nk=1", str(v)],
            capture_output=True, text=True, check=True).stdout.strip()
        print(f"  fertiges Video              {float(a):.3f} s")

    if fehler:
        print("\nFEHLER:")
        for f in fehler:
            print("  " + f)

    # Das eigentliche Kriterium. Der Ankerversatz gegen den PLAN darf nicht
    # null sein und soll es auch nicht: jede Einstellung wird auf ganze
    # Frames gerundet, und die Reste summieren sich als Zufallsweg auf ein
    # bis zwei Frames. Die alte Montage rundet mit derselben Formel, hat
    # also denselben Versatz. Unveraendert heisst deshalb nicht "kein
    # Versatz gegen den Plan", sondern "je Einstellung exakt dieselbe
    # Framezahl wie vorher" - und die ist durch round(dauer*fps) bestimmt.
    abweichler = []
    for i, s in enumerate(plan):
        teil = BAU / f"{s['nr']:03d}.mp4"
        if not teil.exists():
            continue
        soll_n = max(2, round((s["dauer_s"]
                               + (ABSPANN_S if i == len(plan) - 1 else 0.0))
                              * FPS))
        if frames(teil)[0] != soll_n:
            abweichler.append((s["nr"], frames(teil)[0], soll_n))
    print(f"  Framezahl je Einstellung     "
          f"{len(plan) - len(abweichler)}/{len(plan)} exakt wie gefordert")
    for nr, ist, soll in abweichler[:10]:
        print(f"    Einstellung {nr}: {ist} statt {soll} Frames")

    ok = not fehler and not abweichler
    print(f"\n  {'BESTANDEN' if ok else 'DURCHGEFALLEN'}")
    print("  Der Ankerversatz gegen den Plan oben ist Rundung auf ganze "
          "Frames,\n  kein Fehler - die alte Montage rundet genauso. "
          "Massgeblich ist die\n  Framezahl je Einstellung.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
