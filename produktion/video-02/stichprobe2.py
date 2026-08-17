#!/usr/bin/env python3
"""Zweiter Stichprobenlauf zu Video 2 — die Risikofaelle der Erzaehlfassung.

Fuenf Motive, keines davon im ersten Lauf geprueft:

M33, M51, M68  beschriebenes Papier. DER Fall, an dem Video 1 zweimal
               gescheitert ist: die Handschrift wurde lesbar und schrieb
               Promptwoerter ab, Tippfehler eingeschlossen. Verbote hat das
               Modell dort ignoriert. Hier steht darum kein Verbot, sondern
               eine Beschreibung dessen, was auf dem Papier LIEGT —
               Tintenspur, Zeilenrhythmus, Wortlaengen.
M28            Triptychon: drei Nachtvignetten in einem Bild. Gab es in
               Video 1 nicht; unerprobte Komposition.
M44            Licht von unten am Gesicht. Genau das hat der erste
               Stichprobenlauf ignoriert (M55 damals): der Leuchttisch
               gluehte, das Gesicht war konventionell von vorn beleuchtet.

Die Bausteine kommen aus produktion/video-01/bildplan.py, die Szenentexte
aus szenenplan.py — kein zweiter Wortlaut, der auseinanderlaufen koennte.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib

HIER = pathlib.Path(__file__).resolve().parent


def _lade(name: str, pfad: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bp = _lade("bildplan", HIER.parent / "video-01" / "bildplan.py")
sp = _lade("szenenplan", HIER / "szenenplan.py")

MOTIVE = ["M33", "M51", "M68", "M28", "M44"]

# Englische Fassung der Szenentexte. Der deutsche Text in szenenplan.py ist
# die Quelle; hier steht seine Uebersetzung, damit beide zusammen gelesen
# werden koennen.
SZENE_EN = {
 "M33":
   "a close view of one hand laying a sheet of paper into an open desk "
   "drawer. The sheet fills a good part of the frame. Across it run dense "
   "horizontal rows of short slanted marks, every mark the same height, set "
   "in small clusters of three to eight with narrow gaps between the "
   "clusters. Every mark is the same length; none is curved, none carries "
   "an ascender or a descender, and no cluster repeats another",
 "M51":
   "a close view of a document lying on a desk. At the lower right sits a "
   "large sweeping signature drawn as one single continuous loop of ink, "
   "with a strong upstroke and a long trailing tail, no separated marks "
   "anywhere in it. Above it, the cropped first line of the sheet: one row "
   "of short slanted marks of the same height, set in small clusters with "
   "narrow gaps between the clusters",
 "M68":
   "a close view of one hand writing with a pencil on a sheet, adding a "
   "second, shorter column beside an existing column of measurements. Both "
   "columns are built from short even pencil strokes set one under the "
   "other, aligned in clean rows; each entry is a small cluster of strokes, "
   "none of them formed into a figure",
 "M28":
   "one picture divided into three equal upright panels side by side, each "
   "a small night scene. Left panel: a domed observatory building among "
   "bare-branched lime and chestnut trees. Middle panel: a low white "
   "flat-roofed observatory on a ridge with silvery fynbos scrub and a "
   "flat-topped mountain behind it. Right panel: a low wooden observatory "
   "under snow among bare birches. The same field of stars runs across all "
   "three panels above the buildings",
 "M44":
   "one adult woman in a dark high-necked blouse sits alone at a light "
   "table, her gaze lowered onto a large glass photographic plate lying on "
   "the glowing glass, a magnifying lens in one hand. Stacks of further "
   "glass plates are piled around her. The glowing glass is the only light "
   "in the room: it strikes her from below, so the bright areal patches lie "
   "on the underside of her chin, on her jaw and on the lower half of her "
   "cheeks and forearms, while her forehead, the top of her head and the "
   "wall behind her stay in flat shadow",
}

LICHT_EN = {
 "M33": ("a desk lamp standing outside the frame to the left, throwing a "
         "hard flat shadow of the hand across the sheet"),
 "M51": ("a window outside the frame at the upper left, throwing a hard "
         "flat shadow of the paper edge across the desk"),
 "M68": None,   # Durchlicht
 "M28": None,   # je Vignette der Nachthimmel, sichtbar
 "M44": ("the light table itself, its glowing glass top filling the lower "
         "part of the frame"),
}

EPOCHE_EN = {
 "M33": ("Cape Town in 1833. Clothing, furniture and instruments belong to "
         "that period and place and to no other. This is an interior: "
         "dark stained wood, no vegetation of any kind."),
 "M51": ("the Harvard College Observatory in Massachusetts in 1912. Paper, "
         "ink and desk belong to that period and place and to no other. "
         "This is an interior: no vegetation of any kind."),
 "M68": ("the Harvard College Observatory in Massachusetts around 1910. "
         "This is an interior: no vegetation of any kind."),
 "M28": ("the 1830s. Buildings, instruments and vegetation belong to that "
         "decade and to the three places shown, and to no others."),
 "M44": ("the Harvard College Observatory in Massachusetts around 1910. "
         "Clothing, furniture and instruments belong to that period and "
         "place and to no other. This is an interior: wood panelling and "
         "tall sash windows, no vegetation of any kind."),
}

DURCHLICHT = (
    " ADDITION - ONE LIGHT SOURCE: the picture is lit from behind the sheet "
    "by a light table whose glowing glass top is directly beneath it. The "
    "glass itself is the brightest surface in the frame; the sheet and the "
    "hand above it are lit from below, and nothing casts a downward shadow.")

DREITEILIG = (
    " COMPOSITION: the frame is divided into three equal upright panels by "
    "two thin vertical rules. Each panel holds its own complete little "
    "scene, drawn at the same scale and with the same line weight as the "
    "others. This is one single picture of three panels, not three "
    "pictures, and not a scene seen through a window frame.")


def prompt(mid: str) -> str:
    d = sp.M[mid]
    bp.pruefe_szene(mid, d["szene"])          # Versalien-Pruefung, wie im Plan
    fr = d["framing"]
    if fr == "ganz":
        rahmen = bp.FRAMING_SITZEND if d.get("sitzend") else bp.FRAMING_EINZEL
    elif fr == "teil":
        rahmen = bp.FRAMING_TEIL
    else:
        rahmen = bp.FRAMING_OHNE

    p = bp.MACHART + rahmen
    if d["licht"].startswith("Durchlicht:"):
        p += DURCHLICHT
    elif d["licht"].startswith("Schatten:"):
        p += bp.Z3_AUSSERHALB.format(quelle=LICHT_EN[mid])
    else:
        p += bp.Z3_SICHTBAR.format(quelle=LICHT_EN[mid] or "the stars above "
                                   "each of the three buildings")
    p += bp.FARBEN
    p += f" PERIOD AND PLACE: {EPOCHE_EN[mid]}"
    p += bp.FLAECHE_HART
    if mid == "M28":
        p += DREITEILIG
        # Drei Nachtszenen. Ohne den Nachtblock verspricht FARBEN blauen
        # Himmel — bei Video 1 kamen alle drei Nachtmotive taghell zurueck.
        p += bp.NACHT
    if fr in ("ganz",):
        p += " " + bp.FIGUR
    elif fr == "teil":
        p += " " + bp.FIGUR_TEIL
    return p + " SCENE: " + SZENE_EN[mid].rstrip(".") + "." + bp.NEGATIV


if __name__ == "__main__":
    aus = {mid: prompt(mid) for mid in MOTIVE}
    (HIER / "stichprobe2-prompts.json").write_text(
        json.dumps(aus, indent=1, ensure_ascii=False), encoding="utf-8")
    for mid, p in aus.items():
        print(f"=== {mid}  ({len(p)} Zeichen)")
        print(p[p.index(" SCENE:"):])
        print()
