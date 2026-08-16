#!/usr/bin/env python3
"""Thumbnails messen: Palette, Kontrast, Farbflaechen. Plus 160x90-Kontaktbogen."""
import csv
import os
from collections import Counter

import numpy as np
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))


def lade(vid):
    im = Image.open(os.path.join(DIR, f'{vid}.jpg')).convert('RGB')
    return im


def luminanz(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def palette(im, n=6):
    q = im.convert('P', palette=Image.ADAPTIVE, colors=n).convert('RGB')
    a = np.asarray(q).reshape(-1, 3)
    cnt = Counter(map(tuple, a))
    tot = sum(cnt.values())
    return [(f'#{r:02X}{g:02X}{b:02X}', 100 * c / tot) for (r, g, b), c in cnt.most_common(n)]


def saettigung(a):
    mx = a.max(axis=2).astype(float)
    mn = a.min(axis=2).astype(float)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    return s.mean()


def kantendichte(a):
    """Anteil der Pixel mit starkem lokalem Luminanzsprung — Mass fuer Detailmenge."""
    L = luminanz(a)
    gx = np.abs(np.diff(L, axis=1))[:-1, :]
    gy = np.abs(np.diff(L, axis=0))[:, :-1]
    return float(((gx + gy) > 40).mean())


rows = []
with open(os.path.join(DIR, 'ids.txt'), encoding='utf-8') as f:
    for r in csv.reader(f, delimiter='\t'):
        if len(r) < 3:
            continue
        vid, views, titel = r[0], int(r[1]), r[2]
        im = lade(vid)
        a = np.asarray(im).astype(np.uint8)
        L = luminanz(a)
        pal = palette(im)
        rows.append({
            'vid': vid, 'views': views, 'titel': titel,
            'groesse': f'{im.width}x{im.height}',
            'lum_mittel': L.mean(), 'lum_sd': L.std(),
            'kontrast_p95_p5': np.percentile(L, 95) - np.percentile(L, 5),
            'saettigung': saettigung(a),
            'kantendichte': kantendichte(a),
            'dunkelanteil': float((L < 60).mean()),
            'hellanteil': float((L > 200).mean()),
            'palette': ' '.join(f'{h}:{p:.0f}%' for h, p in pal[:4]),
        })

rows.sort(key=lambda r: -r['views'])
print(f"{'Video':13}{'Views':>9}{'Groesse':>11}{'Lum':>6}{'Kontr':>7}{'Saett':>7}"
      f"{'Kanten':>8}{'dunkel':>8}{'hell':>7}")
for r in rows:
    print(f"{r['vid']:13}{r['views']:>9,}{r['groesse']:>11}{r['lum_mittel']:>6.0f}"
          f"{r['kontrast_p95_p5']:>7.0f}{r['saettigung']:>7.2f}{r['kantendichte']:>8.3f}"
          f"{r['dunkelanteil']:>8.2f}{r['hellanteil']:>7.2f}")

print('\nPaletten (4 groesste Flaechen je Thumbnail):')
for r in rows:
    print(f"  {r['vid']:13} {r['palette']}")

import statistics as st
print('\nMediane ueber alle 16:')
for k in ('lum_mittel', 'kontrast_p95_p5', 'saettigung', 'kantendichte', 'dunkelanteil'):
    print(f"  {k:18} {st.median(r[k] for r in rows):.3f}")

# gemeinsame Palette ueber alle 16
gross = Image.new('RGB', (16 * 160, 90))
for i, r in enumerate(rows):
    gross.paste(lade(r['vid']).resize((160, 90), Image.LANCZOS), (i * 160, 0))
print('\nGemeinsame Palette aller 16 Thumbnails:')
for h, p in palette(gross, 8):
    print(f'  {h}  {p:5.1f}%')

# Kontaktbogen 4x4 aus 160x90-Kacheln
KB = Image.new('RGB', (4 * 160, 4 * 90), (24, 24, 24))
for i, r in enumerate(rows):
    KB.paste(lade(r['vid']).resize((160, 90), Image.LANCZOS), ((i % 4) * 160, (i // 4) * 90))
KB.save(os.path.join(DIR, 'kontaktbogen-160x90.png'))
print(f"\nKontaktbogen: {KB.width}x{KB.height} -> kontaktbogen-160x90.png")

with open(os.path.join(DIR, 'messwerte.tsv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
    w.writeheader()
    w.writerows(rows)
