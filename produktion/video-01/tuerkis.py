#!/usr/bin/env python3
"""Zaehlt zusammenhaengende Tuerkisflaechen je Bild.

Die Signalfarbe ist #1BBFB0. Gepruefte Regel: genau EIN tuerkises Objekt je
Bild, ausser das Motiv steht in OHNE_SIGNAL. Gemessen wird, nicht geschaetzt:
Farbabstand im Lab-nahen Raum, dann Zusammenhangskomponenten mit einer
Mindestflaeche, damit Antialias-Saeume nicht als Objekt zaehlen.
"""
import sys, pathlib
import numpy as np
from PIL import Image

ZIEL = np.array([0x1B, 0xBF, 0xB0], dtype=float)
BILD = pathlib.Path("/home/user/explainer-channel/produktion/video-01/bilder")


def komponenten(maske, mindest):
    """Flood fill ueber 4er-Nachbarschaft, iterativ."""
    h, w = maske.shape
    besucht = np.zeros_like(maske, dtype=bool)
    gefunden = []
    for y in range(h):
        for x in range(w):
            if not maske[y, x] or besucht[y, x]:
                continue
            stapel = [(y, x)]
            besucht[y, x] = True
            zellen = 0
            while stapel:
                cy, cx = stapel.pop()
                zellen += 1
                for ny, nx in ((cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)):
                    if 0 <= ny < h and 0 <= nx < w and maske[ny, nx] and not besucht[ny, nx]:
                        besucht[ny, nx] = True
                        stapel.append((ny, nx))
            if zellen >= mindest:
                gefunden.append(zellen)
    return sorted(gefunden, reverse=True)


def pruefe(name, tol=52.0, mindest_promille=0.12):
    p = BILD / f"{name}.png"
    im = Image.open(p).convert("RGB")
    # herunterrechnen: Objekte bleiben zusammenhaengend, Saeume verschwinden
    im = im.resize((320, 180), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    d = np.sqrt(((a - ZIEL) ** 2).sum(axis=2))
    maske = d < tol
    # Schwarze Konturlinien zerschneiden ein einzelnes Objekt in Teilstuecke —
    # das Reliefpanel in M57 zerfaellt sonst am Loewenumriss in zehn Stuecke.
    # Zwei Runden Dilatation schliessen Linien bis 4 px Breite wieder zusammen.
    voll = maske.copy()
    for _ in range(2):
        n = voll.copy()
        n[1:, :] |= voll[:-1, :]
        n[:-1, :] |= voll[1:, :]
        n[:, 1:] |= voll[:, :-1]
        n[:, :-1] |= voll[:, 1:]
        voll = n
    mindest = max(3, int(320 * 180 * mindest_promille / 1000))
    k = komponenten(voll, mindest)
    anteil = round(maske.sum() / maske.size * 100, 2)
    return {"motiv": name, "objekte": len(k), "groessen_px": k[:6], "flaeche_pct": anteil}


if __name__ == "__main__":
    for n in sys.argv[1:]:
        r = pruefe(n)
        marke = "ok " if r["objekte"] == 1 else ("LEER" if r["objekte"] == 0 else "MEHR")
        print(f'{marke} {r["motiv"]}  Objekte={r["objekte"]}  Flaeche={r["flaeche_pct"]}%  {r["groessen_px"]}')
