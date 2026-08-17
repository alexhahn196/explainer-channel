#!/usr/bin/env python3
"""schema_anteil.py — wie viel Schema steckt im FERTIGEN Video 2?

Der Zusatz vom 16.08.2026 setzt die Grenze bei hoechstens 10 % der Laufzeit
als Schema. Gemessen wurde das bisher nur an einer 87-Sekunden-Tonprobe
(`tonprobe-bilder.py`: Erklaerform 73 %, Erzaehlfassung 10 %). Dieses Skript
rechnet denselben Anteil ueber die **ganze montierte Fassung**: 159
Einstellungen, 66 Motive, 614,8 s — laufzeitgewichtet, nicht nach Motivzahl.

VERFAHREN
  1. Aus bildplan2-prompts.json den Szenenteil je Motiv schneiden. Alle 66
     Prompts tragen denselben Stilvorspann; der Szenenteil beginnt hinter dem
     Marker "SCENE:". Ohne diesen Schnitt zaehlt man den Stilblock mit — dort
     steht z. B. "curved arm" einer Strassenlaterne, was 41 der 66 Motive
     faelschlich als Schema markieren wuerde.
  2. Den Szenenteil gegen eine feste Wortliste pruefen.
  3. Die Motivurteile ueber schnittplan.json auf Sekunden umlegen.

WAS DIESE ZAHL IST UND WAS NICHT
  [abgeleitet, regelbasiert] — nicht [gemessen]. Die Wortliste ist ein
  Urteil darueber, was ein Bild zum Schaubild macht; sie ist nur insofern
  besser als freies Schaetzen, als sie fuer alle 66 Motive gleich angewandt
  und hier vollstaendig aufgeschrieben wird. Die Grenzfaelle stehen unten.

  NICHT moeglich ist der Vergleich beider Skriptfassungen: skript.md und
  skript-erklaerform.md tragen keine Bildannotationen (0 Treffer in der
  Erklaerform), und zur Erklaerform existiert kein Bildplan — sie wurde am
  16.08.2026 abgeloest, bevor einer gebaut wurde. Messbar ist deshalb nur
  die Seite, die produziert wurde.

Aufruf: python3 produktion/video-02/schema_anteil.py
"""
import json
import pathlib
import re
import sys

HIER = pathlib.Path(__file__).resolve().parent

# Ein Bild gilt als Schema, wenn sein Szenenteil mindestens eines dieser
# Wortmuster traegt. Als REGULAERE AUSDRUECKE mit Wortgrenzen, nicht als
# Teilzeichenketten — zwei Fehler, die das kostet, sind unten dokumentiert.
SCHEMA_MUSTER = [
    r"dashed line",   # Sicht-/Hilfslinie, kein Gegenstand der Welt
    r"sight line",
    r"pie slice",     # Winkelflaeche
    r"\btriangles?\b",  # das Parallaxendreieck
    r"\baxis\b",
    r"\barrows?\b",
    r"\bdiagram\b",
    r"\bchart\b",
    r"\bgraph\b",
    r"tick mark",
]

# Die Entfernungsleiter wird als Leiter GEZEICHNET und ist damit Schema; im
# Video kommt aber auch eine echte Holzleiter vor. Ein Wortmuster kann die
# beiden nicht trennen, also stehen sie namentlich hier:
LEITER_ALS_SCHEMA = {"M42", "M54", "M64"}   # Sprossen, gerissene Sprossen, Austausch
LEITER_ALS_GEGENSTAND = {"M66"}             # zwei Haende, ein Nagel, Fuss der Leiter

# ZWEI FEHLER DER ERSTEN FASSUNG, hier festgehalten, weil sie die Zahl um
# vier Prozentpunkte verschoben haben:
#   1. "arrow" ohne Wortgrenze trifft "n-arrow gaps". M23, M32, M33 und M51
#      sind Handschriftszenen (Federkiel, Blatt mit Schraegstrichen) und
#      wurden dadurch faelschlich als Schaubild gezaehlt.
#   2. "ladder" ohne Ausnahmeliste trifft M66, die echte Holzleiter.
#   Mit beiden Fehlern kam 14,7 % heraus, ohne sie 10,8 %.
#
# WEITERE GRENZFAELLE, so entschieden:
#   Glasplatte mit Sternpunkten (M60), Lupe ueber Platte (M45) -> Welt.
#                Gegenstaende auf einem Tisch, keine Zeichnungen.
#   Mann am Mauerquadranten (M20) -> Welt. Mensch bei einer Handlung.
#   Der Stiltext enthaelt "no axis labels" als Verbot; er steht vor dem
#                letzten "SCENE:" und wird daher nicht mitgeschnitten.


def szene(prompt):
    i = prompt.rfind("SCENE:")
    return prompt[i + 6:] if i >= 0 else prompt


def ist_schema(motiv, prompt):
    t = szene(prompt).lower()
    treffer = [m for m in SCHEMA_MUSTER if re.search(m, t)]
    if motiv in LEITER_ALS_SCHEMA:
        treffer.append("Leiter als Denkfigur (Handentscheid)")
    if motiv in LEITER_ALS_GEGENSTAND:
        return []
    return treffer


def main():
    prompts = json.loads((HIER / "bildplan2-prompts.json").read_text())
    plan = json.loads((HIER / "schnittplan.json").read_text())

    ohne_marker = [m for m, p in prompts.items() if "SCENE:" not in p]
    urteil = {m: ist_schema(m, pr) for m, pr in prompts.items()}
    schema_motive = {m for m, h in urteil.items() if h}

    sek_gesamt = sum(s["dauer_s"] for s in plan)
    sek_schema = sum(s["dauer_s"] for s in plan if s["motiv"] in schema_motive)
    n_schema = sum(1 for s in plan if s["motiv"] in schema_motive)

    print(f"Motive ohne SCENE:-Marker: {len(ohne_marker)} "
          f"{ohne_marker if ohne_marker else ''}")
    print(f"Motive als Schema eingestuft: {len(schema_motive)} von {len(prompts)}")
    for m in sorted(schema_motive):
        print(f"   {m}: {', '.join(urteil[m])}")
    print()
    print(f"Einstellungen mit Schema-Motiv: {n_schema} von {len(plan)}")
    print(f"Laufzeit gesamt   {sek_gesamt:8.1f} s")
    print(f"davon Schema      {sek_schema:8.1f} s"
          f"  = {sek_schema / sek_gesamt * 100:.1f} % der Laufzeit")
    print()
    print(f"Grenze aus dem Zusatz vom 16.08.2026: hoechstens 10 %")
    print(f"Urteil: {'eingehalten' if sek_schema/sek_gesamt <= 0.10 else 'UEBERSCHRITTEN'}")
    print()
    print("Zum Vergleich, aus tonprobe-bilder.py ueber 87 s Tonprobe:")
    print("   Erklaerform 73 %   Erzaehlfassung 10 %")
    return 0


if __name__ == "__main__":
    sys.exit(main())
