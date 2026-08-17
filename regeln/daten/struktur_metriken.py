#!/usr/bin/env python3
"""struktur_metriken.py — Kanalstruktur (Teil B, STRUKTUR).

Je Kanal: Uploads/Woche (aus Katalog + aus der Videoliste gerechnet),
Videolaenge Median und Spanne (Long-Form), Kanalalter, Videoanzahl,
Monetarisierung, RPM, Quellenangaben ja/nein (Videobeschreibungen der
beiden vermessenen Videos), Beschreibungs-Bausteine.

Quellenangaben-Heuristik (offen dokumentiert): eine Videobeschreibung
zaehlt als "mit Quellen", wenn sie einen Abschnitt "sources"/"references"/
"bibliography" ODER >= 2 DOI-/Journal-/akademische Links enthaelt.
Blosse Social-Links zaehlen nicht.
"""
import json, glob, os, re, statistics as st
from datetime import date

ROH = os.path.join(os.path.dirname(__file__), '..', 'rohdaten')
SCRATCH = os.path.join(os.path.dirname(__file__), '..')
HEUTE = date(2026, 8, 10)

QUELLEN_KOPF = re.compile(r"\b(sources?|references?|bibliography|citations?|further reading)\b\s*[:\n]", re.I)
# Ein "Source:" direkt neben Musik-/Lizenzbegriffen ist eine Musikquelle, keine
# inhaltliche Quellenangabe (Fehltreffer bei Prehistoric Archive: Chris
# Zabriskie / Creative Commons). Solche Treffer werden verworfen.
MUSIKQUELLE = re.compile(
    r"(creativecommons|creative commons|\bartist\s*:|audio ?library|epidemic ?sound|"
    r"artlist|chriszabriskie|incompetech|kevin macleod|royalty[- ]free|\bmusic by\b)", re.I)
DOI = re.compile(r"\b(doi\.org|doi:|10\.\d{4,9}/)", re.I)
AKADEMISCH = re.compile(r"\b(jstor|pubmed|ncbi|nature\.com|sciencedirect|springer|cambridge\.org|oup\.com|academia\.edu|researchgate|journal|university press|\.edu/)\b", re.I)
LINK = re.compile(r"https?://\S+")


def beschreibung_analyse(txt):
    if not txt:
        return {'laenge_zeichen': 0, 'quellen': False, 'links': 0,
                'bausteine': []}
    links = LINK.findall(txt)
    akademische_links = [l for l in links if DOI.search(l) or AKADEMISCH.search(l)]
    # Quellenkopf nur zaehlen, wenn im Umfeld (+-200 Zeichen) keine
    # Musik-/Lizenzbegriffe stehen.
    echter_kopf = False
    for m in QUELLEN_KOPF.finditer(txt):
        umfeld = txt[max(0, m.start() - 200):m.end() + 200]
        if not MUSIKQUELLE.search(umfeld):
            echter_kopf = True
            break
    quellen = echter_kopf or len(akademische_links) >= 2
    bausteine = []
    if echter_kopf: bausteine.append('quellenblock')
    elif QUELLEN_KOPF.search(txt): bausteine.append('nur-musikquelle')
    if re.search(r"\b\d{1,2}:\d{2}\b", txt): bausteine.append('timestamps')
    if re.search(r"\bpatreon|member|join\b", txt, re.I): bausteine.append('support')
    if re.search(r"\bsubscribe\b", txt, re.I): bausteine.append('abo-aufruf')
    if re.search(r"\b(instagram|tiktok|twitter|x\.com|discord|facebook)\b", txt, re.I): bausteine.append('social')
    if re.search(r"\b(disclaimer|ai[- ]generated|artificial intelligence|for educational purposes)\b", txt, re.I): bausteine.append('disclaimer')
    if re.search(r"\bmusic\b.*\b(license|epidemic|artlist)\b|\b(license|epidemic|artlist)\b.*\bmusic\b", txt, re.I|re.S): bausteine.append('musiklizenz')
    # Kapitelmarken = Zeilen, die mit einem Zeitstempel beginnen. Sie zeigen
    # den Aufbau, den der Kanal selbst auszeichnet.
    kapitel = re.findall(r"^\s*\(?\d{1,2}:\d{2}(?::\d{2})?\)?\s*[-–—:|]?\s*\S",
                         txt, re.M)
    return {'laenge_zeichen': len(txt), 'quellen': quellen,
            'links': len(links), 'akademische_links': len(akademische_links),
            'kapitelmarken': len(kapitel), 'bausteine': bausteine}


def main():
    gruppen_meta = json.load(open(os.path.join(SCRATCH, 'gruppen.json')))
    katalog = {k['ytChannelId']: k for k in gruppen_meta['kanaele']}
    aus = {}
    for f in sorted(glob.glob(os.path.join(ROH, '*.json'))):
        d = json.load(open(f))
        kanal = d.get('kanal') or os.path.basename(f)
        cid = d.get('channelId')
        kat = (katalog.get(cid) or {}).get('katalog') or {}
        about = d.get('about') or {}
        if isinstance(about, str):
            try: about = json.loads(about)
            except Exception: about = {}
        lf = [v for v in d.get('videos', []) if (v.get('laenge_s') or 0) > 180]
        laengen = sorted(v['laenge_s'] for v in lf)
        # Kanalalter: joinedDate aus youtube_channel_about [gemessen] hat
        # Vorrang vor dem NexLev-Katalogdatum.
        gegr = about.get('joinedDate') or kat.get('gegruendet')
        alter_monate = alter_tage = None
        if gegr:
            j, m, t = map(int, str(gegr)[:10].split('-'))
            alter_tage = (HEUTE - date(j, m, t)).days
            alter_monate = round(alter_tage / 30.44, 1)
        # Uploads/Woche ueber die gesamte Lebenszeit (eigene Rechnung) neben
        # dem NexLev-Katalogwert, der die juengste Aktivitaet misst.
        vids_yt = about.get('videosCount')
        try:
            vids_yt = int(vids_yt)
        except (TypeError, ValueError):
            vids_yt = None
        # Lebenszeit-Kadenz auf Basis der ERFASSTEN Long-Form-Videos. Die
        # Zahl aus `about` enthaelt bei Kanaelen mit Shorts-Tab auch Shorts
        # (Historically: 69 in `about`, 21 im Videos-Tab) und taugt dafuer
        # nicht.
        up_lebenszeit = None
        if lf and alter_tage:
            up_lebenszeit = round(len(lf) / (alter_tage / 7.0), 2)
        e = {
            'gruppe': d.get('gruppe'), 'channelId': cid,
            'gegruendet': gegr, 'kanalalter_monate': alter_monate,
            'abonnenten_yt': about.get('subscriberCount'),
            'gesamtviews_yt': about.get('viewCount'),
            'videoanzahl_yt': vids_yt,
            'uploads_pro_woche_lebenszeit': up_lebenszeit,
            'land': about.get('country') or None,
            'videoanzahl_katalog': kat.get('gesamtvideos'),
            'videoanzahl_gesehen': len(d.get('videos', [])),
            'langform_gesehen': len(lf),
            'uploads_pro_woche_katalog': kat.get('uploads_pro_woche'),
            'monetarisiert': kat.get('monetarisiert'),
            'rpm_total': kat.get('rpm_total'),
            'monatsumsatz_usd': kat.get('monatsumsatz_usd'),
            'abonnenten': kat.get('abonnenten'),
            'laenge_median_s': st.median(laengen) if laengen else None,
            'laenge_min_s': laengen[0] if laengen else None,
            'laenge_max_s': laengen[-1] if laengen else None,
        }
        # Views-Verteilung ueber alle Long-Form-Videos. Der MEDIAN zeigt, was
        # ein durchschnittliches Video des Kanals erreicht — der Maximalwert
        # zeigt nur, ob je ein Video durchgeschlagen ist.
        views = sorted(v['views'] for v in lf if v.get('views') is not None)
        if views:
            e['views_median'] = int(st.median(views))
            e['views_min'] = views[0]
            e['views_max'] = views[-1]
            e['views_spreizung'] = round(views[-1] / max(st.median(views), 1))
        for rolle in ('treffer', 'schwach'):
            det = d.get(f'details_{rolle}') or {}
            if isinstance(det, str):
                try: det = json.loads(det)
                except Exception: det = {}
            besch = None
            if isinstance(det, dict):
                besch = det.get('description') or det.get('video_description')
                if besch is None:
                    for v in det.values():
                        if isinstance(v, dict) and 'description' in v:
                            besch = v['description']; break
            e[f'beschreibung_{rolle}'] = beschreibung_analyse(besch)
        e['quellenangaben'] = bool(e['beschreibung_treffer']['quellen'] or e['beschreibung_schwach']['quellen'])
        aus[kanal] = e
    ziel = os.path.join(os.path.dirname(__file__), 'struktur.json')
    json.dump(aus, open(ziel, 'w'), indent=1, ensure_ascii=False)
    print(f'-> {ziel}')
    for k, v in aus.items():
        print(f"{v['gruppe']} {k[:24]:24} alter {v['kanalalter_monate']} Mon | vids {v['videoanzahl_yt']} | "
              f"up/wo {v['uploads_pro_woche_lebenszeit']}/{v['uploads_pro_woche_katalog']} | "
              f"median {v['laenge_median_s']}s [{v['laenge_min_s']}-{v['laenge_max_s']}] | "
              f"quellen {v['quellenangaben']}")


if __name__ == '__main__':
    main()
