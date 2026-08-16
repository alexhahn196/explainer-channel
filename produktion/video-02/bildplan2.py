#!/usr/bin/env python3
"""Prompts fuer alle 66 Motive von Video 2 (Erzaehlfassung).

Bausteine aus produktion/video-01/bildplan.py, Motivdaten aus szenenplan.py.
Hier stehen nur die englischen Szenentexte und die zwei Pruefungen, die
sich aus den beiden Stichprobenlaeufen ergeben haben:

  1. VERSALIEN in der Bildbeschreibung -> pruefe_szene() aus bildplan.py.
     Lehre aus Lauf 1 (M15): "a WIDE arrow" wurde als Schriftzug gezeichnet.

  2. RISIKOVOKABULAR. Lehre aus Lauf 2 (M33, M51): das Modell schrieb
     Woerter aus dem Prompt aufs Papier — loops, word, ink, trace. Die
     Beschreibung darf also kein Vokabular fuehren, das man nicht im Bild
     sehen moechte. Das gilt nicht nur fuer Schrift: wer "diagram",
     "chart", "label", "symbol" sagt, bittet um ein beschriftetes Bild.
     Jeder Treffer muss entweder verschwinden oder unter FREIGABE mit
     Begruendung stehen — sonst bricht das Modul ab.

Ein dritter Punkt steht nirgends als Pruefung, weil er sich nicht messen
laesst, und ist trotzdem die wichtigste Lehre: VERBOTE WIRKEN NICHT.
"keine Beschriftung", "ohne ausgeformte Ziffer", "kein Zeichen" hat das
Modell zweimal ignoriert. Beschrieben wird, was DA IST.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent


def _lade(name: str, pfad: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bp = _lade("bildplan", HIER.parent / "video-01" / "bildplan.py")
sp = _lade("szenenplan", HIER / "szenenplan.py")

# --------------------------------------------------------- Risikovokabular --
# Woerter, die ein beschriftetes Bild herbeirufen. Getrennt nach dem Grund,
# warum sie gefaehrlich sind.
RISIKO = {
    "Schrift": ["text", "letter", "letters", "word", "words", "writing",
                "written", "handwriting", "script", "signature", "inscription",
                "caption", "title", "heading", "print", "printed", "type",
                "typeface", "font", "read", "reads", "reading", "spell"],
    "Grafik-Gattung": ["diagram", "chart", "graph", "map", "plot", "table",
                       "schematic", "figure", "illustration", "drawing",
                       "sketch", "blueprint", "plan"],
    "Beschriftung": ["label", "labelled", "labeled", "legend", "key",
                     "annotation", "annotated", "mark", "marked", "marking",
                     "symbol", "sign", "character", "digit", "digits",
                     "number", "numbers", "numeral", "figure", "scale",
                     "tick", "ticks", "graduation", "graduated", "dial",
                     "index", "note", "notes", "notation"],
}

# Freigaben: Treffer, die bleiben duerfen, jeweils mit Grund. Ohne Eintrag
# hier bricht die Pruefung ab.
FREIGABE = {
    # "mark" steht in der Strichformulierung, die im zweiten
    # Stichprobenlauf BESTANDEN hat (M33-v2, M51-v2, M68): dort kam kein
    # einziges Zeichen zurueck. Das Wort ist damit nicht vermutet
    # ungefaehrlich, sondern gemessen. Es zu ersetzen hiesse, die einzige
    # belegt funktionierende Formulierung aufzugeben.
    ("*", "mark"): "gemessen unbedenklich — Strichformulierung aus Lauf 2",
    ("*", "marks"): "dito",
    # "table" ist ein Homonym: gemeint ist der Leuchttisch, nicht die
    # Wertetabelle. In Lauf 2 stand "light table" in vier Prompts (M44,
    # M45, M68 und den Nachlaeufen) — keine Tabelle kam zurueck.
    ("*", "table"): "Homonym, gemessen unbedenklich — 'light table'",
    # M68 ist der EINE Fall, fuer den harte Evidenz vorliegt: genau dieser
    # Wortlaut, "one hand writing with a pencil", kam in Lauf 2 ohne einen
    # einzigen Buchstaben zurueck. Ihn umzuformulieren hiesse, die Evidenz
    # wegzuwerfen und ungeprueft neu anzufangen.
    ("M68", "writing"): "gemessener Wortlaut aus Lauf 2, bestanden",
}


def pruefe_vokabular(mid: str, text: str) -> list[str]:
    """Meldet Risikowoerter im englischen Szenentext."""
    worte = [re.sub(r"[^a-z]", "", w.lower()) for w in text.split()]
    treffer = []
    for gruppe, liste in RISIKO.items():
        for w in liste:
            if (w in worte and (mid, w) not in FREIGABE
                    and ("*", w) not in FREIGABE):
                treffer.append(f"{gruppe}: {w}")
    return treffer


# ---------------------------------------------------------- Szenentexte EN --
# Geschrieben unter der Regel oben: keine Gattungsnamen, keine
# Beschriftungswoerter, keine Verbote. Was auf Papier liegt, wird als
# Strichfolge beschrieben (die Formulierung, die in Lauf 2 bestanden hat).
STRICHE = ("dense horizontal rows of short slanted marks of one constant "
           "height, set in small clusters of three to eight with narrow gaps "
           "between the clusters; every mark is the same length, none is "
           "curved, and no cluster repeats another")

SZENE = {
 "M01": "seen from below, a night sky full of stars, one of them a little "
        "brighter than the rest; along the bottom edge the dark roofline of "
        "a residential street",
 "M02": "one person seen from behind, small in the frame, head tipped back, "
        "standing under the star-filled sky; empty street space all around",
 "M03": "a town square in the evening with several passers-by; most of them "
        "shrug or shake their heads, one points up at the sky",
 "M04": "an outstretched arm with the thumb held up, and behind it a room "
        "wall carrying a small picture hook; the thumb sits to the left of "
        "the hook",
 "M05": "exactly the same view, but the thumb now sits to the right of the "
        "picture hook - crop and camera position unchanged",
 "M06": "a face seen from the side in close view, one eye shut, the open one "
        "looking past the raised thumb",
 "M07": "the same residential street in winter: snow on the roofs, bare "
        "trees, one distinctive paving slab in the pavement at the front",
 "M08": "exactly the same crop in summer: the trees in full leaf, the same "
        "paving slab in the pavement - camera position unchanged",
 "M09": "looking straight down at two shoes standing on a paving slab",
 "M10": "a rectangular patch of the night sky: one brighter star to the left "
        "of two fainter background stars",
 "M11": "the same patch, the same sky - the bright star now sits to the "
        "right of the two background stars",
 "M12": "the parallax triangle in ink on pale paper. The Sun is a plain "
        "circle; around it the Earth's orbit is one flat ellipse. The Earth "
        "appears twice, at two opposite points of that ellipse. From each "
        "Earth a long dashed sight line runs up to one near star above, and "
        "the two lines meet there. In the narrow gap where they meet sits a "
        "small filled pie slice with its point at the star. Both sight lines "
        "are thin dashed lines of the same weight; neither is a beam or a ray "
        "of light, and no glow is drawn anywhere. Around and behind the near "
        "star lie the distant stars as small dark dots on the pale ground. "
        "The near star itself is a clearly larger dark shape, several times "
        "the size of any dot of that field",
 "M13": "a domed classical observatory building at night, bare trees and a "
        "paved approach in front of it",
 "M14": "a close view of a round objective lens sawn exactly through the "
        "middle; one half is slid sideways against the other, and a fine "
        "brass screw sits against it",
 "M15": "one man in the high-collared coat of the early nineteenth century "
        "sits at the eyepiece of a large refracting telescope, turning a fine "
        "brass micrometer screw with his right hand",
 "M16": "looking through an eyepiece: two separate images of one and the "
        "same star side by side in the round field of view",
 "M17": "the same round field of view - the two images now lie exactly on "
        "top of one another, a single point",
 "M18": "a close view of the brass barrel of the micrometer screw, its "
        "surface cut with a row of fine evenly spaced notches, a slim pointer "
        "resting against them; an oil lamp stands beside it",
 "M19": "an open book of the sixteenth century lying on a wooden stand "
        "with a candle beside it. The left page carries a circle of "
        "concentric rings crossed by a few straight lines; the right page "
        "carries an even grey block of fine horizontal strokes in regular "
        "rows",
 "M20": "one bearded man in a doublet and ruff stands at a large brass mural "
        "quadrant, his eye at the sighting vane; there is no telescope "
        "anywhere in the picture",
 "M22": "a close view of the sighting vane of the quadrant, and beside it the "
        "brass arc cut with a row of fine evenly spaced notches and a slim "
        "pointer",
 "M23": "the same man sits at a desk surrounded by measuring "
        "instruments; in front of him a sheet of paper with a quill resting "
        "on its edge, and across the sheet run " + STRICHE,
 "M24": "an extreme close view of one single star as a bare eye sees it: a "
        "small round disc with a soft edge",
 "M25": "the same close view of the same star - the disc is gone, and a tiny "
        "hard point of light remains",
 "M26": "the same man turns away from his quadrant; behind him a globe of "
        "the Earth rests still on a plinth",
 "M27": "a telescope on a wooden tripod, and beside it several men in wigs "
        "and coat-tails bending over a large sheet of paper on which a circle "
        "is crossed by a few straight lines",
 "M28": "one picture divided into three equal upright panels side by side, "
        "each a small night scene. Left panel: a domed observatory building "
        "among bare-branched lime and chestnut trees. Middle panel: a low "
        "white flat-roofed observatory on a ridge with silvery fynbos scrub "
        "and a flat-topped mountain behind it. Right panel: a low wooden "
        "observatory under snow among bare birches. The same field of stars "
        "runs across all three panels above the buildings",
 "M29": "a field of stars holding one inconspicuous double star, with a "
        "short fine trail behind it showing how fast it travels",
 "M30": "a dead straight country road running to the horizon, a two-euro "
        "coin standing upright on the asphalt at the front of the frame, and "
        "at the far end of the road a barely visible dot",
 "M31": "a white flat-roofed observatory building on a ridge, with a "
        "flat-topped mountain and the sea behind it",
 "M32": "one man in the dark coat of the eighteen-thirties sits at a desk, a "
        "sheet of paper in his hand, his eyes lowered onto it; across the "
        "sheet run " + STRICHE,
 "M33": "a close view of one hand laying a sheet of paper into an open desk "
        "drawer. The sheet fills a good part of the frame, and across it run "
        + STRICHE,
 "M34": "the same drawer, the same crop - now closed, with the hand resting "
        "flat on the wood",
 "M35": "a low rendered observatory with timber cladding in a winter "
        "landscape, snow cover, bare trees",
 "M36": "a wide dense field of stars filling the whole frame, with no "
        "foreground",
 "M37": "a satellite with an unfolded solar sail above the curved edge of "
        "the Earth, stars behind it",
 "M38": "a compact satellite with a cylindrical sun shield, far from the "
        "Earth against black space",
 "M39": "the full Moon above the residential street, and in the foreground a "
        "two-euro coin standing sharp on a window sill",
 "M40": "a spiral galaxy seen from an oblique angle, filling the frame - "
        "arms, dust lanes, a dense core",
 "M41": "looking through an eyepiece: on one side a sharp point of light, on "
        "the other a washed-out frayed smudge",
 "M42": "a ladder in ink on pale paper, standing upright and seen straight "
        "from the side. It is shaped like a long narrow wedge that opens "
        "towards the top: its two rails start together at a single point at "
        "the very bottom and spread steadily apart as they rise, so each rung "
        "is longer than the rung below it - the lowest a short stub, the "
        "topmost several times as long. Directly below stands one large "
        "triangle resting on its own horizontal base with its point aimed "
        "straight up, and the single bottom point of the ladder sits exactly "
        "on that point, the two touching tip to tip. Small dark dots for "
        "stars lie scattered around the upper, wider end",
 "M54": "the same ladder, the same crop - two of its rungs have snapped and "
        "hang down askew",
 "M64": "the same ladder, intact - but the second rung from the bottom is "
        "visibly a different one: darker in colour, cut to another profile, "
        "newly set in",
 "M43": "a long bright workroom; at several tables women in high-necked "
        "blouses sit bent over glass plates; at the door a man in a suit "
        "hands in a plate box",
 "M44": "one woman with her hair pinned up in a bun at the back of her head, "
        "in a dark high-necked blouse, sits alone at a light table. Her head "
        "is tipped forward and down so that her eyes look straight down at "
        "the plate; her face is seen from above at an angle, not turned "
        "towards the viewer. Her right hand holds a round magnifying lens by "
        "its handle just above the plate, her left rests at the edge of the "
        "plate; stacks of further plates lie around her",
 "M45": "a close view of one hand holding a magnifying lens over a glass "
        "plate on a light table; under the glass lies an irregular cloud of "
        "stars with a dense core and frayed edges",
 "M46": "one single star in a field of stars, large and bright",
 "M47": "the same field of stars, the same crop - the one star has shrunk to "
        "a small dull point",
 "M48": "a close view of a sheet of paper lying on a light table. Scattered "
        "across it are small dots which line up along two parallel rising "
        "straight lines. The rest of the sheet is bare pale paper, empty "
        "apart from the dots and the two lines. Beside it, one hand with a "
        "pencil",
 "M49": "the same crop, the same hand with the pencil - on the sheet the "
        "upright edge line is now one clean bare stroke, smooth along its "
        "whole length",
 "M50": "a field of stars in which thirteen stand out noticeably brighter, "
        "scattered widely across the frame",
 "M51": "a close view of a sheet of paper lying on a desk. At the lower "
        "right sweeps one large flourish of ink, drawn as a single unbroken "
        "line from start to finish, with a strong upstroke and a long "
        "trailing tail. Above it, the cropped top edge of the sheet carries "
        "one row of short slanted marks of the same height, set in small "
        "clusters with narrow gaps between the clusters",
 "M52": "an empty desk at a window with one unopened envelope on it; the "
        "chair pushed back a little",
 "M55": "one man in a tweed jacket sits at the eyepiece of a very large "
        "reflecting telescope inside a dome, steel latticework above him",
 "M56": "a field of small spiral galaxies scattered across the whole frame, "
        "of differing sizes",
 "M58": "two pulsing stars side by side in a field of stars, one large and "
        "yellowish, the other smaller and bluish",
 "M59": "a hall with rows of seating, at the front one man at a lectern in "
        "front of a bright projection surface, the listeners leaning forward",
 "M60": "a close view of a photographic plate: one sharp bright point, and "
        "directly beside it a soft glowing patch of about the same brightness",
 "M61": "a small dense cluster of a few bright stars wrapped in faint nebula, "
        "above tree silhouettes in the night sky",
 "M62": "several large parabolic dish antennas on open ground, all tilted the "
        "same way, long shadows across the ground",
 "M63": "a fine-grained speckle pattern across the whole frame, and small in "
        "front of it a satellite in profile",
 "M65": "two spiral galaxies side by side against a dark ground, of about "
        "the same size",
 "M66": "a close view of two hands at the foot of a solid wooden ladder, one "
        "holding a single nail, the other reaching for it",
 "M67": "a field of stars in which several distinctly reddish, swollen stars "
        "stand among white points",
 "M69": "a field of galaxies in which one single point of light flares "
        "brilliantly at the edge of one galaxy, brighter than its core",
 "M68": "a close view of one hand writing with a pencil on a sheet, adding a "
        "second, shorter column beside an existing column. Both columns are "
        "built from short even pencil strokes set one under the other, "
        "aligned in clean rows; each entry is a small cluster of strokes",
}

LICHT = {
 "M01": "the stars themselves, and nothing else",
 "M02": "the stars",
 "M03": "one street lamp standing in the middle of the picture",
 "M04": "a window outside the frame to the left",
 "M05": "a window outside the frame to the left",
 "M06": "a window outside the frame to the left",
 "M07": "one street lamp",
 "M08": "the same street lamp",
 "M09": "a street lamp outside the frame to the left",
 "M10": "the stars", "M11": "the stars",
 "M13": "the Moon above the dome",
 "M14": "a workbench lamp outside the frame to the right",
 "M15": "a shaded oil lamp standing beside the instrument",
 "M16": "the star images in the field of view",
 "M17": "the star image in the field of view",
 "M18": "the oil lamp",
 "M19": "the candle",
 "M20": "the night sky through an open roof hatch",
 "M22": "the night sky through the roof hatch, outside the frame above",
 "M23": "a candle on the desk",
 "M24": "the star itself", "M25": "the star itself",
 "M26": "the night sky through the roof hatch",
 "M27": "a window with daylight",
 "M28": "the field of stars above the buildings",
 "M29": "the stars",
 "M30": "the low sun at the end of the road",
 "M31": "the low sun over the sea",
 "M32": "an oil lamp on the desk",
 "M33": "a desk lamp outside the frame to the left",
 "M34": "a desk lamp outside the frame to the left",
 "M35": "the Moon behind thin cloud",
 "M36": "the stars",
 "M37": "the Sun outside the frame to the right",
 "M38": "the Sun outside the frame to the left",
 "M39": "the Moon",
 "M40": "the galaxy itself",
 "M41": "the stars in the field of view",
 "M43": "tall sash windows along the left-hand side",
 "M44": "the light table itself, its glowing glass top filling the lower "
        "part of the frame",
 "M45": "the light table beneath the plate",
 "M46": "the star itself", "M47": "the star itself",
 "M48": "the light table beneath the sheet",
 "M49": "the light table beneath the sheet",
 "M50": "the stars",
 "M51": "a window outside the frame at the upper left",
 "M52": "the window with pale daylight",
 "M55": "the night sky through the open dome slit",
 "M56": "the galaxies themselves",
 "M58": "the stars themselves",
 "M59": "the projection beam from behind",
 "M60": "a light table behind the plate",
 "M61": "the stars of the cluster",
 "M62": "the low sun outside the frame to the right",
 "M63": "the speckle pattern glows by itself",
 "M65": "the galaxies themselves",
 "M66": "a lamp outside the frame to the left",
 "M67": "the stars themselves",
 "M69": "the flaring star itself",
 "M68": "a light table beneath the sheet",
}

ORT = {
 "Gegenwart, eine Wohnstraße bei Nacht": "a present-day residential street at night",
 "Gegenwart, dieselbe Straße": "the same present-day residential street",
 "Gegenwart, ein Stadtplatz am Abend": "a present-day town square in the evening",
 "Gegenwart, ein Wohnzimmer": "a present-day living room",
 "Gegenwart, dasselbe Zimmer": "the same present-day living room",
 "Gegenwart, dieselbe Straße im Januar": "the same residential street in January, present day",
 "Gegenwart, dieselbe Straße im Juli": "the same residential street in July, present day",
 "zeitlos, Blick ins All": None,
 "zeitlos, reine Zeichnung": None,
 "zeitlos, Blick zum Nachthimmel": None,
 "zeitlos, sinnbildlich": None,
 "Königsberg in Ostpreußen, 1838": "Koenigsberg in East Prussia in 1838",
 "Frauenburg im Ermland, 1543": "Frauenburg in Warmia in 1543",
 "Uraniborg auf der Insel Ven, um 1580": "Uraniborg on the island of Ven around 1580",
 "eine europäische Sternwarte, um 1700": "a European observatory around 1700",
 "1830er Jahre: Königsberg, Kap der Guten Hoffnung, Dorpat":
     "the eighteen-thirties, in three places: Koenigsberg, the Cape of Good "
     "Hope and Dorpat",
 "Royal Observatory am Kap der Guten Hoffnung, 1833":
     "the Royal Observatory at the Cape of Good Hope in 1833",
 "Kapstadt, 1833": "Cape Town in 1833",
 "Dorpat im Baltikum, 1837": "Dorpat in the Baltic in 1837",
 "Erdumlaufbahn, um 1990": "Earth orbit around 1990",
 "Lagrangepunkt hinter der Erde, 2015": "a Lagrange point beyond the Earth in 2015",
 "Lagrangepunkt, 2013": "a Lagrange point in 2013",
 "Harvard College Observatory, Massachusetts, 1908 bis 1912":
     "the Harvard College Observatory in Massachusetts between 1908 and 1912",
 "Harvard College Observatory, Massachusetts, um 1910":
     "the Harvard College Observatory in Massachusetts around 1910",
 "Harvard College Observatory, 1912": "the Harvard College Observatory in 1912",
 "Harvard College Observatory, um 1910":
     "the Harvard College Observatory around 1910",
 "Harvard, Massachusetts, 1925": "Harvard in Massachusetts in 1925",
 "Mount-Wilson-Observatorium, Kalifornien, 1929":
     "the Mount Wilson Observatory in California in 1929",
 "Rom, Tagung der Internationalen Astronomischen Union, 1952":
     "Rome in 1952, at a meeting of the International Astronomical Union",
 "Kalifornien, 1958": "California in 1958",
 "Gegenwart, Blick vom Boden": "the present day, seen from the ground",
 "Gegenwart, eine Landstraße": "a present-day country road",
 "Gegenwart, ein Antennenfeld im Hochland des amerikanischen Südwestens":
     "the present day, an antenna field in the uplands of the American "
     "south-west",
}

FLORA = {
 "mitteleuropäische Stadtbäume als dunkle Silhouetten — Linden, Ahorn; keine Palmen, keine Nadelwaldkulisse":
   "Central European street trees in silhouette - limes and maples; no palms "
   "and no conifer backdrop.",
 "einzelne beschnittene Platanen am Platzrand":
   "a few pollarded plane trees at the edge of the square.",
 "kahle Linden und Ahorne, Schneedecke":
   "bare limes and maples under snow cover.",
 "dieselben Bäume in vollem Laub": "the same trees in full leaf.",
 "norddeutsche Stadtbäume ohne Laub — Linden, Kastanien; keine Palmen, keine Nadelbäume":
   "north German street trees without leaves - limes and chestnuts; no palms "
   "and no conifers.",
 "Innenraum einer Kuppel, Holzdielen, keine Vegetation":
   "This is the interior of a dome: board floors, no vegetation.",
 "Innenraum, keine Vegetation": "This is an interior: no vegetation.",
 "Innenraum einer Sternwarte, Backsteinnischen, keine Vegetation":
   "This is an observatory interior: brick niches, no vegetation.",
 "Innenraum, Stuckdecke, keine Vegetation":
   "This is an interior: a plaster ceiling, no vegetation.",
 "je Vignette die Vegetation ihres Ortes: kahle Linden — Fynbos-Buschwerk — verschneite Birken":
   "each panel carries the vegetation of its own place: bare limes, then "
   "fynbos scrub, then snow-covered birches.",
 "Fynbos des Kaps — silbriges Buschwerk, Proteen, niedrige Hartlaubsträucher; ausdrücklich keine Palmen, keine Akazien":
   "Cape fynbos - silvery scrub, proteas, low hard-leaved shrubs; no palms "
   "and no acacias.",
 "baltische Winterlandschaft — Birken und Kiefern, Schneedecke":
   "a Baltic winter landscape - birches and pines under snow.",
 "Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation":
   "This is an interior: wood panelling and sash windows, no vegetation.",
 "Innenraum, Holzvertäfelung, keine Vegetation":
   "This is an interior: wood panelling, no vegetation.",
 "Innenraum; durch das Fenster kahle Laubbäume Neuenglands":
   "This is an interior; through the window, bare New England broadleaf trees.",
 "Innenraum einer Kuppel, keine Vegetation":
   "This is the interior of a dome: no vegetation.",
 "Innenraum, Marmorpilaster, keine Vegetation":
   "This is an interior: marble pilasters, no vegetation.",
 "mitteleuropäische Laubbäume als Silhouette":
   "Central European broadleaf trees in silhouette.",
 "trockenes Steppengras, niedrige Beifußbüsche, ferne kahle Bergrücken; keine Bäume, keine Kakteen":
   "dry steppe grass, low sagebrush, bare ridges in the distance; no trees "
   "and no cacti.",
 "Alleebäume beidseits — Pappeln oder Linden":
   "avenue trees on both sides - poplars or limes.",
}

# Diagramm-Grund fuer die vier Schemata, im ersten Lauf freigegeben.
SCHEMA_HART = (
    " DIAGRAM VOCABULARY: this picture is built only from simple graphic "
    "elements - straight lines, bars, dots, circles, arrows and wedges - "
    "arranged on one plain even field. There is no room, no ground plane, no "
    "table, no wall, no horizon and no floor for anything to stand on; "
    "nothing casts a shadow and nothing recedes into depth. Anything that "
    "exists as a real object in the world is drawn flat, seen straight from "
    "the side: one flat fill per part, plain straight bars, no wood grain, no "
    "metal sheen, no rounded or cylindrical parts, no vanishing point and no "
    "foreshortening.")
SCHEMA_TEXTFREI = (
    " ABSOLUTELY NO WRITING: no numbers, no digits, no tick marks with "
    "values, no axis labels, no legend, no caption, no letters of any "
    "alphabet anywhere in the picture. The picture must carry its meaning by "
    "shape, size and position alone.")
DURCHLICHT = (
    " ADDITION - ONE LIGHT SOURCE: the picture is lit from behind the sheet "
    "by a light table whose glowing glass top is directly beneath it. The "
    "glass itself is the brightest surface in the frame; the sheet and "
    "anything above it are lit from below, and nothing casts a downward "
    "shadow.")
DREITEILIG = (
    " COMPOSITION: the frame is divided into three equal upright panels side "
    "by side by two thin vertical rules. Each panel holds its own complete "
    "little scene, drawn at the same scale and with the same line weight as "
    "the others. This is one single picture of three panels, not three "
    "pictures, and not a scene seen through a window frame.")

NACHT_MOTIVE = {"M01", "M02", "M13", "M28", "M35", "M39", "M61"}


def prompt(mid: str) -> str:
    d = sp.M[mid]
    szene = SZENE[mid]
    bp.pruefe_szene(mid, szene)
    treffer = pruefe_vokabular(mid, szene)
    if treffer:
        raise SystemExit(f"{mid}: Risikovokabular im Szenentext: {treffer}. "
                         "Entweder umformulieren oder unter FREIGABE "
                         "eintragen (Lehre aus Stichprobe 2).")

    ist_schema = d.get("schema", False)
    fr = d["framing"]
    if ist_schema:
        rahmen = bp.FRAMING_OHNE
    elif fr == "ganz":
        rahmen = bp.FRAMING_SITZEND if d.get("sitzend") else bp.FRAMING_EINZEL
    elif fr == "teil":
        rahmen = bp.FRAMING_TEIL
    else:
        rahmen = bp.FRAMING_OHNE

    p = bp.MACHART + rahmen
    if ist_schema:
        p += bp.DIAGRAMM + SCHEMA_HART + bp.FARBEN_SCHEMA + SCHEMA_TEXTFREI
    else:
        if d["licht"].startswith("Durchlicht:"):
            p += DURCHLICHT
        elif d["licht"].startswith("Schatten:"):
            p += bp.Z3_AUSSERHALB.format(quelle=LICHT[mid])
        else:
            p += bp.Z3_SICHTBAR.format(quelle=LICHT[mid])
        p += bp.FARBEN
        ort = ORT[d["ort"]]
        if ort:
            p += (f" PERIOD AND PLACE: {ort}. Clothing, tools, architecture "
                  "and vegetation all belong to that period and place and to "
                  "no other.")
            if d["flora"] != "—":
                p += " " + FLORA[d["flora"]]
        p += bp.FLAECHE_HART
        if mid == "M28":
            p += DREITEILIG
        if mid in NACHT_MOTIVE:
            p += bp.NACHT
        if fr == "ganz":
            p += " " + bp.FIGUR
        elif fr == "teil":
            p += " " + bp.FIGUR_TEIL
    return p + " SCENE: " + szene.rstrip(".") + "." + bp.NEGATIV


def main() -> None:
    fehlend = sorted(set(sp.M) - set(SZENE))
    if fehlend:
        raise SystemExit(f"Szenentext fehlt: {fehlend}")
    ueberzaehlig = sorted(set(SZENE) - set(sp.M))
    if ueberzaehlig:
        raise SystemExit(f"Szenentext ohne Motiv: {ueberzaehlig}")
    for mid, d in sp.M.items():
        if not d.get("schema"):
            if d["ort"] not in ORT:
                raise SystemExit(f"{mid}: Ort '{d['ort']}' nicht übersetzt")
            if d["flora"] != "—" and d["flora"] not in FLORA:
                raise SystemExit(f"{mid}: Flora nicht übersetzt")
            if not d["licht"].startswith("Durchlicht:") and mid not in LICHT:
                raise SystemExit(f"{mid}: Lichtquelle nicht übersetzt")

    aus = {mid: prompt(mid) for mid in sp.M}
    (HIER / "bildplan2-prompts.json").write_text(
        json.dumps(aus, indent=1, ensure_ascii=False), encoding="utf-8")
    laengen = [len(p) for p in aus.values()]
    print(f"{len(aus)} Prompts · {min(laengen)}–{max(laengen)} Zeichen")
    print("Versalien- und Vokabelprüfung bestanden")


if __name__ == "__main__":
    main()
