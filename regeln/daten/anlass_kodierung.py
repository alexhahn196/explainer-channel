#!/usr/bin/env python3
"""anlass_kodierung.py — testet B1: "Anlassnennung im Titel wirkt."

Prueft das Merkmal `anlass_genannt` an zwei Korpora:
  (1) Shadow of the Gods (UC7OMVRiJcIqoIHoC4u7lIsw), 38 Videos — der einzige
      Beleg, auf den sich die Wirkungsannahme in themen-erklaerkanal.md stuetzt.
  (2) dem bestehenden 429-Video-Korpus regeln/daten/themen_korpus.tsv,
      kanalintern, gleiche Methode wie regeln/themenwahl-test.md.

METHODE wortgleich aus themen_test.py uebernommen: kanalintern Median mit
Merkmal gegen Median ohne, Kanal zaehlt nur bei >= 3 Videos je Gruppe,
Zufallstest durch Mischen der Views INNERHALB des Kanals.

--------------------------------------------------------------------------
KODIERREGEL, vorab festgelegt (2026-08-17), zwei Stufen
--------------------------------------------------------------------------
Stufe A — ANLASS IM ENGEN SINN: Der Titel nennt eine zum Veroeffentlichungs-
  zeitpunkt LAUFENDE ODER UNMITTELBAR BEVORSTEHENDE fremde Produktion oder
  deren Urheber. Nur das ist ein "Anlass" im Sinne von themen-erklaerkanal.md,
  wo der Anlass ein datierbares Ereignis ist (Kinostart, Jubilaeum, Sonde).

Stufe B — FREMDMARKE IM WEITEN SINN: Der Titel nennt irgendeine fremde Marke,
  ein Studio, eine Franchise oder eine Figur aus fremdem IP — unabhaengig
  davon, ob dazu gerade etwas erscheint.

Beide werden getrennt gerechnet, weil der Auftragstext beides vermischt
("Marke, Film, Regisseur, Studio, laufende Produktion"). Die Behauptung in
themen-erklaerkanal.md stuetzt sich auf EIN Beispiel der Stufe A
("The Odyssey Nolan Won't Show You"), nicht auf Stufe B.

GRENZFAELLE, wie entschieden und warum:
  - "Hollywood"        -> B ja, A nein. Branchenbegriff, keine datierbare
                          Produktion. Kommt bei diesem Kanal als Floskel vor.
  - "Disney lied"      -> B ja, A nein. Bezug ist Hercules (1997) bzw. Hades
                          aus demselben Film — kein aktueller Anlass.
  - "Marvel"           -> B ja, A nein. Kein benannter aktueller Film.
  - "Nolan"            -> A ja. Regisseur der Odyssee-Verfilmung, Kinostart
                          17.07.2026, also zum Uploadzeitpunkt laufend.
  - "Percy Jackson"    -> B ja, A GRENZFALL: Serie lief 2026, aber der Titel
                          nennt keinen Termin. Konservativ als A nein gefuehrt;
                          die Gegenrechnung mit A ja steht im Bericht.
  - "the Odyssey" ohne
    Nolan               -> beides nein. Bezeichnet das antike Epos, nicht den
                          Film; sonst waere jeder Stoffname eine Anlassnennung.
  - Anime/Spiele
    (Goku, Beerus,
     Gojo, Kratos)      -> B ja, A nein. Franchise ohne benannten Termin.

DIE KODIERUNG IST NICHT BLIND. Die Abrufzahlen lagen beim Kodieren vor; sie
kamen mit demselben API-Aufruf. Das ist der entscheidende Unterschied zu
themenwahl-test.md, dessen Klassifikation nachweislich vor dem View-Join
entstand (Commit 8ae6ad0). Der Befund hier ist entsprechend schwaecher zu
gewichten. Gegenmassnahme: die Regel ist rein lexikalisch (Wortliste unten),
also nicht je Titel nach Gefuehl entschieden und von jedem nachrechenbar.

Aufruf: python3 regeln/daten/anlass_kodierung.py
"""
import json
import pathlib
import random
import statistics
import sys

BASIS = pathlib.Path("/home/user/explainer-channel")
HEUTE = "2026-08-17"
ALTERSGRENZE = "2026-05-19"          # 90 Tage vor HEUTE
RUNDEN = 10000
random.seed(20260817)

# Stufe A: laufende/bevorstehende Produktion oder deren Urheber, namentlich
MARKER_A = ["nolan"]

# Stufe B: jede fremde Marke, Studio, Franchise, IP-Figur
MARKER_B = MARKER_A + [
    "marvel", "disney", "hollywood", "percy jackson", "aquaman", "superman",
    "goku", "beerus", "gojo", "kratos", "flash", "thanos", "spider-man",
    "spiderman", "ghost rider", "dragon ball", "god of war", "dc ",
]


def stufe(titel, marker):
    t = titel.lower()
    return any(m in t for m in marker)


def median(xs):
    return statistics.median(xs) if xs else None


def kanalintern(zeilen, merkmal_fn, min_pro_gruppe=3):
    """Median mit Merkmal / Median ohne, je Kanal; Rueckgabe je Kanal."""
    kanaele = {}
    for k, views, titel in zeilen:
        kanaele.setdefault(k, []).append((views, merkmal_fn(titel)))
    raus = {}
    for k, vs in kanaele.items():
        mit = [v for v, m in vs if m]
        ohne = [v for v, m in vs if not m]
        if len(mit) >= min_pro_gruppe and len(ohne) >= min_pro_gruppe:
            raus[k] = (median(mit) / median(ohne), len(mit), len(ohne),
                       median(mit), median(ohne))
    return raus


def zufallstest(zeilen, merkmal_fn, beobachtet, min_pro_gruppe=3):
    """Views innerhalb jedes Kanals mischen, Test wiederholen."""
    kanaele = {}
    for k, views, titel in zeilen:
        kanaele.setdefault(k, []).append((views, merkmal_fn(titel)))
    treffer = 0
    gueltig = 0
    for _ in range(RUNDEN):
        faktoren = []
        for k, vs in kanaele.items():
            v = [x[0] for x in vs]
            m = [x[1] for x in vs]
            random.shuffle(v)
            mit = [a for a, b in zip(v, m) if b]
            ohne = [a for a, b in zip(v, m) if not b]
            if len(mit) >= min_pro_gruppe and len(ohne) >= min_pro_gruppe:
                faktoren.append(median(mit) / median(ohne))
        if not faktoren:
            continue
        gueltig += 1
        if abs(__import__("math").log(median(faktoren))) >= abs(
                __import__("math").log(beobachtet)):
            treffer += 1
    return treffer / gueltig if gueltig else float("nan")


def bericht(name, zeilen, merkmal_fn):
    erg = kanalintern(zeilen, merkmal_fn)
    if not erg:
        print(f"  {name:38} keine auswertbaren Kanaele "
              f"(< 3 Videos in einer Gruppe)")
        return None
    faktoren = [v[0] for v in erg.values()]
    f = median(faktoren)
    p = zufallstest(zeilen, merkmal_fn, f)
    print(f"  {name:38} Faktor {f:6.2f}x  ({len(erg)} Kanal/Kanaele, p = {p:.3f})")
    for k, (fk, nm, no, mm, mo) in sorted(erg.items()):
        print(f"      {k:26} {fk:6.2f}x   mit {nm:3d} (Md {mm:>10,.0f})"
              f"   ohne {no:3d} (Md {mo:>10,.0f})".replace(",", "."))
    return f, p, erg


def main():
    print("=" * 78)
    print("B1 — Wirkt eine Anlassnennung im Titel?")
    print("=" * 78)

    # ---------------------------------------------------------- (1) SotG
    sotg = json.load(open(BASIS / "recherche/daten/shadow_of_the_gods.json"))["videos"]
    zeilen = [("Shadow of the Gods", v["views"], v["titel"]) for v in sotg]
    alt = [z for z, v in zip(zeilen, sotg) if v["datum"] < ALTERSGRENZE]

    print(f"\nShadow of the Gods — {len(zeilen)} Videos, "
          f"{len(alt)} davon aelter als 90 Tage\n")
    for stufe_name, marker in (("Stufe A (nur Nolan)", MARKER_A),
                               ("Stufe B (jede Fremdmarke)", MARKER_B)):
        fn = lambda t, m=marker: stufe(t, m)
        n_mit = sum(1 for _, _, t in zeilen if fn(t))
        print(f"{stufe_name}: {n_mit} von {len(zeilen)} Titeln tragen das Merkmal")
        bericht("alle Videos", zeilen, fn)
        bericht("nur > 90 Tage", alt, fn)
        # Ausreisserpruefung: bestes Video je Gruppe streichen
        mit = sorted([z for z in zeilen if fn(z[2])], key=lambda z: -z[1])
        ohne = sorted([z for z in zeilen if not fn(z[2])], key=lambda z: -z[1])
        if len(mit) > 3 and len(ohne) > 3:
            gekuerzt = mit[1:] + ohne[1:]
            print(f"      gestrichen: '{mit[0][2]}' ({mit[0][1]:,} Views) "
                  f"und '{ohne[0][2]}' ({ohne[0][1]:,} Views)".replace(",", "."))
            bericht("ohne bestes Video je Gruppe", gekuerzt, fn)
        print()

    # ------------------------------------------------------- (2) 429-Korpus
    print("=" * 78)
    print("Dasselbe Merkmal ueber den 429-Video-Korpus (NICHT blind kodiert)")
    print("=" * 78 + "\n")
    korpus = []
    with open(BASIS / "regeln/daten/themen_korpus.tsv") as fh:
        kopf = fh.readline().rstrip("\n").split("\t")
        i_k, i_t, i_v, i_d = (kopf.index("kanal"), kopf.index("titel"),
                              kopf.index("views"), kopf.index("datum"))
        for zeile in fh:
            s = zeile.rstrip("\n").split("\t")
            korpus.append((s[i_k], int(s[i_v]), s[i_t], s[i_d]))
    zeilen_k = [(k, v, t) for k, v, t, _ in korpus]
    alt_k = [(k, v, t) for k, v, t, d in korpus if d < ALTERSGRENZE]
    for stufe_name, marker in (("Stufe A (nur Nolan)", MARKER_A),
                               ("Stufe B (jede Fremdmarke)", MARKER_B)):
        fn = lambda t, m=marker: stufe(t, m)
        n_mit = sum(1 for _, _, t in zeilen_k if fn(t))
        print(f"{stufe_name}: {n_mit} von {len(zeilen_k)} Titeln")
        bericht("alle Videos", zeilen_k, fn)
        bericht("nur > 90 Tage", alt_k, fn)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
