#!/usr/bin/env python3
"""Baut die 84 Bildprompts fuer Video 1 aus `szenen.md` plus Stilfestlegung.

Der Prompt setzt sich in dieser Reihenfolge zusammen:

  1. Machart-Block  — woertlich aus `recherche/stil-figuren/lauf2-erwachsen/README.md`
  2. Z3-Lichtquelle — woertlich aus `recherche/stil-touch/README.md`, nur bei
                      Raumbildern; Schemabilder bekommen stattdessen die
                      Diagrammzeile
  3. Palette        — Themenpalette nach Epoche plus Signaltuerkis #1BBFB0
  4. THIS CHARACTER — nur bei Motiven mit Figur
  5. SCENE          — die Bildbeschreibung aus `szenen.md`
  6. Negativliste

Der `FRAMING:`-Satz des Machart-Blocks wird bei Mehrfigurenszenen ersetzt,
wie es der Machart-Block selbst vorschreibt.
"""
from __future__ import annotations

import json
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
WURZEL = HIER.parent.parent

# ---------------------------------------------------------------- Machart ----
MACHART = (
    "Flat 2D vector illustration in the style of a serious documentary explainer "
    "video made for adults. Clean uniform anti-aliased black outlines of constant "
    "medium weight - the same line weight on figures, clothing, props and background "
    "alike; no sketchy lines, no hand-drawn jitter, no crosshatching, no thick-thin "
    "variation in the outline. Completely flat colour fills, no gradients, no "
    "shading, no rendering; hard-edged angular shapes with straight edges and clear "
    "corners rather than soft rounded blobs. ADULT PROPORTIONS - the most important "
    "rule: the head is about one fifth of the total body height and never larger than "
    "one quarter; these are grown adults, not children, not chibi mascots, not cute "
    "cartoon toys; shoulders clearly wider than the head, a visible neck, a defined "
    "angular jaw, long straight limbs, simple flat hands with a thumb and a hint of "
    "finger separation. Both arms are visible and attached to the body, and the hand "
    "that holds or carries an object is drawn. Any description of head shape refers "
    "to the outline of the skull only and never changes this head-to-body proportion. "
    "FACE BUILD, identical construction for every character in this series: small "
    "eyes, each about one tenth of the head width, a rounded white eye shape with one "
    "solid dark pupil, fully open, no catchlight highlight, no eyelashes, no "
    "half-closed lids, no wide staring doll eyes; EYEBROWS ARE MANDATORY on every "
    "character, male and female alike - two clearly drawn brows sit above the eyes, "
    "never omitted, never replaced by eyelashes; only their shape and weight vary, "
    "and they carry the expression; a minimal nose indicated by one short straight "
    "line or a small flat shadow shape; below it one short thin straight mouth line; "
    "no cheek blush, no baby face. Minimal symbolic background built from a few large "
    "flat shapes, generous empty space, muted era-appropriate colours. "
)
FRAMING_EINZEL = (
    "FRAMING: a single person, alone in the frame, full body visible, not cropped - "
    "head, both hands and both feet inside the picture, no second figure, no mirrored "
    "duplicate. Sober, restrained, documentary - never cute."
)
FRAMING_MEHR = (
    "FRAMING: figures are shown in full, not cropped at the edge of the frame. "
    "Sober, restrained, documentary - never cute."
)
FRAMING_OHNE = (
    "FRAMING: no people in this picture at all. "
    "Sober, restrained, documentary - never cute."
)

# ------------------------------------------------------------------- Z3 ------
# Z3 in zwei Fassungen. Der Zusatz aus `stil-touch/` verlangt woertlich eine
# *sichtbare* Quelle. Gemessen an den 62 Raumbildern ist das bei 27 (44 %)
# physisch unmoeglich - Nahaufnahmen, Aufsichten, Luftbilder, und M02, wo
# `szenen.md` ausdruecklich "kein Horizont" vorschreibt. Die Regel wuerde dort
# 27-mal reissen. Praezisiert auf: sichtbare Quelle, wo sie ins Bild passt,
# sonst eindeutig gerichteter harter Schatten aus derselben einen Richtung.
# Der harte, flaechige, verlauffreie Schatten - der eigentliche Bildeffekt von
# Z3 - ist in beiden Fassungen identisch gefordert.
SCHATTEN = (
    "Everything the light strikes casts a hard flat shadow: each shadow is a solid "
    "shape in one single darker tone of the surface it falls on, with straight or "
    "simply curved edges, no gradient, no blur, no soft falloff, no ambient shading. "
    "All shadows run in the same direction, away from the light. The lit sides stay "
    "completely flat and unshaded. The cast shadow is drawn even where it falls "
    "across stairs, steps, rubble or patterned and textured ground - it steps over "
    "those surfaces and stays clearly visible on them; no surface is exempt."
)
Z3_SICHTBAR = (
    " ADDITION - ONE LIGHT SOURCE: exactly one light source is visible in the picture, "
    "{quelle}. " + SCHATTEN
)
Z3_AUSSERHALB = (
    " ADDITION - ONE LIGHT SOURCE: the picture is lit by exactly one light source, "
    "{quelle}. The source itself lies outside the frame and is not drawn - this shot "
    "is too close in for it to fit. " + SCHATTEN
)
DIAGRAMM = (
    " This is a flat diagram, not a photograph of a place: no light source, no cast "
    "shadows, no depth, no perspective - flat shapes on an even ground."
)

# -------------------------------------------------------------- Paletten -----
PALETTEN = {
    "moor": ("bog near-black #241C16 as the darkest tone and the outlines, peat brown "
             "#4A3B2A, moss green #6E7A4F, bog water grey #8A8F7D, pale linen #E6DFCF "
             "as the lightest surface"),
    "antike": ("deep shadow #3A3026 as the darkest tone and the outlines, terracotta "
               "#A85E3C, burnt ochre #8A6A2F, sand #D9C49A, limestone #C9BFA8, bleached "
               "linen #EDE4D2 as the lightest surface"),
    "nord": ("night blue #26313A as the darkest tone and the outlines, forest green "
             "#3F4A38, oak wood #6B4F35, muted madder red #7A3B2E, tin grey #9AA0A2, "
             "tallow #DED3B8 as the lightest surface"),
}
# Korrektur, dritte Fassung: Das Tuerkis wurde flaechig gelesen - zwei Stellen in
# M06, Randstreifen in M62, der ganze Basaltblock in M49.
SIGNAL = (" SIGNAL COLOUR: exactly ONE object in the image carries the turquoise "
          "#1BBFB0 - no second occurrence, no turquoise in water, sky, ground, "
          "vegetation, edges or borders. If no single object needs marking, the "
          "turquoise is absent from the picture entirely.")

# --------------------------------------------------- Figur des Erzaehlstrangs -
# Korrektur 4: Die Hand war in M72 als gespreizte Klaue geraten. Der
# Machart-Block sagt "a hint of finger separation"; das reicht offenbar nicht.
FIGUR = (
    "THIS CHARACTER: one adult human being, plainly built, dressed and equipped for "
    "the period and place named above; small eyes with one dark pupil each, above them "
    "two clearly drawn eyebrows, then a minimal nose and one short straight mouth line, "
    "then hair and headwear of that period. HANDS: simple mitten-like shapes with a "
    "thumb, the other fingers only hinted by one or two short notches, never spread "
    "apart, never drawn as separate claws or splayed digits. "
)

# Korrektur 3: Anschnittverbot. M62 (Fuesse) und M49 (Figur am linken Rand)
# hielten den FRAMING-Satz nicht ein.
KEIN_ANSCHNITT = (" Every figure stands complete inside the picture; no part of any "
                  "figure touches or crosses the edge of the frame.")

# Korrektur 2: Figurengroesse, wo szenen.md ausdruecklich "klein" verlangt.
# Korrektur 2, zweite Fassung. Die Bruchzahl ("no more than one sixth") wurde in
# beiden Laeufen ignoriert - M06 und M62 zeigten die Figur auf halber Bildhoehe.
# Ersetzt durch eine Beschreibung ohne Zahl.
KLEIN = (" The figure is a small distant element, the landscape dominates, the "
         "figure occupies roughly the lower quarter of the frame and is clearly "
         "subordinate to the surroundings.")

NEGATIV = (" no text, no letters, no numbers, no watermark, no logo.")

MODELL = "nano_banana_2"
SEITE = "16:9"

# ----------------------------------------------------------- Zuordnungen -----
# Palette je Motiv. Regel: Nordwesteuropaeisches Moor -> moor · Aegypten,
# Babylon, Persien, Chaco, Rom -> antike · Anden und die Gegenwartsklammer
# -> nord (kuehle Toene: Zinngrau, Nachtblau). Schemabilder erben die Palette
# ihres Zusammenhangs, tragen aber kein Licht.
PALETTE = {
    **{m: "moor" for m in """M06 M07 M08 M09 M10 M11 M12 M13 M14 M15 M16 M17 M18 M19
        M20 M21 M22 M23 M24 M25 M26 M27 M28 M29 M30 M31 M32 M34 M35 M36 M37 M38 M39
        M40 M41 M42 M77 M78 M79 M80 M81 M82""".split()},
    **{m: "antike" for m in """M43 M45 M46 M47 M48 M49 M50 M51 M52 M53 M54 M55 M56 M57
        M58 M59 M60 M61 M62 M63 M64 M65 M66 M74 M75 M76""".split()},
    **{m: "nord" for m in "M01 M02 M03 M04 M05 M33 M44 M67 M68 M69 M70 M71 M72 M73 M83 M84".split()},
}

# Korrektur 1: Zeit und Ort in den Prompt. Die Spalte `Epoche/Ort` in
# szenen.md nennt bei 41 Motiven nur den Ort und bei 6 nur die Zeit; nur 8
# tragen eine Jahreszahl. Ohne diese Zeile raet das Modell nach der Palette -
# daher der aegyptische Nemes in Chaco Canyon und die Schiebermuetze auf der
# Inka-Treppe im ersten Stapel.
#
# Die Jahreszahlen sind NICHT erfunden, sondern aus `skript.md` uebernommen:
# Sweet Track 3807 v. Chr., Campemoor "rund sechseinhalbtausend Jahre",
# Aegypten "vor etwa 4.500 Jahren", Babylon 569 v. Chr., Persien "um 500 v.
# Chr.", Chaco "etwa tausend Jahre zurueck", Inka "um 1450", Via Appia 312 v.
# Chr.
EPOCHE_EN = {
    "heute": "the present day",
    "heute / Studie": "the present day",
    "heute / urzeitlich": "the present day",
    "urzeitlich": "Neolithic north-west Europe, around 3800 BC",
    "Moor": "Neolithic north-west Europe, around 3800 BC",
    "Somerset": "the Somerset Levels in southern England, 3807 BC",
    "Somerset ~3800 v. Chr.": "the Somerset Levels in southern England, 3807 BC",
    "Somerset 3807/3806 v. Chr.": "the Somerset Levels in southern England, 3807 BC",
    "Somerset / Wald": "the Somerset Levels in southern England, 3807 BC",
    "Campemoor": "the Campemoor bog in Lower Saxony, northern Germany, around 4500 BC",
    "Dümmer": "the Dümmer lake region in Lower Saxony, northern Germany, around 4500 BC",
    "Niedersachsen": "Lower Saxony, northern Germany, prehistoric bog country",
    "Niedersachsen, heute": "a present-day archaeological excavation in Lower Saxony, northern Germany",
    "Ägypten": "Old Kingdom Egypt, around 2500 BC",
    "Ägypten ~2500 v. Chr.": "Old Kingdom Egypt, around 2500 BC",
    "Ägypten, Altes Reich": "Old Kingdom Egypt, around 2500 BC",
    "Babylon": "Babylon in Mesopotamia, 569 BC, under Nebuchadnezzar II",
    "Babylon, 569 v. Chr.": "Babylon in Mesopotamia, 569 BC, under Nebuchadnezzar II",
    "Babylon, Neujahr": "Babylon in Mesopotamia, 569 BC, the spring new year festival",
    "Persien ~500 v. Chr.": "the Achaemenid Persian empire, around 500 BC",
    "Chaco": "Chaco Canyon in New Mexico, ancestral Pueblo culture, around 1000 AD",
    "Chaco ~1000 n. Chr.": "Chaco Canyon in New Mexico, ancestral Pueblo culture, around 1000 AD",
    "Anden": "the Inca empire in the Andes, around 1450 AD",
    "Anden ~1450 n. Chr.": "the Inca empire in the Andes, around 1450 AD",
    "Rom, 312 v. Chr.": "the Roman Republic, 312 BC",
    "Rom, Via Appia": "the Roman Republic, 312 BC, the Appian Way",
}

# Motive, deren Epochenspalte in szenen.md unbrauchbar ist ("Schema", "Detail",
# "zeitlos"), hier einzeln zugeordnet. Entschieden am 15.08.2026:
#   M41, M78, M42, M77 bleiben bewusst zeitlos - ohne Epochenzeile.
#   M48 ist Aegypten (Auftrag).
#   Die uebrigen aus dem Zusammenhang der Szenenliste, Herleitung in
#   bilder/README.md.
EPOCHE_JE_MOTIV = {
    "M12": "the Somerset Levels in southern England, 3807 BC",
    "M17": "the Somerset Levels in southern England, 3807 BC",
    "M18": "the Somerset Levels in southern England, 3807 BC",
    "M20": "the Somerset Levels in southern England, 3807 BC",
    "M31": "the Campemoor bog in Lower Saxony, northern Germany, around 4500 BC",
    "M39": "Lower Saxony, northern Germany, the 25th century BC",
    "M47": "Old Kingdom Egypt, around 2500 BC",
    "M48": "Old Kingdom Egypt, around 2500 BC",
    "M79": "no particular period - an old road anywhere, with no modern vehicles, "
           "no modern signage and no electric lighting",
    "M80": "no particular period - an old road anywhere, with no modern vehicles, "
           "no modern signage and no electric lighting",
}
# Bewusst ohne Epochenzeile: M41 und M42 stellen zwei Zeiten absichtlich
# nebeneinander, M77 und M78 sind laut Skript zeitlos gemeint.
ZEITLOS = {"M41", "M42", "M77", "M78"}

# Kulturen, die laut skript.md kein Rad hatten oder es hier nicht benutzten:
# Chaco ("no wheel, no horse, no ox"), Anden ("no wheel and no animal to pull a
# cart"), das nordwesteuropaeische Moor ("twenty centuries before anything
# rolled on one") und Aegypten, wo die Bloecke auf Schlitten und per Boot
# bewegt wurden. In M49 hatte das Modell dem Schlitten Raeder gegeben - das
# widerspricht der Kernaussage des Videos.
KEIN_RAD = set("""M06 M07 M08 M09 M10 M11 M12 M14 M15 M16 M17 M18 M19 M20 M21 M22
    M23 M24 M27 M28 M29 M30 M31 M32 M34 M37 M45 M46 M47 M48 M49 M50 M51 M60 M62
    M63 M64 M65 M66 M67 M69 M70 M72 M81""".split())
RADVERBOT = (" This culture has no wheeled transport at all: no wheels, no carts, "
             "no wagons, no barrows, no chariots and no draught animals anywhere "
             "in the picture.")

# Epochenangabe fehlt in szenen.md ganz. Bei Motiven OHNE Figur ist das
# unkritisch - ein Diagramm oder ein freigestelltes Fundstueck braucht keine
# Tracht. Bei Motiven MIT Figur ist es das nicht: diese drei sind gemeldet und
# laufen erst, wenn die Epoche entschieden ist.
OHNE_EPOCHE_MIT_FIGUR = {"M41", "M48", "M78"}

# Raumbilder, in denen die Lichtquelle physisch nicht ins Bild passt.
QUELLE_AUSSERHALB = set("""M01 M02 M03 M07 M09 M12 M15 M17 M18 M19 M20 M27 M28 M31
    M32 M38 M39 M45 M47 M48 M51 M52 M60 M66 M70 M83 M84""".split())

# Schemabilder: flaches Diagramm, kein Licht, keine Tiefe.
SCHEMA = set("""M04 M05 M13 M16 M25 M26 M30 M34 M35 M36 M40 M41 M43 M44 M54 M59 M61
                M64 M65 M68 M73 M76""".split())

# Mehrfigurenszenen — hier wird der FRAMING-Satz getauscht.
MEHRFIGUR = set("M49 M56 M74 M75 M78".split())

# Genau eine Lichtquelle je Raumbild. Wo szenen.md eine Richtung oder Tageszeit
# vorgibt (Gegenlicht, Nacht, Fackel, Morgennebel), ist sie uebernommen;
# sonst ergaenzt. Motive derselben Szene teilen die Richtung, damit der
# Schnitt nicht springt.
LICHT = {
    "M01": "the low morning sun, coming from the left",
    "M02": "the low sun, raking across the surface from the right",
    "M03": "the low sun, coming from the left",
    "M06": "the low sun, coming from the right, low over the water",
    "M07": "the low sun, coming from the left",
    "M08": "the low sun, coming from the right",
    "M09": "the low sun, coming from the left",
    "M10": "the low morning sun, standing behind the mist",
    "M11": "the low morning sun, coming from the left",
    "M12": "the low sun, raking across the cut surface from the left",
    "M14": "the low winter sun, coming from the right",
    "M15": "the low sun, coming from the left",
    "M17": "the low sun, coming from the left",
    "M18": "the low sun, coming from the left",
    "M19": "the low sun, coming from the right",
    "M20": "the low sun, coming from the left",
    "M21": "the low sun, coming from the right",
    "M22": "the low sun directly ahead, behind the walkway, throwing it into backlight",
    "M23": "the low sun directly ahead, behind the walkway, throwing it into backlight",
    "M24": "daylight from directly above, entering through the water surface",
    "M27": "the low sun, coming from the right",
    "M28": "the low sun, coming from the left",
    "M29": "the low sun, coming from the right",
    "M31": "the low sun, raking across the cut end from the left",
    "M32": "the low sun, coming from the left",
    "M33": "a single desk lamp, standing at the upper left of the desk",
    "M37": "the low sun, coming from the right",
    "M38": "the low sun, coming from the right",
    "M39": "the low sun, coming from the left",
    "M42": "the low sun, coming from the right",
    "M45": "the low sun, coming from the right",
    "M46": "the low sun, coming from the right",
    "M47": "the low sun, raking across the paving from the left",
    "M48": "the low sun, raking across the slab from the left",
    "M49": "the low sun, coming from the right",
    "M50": "the low sun, coming from the left, low over the water",
    "M51": "the low sun, coming from the right",
    "M52": "the low sun, raking across the relief from the left",
    "M53": "the low sun, standing directly behind the gate",
    "M55": "the low sun, standing directly ahead behind the gate",
    "M56": "the low spring sun, coming from the left",
    "M57": "a single burning torch on the wall, the only light in the night street",
    "M58": "the low sun, coming from the right",
    "M60": "the low sun, coming from the left",
    "M62": "the low sun, standing directly ahead at the end of the road bed",
    "M63": "the low sun, coming from the right",
    "M66": "the low sun, coming from the left",
    "M67": "the low sun, coming from the right",
    "M69": "the low sun, coming from the right",
    "M70": "the low sun, coming from the right",
    "M71": "the low sun, coming from the left",
    "M72": "the low sun, coming from the right",
    "M74": "the low sun behind the column, throwing the figures into backlight",
    "M75": "the low sun directly ahead, throwing the column into backlight",
    "M77": "the low sun, coming from the left",
    "M78": "the low sun, coming from the left",
    "M79": "a single street lamp, reflected in the water film",
    "M80": "the moon, the only light left on the road edge",
    "M81": "the low sun, breaking through the rain from the left",
    "M82": "the low sun, standing behind the fog",
    "M83": "the low sun, coming from the left",
    "M84": "the low sun, coming from the right",
}


# Englische Fassung der SCENE-Texte. Der Machart-Block ist englisch; ein
# gemischtsprachiger Prompt senkt die Treue. Die Stichprobe lief ebenfalls
# mit englischem SCENE-Text.
SZENE_EN = {
 "M01": "top-down view: the character steps out of a house door onto an empty asphalt road that fills the lower third of the frame",
 "M02": "a frame-filling expanse of asphalt with joints and cracks, no horizon",
 "M03": "three flat vehicle silhouettes - a car, a truck, a shipping container - moving across the road as bands",
 "M04": "three equally sized panels side by side: a Roman helmet, a merchant's balance scale, a single spoked wheel",
 "M05": "the same three panels, each struck through with one broad diagonal bar",
 "M06": "a wide flat meadow landscape, dark water spreading across the ground from the right, the character standing small at the left edge, a broad band of sky with a hard cloud edge filling the upper third",
 "M07": "close view: the character kneels and lays a pale wooden plank onto the soft ground, the water stopping at its edge",
 "M08": "a wide bog surface with cushions of peat moss and open black eyes of water, the character standing small in the middle, a broad band of sky filling the upper third",
 "M09": "close view of bog ground: a boot sinks to the shaft in black water between moss cushions",
 "M10": "a wide marsh landscape in morning mist: bands of reeds, open sheets of water, a wooded island on the horizon",
 "M11": "the same marsh landscape, now with the character at the shore and a first plank lying in the reeds",
 "M12": "a frame-filling cross-section slice of an oak trunk, concentric annual rings as flat rings",
 "M13": "the same sequence of rings unrolled into a straight band, wide and narrow rings alternating",
 "M14": "a bare winter forest in snow, the character striking a massive oak with a stone axe",
 "M15": "aerial view: a dead-straight pale plank line runs through dark reed bog",
 "M16": "a flat map: an island at the left, a ridge of higher ground at the right, the line running through the marsh between them",
 "M17": "a still life on empty ground: one long, broad, strikingly thin oak plank, beside it the trunk with splitting wedges driven into it",
 "M18": "three tools side by side on empty ground: a stone axe, a wooden wedge, a mallet",
 "M19": "medium close view: the character's hands drive crossed pegs into the peat and lay a plank into the notch",
 "M20": "extreme close view of the push-fit joint: notch and peg interlock, no nail",
 "M21": "coppiced woodland in rows: dead-straight branchless hazel rods, old cut faces on the stools",
 "M22": "low to the ground and backlit: the finished walkway is exactly one plank wide and loses itself in the reeds",
 "M23": "the same walkway, water already standing over the planks",
 "M24": "a view below the water surface: beneath the sunken walkway a second, older plank line shimmers",
 "M25": "a flat map of north-west Europe: one point of light in southern England, the land mass reaching north-east to the north German plain",
 "M26": "the same map, hundreds of small points of light igniting over the plain",
 "M27": "an excavation trench in peat: the character kneels with a trowel before a half-uncovered find under a tarpaulin",
 "M28": "a still aerial view: a shallow lake in dark wet bog country",
 "M29": "an uncovered stretch of trackway in the peat profile, the character standing small beside it as a scale, the trench edge and a band of sky filling the upper third",
 "M30": "a cross-section diagram: thin birch trunks at the bottom, above them three rows of pine logs, above that a thick round-timber surface, angled pegs at the sides",
 "M31": "extreme close view: the cut end of a round timber with facetted axe marks in the old wood",
 "M32": "aerial view: two parallel pale lines run thirty metres apart through the same bog",
 "M33": "a desk seen from above: an open study, a hand drawing a rising curve and setting a question mark in the margin",
 "M34": "a shoreline over time: water pushes across flat land in steps, each step a separate pale edge",
 "M35": "a split picture: rising water at the left, migrating settlement points on a stylised map at the right",
 "M36": "a diagram: along a horizontal time axis, plank trackways stack into three waves, the gaps between them staying empty",
 "M37": "a pine stand at the bog edge, visibly thinned: stumps in the foreground, few crowns behind",
 "M38": "the same excavation as before, the tarpaulin folded back: two broken wooden cart axles lying in the wet peat",
 "M39": "the two axles isolated on empty ground, like a museum find",
 "M40": "a timeline drawn as a plank trackway: the track runs from left to right, its beginning far to the left, and only just before the right edge lies a small wheel",
 "M41": "the character walks along that same timeline, the wheel still far ahead",
 "M42": "a single spoked wheel rolls onto an old plank road, slows and comes to a stop",
 "M43": "a flat world map: the two northern European points go dark, lights ignite in Egypt, Iraq, Iran, New Mexico and the Andes",
 "M44": "five empty frames side by side, a question mark in each",
 "M45": "a desert aerial view: a pale stone road runs from a dark basalt quarry through scree slopes to a distant shoreline",
 "M46": "the quarry in section: dark basalt benches with tool marks, the road beginning in front of them",
 "M47": "close to the ground: paving of basalt lumps, limestone and sandstone, and between them slabs of petrified wood with visible grain",
 "M48": "a hand runs across a slab of petrified wood, the grain lying exposed",
 "M49": "three haulers in a line drag a heavy dark basalt block down the road on a flat wooden sledge with no wheels of any kind, the sledge sliding forward over loose wooden rollers laid across its path, all three haulers complete and well inside the frame",
 "M50": "a loaded barge with dark blocks on wide water, a pyramid construction site with ramps on the horizon",
 "M51": "the finished dark temple floor of basalt slabs, strictly gridded",
 "M52": "a relief wall seen frontally: lions, bulls and dragons as flat figures in rows",
 "M53": "the skyline of Babylon, the gate as the brightest surface",
 "M54": "a road cross-section: stone slabs bedded in a dark layer of bitumen, the width indicated by a measuring band",
 "M55": "the character stands at the left edge of the frame in profile, looking down the broad street towards the gate rising in the distance, relief walls on both sides",
 "M56": "a procession in spring light: statues of gods on litters move through the gate, a dense crowd, the character carrying with them",
 "M57": "the same street empty at night, only torchlight on the relief walls",
 "M58": "a rider changes horse at a relay station without stopping, behind him the road runs to the horizon",
 "M59": "a map band from Susa to Sardis: one line with chain links as stations",
 "M60": "a canyon aerial view: red rock walls, a hair-fine straight line in the desert floor",
 "M61": "three panels, each struck through: a wheel, a horse, an ox",
 "M62": "low in the scraped-out road bed: nine metres wide, edges of stone, dead straight to the horizon, the character standing small at the edge, the canyon rim and sky filling the upper third",
 "M63": "a stone stairway cut into the rock face, the road continuing unbroken above",
 "M64": "four symbol panels above the road bed: a carrying basket, a spear, a rattle staff, a circle of assembly",
 "M65": "a lidar overlay: a point cloud of the terrain, one road line aiming at a low sun point above a mountain",
 "M66": "a vertical climb away: the road becomes a thin line and ends in emptiness",
 "M67": "an Andean panorama: a thread of road runs over ridges and through valleys, no end in sight",
 "M68": "three number bands of different lengths above one another, all three equally bright",
 "M69": "the same Andean route, one older section tinted in a different hue",
 "M70": "a fly-past, the surface changing in three sections: paving, packed earth, sand",
 "M71": "an empty route on a steep slope, no wheel and no draught animal in the picture",
 "M72": "a stone stairway climbs a steep slope, the character running up it lightly",
 "M73": "a map of South America: the network glows in full, only a quarter of the lines staying bright",
 "M74": "a long row of blurred figures, and at the very end a single legionary steps into frame",
 "M75": "a marching column on a straight stone road heading south, dust, spear tips backlit",
 "M76": "two equally sized cross-sections side by side: at the left the four-layer stone stack, at the right an earth track with a thin gravel top",
 "M77": "a visibly centuries-old plank road, worn smooth, empty",
 "M78": "the same road, now traders with bundles moving across it",
 "M79": "a rainy night: a simple old road holds under a film of water, lights reflecting in it",
 "M80": "the same road in darkness, only the edge of the way still visible",
 "M81": "back to Somerset: the character lays the last plank in the rain, water already standing at the pegs",
 "M82": "a wide shot in fog: the broken axle beside the ancient plank line",
 "M83": "modern shoes at a softened path edge, water collecting in the prints",
 "M84": "the same ordinary present-day passer-by as in the opening shot, in the same plain everyday jacket and trousers and flat cap - no high-visibility vest, no hard hat, no building site and no machinery - has just laid a fresh wooden plank on soft wet ground and now stands upright over it, head raised, looking straight out of the picture directly at the viewer",
}

# Haertung aus dem Stichprobenlauf: Motive, in denen die Figur unter etwa 15 %
# der Bildhoehe misst, erzeugten zwei ueberlebensgrosse "Geisterkoepfe" und eine
# gespiegelte Komposition. Gegenmittel laut Stichprobe: oberes Bilddrittel
# belegen (oben in SZENE_EN eingearbeitet) und dieser Zusatz.
KLEINE_FIGUR = set("M06 M08 M29 M62".split())
GEISTERKOPF = (" Exactly one character in the frame, no floating heads, no duplicated "
               "or mirrored composition.")


def motive() -> dict:
    t = (HIER / "szenen.md").read_text(encoding="utf-8")
    rows = [l for l in t.splitlines()
            if l.startswith("|") and re.match(r"^\|\s*\d+\s*\|", l)]
    mot: dict = {}
    for l in rows:
        c = [x.strip() for x in l.split("|")[1:-1]]
        if len(c) < 12:
            continue
        m = re.search(r"M\d{1,3}", c[4] or "")
        if not m:
            continue
        k = m.group()
        if k in mot:
            mot[k]["einstellungen"].append(int(c[0]))
            mot[k]["dauer"] += float(c[3].replace(" s", "").replace(",", "."))
            continue
        mot[k] = {"bild": c[5], "fahrt": c[6], "epoche": c[7],
                  "fig": c[8] == "ja", "ebenen": c[10] == "ja",
                  "anmerkung": c[11], "einstellungen": [int(c[0])],
                  "dauer": float(c[3].replace(" s", "").replace(",", "."))}
    return mot


def prompt(mid: str, m: dict) -> str:
    ist_schema = mid in SCHEMA
    if not m["fig"]:
        framing = FRAMING_OHNE
    elif mid in MEHRFIGUR:
        framing = FRAMING_MEHR
    else:
        framing = FRAMING_EINZEL

    p = MACHART + framing
    if m["fig"]:
        p += KEIN_ANSCHNITT
    if ist_schema:
        p += DIAGRAMM
    elif mid in QUELLE_AUSSERHALB:
        p += Z3_AUSSERHALB.format(quelle=LICHT[mid])
    else:
        p += Z3_SICHTBAR.format(quelle=LICHT[mid])
    p += f" PALETTE: the picture uses only these colours - {PALETTEN[PALETTE[mid]]}." + SIGNAL
    epoche = None if mid in ZEITLOS else (
        EPOCHE_JE_MOTIV.get(mid) or EPOCHE_EN.get(m["epoche"].strip()))
    if epoche:
        p += f" PERIOD AND PLACE: {epoche}. Clothing, tools, architecture and " \
             "vegetation all belong to that period and place and to no other."
    if m["fig"]:
        p += " " + FIGUR
    p += " SCENE: " + SZENE_EN[mid].rstrip(".") + "."
    if mid in KLEINE_FIGUR:
        p += KLEIN + GEISTERKOPF
    if mid in KEIN_RAD:
        p += RADVERBOT
    return p + NEGATIV


if __name__ == "__main__":
    mot = motive()
    for mid, m in mot.items():
        m["palette"] = PALETTE[mid]
        m["licht"] = "Schema - keine Lichtquelle" if mid in SCHEMA else LICHT[mid]
        m["schema"] = mid in SCHEMA
        m["prompt"] = prompt(mid, m)
    (HIER / "bildplan.json").write_text(
        json.dumps(mot, indent=1, ensure_ascii=False), encoding="utf-8")
    fehlt = [k for k in mot if k not in SCHEMA and k not in LICHT]
    print(f"{len(mot)} Motive · Schema {sum(1 for k in mot if k in SCHEMA)} · "
          f"Raumbild {sum(1 for k in mot if k not in SCHEMA)}")
    print(f"ohne Lichtquelle (muss 0 sein): {fehlt}")
    from collections import Counter
    print("Paletten:", dict(Counter(PALETTE[k] for k in mot)))
    print("Figurenmotive:", sum(1 for m in mot.values() if m["fig"]))
