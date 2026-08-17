#!/usr/bin/env python3
"""thumb_werkzeuge.py — Thumbnail-Messwerkzeuge (Teil B, THUMBNAIL).

Methodik nach dem Muster von formel/thumbnail-checkliste.md (BibelTube):
Wortzahl, Versalhoehe in % der Bildhoehe, WCAG-Kontrast Text gegen direkten
Hintergrund, Textposition, Figur ja/nein, Feed-Test 160x90. Alle Werte hier
werden SELBST gemessen — keine Schwellenwerte uebernommen.

Kommandos:
  raster   <in.jpg> <out.png>   — 5-%-Gitternetz + 160x90-Feedversion
  kontrast <in.jpg> x0 y0 x1 y1 — WCAG-Kontrast im Text-Rechteck (Anteile 0..1)

Kontrast-Methode: im angegebenen Rechteck werden die Pixel per Otsu-Schwelle
in zwei Luminanz-Cluster geteilt (Text gegen direkten Hintergrund);
berichtet wird (L_hell+0.05)/(L_dunkel+0.05) mit den Cluster-Medianen —
dieselbe Relativluminanz-Formel wie in produktion/pipeline/thumbnail.py.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw

def lum(a):
    a = np.asarray(a, np.float32) / 255
    a = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

def raster(ein, aus):
    im = Image.open(ein).convert('RGB')
    W, H = im.size
    im2 = im.copy()
    d = ImageDraw.Draw(im2)
    for pct in range(5, 100, 5):
        y = int(H * pct / 100)
        farbe = (255, 0, 255) if pct % 25 else (0, 255, 255)
        d.line([(0, y), (W, y)], fill=farbe, width=1)
        d.text((4, y + 1), f'{pct}', fill=(255, 0, 255))
    for pct in range(10, 100, 10):
        x = int(W * pct / 100)
        d.line([(x, 0), (x, H)], fill=(255, 0, 255), width=1)
    im2.save(aus)
    im.resize((160, 90), Image.LANCZOS).save(aus.rsplit('.', 1)[0] + '_160x90.png')
    print(f'{os.path.basename(ein)}: {W}x{H} -> {aus}')

def otsu(l):
    hist, kanten = np.histogram(l, bins=64, range=(0, 1))
    gesamt = l.size
    beste, schwelle = 0.0, 0.5
    w0 = 0; s0 = 0.0
    mitten = (kanten[:-1] + kanten[1:]) / 2
    s_alle = float((hist * mitten).sum())
    for i in range(64):
        w0 += hist[i]
        if w0 == 0 or w0 == gesamt:
            continue
        s0 += hist[i] * mitten[i]
        m0 = s0 / w0
        m1 = (s_alle - s0) / (gesamt - w0)
        zw = w0 * (gesamt - w0) * (m0 - m1) ** 2
        if zw > beste:
            beste, schwelle = zw, mitten[i]
    return schwelle

def kontrast(ein, x0, y0, x1, y1):
    im = Image.open(ein).convert('RGB')
    W, H = im.size
    box = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    l = lum(np.asarray(box, np.float32)).ravel()
    t = otsu(l)
    hell = np.median(l[l >= t]) if (l >= t).any() else 1.0
    dunkel = np.median(l[l < t]) if (l < t).any() else 0.0
    ratio = (hell + 0.05) / (dunkel + 0.05)
    hell_anteil = float((l >= t).mean())
    print(f'{os.path.basename(ein)} box=({x0},{y0},{x1},{y1}) '
          f'kontrast={ratio:.1f}:1 (hell {hell:.3f} / dunkel {dunkel:.3f}, '
          f'hell-Anteil {hell_anteil:.2f})')
    return round(ratio, 1)

def caphoehe(ein, x0, y0, x1, y1):
    """Versalhoehe einer EINZELNEN Textzeile im Rechteck (Anteile 0..1).

    Otsu-Binarisierung im Rechteck; Text = Minderheits-Cluster. Textzeilen =
    Zeilen, in denen der Text-Pixel-Anteil >= 4 % der Rechteckbreite ist.
    Versalhoehe = Abstand erster bis letzter solcher Zeile, in % der
    Bildhoehe. Dazu der WCAG-Kontrast beider Cluster (wie 'kontrast').
    """
    im = Image.open(ein).convert('RGB')
    W, H = im.size
    px0, py0, px1, py1 = int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)
    box = im.crop((px0, py0, px1, py1))
    l2 = lum(np.asarray(box, np.float32))
    t = otsu(l2.ravel())
    hell_anteil = float((l2 >= t).mean())
    text_ist_hell = hell_anteil < 0.5      # Minderheit = Text
    maske = (l2 >= t) if text_ist_hell else (l2 < t)
    zeilen = maske.mean(axis=1) >= 0.04
    idx = np.where(zeilen)[0]
    if idx.size == 0:
        print(f'{os.path.basename(ein)}: keine Textzeile im Rechteck gefunden')
        return None
    # Zusammenhaengende Zeilenbaender = einzelne Textzeilen. Die Versalhoehe
    # ist die Hoehe des GROESSTEN Bandes (eine Zeile), nicht die Spanne ueber
    # alle Zeilen — sonst misst man bei mehrzeiligem Text den ganzen Block.
    baender, start = [], idx[0]
    for a, b in zip(idx, idx[1:]):
        if b - a > 1:
            baender.append((start, a)); start = b
    baender.append((start, idx[-1]))
    baender = [(a, b) for a, b in baender if b - a + 1 >= 8]   # Rauschen weg
    if not baender:
        baender = [(idx[0], idx[-1])]
    groesstes = max(baender, key=lambda ab: ab[1] - ab[0])
    hoehe_px = int(groesstes[1] - groesstes[0] + 1)
    pct = round(hoehe_px / H * 100, 1)
    block_px = int(idx[-1] - idx[0] + 1)
    lt = float(np.median(l2[maske])) if maske.any() else 0.0
    lb = float(np.median(l2[~maske])) if (~maske).any() else 1.0
    ratio = round((max(lt, lb) + 0.05) / (min(lt, lb) + 0.05), 1)
    print(f'{os.path.basename(ein)}: versalhoehe {hoehe_px}px = {pct}% der '
          f'Bildhoehe ({H}px) | zeilen {len(baender)} | block {round(block_px/H*100,1)}% | '
          f'kontrast {ratio}:1 | text {"hell" if text_ist_hell else "dunkel"}')
    return pct

if __name__ == '__main__':
    if sys.argv[1] == 'raster':
        raster(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'kontrast':
        kontrast(sys.argv[2], *map(float, sys.argv[3:7]))
    elif sys.argv[1] == 'caphoehe':
        caphoehe(sys.argv[2], *map(float, sys.argv[3:7]))
