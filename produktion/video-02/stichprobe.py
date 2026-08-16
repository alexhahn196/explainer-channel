#!/usr/bin/env python3
"""Prompts fuer den Stichprobenlauf zu Video 2.

Fuenf Motive, ausgewaehlt nach Risiko:

M06, M15, M87  die drei, an denen die Textlosigkeit am ehesten scheitert
M52            die Leiter — sie kehrt in sieben Motiven wieder (M52, M66,
               M67, M68, M84, M86, M91). Traegt das Sinnbild nicht, faellt
               ein Siebtel des Plans, nicht ein Bild. Ausserdem steht sie
               als einziges Schema in einem Sternhimmel und ist damit der
               Grenzfall zwischen Schema und Weltbild.
M55            das einzige Weltbild der Stichprobe, und zugleich das
               schwerste: Ganzfigur, Innenraum, Licht VON UNTEN, epochen-
               gebunden, Epochenfigur ohne Portraitaehnlichkeit. Ohne ein
               Weltbild laesst sich die Kanalfrage gar nicht pruefen.

Die Bausteine kommen aus produktion/video-01/bildplan.py, damit die
Stichprobe dieselbe Machart traegt wie Video 1 in seiner neuen Farbfassung.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib

HIER = pathlib.Path(__file__).resolve().parent
V1 = HIER.parent / "video-01" / "bildplan.py"

spec = importlib.util.spec_from_file_location("bildplan", V1)
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

# Video 2 zeichnet abstrakter als Video 1. Dort waren die Schemata
# Querschnitte und Karten — Dinge mit einer Gestalt. Hier sind es Balken,
# Punkte und Pfeile. Der DIAGRAMM-Block aus Video 1 verbietet Licht und
# Perspektive, sagt aber nicht, WORAUS ein Diagramm besteht; ohne das baut
# das Modell aus einem "Fehlerbalken" eine Szene mit Boden und Wand.
SCHEMA_HART = (
    " DIAGRAM VOCABULARY: this picture is built only from simple graphic "
    "elements - straight lines, bars, dots, circles, arrows, wedges and plain "
    "silhouettes - arranged on one plain even field. There is no room, no "
    "ground plane, no table, no wall, no horizon and no floor for anything to "
    "stand on; nothing casts a shadow and nothing recedes into depth. Every "
    "element sits flat on the same background."
)

# Das Negativ aus Video 1 verbietet Text schon. Bei Diagrammen ist die
# Versuchung groesser: Achsen wollen Zahlen, Balken wollen Beschriftung.
# Darum ein zweites Mal und ausdruecklich.
SCHEMA_TEXTFREI = (
    " ABSOLUTELY NO WRITING: no numbers, no digits, no tick marks with values, "
    "no axis labels, no legend, no caption, no letters of any alphabet "
    "anywhere in the picture. The diagram must carry its meaning by shape, "
    "size and position alone."
)

# Video 1 kannte nur stehende Einzelfiguren; FRAMING_EINZEL verlangt darum
# beide Fuesse im Bild. Video 2 hat drei sitzende Figuren (M34 am Okular,
# M55 am Leuchttisch, M69 am Okular) — dort kaempft die Fussforderung gegen
# den Tisch, an dem die Figur sitzt. Eigener Fall statt Kompromiss.
FRAMING_SITZEND = (
    "FRAMING: a single person, alone in the frame, seated at their work and "
    "shown from the knees or the waist up; no second figure, no mirrored "
    "duplicate. The feet need not be visible - the figure is seated and the "
    "table or instrument covers the lower body. Head, both shoulders, both "
    "arms and both hands are inside the picture and are drawn. Sober, "
    "restrained, documentary - never cute."
)

MOTIVE = {
 "M06": dict(
   schema=True,
   szene="the parallax triangle. The Sun sits at the centre; around it the "
         "Earth's orbit is drawn as one flat ellipse seen at a slight angle. "
         "The Earth appears twice, at two opposite points of that ellipse. "
         "From each of the two Earths one long dashed sight line runs up to "
         "the SAME single near star, and the two lines meet at that star, "
         "enclosing a narrow wedge which is drawn as a filled sliver at the "
         "meeting point. Behind and around the near star lies a field of "
         "distant stars. The near star is drawn clearly larger and brighter "
         "than every star of that background field, so that the wedge "
         "unmistakably belongs to it and not to the field"),
 "M15": dict(
   schema=True,
   szene="two stars shown side by side above one common horizontal base line. "
         "At each end of the base line sits a small marker for a viewpoint, "
         "and from both markers a thin sight line runs up to each star. The "
         "left star sits low and near, and carries a WIDE double-headed "
         "horizontal arrow showing a large sideways shift. The right star "
         "sits high and far, and carries a VERY SMALL double-headed "
         "horizontal arrow showing a tiny shift. The two arrows differ "
         "grossly in length; that difference is the whole point of the "
         "picture"),
 "M87": dict(
   schema=True,
   szene="seven horizontal error bars stacked one above the other, each bar a "
         "plain straight line with a short upright cap at both ends and a dot "
         "at its middle, all measured against one common vertical line at the "
         "left. At the left end of every bar sits one small symbol. The "
         "topmost bar carries a finely speckled round disc. The next three "
         "bars each carry a large red circular star. The lowest three bars "
         "each carry a small lamp with short radiating lines around it. The "
         "topmost four bars - the speckled disc and the three red stars - lie "
         "at the same height range and overlap one another horizontally. The "
         "lowest three bars, the ones with the lamps, sit clearly further to "
         "the right and their left caps do not reach the right caps of the "
         "group above, leaving a visible gap between the two groups"),
 "M52": dict(
   schema=True,
   szene="a ladder leaning steeply upwards into a field of stars. Its lowest "
         "rung rests on a small triangle which stands alone at the foot of "
         "the ladder. The rungs grow longer towards the top, and the top of "
         "the ladder fades away among the stars. Nothing else in the picture"),
 "M55": dict(
   schema=False,
   framing="sitzend",
   licht="a light table whose glass top glows from below, lighting the woman's "
         "face and hands from underneath",
   epoche="the Harvard College Observatory in Massachusetts around 1910",
   flora="This is an interior: wood panelling and tall sash windows, no "
         "vegetation of any kind.",
   szene="one adult woman in a dark high-necked blouse and a long skirt sits "
         "alone at a light table, her gaze lowered onto a large glass "
         "photographic plate lying on the glowing glass, a magnifying lens in "
         "one hand. Stacks of further glass plates are piled around her on "
         "the table"),
}


def prompt(mid: str) -> str:
    m = MOTIVE[mid]
    if m["schema"]:
        p = (bp.MACHART + bp.FRAMING_OHNE + bp.DIAGRAMM + SCHEMA_HART
             + bp.FARBEN_SCHEMA + SCHEMA_TEXTFREI)
    else:
        rahmen = (FRAMING_SITZEND if m.get("framing") == "sitzend"
                  else bp.FRAMING_EINZEL)
        p = bp.MACHART + rahmen
        if m.get("framing") != "sitzend":
            p += bp.KEIN_ANSCHNITT
        p += bp.Z3_SICHTBAR.format(quelle=m["licht"])
        p += bp.FARBEN
        p += (f" PERIOD AND PLACE: {m['epoche']}. Clothing, tools, "
              "architecture and vegetation all belong to that period and "
              "place and to no other. " + m["flora"])
        p += bp.FLAECHE_HART
        p += " " + bp.FIGUR
    return p + " SCENE: " + m["szene"].rstrip(".") + "." + bp.NEGATIV


if __name__ == "__main__":
    aus = {mid: prompt(mid) for mid in MOTIVE}
    (HIER / "stichprobe-prompts.json").write_text(
        json.dumps(aus, indent=1, ensure_ascii=False), encoding="utf-8")
    for mid, p in aus.items():
        print(f"=== {mid} ({len(p)} Zeichen)")
        print(p)
        print()
