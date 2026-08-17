#!/usr/bin/env python3
"""Baut den Testtext fuer die Stimmprobe aus vier Stellen von `skript.md`.

Der Testtext ist kein Skriptauszug am Stueck, sondern eine Montage. Er soll in
rund 200 Woertern vier Dinge gleichzeitig pruefen:

  1. Eroeffnung bis "They were fighting water."  — Tempo im Flieẞtext,
     Direktansprache, und ob die Ein-Satz-Antwort als Antwort klingt.
  2. Duemmer / Pr 31 / Campemoor                 — deutsche Ortsnamen und ein
     Label ohne etablierte Sprechweise.
  3. Widan el-Faras                              — der schwerste Eigenname der
     Liste, arabisch, Betonung auf der zweiten Silbe.
  4. "The wheel is not the parent of the road."  — bekommt eine Pointe
     Betonung?

Jeder Baustein ist **woertlich** aus dem Sprechtext von `skript.md` uebernommen
(nur die Quellen-IDs sind entfernt). Dazwischen stehen drei selbst geschriebene
**Uebergaenge**, die im Skript nicht vorkommen — sie sind unten als solche
ausgewiesen und in `testtext_herkunft.md` Zeile fuer Zeile belegt, damit der
Testtext nicht versehentlich fuer Skriptinhalt gehalten wird.

Zur Auswahl von Baustein 2: Vorgegeben war "der Satz mit Pr 31 und Campemoor".
Der davorstehende Duemmer-Satz ist mitgenommen, aus zwei Gruenden — "One of
them" braucht sein Bezugswort, sonst ist der Satz grammatisch in der Luft, und
Duemmer ist der in `aussprache.md` als **kritisch** markierte Fall (englisch
gelesen klingt er wie *dumber*).
"""
from __future__ import annotations

import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
SKRIPT = HIER.parent.parent / "skript.md"

# Woertliche Bausteine: (Kennung, Absatznummer im Sprechtext, Startmarke, Endmarke)
# Start-/Endmarke sind woertliche Teilstrings; der Ausschnitt laeuft von
# Start bis einschliesslich Ende.
BAUSTEINE = [
    ("Eroeffnung", 1, "Look down the next time", "They were fighting water."),
    ("Duemmer/Pr 31/Campemoor", 6, "Some of the oldest paths", "called the Campemoor."),
    ("Widan el-Faras", 10, "The quarry is called", "laid as pavement."),
    ("Pointe", 8, "The wheel is not the parent", "a guest on it."),
]

# Selbst geschriebene Uebergaenge. Stehen NICHT im Skript.
UEBERGAENGE = [
    "The same answer turns up in northern Germany.",
    "Egypt built for something else entirely.",
    "And in that German bog country, the oldest road beats the oldest wheel "
    "by some two thousand years.",
]

# Ersatzschreibungen fuer die Fassung MIT Aussprachekorrektur.
# Werte identisch mit dem Alias-Lexikon, damit Text- und Lexikonkorrektur
# vergleichbar sind.
ERSATZ = [
    ("Dümmer", "Deemer"),
    ("Pr 31", "P-R thirty-one"),
    ("Campemoor", "Kahm-puh-mohr"),
    ("Widan el-Faras", "wih-Dahn el Fah-rass"),
]


def woerter(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", text))


def absaetze() -> list[str]:
    src = SKRIPT.read_text(encoding="utf-8")
    body = src.split("## Sprechtext", 1)[1].split("---\n\n## Quellen-IDs", 1)[0]
    return [re.sub(r"\s*\[[WL]\d+\]", "", p.strip())
            for p in body.strip().split("\n\n") if p.strip()]


def ausschnitt(absatz: str, start: str, ende: str) -> str:
    i = absatz.index(start)
    j = absatz.index(ende, i) + len(ende)
    return absatz[i:j]


def main() -> None:
    paras = absaetze()
    teile, herkunft = [], []

    for n, (kennung, nr, start, ende) in enumerate(BAUSTEINE):
        stueck = ausschnitt(paras[nr - 1], start, ende)
        teile.append(stueck)
        herkunft.append(("wörtlich", f"{kennung} (Absatz {nr})", stueck))
        if n < len(UEBERGAENGE):
            teile.append(UEBERGAENGE[n])
            herkunft.append(("Übergang", f"nach {kennung}", UEBERGAENGE[n]))

    text = " ".join(teile)
    (HIER / "testtext.txt").write_text(text + "\n", encoding="utf-8")

    korr = text
    for alt, neu in ERSATZ:
        assert alt in korr, f"{alt} fehlt im Testtext"
        korr = korr.replace(alt, neu)
    (HIER / "testtext_korrigiert.txt").write_text(korr + "\n", encoding="utf-8")

    # Herkunftsnachweis
    zeilen = [
        "# Herkunft des Testtexts",
        "",
        "Erzeugt von `testtext_bauen.py`. Nicht von Hand ändern — sonst",
        "stimmen Wortzahl und Messwerte in `messungen.json` nicht mehr.",
        "",
        "| # | Art | Stelle | Wörter | Text |",
        "|---|---|---|---|---|",
    ]
    for i, (art, stelle, stueck) in enumerate(herkunft, 1):
        kurz = stueck if len(stueck) <= 90 else stueck[:87] + "…"
        zeilen.append(f"| {i} | {art} | {stelle} | {woerter(stueck)} | {kurz} |")

    wl = sum(woerter(s) for a, _, s in herkunft if a == "wörtlich")
    wu = sum(woerter(s) for a, _, s in herkunft if a == "Übergang")
    zeilen += [
        "",
        f"**Wörtlich aus `skript.md`: {wl} Wörter · "
        f"Übergänge: {wu} Wörter · gesamt: {woerter(text)} Wörter, "
        f"{len(text)} Zeichen.**",
        "",
        "## Geprüfte Stolperstellen aus `aussprache.md`",
        "",
        "| Eintrag | im Testtext | Art der Prüfung |",
        "|---|---|---|",
        "| **Dümmer** | ja | kritisch — darf nicht wie *dumber* klingen |",
        "| **Campemoor** | ja | deutscher Ortsname, zweites Glied ist *Moor* |",
        "| **Pr 31** | ja | Label: „P-R thirty-one“, Buchstaben einzeln |",
        "| **Widan el-Faras** | ja | schwerster Eigenname, Betonung 2. Silbe |",
        "",
        "Nicht im Testtext, aber im Lexikon abgedeckt: Nebuchadnezzar, Ishtar,",
        "Susa, Sardis, Chaco, Pueblo, Wari, Tiwanaku, Westhay, Shapwick, Pr 7",
        "sowie sämtliche BC-Jahreszahlen.",
    ]
    (HIER / "testtext_herkunft.md").write_text("\n".join(zeilen) + "\n", encoding="utf-8")

    print(f"testtext.txt            {woerter(text):4d} W  {len(text):5d} Z")
    print(f"testtext_korrigiert.txt {woerter(korr):4d} W  {len(korr):5d} Z"
          f"  ({len(ERSATZ)} Ersetzungen)")
    print(f"  davon wörtlich {wl} W, Übergänge {wu} W")


if __name__ == "__main__":
    main()
