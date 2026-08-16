#!/usr/bin/env python3
"""Misst zwei Fassungen derselben Stelle gegeneinander.

Anlass: Tonprobe vom 16.08.2026. Der bestehende Anfang von Video 2 gegen
eine Neufassung in der Schreibart von Unknown Frequencies. Gemessen wird,
was der Auftrag als Vorgabe nennt:

  Anrede-Marker je 1.000 Woerter   Vorgabe 74,7
  Satzlaenge, Median               Vorgabe 7
  epistemische Marker              Vorgabe nahe null
  Fragezeichen                     sparsam
  benannte Personen                sparsam

Anrede-Marker wie in messung.py, damit die Zahlen vergleichbar bleiben.
"""
from __future__ import annotations

import pathlib
import re
import statistics

HIER = pathlib.Path(__file__).resolve().parent

ANREDE = re.compile(
    r"^(you|your|you're|you'll|you've|you'd|yours|yourself)$", re.I)

# Woerter, die eine Aussage abschwaechen oder auf Distanz halten. Ohne die
# blanken Modalverben (could, would, may) — die stehen im Englischen zu oft
# rein grammatisch und wuerden die Zahl unbrauchbar machen.
EPISTEMISCH = {
    "about", "roughly", "around", "nearly", "almost", "approximately",
    "apparently", "seemingly", "presumably", "probably", "possibly",
    "perhaps", "maybe", "arguably", "likely", "reportedly", "supposedly",
    "estimated", "estimates", "suggests", "suggest", "indicates",
    "seems", "seem", "appears", "appear", "thought", "said",
    "generally", "usually", "mostly", "largely", "often", "tends",
    "somewhat", "fairly", "rather", "quite", "sort", "kind",
}
# Mehrwortige Absicherungen
EPISTEMISCH_PHRASEN = [
    "give or take", "or so", "more or less", "in the region of",
    "on paper", "as far as we know", "we think", "it is thought",
    "the story handed down", "for want of",
]

PERSONEN = ("Copernicus", "Tycho", "Brahe", "Bessel", "Henderson", "Struve",
            "Piazzi", "Leavitt", "Henrietta", "Hertzsprung", "Ejnar",
            "Hubble", "Baade", "Sandage", "Freedman", "Riess", "Walter",
            "Edwin", "Thomas", "Wilhelm", "Giuseppe", "Allan")


def messe(text: str) -> dict:
    t = " ".join(text.split())
    woerter = t.split()
    n = len(woerter)

    def blank(w):
        return re.sub(r"[^A-Za-z']", "", w).lower()

    anrede = sum(1 for w in woerter if ANREDE.match(blank(w)))

    saetze = [s for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
    laengen = [len(s.split()) for s in saetze]

    epi = sum(1 for w in woerter if blank(w) in EPISTEMISCH)
    epi += sum(t.lower().count(p) for p in EPISTEMISCH_PHRASEN)

    fragen = t.count("?")
    pers = sum(1 for w in woerter
               if re.sub(r"[^A-Za-z]", "", w) in PERSONEN)
    kurz = sum(1 for w in woerter
               if len(re.sub(r"[^A-Za-z0-9'\-]", "", w)) < 7)

    return dict(
        woerter=n,
        saetze=len(saetze),
        anrede=anrede,
        anrede_1000=anrede / n * 1000,
        median=statistics.median(laengen),
        mittel=sum(laengen) / len(laengen),
        laengster=max(laengen),
        epi=epi,
        epi_1000=epi / n * 1000,
        fragen=fragen,
        personen=pers,
        kurz_pct=kurz / n * 100,
    )


if __name__ == "__main__":
    alt = (HIER / "tonprobe-alt.txt").read_text(encoding="utf-8")
    neu = (HIER / "tonprobe-neu.txt").read_text(encoding="utf-8")
    a, b = messe(alt), messe(neu)
    zeilen = [
        ("Wörter", f'{a["woerter"]}', f'{b["woerter"]}', "—"),
        ("Sätze", f'{a["saetze"]}', f'{b["saetze"]}', "—"),
        ("Anrede-Marker je 1.000", f'{a["anrede_1000"]:.1f}',
         f'{b["anrede_1000"]:.1f}', "74,7"),
        ("Anrede-Marker absolut", f'{a["anrede"]}', f'{b["anrede"]}', "—"),
        ("Satzlänge Median", f'{a["median"]:.1f}', f'{b["median"]:.1f}', "7"),
        ("Satzlänge Mittel", f'{a["mittel"]:.1f}', f'{b["mittel"]:.1f}', "—"),
        ("längster Satz", f'{a["laengster"]}', f'{b["laengster"]}', "—"),
        ("epistemische Marker", f'{a["epi"]}', f'{b["epi"]}', "nahe null"),
        ("epistemische je 1.000", f'{a["epi_1000"]:.1f}',
         f'{b["epi_1000"]:.1f}', "nahe null"),
        ("Fragezeichen", f'{a["fragen"]}', f'{b["fragen"]}', "sparsam"),
        ("benannte Personen", f'{a["personen"]}', f'{b["personen"]}',
         "sparsam"),
        ("Wörter unter 7 Zeichen", f'{a["kurz_pct"]:.1f} %',
         f'{b["kurz_pct"]:.1f} %', "≥ 82 %"),
    ]
    print("| Kennwert | bestehend | neu | Vorgabe |")
    print("|---|---:|---:|---:|")
    for name, x, y, v in zeilen:
        print(f"| {name} | {x} | {y} | {v} |")
