#!/usr/bin/env python3
"""
thumbnail.py - legt die Textzeile auf ein Serienmotiv und misst nach.

Harte Werte aus formel/thumbnail-checkliste.md:
  - hoechstens 4 Woerter
  - Versalien, fett
  - Versalhoehe >= 11,5 % der Bildhoehe (>= 125 px bei 1080p)
  - Kontrast Text zu direktem Hintergrund >= 10:1
  - Text im oberen Drittel, weiss, zentriert
  - Export als JPEG/PNG, >= 150 KB (Gewinner-Median 237 KB)

Gemessen wird gegen den DIREKTEN Hintergrund im fertigen Bild - also nach
dem weichen dunklen Schein hinter der Schrift. Zusaetzlich wird der
Rohhintergrund ausgewiesen, damit sichtbar bleibt, wie viel der Schein
traegt.

Aufruf:
    python3 produktion/pipeline/thumbnail.py motiv-V3.png "REST TONIGHT" \
        --aus produktion/video-01/thumbnail-b.png
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SCHRIFTEN = [
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
CAP_MIN_PCT = 11.5
KONTRAST_MIN = 10.0
MAX_WOERTER = 4


def lum(a):
    a = np.asarray(a, np.float32) / 255
    a = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def kontrast(l):
    return float(1.05 / (l + 0.05))


def schrift_fuer(pfad, cap_ziel):
    """Groesse so waehlen, dass die VERSALHOEHE das Ziel trifft.

    Nicht die em-Groesse: die enthaelt Ober- und Unterlaengen, und die
    Checkliste misst die Versalhoehe.
    """
    lo, hi = 40, 500
    while hi - lo > 1:
        m = (lo + hi) // 2
        b = ImageFont.truetype(pfad, m).getbbox("T")
        if b[3] - b[1] < cap_ziel:
            lo = m
        else:
            hi = m
    f = ImageFont.truetype(pfad, hi)
    b = f.getbbox("T")
    return f, hi, b[3] - b[1]


def bauen(bild, text, aus, oben_pct=8.5, rand_min=40):
    im = Image.open(bild).convert("RGB")
    W, H = im.size
    woerter = len(text.split())
    if woerter > MAX_WOERTER:
        raise SystemExit(f"{woerter} Woerter — die Checkliste erlaubt hoechstens "
                         f"{MAX_WOERTER}.")

    cap_ziel = int(np.ceil(H * CAP_MIN_PCT / 100))
    d = ImageDraw.Draw(im)
    gewaehlt = None
    for p in SCHRIFTEN:
        if not os.path.exists(p):
            continue
        f, groesse, cap = schrift_fuer(p, cap_ziel)
        bb = d.textbbox((0, 0), text, font=f)
        breite = bb[2] - bb[0]
        if breite <= W - 2 * rand_min:
            gewaehlt = (p, f, groesse, cap, bb, breite)
            break
    if gewaehlt is None:
        raise SystemExit(
            f"'{text}' passt bei {cap_ziel} px Versalhoehe in keine der "
            f"installierten Serifen (schmalste braucht {breite} px von "
            f"{W - 2*rand_min} px). Woerter kuerzen — nicht die Schrift "
            f"verkleinern (Checkliste).")
    p, font, groesse, cap, bb, breite = gewaehlt

    x = (W - breite) // 2 - bb[0]
    y = int(H * oben_pct / 100) - bb[1]

    maske = Image.new("L", (W, H), 0)
    ImageDraw.Draw(maske).text((x, y), text, font=font, fill=255)
    mk = np.asarray(maske) > 128

    L_roh = lum(np.asarray(im, np.float32))[mk]
    schein = maske.filter(ImageFilter.GaussianBlur(12))
    dunkel = Image.new("RGB", (W, H), (6, 9, 18))
    im2 = Image.composite(dunkel, im, schein.point(lambda v: int(v * 0.6)))
    L_fertig = lum(np.asarray(im2, np.float32))[mk]
    ImageDraw.Draw(im2).text((x, y), text, font=font, fill=(255, 255, 255))
    im2.save(aus)
    im2.resize((160, 90), Image.LANCZOS).save(
        aus.rsplit(".", 1)[0] + "_160x90.png")

    b = {
        "datei": os.path.basename(aus), "text": text, "woerter": woerter,
        "schrift": os.path.basename(p), "fontgroesse_px": groesse,
        "versalhoehe_px": int(cap), "versalhoehe_pct": round(cap / H * 100, 2),
        "textbreite_px": int(breite), "rand_je_seite_px": int((W - breite) // 2),
        "kontrast_direkt_mittel": round(kontrast(float(L_fertig.mean())), 1),
        "kontrast_direkt_p95": round(kontrast(float(np.percentile(L_fertig, 95))), 1),
        "kontrast_roh_mittel": round(kontrast(float(L_roh.mean())), 1),
        "kontrast_roh_p95": round(kontrast(float(np.percentile(L_roh, 95))), 1),
        "groesse_kb": round(os.path.getsize(aus) / 1000, 1),
    }
    b["cap_ok"] = bool(b["versalhoehe_pct"] >= CAP_MIN_PCT)
    b["kontrast_ok"] = bool(b["kontrast_direkt_p95"] >= KONTRAST_MIN)
    b["woerter_ok"] = bool(woerter <= MAX_WOERTER)
    b["bestanden"] = bool(b["cap_ok"] and b["kontrast_ok"] and b["woerter_ok"])
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bild")
    ap.add_argument("text")
    ap.add_argument("--aus", required=True)
    a = ap.parse_args()
    b = bauen(a.bild, a.text, a.aus)
    print(f"\n{b['datei']}   „{b['text']}\"")
    print(f"  Wörter                {b['woerter']} {'✓' if b['woerter_ok'] else '✗'} (max 4)")
    print(f"  Versalhöhe            {b['versalhoehe_px']} px = {b['versalhoehe_pct']} % "
          f"{'✓' if b['cap_ok'] else '✗'} (≥ 11,5 % / ≥ 125 px)")
    print(f"  Schrift               {b['schrift']} @ {b['fontgroesse_px']} px, "
          f"Breite {b['textbreite_px']} px, Rand {b['rand_je_seite_px']} px")
    print(f"  Kontrast (direkt)     Mittel {b['kontrast_direkt_mittel']}:1, "
          f"p95 {b['kontrast_direkt_p95']}:1 {'✓' if b['kontrast_ok'] else '✗'} (≥ 10:1)")
    print(f"  Kontrast (roh)        Mittel {b['kontrast_roh_mittel']}:1, "
          f"p95 {b['kontrast_roh_p95']}:1")
    print(f"  Dateigröße            {b['groesse_kb']} kB")
    print(f"  → {'BESTANDEN' if b['bestanden'] else 'DURCHGEFALLEN'}")
    json.dump(b, open(a.aus.rsplit(".", 1)[0] + "_messung.json", "w"),
              ensure_ascii=False, indent=1)
    return 0 if b["bestanden"] else 1


if __name__ == "__main__":
    sys.exit(main())
