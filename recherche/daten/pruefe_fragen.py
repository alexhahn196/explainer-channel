#!/usr/bin/env python3
"""
pruefe_fragen.py - prueft die Themenvorschlaege fuer Kanal 2 auf zwei Achsen.

(1) BESETZT: Titelaehnlichkeit gegen die geernteten Konkurrenztitel.
    Methode wortgleich uebernommen aus produktion/titel_pruefung.py
    (Funktionswoerter raus, einfaches Stemming, Grenze 50 %).

(2) BELEGBARKEIT: Stichprobe ueber Crossref (Zahl der Treffer zu einer
    fachlichen Suchphrase) und Wikipedia (existiert ein Artikel, wie lang).
    Beides sind die Quellen, die laut recherche/nischen-kanal-2.md aus dem
    Container erreichbar sind (Crossref 200, Wikipedia REST 200).

Aufruf: python3 recherche/daten/pruefe_fragen.py
"""
import json, re, sys, time, urllib.parse, urllib.request

BASIS = "/home/user/BibelTube/recherche/daten"
UA = "BibelTube-Recherche/1.0 (mailto:alexhahn196@gmail.com)"

# ---------------------------------------------------------------- (1) Titel
STOPP = {
    "a", "an", "the", "to", "of", "in", "on", "and", "or", "but", "for", "with",
    "is", "are", "was", "be", "am", "at", "by", "from", "as", "so", "that",
    "this", "these", "those", "it", "its", "will", "shall", "can", "do", "does",
    "did", "have", "has", "had", "there", "here", "then", "than", "into", "over",
    "under", "up", "down", "out", "all", "any", "some", "more", "just", "very",
}


def stamm(w):
    for endung in ("ing", "ed", "es", "s"):
        if len(w) > 4 and w.endswith(endung):
            return w[: -len(endung)]
    return w


def inhalt(titel):
    t = titel.lower().replace("’", "'")
    t = t.replace("you're", "you are").replace("don't", "do not")
    t = re.sub(r"[^a-z' ]", " ", t)
    woerter = [w.strip("'") for w in t.split()]
    return {stamm(w) for w in woerter if w and w not in STOPP and len(w) > 1}


def aehnlichkeit(mein, fremde):
    m = inhalt(mein)
    schlimmster = (0.0, None, set())
    for f in fremde:
        g = inhalt(f)
        if not m:
            continue
        anteil = len(m & g) / len(m)
        if anteil > schlimmster[0]:
            schlimmster = (anteil, f, m & g)
    return schlimmster[0], schlimmster[1], schlimmster[2], len(m)


# --------------------------------------------------------- (2) Belegbarkeit
def hole(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def crossref(phrase):
    """Trefferqualitaet statt Trefferzahl.

    Die Gesamttrefferzahl von Crossref ist als Mass wertlos: query.bibliographic
    verknuepft die Begriffe lose, jede Phrase liefert Millionen. Gemessen wird
    deshalb, wie viele der acht relevantesten Treffer im TITEL mindestens zwei
    der Suchbegriffe tragen - also echte Fachliteratur zum Thema sind.

    Rueckgabe: (einschlaegige von 8, Gesamttreffer, Beispieltitel) - (-1,..) = Fehler.
    """
    stichworte = [w.lower()[:5] for w in phrase.split() if len(w) > 3]
    url = ("https://api.crossref.org/works?rows=8&select=title,DOI"
           "&query.bibliographic=" + urllib.parse.quote(phrase))
    for versuch in range(3):
        try:
            status, roh = hole(url)
            if status != 200:
                continue
            m = json.loads(roh)["message"]
            treffer, beispiel = 0, None
            for eintrag in m["items"]:
                titel = " ".join(eintrag.get("title") or []).lower()
                if sum(1 for s in stichworte if s in titel) >= 2:
                    treffer += 1
                    if beispiel is None:
                        beispiel = " ".join(eintrag.get("title") or [])[:110]
            return treffer, m["total-results"], beispiel
        except Exception:
            time.sleep(2 * (versuch + 1))
    return -1, -1, None


def wikipedia(artikel):
    """(bytes des Artikels, Titel) - 0 = kein Artikel gefunden, -1 = Fehler."""
    url = ("https://en.wikipedia.org/w/api.php?action=query&format=json"
           "&prop=info&redirects=1&titles=" + urllib.parse.quote(artikel))
    for versuch in range(3):
        try:
            status, roh = hole(url)
            if status == 200:
                seiten = json.loads(roh)["query"]["pages"]
                for pid, p in seiten.items():
                    if pid == "-1" or "missing" in p:
                        return 0, artikel
                    return p.get("length", 0), p.get("title", artikel)
        except Exception:
            time.sleep(2 * (versuch + 1))
    return -1, artikel


def note(einschlaegig, wb):
    """Skala: einschlaegige Crossref-Treffer (von 8) x Wikipedia-Artikelgroesse.

    gut belegt  = >=4 von 8 Treffern thematisch einschlaegig UND Wikipedia-
                  Artikel >= 8.000 Bytes (also mehr als ein Stub)
    duenn       = 2-3 einschlaegige Treffer, oder Artikel 2.000-8.000 Bytes
    kaum etwas  = <=1 einschlaegiger Treffer, oder gar kein Wikipedia-Artikel
    """
    if einschlaegig < 0 or wb < 0:
        return "abruf fehlgeschlagen"
    if wb == 0 or einschlaegig <= 1:
        return "kaum etwas"
    if einschlaegig >= 4 and wb >= 8000:
        return "gut belegt"
    if einschlaegig >= 2 and wb >= 2000:
        return "duenn"
    return "kaum etwas"


def main():
    fragen = json.load(open(f"{BASIS}/fragen_kanal2.json"))
    korpus = json.load(open(f"{BASIS}/besetzung_erklaerkanal.json"))
    fremde = [z[3] for z in korpus]

    print(f"Titelpruefung gegen {len(fremde)} Konkurrenztitel, Grenze 50 %")
    print(f"Belegbarkeit ueber Crossref + Wikipedia, {len(fragen)} Fragen\n")

    ergebnis = []
    for f in fragen:
        anteil, quelle, gem, n = aehnlichkeit(f["titel"], fremde)
        einschlaegig, gesamt, beispiel = crossref(f["cr"])
        wb, wtitel = wikipedia(f["wiki"])
        b = note(einschlaegig, wb)
        ergebnis.append({
            **f, "aehnlichkeit": round(anteil, 4), "naechster": quelle,
            "geteilt": sorted(gem), "woerter": n,
            "cr_einschlaegig": einschlaegig, "cr_gesamt": gesamt,
            "cr_beispiel": beispiel,
            "wiki_bytes": wb, "wiki_titel": wtitel,
            "belegbarkeit": b,
            "besetzt": "ZU NAH" if anteil > 0.5 else "frei",
        })
        print(f"{f['id']}  {anteil*100:5.1f} %  {'ZU NAH' if anteil>0.5 else 'frei  '}  "
              f"cr={einschlaegig}/8  wiki={wb:>7}  {b:<10}  {f['titel']}")
        if beispiel:
            print(f"        Beleg: {beispiel}")
        if anteil > 0.35:
            print(f"        naechster: {quelle}")
            print(f"        geteilt: {sorted(gem)}")
        if wb == 0:
            print(f"        WARNUNG: kein Wikipedia-Artikel '{f['wiki']}'")
        time.sleep(0.4)

    json.dump(ergebnis, open(f"{BASIS}/fragen_bewertet.json", "w"),
              indent=1, ensure_ascii=False)

    v = sum(1 for e in ergebnis if e["besetzt"] == "ZU NAH")
    print(f"\nZu nah an der Besetzung: {v} von {len(ergebnis)}")
    from collections import Counter
    for k, z in Counter(e["belegbarkeit"] for e in ergebnis).items():
        print(f"  {k}: {z}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
