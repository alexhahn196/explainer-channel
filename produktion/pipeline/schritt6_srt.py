#!/usr/bin/env python3
"""
Schritt 6 - Untertitelspur.

Formel §7: **0 von 19 Gewinner-Videos hat eine SRT.** Eine echte, unbesetzte
Luecke. Wirkung ungeprueft, Kosten nahe null - der Text liegt aus Schritt 1
ohnehin vor.

Die WOERTER kommen aus dem Skript, nur die ZEITEN aus der Spracherkennung.
Damit steht im Untertitel garantiert der gelesene Bibeltext und nicht das,
was ein ASR-Modell verstanden hat. Erkannt wird chunkweise: jeder Chunk hat
einen bekannten Startpunkt in der Gesamtspur, deshalb kann sich ueber
3,5 Stunden kein Versatz aufbauen.

Aufruf:
    python3 produktion/pipeline/schritt6_srt.py V1
    python3 produktion/pipeline/schritt6_srt.py V1 --modell tiny.en --prozesse 3
"""
import argparse
import difflib
import json
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import arbeit, config, hms, ordner  # noqa: E402

MAX_ZEICHEN = 84          # zwei Zeilen a 42
MAX_DAUER = 6.5
MIN_DAUER = 0.9
_MODELL = {}


def normal(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def _asr(args):
    """Wort-Zeitstempel eines Chunks. Laeuft im eigenen Prozess."""
    pfad, modellname, threads = args
    from faster_whisper import WhisperModel
    if modellname not in _MODELL:
        _MODELL[modellname] = WhisperModel(modellname, device="cpu",
                                           compute_type="int8", cpu_threads=threads)
    segs, _ = _MODELL[modellname].transcribe(pfad, word_timestamps=True, beam_size=1)
    return [(w.word.strip(), float(w.start), float(w.end))
            for s in segs for w in (s.words or [])]


def zuordnen(skript_woerter, asr_woerter):
    """Skriptwoerter auf ASR-Zeiten legen; Luecken linear interpolieren."""
    a = [normal(w) for w in skript_woerter]
    b = [normal(w) for w, _, _ in asr_woerter]
    zeiten = [None] * len(a)
    for i, j, n in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks():
        for k in range(n):
            zeiten[i + k] = (asr_woerter[j + k][1], asr_woerter[j + k][2])

    bekannt = [i for i, z in enumerate(zeiten) if z]
    if not bekannt:
        return None, 0.0
    # Raender fortschreiben, Luecken gleichmaessig fuellen
    for i in range(bekannt[0]):
        zeiten[i] = (zeiten[bekannt[0]][0], zeiten[bekannt[0]][0])
    for i in range(bekannt[-1] + 1, len(a)):
        zeiten[i] = (zeiten[bekannt[-1]][1], zeiten[bekannt[-1]][1])
    for links, rechts in zip(bekannt, bekannt[1:]):
        if rechts - links <= 1:
            continue
        t0, t1 = zeiten[links][1], zeiten[rechts][0]
        for k in range(links + 1, rechts):
            f0 = (k - links - 1) / (rechts - links - 1)
            f1 = (k - links) / (rechts - links - 1)
            zeiten[k] = (t0 + (t1 - t0) * f0, t0 + (t1 - t0) * f1)
    return zeiten, len(bekannt) / len(a)


def zeilenumbruch(text, breite=42):
    worte, zeilen, akt = text.split(), [], ""
    for w in worte:
        if akt and len(akt) + 1 + len(w) > breite:
            zeilen.append(akt)
            akt = w
        else:
            akt = f"{akt} {w}".strip()
    if akt:
        zeilen.append(akt)
    if len(zeilen) > 2:                       # notfalls mittig zweiteilen
        m = len(worte) // 2
        zeilen = [" ".join(worte[:m]), " ".join(worte[m:])]
    return "\n".join(zeilen)


def zeit(s):
    """SRT-Zeitstempel. Erst auf ganze Millisekunden runden, dann zerlegen.

    Andersherum - Sekunden zerlegen und den Rest einzeln runden - entsteht
    bei .9996 der Wert "40,1000": vier Stellen, und YouTube weist die Datei
    ab. Der Uebertrag muss in die Sekunde laufen.
    """
    ms = int(round(max(0.0, s) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    sek, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sek:02d},{ms:03d}"


def kacheln(woerter, zeiten):
    """Woerter zu Untertitelkacheln gruppieren - Satzende hat Vorrang."""
    kacheln, akt, von = [], [], None
    for i, w in enumerate(woerter):
        if not akt:
            von = zeiten[i][0]
        akt.append(w)
        txt = " ".join(akt)
        satzende = bool(re.search(r'[.!?][”"’]?$', w))
        zu_lang = len(txt) >= MAX_ZEICHEN
        zu_spaet = zeiten[i][1] - von >= MAX_DAUER
        letztes = i == len(woerter) - 1
        if satzende or zu_lang or zu_spaet or letztes:
            kacheln.append([von, zeiten[i][1], txt])
            akt = []
    return kacheln


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--modell", default="base.en")
    ap.add_argument("--prozesse", type=int, default=3)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--neu-erkennen", action="store_true",
                    dest="neu_erkennen", help="Erkennung nicht aus dem Cache nehmen")
    a = ap.parse_args()
    cfg = config()
    t0 = time.time()

    d = json.load(open(arbeit(a.video, "chunks.json"), encoding="utf-8"))
    vorlauf = float(cfg["vorlauf_s"])
    ordn = arbeit(a.video, "chunks", "x")[:-1]
    pfade = [(os.path.join(ordn, f"{c['i']:04d}.wav"), a.modell, a.threads)
             for c in d["chunks"]]

    # Die Erkennung ist der teuerste Schritt der ganzen Pipeline (3,5 h Audio).
    # Sie wird deshalb einmal gespeichert und danach wiederverwendet, damit
    # eine Änderung an der Kachelbildung nicht zehn Minuten kostet.
    cache = arbeit(a.video, "asr.json")
    if os.path.exists(cache) and not a.neu_erkennen:
        erkannt = json.load(open(cache, encoding="utf-8"))
        if len(erkannt) == len(pfade):
            print(f"  Erkennung aus {os.path.basename(cache)} übernommen "
                  f"({len(erkannt)} Chunks).", flush=True)
        else:
            erkannt = None
    else:
        erkannt = None

    if erkannt is None:
        print(f"  Spracherkennung über {len(pfade)} Chunks "
              f"({a.modell}, {a.prozesse}×{a.threads} Threads)…", flush=True)
        erkannt = [None] * len(pfade)
        with ProcessPoolExecutor(max_workers=a.prozesse) as ex:
            for n, (i, r) in enumerate(zip(range(len(pfade)), ex.map(_asr, pfade)), 1):
                erkannt[i] = r
                if n % 15 == 0 or n == len(pfade):
                    print(f"    {n}/{len(pfade)}  ({time.time()-t0:.0f}s)", flush=True)
        json.dump([[[w, round(s, 3), round(e, 3)] for w, s, e in r] for r in erkannt],
                  open(cache, "w"), ensure_ascii=False)

    alle, quoten, wortmarken = [], [], []
    for c, asr in zip(d["chunks"], erkannt):
        woerter = c["text"].split()
        # Zugeordnet wird gegen den TTS-Text (der wurde gesprochen),
        # angezeigt wird der WEBBE-Wortlaut mit "LORD".
        anzeige = c.get("anzeige", c["text"]).split()
        if len(anzeige) != len(woerter):
            anzeige = woerter
        zeiten, quote = zuordnen(woerter, asr)
        quoten.append(quote)
        if zeiten is None:
            print(f"    Chunk {c['i']}: keine Zuordnung möglich — übersprungen")
            continue
        basis = vorlauf + c["start_s"]
        # Zeichenposition jedes Wortes im Gesamttext festhalten - daraus
        # entstehen spaeter die Kapitelmarken, ohne zweite Erkennung.
        cursor = c["von_zeichen"]
        for w, z in zip(woerter, zeiten):
            wortmarken.append([cursor, round(basis + z[0], 3)])
            cursor += len(w) + 1
        for k in kacheln(anzeige, zeiten):
            alle.append([basis + k[0], basis + k[1], k[2]])

    # Kapitelmarken: erste Wortzeit ab dem Beginn jeder Kapitelansage
    skript = json.load(open(arbeit(a.video, "skript.json"), encoding="utf-8"))
    offsets = {s[0]: s[1] for s in d["segment_offsets"]}
    wortmarken.sort()
    starts = [m[0] for m in wortmarken]
    import bisect
    marken = [{"zeit_s": 0.0, "titel": "Opening prayer"}]
    for kap in skript["kapitel"]:
        o = offsets[kap["von_segment"]]
        i = bisect.bisect_left(starts, o)
        if i < len(wortmarken):
            ref = kap["ref"].split()
            titel = (f"Psalm {ref[-1]}" if ref[0] == "psalms"
                     else " ".join(w.capitalize() for w in ref[:-1]) + f" {ref[-1]}")
            marken.append({"zeit_s": wortmarken[i][1], "titel": titel})
    json.dump(marken, open(arbeit(a.video, "kapitelmarken.json"), "w"),
              ensure_ascii=False, indent=1)

    # Ueberlappungen aufloesen. Eine kurze Kachel ist unkritisch, eine
    # ueberlappende nicht: YouTube zeigt dann zwei Kacheln gleichzeitig.
    # Die Trennung hat deshalb Vorrang vor der Mindestdauer.
    # Ein Vorwaertslauf statt paarweiser Korrektur: wo die Erkennung eine
    # Strecke ausgelassen hat, fallen mehrere interpolierte Startzeiten auf
    # denselben Moment: jede paarweise Regel laesst dort eine Ueberlappung
    # stehen. Der Vorwaertslauf schiebt stattdessen die Folgekachel.
    ABSTAND, KURZ = 0.04, 0.30
    alle.sort(key=lambda x: (x[0], x[1]))
    for i in range(len(alle)):
        if i > 0:
            alle[i][0] = max(alle[i][0], alle[i - 1][1] + ABSTAND)
        ziel = max(MIN_DAUER if i + 1 >= len(alle) else
                   min(MIN_DAUER, max(KURZ, alle[i + 1][0] - ABSTAND - alle[i][0])), KURZ)
        alle[i][1] = max(alle[i][1], alle[i][0] + ziel)
        if i + 1 < len(alle) and alle[i][1] > alle[i + 1][0] - ABSTAND:
            alle[i][1] = max(alle[i][0] + KURZ, alle[i + 1][0] - ABSTAND)

    ziel = os.path.join(ordner(a.video), f"video-{int(a.video[1:]):02d}.srt")
    with open(ziel, "w", encoding="utf-8") as f:
        for n, (von, bis, txt) in enumerate(alle, 1):
            f.write(f"{n}\n{zeit(von)} --> {zeit(bis)}\n{zeilenumbruch(txt)}\n\n")

    gesamt = json.load(open(arbeit(a.video, "qa_mix.json"), encoding="utf-8"))["dauer_s"]
    abdeckung = sum(b - v for v, b, _ in alle) / gesamt * 100
    laengen = [len(t.replace("\n", " ")) for _, _, t in alle]
    dauern = [b - v for v, b, _ in alle]
    b = {
        "kacheln": len(alle),
        "modell": a.modell,
        "zuordnungsquote_median": round(float(np.median(quoten)), 4),
        "zuordnungsquote_min": round(float(np.min(quoten)), 4),
        "abdeckung_pct": round(abdeckung, 1),
        "zeichen_median": int(np.median(laengen)),
        "zeichen_max": int(np.max(laengen)),
        "dauer_median_s": round(float(np.median(dauern)), 2),
        "dauer_max_s": round(float(np.max(dauern)), 2),
        "dauer_min_s": round(float(np.min(dauern)), 2),
        "erste_kachel_s": round(alle[0][0], 2),
        "letzte_kachel_ende_s": round(alle[-1][1], 2),
        "ueberlappungen": sum(1 for i in range(len(alle) - 1) if alle[i][1] > alle[i + 1][0]),
        "zeilen_ueber_2": sum(1 for _, _, t in alle if zeilenumbruch(t).count("\n") > 1),
        "rechenzeit_s": round(time.time() - t0, 1),
    }
    json.dump(b, open(arbeit(a.video, "qa_srt.json"), "w"), ensure_ascii=False, indent=1)

    print(f"\nUNTERTITEL {a.video}")
    print(f"  Kacheln               {b['kacheln']:,}".replace(",", "."))
    print(f"  Zuordnung Skript↔ASR  Median {b['zuordnungsquote_median']*100:.1f} %, "
          f"schlechtester Chunk {b['zuordnungsquote_min']*100:.1f} %")
    print(f"  Textlänge             Median {b['zeichen_median']}, Max {b['zeichen_max']} Zeichen")
    print(f"  Kacheldauer           Median {b['dauer_median_s']} s, "
          f"{b['dauer_min_s']}–{b['dauer_max_s']} s")
    print(f"  erste Kachel bei      {b['erste_kachel_s']} s "
          f"(Formel §3: Sprache in Sekunde 0–{cfg['sprachstart_max_s']})")
    print(f"  Überlappungen         {b['ueberlappungen']} · Kacheln über 2 Zeilen "
          f"{b['zeilen_ueber_2']}")
    print(f"  Abdeckung der Laufzeit {b['abdeckung_pct']} % "
          f"(so ist der Konkurrenz-Sprachanteil gemessen)")
    print(f"  Rechenzeit            {b['rechenzeit_s']} s")
    print(f"  geschrieben: {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
