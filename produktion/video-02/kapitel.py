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
    1:  "Pick a star. How far away is it?",
    3:  "The triangle you already own",
    5:  "Two spots, six months apart",
    6:  "Koenigsberg, 1838",
    8:  "Why it took 295 years",
    9:  "Three men, three cities, three stars",
    13: "Sixty distances by 1900 - then satellites",
    # Absatz 14 ist eine Bruecke von 9,5 s und liegt damit 9,941 s vor
    # Absatz 15 — unter der Zehn-Sekunden-Grenze von YouTube. Nur einer der
    # beiden kann eine Marke tragen. Sie sitzt auf 14, weil dort die Leiter
    # eingefuehrt wird, und heisst nach der Szene, die unmittelbar folgt.
    14: "The ladder, and Harvard 1908",
    17: "The rung with no scale",
    19: "What you now own",
    20: "The ladder has snapped twice",
    22: "The Pleiades, measured wrong",
    23: "The third fight, still open",
    24: "How well you know it",
}


def mmss(s: float) -> str:
    return f"{int(s // 60):02d}:{int(s % 60):02d}"


def main() -> None:
    plan = json.loads((HIER / "ton" / "_zeitplan.json").read_text(encoding="utf-8"))
    zeilen, vorher = [], None
    for e in plan:
        # Video 2 hat 24 Absaetze, aber nicht jeder ist ein Kapitel: bei 24
        # Marken auf zehn Minuten waere die Leiste unlesbar. Ueberschrieben
        # sind darum nur die Absaetze, an denen der Text wirklich umschlaegt;
        # die uebrigen laufen im vorigen Kapitel mit.
        if e["absatz"] not in UEBERSCHRIFT:
            continue
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
