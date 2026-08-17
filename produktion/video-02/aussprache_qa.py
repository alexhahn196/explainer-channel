#!/usr/bin/env python3
"""Prueft die Aussprache aller Eigennamen in der fertigen Tonspur.

Aus produktion/video-01/aussprache_qa.py uebernommen; getauscht sind nur
die beiden Tabellen NAMEN und ZAHLEN. Das Verfahren bleibt: zwei
Erkenner hoeren die Spur ab, ohne den Solltext zu kennen, und die
Fundstelle wird ueber die vollstaendige Wortausrichtung bestimmt, nicht
ueber Ankerwoerter.

Was bei Video 2 anders ist: dort waren vier Korrekturen aus einem
gemessenen Hoerbericht uebernommen, hier ist KEINE gemessen. Diese
Pruefung ist also die erste Messung ueberhaupt, und sie prueft die
Lautfolge, nicht die Betonung.

Eine Grenze, die fuer zwei Namen dieses Videos besonders zaehlt: der
Erkenner normalisiert. Bei "LEV-it" gegen "LEE-vit" und bei "GUY-uh"
gegen "GAY-uh" schreibt er in beiden Faellen wahrscheinlich die
Normalform ("Leavitt", "Gaia"). Der Vokal ist damit nur teilweise
pruefbar und die Betonung gar nicht. Das steht so auch im Bericht.

Der Weg ist derselbe wie im Hoerbericht: zwei Spracherkenner hoeren die Spur
ab, ohne den Solltext zu kennen. Was sie schreiben, ist das, was tatsaechlich
zu hoeren war.

Wie die Fundstelle bestimmt wird — und warum nicht ueber Ankerwoerter
---------------------------------------------------------------------
Erster Versuch war, jede Stelle an ein paar Nachbarwoertern wiederzufinden
("quarry is called" …). Untauglich: kurze Anker wie "to the" treffen im Text
dutzendfach, und die Pruefung fuer *Ishtar* landete prompt fuenf Absaetze zu
frueh. Drei der gemeldeten Fehlformen waren reine Ortungsfehler.

Tragfaehig ist die vollstaendige Ausrichtung: der Solltext ist bekannt, also
wird die Erkennung Wort fuer Wort gegen ihn ausgerichtet (Levenshtein mit
Rueckverfolgung). Fuer jeden Namen steht damit fest, welche erkannten Woerter
ihm gegenueberstehen — auch dann, wenn der Name voellig verhoert wurde.

Wie das Urteil zu lesen ist
---------------------------
Geprueft wird gegen die erwartete LAUTFOLGE, nicht gegen die Schreibung.
Zwei Fallen dabei, beide real aufgetreten:

  * Der Erkenner normalisiert. Er hoert "P-R thirty-one" und schreibt "PR 31",
    er hoert "neb-yoo-kad-Nezzer the second" und schreibt "Nebuchadnezzar II".
    Das ist ein Beleg fuer richtige Aussprache, nicht gegen sie.
  * Ein Treffer der Sollschreibung beweist nichts ueber die Betonung. Der
    Erkenner schreibt "Tiwanaku", gleich ob die dritte oder die erste Silbe
    betont war. Betonung ist auf diesem Weg NICHT pruefbar und wird hier auch
    nicht behauptet.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import numpy as np

HIER = pathlib.Path(__file__).resolve().parent
SPUR = HIER / "ton" / "tonspur.mp3"
ASR_DATEI = HIER / "ton" / "_asr.json"

# Name -> (wie er im Sprechtext steht, akzeptierte Hoerformen)
# Die Sollform ist der Anker im Text; gesucht wird ihre Position, dann wird
# verglichen, was der Erkenner an dieser Stelle geschrieben hat.
NAMEN = [
    # Der haeufigste Name des Videos, 14 Vorkommen. Vorsicht bei der Lesung
    # dieses Ergebnisses: "Leavitt" als Erkennerausgabe belegt die Lautfolge
    # nur schwach, weil der Erkenner auch bei falscher Vokalqualitaet die
    # Normalform schreibt. Eindeutig falsch ist nur, was mit langem ee kommt.
    ("Leavitt",        "LEV-it",              ["levit", "levitt", "leavitt", "leavit", "levid", "lovett"]),
    ("Cepheid",        "SEF-ee-id",           ["sefeeid", "cepheid", "seffeeid", "sephied", "sefid"]),
    ("Cepheids",       "SEF-ee-ids",          ["sefeeids", "cepheids", "seffeeids", "sephieds", "sefids"]),
    ("Koenigsberg",    "Koenigsberg",         ["koenigsberg", "konigsberg", "kohnigsberg", "koenigsburg", "kernigsberg"]),
    ("Hipparcos",      "hip-AR-koss",         ["hiparkoss", "hipparcos", "hipparkos", "hiparkos", "hipparkus"]),
    ("Gaia",           "GUY-uh",              ["guyuh", "gaia", "guya", "gia", "gaya"]),
    ("Dorpat",         "DOR-pat",             ["dorpat", "dorpad", "doorpat", "dorpaht"]),
    ("Vega",           "VEE-guh",             ["veeguh", "vega", "veega", "veiga"]),
    ("Pleiades",       "PLY-uh-deez",         ["plyuhdeez", "pleiades", "pliadeez", "plyadees", "plyadeez"]),
    ("SH0ES",          "shoes",               ["shoes", "shoos", "shoez"]),
    ("Alpha Centauri", "AL-fuh sen-TOR-ee",   ["alfuhsentoree", "alphacentauri", "alfasentauri", "alfuhsentauri"]),
    ("Magellanic",     "maj-uh-LAN-ik",       ["majuhlanik", "magellanic", "majelanik", "majulanic"]),
    ("Planck",         "plahnk",              ["plahnk", "planck", "plank", "plonk"]),
    ("61 Cygni",       "sixty-one SIG-nye",   ["sixtyonesignye", "61cygni", "sixtyonecygni", "sixtyonesigni", "sixtyonesignii"]),
]

# Zahlen: die Ausspracheliste verlangt Ziffernpaare. Der Erkenner schreibt sie
# oft wieder als Ziffern zurueck — auch das ist ein Beleg, kein Gegenbeleg.
# Verworfen wird nur, was auf die LANGFORM hindeutet ("three thousand …").
ZAHLEN = [
    ("1543",      "fifteen forty-three",        ["1543", "fifteenfortythree"],                            ["onethousand"]),
    ("1700",      "seventeen hundred",          ["1700", "seventeenhundred"],                             ["onethousand"]),
    ("0.125",     "zero point one two five",    ["0125", "zeropointonetwofive", "0.125"],                 ["onehundred", "twentyfive"]),
    ("0.129",     "zero point one two nine",    ["0129", "zeropointonetwonine", "0.129"],                 ["onehundred", "twentynine"]),
    ("67.4",      "sixty-seven point four",     ["674", "sixtysevenpointfour", "67.4"],                   []),
    ("73.0",      "seventy-three point oh",     ["730", "seventythreepointoh", "73.0", "seventythreepointzero"], []),
    ("67.8",      "sixty-seven point eight",    ["678", "sixtysevenpointeight", "67.8"],                  []),
    ("118.000",   "a hundred and eighteen thousand", ["118000", "hundredandeighteenthousand", "118thousand"], []),
    ("759.000",   "seven hundred and fifty-nine thousand", ["759000", "sevenhundredandfiftyninethousand"], []),
    ("87.000",    "eighty-seven thousand",      ["87000", "eightyseventhousand"],                         []),
]


def blank(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def erkenne(modell: str) -> dict:
    from faster_whisper import WhisperModel
    m = WhisperModel(modell, device="cpu", compute_type="int8")
    seg, _ = m.transcribe(str(SPUR), language="en", word_timestamps=True,
                          beam_size=5, condition_on_previous_text=False)
    woerter, text = [], []
    for s in seg:
        text.append(s.text)
        for w in (s.words or []):
            woerter.append({"wort": w.word.strip(), "von": round(w.start, 2),
                            "bis": round(w.end, 2)})
    return {"text": " ".join(text).strip(), "woerter": woerter}


def richte_aus(soll: list[str], ist: list[str]) -> list[list[int]]:
    """Levenshtein mit Rueckverfolgung. Gibt je Sollwort die zugeordneten
    Ist-Indizes zurueck (leer, wenn das Wort ueberhoert wurde).

    Die Ersetzungskosten sind abgestuft, nicht binaer. Grund: der Solltext
    traegt die Umschreibungen ("neb-yoo-kad-Nezzer"), der Erkenner schreibt die
    Normalform ("Nebuchadnezzar"). Bei binaeren Kosten ist so ein Paar genauso
    teuer wie zwei voellig fremde Woerter, und die Ausrichtung verschiebt sich
    dann um eine Stelle — genau daran ist der Name zuerst als "ueberhoert"
    gemeldet worden, obwohl beide Erkenner ihn sauber geschrieben hatten.
    Gleicher Wortanfang senkt die Kosten und haelt solche Paare zusammen.
    """
    n, m = len(soll), len(ist)
    kopf_s = [w[:3] for w in soll]
    kopf_i = [w[:3] for w in ist]
    d = np.zeros((n + 1, m + 1), dtype=np.float32)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        si, ki = soll[i - 1], kopf_s[i - 1]
        for j in range(1, m + 1):
            if si == ist[j - 1]:
                k = 0.0
            elif ki and ki == kopf_i[j - 1]:
                k = 0.35
            else:
                k = 1.0
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + k)
    zu = [[] for _ in range(n)]
    i, j = n, m
    while i > 0 and j > 0:
        if soll[i - 1] == ist[j - 1]:
            k = 0.0
        elif kopf_s[i - 1] and kopf_s[i - 1] == kopf_i[j - 1]:
            k = 0.35
        else:
            k = 1.0
        if abs(float(d[i, j]) - float(d[i - 1, j - 1] + k)) < 1e-4:
            zu[i - 1].append(j - 1)
            i, j = i - 1, j - 1
        elif d[i, j] == d[i - 1, j] + 1:
            i -= 1
        else:
            zu[i - 1 if i else 0].append(j - 1)
            j -= 1
    for z in zu:
        z.reverse()
    return zu


def stelle(soll_w: list[str], zu: list[list[int]], ist: list[dict],
           sollform: str) -> dict | None:
    """Sucht die Sollform im Solltext und liest die zugeordnete Erkennung ab."""
    ziel = [blank(x) for x in sollform.split()]
    n = len(ziel)
    for i in range(len(soll_w) - n + 1):
        if [blank(x) for x in soll_w[i:i + n]] == ziel:
            idx = [k for w in range(i, i + n) for k in zu[w]]
            if not idx:
                # Dem Sollwort ist direkt nichts zugeordnet. Das heisst nicht,
                # dass nichts gesprochen wurde: bei "neb-yoo-kad-Nezzer the
                # second" schreibt der Erkenner "Nebuchadnezzar II" und die
                # Ausrichtung haengt alles an "the second". Darum das Fenster
                # bis zu den naechsten zugeordneten Nachbarn aufziehen und
                # ablesen, was dazwischen steht.
                links = max((max(zu[w]) for w in range(i - 1, -1, -1) if zu[w]),
                            default=None)
                rechts = min((min(zu[w]) for w in range(i + n, len(zu)) if zu[w]),
                             default=None)
                if links is None or rechts is None or rechts - links < 2:
                    return {"gehoert": "", "umfeld": "", "von": None, "bis": None}
                a, b = links + 1, rechts - 1
                u0, u1 = max(0, a - 4), min(len(ist), b + 5)
                return {
                    "gehoert": " ".join(ist[k]["wort"] for k in range(a, b + 1)),
                    "umfeld": " ".join(ist[k]["wort"] for k in range(u0, u1)),
                    "von": ist[a]["von"], "bis": ist[b]["bis"],
                }
            a, b = min(idx), max(idx)
            u0, u1 = max(0, a - 4), min(len(ist), b + 5)
            return {
                "gehoert": " ".join(ist[k]["wort"] for k in range(a, b + 1)),
                "umfeld": " ".join(ist[k]["wort"] for k in range(u0, u1)),
                "von": ist[a]["von"], "bis": ist[b]["bis"],
            }
    return None


def urteil(gehoert: str, gut: list[str], schlecht: list[str]) -> str:
    v = blank(gehoert)
    if not v:
        return "ueberhoert"
    if any(blank(s) in v for s in schlecht if s):
        return "FEHLFORM"
    if any(blank(g) in v or v in blank(g) for g in gut):
        return "sitzt"
    return "abweichend"


def main() -> None:
    if ASR_DATEI.exists() and "--neu" not in sys.argv:
        asr = json.loads(ASR_DATEI.read_text(encoding="utf-8"))
        print(f"Erkennung aus {ASR_DATEI.name} uebernommen "
              f"({', '.join(asr)})")
    else:
        asr = {}
        for m in ["small", "medium"]:
            print(f"Erkenner {m} laeuft …", flush=True)
            asr[m] = erkenne(m)
        ASR_DATEI.write_text(json.dumps(asr, indent=1, ensure_ascii=False),
                             encoding="utf-8")

    soll_roh = (HIER / "sprechtext.txt").read_text(encoding="utf-8").split()
    soll_b = [blank(w) for w in soll_roh]

    ausricht = {}
    for m in asr:
        ist_b = [blank(w["wort"]) for w in asr[m]["woerter"]]
        ausricht[m] = richte_aus(soll_b, ist_b)
        treffer = sum(1 for i, z in enumerate(ausricht[m])
                      if z and soll_b[i] in [ist_b[k] for k in z])
        print(f"  {m}: {len(asr[m]['woerter'])} Woerter erkannt, "
              f"{treffer}/{len(soll_b)} deckungsgleich "
              f"({treffer/len(soll_b)*100:.1f} %)")

    zeilen = []
    kopf = f"\n{'Name':16s} {'small':11s} {'medium':11s} {'Zeit':>7s}  gehoert"
    print(kopf)
    print("-" * 86)
    for anzeige, sollform, gut in NAMEN:
        e = {"name": anzeige, "sollform": sollform}
        zeit, geh = None, ""
        for m in asr:
            s = stelle(soll_roh, ausricht[m], asr[m]["woerter"], sollform)
            if s is None:
                e[m] = "Sollform nicht im Text"
                continue
            e[m] = urteil(s["gehoert"], gut, [])
            e[f"gehoert_{m}"] = s["gehoert"]
            if m == "medium" or not geh:
                geh, zeit = s["gehoert"], s["von"]
        t = f"{zeit:7.1f}" if zeit is not None else "      -"
        print(f"{anzeige:16s} {e.get('small','-'):11s} {e.get('medium','-'):11s} {t}  {geh[:34]}")
        zeilen.append(e)

    print(f"\n{'Zahl':16s} {'small':11s} {'medium':11s} {'Zeit':>7s}  gehoert")
    print("-" * 86)
    for anzeige, sollform, gut, schlecht in ZAHLEN:
        e = {"name": anzeige, "sollform": sollform}
        zeit, geh = None, ""
        for m in asr:
            s = stelle(soll_roh, ausricht[m], asr[m]["woerter"], sollform)
            if s is None:
                e[m] = "Sollform nicht im Text"
                continue
            e[m] = urteil(s["gehoert"], gut, schlecht)
            e[f"gehoert_{m}"] = s["gehoert"]
            if m == "medium" or not geh:
                geh, zeit = s["gehoert"], s["von"]
        t = f"{zeit:7.1f}" if zeit is not None else "      -"
        print(f"{anzeige:16s} {e.get('small','-'):11s} {e.get('medium','-'):11s} {t}  {geh[:34]}")
        zeilen.append(e)

    (HIER / "ton" / "_aussprache_qa.json").write_text(
        json.dumps(zeilen, indent=1, ensure_ascii=False), encoding="utf-8")

    def hat(z, w):
        return w in (z.get("small", ""), z.get("medium", ""))
    fehl = [z for z in zeilen if hat(z, "FEHLFORM")]
    abw = [z for z in zeilen if hat(z, "abweichend") and not hat(z, "FEHLFORM")]
    ueb = [z for z in zeilen if hat(z, "ueberhoert")]
    print(f"\n{len(zeilen)} Stellen · Fehlform {len(fehl)} · "
          f"abweichend {len(abw)} · ueberhoert {len(ueb)}")
    for z in fehl + abw + ueb:
        print(f"  {z['name']:16s} soll {z['sollform']!r}")
        for m in ("small", "medium"):
            if f"gehoert_{m}" in z:
                print(f"      {m:7s} {z[m]:11s} -> {z[f'gehoert_{m}']!r}")


if __name__ == "__main__":
    main()
