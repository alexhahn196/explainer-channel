#!/usr/bin/env python3
"""Erzeugt die Kapitelmarken fuer die YouTube-Beschreibung.

Die Marken sind an der fertigen Tonspur gemessen, nicht geschaetzt: jeder
Absatz des Sprechtexts hat in `ton/_zeitplan.json` eine echte Startzeit.
Ueberschriften sind je Absatz von Hand gesetzt — sie sind eine
Inhaltsangabe, keine Ableitung.

YouTube verlangt fuer Kapitel: mindestens drei, erste bei 00:00, jedes
mindestens zehn Sekunden lang.
"""
from __future__ import annotations

import json
import pathlib

HIER = pathlib.Path(__file__).resolve().parent

UEBERSCHRIFT = {
    1:  "Roads are older than you think",
    2:  "Standing in a bog",
    3:  "The Sweet Track, 3807 BC",
    4:  "Oak planks, stone axes, no nails",
    5:  "A plank line — and an older one beneath it",
    6:  "550 wooden paths in Lower Saxony",
    7:  "Why there, why then",
    8:  "The thing that had no business being there",
    9:  "So what were roads for?",
    10: "Egypt: a road that served a building site",
    11: "Babylon: a street built as a stage",
    12: "Persia: a road that moved messages",
    13: "Chaco Canyon: the road nobody can explain",
    14: "The Andes: where a road becomes a staircase",
    15: "Rome, in last place",
    16: "The answer that keeps not showing up",
    17: "What a road actually promises",
}


def mmss(s: float) -> str:
    return f"{int(s // 60):02d}:{int(s % 60):02d}"


def main() -> None:
    plan = json.loads((HIER / "ton" / "_zeitplan.json").read_text(encoding="utf-8"))
    zeilen, vorher = [], None
    for e in plan:
        start = e["start_s"]
        if vorher is not None and start - vorher < 10:
            continue                      # YouTube verlangt zehn Sekunden
        zeilen.append(f"{mmss(start)}  {UEBERSCHRIFT[e['absatz']]}")
        vorher = start
    zeilen[0] = "00:00  " + UEBERSCHRIFT[1]
    (HIER / "upload" / "kapitel.txt").write_text("\n".join(zeilen) + "\n",
                                                 encoding="utf-8")
    print("\n".join(zeilen))
    print(f"\n{len(zeilen)} Kapitel · Gesamtlaufzeit "
          f"{mmss(plan[-1]['start_s'] + plan[-1]['dauer_s'])}")


if __name__ == "__main__":
    main()
