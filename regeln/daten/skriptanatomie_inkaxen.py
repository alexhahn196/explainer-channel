#!/usr/bin/env python3
"""skriptanatomie_inkaxen.py — Skriptanatomie der 26 Videos von Ink Explainer
und Axen. Liest die per get_bulk_video_transcripts gezogenen JSON-Dateien und
gibt ausschliesslich Kennzahlen aus.

**Dieses Skript gibt zu keinem Zeitpunkt Transkripttext aus.** Alle Rueckgaben
sind Zahlen, Anteile oder Kategorienamen. Das ist Absicht: der Bericht soll
ohne Zitate auskommen.

Gemessen je Video:
  kernfrage_pct       Position des ersten woertlichen Vorkommens des
                      Titel-Fragewortes plus des staerksten Titel-Inhaltswortes,
                      in Prozent der Laufzeit
  antwort_pct         Position des ersten Antwortmarkers ("because",
                      "the reason", "turns out", "the answer is", ...)
  antwort_drittel     in welchem Laufzeit-Drittel dieser Marker faellt
  du/wir/man/sie      Perspektivpronomen je 1.000 Woerter
  fuenftel[]          je Fuenftel der Laufzeit: Woerter, Fragezeichen-Saetze,
                      Zahlenangaben, Treffer der zweiten Person
  satzlaenge_median   Woerter je Satz (ASR ohne Satzzeichen -> Segmentgrenzen
                      als Satzproxy, siehe unten)
  kurzwort_anteil     Anteil der Woerter mit weniger als 7 Zeichen

Satzproxy: ASR-Transkripte tragen keine Satzzeichen. Als Satzgrenze gilt hier
das Ende eines Transkriptsegments, wenn danach eine Pause > 0,4 s liegt oder
das naechste Segment mit einem Grossbuchstaben beginnt. Der Wert ist deshalb
ein Vergleichsmass zwischen Videos, keine Grammatikmessung.

Aufruf:
    python3 skriptanatomie_inkaxen.py <transkript-datei> [...] > anatomie.json
"""
import json, re, statistics as st, sys

FRAGEWORT = re.compile(r"\b(what|why|how|when|where|who|which|did|do|does|is|are|was|were|can|could)\b", re.I)
STOPP = set("the a an of in on to for and or is are was were do does did what why how "
            "when where who which that this it its with from by at as be been being "
            "you your we our they their he she his her".split())

PRONOMEN = {
    'du':  re.compile(r"\byou(?:r|'re|'ve|'ll|rself|rselves)?\b", re.I),
    'wir': re.compile(r"\bwe(?:'re|'ve|'ll|\b)|\bour(?:s|selves)?\b|\bus\b", re.I),
    'man': re.compile(r"\b(?:one|people|humans|someone|somebody|anyone)\b", re.I),
    'sie': re.compile(r"\bthey(?:'re|'ve|'ll)?\b|\bthem(?:selves)?\b|\btheir(?:s)?\b", re.I),
}
ANTWORTMARKER = re.compile(
    r"\b(because|the reason (?:is|why|for)|turns out|it turns out|the answer(?:'s| is)?|"
    r"that'?s why|which is why|the short answer|here'?s why|the explanation)\b", re.I)
ZAHL = re.compile(r"\b\d[\d,.]*\b")
FRAGE = re.compile(r"\?")


def segmente(eintrag):
    """[(start_s, text), ...] aus einem Transkript-Eintrag."""
    segs = []
    for s in eintrag.get('transcript') or []:
        try:
            start = float(s.get('startMs', 0)) / 1000.0
        except (TypeError, ValueError):
            start = 0.0
        t = s.get('text') or ''
        if t:
            segs.append((start, t))
    return segs


def erstes_vorkommen(segs, rx, dauer):
    for s, t in segs:
        if rx.search(t):
            return round(s / dauer * 100, 1) if dauer else None
    return None


def titel_kernwoerter(titel):
    """Fragewort und das laengste Inhaltswort des Titels."""
    fw = FRAGEWORT.search(titel)
    inhalt = [w for w in re.findall(r"[A-Za-z']+", titel.lower())
              if w not in STOPP and len(w) > 3]
    kern = max(inhalt, key=len) if inhalt else None
    return (fw.group(0) if fw else None), kern


def messen(vid, titel, segs, dauer_s):
    volltext = ' '.join(t for _, t in segs)
    woerter = re.findall(r"[A-Za-z0-9']+", volltext)
    n = len(woerter) or 1
    ende = max((s for s, _ in segs), default=0)
    dauer = dauer_s or ende or 1

    fw, kern = titel_kernwoerter(titel)
    pos_fw = erstes_vorkommen(segs, re.compile(rf"\b{re.escape(fw)}\b", re.I), dauer) if fw else None
    pos_kern = erstes_vorkommen(segs, re.compile(rf"\b{re.escape(kern)}", re.I), dauer) if kern else None
    kandidaten = [p for p in (pos_fw, pos_kern) if p is not None]
    kernfrage_pct = max(kandidaten) if kandidaten else None

    pos_antwort = erstes_vorkommen(segs, ANTWORTMARKER, dauer)
    drittel = (None if pos_antwort is None else
               'erstes' if pos_antwort < 33.4 else
               'zweites' if pos_antwort < 66.7 else 'drittes')

    pron = {k: round(len(rx.findall(volltext)) / n * 1000, 1) for k, rx in PRONOMEN.items()}

    # Fuenftel nach Laufzeit
    fuenftel = []
    for i in range(5):
        a, b = dauer * i / 5, dauer * (i + 1) / 5
        teil = ' '.join(t for s, t in segs if a <= s < b)
        w = re.findall(r"[A-Za-z0-9']+", teil)
        fuenftel.append({
            'woerter': len(w),
            'fragezeichen': len(FRAGE.findall(teil)),
            'zahlen': len(ZAHL.findall(teil)),
            'zweite_person': len(PRONOMEN['du'].findall(teil)),
        })

    # Satzproxy
    saetze, aktuell = [], 0
    for i, (s, t) in enumerate(segs):
        aktuell += len(re.findall(r"[A-Za-z0-9']+", t))
        naechster = segs[i + 1] if i + 1 < len(segs) else None
        pause = (naechster[0] - s) if naechster else 99
        grossanfang = bool(naechster and re.match(r"\s*[A-Z]", naechster[1]))
        if pause > 0.4 or grossanfang or naechster is None:
            if aktuell:
                saetze.append(aktuell)
            aktuell = 0
    kurz = sum(1 for w in woerter if len(w) < 7)

    return {
        'videoId': vid,
        'woerter': n,
        'dauer_s': round(dauer),
        'wpm': round(n / (dauer / 60)) if dauer else None,
        'kernfrage_pct': kernfrage_pct,
        'antwort_pct': pos_antwort,
        'antwort_drittel': drittel,
        'pronomen_pro_1000w': pron,
        'fuenftel': fuenftel,
        'satzlaenge_median': round(st.median(saetze), 1) if saetze else None,
        'saetze': len(saetze),
        'kurzwort_anteil_pct': round(kurz / n * 100, 1),
    }


def main(dateien, titel_map, dauer_map):
    aus = {}
    for f in dateien:
        d = json.load(open(f))
        for r in d.get('transcripts', {}).get('results', []):
            vid = r.get('videoId')
            if not r.get('success') or not vid:
                continue
            segs = segmente(r.get('data') or {})
            if not segs:
                continue
            aus[vid] = messen(vid, titel_map.get(vid, ''), segs, dauer_map.get(vid))
    return aus


if __name__ == '__main__':
    import os
    basis = os.path.dirname(os.path.abspath(__file__))
    meta = json.load(open(os.path.join(basis, 'inkaxen_videos.json')))
    titel = {k: v['titel'] for k, v in meta.items()}
    dauer = {k: v['laenge_s'] for k, v in meta.items()}
    ergebnis = main(sys.argv[1:], titel, dauer)
    print(json.dumps(ergebnis, indent=1, ensure_ascii=False))
