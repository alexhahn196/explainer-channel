#!/usr/bin/env python3
"""Prueft das fertige Video gegen den Schnittplan.

Die Frage ist nicht, ob ffmpeg durchgelaufen ist — das sagt der Rueckgabewert.
Die Frage ist, ob an jeder Stelle das RICHTIGE Bild steht. Geprueft wird das,
indem an Stichproben ein Einzelbild aus dem Video gezogen und gegen alle 84
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
VIDEO = HIER / "video-01.mp4"


def histogramm(im: Image.Image) -> np.ndarray:
    a = np.asarray(im.convert("RGB").resize((64, 36), Image.LANCZOS))
    h, _ = np.histogramdd(a.reshape(-1, 3), bins=(6, 6, 6),
                          range=((0, 256), (0, 256), (0, 256)))
    h = h.ravel().astype(float)
    return h / max(h.sum(), 1)


def bild_bei(t: float) -> Image.Image:
    roh = subprocess.run(
        [FFMPEG, "-v", "error", "-ss", f"{t:.3f}", "-i", str(VIDEO),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True).stdout
    import io
    return Image.open(io.BytesIO(roh))


def main() -> None:
    plan = json.loads((HIER / "schnittplan.json").read_text(encoding="utf-8"))
    motive = {p.stem: histogramm(Image.open(p))
              for p in sorted((HIER / "bilder").glob("M*.png"))}

    schritt = max(1, len(plan) // int(sys.argv[1] if len(sys.argv) > 1 else 20))
    proben = plan[::schritt]
    treffer, fehler = 0, []
    for s in proben:
        t = s["start_s"] + s["dauer_s"] / 2          # Mitte der Einstellung
        h = histogramm(bild_bei(t))
        rang = sorted(motive, key=lambda k: float(np.abs(motive[k] - h).sum()))
        if rang[0] == s["motiv"]:
            treffer += 1
        else:
            fehler.append((s["nr"], round(t, 1), s["motiv"], rang[0], rang.index(s["motiv"]) + 1))
    print(f"Bild-zu-Plan: {treffer}/{len(proben)} Stichproben treffen das "
          f"eingetragene Motiv")
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
