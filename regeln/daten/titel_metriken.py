#!/usr/bin/env python3
"""titel_metriken.py — Titelmuster ausgezaehlt (Teil B, TITEL).

Je Kanal ueber alle erfassten Long-Form-Videos: Frageform, Laenge (Woerter/
Zeichen), Zahlen im Titel, Superlative/Extremmarker. Zusaetzlich je Kanal
Treffer- gegen Flop-Drittel (nach Views) und Gruppen-Aggregate.

Definitionen (offen dokumentiert, keine Schwellen von anderswo):
- Frageform: Titel endet mit "?" ODER beginnt mit Fragewort/Hilfsverb
  (who/what/why/how/when/where/which/did/do/does/was/were/is/are/can/could/
  should/would/will/has/have).
- Zahl: enthaelt eine Ziffer.
- Superlativ: most/best/worst/greatest/biggest/largest/oldest/deadliest/
  darkest/strangest/weirdest + generisch -est-Woerter aus einer Positivliste.
- Extremmarker (getrennt gezaehlt): first, last, only, ever, never, all,
  entire, every, no one, nobody, actually, really, truly, secret, hidden,
  forbidden, banned.
- Long-Form: Laenge > 180 s.
- Treffer-/Flop-Drittel: obere/untere Drittel nach Views innerhalb des
  Kanals (nur Long-Form, mindestens 6 Videos, sonst uebersprungen).
"""
import json, glob, os, re, statistics as st

ROH = os.path.join(os.path.dirname(__file__), '..', 'rohdaten')

FRAGE_START = re.compile(
    r"^(who|what|why|how|when|where|which|did|do|does|was|were|is|are|can|could|should|would|will|has|have)\b", re.I)
SUPERLATIVE = re.compile(
    r"\b(most|best|worst|greatest|biggest|largest|smallest|oldest|youngest|longest|shortest|deadliest|darkest|strangest|weirdest|toughest|hardest|craziest|richest|poorest|coldest|hottest|rarest|earliest|finest|grossest|dumbest|smartest|scariest)\b", re.I)
EXTREM = re.compile(
    r"\b(first|last|only|ever|never|all|entire|every|no one|nobody|actually|really|truly|secret|hidden|forbidden|banned)\b", re.I)
ZAHL = re.compile(r"\d")


def titel_merkmale(t):
    return {
        'frage': t.strip().endswith('?') or bool(FRAGE_START.match(t.strip())),
        'fragezeichen': t.strip().endswith('?'),
        'woerter': len(t.split()),
        'zeichen': len(t),
        'zahl': bool(ZAHL.search(t)),
        'superlativ': bool(SUPERLATIVE.search(t)),
        'extremmarker': bool(EXTREM.search(t)),
    }


def anteil(videos, key):
    if not videos:
        return None
    return round(100 * sum(1 for v in videos if v['m'][key]) / len(videos))


def block(videos):
    if not videos:
        return None
    return {
        'n': len(videos),
        'frage_pct': anteil(videos, 'frage'),
        'fragezeichen_pct': anteil(videos, 'fragezeichen'),
        'zahl_pct': anteil(videos, 'zahl'),
        'superlativ_pct': anteil(videos, 'superlativ'),
        'extremmarker_pct': anteil(videos, 'extremmarker'),
        'woerter_median': round(st.median(v['m']['woerter'] for v in videos), 1),
        'zeichen_median': round(st.median(v['m']['zeichen'] for v in videos), 1),
    }


def main():
    aus = {}
    for f in sorted(glob.glob(os.path.join(ROH, '*.json'))):
        d = json.load(open(f))
        kanal = d.get('kanal') or os.path.basename(f)
        lf = [v for v in d.get('videos', [])
              if (v.get('laenge_s') or 0) > 180 and v.get('titel')]
        for v in lf:
            v['m'] = titel_merkmale(v['titel'])
        eintrag = {'gruppe': d.get('gruppe'), 'alle': block(lf)}
        if len(lf) >= 6:
            nach_views = sorted(lf, key=lambda v: v.get('views') or 0)
            drittel = max(2, len(lf) // 3)
            eintrag['flops'] = block(nach_views[:drittel])
            eintrag['treffer'] = block(nach_views[-drittel:])
        aus[kanal] = eintrag
    # Gruppen-Aggregate (alle Titel der Gruppe zusammengeworfen)
    gruppen = {}
    for f in sorted(glob.glob(os.path.join(ROH, '*.json'))):
        d = json.load(open(f))
        lf = [v for v in d.get('videos', [])
              if (v.get('laenge_s') or 0) > 180 and v.get('titel')]
        for v in lf:
            v['m'] = titel_merkmale(v['titel'])
        gruppen.setdefault(d.get('gruppe'), []).extend(lf)
    aus['_gruppen'] = {g: block(vs) for g, vs in sorted(gruppen.items())}

    # Wortfrequenz Treffer- gegen Flop-Drittel je Gruppe: welche
    # inhaltstragenden Woerter tragen die starken Titel, welche die schwachen?
    stopp = set('the a an of in on to for and or is are was were do does did '
                'what why how when where who which that this it its with from '
                'by at as be been being'.split())
    def woerter(vs):
        z = {}
        for v in vs:
            for w in re.findall(r"[a-z']+", v['titel'].lower()):
                if w in stopp or len(w) < 3:
                    continue
                z[w] = z.get(w, 0) + 1
        return z
    wort = {}
    for g, vs in sorted(gruppen.items()):
        nach = sorted([v for v in vs if v.get('views') is not None],
                      key=lambda v: v['views'])
        if len(nach) < 12:
            continue
        d3 = len(nach) // 3
        tw, fw = woerter(nach[-d3:]), woerter(nach[:d3])
        n_t, n_f = d3, d3
        eintraege = []
        for w in set(tw) | set(fw):
            at, af = tw.get(w, 0) / n_t, fw.get(w, 0) / n_f
            if max(tw.get(w, 0), fw.get(w, 0)) < 3:
                continue
            eintraege.append({'wort': w, 'treffer_n': tw.get(w, 0),
                              'flop_n': fw.get(w, 0),
                              'treffer_pct': round(at * 100, 1),
                              'flop_pct': round(af * 100, 1),
                              'differenz_pp': round((at - af) * 100, 1)})
        eintraege.sort(key=lambda e: -abs(e['differenz_pp']))
        wort[g] = {'n_je_drittel': d3, 'woerter': eintraege[:20]}
    aus['_wortfrequenz'] = wort
    ziel = os.path.join(os.path.dirname(__file__), 'titel.json')
    json.dump(aus, open(ziel, 'w'), indent=1, ensure_ascii=False)
    print(f'-> {ziel}')
    for g, b in aus['_gruppen'].items():
        print(g, b)


if __name__ == '__main__':
    main()
