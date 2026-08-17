#!/usr/bin/env python3
"""Stellt die sechs Testmotive alt gegen neu.

Zwei Ausgaben, weil zwei verschiedene Fragen dahinterstehen:

  * `paar-MXX.png` — beide Fassungen in voller Breite nebeneinander. Hier ist
    zu sehen, was die Farbe mit dem einzelnen Bild macht.
  * `raster-160x90.png` — alle zwoelf in Briefmarkengroesse. Das ist die
    haertere Pruefung: bei 160x90 verschwindet jedes Detail, und was uebrig
    bleibt, ist genau das, was die Serie zusammenhaelt oder eben nicht.

Die alten Fassungen liegen in `produktion/video-01/bilder/`, die neuen hier
daneben. Video 1 wird dabei nicht angefasst.
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw

HIER = pathlib.Path(__file__).resolve().parent
ALT = HIER.parent.parent / "produktion" / "video-01" / "bilder"

MOTIVE = [
    ("M08", "Moor — Somerset, Neolithikum"),
    ("M45", "Wueste — Aegypten, Altes Reich"),
    ("M56", "Babylon — glasierte Reliefwaende"),
    ("M67", "Anden — Inka"),
    ("M76", "Schema — Strassenquerschnitt"),
    ("M01", "Gegenwart — Haustuer, Asphalt"),
]


def paare(breite: int = 900) -> None:
    hoehe = int(breite * 9 / 16)
    kopf = 26
    for mid, titel in MOTIVE:
        a, n = ALT / f"{mid}.png", HIER / f"{mid}.png"
        if not (a.exists() and n.exists()):
            print(f"  {mid}: fehlt")
            continue
        blatt = Image.new("RGB", (breite * 2 + 12, hoehe + kopf), "white")
        z = ImageDraw.Draw(blatt)
        for i, (p, marke) in enumerate(((a, "ALT — Themenpalette + Tuerkis"),
                                        (n, "NEU — natuerliche Farben"))):
            im = Image.open(p).convert("RGB").resize((breite, hoehe), Image.LANCZOS)
            x = i * (breite + 12)
            blatt.paste(im, (x, kopf))
            z.text((x + 6, 6), f"{mid}  {marke}", fill="black")
        blatt.save(HIER / f"paar-{mid}.png", quality=92)
        print(f"  paar-{mid}.png  {titel}")


def raster() -> None:
    """Alle zwoelf bei 160x90, alt ueber neu, damit die Spalten vergleichbar sind."""
    b, h, rand, kopf = 160, 90, 10, 18
    blatt = Image.new("RGB", (len(MOTIVE) * (b + rand) + rand,
                              2 * (h + kopf) + rand * 2 + 14), "white")
    z = ImageDraw.Draw(blatt)
    for spalte, (mid, _) in enumerate(MOTIVE):
        x = rand + spalte * (b + rand)
        z.text((x, 4), mid, fill="black")
        for zeile, ordner in enumerate((ALT, HIER)):
            p = ordner / f"{mid}.png"
            if not p.exists():
                continue
            y = 16 + zeile * (h + kopf)
            blatt.paste(Image.open(p).convert("RGB").resize((b, h), Image.LANCZOS), (x, y))
            z.text((x, y + h + 2), "alt" if zeile == 0 else "neu", fill="black")
    blatt.save(HIER / "raster-160x90.png")
    print(f"  raster-160x90.png  {blatt.size}")


def farbmass() -> None:
    """Wie bunt ist es geworden? Saettigung und Zahl der Farbtoene, alt gegen neu."""
    import numpy as np
    print(f"\n{'Motiv':6s} {'Saettigung alt':>15s} {'neu':>7s} "
          f"{'Farbtoene alt':>14s} {'neu':>6s}")
    for mid, _ in MOTIVE:
        werte = []
        for ordner in (ALT, HIER):
            p = ordner / f"{mid}.png"
            if not p.exists():
                werte.append((float("nan"), 0))
                continue
            im = Image.open(p).convert("HSV").resize((320, 180), Image.LANCZOS)
            a = np.asarray(im)
            s = a[:, :, 1].astype(float) / 255
            # Farbtoene nur dort zaehlen, wo ueberhaupt Farbe ist
            bunt = a[:, :, 1] > 40
            toene = len(np.unique(a[:, :, 0][bunt] // 8)) if bunt.any() else 0
            werte.append((float(s.mean()), toene))
        (sa, ta), (sn, tn) = werte
        print(f"{mid:6s} {sa:15.3f} {sn:7.3f} {ta:14d} {tn:6d}")


if __name__ == "__main__":
    paare()
    raster()
    farbmass()
