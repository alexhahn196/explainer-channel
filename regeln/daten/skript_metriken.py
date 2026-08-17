#!/usr/bin/env python3
"""skript_metriken.py — Skript-Messwerte je Transkript (Teil B, SKRIPT).

Liest rohdaten/*.json und schreibt skript.json:
je Kanal x {treffer, schwach}: Wortzahl, WPM, Hook-60s-Text, CTAs (Anzahl +
Position), epistemische Marker je 1.000 Woerter, zweite Person.

Methodik epistemische Marker: Wortlisten-Heuristik wie in
recherche/nischen-kanal-2.md ("Umgang mit unsicheren Fakten") — echte
Unsicherheits-Kennzeichnung. Die Liste steht unten offen im Code und wird an
den drei Ueberschneidungs-Videos der bestehenden Auswertung kalibriert
(Ink TOP 3,7 / Historically TOP 2,4 / quack doc TOP 0,7 je 1.000 W).
"""
import json, glob, os, re, sys

ROH = os.path.join(os.path.dirname(__file__), '..', 'rohdaten')

# --- epistemische Marker (kalibrierte Wortliste, siehe Docstring) ---
EPISTEMISCH = [
    # explizites Nichtwissen
    r"we (?:do not|don'?t) (?:really |fully |actually )?know",
    r"we (?:may|might|will) never know",
    r"no ?(?:one|body) (?:really )?knows",
    r"we(?:'re| are) not (?:entirely |completely |quite )?(?:sure|certain)",
    r"not (?:entirely |completely |quite )?(?:sure|certain)",
    r"we can(?:not|'t) (?:be sure|be certain|say for (?:sure|certain)|know)",
    r"remains? (?:a mystery|unclear|unknown|uncertain|debated)",
    r"is still debated", r"still a mystery", r"hard to say",
    r"the honest answer is",
    # Theorie / Zuschreibung
    r"(?:the |one |a |another |leading |most common )theor(?:y|ies)",
    r"hypothes[ie]s",
    r"(?:historians?|archa?eologists?|scientists?|researchers?|experts?|anthropologists?|scholars?) (?:believe|think|suspect|argue|estimate|assume|disagree)",
    r"(?:is|are|was|were) (?:widely )?(?:believed|thought|assumed) to",
    r"(?:evidence|research|studies|findings|the data) suggests?",
    r"seems? to (?:have|suggest|indicate)",
    r"appears? to (?:have|be)",
    r"according to (?:some|one theory|current thinking)",
    # Abschwaechungs-Adverbien und klassische Hedges
    r"\bprobably\b", r"\bapparently\b", r"\bperhaps\b", r"\bpossibly\b",
    r"\bpresumably\b", r"\bseemingly\b", r"\blikely\b",
    r"\b(?:may|might) have\b",
]
EPISTEMISCH_RE = [re.compile(p, re.I) for p in EPISTEMISCH]


def marker_zaehlen(text, regexe):
    """Zaehlt Treffer ueber alle Muster, ueberlappende Spannen nur einmal."""
    spannen = []
    for rx in regexe:
        for m in rx.finditer(text):
            spannen.append((m.start(), m.end()))
    spannen.sort()
    n = 0
    ende = -1
    for a, b in spannen:
        if a >= ende:
            n += 1
            ende = b
        else:
            ende = max(ende, b)
    return n

# --- CTAs ---
CTA = [
    r"\bsubscrib\w*", r"like (?:this|the) video", r"leave a like",
    r"hit (?:the )?like", r"thumbs up", r"comment(?:s)? below",
    r"in the comments", r"let (?:me|us) know", r"\bshare (?:this|the) video",
    r"\bpatreon\b", r"join (?:this channel|the channel|our)", r"\bmembership\b",
    r"link in (?:the )?description", r"check out (?:my|our|the channel)",
    r"notification(?:s| bell)", r"turn on (?:the )?bell", r"\bfollow (?:me|us)\b",
]
CTA_RE = [re.compile(p, re.I) for p in CTA]

ZWEITE_PERSON_RE = re.compile(r"\byou(?:r|'re|'ve|'ll|rself|rselves)?\b", re.I)

# Aufbau: Gliederungssignale. LISTE = nummerierte oder abzaehlende Struktur,
# FLIESS = Uebergaenge ohne Nummerierung. Das Verhaeltnis zeigt, ob ein Skript
# eine Aufzaehlung abarbeitet oder einen Gedanken entwickelt.
LISTENSIGNAL = re.compile(
    r"\b(number (?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)|"
    r"tier (?:one|two|three|four|five|\d+)|"
    r"(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)(?:ly)?,|"
    r"next up|first up|entry (?:number )?\d|"
    r"(?:and )?(?:that|this) (?:brings us to|was) number)\b", re.I)
FLIESSSIGNAL = re.compile(
    r"\b(but here'?s|here'?s (?:the|where|why|what)|and (?:that'?s|this is) (?:where|why|when)|"
    r"which (?:brings|leads) (?:us )?to|so (?:what|why|how) (?:happened|did|does)|"
    r"but (?:first|before)|now,? (?:here|think|imagine)|the (?:answer|reason|problem) is|"
    r"and that'?s (?:exactly )?(?:the|why|when))\b", re.I)

# Einstiegstyp der ersten 60 s — Klassifikation am ERSTEN Satz, offen
# dokumentiert. Reihenfolge = Vorrang.
EINSTIEG = [
    ('du-versetzung', re.compile(
        r"^\W*(imagine|picture this|you(?:'|\s|r\b)|if you\b|let'?s say you\b|"
        r"right now,? (?:you|your)\b)", re.I)),
    ('szene-datum-ort', re.compile(
        r"^\W*(it'?s\s+(?:the\s+)?\w+\s+\d|in the (?:year|sweltering|summer|winter|spring|autumn|fall)\b|"
        r"(?:on|in)\s+\w+\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{3,4}|around\s+\d|"
        r"(?:roughly\s+)?\d{2,3}\s*(?:million|thousand)\s+years ago|this is a \w+ (?:morning|day|night)|"
        r"there was a moment)", re.I)),
    ('ankuendigung', re.compile(
        r"^\W*(today,? (?:we|i)\b|in this video|welcome (?:back|to)|here are\b|"
        r"we(?:'| a)re going (?:over|to (?:look|talk))|tier one\b)", re.I)),
]


def einstiegstyp(hook):
    """Klassifiziert den Einstieg am ersten Satz.

    Vorher werden ASR-Artefakte und einleitende Zeitadverbien entfernt:
    „[music] >> You wander…" und „Tonight, you'll open your fridge…" sind
    Du-Versetzungen und wurden sonst als These gezaehlt.
    """
    if not hook:
        return 'aussage-these'
    h = re.sub(r"\[[a-z ]+\]|>>+", ' ', hook)                 # ASR-Artefakte
    h = re.sub(r"^\W*(?:tonight|today|right now|now|so|okay|well|and)\s*,?\s+",
               '', h.strip(), flags=re.I)                      # Zeitadverbien
    h = h.strip()
    erster = re.split(r"(?<=[.!?])\s", h, maxsplit=1)[0]
    for name, rx in EINSTIEG:
        if rx.search(erster) or rx.search(h[:60]):
            return name
    return 'aussage-these'


def transcript_segmente(t):
    """Normalisiert die Transkript-Rohantwort zu [(start_s, text), ...]."""
    if t is None:
        return None
    if isinstance(t, str):
        try:
            t = json.loads(t)
        except Exception:
            return [(0.0, t)] if t.strip() else None
    if isinstance(t, dict):
        for k in ('transcript', 'captions', 'segments', 'data', 'result', 'content'):
            if k in t and t[k]:
                t = t[k]
                break
        else:
            if 'text' in t:
                return [(0.0, t['text'])] if str(t['text']).strip() else None
            return None
    if isinstance(t, list):
        segs = []
        for seg in t:
            if isinstance(seg, str):
                segs.append((0.0, seg)); continue
            txt = seg.get('text') or seg.get('caption') or seg.get('snippet') or ''
            if 'startMs' in seg or 'start_ms' in seg:
                try:
                    start = float(seg.get('startMs', seg.get('start_ms'))) / 1000.0
                except Exception:
                    start = 0.0
            else:
                try:
                    start = float(seg.get('start', seg.get('offset', 0)))
                except Exception:
                    start = 0.0
            if txt:
                segs.append((start, str(txt)))
        return segs or None
    return None


def messen(segs, dauer_s):
    volltext = ' '.join(x[1] for x in segs)
    woerter = re.findall(r"[A-Za-z0-9']+", volltext)
    n = len(woerter)
    # WPM gegen die Videodauer (Sprechzeit inkl. Pausen); zusaetzlich gegen
    # das Transkriptende, falls die Dauer fehlt.
    ende = max((s for s, _ in segs), default=0)
    basis = dauer_s if dauer_s else ende
    wpm = round(n / (basis / 60.0)) if basis else None
    hook = ' '.join(t for s, t in segs if s < 60.0)
    # Marker (ueberlappungsfrei gezaehlt)
    ep = marker_zaehlen(volltext, EPISTEMISCH_RE)
    du = len(ZWEITE_PERSON_RE.findall(volltext))
    # CTAs: Treffer je Segment, Cluster <15 s = ein Ereignis
    roh = []
    for s, t in segs:
        for rx in CTA_RE:
            if rx.search(t):
                roh.append(s)
                break
    roh.sort()
    ctas = []
    for s in roh:
        if not ctas or s - ctas[-1] > 15:
            ctas.append(s)
    # Erste 60 s: Einstiegstyp, Anrede, erste Zahl
    du60 = len(ZWEITE_PERSON_RE.findall(hook))
    erste_anrede_s = None
    for s, t in segs:
        if ZWEITE_PERSON_RE.search(t):
            erste_anrede_s = round(s, 1)
            break
    zahl60 = bool(re.search(r"\d", hook))
    liste = marker_zaehlen(volltext, [LISTENSIGNAL])
    fliess = marker_zaehlen(volltext, [FLIESSSIGNAL])
    return {
        'listensignale': liste,
        'fliesssignale': fliess,
        'aufbau': ('ohne signal' if liste == 0 and fliess == 0 else
                   'liste' if liste >= 3 and liste > fliess else
                   'fliess' if fliess > liste else 'gemischt'),
        'wortzahl': n,
        'wpm': wpm,
        'dauer_s': dauer_s,
        'einstiegstyp': einstiegstyp(hook),
        'anrede_in_60s': du60,
        'erste_anrede_s': erste_anrede_s,
        'zahl_in_60s': zahl60,
        'hook_60s': hook[:1200],
        'cta_anzahl': len(ctas),
        'cta_positionen_s': [round(c) for c in ctas],
        'cta_positionen_pct': [round(c / basis * 100, 1) for c in ctas] if basis else [],
        'epistemische_marker': ep,
        'epistemisch_pro_1000w': round(ep / n * 1000, 1) if n else None,
        'zweite_person_treffer': du,
        'zweite_person_pro_1000w': round(du / n * 1000, 1) if n else None,
        'zweite_person': du >= 2,
    }


def main():
    aus = {}
    for f in sorted(glob.glob(os.path.join(ROH, '*.json'))):
        d = json.load(open(f))
        kanal = d.get('kanal') or os.path.basename(f)
        eintrag = {'gruppe': d.get('gruppe'), 'channelId': d.get('channelId')}
        for rolle in ('treffer', 'schwach'):
            det = d.get(f'details_{rolle}') or {}
            if isinstance(det, str):
                try: det = json.loads(det)
                except Exception: det = {}
            dauer = None
            for k in ('lengthSeconds', 'duration', 'length_seconds', 'durationSeconds'):
                v = det.get(k) if isinstance(det, dict) else None
                if v:
                    try: dauer = int(float(v)); break
                    except Exception: pass
            if dauer is None:
                dauer = (d.get('auswahl', {}).get(rolle) or {}).get('laenge_s')
            segs = transcript_segmente(d.get(f'transkript_{rolle}'))
            meta = d.get('auswahl', {}).get(rolle) or {}
            if segs is None:
                eintrag[rolle] = {'videoId': meta.get('videoId'), 'titel': meta.get('titel'),
                                  'views': meta.get('views'), 'status': 'transkript fehlt'}
            else:
                m = messen(segs, dauer)
                m.update({'videoId': meta.get('videoId'), 'titel': meta.get('titel'),
                          'views': meta.get('views'), 'status': 'ok'})
                eintrag[rolle] = m
        aus[kanal] = eintrag
    ziel = os.path.join(os.path.dirname(__file__), 'skript.json')
    json.dump(aus, open(ziel, 'w'), indent=1, ensure_ascii=False)
    print(f'{len(aus)} Kanaele -> {ziel}')
    for k, v in aus.items():
        for rolle in ('treffer', 'schwach'):
            e = v.get(rolle, {})
            if e.get('status') == 'ok':
                print(f"{v['gruppe']} {k[:22]:22} {rolle:8} {e['wortzahl']:>5} W  {e['wpm'] or '?':>4} WPM  "
                      f"CTA {e['cta_anzahl']}  epist {e['epistemisch_pro_1000w']}  du/1k {e['zweite_person_pro_1000w']}")
            else:
                print(f"{v['gruppe']} {k[:22]:22} {rolle:8} {e.get('status')}")


if __name__ == '__main__':
    sys.exit(main())
