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
    # Gegenstaende, die in der Wirklichkeit eine Aufschrift TRAGEN. Lehre
    # aus Stapel 3: "a two-euro coin" kam mit einer grossen 2 und dem Wort
    # EURO zurueck, in beiden Motiven. Das Modell zeichnet den echten
    # Gegenstand, und der echte Gegenstand ist beschriftet — das Verbot am
    # Prompt-Ende hat es wie immer uebergangen. Wer so einen Gegenstand
    # braucht, beschreibt ihn als Form, nicht als Ware.
    "Aufschrift-Träger": ["euro", "euros", "dollar", "dollars", "cent",
                          "cents", "pound", "banknote", "note", "stamp",
                          "newspaper", "poster", "packet", "calendar",
                          "keyboard", "licence", "license"],
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
 "M01": "seen from below, a night sky full of stars, one of them drawn about "
        "twice as wide as the rest; along the bottom edge the dark "
        "roofline of a residential street",
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
 # "a rectangular patch of the night sky" wurde in M11 als rechteckiger
 # Gegenstand gezeichnet, ein gerahmter Bildschirm mit Fuss. Und "fainter"
 # las das Modell als "dunkler" und fuellte die beiden Hintergrundsterne
 # dunkel aus. Beides steht jetzt als Bauform da: der Himmel fuellt das
 # ganze Bild, und der Unterschied zwischen den Sternen ist eine Groesse,
 # keine Bewertung.
 "M10": "the night sky over the whole frame, white star shapes scattered on "
        "deep blue; one star near the left is about three times as wide as "
        "the small ones, and two stars of middling size stand to the right "
        "of it",
 "M11": "the same sky with the same stars in the same places; only the one "
        "large star now stands to the right of the two middle-sized ones",
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
 # Erste Fassung nannte die Handlung als Attribut ("sits at the eyepiece,
 # turning a screw"). Das Modell setzte den Mann hin und gab ihm ein
 # kleines Handfernrohr in die Luft, waehrend der grosse Refraktor daneben
 # stand. Derselbe Fehler wie bei M44 in Stichprobe 2: Attribute fallen
 # weg, Bauanweisungen bleiben. Jetzt steht jede Hand, jedes Auge und
 # jeder Beruehrungspunkt einzeln da.
 "M15": "one man in the high-collared coat of the early nineteenth century "
        "sits on a low stool, his upper body leaning forward and his head "
        "bent down so that his right eye rests against the small eyepiece "
        "at the near, lower end of one single long telescope tube; the tube "
        "runs away from him and rises towards the upper right corner of the "
        "picture. His right hand is closed around a small ribbed brass drum "
        "set on the side of that tube just below the eyepiece, thumb and "
        "fingers on the drum. His left hand lies flat on his knee. Both "
        "hands are drawn and both are on the things named here",
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
 # "a soft edge" hat das Modell als Leuchthof gezeichnet — ein weicher
 # Verlauf, das einzige Bild der Reihe mit einem. Der weiche Rand ist
 # inhaltlich richtig (er ist der Unterschied zu M25), muss aber flaechig
 # gebaut werden: zwei harte Stufen statt eines Verlaufs.
 "M24": "one single star seen very close as a bare eye sees it, on the dark "
        "ground: a plain round white disc, and around it one broader ring in "
        "a single paler tone; both the disc and the ring have clean sharp "
        "edges and one even fill each",
 "M25": "the same close view of the same star - the wide disc and its ring "
        "are gone, and one small hard point of light remains in their place",
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
 "M30": "a dead straight country road running to the horizon; at the front of "
        "the frame one single small round metal coin stands upright on its "
        "edge on the asphalt, drawn flat like everything else - one solid "
        "pale ring for its rim and one solid gold circle inside it, both "
        "faces of the coin smooth and bare, and only the rim carries fine "
        "even notches; at the far end of the road a barely visible dot",
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
 "M39": "the full Moon above the residential street, and in the foreground on a "
        "window sill one single small round metal coin standing upright on "
        "its edge, drawn flat - one solid pale ring for its rim and one "
        "solid gold circle inside it, both faces smooth and bare; this one "
        "coin is the sharpest thing in the picture",
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
 "M46": "a field of stars in which one is drawn three times the width of all "
        "the others",
 "M47": "the same field of stars, the same crop - the one large star is now "
        "drawn the same small width as the others",
 "M48": "a close view of a sheet of paper lying on a light table. Scattered "
        "across it are small dots which line up along two parallel rising "
        "straight lines. The rest of the sheet is bare pale paper, empty "
        "apart from the dots and the two lines. Beside it, one hand with a "
        "pencil",
 "M49": "the same crop, the same hand with the pencil - on the sheet the "
        "upright edge line is now one clean bare stroke, smooth along its "
        "whole length",
 "M50": "a field of small stars in which thirteen are drawn twice as wide as "
        "the rest, scattered widely across the frame",
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
 "M60": "a close view of one glass plate: on it one small hard-edged dark dot, "
        "and directly beside it a larger soft-looking dark patch of about "
        "the same depth of tone, the two almost touching",
 "M61": "a small dense cluster of a few large white stars wrapped in a thin "
        "pale veil of nebula, high in the night sky; along the bottom edge "
        "the crowns of trees stand as flat shapes filled with one single "
        "near-black tone, their leaf edges readable only as the outline of "
        "that shape",
 "M62": "several large parabolic dish antennas on open ground, all tilted the "
        "same way, long shadows across the ground",
 "M63": "a fine-grained speckle pattern of small irregular blotches covers the "
        "whole frame from edge to edge, with nothing behind it and nothing "
        "beyond it; in front of that pattern, small and near the middle, "
        "stands one satellite seen from the side, and it is the only solid "
        "object in the picture",
 "M65": "two spiral galaxies side by side against a dark ground, of about "
        "the same size",
 "M66": "a close view of two hands at the foot of a solid wooden ladder, one "
        "holding a single nail, the other reaching for it",
 "M67": "a field of stars in which several distinctly reddish, swollen stars "
        "stand among white points",
 "M69": "a field of galaxies; at the edge of one of them sits a single white "
        "point drawn larger and whiter than that galaxy's own centre",
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
 # "without leaves" nennt Laub, um es zu verneinen — und M13 kam mit
 # belaubten Kronen und einer leuchtend gruenen Wiese zurueck. Jetzt steht
 # da, was gezeichnet werden soll: nacktes Astwerk.
 "norddeutsche Stadtbäume ohne Laub — Linden, Kastanien; keine Palmen, keine Nadelbäume":
   "north German street trees in winter - limes and chestnuts, each drawn as "
   "a bare branching silhouette of trunk and open twigs against the sky; no "
   "palms and no conifers.",
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
    # "no wood grain, no metal sheen" nannte Holz und Metall, um sie zu
    # verneinen. Drei der vier Schemata sind eine Leiter, die ausdruecklich
    # keine Holzleiter sein soll — zusammen mit dem Farbsatz stand das Wort
    # Holz zweimal im selben Prompt. Jetzt steht positiv da, wie die Flaeche
    # aussieht.
    "the side: one flat fill per part, plain straight bars, every surface "
    "one even colour from edge to edge, no rounded or cylindrical parts, no "
    "vanishing point and no foreshortening.")
SCHEMA_TEXTFREI = (
    " ABSOLUTELY NO WRITING: no numbers, no digits, no tick marks with "
    "values, no axis labels, no legend, no caption, no letters of any "
    "alphabet anywhere in the picture. The picture must carry its meaning by "
    "shape, size and position alone.")
# Der Block nannte dreimal "the sheet". Zwei der fuenf Durchlichtmotive
# haben aber gar kein Blatt: M45 und M60 zeigen eine Glasplatte. Jetzt
# benennt er nur, was in allen fuenf vorkommt — die leuchtende Glasflaeche
# und das, was darauf liegt.
DURCHLICHT = (
    " ADDITION - ONE LIGHT SOURCE: the picture is lit from below by a light "
    "table whose glowing glass top lies directly under whatever is being "
    "looked at. That glass is the brightest surface in the frame and it "
    "glows one flat pale warm cream - the same pale warm cream in every "
    "picture of this series, a white with a faint yellow in it and no blue. "
    "Everything resting on it and everything above it is lit from below, and "
    "nothing casts a downward shadow.")

# Im Weltraum gibt es keine Flaeche, auf die ein Schatten faellt, und keine
# beleuchtete Seite. Der allgemeine Lichtblock redet aber von beidem — vier
# Saetze ueber Schlagschatten und Lichtseiten fuer sechzehn Motive, die
# nichts als Sterne und Galaxien zeigen. Hier steht nur, was dort gilt.
# ------------------------------------------------- gemessene Serientoene --
# Zweite Haelfte der Bedingungsregel: was ueber alle Motive einer Gruppe
# gleich sein soll, muss ausdruecklich dastehen. Diese vier Bloecke sind aus
# der Messung der ersten 35 Bilder entstanden — jeder schliesst eine Spanne,
# die niemand angesagt hatte.

# Nachthimmel und Weltraumgrund: gemessen von (0,0,0) reinem Schwarz ueber
# (24,24,24) neutralem Grau bis (12,24,36) Tiefblau, und M02 lag mit
# (48,48,60) doppelt so hell wie der Rest.
DUNKELGRUND = (
    " THE DARK GROUND: the dark part of this picture is one flat near-black "
    "blue - the same near-black blue in every dark picture of this series. "
    "It is dark enough to read as night at a glance, and it is a blue: its "
    "blue is clearly stronger than its green, and its green clearly stronger "
    "than its red. It carries one even fill from edge to edge.")
DUNKELGRUND_MOTIVE = {"M01", "M02", "M10", "M11", "M13", "M24", "M25", "M28",
                      "M29", "M35", "M36", "M37", "M38", "M39", "M40", "M41",
                      "M46", "M47", "M50", "M56", "M58", "M61", "M65", "M67",
                      "M69"}

# Papier: gemessen von (228,228,228) neutralem Grauweiss ueber (240,228,228)
# rosastichig bis (240,240,216) gelblich. Der Ton ist derselbe, den der
# Schema-Farbsatz fuer seinen Grund verlangt — Blatt und Diagrammgrund
# gehoeren im selben Video zusammen.
PAPIERTON = (
    " THE PAPER: every sheet, page, card and plate of paper in this picture "
    "is one flat pale warm off-white with a faint cream cast - the same pale "
    "warm off-white in every picture of this series, at the brightness of "
    "fresh paper, one even fill with no shading across it.")
PAPIER_MOTIVE = {"M19", "M23", "M27", "M32", "M33", "M43", "M44", "M45",
                 "M48", "M49", "M51", "M60", "M68"}

# Messing: gemessen von (160,130,60) dunklem Ocker ueber (230,170,70)
# leuchtendem Gold bis (250,220,160) blassem Sand. Drei Messinggeraete, drei
# Goldtoene.
MESSINGTON = (
    " THE BRASS: every brass part in this picture carries one and the same "
    "flat medium gold - a warm yellow-brown gold of middling brightness, the "
    "same gold in every picture of this series, one even fill per part with "
    "no sheen, no highlight and no darkening towards an edge.")
MESSING_MOTIVE = {"M14", "M15", "M18", "M20", "M22"}

# ---------------------------------------------------- Steckbriefe --------
# Alles, was in mehr als einem Motiv vorkommt, braucht eine Beschreibung —
# nicht weil sie im einzelnen Bild fehlte, sondern weil die Bilder
# unabhaengig voneinander entstehen und das Modell das erste nie gesehen
# hat. Dieselbe Lage wie bei den Zustandspaaren, nur ueber einen
# Gegenstand, ein Gebaeude, einen Ort oder eine Person.
#
# Die 66 Szenentexte samt Licht- und Ortsangabe ergeben 47 Gegenstands-
# klassen in mehr als einem Motiv. Davon sind zwoelf ueber die Serientoene
# und die Farbbloecke schon festgelegt (Sterne, Galaxien, Papier, Messing,
# Leuchttisch, Platte, Dunkelgrund, Himmel, Baeume je Motiv, Leiter als
# Schema, Muenze, Sprosse). Die uebrigen stehen hier — jeweils fuer die
# Motive, in denen sie wirklich vorkommen, und nur mit dem, was in allen
# diesen Motiven gilt.
#
# Nach der Kanalvorgabe sind Figuren Epochenfiguren ohne
# Portraitaehnlichkeit: der Steckbrief legt darum eine Bauform fest, kein
# Gesicht einer bestimmten Person.
WIEDERKEHRER = {
    ("M20", "M23", "M26"): (
        " THIS PERSON APPEARS IN MORE THAN ONE PICTURE OF THIS SERIES AND IS "
        "BUILT THE SAME WAY IN EACH: a man of about forty, of middling "
        "build, with fair skin; a short full beard and moustache of dark "
        "reddish brown, trimmed close to the jaw; short hair of that same "
        "dark reddish brown, combed back from the forehead, the head bare; "
        "a dark plum-red doublet buttoned to the throat, and above it one "
        "narrow white pleated collar standing out from the neck."),
}

# Die Wohnstrasse der Gegenwart. Sechs Motive, gemessen an M07/M08/M39/M01
# beschrieben — dort stimmen sie schon ueberein. M02 fiel heraus: keine
# Haeuserzeile, eine weite leere Fahrbahn, ein flaches modernes Gebaeude.
# M02 ist die Klammer des Videos, erstes und letztes Bild, 26,6 s Laufzeit.
WIEDERKEHRER[("M01", "M02", "M07", "M08", "M39")] = (
    " THIS STREET APPEARS IN MORE THAN ONE PICTURE OF THIS SERIES AND IS THE "
    "SAME STREET IN EACH: two facing rows of two-storey terraced houses, "
    "their walls dark red brick with a few in pale cream render, each house "
    "with one square bay window on the ground floor and a plain pitched roof "
    "of dark grey slate; a low brick garden wall about knee height runs along "
    "the front of both rows; between the walls lies a grey asphalt roadway "
    "with a kerbed pavement of pale grey slabs on either side; one cast-iron "
    "street lamp with a single curved arm stands on the near pavement; "
    "broad-leaved street trees of middling height stand at even spacing "
    "along both kerbs.")

# Drei Sternwarten, jede in zwei Motiven — und zwei der drei liefen
# auseinander: die Koenigsberger war in M13 ein grosser roter Backsteinbau
# mit Portikus, in M28 ein kleines cremefarbenes Haus; die Dorpater war in
# M35 ein verputzter Bau mit Portikus und Kuppel, in M28 eine Blockhuette
# ohne Kuppel. Die Kapstaedter stimmte schon ueberein.
WIEDERKEHRER[("M13", "M28")] = (
    " THE OBSERVATORY AT KOENIGSBERG APPEARS IN MORE THAN ONE PICTURE OF "
    "THIS SERIES AND IS THE SAME BUILDING IN EACH: a two-storey block of "
    "dark red brick, wider than it is tall, with a shallow classical porch "
    "of four plain columns over the central entrance and one hemispherical "
    "dome of dull green copper set on the middle of its roof.")
WIEDERKEHRER[("M28b", "M31")] = (
    " THE OBSERVATORY AT THE CAPE APPEARS IN MORE THAN ONE PICTURE OF THIS "
    "SERIES AND IS THE SAME BUILDING IN EACH: a long single-storey block "
    "with white rendered walls and a flat roof, its windows tall and narrow "
    "with dark frames, and one small pale dome at its right-hand end.")
WIEDERKEHRER[("M28c", "M35")] = (
    " THE OBSERVATORY AT DORPAT APPEARS IN MORE THAN ONE PICTURE OF THIS "
    "SERIES AND IS THE SAME BUILDING IN EACH: a low single-storey house of "
    "pale rendered walls with horizontal timber boarding along the lower "
    "half, a shallow porch of two columns at its centre, and one small dark "
    "dome at the right-hand end of its roof.")

# Der Mauerquadrant des Daenen. M20 zeigte ihn als Handgeraet, M26 als
# kleines Tischgeraet, M22 als grossen Bogen in Nahsicht — drei Formen
# desselben Instruments.
WIEDERKEHRER[("M20", "M22", "M26")] = (
    " THIS INSTRUMENT APPEARS IN MORE THAN ONE PICTURE OF THIS SERIES AND IS "
    "THE SAME ONE IN EACH: one brass quarter-circle as tall as a doorway, "
    "set upright in a plain dark timber frame that rests on the "
    "floor; its curved outer edge is cut with fine even notches all along "
    "it; a slim brass bar pivots from the corner of the quarter-circle and "
    "carries a narrow slotted sight near its far end. It is far too large "
    "to be carried.")

# Das Blickfeld im Okular. M16 kam als flache dunkelblaue Scheibe mit
# blassen Streifen dahinter, M41 als dunkles Rundfeld mit konzentrischen
# Ringen.
WIEDERKEHRER[("M16", "M41")] = (
    " THE VIEW THROUGH AN EYEPIECE IS DRAWN THE SAME WAY IN EVERY PICTURE OF "
    "THIS SERIES: one true circle centred in the frame and reaching almost "
    "to the top and bottom edges; inside it one flat near-black blue and "
    "nothing else but what the scene names; its edge one clean black ring of "
    "the same weight as every other outline; outside the circle the frame is "
    "one flat dark neutral grey, empty from corner to corner.")

# Der Mond. In M13, M35 und M39 hat er je einen weichen Leuchthof — der
# einzige Verlauf, der in dieser Reihe dreimal durchgekommen ist.
# Nach dem M24-Muster gebaut: der weiche Rand wird zur harten Stufe. Dort
# hat genau das den Leuchthof geloest — Scheibe plus breiterer Ring in
# hellerem Ton, saubere Kante, je eine Fuellung. Ein Verbot ("no glow")
# haette hier nichts geholfen; der Hof ist dreimal durchgekommen.
WIEDERKEHRER[("M13", "M35", "M39")] = (
    " THE MOON IS DRAWN THE SAME WAY IN EVERY PICTURE OF THIS SERIES, AND IT "
    "IS BUILT FROM TWO FLAT STEPS: first one plain circle filled with a "
    "single off-white, and inside it three or four flat round patches of one "
    "slightly darker grey with clean edges; second, around that circle, one "
    "broader ring filled with a single tone lighter than the night ground "
    "and darker than the disc, its outer edge as clean and as sharp as the "
    "disc's own. Both the disc and the ring carry one even fill each, and "
    "the ring's outer edge meets the night ground directly with no third "
    "step between them.")

# Die Lupe, der Bleistift, die Kerze, der Schreibtisch in Kapstadt: kleine
# Gegenstaende, die zweimal oder dreimal vorkommen. Je ein Satz.
WIEDERKEHRER[("M44", "M45")] = (
    " THE MAGNIFYING LENS IS THE SAME ONE IN EACH PICTURE: a plain round "
    "glass in a thin brass rim with one short straight brass handle.")
WIEDERKEHRER[("M48", "M49", "M68")] = (
    " THE PENCIL IS THE SAME ONE IN EACH PICTURE: a plain six-sided wooden "
    "shaft of one flat mid-yellow, sharpened to a short dark tip.")
WIEDERKEHRER[("M19", "M23")] = (
    " THE CANDLE IS THE SAME ONE IN EACH PICTURE: one plain upright white "
    "candle standing in a small shallow metal dish with a ring handle.")
WIEDERKEHRER[("M32", "M33", "M34")] = (
    " THIS DESK APPEARS IN MORE THAN ONE PICTURE OF THIS SERIES AND IS THE "
    "SAME DESK IN EACH: a plain writing desk of mid-brown timber with a "
    "single wide drawer set in its front below the top.")

# Mehrere Steckbriefe koennen dasselbe Motiv treffen: M28 zeigt alle drei
# Sternwarten in einem Bild, M13 zeigt eine davon und den Mond. Die
# Schluessel M28b und M28c sind darum nur Platzhalter — sie landen alle auf
# M28 und werden aneinandergehaengt.
STECKBRIEF: dict[str, str] = {}
for _gruppe, _text in WIEDERKEHRER.items():
    for _mid in _gruppe:
        _echt = "M28" if _mid.startswith("M28") else _mid
        STECKBRIEF[_echt] = STECKBRIEF.get(_echt, "") + _text


# Vierzehn Motive zeigen ein Sternfeld, und bis zum 16.08.2026 sagte kein
# Block, wie ein Stern in dieser Reihe aussieht. Das Ergebnis war messbar:
# in M10 sind 0,0 % der hellen Punkte farbig, in M29 60,3 %, in M36 81,2 %
# — drei Sternfelder in einem Video, die aus drei Kanaelen stammen koennten.
# Die Regel nennt nur, was in allen vierzehn gilt: die kleinen Sterne des
# Hintergrunds. Was die Szene eigens faerbt (M58 gelblich und blaeulich,
# M67 roetlich), bleibt der Szene ueberlassen.
# M28 ist das einzige Motiv, das drei Orte in einem Bild zeigt. Die
# Bedingung "kommt Vegetation vor" ist dort fuer die mittlere Vignette
# wahr und fuer die beiden anderen falsch — und das Modell hat die
# Laubzusage prompt auf die kahle Vignette angewendet und einen
# belaubten Baum zwischen die kahlen Linden gesetzt. Wo eine Bedingung
# innerhalb eines Bildes wechselt, gilt die vorsichtigere Fassung; die
# Vegetation der einzelnen Vignetten steht ohnehin in der Florazeile.
GEMISCHTE_FLORA = {"M28"}

STERNFELD_MOTIVE = {"M01", "M02", "M10", "M11", "M28", "M29", "M36", "M37",
                    "M46", "M47", "M50", "M58", "M61", "M67"}
# Die Farbe war nach einem Lauf geloest (M29 und M36 kamen mit 0,0 %
# farbigen Sternpunkten zurueck, vorher 60,3 % und 81,2 %) — und prompt
# stand die Groesse als naechste ungesagte Eigenschaft da: M29s Sterne
# waren fuenfmal so gross wie M36s, und der "unscheinbare" Doppelstern der
# Szene war zwischen Riesensternen nicht mehr unscheinbar. Die Groesse wird
# darum wie in Video 1 an etwas im Bild gemessen, nicht als Bruchzahl —
# Bruchzahlen wurden dort zweimal uebergangen.
STERNFELD = (
    " THE STARS: the small stars of the background are plain five-pointed "
    "star shapes of one and the same white, all filled with that one white "
    "and differing from one another only in size. They are specks: each of "
    "the small ones is only a few times wider than the black outlines of "
    "this series are thick, so that many dozens of them fit across the width "
    "of the picture. They sit on the flat dark ground with nothing around "
    "them - each star is its own clean shape and carries no halo, no ray and "
    "no glow. Where the scene above gives one single star a size, a colour "
    "or a shape of its own, that one star follows the scene, is drawn "
    "clearly larger than these specks, and the rest follow this rule.")

# Dieselbe Luecke eine Objektklasse weiter: die Sternfarbe stand, die
# Galaxienfarbe nicht. M56 kam mit weiss-blauen Spiralen zurueck, M65 mit
# regenbogenfarbenen in Blau, Rosa, Orange und Violett.
GALAXIEN = (
    " THE GALAXIES: every spiral galaxy in this picture is drawn in the same "
    "two tones as the stars around it - a white core and arms of one single "
    "pale cool blue-white, each arm one flat fill from end to end. No galaxy "
    "carries pink, orange, violet or green, and no two galaxies are coloured "
    "differently from one another.")
GALAXIEN_MOTIVE = {"M40", "M56", "M65", "M69"}

# Und noch eine: wie eine hinterleuchtete Fotoplatte Sterne zeigt. M45 kam
# mit weissen Punkten auf dunklem Glas zurueck, M60 mit einem dunklen Keil
# auf hellem Grund — zwei Platten, zwei Konventionen, und die zweite
# widersprach ihrer eigenen Szene ("ein scharfer heller Punkt"). Auf einer
# Glasplatte gegen das Licht sind Sterne dunkel; das ist zugleich die
# Konvention, die fuer die Schemata schon gilt (dunkle Punkte auf hellem
# Grund wie auf gedruckten Sternkarten).
PLATTE = (
    " THE PLATE: this glass plate is a negative held against the light, so "
    "its ground is the pale warm cream of the lit glass and every star on it "
    "is a DARK speck on that pale ground - small dark round dots, in the "
    "manner of a printed star chart, never light dots on a dark field. A "
    "star that the scene calls sharp is one small hard-edged dark dot; a "
    "star the scene calls soft or swollen is a larger dark patch with a "
    "clean edge.")
PLATTE_MOTIVE = {"M45", "M60"}

LICHT_WELTRAUM = (
    " ADDITION - ONE LIGHT SOURCE: the only thing that gives light in this "
    "picture is {quelle}, and it is drawn as a flat bright shape on the dark "
    "ground. Nothing else in the frame is lit and nothing casts a shadow, "
    "because there is no surface for a shadow to fall on.")
DREITEILIG = (
    " COMPOSITION: the frame is divided into three equal upright panels side "
    "by side by two thin vertical rules. Each panel holds its own complete "
    "little scene, drawn at the same scale and with the same line weight as "
    "the others. This is one single picture of three panels, not three "
    "pictures, and not a scene seen through a window frame.")

NACHT_MOTIVE = {"M01", "M02", "M13", "M28", "M35", "M39", "M61"}

# M06 ist der einzige Koerperausschnitt, der ein Gesicht zeigt.
KOPF_MOTIVE = {"M06"}

# Vier Motive zeigen mehrere Menschen — und bekamen bis zum 16.08.2026
# FRAMING_EINZEL, das woertlich "no second figure" verlangt. Derselbe
# Widerspruch wie bei M06, nur haeufiger: der Anweisungsteil verbot, was die
# Szene verlangte. In M03 und M27 hat das Modell das Verbot uebergangen und
# die Gruppe gezeichnet, in M43 hat das Verbot gewonnen — von mehreren
# Frauen am Arbeitstisch und dem Mann an der Tuer kam eine einzige Frau
# zurueck. Welche Seite gewinnt, ist Zufall; der Widerspruch gehoert weg.
MEHRFIGUR = {"M03", "M27", "M43", "M59"}
FRAMING_GRUPPE = (
    "FRAMING: several people are in this picture and every one of them is "
    "drawn whole - nobody is cut off by the edge of the frame, and nobody is "
    "a mirrored copy of anyone else. They are shown at what they are doing; "
    "where someone sits at a table or a desk, that furniture may cover the "
    "lower body. Sober, restrained, documentary - never cute."
)

# Nur wo die Szene selbst eine Kopfbedeckung verlangt. Alle uebrigen
# Figurenmotive bekommen "the hair of that period" ohne Hut.
KOPFBEDECKUNG = {"M27"}

# Sechzehn Motive zeigen nichts als den Weltraum — kein Ort, kein Boden,
# kein Horizont. Bis zum 16.08.2026 hatten sie ueberhaupt keinen Block, der
# das sagt: der Nachtblock galt nur fuer irdische Nachtbilder, und FARBEN
# versprach ihnen blauen Himmel und gruenes Gras. M24 verlangte die extreme
# Nahaufnahme eines Sterns und kam als Tageslandschaft mit Teich, Rasen und
# einem Backsteingebaeude zurueck: 60 % des Bildes blauer Himmel.
WELTRAUM_MOTIVE = {"M10", "M11", "M24", "M25", "M29", "M36", "M40", "M41",
                   "M46", "M47", "M50", "M56", "M58", "M65", "M67", "M69"}

# Beschrieben, nicht verboten: was da IST, ist eine schwarze Flaeche und
# darin die Lichtquellen. Eine Liste dessen, was fehlen soll — Horizont,
# Wolke, Boden, Pflanze — wuerde nach der Regel dieses Projekts genau das
# herbeirufen.
WELTRAUM = (
    " DEEP SPACE: this picture shows airless space. Its ground is one flat "
    "near-black tone across almost the whole frame, and the only bright "
    "shapes anywhere in it are the light sources named above; every other "
    "part of the frame stays that same near-black. The picture reads as "
    "space at a glance, and the brightest tones appear only inside those "
    "sources.")


def hat_pflanzen(flora: str) -> bool:
    """Ob im Bild ueberhaupt gruene Vegetation vorkommt.

    Nur dann darf der Weltfarbsatz Laub und Gras benennen. "ohne Laub"
    zaehlt nicht: M13 verlangte kahle Baeume und bekam belaubte Kronen,
    weil derselbe Prompt zwei Zeilen weiter "foliage and grass are green"
    versprach.
    """
    # "als Silhouette" ist der dritte Fall neben "—" und "ohne Laub": ein
    # Baum, der als dunkle Silhouette gezeichnet werden soll, zeigt keine
    # Blattfarbe. M61 verlangte Baumsilhouetten am Nachthimmel und bekam
    # gruene, beleuchtete Kronen und eine leuchtende Wiese — dieselbe
    # Ursache wie bei M13, dritter Fall.
    return (flora != "—" and "keine Vegetation" not in flora
            and "ohne Laub" not in flora and "ilhouette" not in flora)




# Der Anweisungsteil liegt seit dem 16.08.2026 in zwei Fassungen in
# bildplan.py: mit Figur der Wortlaut aus Video 1, ohne Figur der um die
# Personenwoerter erleichterte. Der Umbau steht dort begruendet.
_machart = bp.machart


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
        rahmen = bp.FRAMING_LEER
    elif fr == "ganz" and mid in MEHRFIGUR:
        rahmen = FRAMING_GRUPPE
    elif fr == "ganz":
        rahmen = bp.FRAMING_SITZEND if d.get("sitzend") else bp.FRAMING_EINZEL
    elif fr == "teil":
        rahmen = bp.FRAMING_KOPF if mid in KOPF_MOTIVE else bp.FRAMING_TEIL
    else:
        rahmen = bp.FRAMING_LEER

    def ohne_treppen(x: str) -> str:
        i = x.find(" The cast shadow is drawn even where it falls across")
        return x if i < 0 else x[:i] + x[x.index("no surface is exempt.") + 21:]

    mit_figur = not ist_schema and fr in ('ganz', 'teil')
    p = _machart(mit_figur) + rahmen
    if ist_schema:
        p += (bp.DIAGRAMM + SCHEMA_HART + bp.FARBEN_SCHEMA_OHNE_STOFFE
              + SCHEMA_TEXTFREI)
    else:
        if d["licht"].startswith("Durchlicht:"):
            p += DURCHLICHT
        elif mid in WELTRAUM_MOTIVE:
            p += LICHT_WELTRAUM.format(quelle=LICHT[mid])
        elif d["licht"].startswith("Schatten:"):
            p += bp.Z3_AUSSERHALB.format(quelle=LICHT[mid])
        else:
            p += bp.Z3_SICHTBAR.format(quelle=LICHT[mid])
        pflanzen = hat_pflanzen(d["flora"]) and mid not in GEMISCHTE_FLORA
        p += bp.farben(mit_figur, pflanzen)
        ort = ORT[d["ort"]]
        if ort:
            if mit_figur:
                epoche = bp.EPOCHE_MIT_FIGUR
            elif pflanzen:
                epoche = bp.EPOCHE_OHNE_FIGUR
            else:
                epoche = bp.EPOCHE_NEUTRAL
            p += f" PERIOD AND PLACE: {ort}. {epoche}"
            if d["flora"] != "—":
                p += " " + FLORA[d["flora"]]
        p += bp.FLAECHE_HART_OHNE_LISTE
        if mid == "M28":
            p += DREITEILIG
        if mid in NACHT_MOTIVE:
            p += bp.NACHT
        if mid in WELTRAUM_MOTIVE:
            p += WELTRAUM
        if mid in STERNFELD_MOTIVE:
            p += STERNFELD
        if mid in GALAXIEN_MOTIVE:
            p += GALAXIEN
        if mid in PLATTE_MOTIVE:
            p += PLATTE
        if mid in DUNKELGRUND_MOTIVE:
            p += DUNKELGRUND
        if mid in PAPIER_MOTIVE:
            p += PAPIERTON
        if mid in MESSING_MOTIVE:
            p += MESSINGTON
        if mid in STECKBRIEF:
            p += STECKBRIEF[mid]
        if fr == "ganz":
            p += " " + bp.figur(mid in KOPFBEDECKUNG)
        elif fr == "teil":
            p += " " + (bp.FIGUR_KOPF if mid in KOPF_MOTIVE else bp.FIGUR_TEIL)
    return ohne_treppen(p) + " SCENE: " + szene.rstrip(".") + "." + bp.NEGATIV


# Ein Prompt fuer ein Bild ohne Figur darf keine Person benennen. Einzige
# Ausnahme ist der Framing-Satz selbst, der die Leere ausspricht — ohne das
# Wort "people" laesst sie sich nicht sagen. Alles andere ist der Fehler aus
# Stapel 1 und bricht den Lauf ab, bevor Credits fliessen.
PERSONENWORT = re.compile(
    r"\b(figure|figures|clothing|clothes|clothed|prop|props|tool|tools|"
    r"person|adult|adults|dressed|garment|garments|wearing|worn)\b", re.I)


# Dieselbe Regel eine Ebene weiter, Lehre aus Stapel 2: der Anweisungsteil
# darf auch keine Pflanze und keinen Baustoff benennen, wenn im Bild keine
# vorkommt. M24 verlangte die Nahaufnahme eines Sterns und bekam eine
# Tageslandschaft, weil FARBEN gruenes Gras und blauen Himmel zusagte.
PFLANZENWORT = re.compile(
    r"\b(foliage|grass|greenery|leaves|shrub|shrubs|hedge|lawn|brick|"
    r"masonry|render)\b", re.I)


def pruefe_pflanzenworte(prompts: dict[str, str]) -> None:
    for mid, p in prompts.items():
        d = sp.M[mid]
        if d.get("schema") or hat_pflanzen(d["flora"]):
            continue
        # Der Flora- und Ortssatz des Motivs ist ausgenommen: was dort
        # steht, ist ausdruecklich gewollt (M20 hat wirklich Backsteinnischen).
        # Geprueft werden die geteilten Bloecke, die allen Motiven gleich
        # mitlaufen — dort sitzt der Fehler aus Stapel 2.
        kopf = p.split(" SCENE:")[0]
        if d["flora"] != "—":
            kopf = kopf.replace(FLORA[d["flora"]], "")
        # Der Steckbrief des Motivs ist aus demselben Grund ausgenommen wie
        # der Florasatz: was dort steht, ist ausdruecklich gewollt. Die
        # Wohnstrasse besteht wirklich aus Backstein und Putz.
        if mid in STECKBRIEF:
            kopf = kopf.replace(STECKBRIEF[mid], "")
        treffer = sorted(set(m.group(0).lower()
                             for m in PFLANZENWORT.finditer(kopf)))
        if treffer:
            raise SystemExit(
                f"{mid}: Pflanzen- oder Baustoffwort im Anweisungsteil eines "
                f"Bildes ohne Vegetation: {treffer}. Das ist die Ursache aus "
                "Stapel 2.")


def pruefe_personenworte(prompts: dict[str, str]) -> None:
    for mid, p in prompts.items():
        d = sp.M[mid]
        if not d.get("schema") and d["framing"] in ("ganz", "teil"):
            continue
        rest = p.replace(bp.FRAMING_LEER, "")
        treffer = sorted(set(m.group(0).lower()
                             for m in PERSONENWORT.finditer(rest)))
        if treffer:
            raise SystemExit(
                f"{mid}: Personenwort im Prompt eines figurenlosen Bildes: "
                f"{treffer}. Das ist die Ursache aus Stapel 1.")


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
    pruefe_personenworte(aus)
    pruefe_pflanzenworte(aus)
    (HIER / "bildplan2-prompts.json").write_text(
        json.dumps(aus, indent=1, ensure_ascii=False), encoding="utf-8")
    laengen = [len(p) for p in aus.values()]
    print(f"{len(aus)} Prompts · {min(laengen)}–{max(laengen)} Zeichen")
    print("Versalien- und Vokabelprüfung bestanden")
    ohne = sum(1 for mid, d in sp.M.items()
               if d.get("schema") or d["framing"] not in ("ganz", "teil"))
    print(f"Personenwortprüfung bestanden ({ohne} figurenlose Prompts)")
    kahl = sum(1 for mid, d in sp.M.items()
               if not d.get("schema") and not hat_pflanzen(d["flora"]))
    print(f"Pflanzenwortprüfung bestanden ({kahl} Motive ohne Vegetation)")


if __name__ == "__main__":
    main()
