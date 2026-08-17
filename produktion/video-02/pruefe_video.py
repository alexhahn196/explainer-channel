#!/usr/bin/env python3
"""Prueft das fertige Video gegen den Schnittplan.

Die Frage ist nicht, ob ffmpeg durchgelaufen ist — das sagt der Rueckgabewert.
Die Frage ist, ob an jeder Stelle das RICHTIGE Bild steht. Geprueft wird das,
indem an Stichproben ein Einzelbild aus dem Video gezogen und gegen alle 66
Motivbilder verglichen wird. Das aehnlichste muss das im Schnittplan
eingetragene sein.

Verglichen wird ueber ein grobes Farbhistogramm statt Pixel fuer Pixel: die
Kamerafahrt schneidet ja einen wandernden Ausschnitt heraus, ein direkter
Pixelvergleich schluege deshalb auch bei richtiger Zuordnung fehl.
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import imageio_ffmpeg
import numpy as np
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
VIDEO = HIER / "video-02.mp4"


def histogramm(im: Image.Image) -> np.ndarray:
    a = np.asarray(im.convert("RGB").resize((64, 36), Image.LANCZOS))
    h, _ = np.histogramdd(a.reshape(-1, 3), bins=(6, 6, 6),
                          range=((0, 256), (0, 256), (0, 256)))
    h = h.ravel().astype(float)
    return h / max(h.sum(), 1)


def zustaende(mid: str) -> set[str]:
    """Die anderen Zustaende desselben Gegenstands.

    Ein Zustandspaar ist definiert als dasselbe Bild mit einer Aenderung. Kein
    globales Mass kann M48 von M49 trennen, und keines soll es: die beiden
    unterscheiden sich in einer Punktreihe. Wo das aehnlichste Bild der
    Partner ist, ist das Bild richtig — die Zuordnung ist nur nicht
    entscheidbar. Die Leiter kommt in drei Zustaenden vor (M42, M54, M64) und
    zaehlt darum als Gruppe, nicht als Paar.
    """
    import itertools
    gruppen = [{"M04", "M05"}, {"M07", "M08"}, {"M10", "M11"}, {"M16", "M17"},
               {"M24", "M25"}, {"M33", "M34"}, {"M42", "M54", "M64"},
               {"M46", "M47"}, {"M48", "M49"}]
    for g in gruppen:
        if mid in g:
            return g - {mid}
    return set()


def muster(im: Image.Image, n: int = 64) -> np.ndarray:
    """Grobes Helligkeitsraster, mittelwertfrei und auf Streuung normiert.

    Das Farbhistogramm allein reicht fuer diese Reihe nicht: vierzehn Motive
    sind weisse Sterne auf demselben Tiefblau und haben damit nahezu dasselbe
    Histogramm. Einstellung 29 (M11) wurde deshalb als M46 gemeldet, obwohl
    das richtige Bild dort stand — gemessen am Muster kommt M11 auf +0,76 und
    M46 auf -0,03. Das Raster vergleicht, WO das Helle liegt, und ueberlebt
    den wandernden Ausschnitt der Kamerafahrt, weil es stark verkleinert und
    normiert ist.
    """
    a = np.asarray(im.convert("L").resize((n, n), Image.LANCZOS)).astype(float)
    a -= a.mean()
    return a.ravel() / (np.linalg.norm(a) + 1e-6)


def bild_bei(t: float) -> Image.Image:
    roh = subprocess.run(
        [FFMPEG, "-v", "error", "-ss", f"{t:.3f}", "-i", str(VIDEO),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout
    import io
    return Image.open(io.BytesIO(roh))


def main() -> None:
    plan = json.loads((HIER / "schnittplan.json").read_text(encoding="utf-8"))
    motive = {p.stem: (histogramm(Image.open(p)), muster(Image.open(p)))
              for p in sorted((HIER / "bilder").glob("M[0-9][0-9].png"))}
    # Nur die kanonischen 66 Namen. Der Ordner enthaelt zusaetzlich die
    # Zwischenstaende der Ableitungen (M47-montage.png, M54-i2i.png) —
    # Dateien, die mit ihrem kanonischen Gegenstueck BITGLEICH sind. Gegen
    # alles im Ordner geprueft, gewinnt die Kopie mit Haaresbreite, und die
    # Pruefung meldet einen Fehler, wo keiner ist.

    schritt = max(1, len(plan) // int(sys.argv[1] if len(sys.argv) > 1 else 20))
    proben = plan[::schritt]
    treffer, fehler, paare = 0, [], []
    for s in proben:
        t = s["start_s"] + s["dauer_s"] / 2          # Mitte der Einstellung
        im = bild_bei(t)
        h, mu = histogramm(im), muster(im)
        # Erst nach Farbe vorsortieren, dann unter den zehn naechsten nach dem
        # Muster entscheiden. Die Farbe allein verwechselt die Sternfelder.
        # Nach dem Muster ueber ALLE Motive sortieren, nicht nur ueber die
        # farblich naechsten: M10 gegen M65 lag farblich auf Platz 24, und ein
        # Vorfilter von zehn haette das Muster nie abstimmen lassen.
        rang = sorted(motive, key=lambda k: -float(np.dot(motive[k][1], mu)))
        if rang[0] == s["motiv"] or rang[0] in zustaende(s["motiv"]):
            treffer += 1
            if rang[0] != s["motiv"]:
                paare.append((s["nr"], s["motiv"], rang[0]))
        else:
            fehler.append((s["nr"], round(t, 1), s["motiv"], rang[0], rang.index(s["motiv"]) + 1))
    print(f"Bild-zu-Plan: {treffer}/{len(proben)} Stichproben treffen das "
          f"eingetragene Motiv")
    if paare:
        print(f"  davon {len(paare)} auf dem Zustandspartner statt dem Motiv — "
              "das sind Bilder, die sich per Konstruktion nur in einer Sache "
              "unterscheiden:")
        for nr, soll, ist in paare:
            print(f"    Einstellung {nr}: {soll} / {ist}")
    for nr, t, soll, ist, platz in fehler:
        print(f"  Einstellung {nr} bei {t}s: erwartet {soll}, "
              f"aehnlichstes {ist} (Soll auf Platz {platz})")

    # Laufzeitabgleich
    dauer = float(subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(VIDEO), "-f", "null", "-"],
        capture_output=True).returncode == 0)
    ton = json.loads((HIER / "ton" / "_zeitplan.json").read_text(encoding="utf-8"))
    tonende = ton[-1]["start_s"] + ton[-1]["dauer_s"]
    planende = plan[-1]["start_s"] + plan[-1]["dauer_s"]
    print(f"\nTonspur endet bei   {tonende:.2f} s")
    print(f"Schnittplan endet bei {planende:.2f} s")
    print(f"Versatz: {abs(tonende - planende):.2f} s")
    print(f"Video dekodiert fehlerfrei: {'ja' if dauer else 'NEIN'}")


if __name__ == "__main__":
    main()
