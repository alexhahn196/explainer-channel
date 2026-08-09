#!/usr/bin/env python3
"""
Aussprache-QA der Eigennamen.

Formel §5b fuehrt das als PFLICHT: der einzige stimmseitige Mangel mit
Trennschaerfe war falsche Betonung beim Verlierer C ("so-LACE", "super-VISE").
Psalmen 1-89 stecken voller hebraeischer Namen, die kein TTS-Modell haeufig
gesehen hat - Jeduthun, Meshech, Ephraim, Selah.

Verfahren: Aus dem Skript werden Eigennamen gezogen (grossgeschrieben, nicht
satzanfaenglich, kein gelaeufiges Wort). Fuer jedes Vorkommen wird geprueft,
was die Spracherkennung an dieser Stelle verstanden hat.

**Grenze des Verfahrens, ausdruecklich:** Eine Abweichung heisst NICHT
automatisch, dass die Stimme falsch spricht. In Runde 1 stellte sich
"Nathanael" -> "Nathaniel" und "Cephas" -> "Sephas" als korrekte Aussprache
bei abweichender ASR-Schreibung heraus. Gemeldet wird deshalb, WAS die
Erkennung gehoert hat - die Entscheidung, ob das ein Fehler ist, bleibt beim
Gegenhoeren. Automatisch beanstandet wird nur, was klanglich weit weg liegt.

Aufruf:
    python3 produktion/pipeline/qa_namen.py V1
    python3 produktion/pipeline/qa_namen.py V1 --top 60
"""
import argparse
import difflib
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import arbeit  # noqa: E402

# Grossgeschriebene Woerter, die keine Eigennamen im gesuchten Sinn sind.
GELAEUFIG = {
    "god", "lord", "jesus", "christ", "father", "son", "spirit", "holy", "amen",
    "psalm", "chapter", "first", "second", "third", "selah", "i", "o", "oh",
    "he", "his", "him", "the", "and", "but", "for", "yet", "so", "then", "when",
    "who", "whom", "whose", "which", "that", "this", "these", "those", "there",
    "let", "may", "blessed", "praise", "hallelujah", "king", "israel", "lorde",
}
KONSONANTEN = re.compile(r"[aeiouy]+")


def skelett(w):
    """Konsonantengeruest - unempfindlich gegen Vokalschreibweisen."""
    return KONSONANTEN.sub("", w.lower())


def aehnlich(a, b):
    """Klangnaehe zweier Schreibweisen, grob."""
    a, b = a.lower(), b.lower()
    direkt = difflib.SequenceMatcher(a=a, b=b).ratio()
    sk = difflib.SequenceMatcher(a=skelett(a), b=skelett(b)).ratio()
    return max(direkt, sk)


WORT = re.compile(r"[A-Za-z][A-Za-z’']*")


def namen_im_text(text):
    """Grossgeschriebene Woerter, die nicht am Satzanfang stehen.

    Ueber einen Regex statt ueber split(): sonst haengen Gedankenstriche am
    Wort ("Sinai—", "God—through") und jeder Vergleich geht daneben.
    """
    aus = []
    for m in WORT.finditer(text):
        w = m.group(0)
        if len(w) < 3 or not w[0].isupper() or w.lower() in GELAEUFIG:
            continue
        if not w[1:].replace("’", "").replace("'", "").islower():
            continue
        davor = text[:m.start()].rstrip()
        if not davor or re.search(r'[.!?:;][”"’]?$', davor):
            continue                       # Satzanfang
        aus.append(w)
    return aus


def eigennamen(segmente):
    zaehler = Counter()
    for s in segmente:
        zaehler.update(namen_im_text(s["text"]))
    return zaehler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--top", type=int, default=45,
                    help="wie viele der seltensten Namen geprueft werden")
    ap.add_argument("--grenze", type=float, default=0.55,
                    help="Klangnaehe, unterhalb derer beanstandet wird")
    a = ap.parse_args()

    pfad_asr = arbeit(a.video, "asr.json")
    if not os.path.exists(pfad_asr):
        raise SystemExit(f"{pfad_asr} fehlt — erst Schritt 6 laufen lassen "
                         "(dort entsteht die Erkennung).")
    skript = json.load(open(arbeit(a.video, "skript.json"), encoding="utf-8"))
    chunks = json.load(open(arbeit(a.video, "chunks.json"), encoding="utf-8"))["chunks"]
    asr = json.load(open(pfad_asr, encoding="utf-8"))

    zaehler = eigennamen(skript["segmente"])
    # ALLE Namen pruefen, nicht nur die seltensten. Ein Positionsfenster
    # waere schneller, trifft aber daneben, sobald die Erkennung ein Wort
    # auslaesst - dann wird ein Nachbarwort als "Treffer" gemeldet und der
    # Bericht ist wertlos. Deshalb der ganze Chunk als Suchraum.
    kandidaten = sorted(zaehler)
    gesucht = {w.lower(): w for w in kandidaten}

    treffer = {w: [] for w in kandidaten}
    for c, worte in zip(chunks, asr):
        erkannt = [(x[0].strip(".,;:!?()[]\"'“”’—–"), x[1]) for x in worte]
        erkannt = [e for e in erkannt if e[0]]
        for sw in namen_im_text(c["text"]):
            if sw.lower() not in gesucht or not erkannt:
                continue
            best = max(erkannt, key=lambda e: aehnlich(sw, e[0]))
            treffer[gesucht[sw.lower()]].append(
                (best[0], round(aehnlich(sw, best[0]), 2),
                 round(c["start_s"] + best[1], 1)))

    zeilen, beanstandet = [], []
    for w in kandidaten:
        t = treffer[w]
        if not t:
            zeilen.append((w, zaehler[w], "—", 0.0, None, "nicht auffindbar"))
            continue
        # Der SCHLECHTESTE Treffer entscheidet: ein Name, der 9-mal sitzt
        # und einmal nicht, ist genau der Fall, den man hoeren will.
        bester = min(t, key=lambda x: x[1])
        schnitt = sum(x[1] for x in t) / len(t)
        urteil = ("gut getroffen" if bester[1] >= 0.85 else
                  "abweichende Schreibung" if bester[1] >= a.grenze else
                  "WEIT ENTFERNT — gegenhören")
        if bester[1] < a.grenze:
            beanstandet.append((w, bester[0], bester[2]))
        zeilen.append((w, zaehler[w], bester[0], round(schnitt, 2), bester[2], urteil))

    zeilen.sort(key=lambda z: z[3])
    zeilen = zeilen[:a.top]
    bericht = {
        "geprueft": len(kandidaten),
        "eigennamen_gesamt": len(zaehler),
        "vorkommen_gesamt": int(sum(zaehler.values())),
        "beanstandet": [{"name": w, "asr": g, "bei_s": t} for w, g, t in beanstandet],
        "tabelle": [{"name": w, "vorkommen": n, "asr": g, "naehe_mittel": s,
                     "erstes_bei_s": t, "urteil": u} for w, n, g, s, t, u in zeilen],
    }
    json.dump(bericht, open(arbeit(a.video, "qa_namen.json"), "w"),
              ensure_ascii=False, indent=1)

    print(f"\nAUSSPRACHE-QA {a.video}")
    print(f"  {len(zaehler)} verschiedene Eigennamen, {sum(zaehler.values())} Vorkommen "
          f"— alle geprüft. Gezeigt: die {len(zeilen)} schwächsten.\n")
    print(f"  {'Name':16s} {'n':>4}  {'ASR hörte':18s} {'Nähe':>5}  bei      Urteil "
          f"(Nähe = schlechtestes Vorkommen)")
    for w, n, g, s, t, u in zeilen:
        zeit = f"{int(t)//3600}:{(int(t)%3600)//60:02d}:{int(t)%60:02d}" if t else "—"
        print(f"  {w:16s} {n:>4}  {g:18s} {s:>5.2f}  {zeit:8s} {u}")
    print(f"\n  Zu beanstanden: {len(beanstandet)}"
          + (f" → {[b[0] for b in beanstandet]}" if beanstandet else " — keiner"))
    print("  Hinweis: geringe Nähe ist ein Hörauftrag, kein Befund. Die "
          "Spracherkennung\n  schreibt Namen oft anders, als sie korrekt "
          "gesprochen werden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
