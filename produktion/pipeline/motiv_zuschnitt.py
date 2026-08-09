#!/usr/bin/env python3
"""
Motiv-Zuschnitt: eingebrannte Letterbox-Balken entfernen und auf 1920x1080
bringen — ohne Hochrechnung.

Hintergrund: nano-banana liefert bei 16:9 gelegentlich ein Bild mit gemalten
schwarzen Balken oben und unten (Kinoformat im Bild statt am Bildrand). Der
Prompt-Zusatz "no letterbox" hilft nicht zuverlaessig. Dieses Skript misst die
Balken, schneidet sie weg, beschneidet das verbleibende Breitband mittig auf
16:9 und skaliert **herunter** auf 1920x1080.

Bedingung: das Nutzband muss nach dem Balkenschnitt mindestens 1080 px hoch
sein, sonst muesste hochgerechnet werden — das Skript bricht dann ab.

Aufruf:
    python3 produktion/pipeline/motiv_zuschnitt.py roh.png ziel.png
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

BREITE, HOEHE = 1920, 1080
# Zeilen mit einer 99,5-%-Luminanz darunter gelten als schwarzer Balken.
# Gemessene Trennung: Balken liegen bei 13-25, Bildinhalt ab ~60.
BALKEN_SCHWELLE = 40.0


def luminanz(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    return 0.2126 * a[:, :, 0] + 0.7152 * a[:, :, 1] + 0.0722 * a[:, :, 2]


def balken_messen(lum):
    """Balkenhoehe oben und unten. Robust gegen einzelne helle Pixel."""
    p = np.percentile(lum, 99.5, axis=1)
    h = len(p)
    oben = 0
    while oben < h and p[oben] < BALKEN_SCHWELLE:
        oben += 1
    unten = 0
    while unten < h - oben and p[h - 1 - unten] < BALKEN_SCHWELLE:
        unten += 1
    return oben, unten, p


def zonen_pruefen(lum):
    """Formel-Vorgaben: ruhiges oberes Sechstel (Thumbnail-Text) und ruhiges
    unteres Achtel (Untertitel)."""
    h, w = lum.shape
    oben = lum[: h // 6]
    unten = lum[-(h // 8) :]
    drittel = lum[: h // 3]
    return {
        "oberes_sechstel_p95": round(float(np.percentile(oben, 95)), 1),
        "unteres_achtel_p95": round(float(np.percentile(unten, 95)), 1),
        "oberes_drittel_hell_pct": round(
            float((drittel > 60).sum()) * 100 / drittel.size, 2
        ),
        "gesamt_mittel": round(float(lum.mean()), 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quelle")
    ap.add_argument("ziel")
    ap.add_argument("--messung", help="Pfad fuer die JSON-Messwerte")
    a = ap.parse_args()

    im = Image.open(a.quelle).convert("RGB")
    lum = luminanz(im)
    h, w = lum.shape
    oben, unten, profil = balken_messen(lum)

    nutz_h = h - oben - unten
    print(f"Quelle      {w}x{h}")
    print(f"Balken oben {oben:4d} px ({100*oben/h:.1f} %)   "
          f"Uebergang p99.5: {profil[max(oben-3,0)]:.0f} -> {profil[min(oben+2,h-1)]:.0f}")
    print(f"Balken unten{unten:4d} px ({100*unten/h:.1f} %)   "
          f"Uebergang p99.5: {profil[h-unten+2] if unten>2 else float('nan'):.0f} "
          f"<- {profil[h-unten-3]:.0f}")
    print(f"Nutzband    {w}x{nutz_h} = {w/nutz_h:.3f}:1")

    if nutz_h < HOEHE:
        raise SystemExit(
            f"ABBRUCH: Nutzband nur {nutz_h} px hoch, 1080 noetig — "
            "das waere Hochrechnung."
        )

    # Balken weg
    band = im.crop((0, oben, w, h - unten))

    # Breite mittig auf 16:9
    ziel_b = int(round(nutz_h * BREITE / HOEHE))
    if ziel_b > w:
        raise SystemExit(f"ABBRUCH: fuer 16:9 waeren {ziel_b} px Breite noetig, da sind {w}.")
    links = (w - ziel_b) // 2
    schnitt = band.crop((links, 0, links + ziel_b, nutz_h))
    verlust_pct = 100 * (w - ziel_b) / 2 / w
    faktor = BREITE / ziel_b
    print(f"Breitenschnitt {w} -> {ziel_b} px  (je Seite {links} px = {verlust_pct:.1f} %)")
    print(f"Skalierung  {ziel_b}x{nutz_h} -> {BREITE}x{HOEHE}  Faktor {faktor:.3f}"
          f"  ({'Verkleinerung' if faktor <= 1 else 'HOCHRECHNUNG'})")

    fertig = schnitt.resize((BREITE, HOEHE), Image.LANCZOS)
    fertig.save(a.ziel)

    # Restbalken-Kontrolle am Ergebnis
    rest_o, rest_u, _ = balken_messen(luminanz(fertig))
    zonen = zonen_pruefen(luminanz(fertig))
    print(f"Ergebnis    Restbalken oben {rest_o} px, unten {rest_u} px")
    print(f"Zonen       {zonen}")

    if a.messung:
        with open(a.messung, "w") as f:
            json.dump(
                {
                    "quelle": os.path.basename(a.quelle),
                    "quelle_groesse": [w, h],
                    "balken_oben_px": oben,
                    "balken_unten_px": unten,
                    "balken_oben_pct": round(100 * oben / h, 1),
                    "balken_unten_pct": round(100 * unten / h, 1),
                    "nutzband": [w, nutz_h],
                    "breitenschnitt_je_seite_px": links,
                    "breitenverlust_je_seite_pct": round(verlust_pct, 1),
                    "skalierfaktor": round(faktor, 3),
                    "ergebnis": [BREITE, HOEHE],
                    "restbalken_oben_px": rest_o,
                    "restbalken_unten_px": rest_u,
                    "zonen": zonen,
                },
                f,
                indent=2,
            )


if __name__ == "__main__":
    main()
