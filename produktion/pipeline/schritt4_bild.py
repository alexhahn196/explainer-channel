#!/usr/bin/env python3
"""
Schritt 4 - Standbild fuer die Videospur.

**Das ist ausdruecklich kein Thumbnail.** Das Thumbnail entsteht ausserhalb
der Pipeline und wird vor dem Upload von Hand eingesetzt. Was hier entsteht,
traegt nur die Videospur und heisst deshalb im Dateinamen PLATZHALTER.

Vorgaben aus Formel §5 (PFLICHT, 11 Stichproben + 90 Thumbnails):
  - 1920x1080
  - tiefes Nachtblau/Schwarz, hoher Kontrast, dunkles Gesamtbild
  - **genau eine** warme Lichtquelle im Bild
  - gemalt, nicht fotorealistisch

Mit `--bild` wird ein extern erzeugtes Bild uebernommen und geprueft. Ohne
`--bild` erzeugt das Skript selbst einen einfachen Ersatz, damit die
Pipeline auch ohne Bildgenerator vollstaendig durchlaeuft.

Aufruf:
    python3 produktion/pipeline/schritt4_bild.py V1 --bild roh.png
    python3 produktion/pipeline/schritt4_bild.py V1
"""
import argparse
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import arbeit, config, ordner  # noqa: E402
import vorlage                                # noqa: E402

NAME = "PLATZHALTER_standbild.png"


def zuschneiden(im, b, h):
    """Auf Zielformat bringen, ohne zu verzerren."""
    im = im.convert("RGB")
    q = im.width / im.height
    z = b / h
    if abs(q - z) > 0.001:
        if q > z:
            neu = int(im.height * z)
            im = im.crop(((im.width - neu) // 2, 0, (im.width + neu) // 2, im.height))
        else:
            neu = int(im.width / z)
            im = im.crop((0, (im.height - neu) // 2, im.width, (im.height + neu) // 2))
    return im.resize((b, h), Image.LANCZOS)


def ersatzbild(b, h, saat=1):
    """Notloesung ohne Bildgenerator: Nachthimmel, Horizont, ein Feuer."""
    rnd = random.Random(saat)
    y, x = np.mgrid[0:h, 0:b]
    himmel = np.zeros((h, b, 3), np.float32)
    t = y / h
    himmel[..., 0] = 6 + 10 * (1 - t)
    himmel[..., 1] = 10 + 14 * (1 - t)
    himmel[..., 2] = 26 + 30 * (1 - t)
    boden = y > h * 0.72
    himmel[boden] *= 0.35

    for _ in range(700):                       # Sterne
        sx, sy = rnd.randrange(b), rnd.randrange(int(h * 0.72))
        hell = rnd.uniform(0.3, 1.0) * (1 - sy / h * 0.5)
        himmel[sy, sx] += 200 * hell

    mx, my, mr = int(b * 0.17), int(h * 0.17), int(h * 0.045)   # Mond
    d = np.hypot(x - mx, y - my)
    himmel += np.clip(1 - d / mr, 0, 1)[..., None] * np.array([150, 160, 185])
    himmel += (np.exp(-d / (mr * 5)) * 16)[..., None] * np.array([0.5, 0.6, 1.0])

    fx, fy = int(b * 0.72), int(h * 0.80)                        # Feuer
    d = np.hypot((x - fx) * 1.0, (y - fy) * 1.6)
    kern = np.clip(1 - d / (h * 0.035), 0, 1) ** 1.5
    schein = np.exp(-d / (h * 0.20))
    himmel += kern[..., None] * np.array([255, 170, 70])
    himmel += schein[..., None] * np.array([70, 34, 10])

    v = 1 - 0.55 * (np.hypot((x - b / 2) / (b / 2), (y - h / 2) / (h / 2)) ** 2)
    himmel *= np.clip(v, 0, 1)[..., None]
    return Image.fromarray(np.clip(himmel, 0, 255).astype(np.uint8))


def pruefen(im):
    """Misst, was Formel §5 verlangt - statt es zu behaupten."""
    a = np.asarray(im, np.float32)
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    warm = (a[..., 0] > a[..., 2] + 25) & (lum > 60)
    dunkel = lum < 60
    # Groesste zusammenhaengende warme Flaeche = "eine Lichtquelle"?
    from scipy import ndimage
    marken, n = ndimage.label(warm)
    groessen = sorted(ndimage.sum(warm, marken, range(1, n + 1)), reverse=True) if n else []
    return {
        "breite": im.width, "hoehe": im.height,
        "mittlere_helligkeit": round(float(lum.mean()), 1),
        "dunkelanteil_pct": round(float(100 * dunkel.mean()), 1),
        "warmanteil_pct": round(float(100 * warm.mean()), 2),
        "warme_flecken": n,
        "groesster_warmer_fleck_px": int(groessen[0]) if groessen else 0,
        "zweitgroesster_px": int(groessen[1]) if len(groessen) > 1 else 0,
        "kontrast_p95_zu_p5": round(float(np.percentile(lum, 95) - np.percentile(lum, 5)), 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--bild", help="extern erzeugtes Bild uebernehmen")
    a = ap.parse_args()
    cfg = config()
    b, h = int(cfg["breite"]), int(cfg["hoehe"])

    if a.bild:
        im = zuschneiden(Image.open(a.bild), b, h)
        herkunft = f"extern: {os.path.basename(a.bild)}"
    else:
        im = ersatzbild(b, h, saat=int(a.video[1:]))
        herkunft = "im Skript erzeugt (kein Bildgenerator verwendet)"

    ziel = os.path.join(ordner(a.video), NAME)
    im.save(ziel)
    p = pruefen(im)
    p["herkunft"] = herkunft
    p["datei"] = os.path.relpath(ziel, os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))
    p["motiv_vorgabe"] = vorlage.lies(a.video)["thumb_motiv"]
    json.dump(p, open(arbeit(a.video, "qa_bild.json"), "w"), ensure_ascii=False, indent=1)

    print(f"\nSTANDBILD {a.video}   ({herkunft})")
    print(f"  Auflösung             {p['breite']}×{p['hoehe']}"
          f" {'✓' if (p['breite'], p['hoehe']) == (b, h) else '✗'}")
    print(f"  mittlere Helligkeit   {p['mittlere_helligkeit']} von 255 "
          f"({p['dunkelanteil_pct']} % der Fläche dunkel)")
    print(f"  Kontrast p95−p5       {p['kontrast_p95_zu_p5']}")
    print(f"  warme Fläche          {p['warmanteil_pct']} %, größter Fleck "
          f"{p['groesster_warmer_fleck_px']} px, zweiter "
          f"{p['zweitgroesster_px']} px")
    print(f"  geschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
