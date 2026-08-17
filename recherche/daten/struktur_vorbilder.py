#!/usr/bin/env python3
"""struktur_vorbilder.py — Strukturmessung an Vorbild-Transkripten.

Ergaenzt `regeln/daten/skriptanatomie_inkaxen.py` um zwei Groessen, die dort
fehlen: Themenwechsel und den Weg bis zur ersten Tatsachenbehauptung.

**Gibt keinen Transkripttext aus.** Nur Zahlen und Positionen.

Messgroessen je Video:
  kernfrage_pct        erstes Vorkommen von Fragewort + staerkstem Titelwort
  antwort_pct          erster Antwortmarker (because, the reason, turns out ...)
  erste_tatsache_s     Sekunde der ersten Tatsachenbehauptung: erstes Segment
                       mit Jahreszahl, Messwert, Prozentangabe oder Eigenname
                       (Grossschreibung mitten im Segment)
  erste_tatsache_pct   dieselbe Position in Prozent der Laufzeit
  einstieg_woerter     Woerter bis dorthin
  themenwechsel        Anzahl der Einbrueche in der Wortschatz-Ueberlappung
                       zwischen aufeinanderfolgenden Fenstern (siehe unten)
  wechsel_positionen   deren Position in Prozent der Laufzeit
  abschnitt_laenge_med Median-Abstand zwischen zwei Wechseln, in Prozent

Themenwechsel-Heuristik: Das Transkript wird in Fenster zu je 60 Sekunden
geteilt. Fuer jedes Fensterpaar wird die Jaccard-Aehnlichkeit der
inhaltstragenden Woerter berechnet. Ein Wert unter dem 30. Perzentil aller
Paare des Videos gilt als Themenwechsel. Das Mass ist relativ zum Video —
es vergleicht Videos untereinander, misst aber keine absolute Gliederung.
"""
import json, re, statistics as st, sys

STOPP = set("""the a an of in on to for and or is are was were do does did what why how when
where who which that this it its with from by at as be been being you your we our they their
he she his her but so if then than there here have has had will would can could not no yes
just like get got make made one two some all more most other into out up down over about""".split())

FRAGEWORT = re.compile(r"\b(what|why|how|when|where|who|which|did|do|does|is|are|was|were|can|could)\b", re.I)
ANTWORT = re.compile(r"\b(because|the reason (?:is|why|for)|turns out|it turns out|"
                     r"the answer(?:'s| is)?|that'?s why|which is why|here'?s why)\b", re.I)
JAHR = re.compile(r"\b\d{2,6}\s*(?:years?|bce?|ce|ad|bc)\b|\b\d{4}\b", re.I)
MESSWERT = re.compile(r"\b\d+[\d,.]*\s*(?:%|percent|meters?|metres?|feet|foot|miles?|km|"
                      r"kilometers?|kilometres?|pounds?|kilos?|kg|degrees?|times|x)\b", re.I)
EIGENNAME = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{3,}\b")


def segmente(eintrag):
    out = []
    for s in eintrag.get('transcript') or []:
        try:
            start = float(s.get('startMs', 0)) / 1000.0
        except (TypeError, ValueError):
            start = 0.0
        if s.get('text'):
            out.append((start, s['text']))
    return out


def inhaltswoerter(text):
    return {w for w in re.findall(r"[a-z']{3,}", text.lower()) if w not in STOPP}


def messen(vid, titel, segs, dauer):
    ende = max((s for s, _ in segs), default=0)
    dauer = dauer or ende or 1
    volltext = ' '.join(t for _, t in segs)

    def erste(rx):
        for s, t in segs:
            if rx.search(t):
                return s
        return None

    fw = FRAGEWORT.search(titel)
    inhalt = [w for w in re.findall(r"[A-Za-z']+", titel.lower())
              if w not in STOPP and len(w) > 3]
    kern = max(inhalt, key=len) if inhalt else None
    pos = [p for p in (
        erste(re.compile(rf"\b{re.escape(fw.group(0))}\b", re.I)) if fw else None,
        erste(re.compile(rf"\b{re.escape(kern)}", re.I)) if kern else None) if p is not None]
    kernfrage = max(pos) if pos else None
    antwort = erste(ANTWORT)

    # erste Tatsachenbehauptung
    tatsache_s, tatsache_typ, woerter_bis = None, None, 0
    for s, t in segs:
        if JAHR.search(t):
            tatsache_s, tatsache_typ = s, 'jahreszahl'
        elif MESSWERT.search(t):
            tatsache_s, tatsache_typ = s, 'messwert'
        elif len(EIGENNAME.findall(t)) >= 1:
            tatsache_s, tatsache_typ = s, 'eigenname'
        if tatsache_s is not None:
            break
        woerter_bis += len(re.findall(r"[A-Za-z0-9']+", t))

    # Themenwechsel ueber Fensteraehnlichkeit
    fenster, akt, grenze = [], [], 60.0
    for s, t in segs:
        if s >= grenze:
            fenster.append(' '.join(akt)); akt = []; grenze += 60.0
        akt.append(t)
    if akt:
        fenster.append(' '.join(akt))
    aehnlich = []
    for i in range(len(fenster) - 1):
        a, b = inhaltswoerter(fenster[i]), inhaltswoerter(fenster[i + 1])
        aehnlich.append(len(a & b) / len(a | b) if (a | b) else 0.0)
    wechsel_pos = []
    if len(aehnlich) >= 3:
        schwelle = st.quantiles(aehnlich, n=10)[2]      # 30. Perzentil
        for i, v in enumerate(aehnlich):
            if v <= schwelle:
                wechsel_pos.append(round((i + 1) * 60.0 / dauer * 100, 1))
    abstaende = [b - a for a, b in zip(wechsel_pos, wechsel_pos[1:])]

    return {
        'videoId': vid,
        'dauer_s': round(dauer),
        'woerter': len(re.findall(r"[A-Za-z0-9']+", volltext)),
        'kernfrage_s': round(kernfrage, 1) if kernfrage is not None else None,
        'kernfrage_pct': round(kernfrage / dauer * 100, 1) if kernfrage is not None else None,
        'antwort_s': round(antwort, 1) if antwort is not None else None,
        'antwort_pct': round(antwort / dauer * 100, 1) if antwort is not None else None,
        'erste_tatsache_s': round(tatsache_s, 1) if tatsache_s is not None else None,
        'erste_tatsache_pct': round(tatsache_s / dauer * 100, 1) if tatsache_s is not None else None,
        'erste_tatsache_typ': tatsache_typ,
        'einstieg_woerter': woerter_bis,
        'fenster': len(fenster),
        'aehnlichkeit_median': round(st.median(aehnlich), 3) if aehnlich else None,
        'themenwechsel': len(wechsel_pos),
        'wechsel_positionen_pct': wechsel_pos,
        'abschnitt_laenge_pct_med': round(st.median(abstaende), 1) if abstaende else None,
    }


def main(dateien, wunsch, titel, dauer):
    aus = {}
    for f in dateien:
        d = json.load(open(f))
        for r in d.get('transcripts', {}).get('results', []):
            vid = r.get('videoId')
            if vid in wunsch and r.get('success'):
                segs = segmente(r.get('data') or {})
                if segs:
                    aus[vid] = messen(vid, titel.get(vid, ''), segs, dauer.get(vid))
    return aus


if __name__ == '__main__':
    import os
    basis = os.path.dirname(os.path.abspath(__file__))
    meta = json.load(open(os.path.join(basis, '..', '..', 'regeln', 'daten',
                                       'inkaxen_videos.json')))
    ziel = [v for v in sys.argv[1:] if not v.endswith('.txt')]
    dateien = [v for v in sys.argv[1:] if v.endswith('.txt')]
    wunsch = set(ziel) or {k for k, v in meta.items() if v['kanal'] == 'Ink'}
    print(json.dumps(main(dateien, wunsch,
                          {k: v['titel'] for k, v in meta.items()},
                          {k: v['laenge_s'] for k, v in meta.items()}),
                     indent=1, ensure_ascii=False))
