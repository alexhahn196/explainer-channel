#!/usr/bin/env python3
"""uf_schreibstil_messen.py — Schreibstil-Messung der 16 Videos von
Unknown Frequencies (UCm1yxl_4qMbStLHpHQu6xWg).

**Dieses Skript gibt zu keinem Zeitpunkt Transkripttext aus.** Alle Rueckgaben
sind Zahlen, Anteile oder Kategorienamen — dieselbe Regel wie in
regeln/daten/skriptanatomie_inkaxen.py.

VERHAELTNIS ZU skriptanatomie_inkaxen.py
----------------------------------------
Die Kennzahlen aus Teil 1 des Berichts (Wortzahl, WPM, Fuenftel, Kernfrage,
Antwortposition, Perspektivpronomen, Satzlaenge, Kurzwortanteil) werden NICHT
hier neu definiert. Dieses Skript importiert `skriptanatomie_inkaxen.py`
unveraendert und ruft dessen `messen()` auf. Nur so bleiben die Werte mit
Ink Explainer und Axen vergleichbar.

Ergaenzt werden:
  * epistemische Marker — Wortliste aus regeln/daten/skript_metriken.py
  * Erzaehlmerkmale (Teil 3): Chronologie, Erzaehlerhaltung, Personen,
    Fragen, Schluss, Satzbauformen

ACHTUNG — Pfadabhaengigkeit: skriptanatomie_inkaxen.py und skript_metriken.py
liegen unter regeln/daten/ auf dem Branch claude/kanal-2-datengrundlage-bldjee
und existieren auf main nicht. Ohne sie laeuft dieses Skript nicht; das ist
Absicht, damit die Messdefinition nicht unbemerkt auseinanderlaeuft.

DATENBESCHAFFUNG (0 Credits)
----------------------------
  1. get_video_subtitle / get_bulk_video_subtitles je Video -> signierte
     timedtext-URL (Format srv1). Die URLs laufen nach wenigen Stunden ab.
  2. curl der URL -> XML mit <text start="..." dur="...">.
  3. --aufbereiten wandelt das XML in die Form, die
     get_bulk_video_transcripts liefert.

Gegenprobe: fuer EhT6IhuZQp4 liefern beide Wege 213 Segmente mit identischen
startMs-Werten und identischem Text. Der Satzproxy haengt an den
Segmentgrenzen — ohne diese Gleichheit waeren die Werte nicht vergleichbar.

AUFRUF
------
    python3 uf_schreibstil_messen.py --aufbereiten <captions-verzeichnis>
    python3 uf_schreibstil_messen.py --messen
"""
import collections, html, importlib.util, json, os, re, statistics as st, sys
import xml.etree.ElementTree as ET

HIER = os.path.dirname(os.path.abspath(__file__))
REGELN = os.path.abspath(os.path.join(HIER, '..', '..', 'regeln', 'daten'))

# --- Videoliste, Reihenfolge = Upload (youtube_channel_videos, sort_by=oldest) ---
# form: POV = Zweite-Person-Form, CHRON = Chronikform ("The ENTIRE History of ...")
# Die Monatsangabe ist monatsgenau (publishedTimeText), nicht taggenau.
VIDEOS = [
    ("EhT6IhuZQp4", "POV",   "Why It Sucked to Be a U.S. Soldier (in WW2)",                   537,  396000, "2026-03"),
    ("re_Av02zWcc", "POV",   "Your Life as Every German Army Rank in WW2",                    541,  992000, "2026-03"),
    ("COSuWgQjBhQ", "POV",   "POV: You're a German Soldier in WW2",                           721,  774000, "2026-03"),
    ("Wrv5t7VmmXw", "POV",   "What It Was Like to be Every British Army Rank in WW2",         604,  315000, "2026-04"),
    ("O56b0J6Rgn8", "POV",   "Your Life as Every Japanese Army Rank in WW2",                  568,   97000, "2026-04"),
    ("6DHpRoZw974", "POV",   "Iwo Jima from the Japanese Soldier's Perspective",              733,  222000, "2026-04"),
    ("FXsah-HUdFo", "POV",   "What 24 Hours Trapped in a WW1 Trench Would Be Like",           644,  144000, "2026-05"),
    ("wZTEbo-HM_g", "CHRON", "The ENTIRE History of WW1 Explained",                           753,  549000, "2026-06"),
    ("mCWyBV45SA0", "POV",   "POV: You Are a Japanese Sailor in WW2",                         594,   47000, "2026-06"),
    ("OCXZSk9IVm8", "POV",   "POV: You're a Soldier in the Vietnam War",                      540,   19000, "2026-06"),
    ("2oDLttbgF4k", "CHRON", "The Entire History of WW2's Deadliest Battle",                  855,  140000, "2026-07"),
    ("PXxir5GIqKU", "CHRON", "The Reason Germany Failed at the Battle of the Bulge",          722,   46000, "2026-07"),
    ("Nlu6Fe-vbYQ", "CHRON", "The ENTIRE History of WW2 Explained",                           823,  293000, "2026-07"),
    ("mJS-QVw8lzY", "CHRON", "The ENTIRE Story of The Odyssey Explained",                     789, 1100000, "2026-07"),
    ("X3_q5A18qfc", "CHRON", "The Entire Story of The Trojan War & Iliad Explained (Before The Odyssey)", 795, 183000, "2026-08"),
    ("9G3xztcRXQM", "CHRON", "Evolution of The Greek Soldier",                                665,   12000, "2026-08"),
]


def modul(name, pfad):
    if not os.path.exists(pfad):
        sys.exit(f"FEHLT: {pfad}\n"
                 f"Liegt auf Branch claude/kanal-2-datengrundlage-bldjee, nicht auf main.")
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- Aufbereitung
def aufbereiten(capdir):
    """srv1-XML -> JSON in der Form von get_bulk_video_transcripts."""
    ergebnisse, meta = [], {}
    for vid, form, titel, laenge, views, monat in VIDEOS:
        baum = ET.parse(os.path.join(capdir, vid + '.xml'))
        segs = []
        for t in baum.getroot().iter('text'):
            # srv1 ist doppelt escaped: &amp;#39; -> &#39; -> '
            txt = html.unescape(html.unescape(t.text or '')).replace('\n', ' ').strip()
            txt = re.sub(r'\s+', ' ', txt)
            if txt:
                segs.append({'startMs': str(int(round(float(t.get('start', '0')) * 1000))),
                             'text': txt})
        ergebnisse.append({'videoId': vid, 'success': True,
                           'data': {'transcript': segs}})
        meta[vid] = {'kanal': 'UF', 'form': form, 'titel': titel,
                     'laenge_s': laenge, 'views': views, 'monat': monat,
                     'segmente': len(segs)}
    json.dump({'transcripts': {'results': ergebnisse}},
              open(os.path.join(HIER, 'uf_transkripte.json'), 'w'), ensure_ascii=False)
    json.dump(meta, open(os.path.join(HIER, 'uf_videos.json'), 'w'),
              ensure_ascii=False, indent=1)
    for vid, m in meta.items():
        print(f"{vid}  {m['segmente']:4d} Segmente  {m['laenge_s']:4d}s  {m['form']:<5} {m['titel'][:46]}")
    print("\nHINWEIS: uf_transkripte.json enthaelt Transkripttext und gehoert "
          "NICHT ins Repository (siehe .gitignore).")


# -------------------------------------------------------------- Erzaehlmuster
RUECKBLENDE = re.compile(
    r"\b(before that|years? earlier|decades? earlier|back in|meanwhile|"
    r"at the same time|earlier that|but first|let'?s go back|rewind|"
    r"to understand (?:this|that|why|how)|it started|it all started|"
    r"years? before|months? before)\b", re.I)
ICH = re.compile(r"\bI\b|\bI'?(?:m|ve|ll|d)\b|\bmy\b|\bme\b|\bmine\b")
HALTUNG = re.compile(
    r"\b(let'?s|let me|here'?s the thing|believe it or not|of course|honestly|"
    r"frankly|to be fair|the truth is|and that'?s the|which is why|the problem is|"
    r"the catch|the irony|make no mistake|keep in mind|remember though|"
    r"and yes|and no|sounds? (?:crazy|insane|mad)|if that sounds)\b", re.I)
IMPERATIV = re.compile(
    r"\b(imagine|picture (?:this|yourself|it)|look at|think about|remember|"
    r"consider|now picture|say hello|meet )\b", re.I)
CTA = re.compile(
    r"\b(subscribe|hit the like|like this video|comment below|let me know|"
    r"leave a comment|next video|check out|links? in the description|"
    r"we'?re on spotify|if you'?d rather listen|catch you next time|"
    r"thanks for watching|see you (?:next|in))\b", re.I)
JAHR = re.compile(r"\b(1[0-9]{3}|20[0-2][0-9])\b")
BC = re.compile(r"\b(\d{1,4})\s*(?:BC|BCE|B\.C\.)\b", re.I)
APPOSITION = re.compile(
    r"([A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*,\s*(?:a|an|the)\s+[a-z]|"
    r"\b(?:a|the)\s+(?:man|soldier|general|officer|king|commander|sailor|pilot|"
    r"private|captain|sergeant|colonel|admiral|poet|scholar)\s+(?:named|called)\s+([A-Z][a-z]+)")
# Eroeffnungs- und Schlussformeln
URSACHE = re.compile(r"\bbut (?:the whole thing|it all started|the entire|it started|all of it)\b", re.I)
BESTAETIGUNG = re.compile(r"\byeah,? (?:seriously|really)\b", re.I)
LEVEL = re.compile(r"\blevel (?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)\b", re.I)
GROSSZAHL = re.compile(r"\b\d[\d.,]*\s*(?:million|billion|thousand)\b", re.I)
SUPERLATIV = re.compile(r"\b(?:most|greatest|deadliest|oldest|largest|biggest|famous|worst)\b", re.I)

# Satzbauformen, gemessen an echter Interpunktion (nicht am Segment-Satzproxy)
FORMEN = {
    'du_bist':       re.compile(r"^(?:and |but |now |so )?you(?:'re| are)\b", re.I),
    'du_negativ':    re.compile(r"^you (?:don'?t|can'?t|won'?t|didn'?t|couldn'?t)\b", re.I),
    'wenn_du':       re.compile(r"^(?:and |but |so )?if you\b", re.I),
    'aber_anfang':   re.compile(r"^but\b", re.I),
    'und_anfang':    re.compile(r"^and\b", re.I),
    'das_ist':       re.compile(r"^(?:that'?s|this is|that is)\b", re.I),
    'jetzt':         re.compile(r"^now\b", re.I),
    'frage':         re.compile(r"\?\s*$"),
    'zahl_anfang':   re.compile(r"^\d"),
}
# Wortliste fuer die Personenzaehlung: Laender, Voelker, Orte, Raenge, Monate
NICHTPERSON = set("""January February March April May June July August September October
November December Monday Tuesday Wednesday Thursday Friday Saturday Sunday
Germany German Germans Japan Japanese America American Americans Britain British
Russia Russian Russians France French Italy Italian Europe European Africa Asia
Pacific Atlantic Berlin London Paris Moscow Tokyo Washington Poland Polish China
Chinese Vietnam Vietnamese Korea Korean Greece Greek Greeks Troy Trojan Trojans
Rome Roman Romans Egypt Egyptian Spain Spanish Austria Hungary Belgium Holland
Netherlands Norway Denmark Sweden Finland Turkey Ottoman Soviet Union Allies
Allied Axis Nazi Nazis Wehrmacht Luftwaffe Reich SS Army Navy Marines Corps
World War One Two North South East West New Old Great Battle Operation
God Gods Lord King Queen Emperor General Colonel Captain Major Sergeant Private
Christmas Easter English England Scotland Ireland Wales Iwo Jima Okinawa
Stalingrad Normandy Dunkirk Verdun Somme Ardennes Bulge Midway Pearl Harbor
Sparta Spartan Spartans Athens Athenian Athenians Persia Persian Persians
Macedonia Macedonian Mycenae Mycenaean Ithaca Olympus Hades Mount Aegean
Mediterranean Sea Island Islands City Empire Republic State States United
Kingdom Force Air Front Line Day Night Hour Minute Second Week Month Year
""".split())


def woerter(t):
    return re.findall(r"[A-Za-z0-9']+", t)


def echte_saetze(segs):
    """Saetze an echter Interpunktion. Der Satzproxy aus
    skriptanatomie_inkaxen.py schneidet an Segmentgrenzen und zerlegt zu fein
    (4.630 statt 3.404 Saetze); fuer Satzbauformen ist er unbrauchbar."""
    text = re.sub(r'\s+', ' ', ' '.join(t for _, t in segs))
    return [s.strip() for s in re.split(r'(?<=[.?!])\s+', text) if s.strip()]


def erzaehlweise(ana, segs, dauer):
    volltext = re.sub(r'\s+', ' ', ' '.join(t for _, t in segs))
    n = len(woerter(volltext)) or 1

    jahre = [int(m.group(1)) for m in JAHR.finditer(volltext)]
    jahre += [-int(m.group(1)) for m in BC.finditer(volltext)]
    rueck = sum(1 for a, b in zip(jahre, jahre[1:]) if b < a)

    fragen = offen = 0
    for m in re.finditer(r"\?", volltext):
        fragen += 1
        if not ana.ANTWORTMARKER.search(volltext[m.start():m.start() + 1200]):
            offen += 1

    kand = collections.Counter()
    for m in re.finditer(r"\b([A-Z][a-z]{2,})\b", volltext):
        if m.group(1) in NICHTPERSON or m.start() == 0:
            continue
        if re.search(r"[.?!]\s$", volltext[max(0, m.start() - 2):m.start()]):
            continue
        kand[m.group(1)] += 1

    schluss = ' '.join(t for s, t in segs if s >= dauer * 0.9)
    schluss_w = woerter(schluss) or ['x']
    eroeffnung = ' '.join(volltext.split()[:35])

    return {
        'woerter': n,
        'jahre_genannt': len(jahre),
        'jahre_rueckspruenge': rueck,
        'jahre_rueck_anteil': round(rueck / (len(jahre) - 1) * 100, 1) if len(jahre) > 1 else None,
        'rueckblende_marker': len(RUECKBLENDE.findall(volltext)),
        'ich_treffer': len(ICH.findall(volltext)),
        'ich_pro_1000w': round(len(ICH.findall(volltext)) / n * 1000, 1),
        'haltung_marker': len(HALTUNG.findall(volltext)),
        'haltung_pro_1000w': round(len(HALTUNG.findall(volltext)) / n * 1000, 1),
        'imperativ_marker': len(IMPERATIV.findall(volltext)),
        'personen_anzahl': sum(1 for c in kand.values() if c >= 2),
        'personen_apposition': len(set(x for tup in APPOSITION.findall(volltext) for x in tup if x)),
        'fragen': fragen,
        'fragen_offen': offen,
        'cta_gesamt': len(CTA.findall(volltext)),
        'cta_im_schluss': len(CTA.findall(schluss)),
        'ursache_wendung': len(URSACHE.findall(volltext)),
        'bestaetigungsfloskel': len(BESTAETIGUNG.findall(volltext)),
        'level_marken': len(LEVEL.findall(volltext)),
        'eroeffnung_grosszahl': bool(GROSSZAHL.search(eroeffnung)),
        'eroeffnung_superlativ': bool(SUPERLATIV.search(eroeffnung)),
        'schluss_woerter': len(schluss_w),
        'schluss_frage': schluss.count('?'),
        'schluss_du_pro_1000w': round(len(ana.PRONOMEN['du'].findall(schluss)) / len(schluss_w) * 1000, 1),
    }


# ------------------------------------------------------------------- Messung
def messen():
    ana = modul('ana', os.path.join(REGELN, 'skriptanatomie_inkaxen.py'))
    met = modul('met', os.path.join(REGELN, 'skript_metriken.py'))
    meta = json.load(open(os.path.join(HIER, 'uf_videos.json')))
    roh = json.load(open(os.path.join(HIER, 'uf_transkripte.json')))

    anatomie, erz = {}, {}
    satz_stat = collections.defaultdict(lambda: collections.Counter())
    satz_laengen = collections.defaultdict(list)
    anaphern = collections.Counter()
    satz_gesamt = collections.Counter()

    for r in roh['transcripts']['results']:
        vid = r['videoId']
        segs = ana.segmente(r['data'])
        m = meta[vid]

        # --- Teil 1: unveraenderte Funktion aus dem Repo ---
        e = ana.messen(vid, m['titel'], segs, m['laenge_s'])
        volltext = ' '.join(t for _, t in segs)
        nw = len(woerter(volltext)) or 1
        ep = met.marker_zaehlen(volltext, met.EPISTEMISCH_RE)
        e['epistemische_marker'] = ep
        e['epistemisch_pro_1000w'] = round(ep / nw * 1000, 1)
        e.update({'form': m['form'], 'titel': m['titel'], 'views': m['views'],
                  'monat': m['monat']})
        anatomie[vid] = e

        # --- Teil 3 ---
        erz[vid] = dict(erzaehlweise(ana, segs, m['laenge_s']),
                        form=m['form'], titel=m['titel'])

        # --- Satzbauformen ---
        vorher = None
        for s in echte_saetze(segs):
            w = woerter(s)
            if not w:
                continue
            for gruppe in ('ALLE', m['form']):
                satz_gesamt[gruppe] += 1
                satz_laengen[gruppe].append(len(w))
                satz_stat[gruppe][w[0].lower()] += 1
                if vorher == w[0].lower():
                    anaphern[gruppe] += 1
                for k, rx in FORMEN.items():
                    if rx.search(s):
                        satz_stat[gruppe]['#' + k] += 1
            vorher = w[0].lower()

    json.dump(anatomie, open(os.path.join(HIER, 'uf_skript_anatomie.json'), 'w'),
              ensure_ascii=False, indent=1)
    json.dump(erz, open(os.path.join(HIER, 'uf_erzaehlweise.json'), 'w'),
              ensure_ascii=False, indent=1)

    gruppen = {'ALLE': list(meta),
               'POV': [v for v in meta if meta[v]['form'] == 'POV'],
               'CHRON': [v for v in meta if meta[v]['form'] == 'CHRON']}

    def med(ids, quelle, feld, sub=None):
        vals = []
        for v in ids:
            x = quelle[v][feld]
            if sub is not None:
                x = x[sub]
            if x is not None:
                vals.append(x)
        return round(st.median(vals), 1) if vals else None

    print("=" * 78)
    print("TEIL 1 — Skriptanatomie (Mediane)")
    print("=" * 78)
    print(f"{'Groesse':<28} " + ' '.join(f"{g:>9}" for g in gruppen))
    zeilen = [('woerter', None, 'Woerter'), ('dauer_s', None, 'Dauer s'), ('wpm', None, 'WPM'),
              ('kernfrage_pct', None, 'Kernfrage %'), ('antwort_pct', None, 'Antwort %'),
              ('pronomen_pro_1000w', 'du', 'du /1000W'), ('pronomen_pro_1000w', 'wir', 'wir /1000W'),
              ('pronomen_pro_1000w', 'man', 'man /1000W'), ('pronomen_pro_1000w', 'sie', 'sie /1000W'),
              ('satzlaenge_median', None, 'Satzlaenge (ASR-Proxy)'),
              ('kurzwort_anteil_pct', None, 'kurz <7 Zeichen %'),
              ('epistemisch_pro_1000w', None, 'epistemisch /1000W')]
    for feld, sub, name in zeilen:
        print(f"{name:<28} " + ' '.join(f"{str(med(ids, anatomie, feld, sub)):>9}" for ids in gruppen.values()))

    print(f"\n{'du je 1.000W je Fuenftel':<28}")
    for g, ids in gruppen.items():
        z = [round(st.median([anatomie[v]['fuenftel'][i]['zweite_person'] /
                              anatomie[v]['fuenftel'][i]['woerter'] * 1000
                              for v in ids if anatomie[v]['fuenftel'][i]['woerter']]), 1)
             for i in range(5)]
        print(f"  {g:<10} {z}")
    for g, ids in gruppen.items():
        d = [anatomie[v]['antwort_drittel'] for v in ids]
        print(f"  Antwort im 1. Drittel {g:<6} {d.count('erstes')}/{len(d)}")

    print()
    print("=" * 78)
    print("TEIL 3 — Erzaehlweise (Median / Summe)")
    print("=" * 78)
    felder = ['jahre_genannt', 'jahre_rueckspruenge', 'jahre_rueck_anteil',
              'rueckblende_marker', 'ich_pro_1000w', 'haltung_pro_1000w',
              'imperativ_marker', 'personen_anzahl', 'personen_apposition',
              'fragen', 'fragen_offen', 'cta_gesamt', 'ursache_wendung',
              'bestaetigungsfloskel', 'level_marken', 'schluss_woerter',
              'schluss_frage', 'schluss_du_pro_1000w']
    print(f"{'Feld':<24} " + ' '.join(f"{g+' med':>10} {'sum':>7}" for g in gruppen))
    for f in felder:
        zeile = f"{f:<24} "
        for ids in gruppen.values():
            s = sum(erz[v][f] for v in ids if isinstance(erz[v][f], (int, float)))
            zeile += f"{str(med(ids, erz, f)):>10} {round(s, 1):>7} "
        print(zeile)

    print()
    print("=" * 78)
    print("TEIL 3 — Satzbauformen (Anteil aller Saetze der Gruppe)")
    print("=" * 78)
    for g in gruppen:
        n = satz_gesamt[g] or 1
        print(f"\n--- {g}  ({n} Saetze) ---")
        print(f"  Satzlaenge Median (echte Interpunktion) {st.median(satz_laengen[g]):.1f}")
        print(f"  Saetze unter 5 Woertern  {sum(1 for x in satz_laengen[g] if x < 5)/n*100:.1f} %")
        print(f"  Anapher                  {anaphern[g]/n*100:.1f} %")
        for k in FORMEN:
            print(f"    {k:<14} {satz_stat[g]['#'+k]:>5}  {satz_stat[g]['#'+k]/n*100:>5.2f} %")
        print("  haeufigste Satzanfangswoerter:")
        for a, c in [(a, c) for a, c in satz_stat[g].most_common(40) if not a.startswith('#')][:8]:
            print(f"    {a:<14} {c:>5}  {c/n*100:>5.2f} %")


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--aufbereiten':
        aufbereiten(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == '--messen':
        messen()
    else:
        sys.exit(__doc__)
