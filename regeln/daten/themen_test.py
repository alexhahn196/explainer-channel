#!/usr/bin/env python3
"""SCHRITT 2 + 3: Join, kanalinterner Test, Permutationstest.

Darf erst laufen, nachdem regeln/daten/themen_klassifikation.tsv committet ist.
"""
import csv
import os
import random
import statistics
import sys
from collections import defaultdict

DIR = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/explainer-channel'
MIN_VIDEOS_KANAL = 10      # Kanal zaehlt nur ab 10 Videos
MIN_GRUPPE = 3             # je Gruppe mindestens 3 Videos, sonst Kanal uebersprungen
N_PERM = 10000
SEED = 4711

BINAER = ['vorwissen', 'benannte_person', 'benanntes_raetsel',
          'selbsterfahren', 'koerper_alltag', 'frageform']
ZEIT = ['urzeit', 'benannte_epoche', 'zeitlos', 'heute']


def med(xs):
    return statistics.median(xs) if xs else None


def laden(nur_alt=False):
    kl = {}
    with open(os.path.join(DIR, 'themen_klassifikation.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            kl[r['video_id']] = r
    videos = []
    with open(os.path.join(DIR, 'themen_korpus.tsv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            k = kl.get(r['video_id'])
            if not k:
                continue
            if nur_alt and int(r['alter_tage']) < 90:
                continue
            videos.append({
                'kanal': r['kanal'], 'video_id': r['video_id'],
                'views': int(r['views']), 'alter': int(r['alter_tage']),
                **{m: k[m] for m in BINAER + ['zeitbezug']},
            })
    return videos


def gruppieren(videos):
    d = defaultdict(list)
    for v in videos:
        d[v['kanal']].append(v)
    return {k: vs for k, vs in d.items() if len(vs) >= MIN_VIDEOS_KANAL}


def kanal_ratios(kanaele, treffer):
    """log2(Median mit / Median ohne) je Kanal. treffer(v) -> bool."""
    out = {}
    for k, vs in kanaele.items():
        a = [v['views'] for v in vs if treffer(v)]
        b = [v['views'] for v in vs if not treffer(v)]
        if len(a) < MIN_GRUPPE or len(b) < MIN_GRUPPE:
            continue
        ma, mb = med(a), med(b)
        if not ma or not mb:
            continue
        import math
        out[k] = {'mit': ma, 'ohne': mb, 'n_mit': len(a), 'n_ohne': len(b),
                  'log2': math.log2(ma / mb)}
    return out


def statistik(ratios):
    """A = Median der kanalinternen log2-Verhaeltnisse, B = Richtungskonsistenz."""
    if not ratios:
        return None, 0, 0
    rs = [r['log2'] for r in ratios.values()]
    plus = sum(1 for r in rs if r > 0)
    return med(rs), max(plus, len(rs) - plus), len(rs)


def permutation(kanaele, treffer, a_obs, b_obs, n=N_PERM, seed=SEED):
    """Views INNERHALB jedes Kanals mischen, Merkmalslabels bleiben fest."""
    rng = random.Random(seed)
    roh = {k: [v['views'] for v in vs] for k, vs in kanaele.items()}
    flags = {k: [treffer(v) for v in vs] for k, vs in kanaele.items()}
    ta = tb = 0
    import math
    for _ in range(n):
        rs = []
        for k in kanaele:
            vv = roh[k][:]
            rng.shuffle(vv)
            a = [x for x, f in zip(vv, flags[k]) if f]
            b = [x for x, f in zip(vv, flags[k]) if not f]
            if len(a) < MIN_GRUPPE or len(b) < MIN_GRUPPE:
                continue
            ma, mb = med(a), med(b)
            if ma and mb:
                rs.append(math.log2(ma / mb))
        if not rs:
            continue
        ap = med(rs)
        plus = sum(1 for r in rs if r > 0)
        bp = max(plus, len(rs) - plus)
        if abs(ap) >= abs(a_obs) - 1e-12:
            ta += 1
        if bp >= b_obs:
            tb += 1
    return ta / n, tb / n


def merkmal_report(name, kanaele, treffer, alle_videos):
    ratios = kanal_ratios(kanaele, treffer)
    a, b, K = statistik(ratios)
    if a is None:
        print(f'\n### {name}: in keinem Kanal auswertbar '
              f'(nirgends {MIN_GRUPPE}+ Videos in beiden Gruppen)')
        return None
    # gepoolt, ohne Kanaltrennung - zum Kontrast
    pa = [v['views'] for v in alle_videos if treffer(v)]
    pb = [v['views'] for v in alle_videos if not treffer(v)]
    import math
    pooled = math.log2(med(pa) / med(pb)) if pa and pb and med(pa) and med(pb) else float('nan')

    pA, pB = permutation(kanaele, treffer, a, b)
    richt = 'HOEHER' if a > 0 else 'NIEDRIGER'
    print(f'\n### {name}')
    print(f'  gepoolt (alle Kanaele zusammen): {med(pa):>10,.0f} mit  vs {med(pb):>10,.0f} ohne'
          f'   = {2**pooled:>5.2f}x   (n={len(pa)}/{len(pb)})')
    print(f'  kanalintern: Median der log2-Verhaeltnisse {a:+.3f}  -> {2**a:.2f}x  ({richt})')
    print(f'  Richtungskonsistenz: {b} von {K} Kanaelen zeigen dieselbe Richtung')
    print(f'  Zufallstest ({N_PERM} Durchlaeufe):  p(Effektstaerke) = {pA:.4f}   '
          f'p(Richtungskonsistenz) = {pB:.4f}')
    print(f'  {"Kanal":22}{"n mit":>7}{"n ohne":>8}{"Median mit":>13}{"Median ohne":>13}{"Faktor":>9}')
    for k in sorted(ratios, key=lambda k: -ratios[k]['log2']):
        r = ratios[k]
        print(f'  {k:22}{r["n_mit"]:>7}{r["n_ohne"]:>8}{r["mit"]:>13,.0f}'
              f'{r["ohne"]:>13,.0f}{2**r["log2"]:>9.2f}')
    return {'merkmal': name, 'log2': a, 'faktor': 2**a, 'konsistenz': b, 'kanaele': K,
            'p_effekt': pA, 'p_konsistenz': pB, 'gepoolt_faktor': 2**pooled}


def lauf(nur_alt):
    videos = laden(nur_alt)
    kanaele = gruppieren(videos)
    titel = 'NUR VIDEOS AELTER ALS 90 TAGE' if nur_alt else 'ALLE VIDEOS'
    print('=' * 86)
    print(f'{titel}   —  {len(videos)} Videos, {len(kanaele)} Kanaele mit >={MIN_VIDEOS_KANAL}')
    print('=' * 86)
    for k, vs in sorted(kanaele.items(), key=lambda t: -len(t[1])):
        print(f'  {k:22} n={len(vs):>4}  Median {med([v["views"] for v in vs]):>10,.0f}')
    erg = []
    for m in BINAER:
        r = merkmal_report(m, kanaele, lambda v, m=m: v[m] == 'ja', videos)
        if r:
            erg.append(r)
    for z in ZEIT:
        r = merkmal_report(f'zeitbezug={z}', kanaele,
                           lambda v, z=z: v['zeitbezug'] == z, videos)
        if r:
            erg.append(r)
    print('\n' + '-' * 86)
    print(f'ZUSAMMENFASSUNG — {titel}')
    print('-' * 86)
    print(f'{"Merkmal":24}{"Faktor":>8}{"gepoolt":>9}{"Konsistenz":>12}'
          f'{"p(Effekt)":>11}{"p(Konsist.)":>12}  Urteil')
    for r in sorted(erg, key=lambda r: r['p_effekt']):
        best = min(r['p_effekt'], r['p_konsistenz'])
        # ROHES p, OHNE Korrektur fuer 19 Mehrfachvergleiche. Nach Holm bleibt
        # nur selbsterfahren(>=90d) uebrig - und der Befund beruht auf 11 Videos
        # aus 2 Kanaelen. Siehe regeln/themenwahl-test.md, Abschnitt "Die drei
        # Gegenproben", bevor eine dieser Zeilen als Befund gelesen wird.
        urteil = 'p<0.05 (roh)' if best < 0.05 else ('p<0.15 (roh)' if best < 0.15 else '-')
        print(f'{r["merkmal"]:24}{r["faktor"]:>8.2f}{r["gepoolt_faktor"]:>9.2f}'
              f'{str(r["konsistenz"])+"/"+str(r["kanaele"]):>12}'
              f'{r["p_effekt"]:>11.4f}{r["p_konsistenz"]:>12.4f}  {urteil}')
    return erg


if __name__ == '__main__':
    lauf(nur_alt=False)
    print('\n\n')
    lauf(nur_alt=True)
