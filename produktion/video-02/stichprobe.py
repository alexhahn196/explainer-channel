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
    "element sits flat on the same background. Anything that exists as a real "
    "object in the world - a ladder, a lamp, a coin, a telescope - is drawn "
    "here as a flat symbol of that object seen straight from the side, not as "
    "a picture of the thing itself: one flat fill per part, plain straight "
    "bars, no wood grain, no metal sheen, no rounded or cylindrical parts, no "
    "vanishing point and no foreshortening. It reads as a printed symbol, not "
    "as an illustration of an object."
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

MOTIVE = {
 "M06": dict(
   schema=True,
   szene="the parallax triangle, drawn as ink on pale paper. The Sun sits at "
         "the centre as a plain circle; around it the Earth's orbit is one "
         "flat ellipse. The Earth appears twice, at two opposite points of "
         "that ellipse. From each of the two Earths one long dashed sight "
         "line runs up to one single near star above, and the two lines meet "
         "there. Exactly at that meeting point sits an angle marker: a small "
         "filled circular sector, a little pie slice with its point at the "
         "star, spanning the narrow gap between the two lines - the same mark "
         "a geometry drawing uses to label an angle. Both sight lines are "
         "thin dashed lines of the same weight; neither is a beam or a ray of "
         "light, and no glow or shine is drawn anywhere. Around and behind "
         "the near star lie the distant stars, drawn as small dark dots on "
         "the pale ground like a printed star chart. The near star itself is "
         "a clearly larger dark shape, several times the size of any dot of "
         "that field, so the angle marker plainly belongs to it"),
 "M15": dict(
   schema=True,
   szene="two separate cases side by side on pale paper, each showing how "
         "far one star appears to jump. In the left half: the same star drawn "
         "twice, once well to the left and once well to the right, with a "
         "long double-headed horizontal arrow running between the two "
         "positions and touching both. In the right half: another star, also "
         "drawn twice, but its two positions sit almost on top of one "
         "another, with a very short double-headed horizontal arrow between "
         "them, only a small fraction of the length of the first arrow. All "
         "four stars are dark shapes of exactly the same size and sit at the "
         "same height, so the only difference between the left case and the "
         "right case is how far apart the two positions lie. There are no "
         "sight lines, no base line, no viewpoints, no triangle and no other "
         "element of any kind in the picture"),
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
   szene="a ladder drawn as a flat symbol on pale paper, standing upright "
         "and seen straight from the side. The ladder is shaped like a long "
         "narrow wedge that opens towards the top: its two rails are straight "
         "bars that start together at a single point at the very bottom and "
         "spread steadily apart as they rise, so the ladder is at its "
         "narrowest at the foot and at its widest at the top. Because of "
         "that, each rung is longer than the rung below it - the lowest rung "
         "is a short stub and the topmost rung is several times as long. "
         "Directly below the ladder stands one large triangle resting on its "
         "own horizontal base with its point aimed straight up, and the "
         "single bottom point of the ladder sits exactly on that point of the "
         "triangle, the two touching tip to tip. The triangle is wide and "
         "flat, plainly the same triangle as in the parallax drawing, and it "
         "is large enough to read as its own shape. Small dark dots for stars "
         "lie scattered around the upper, wider end of the ladder in the "
         "manner of a printed star chart. Nothing else in the picture"),
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
    # Versalien in der Bildbeschreibung landen als Schriftzug im Bild —
    # das war der Fehlschlag von M15 im ersten Lauf.
    bp.pruefe_szene(mid, m["szene"])
    if m["schema"]:
        p = (bp.MACHART + bp.FRAMING_OHNE + bp.DIAGRAMM + SCHEMA_HART
             + bp.FARBEN_SCHEMA + SCHEMA_TEXTFREI)
    else:
        rahmen = (bp.FRAMING_SITZEND if m.get("framing") == "sitzend"
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
