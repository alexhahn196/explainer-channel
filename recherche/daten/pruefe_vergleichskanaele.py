#!/usr/bin/env python3
"""
pruefe_vergleichskanaele.py - sucht Ausreisser in den letzten 90 Tagen bei den
sechs Vergleichskanaelen und haelt sie gegen unsere 42 Fragen.

(1) MEDIAN je Kanal ueber den gesamten abrufbaren Katalog. Ein Video gilt als
    Treffer, wenn es im 90-Tage-Fenster liegt UND >= 3x den Kanalmedian hat.
    Der Median ist gewaehlt, nicht der Mittelwert: bei 1-2 Ausreissern pro
    Kanal (Faktor 100+) waere jeder Mittelwert von genau den Videos bestimmt,
    die man messen will.

(2) TITELAEHNLICHKEIT unserer 42 Fragen gegen die Treffer UND gegen alle
    Videos im Fenster. Methode wortgleich aus pruefe_fragen.py uebernommen
    (Funktionswoerter raus, einfaches Stemming, Grenze 50 %), damit die Zahlen
    mit fragen_bewertet.json vergleichbar sind.

(3) MUSTERTEST: trennt ein Titelmerkmal die Treffer vom Rest? Gemessen wird
    nicht die Haeufigkeit im Treffer-Set, sondern der Lift gegen die
    Grundrate im selben Fenster - sonst faellt jedes Merkmal auf, das die
    Nische ohnehin durchgehend benutzt. Dazu Fishers exakter Test,
    einseitig, mit Bonferroni-Schwelle fuer die Zahl der geprueften Merkmale.

(4) GEGENPROBE: dasselbe Thema bei mehreren Kanaelen nebeneinander.

Datenquelle: vergleichskanaele_videos.json (NexLev-Abzug vom 17.08.2026).

Aufruf: python3 recherche/daten/pruefe_vergleichskanaele.py
"""
import json
import re
import statistics
import sys
from math import comb

BASIS = "/home/user/explainer-channel/recherche/daten"

# Das Fenster. NexLev rechnet publishDate aus dem relativen YouTube-Label
# zurueck ("3 months ago" -> heute minus 3 Monate), das exakte Uploaddatum ist
# darin nicht enthalten. Der Bucket "3 months ago" (2026-05-17) liegt damit
# rechnerisch 92 Tage zurueck, tatsaechlich aber irgendwo zwischen ~75 und
# ~105 Tagen. Er wird mitgenommen; ein Schnitt bei exakt 90 Tagen wuerde einen
# Bucket zerschneiden, dessen Innenaufloesung die Quelle gar nicht hergibt.
FENSTER_AB = "2026-05-17"
FAKTOR_TREFFER = 3.0

# ---------------------------------------------------------------- (1) Titel
# ab hier wortgleich aus pruefe_fragen.py
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
# bis hier wortgleich aus pruefe_fragen.py


# ------------------------------------------------------------- (3) Mustertest
MERKMALE = {
    "Fragetitel (endet auf ?)": lambda t: t.strip().endswith("?"),
    "beginnt How/Why/What/...": lambda t: t.split()[0].lower() in {
        "how", "why", "what", "when", "where", "who", "did", "do", "does",
        "is", "are", "can"},
    "'ancient' im Titel": lambda t: "ancient" in t.lower(),
    "'human(s)' im Titel": lambda t: re.search(r"\bhumans?\b", t.lower()) is not None,
    "'ancient human(s)'": lambda t: "ancient human" in t.lower(),
    # Wortgrenzen sind hier nicht kosmetisch: "cat" steckt in "education",
    # "rain" in "brain" - ohne \b zaehlt der Test die falschen Videos.
    "Tier-Thema": lambda t: re.search(
        r"\b(animals?|spiders?|cats?|insects?|predators?|mosquitoe?s?)\b",
        t.lower()) is not None,
    "Zuschauer-Koerper (you/we)": lambda t: any(
        w in t.lower().split() for w in ["you", "your", "we", "us", "our"]),
    "'surviv...'": lambda t: "surviv" in t.lower(),
    "Versalien-Wort": lambda t: any(w.isupper() and len(w) > 3 for w in t.split()),
}

GEGENPROBEN = [
    (r"winter|freez", "Winter/Kaelte"), (r"\brain(ed|ing)?\b", "Regen"),
    (r"alcohol", "Alkohol"), (r"smok", "Rauchen"), (r"bathroom", "Toilette"),
    (r"bored|boredom", "Langeweile"), (r"marry|marri", "Heirat"),
    (r"\bpredators?\b", "Raubtiere"), (r"\bsleep\b|\bbeds?\b", "Schlafen"),
]


def fisher(a, b, c, d):
    """Einseitiger exakter Test auf Anreicherung des Merkmals bei den Treffern.

    a = Treffer mit Merkmal, b = Treffer ohne, c = Rest mit, d = Rest ohne.
    """
    n, r1, k = a + b + c + d, a + b, a + c
    return sum(comb(k, x) * comb(n - k, r1 - x) / comb(n, r1)
               for x in range(a, min(r1, k) + 1))


def main():
    daten = json.load(open(f"{BASIS}/vergleichskanaele_videos.json"))
    fragen = json.load(open(f"{BASIS}/fragen_kanal2.json"))

    print(f"Stand {daten['_stand']} | Fenster ab {FENSTER_AB} | "
          f"Treffer = >= {FAKTOR_TREFFER:.0f}x Kanalmedian\n")

    alle_treffer = []
    alle_fenster = []
    for name, k in daten["kanaele"].items():
        vids = k["videos"]
        views = sorted(v[1] for v in vids)
        median = statistics.median(views)
        fenster = [v for v in vids if v[0] >= FENSTER_AB]
        median_f = statistics.median([v[1] for v in fenster]) if fenster else 0
        alle_fenster += [{"kanal": name, "datum": v[0], "views": v[1],
                          "titel": v[3], "faktor": v[1] / median} for v in fenster]

        print(f"=== {name} ({k['abos']:,} Abos) ".replace(",", ".").ljust(64, "="))
        print(f"    {len(vids)} Videos abrufbar, davon {len(fenster)} im Fenster")
        print(f"    Median gesamt {median:>9,.0f} | Median im Fenster {median_f:>9,.0f}"
              .replace(",", "."))
        print(f"    Spanne {views[0]:,} - {views[-1]:,}".replace(",", "."))

        treffer = sorted([v for v in fenster if v[1] >= FAKTOR_TREFFER * median],
                         key=lambda v: -v[1])
        if not treffer:
            print("    keine Treffer\n")
            continue
        for datum, vw, laenge, titel in treffer:
            print(f"    {vw/median:>6.1f}x  {vw:>9,}  {datum}  {laenge:>5}  {titel}"
                  .replace(",", "."))
            alle_treffer.append({"kanal": name, "datum": datum, "views": vw,
                                 "laenge": laenge, "titel": titel,
                                 "faktor": round(vw / median, 1),
                                 "median": median})
        print()

    # -------------------------------------------------- (2) gegen die 42 Fragen
    nach_titel = {v["titel"]: v for v in alle_fenster}
    print("=" * 68)
    for was, menge in (("Treffer", [t["titel"] for t in alle_treffer]),
                       ("alle Videos im Fenster", [v["titel"] for v in alle_fenster])):
        print(f"\nTitelpruefung: 42 Fragen gegen {len(menge)} {was}, Grenze 50 %\n")
        bewertet = []
        for f in fragen:
            anteil, quelle, gem, n = aehnlichkeit(f["titel"], menge)
            bewertet.append({**f, "aehnlichkeit": round(anteil, 4), "naechster": quelle,
                             "geteilt": sorted(gem), "woerter": n,
                             "besetzt": "ZU NAH" if anteil > 0.5 else "frei"})
        for e in sorted(bewertet, key=lambda e: -e["aehnlichkeit"])[:6]:
            marke = "ZU NAH" if e["aehnlichkeit"] > 0.5 else "frei  "
            gegen = nach_titel.get(e["naechster"])
            print(f"{e['id']}  {e['aehnlichkeit']*100:5.1f} %  {marke}  {e['titel']}")
            print(f"        naechster: {e['naechster']}")
            if gegen:
                print(f"        dessen Leistung: {gegen['faktor']:.2f}x Median "
                      f"({gegen['views']:,} Views, {gegen['kanal']})".replace(",", "."))
            print(f"        geteilt: {e['geteilt']}")
        print(f"  ueber 50 %: {sum(1 for e in bewertet if e['besetzt']=='ZU NAH')} von 42")
        if was == "Treffer":
            gegen_treffer = bewertet

    # ------------------------------------------------------- (3) Mustertest
    hits = [v for v in alle_fenster if v["faktor"] >= FAKTOR_TREFFER]
    rest = [v for v in alle_fenster if v["faktor"] < FAKTOR_TREFFER]
    schwelle = 0.05 / len(MERKMALE)
    print("\n" + "=" * 68)
    print(f"Mustertest: {len(hits)} Treffer gegen {len(rest)} Nicht-Treffer")
    print(f"Bonferroni-Schwelle bei {len(MERKMALE)} Merkmalen: {schwelle:.4f}\n")
    print(f"{'Merkmal':28}{'Treffer':>9}{'Rest':>9}{'Lift':>7}{'p':>8}  Urteil")
    muster = []
    for nm, pruef in MERKMALE.items():
        a = sum(1 for v in hits if pruef(v["titel"]))
        c = sum(1 for v in rest if pruef(v["titel"]))
        pa, pc = a / len(hits), c / len(rest)
        lift = pa / pc if pc else float("inf")
        p = fisher(a, len(hits) - a, c, len(rest) - c)
        urteil = "haelt" if p < schwelle else "faellt durch"
        print(f"{nm:28}{pa:>8.0%}{pc:>9.0%}{lift:>6.2f}x{p:>8.3f}  {urteil}")
        muster.append({"merkmal": nm, "treffer_anteil": round(pa, 3),
                       "rest_anteil": round(pc, 3), "lift": round(lift, 2),
                       "p": round(p, 4), "haelt": p < schwelle})

    # -------------------------------------------------------- (4) Gegenprobe
    print("\n" + "=" * 68)
    print("Gegenprobe: dasselbe Thema, verschiedene Kanaele\n")
    for stich, label in GEGENPROBEN:
        tr = sorted([v for v in alle_fenster if re.search(stich, v["titel"].lower())],
                    key=lambda v: -v["faktor"])
        if len(tr) < 2:
            continue
        spanne = tr[0]["faktor"] / tr[-1]["faktor"]
        print(f" {label} - Spanne {spanne:.0f}x zwischen bestem und schwaechstem:")
        for v in tr:
            print(f"   {v['faktor']:>6.2f}x  {v['views']:>9,}  {v['kanal']:20} "
                  f"{v['titel']}".replace(",", "."))
        print()

    json.dump({"treffer": alle_treffer, "fragen": gegen_treffer, "muster": muster,
               "fenster": alle_fenster},
              open(f"{BASIS}/vergleichskanaele_bewertet.json", "w"),
              indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
