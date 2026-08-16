#!/usr/bin/env python3
"""Element-Test: Haelt der Balkenkopf ueber alle vier Szenen?

Misst je Szene die Geometrie des Balkens im Verhaeltnis zum Kopf, die Kopfgroesse,
die Palette und die Bilddichte. Laeuft ohne Argumente.
"""
import itertools
import os
from collections import Counter

import numpy as np
from PIL import Image
from scipy import ndimage

DIR = os.path.dirname(os.path.abspath(__file__))
S = ['szeneA', 'szeneB', 'szeneC', 'szeneD']
PERSON = {'szeneA', 'szeneC'}     # Klassifikation wie im letzten Lauf beibehalten
SACHE = {'szeneB', 'szeneD'}
INDIGO = np.array([0x1F, 0x3A, 0x5F], float)


def srgb2lab(rgb):
    c = np.asarray(rgb, float) / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], -1)


def lade(s):
    return Image.open(os.path.join(DIR, f'{s}.png')).convert('RGB')


def balken_und_kopf(im):
    """Findet den Indigo-Balken und den ihn umschliessenden Kopf.

    Der Kopf wird ueber seine helle Fuellflaeche bestimmt, nicht ueber die Kontur:
    die schwarze Kontur trennt den Kopf vom (oft ebenfalls hellen) Hintergrund,
    der Balken teilt die Kopfflaeche in Stirn und Wangenpartie. Beide Teile werden
    wieder zusammengefasst.
    """
    a = np.asarray(im).astype(float)
    H, W = a.shape[:2]
    nah = np.linalg.norm(a - INDIGO, axis=2) < 60
    lab, n = ndimage.label(nah)
    if n == 0:
        return None
    best = None
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h == 0 or w == 0:
            continue
        flaeche = (lab[sl] == i).sum()
        if w / h < 2.2 or w < W * 0.03 or w > W * 0.35:
            continue
        if sl[0].start > H * 0.75 or flaeche / (h * w) < 0.45:
            continue
        if best is None or flaeche > best[0]:
            best = (flaeche, sl, h, w)
    if best is None:
        return None
    _, sl, bh, bw = best
    cy = (sl[0].start + sl[0].stop) // 2
    cx = (sl[1].start + sl[1].stop) // 2

    # helle Kopffuellung: nahe #F2EDE3, ohne Kontur und ohne Balken
    hell = np.linalg.norm(a - np.array([0xF2, 0xED, 0xE3], float), axis=2) < 42
    L = srgb2lab(a)[..., 0]
    hell &= (L > 60) & ~nah
    hlab, hn = ndimage.label(hell)
    if hn == 0:
        return None
    # Teile, die waagerecht mit dem Balken ueberlappen und ihn senkrecht beruehren
    teile = []
    for i, hsl in enumerate(ndimage.find_objects(hlab), start=1):
        if hsl[1].stop < sl[1].start or hsl[1].start > sl[1].stop:
            continue
        if hsl[0].stop < sl[0].start - bh * 3 or hsl[0].start > sl[0].stop + bh * 6:
            continue
        flaeche = (hlab[hsl] == i).sum()
        breite = hsl[1].stop - hsl[1].start
        if breite > W * 0.5 or flaeche < bw * bh * 0.3:
            continue
        teile.append(hsl)
    if not teile:
        return None
    oben = min(t[0].start for t in teile)
    unten = max(t[0].stop for t in teile)
    links = min(t[1].start for t in teile)
    rechts = max(t[1].stop for t in teile)
    kopfbreite = rechts - links
    kopfhoehe = unten - oben
    if kopfbreite <= 0 or kopfhoehe <= 0:
        return None
    return {
        'balken_breite': bw, 'balken_hoehe': bh,
        'balken_zu_kopf_breite': bw / kopfbreite,
        'balken_dicke_zu_kopf': bh / kopfhoehe,
        'balken_lage_im_kopf': (cy - oben) / kopfhoehe,
        'kopfbreite_px': kopfbreite, 'kopfhoehe_px': kopfhoehe,
        'kopf_zu_bildhoehe': kopfhoehe / H,
        'kopf_mitte': (cx, cy),
    }


def palette(im, n=8):
    q = im.convert('P', palette=Image.ADAPTIVE, colors=n).convert('RGB')
    arr = np.asarray(q).reshape(-1, 3)
    cnt = Counter(map(tuple, arr))
    tot = sum(cnt.values())
    return [(np.array(c, float), v / tot) for c, v in cnt.most_common(n)]


def pal_abstand(p1, p2):
    L1 = srgb2lab(np.array([c for c, _ in p1]))
    L2 = srgb2lab(np.array([c for c, _ in p2]))
    d = np.linalg.norm(L1[:, None, :] - L2[None, :, :], axis=2)
    w = np.array([w for _, w in p1])
    return float((d.min(axis=1) * w).sum() / w.sum())


def dichte(im):
    a = np.asarray(im.resize((1376, 768), Image.LANCZOS)).astype(float)
    L = srgb2lab(a)[..., 0]
    gx = np.abs(np.diff(L, axis=1))[:-1, :]
    gy = np.abs(np.diff(L, axis=0))[:, :-1]
    kanten = (gx + gy) > 12
    lab, n = ndimage.label(~kanten)
    gr = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    objekte = int((gr > a.shape[0] * a.shape[1] * 0.0008).sum())
    pal = palette(im, 8)
    mx = np.asarray(im).max(axis=2).astype(float)
    mn = np.asarray(im).min(axis=2).astype(float)
    return {'kanten': float(kanten.mean()), 'objekte': objekte,
            'farbflaeche': 1.0 - sum(w for _, w in pal[:2]),
            'saettigung': float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0).mean())}


print('=' * 88)
print('GESICHTSGEOMETRIE — haelt der Balkenkopf?')
print('=' * 88)
G = {}
for s in S:
    G[s] = balken_und_kopf(lade(s))
print(f"{'Szene':9}{'Balken px':>11}{'Balken/Kopf':>13}{'Dicke/Kopf':>12}"
      f"{'Lage im Kopf':>14}{'Kopf px':>9}{'Kopf/Bildh.':>13}")
for s in S:
    g = G[s]
    if not g:
        print(f'{s:9}   KEIN BALKEN GEFUNDEN')
        continue
    print(f"{s:9}{g['balken_breite']:>11}{g['balken_zu_kopf_breite']:>13.3f}"
          f"{g['balken_dicke_zu_kopf']:>12.3f}{g['balken_lage_im_kopf']:>14.3f}"
          f"{g['kopfbreite_px']:>9}{g['kopf_zu_bildhoehe']:>13.3f}")

ok = [s for s in S if G[s]]
print(f'\nFigur mit Balkenkopf gefunden in {len(ok)} von 4 Szenen: {", ".join(ok)}')
if len(ok) > 1:
    for feld, name in (('balken_zu_kopf_breite', 'Balkenbreite / Kopfbreite'),
                       ('balken_dicke_zu_kopf', 'Balkendicke / Kopfhoehe'),
                       ('balken_lage_im_kopf', 'Lage des Balkens im Kopf')):
        xs = np.array([G[s][feld] for s in ok])
        print(f'  {name:28} Mittel {xs.mean():.3f}  SD {xs.std():.3f}  '
              f'Spanne {xs.min():.3f}-{xs.max():.3f}  Streuung {100*xs.std()/xs.mean():.1f} %')

print('\n' + '=' * 88)
print('PALETTE UND DICHTE')
print('=' * 88)
D = {s: dichte(lade(s)) for s in S}
print(f"{'Szene':9}{'Kanten':>10}{'Objekte':>9}{'Farbflaeche':>13}{'Saettigung':>12}")
for s in S:
    d = D[s]
    print(f"{s:9}{d['kanten']:>10.4f}{d['objekte']:>9}{d['farbflaeche']:>13.3f}{d['saettigung']:>12.3f}")

pals = {s: palette(lade(s)) for s in S}
paare = [pal_abstand(pals[a], pals[b]) for a, b in itertools.combinations(S, 2)]
print(f'\nPalettenabstand zwischen den Szenen: Mittel {np.mean(paare):.2f}  '
      f'Spanne {min(paare):.2f}-{max(paare):.2f}')
for f, n in (('kanten', 'Kanten'), ('objekte', 'Objekte'),
             ('farbflaeche', 'Farbflaeche'), ('saettigung', 'Saettigung')):
    xs = np.array([D[s][f] for s in S], float)
    print(f'  {n:12} SD {xs.std():.4f}')

kp = np.mean([D[s]['kanten'] for s in S if s in PERSON])
ks = np.mean([D[s]['kanten'] for s in S if s in SACHE])
op = np.mean([D[s]['objekte'] for s in S if s in PERSON])
osa = np.mean([D[s]['objekte'] for s in S if s in SACHE])
print(f'\nDichte Personenszenen (A, C) gegen Sachszenen (B, D):')
print(f'  Kanten  {kp:.4f} -> {ks:.4f} = {ks/kp:.2f}x')
print(f'  Objekte {op:.0f} -> {osa:.0f} = {osa/op:.2f}x')
print('  Vergleich letzter Lauf ohne Dichtebremse: V1 1,45x · V2 1,66x · V3 1,50x (Kanten)')
