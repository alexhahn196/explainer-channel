#!/usr/bin/env python3
"""Varianten messen: Konsistenz ueber die Szenen, Dichte Person gegen Sache,
Abstand zum gemessenen Original."""
import itertools
import os

import numpy as np
from PIL import Image
from scipy import ndimage

DIR = os.path.dirname(os.path.abspath(__file__))
V = ['v1', 'v2', 'v3']
S = ['szeneA', 'szeneB', 'szeneC', 'szeneD']
PERSON = {'szeneA', 'szeneC'}      # Personenszenen laut Auftrag
SACHE = {'szeneB', 'szeneD'}       # Sachszenen

# gemessenes Original: Videopaletten (beide Fassungen) und Thumbnail-Gesamtpalette
ORIG_VIDEO = ['#6B704C', '#708090', '#5C534E', '#F5F5DC', '#B22222',
              '#D8A484', '#8B5E3C', '#5B8C9E', '#8FBC8F', '#C2B280', '#D4AF37']
ORIG_THUMB = ['#36342E', '#FFFEFC', '#94795A', '#070606',
              '#4D636E', '#6F3630', '#1A2933', '#C1C5BE']


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


def srgb2lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], -1)


def lade(v, s):
    return Image.open(os.path.join(DIR, f'{v}-{s}.png')).convert('RGB')


def palette(im, n=8):
    q = im.convert('P', palette=Image.ADAPTIVE, colors=n).convert('RGB')
    a = np.asarray(q).reshape(-1, 3)
    from collections import Counter
    cnt = Counter(map(tuple, a))
    tot = sum(cnt.values())
    return [(np.array(c, float), v / tot) for c, v in cnt.most_common(n)]


def pal_abstand(p1, p2):
    """Gewichteter Erdbewegungs-Ersatz: je Farbe aus p1 die naechste in p2, gewichtet."""
    L1 = srgb2lab(np.array([c for c, _ in p1]))
    L2 = srgb2lab(np.array([c for c, _ in p2]))
    d = np.linalg.norm(L1[:, None, :] - L2[None, :, :], axis=2)
    w = np.array([w for _, w in p1])
    return float((d.min(axis=1) * w).sum() / w.sum())


def kennwerte(im):
    a = np.asarray(im.resize((1376, 768), Image.LANCZOS)).astype(float)
    L = srgb2lab(a)[..., 0]
    gx = np.abs(np.diff(L, axis=1))[:-1, :]
    gy = np.abs(np.diff(L, axis=0))[:, :-1]
    kanten = (gx + gy) > 12
    kantendichte = float(kanten.mean())
    # Objektzahl: geschlossene Flaechen zwischen den Konturen, ab Mindestgroesse
    lab, n = ndimage.label(~kanten)
    groessen = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    objekte = int((groessen > (a.shape[0] * a.shape[1]) * 0.0008).sum())
    # Farbflaechenanteil: Pixel ausserhalb der zwei groessten Farbcluster
    pal = palette(im, 8)
    gross = sum(w for _, w in pal[:2])
    farbflaeche = 1.0 - gross
    mx = np.asarray(im).max(axis=2).astype(float)
    mn = np.asarray(im).min(axis=2).astype(float)
    saett = float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0).mean())
    return {'kanten': kantendichte, 'objekte': objekte,
            'farbflaeche': farbflaeche, 'saettigung': saett}


print('=' * 92)
print('KENNWERTE JE BILD')
print('=' * 92)
print(f"{'Bild':14}{'Kantendichte':>14}{'Objekte':>9}{'Farbflaeche':>13}{'Saettigung':>12}")
K = {}
for v in V:
    for s in S:
        K[(v, s)] = kennwerte(lade(v, s))
        k = K[(v, s)]
        print(f"{v + '-' + s:14}{k['kanten']:>14.4f}{k['objekte']:>9}"
              f"{k['farbflaeche']:>13.3f}{k['saettigung']:>12.3f}")

print('\n' + '=' * 92)
print('KONSISTENZ UEBER DIE VIER SZENEN  (kleiner = konsistenter)')
print('=' * 92)
print(f"{'Variante':10}{'Palettenabstand':>18}{'Kanten SD':>12}{'Objekte SD':>12}"
      f"{'Farbfl. SD':>12}{'Saett. SD':>11}")
konsis = {}
for v in V:
    pals = {s: palette(lade(v, s)) for s in S}
    paare = [pal_abstand(pals[a], pals[b]) for a, b in itertools.combinations(S, 2)]
    pd = float(np.mean(paare))
    ks = float(np.std([K[(v, s)]['kanten'] for s in S]))
    os_ = float(np.std([K[(v, s)]['objekte'] for s in S]))
    fs = float(np.std([K[(v, s)]['farbflaeche'] for s in S]))
    ss = float(np.std([K[(v, s)]['saettigung'] for s in S]))
    konsis[v] = {'palette': pd, 'kanten_sd': ks, 'objekte_sd': os_,
                 'farb_sd': fs, 'saett_sd': ss}
    print(f"{v:10}{pd:>18.2f}{ks:>12.4f}{os_:>12.1f}{fs:>12.3f}{ss:>11.3f}")

# Gesamtrang: z-Werte der vier Streuungsmasse plus Palettenabstand
print('\nZusammengefasster Schwankungsindex (Mittel der z-Werte, kleiner = ruhiger):')
felder = ['palette', 'kanten_sd', 'objekte_sd', 'farb_sd', 'saett_sd']
z = {v: 0.0 for v in V}
for f in felder:
    xs = np.array([konsis[v][f] for v in V], float)
    sd = xs.std() or 1.0
    for i, v in enumerate(V):
        z[v] += (xs[i] - xs.mean()) / sd
for v in sorted(V, key=lambda v: z[v]):
    print(f'  {v}: {z[v] / len(felder):+.3f}')

print('\n' + '=' * 92)
print('DICHTE: PERSONENSZENEN (A, C) GEGEN SACHSZENEN (B, D)')
print('=' * 92)
print(f"{'Variante':10}{'Kanten P':>10}{'Kanten S':>10}{'Faktor':>8}"
      f"{'Obj. P':>8}{'Obj. S':>8}{'Faktor':>8}{'Farbfl. P':>11}{'Farbfl. S':>11}{'Faktor':>8}")
for v in V:
    kp = np.mean([K[(v, s)]['kanten'] for s in S if s in PERSON])
    ks = np.mean([K[(v, s)]['kanten'] for s in S if s in SACHE])
    op = np.mean([K[(v, s)]['objekte'] for s in S if s in PERSON])
    osa = np.mean([K[(v, s)]['objekte'] for s in S if s in SACHE])
    fp = np.mean([K[(v, s)]['farbflaeche'] for s in S if s in PERSON])
    fs = np.mean([K[(v, s)]['farbflaeche'] for s in S if s in SACHE])
    print(f"{v:10}{kp:>10.4f}{ks:>10.4f}{ks / kp:>8.2f}{op:>8.0f}{osa:>8.0f}"
          f"{osa / op:>8.2f}{fp:>11.3f}{fs:>11.3f}{fs / fp if fp else 0:>8.2f}")

print('\n' + '=' * 92)
print('ABSTAND ZUM GEMESSENEN ORIGINAL  (Lab, groesser = weiter weg)')
print('=' * 92)
ov = [(hex2rgb(h), 1 / len(ORIG_VIDEO)) for h in ORIG_VIDEO]
ot = [(hex2rgb(h), 1 / len(ORIG_THUMB)) for h in ORIG_THUMB]
print(f"{'Variante':10}{'zu Videopalette':>18}{'zu Thumbpalette':>18}")
for v in V:
    pv = np.mean([pal_abstand(palette(lade(v, s)), ov) for s in S])
    pt = np.mean([pal_abstand(palette(lade(v, s)), ot) for s in S])
    print(f'{v:10}{pv:>18.2f}{pt:>18.2f}')
