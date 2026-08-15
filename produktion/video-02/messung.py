#!/usr/bin/env python3
"""Misst den Sprechtext von Video 2 gegen die harten Vorgaben.

Die Vorgaben stammen aus dem Ink-Axen-Vergleich (siehe Video 1):
  * 1.850-2.050 Woerter
  * mindestens 82 % der Woerter unter 7 Zeichen
  * Du-Ansprache ab Sekunde 0; im ersten Fuenftel mindestens 40
    Anrede-Marker je 1.000 Woerter
  * die Antwort auf die Titelfrage faellt in den ersten 30 Sekunden
    (bei 219 WPM sind das die ersten ~110 Woerter)

Gezaehlt wird am bereinigten Sprechtext: Quellen-IDs entfernt, dann
Wort = alles zwischen Leerraum. Anrede-Marker: you, your, you're, you'll,
you've, yours, yourself (auch you'd; Gross/klein egal).
"""
from __future__ import annotations

import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
WPM = 219

t = (HIER / "skript.md").read_text(encoding="utf-8")
m = re.search(r"^## Sprechtext\s*\n(.*?)^---\s*$", t, re.S | re.M)
roh = m.group(1).strip()
# Quellen-IDs raus, wie vor der Vertonung
rein = re.sub(r"\s*\[(?:[WLA]\d*|A)\]", "", roh)
absaetze = [a.strip() for a in rein.split("\n\n") if a.strip()]
text = " ".join(absaetze)
woerter = text.split()
n = len(woerter)

sek = n / WPM * 60
kurz = sum(1 for w in woerter if len(re.sub(r"[^A-Za-z0-9'\-]", "", w)) < 7)

fuenftel = woerter[: n // 5]
marker_re = re.compile(r"^(you|your|you're|you'll|you've|you'd|yours|yourself)$", re.I)
def marker_zahl(ws):
    return sum(1 for w in ws if marker_re.match(re.sub(r"[^A-Za-z']", "", w)))
m1 = marker_zahl(fuenftel)
m_ges = marker_zahl(woerter)

# Antwortposition: "with a triangle"
antwort = None
for i in range(n - 2):
    if (woerter[i].lower().strip(".,:;") == "with"
            and woerter[i+1].lower() == "a"
            and woerter[i+2].lower().strip(".,:;") == "triangle"):
        antwort = i + 3
        break

# Behauptungen mit Zahlen/Daten: Saetze mit Ziffer oder ausgeschriebener
# Grosszahl; hat der Satz im ROHTEXT eine Quellen-ID?
saetze_roh = re.split(r"(?<=[.!?])\s+", " ".join(roh.split()))
hart = beleg = ohne = 0
ohne_liste = []
zahlwort = re.compile(r"\d|\b(hundred|thousand|million|billion|trillion|twenty|thirty|forty|fifty|sixty|seventy|ninety)\b", re.I)
for s in saetze_roh:
    kern = re.sub(r"\[(?:[WLA]\d*|A)\]", "", s)
    if zahlwort.search(kern):
        hart += 1
        if re.search(r"\[(?:[WLA]\d*|A)\]", s):
            beleg += 1
        else:
            ohne += 1
            ohne_liste.append(kern.strip()[:90])

print(f"Woerter: {n}  (Ziel 1.850-2.050)")
print(f"Laufzeit bei {WPM} WPM: {int(sek//60)}:{sek%60:04.1f}")
print(f"Woerter unter 7 Zeichen: {kurz} = {kurz/n*100:.1f} %  (Ziel >= 82 %)")
print(f"Anrede-Marker erstes Fuenftel ({len(fuenftel)} Woerter): {m1} "
      f"= {m1/len(fuenftel)*1000:.1f} je 1.000  (Ziel >= 40)")
print(f"Anrede-Marker gesamt: {m_ges} = {m_ges/n*1000:.1f} je 1.000")
if antwort:
    print(f"Antwort ('with a triangle') endet bei Wort {antwort} "
          f"= {antwort/WPM*60:.1f} s  (Ziel < 30 s)")
print(f"Saetze mit harten Zahlen: {hart} · mit Quellen-ID {beleg} · ohne {ohne}")
for s in ohne_liste:
    print(f"   OHNE: {s}")
