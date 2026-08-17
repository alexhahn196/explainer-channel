#!/usr/bin/env python3
"""Stichprobenlauf: haelt der Balkenkopf ueber 12 Ansichten und neben Bildtext?

WARUM HALBAUTOMATISCH — und nicht wie im Elementtest vollautomatisch:

Die Messung aus `recherche/stil-uf-element/_bewertung.py` findet Balken und Kopf
selbstaendig. Sie funktioniert dort, weil alle vier Testszenen nach demselben
Muster gebaut waren: Figur frontal, aufrecht, vor kontrolliertem Hintergrund.

Auf diesem Material scheitert sie reproduzierbar an drei Stellen:
  * **Geneigte Balken** (kniend, gebueckt) fallen durch das Seitenverhaeltnis-Sieb
    der achsenparallelen Bounding-Box.
  * **Kopf und Papiergrund sind beide #F2EDE3.** Die helle Flaeche laeuft ueber
    Hals, Arme und Horizont hinaus; gemessene Kopfhoehen bis 91 % der Bildhoehe
    sind die Folge.
  * **Fehlfunde in figurlosen Bildern**: jede laengliche Indigoflaeche (Bohle,
    Loewe, Wasserlauf) wird als Balken erkannt.

Deshalb wird hier die **Kopfregion je Bild von Hand gesetzt** (Tabelle KOPF,
relative Koordinaten, im Skript nachlesbar und damit reproduzierbar) und **nur
noch der Balken darin automatisch vermessen**. Die Verhaeltniswerte bleiben mit
dem Elementtest vergleichbar; die Kopfabgrenzung ist Augenmass, keine Messung.
"""
import glob, json, os
import numpy as np
from PIL import Image
from scipy import ndimage

DIR = os.path.dirname(os.path.abspath(__file__))
INDIGO = np.array([0x1F, 0x3A, 0x5F], float)

# Kopfregion je Bild, relativ (x0, y0, x1, y1) — per Augenmass gesetzt.
# Gemeint ist die sichtbare helle Kopfflaeche ohne Kapuze, Helm und Kopftuch.
KOPF = {
    '01-M84-nahaufnahme-kopf.png':      (0.350, 0.094, 0.645, 0.645),
    '02-M55-rueckenansicht.png':        (0.465, 0.538, 0.538, 0.672),
    '03-M49-seitenansicht-kopftuch.png':(0.248, 0.251, 0.340, 0.453),
    '04-M62-figur-klein.png':           (0.133, 0.533, 0.180, 0.609),
    '05-M78-zwei-figuren.png':          (0.185, 0.188, 0.330, 0.448),
    '06-M75-bronzehelm.png':            (0.478, 0.354, 0.570, 0.511),
    '07-M07-kniend.png':                (0.308, 0.202, 0.475, 0.484),
    '08-M27-gebueckt-kapuze.png':       (0.293, 0.166, 0.450, 0.439),
    '09-M14-axt-fellkapuze.png':        (0.415, 0.394, 0.505, 0.547),
    '13-M14-text-jahreszahl.png':       (0.462, 0.399, 0.560, 0.556),
    '14-M62-text-ortsname.png':         (0.202, 0.457, 0.240, 0.529),
}
OHNE_FIGUR = ['10-M30-schema.png', '11-M45-landschaft.png', '12-M52-reliefwand.png']


def balken_in_kopf(pfad, box):
    im = Image.open(pfad).convert('RGB')
    W, H = im.size
    x0, y0, x1, y1 = [int(v * s) for v, s in zip(box, (W, H, W, H))]
    a = np.asarray(im.crop((x0, y0, x1, y1))).astype(float)
    kh, kw = a.shape[:2]
    nah = np.linalg.norm(a - INDIGO, axis=2) < 75
    lab, n = ndimage.label(nah)
    if n == 0:
        return None
    best = None
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < kh * kw * 0.01:
            continue
        pts = np.stack([xs - xs.mean(), ys - ys.mean()])
        ev, evec = np.linalg.eigh(np.cov(pts))
        laenge, dicke = 4 * np.sqrt(max(ev[1], 1e-9)), 4 * np.sqrt(max(ev[0], 1e-9))
        if dicke <= 0 or laenge / dicke < 1.8:
            continue
        if best is None or laenge > best[0]:
            best = (laenge, dicke, ys.mean(),
                    np.degrees(np.arctan2(evec[1, 1], evec[0, 1])))
    if best is None:
        return None
    laenge, dicke, cy, winkel = best
    return {'balken_zu_kopf_breite': laenge / kw, 'balken_dicke_zu_kopf': dicke / kh,
            'balken_lage_im_kopf': cy / kh, 'kopf_zu_bildhoehe': kh / H,
            'winkel': (winkel + 180) % 180 - 90, 'kopf_px': f'{kw}x{kh}'}


if __name__ == '__main__':
    print('=' * 100)
    print('STICHPROBENLAUF — Balkenkopf ueber 12 Ansichten + 2 mit Bildtext')
    print('Kopfregion von Hand gesetzt (Tabelle KOPF), Balken darin automatisch vermessen.')
    print('=' * 100)
    print(f"{'Bild':36}{'Kopf px':>10}{'Neigung':>9}{'Balken/Kopf':>13}"
          f"{'Dicke/Kopf':>12}{'Lage':>8}{'Kopf/Bildh':>12}")
    R = {}
    for f in sorted(glob.glob(os.path.join(DIR, '*.png'))):
        name = os.path.basename(f)
        if name.startswith('_'):
            continue
        if name in OHNE_FIGUR:
            print(f"{name[:36]:36}{'— ohne Figur, nur Stilkontrolle —':>55}")
            R[name] = None
            continue
        r = balken_in_kopf(f, KOPF[name])
        R[name] = r
        if r:
            print(f"{name[:36]:36}{r['kopf_px']:>10}{r['winkel']:>8.0f}°"
                  f"{r['balken_zu_kopf_breite']:>13.3f}{r['balken_dicke_zu_kopf']:>12.3f}"
                  f"{r['balken_lage_im_kopf']:>8.3f}{r['kopf_zu_bildhoehe']:>12.3f}")
        else:
            print(f"{name[:36]:36}{'kein Balken in der Kopfregion':>55}")
    fig = [n for n, r in R.items() if r]
    print(f"\nBalken in der Kopfregion gefunden: {len(fig)} von {len(KOPF)} Figurenbildern")

    def block(t, sel):
        if len(sel) < 2:
            return
        print(f"\n{t} (n = {len(sel)}): {', '.join(s[:2] for s in sel)}")
        for k, n in (('balken_zu_kopf_breite', 'Balkenbreite / Kopfbreite'),
                     ('balken_dicke_zu_kopf', 'Balkendicke / Kopfhoehe'),
                     ('balken_lage_im_kopf', 'Lage des Balkens im Kopf')):
            v = np.array([R[s][k] for s in sel])
            print(f"  {n:28} Mittel {v.mean():.3f}  SD {v.std():.3f}  "
                  f"Spanne {v.min():.3f}-{v.max():.3f}  Streuung {v.std()/v.mean()*100:5.1f} %")

    aufrecht = [s for s in fig if s[:2] in ('01', '02', '04', '05', '06', '14')]
    gedreht = [s for s in fig if s[:2] in ('03', '07', '08', '09', '13')]
    block('Alle Figurenbilder', fig)
    block('Aufrecht und frontal', aufrecht)
    block('Profil, kniend, gebueckt, dynamisch', gedreht)
    print('\nVergleichswerte Elementtest (recherche/stil-uf-element, 4 Szenen):')
    print('  B/C/D stehend frontal:      Breite  0,28 %   Dicke 1,38 %   Lage  0,13 %')
    print('  alle vier (mit A geneigt):  Breite 12,4 %    Dicke 3,8 %    Lage 12,2 %')
    json.dump(R, open(os.path.join(DIR, '_messwerte.json'), 'w'), indent=1, default=float)
