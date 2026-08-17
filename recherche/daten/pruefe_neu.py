#!/usr/bin/env python3
"""Prueft Kandidaten fuer die fuenf neuen Fragen.

Methode wortgleich aus recherche/daten/pruefe_fragen.py uebernommen -
nur BASIS korrigiert (dort zeigt es noch auf /home/user/BibelTube) und
zusaetzlich Aehnlichkeit gegen die 42 bestehenden Fragen (Doppelpruefung).
"""
import json, re, sys, time, urllib.parse, urllib.request

BASIS = "/home/user/explainer-channel/recherche/daten"
UA = "BibelTube-Recherche/1.0 (mailto:alexhahn196@gmail.com)"

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


def hole(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def crossref(phrase):
    stichworte = [w.lower()[:5] for w in phrase.split() if len(w) > 3]
    url = ("https://api.crossref.org/works?rows=8&select=title,DOI"
           "&query.bibliographic=" + urllib.parse.quote(phrase))
    for versuch in range(3):
        try:
            status, roh = hole(url)
            if status != 200:
                continue
            m = json.loads(roh)["message"]
            treffer, beispiel, alle = 0, None, []
            for eintrag in m["items"]:
                titel = " ".join(eintrag.get("title") or [])
                alle.append(titel[:100])
                if sum(1 for s in stichworte if s in titel.lower()) >= 2:
                    treffer += 1
                    if beispiel is None:
                        beispiel = titel[:110]
            return treffer, m["total-results"], beispiel, alle
        except Exception:
            time.sleep(2 * (versuch + 1))
    return -1, -1, None, []


def wikipedia(artikel):
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
    kandidaten = json.load(open(sys.argv[1]))
    korpus = json.load(open(f"{BASIS}/besetzung_erklaerkanal.json"))
    fremde = [z[3] for z in korpus]
    alt = [f["titel"] for f in json.load(open(f"{BASIS}/fragen_kanal2.json"))]

    ergebnis = []
    for k in kandidaten:
        anteil, quelle, gem, n = aehnlichkeit(k["titel"], fremde)
        d_anteil, d_quelle, d_gem, _ = aehnlichkeit(k["titel"], alt)
        cr_e, cr_g, beispiel, alle = crossref(k["cr"])
        wb, wtitel = wikipedia(k["wiki"])
        b = note(cr_e, wb)
        ergebnis.append({**k, "aehnlichkeit": round(anteil, 4), "naechster": quelle,
                         "geteilt": sorted(gem), "woerter": n,
                         "dupl": round(d_anteil, 4), "dupl_naechster": d_quelle,
                         "cr_einschlaegig": cr_e, "cr_gesamt": cr_g,
                         "cr_beispiel": beispiel, "cr_alle": alle,
                         "wiki_bytes": wb, "wiki_titel": wtitel, "belegbarkeit": b})
        print(f"{k['id']:<8} Ae={anteil*100:5.1f}%  dupl={d_anteil*100:5.1f}%  "
              f"cr={cr_e}/8  wiki={wb:>7}  {b:<10}  {k['titel']}")
        print(f"         phrase: {k['cr']}")
        if beispiel:
            print(f"         Beleg:  {beispiel}")
        if anteil >= 0.25:
            print(f"         naechster: {quelle}  geteilt={sorted(gem)}")
        if d_anteil >= 0.5:
            print(f"         DOPPEL?  {d_quelle}")
        if cr_e < 8:
            for t in alle:
                stich = [w.lower()[:5] for w in k["cr"].split() if len(w) > 3]
                hit = sum(1 for s in stich if s in t.lower())
                if hit < 2:
                    print(f"           MISS({hit}): {t}")
        if wb == 0:
            print(f"         WARNUNG: kein Wikipedia-Artikel '{k['wiki']}'")
        print()
        time.sleep(0.4)

    json.dump(ergebnis, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
