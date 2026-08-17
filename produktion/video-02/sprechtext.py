#!/usr/bin/env python3
"""Baut den Sprechtext fuer die Vertonung aus skript.md.

Vier Schritte, alle deterministisch und nachpruefbar:
  1. den Abschnitt "## Sprechtext" herausloesen
  2. die Quellen-IDs [W1], [L4], [A] entfernen — sie sind laut skript.md
     ausdruecklich nicht Teil des Sprechtexts
  3. die Aussprachekorrekturen aus aussprache.md einsetzen
  4. pruefen, dass keine Quellen-ID und kein Sonderzeichen uebrig ist

skript.md selbst wird nicht angefasst. Die Ausspracheliste verlangt
ausdruecklich, die Schreibung dort nicht phonetisch zu verfaelschen, sonst
bricht der Abgleich mit den Quellen.

Unterschied zu Video 1: dort waren vier der Korrekturen mit zwei
Spracherkennern GEMESSEN (hoerbericht.md). Hier ist keine gemessen — die
Schreibweisen folgen dem Muster der gemessenen Faelle, sind aber selbst
ungeprueft. Das steht so auch in aussprache.md und muss in der QA
nachgehoert werden.

Aufruf:  python3 sprechtext.py
"""
from __future__ import annotations

import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent

# Gemessenes Tempo der gewaehlten Stimme (ElevenLabs Eric, Lauf A aus
# produktion/video-01/stimmproben/elevenlabs/README.md).
WPM = 214.3

# --------------------------------------------------------------- Eigennamen --
# Reihenfolge zaehlt: laengere Formen zuerst, sonst frisst die kuerzere
# Ersetzung die laengere an ("Leavitt" vor "Miss Leavitt" wuerde
# "Miss LEV-it" nie erreichen, weil "Leavitt" schon ersetzt waere — hier
# umgekehrt sortiert, damit das nicht passiert).
NAMEN = [
    ("Cepheids", "SEF-ee-ids"),
    ("Cepheid", "SEF-ee-id"),
    ("Königsberg", "Koenigsberg"),
    ("Hipparcos", "hip-AR-koss"),
    ("Pleiades", "PLY-uh-deez"),
    ("Magellanic", "maj-uh-LAN-ik"),
    ("Alpha Centauri", "AL-fuh sen-TOR-ee"),
    ("61 Cygni", "sixty-one SIG-nye"),
    ("Leavitt", "LEV-it"),
    ("Dorpat", "DOR-pat"),
    ("Planck", "plahnk"),
    ("SH0ES", "shoes"),
    ("Gaia", "GUY-uh"),
    ("Vega", "VEE-guh"),
]

# ------------------------------------------------------------------ Zahlen --
# Nur die Faelle, die ein TTS erfahrungsgemaess falsch oder mehrdeutig
# liest. Die uebrigen Jahreszahlen bleiben stehen und werden in der QA
# gegengehoert — eine Ersetzung, die nicht noetig ist, kann selbst schaden.
ZAHLEN = [
    ("In 1543", "In fifteen forty-three"),
    ("around 1700", "around seventeen hundred"),
    ("0.125 arcseconds", "zero point one two five arcseconds"),
    ("the modern 0.129", "the modern zero point one two nine"),
    ("reads 67.4", "reads sixty-seven point four"),
    ("reads 73.0", "reads seventy-three point oh"),
    ("67.8 to 70.4", "sixty-seven point eight to seventy point four"),
    ("118,000 stars", "a hundred and eighteen thousand stars"),
    ("759,000 kilometres", "seven hundred and fifty-nine thousand kilometres"),
    ("87,000 light-years", "eighty-seven thousand light-years"),
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
    """Entfernt [W1], [L4], [A] und die Leerzeichen, die dabei entstehen."""
    t = re.sub(r"\s*\[(?:[WL]\d+|A)\]", "", t)
    t = re.sub(r"\s+([.,;:?!])", r"\1", t)
    return re.sub(r"[ \t]{2,}", " ", t)


def korrigiere(t: str) -> tuple[str, list[tuple[str, str, int]]]:
    protokoll = []
    for alt, neu in ZAHLEN + NAMEN:
        n = t.count(alt)
        if n:
            t = t.replace(alt, neu)
        protokoll.append((alt, neu, n))
    return t, protokoll


def pruefe(t: str) -> None:
    """Bricht ab, wenn etwas uebrig ist, das nicht gesprochen werden kann."""
    rest = re.findall(r"\[[^\]]*\]|\([^)]*https[^)]*\)", t)
    if rest:
        raise SystemExit(f"Nicht sprechbare Reste im Sprechtext: {rest[:5]}")
    exoten = sorted(set(re.findall(r"[^\x00-\x7F]", t)))
    erlaubt = {"—", "„", "“", "’", "–"}
    schlimm = [z for z in exoten if z not in erlaubt]
    if schlimm:
        raise SystemExit(f"Zeichen ausserhalb ASCII im Sprechtext: {schlimm}")


def main() -> None:
    roh = ohne_quellen(sprechtext_roh())
    (HIER / "sprechtext-roh.txt").write_text(roh + "\n", encoding="utf-8")

    fertig, protokoll = korrigiere(roh)
    pruefe(fertig)
    (HIER / "sprechtext.txt").write_text(fertig + "\n", encoding="utf-8")

    woerter = len(fertig.split())
    absaetze = len(fertig.split("\n\n"))
    sek = woerter / WPM * 60
    print(f"Sprechtext  {len(fertig)} Zeichen · {woerter} Wörter · "
          f"{absaetze} Absätze")
    print(f"Laufzeit bei {WPM} WPM: {int(sek // 60)}:{sek % 60:04.1f}")
    print(f"Szenenplan verlangt: 9:20,0")
    print("\nErsetzungen:")
    for alt, neu, n in protokoll:
        marke = "  " if n else "!!"
        print(f"  {marke} {n}x  {alt!r} -> {neu!r}")
    fehlt = [a for a, _, n in protokoll if not n]
    if fehlt:
        raise SystemExit(f"\nNICHT GEFUNDEN ({len(fehlt)}): {fehlt}")
    print("\nPrüfung bestanden: keine Quellen-IDs, keine Fremdzeichen.")


if __name__ == "__main__":
    main()
