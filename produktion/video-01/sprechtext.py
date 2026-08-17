#!/usr/bin/env python3
"""Baut den Sprechtext fuer die Vertonung aus skript.md.

Drei Schritte, alle deterministisch und nachpruefbar:
  1. den Abschnitt "## Sprechtext" herausloesen
  2. die Quellen-IDs [W1], [L18] … entfernen — sie sind laut skript.md
     ausdruecklich nicht Teil des Sprechtexts
  3. die Aussprachekorrekturen aus aussprache.md einsetzen

Die Schreibweise der Korrekturen ist nicht frei gewaehlt, sondern die aus
stimmproben/elevenlabs/testtext_korrigiert.txt — die Fassung, deren Wirkung im
Hoerbericht mit zwei Spracherkennern gemessen wurde. Wo ein Name im Testtext
nicht vorkam, folgt die Schreibweise dem Respelling-Muster derselben Datei
(betonte Silbe gross, Silben mit Bindestrich).

skript.md selbst wird nicht angefasst: die Ausspracheliste verlangt
ausdruecklich, die Schreibung dort nicht phonetisch zu verfaelschen, sonst
bricht der Abgleich mit faktencheck.py.
"""
from __future__ import annotations

import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent

# ---------------------------------------------------------------- Korrekturen
# Gemessen wirksam (hoerbericht.md, Befund 4) — Schreibweise unveraendert
# aus testtext_korrigiert.txt uebernommen.
GEMESSEN = [
    ("Dümmer",         "Deemer"),
    ("Campemoor",      "Kahm-puh-mohr"),
    ("Widan el-Faras", "wih-Dahn el Fah-rass"),
    ("Pr 31",          "P-R thirty-one"),
]

# Im Testtext nicht enthalten, daher ungeprueft — Schreibweise nach dem
# Respelling der Ausspracheliste, im Muster der gemessenen Faelle.
UNGEPRUEFT = [
    ("Nebuchadnezzar", "neb-yoo-kad-Nezzer"),
    ("Tiwanaku",       "tee-wah-Nah-koo"),
    ("Pueblo",         "Pweb-loh"),
    ("Chaco",          "Chah-koh"),
    ("Sardis",         "Sar-diss"),
    ("Susa",           "Soo-suh"),
    ("Westhay",        "West-hay"),
    ("Shapwick",       "Shap-wick"),
    ("Wari",           "Wah-ree"),
    ("Ishtar",         "Ish-tar"),
    ("Pr 7",           "P-R seven"),
]

# Zahlen. Die Ausspracheliste schreibt Ziffernpaare vor, nicht
# "three thousand eight hundred and seven".
ZAHLEN = [
    ("3807 BC", "thirty-eight-oh-seven B C"),
    ("or 3806", "or thirty-eight-oh-six"),
    ("3838 BC", "thirty-eight-thirty-eight B C"),
    ("569 BC",  "five-sixty-nine B C"),
    ("312 BC",  "three-twelve B C"),
    ("the 25th century BC", "the twenty-fifth century B C"),
    ("50.5 kilometres", "fifty point five kilometres"),
    ("1,800 metres", "eighteen hundred metres"),
]


def sprechtext_roh() -> str:
    """Der Abschnitt zwischen '## Sprechtext' und dem naechsten '---'."""
    t = (HIER / "skript.md").read_text(encoding="utf-8")
    m = re.search(r"^## Sprechtext\s*\n(.*?)^---\s*$", t, re.S | re.M)
    if not m:
        raise SystemExit("Abschnitt '## Sprechtext' nicht gefunden")
    absaetze = [a.strip() for a in m.group(1).strip().split("\n\n") if a.strip()]
    return "\n\n".join(absaetze)


def ohne_quellen(t: str) -> str:
    t = re.sub(r"\s*\[(?:[WL]\d+)\]", "", t)
    # Leerzeichen vor Satzzeichen, die durch das Entfernen entstehen koennen
    return re.sub(r"\s+([.,;:?!])", r"\1", t)


def korrigiere(t: str) -> tuple[str, list[tuple[str, str, int]]]:
    protokoll = []
    for alt, neu in ZAHLEN + GEMESSEN + UNGEPRUEFT:
        n = t.count(alt)
        if n:
            t = t.replace(alt, neu)
        protokoll.append((alt, neu, n))
    return t, protokoll


def main() -> None:
    roh = ohne_quellen(sprechtext_roh())
    (HIER / "sprechtext-roh.txt").write_text(roh + "\n", encoding="utf-8")

    fertig, protokoll = korrigiere(roh)
    (HIER / "sprechtext.txt").write_text(fertig + "\n", encoding="utf-8")

    woerter = len(fertig.split())
    absaetze = len(fertig.split("\n\n"))
    sek = woerter / 214.3 * 60
    rest = len(re.findall(r"\[[WL]\d+\]", fertig))
    print(f"Sprechtext  {len(fertig)} Zeichen · {woerter} Woerter · {absaetze} Absaetze")
    print(f"Laufzeit bei 214,3 WPM: {int(sek // 60)}:{sek % 60:04.1f}")
    print(f"Quellen-IDs uebrig: {rest}")
    print("\nErsetzungen:")
    for alt, neu, n in protokoll:
        marke = "  " if n else "!!"
        print(f"  {marke} {n}x  {alt!r} -> {neu!r}")
    fehlt = [a for a, _, n in protokoll if not n]
    if fehlt:
        print(f"\nNICHT GEFUNDEN ({len(fehlt)}): {fehlt}")


if __name__ == "__main__":
    main()
