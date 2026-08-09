#!/usr/bin/env python3
"""
Schritt 2 - Sprachsynthese.

Aufteilung in Chunks **ausschliesslich an Satzenden**. Ein Chunk, der mitten
im Satz endet, gibt der TTS keine Kadenz und erzeugt an der Naht einen
hoerbaren Bruch. Deshalb wird nie nach Zeichenzahl geschnitten, sondern
Saetze werden bis zur Obergrenze gepackt.

Chunks werden als **WAV** geholt und sample-exakt gefuegt; die MP3/AAC-
Kodierung passiert genau einmal am Ende (Schritt 3/5). Wuerde man
MP3-Chunks aneinanderhaengen, entstuende an jeder Naht eine Encoder-Luecke.

Der API-Schluessel kommt aus der Umgebungsvariablen FISH_KEY und wird
nirgends gespeichert.

Aufruf:
    python3 produktion/pipeline/schritt2_tts.py V1            # alles
    python3 produktion/pipeline/schritt2_tts.py V1 --nur qa
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import (SR, arbeit, config, hms,  # noqa: E402
                       pausen_aus_maske, rahmen_datei, sprach_maske_env,
                       sprach_rms_db)

SATZENDE = re.compile(r'(?<=[.!?”"’])\s+(?=[A-Z“"‘\'])')


# --------------------------------------------------------------- Chunking

def saetze_mit_offset(volltext):
    """Zerlegt in Saetze und behaelt die Zeichenposition im Volltext."""
    aus, pos = [], 0
    for teil in SATZENDE.split(volltext):
        i = volltext.index(teil, pos)
        aus.append((teil, i, i + len(teil)))
        pos = i + len(teil)
    return aus


def chunks_bauen(video, max_zeichen):
    skript = json.load(open(arbeit(video, "skript.json"), encoding="utf-8"))
    segmente = skript["segmente"]

    volltext, anzeige, seg_offsets, pos = [], [], [], 0
    for i, s in enumerate(segmente):
        t = s["text"]
        seg_offsets.append([i, pos, pos + len(t)])
        volltext.append(t)
        anzeige.append(s.get("anzeige", t))
        pos += len(t) + 1
    volltext = " ".join(volltext)
    anzeige = " ".join(anzeige)
    if len(anzeige) != len(volltext):
        raise SystemExit("Anzeigetext und TTS-Text sind unterschiedlich lang — "
                         "die Zeichenoffsets waeren nicht mehr gueltig.")

    chunks, akt, von = [], [], None
    for satz, a, b in saetze_mit_offset(volltext):
        if len(satz) > max_zeichen:
            raise SystemExit(f"Satz laenger als das Chunk-Limit ({len(satz)} Zeichen): "
                             f"{satz[:120]!r} — Limit anheben oder Satz pruefen.")
        laenge = sum(len(x) + 1 for x in akt)
        if akt and laenge + len(satz) > max_zeichen:
            chunks.append({"i": len(chunks), "text": " ".join(akt),
                           "anzeige": anzeige[von:ende],
                           "von_zeichen": von, "bis_zeichen": ende})
            akt, von = [], None
        if von is None:
            von = a
        akt.append(satz)
        ende = b
    if akt:
        chunks.append({"i": len(chunks), "text": " ".join(akt),
                       "von_zeichen": von, "bis_zeichen": ende})

    d = {"max_zeichen": max_zeichen, "volltext_zeichen": len(volltext),
         "segment_offsets": seg_offsets, "chunks": chunks}
    json.dump(d, open(arbeit(video, "chunks.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    return d


# ------------------------------------------------------------- Generierung

def _auftrag(a):
    i, text, cfg, ziel, key = a
    p = os.path.join(ziel, f"{i:04d}.wav")
    if os.path.exists(p) and os.path.getsize(p) > 2000:
        return (i, "vorhanden", 0.0)
    body = {"text": text, "reference_id": cfg["stimme_id"], "format": "wav",
            "sample_rate": SR, "normalize": True}
    if float(cfg["prosody_speed"]) != 1.0:
        body["prosody"] = {"speed": float(cfg["prosody_speed"])}
    daten = json.dumps(body).encode()
    t0 = time.time()
    for versuch in range(6):
        try:
            r = urllib.request.Request(cfg["tts_endpoint"], data=daten, headers={
                "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                "model": cfg["tts_modell"]})
            with urllib.request.urlopen(r, timeout=600) as f:
                out = f.read()
            if out[:1] == b"{":
                raise RuntimeError(out[:200].decode("utf-8", "replace"))
            if len(out) < 2000:
                raise RuntimeError(f"Antwort zu klein: {len(out)} Bytes")
            tmp = p + ".part"
            open(tmp, "wb").write(out)
            os.replace(tmp, p)
            return (i, "ok", time.time() - t0)
        except Exception as e:
            if versuch == 5:
                return (i, f"FEHLER {e}", time.time() - t0)
            time.sleep(2 ** versuch)


def generieren(video, cfg, d):
    key = os.environ.get("FISH_KEY")
    if not key:
        raise SystemExit("FISH_KEY ist nicht gesetzt.")
    ziel = arbeit(video, "chunks", "x")[:-1]
    os.makedirs(ziel, exist_ok=True)
    jobs = [(c["i"], c["text"], cfg, ziel, key) for c in d["chunks"]]
    n, fehler, t0 = 0, [], time.time()
    with ThreadPoolExecutor(max_workers=int(cfg["tts_parallel"])) as ex:
        for i, status, dauer in ex.map(_auftrag, jobs):
            n += 1
            if status.startswith("FEHLER"):
                fehler.append((i, status))
            if n % 10 == 0 or n == len(jobs) or status.startswith("FEHLER"):
                print(f"  [{n}/{len(jobs)}] Chunk {i}: {status} ({dauer:.1f}s)", flush=True)
    print(f"  Generierung: {time.time()-t0:.0f}s", flush=True)
    if fehler:
        raise SystemExit(f"{len(fehler)} Chunks fehlgeschlagen: {fehler[:5]}")
    return ziel


def fuegen(video, d, ziel, angleichen=True):
    """Sample-exakt zusammensetzen, ohne alles in den Speicher zu laden.

    Die TTS normalisiert JEDEN Chunk fuer sich (`normalize: true`). Dadurch
    driftet der Pegel von Chunk zu Chunk, und genau dieser Versatz landet
    als Sprung an der Naht. Deshalb wird vorab der Sprachpegel jedes Chunks
    gemessen und auf den Median aller Chunks gezogen. Das ist eine reine
    Faktormultiplikation - die Dynamik innerhalb eines Chunks bleibt
    unangetastet.
    """
    aus = arbeit(video, "stimme.wav")

    pegel = []
    for c in d["chunks"]:
        y, s = sf.read(os.path.join(ziel, f"{c['i']:04d}.wav"),
                       dtype="float32", always_2d=True)
        if s != SR:
            raise SystemExit(f"Chunk {c['i']} hat {s} Hz statt {SR}")
        p = sprach_rms_db(y.mean(axis=1), SR)
        c["sprach_rms_roh_db"] = round(p, 2)
        pegel.append(p)
    ziel_db = float(np.median(pegel))
    d["angleich_ziel_dbfs"] = round(ziel_db, 2)
    d["angleich_aktiv"] = bool(angleichen)

    naehte, pos = [], 0
    with sf.SoundFile(aus, "w", samplerate=SR, channels=1, subtype="PCM_16") as f:
        for c in d["chunks"]:
            y, _ = sf.read(os.path.join(ziel, f"{c['i']:04d}.wav"),
                           dtype="float32", always_2d=True)
            y = y.mean(axis=1)
            if angleichen:
                y = y * (10 ** ((ziel_db - c["sprach_rms_roh_db"]) / 20))
            if c["i"] > 0:
                naehte.append(pos / SR)
            f.write(y)
            c["dauer_s"] = round(len(y) / SR, 4)
            c["start_s"] = round(pos / SR, 4)
            c["sprach_rms_db"] = round(sprach_rms_db(y, SR), 2)
            pos += len(y)
    d["naehte_s"] = naehte
    d["dauer_stimme_s"] = pos / SR
    json.dump(d, open(arbeit(video, "chunks.json"), "w", encoding="utf-8"),
              ensure_ascii=False)
    return aus


# ------------------------------------------------------------------- QA

def naht_analyse(rmsf, maske, naehte, rahmen_s, fenster_s=2.5):
    """Pegelsprung an den Naehten gegen die natuerliche Streuung.

    Verglichen werden je ~2,5 s SPRACHE links und rechts der Naht - nicht
    die Stille davor. Wer gegen die Pause misst, bekommt zwangslaeufig einen
    grossen Sprung heraus und haelt ihn faelschlich fuer ein Artefakt.

    Als Massstab dient die Sprunghoehe an allen natuerlichen Satzgrenzen
    derselben Datei. Erst der Vergleich sagt, ob eine Naht auffaellt.
    """
    n = len(rmsf)
    w = int(fenster_s / rahmen_s)

    def sprach_db(a, b):
        a, b = max(0, a), min(n, b)
        if b <= a:
            return None
        mm = maske[a:b]
        if mm.sum() < 5:
            return None
        v = rmsf[a:b][mm].astype(np.float64)
        return float(20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-12))

    alle_pausen = pausen_aus_maske(maske, rahmen_s, min_s=0.2)
    naht_frames = np.array([int(t / rahmen_s) for t in naehte]) if naehte else np.array([])

    def sprung(i):
        links, rechts = sprach_db(i - w, i), sprach_db(i, i + w)
        return None if links is None or rechts is None else abs(rechts - links)

    spruenge, naht_pausenlaenge = [], []
    for t in naehte:
        i = int(t / rahmen_s)
        s = sprung(i)
        if s is None:
            continue
        spruenge.append(s)
        nah = [p for p in alle_pausen
               if p[0] - 0.4 <= t <= p[0] + p[1] + 0.4]
        naht_pausenlaenge.append(max((p[1] for p in nah), default=0.0))

    # Faire Referenz: nur Pausen VERGLEICHBARER LAENGE, und keine Naht.
    # Ohne diese Bedingung besteht der Vergleichspool fast nur aus kurzen
    # Pausen innerhalb eines Verses - dort ist der Inhalt links und rechts
    # naturgemaess aehnlicher als an einem Satz- oder Kapitelwechsel, und
    # jede Naht saehe faelschlich auffaellig aus.
    unten = float(np.percentile(naht_pausenlaenge, 10)) if naht_pausenlaenge else 0.4
    oben = float(np.percentile(naht_pausenlaenge, 90)) if naht_pausenlaenge else 99.0
    referenz = []
    for start, laenge in alle_pausen:
        if not (unten <= laenge <= oben):
            continue
        i = int((start + laenge / 2) / rahmen_s)
        if naht_frames.size and np.abs(naht_frames - i).min() < int(2.0 / rahmen_s):
            continue
        s = sprung(i)
        if s is not None:
            referenz.append(s)
    return spruenge, referenz, (unten, oben), naht_pausenlaenge


def qa(video, cfg):
    d = json.load(open(arbeit(video, "chunks.json"), encoding="utf-8"))
    skript = json.load(open(arbeit(video, "skript.json"), encoding="utf-8"))
    env, rmsf, sr, w, peak = rahmen_datei(arbeit(video, "stimme.wav"))
    rahmen_s = w / sr
    dauer = len(rmsf) * rahmen_s
    woerter = skript["bericht"]["woerter_gesamt"]

    maske = sprach_maske_env(env)
    sprachanteil = 100.0 * maske.mean()
    pau = pausen_aus_maske(maske, rahmen_s, min_s=0.25)
    laengste = max((p[1] for p in pau), default=0.0)
    sprach_db = float(20 * np.log10(
        np.sqrt((rmsf[maske].astype(np.float64) ** 2).mean()) + 1e-12))

    # Der Benchmark "97-100 % Sprachanteil" aus Formel §3 stammt aus
    # Untertitel-Zeitstempeln. Eine Untertitelspanne ueberdeckt die kurzen
    # Atempausen zwischen den Woertern mit. Ein Huellkurven-Schwellwert tut
    # das nicht und meldet denselben Ton systematisch zu niedrig. Damit die
    # Zahl vergleichbar ist, werden Luecken unter 1 s als Sprache gezaehlt.
    geschlossen = maske.copy()
    for start, laenge in pausen_aus_maske(maske, rahmen_s, min_s=0.0):
        if laenge < 1.0:
            geschlossen[int(start / rahmen_s):int((start + laenge) / rahmen_s)] = True
    sprachanteil_vgl = 100.0 * geschlossen.mean()

    spruenge, referenz, fenster, npl = naht_analyse(
        rmsf, maske, d["naehte_s"], rahmen_s)
    b = {
        "dauer_s": round(dauer, 1),
        "dauer_hms": hms(dauer),
        "dauer_h": round(dauer / 3600, 3),
        "woerter": woerter,
        "wpm": round(woerter / (dauer / 60), 1),
        "zeichen_tts": d["volltext_zeichen"],
        "chunks": len(d["chunks"]),
        "chunk_zeichen_min": min(len(c["text"]) for c in d["chunks"]),
        "chunk_zeichen_max": max(len(c["text"]) for c in d["chunks"]),
        "naehte": len(d["naehte_s"]),
        "naht_sprung_median_db": round(float(np.median(spruenge)), 2) if spruenge else None,
        "naht_sprung_max_db": round(float(np.max(spruenge)), 2) if spruenge else None,
        "naht_pausenlaenge_median_s": round(float(np.median(npl)), 2) if npl else None,
        "referenz_pausenfenster_s": [round(fenster[0], 2), round(fenster[1], 2)],
        "satzgrenzen_referenz_n": len(referenz),
        "satzgrenze_sprung_median_db": round(float(np.median(referenz)), 2) if referenz else None,
        "satzgrenze_sprung_p95_db": round(float(np.percentile(referenz, 95)), 2) if referenz else None,
        "chunk_pegel_sprung_median_db": round(float(np.median(np.abs(np.diff(
            [c["sprach_rms_db"] for c in d["chunks"]])))), 2)
            if "sprach_rms_db" in d["chunks"][0] else None,
        "chunk_pegel_sprung_max_db": round(float(np.max(np.abs(np.diff(
            [c["sprach_rms_db"] for c in d["chunks"]])))), 2)
            if "sprach_rms_db" in d["chunks"][0] else None,
        "sprachanteil_pct": round(sprachanteil, 1),
        "sprachanteil_vergleichbar_pct": round(sprachanteil_vgl, 1),
        "pausen_ab_025s": len(pau),
        "laengste_pause_s": round(laengste, 2),
        "sprach_rms_db": round(sprach_db, 2),
        "peak_dbfs": round(float(20 * np.log10(peak + 1e-12)), 2),
    }
    # Auffaellig ist eine Naht dann, wenn ihr TYPISCHER Sprung ueber dem
    # liegt, was an vergleichbaren natuerlichen Pausen ohnehin passiert.
    # Ein einzelner Ausreisser sagt nichts - deshalb Median gegen p95.
    b["naht_auffaellig"] = (
        b["naht_sprung_median_db"] is not None and b["satzgrenze_sprung_p95_db"] is not None
        and b["naht_sprung_median_db"] > b["satzgrenze_sprung_p95_db"])
    json.dump(b, open(arbeit(video, "qa_stimme.json"), "w"), indent=1)
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--nur", choices=["chunks", "gen", "fuegen", "qa"], default=None)
    a = ap.parse_args()
    cfg = config()

    if a.nur in (None, "chunks"):
        d = chunks_bauen(a.video, int(cfg["chunk_max_zeichen"]))
        print(f"  {len(d['chunks'])} Chunks, "
              f"{min(len(c['text']) for c in d['chunks'])}–"
              f"{max(len(c['text']) for c in d['chunks'])} Zeichen, alle an Satzenden")
    else:
        d = json.load(open(arbeit(a.video, "chunks.json"), encoding="utf-8"))

    ziel = arbeit(a.video, "chunks", "x")[:-1]
    if a.nur in (None, "gen"):
        ziel = generieren(a.video, cfg, d)
    if a.nur in (None, "fuegen"):
        p = fuegen(a.video, d, ziel, bool(cfg.get("chunk_pegel_angleichen", True)))
        print(f"  gefügt: {p}")
    if a.nur in (None, "qa"):
        b = qa(a.video, cfg)
        print(f"\nSTIMME {a.video}")
        print(f"  Laufzeit              {b['dauer_hms']}  ({b['dauer_h']:.2f} h)")
        print(f"  Tempo                 {b['wpm']} WPM über {b['woerter']:,} Wörter"
              .replace(",", "."))
        print(f"  Chunks                {b['chunks']} ({b['chunk_zeichen_min']}–"
              f"{b['chunk_zeichen_max']} Zeichen), {b['naehte']} Nähte")
        print(f"  Pegel Chunk zu Chunk  Median {b['chunk_pegel_sprung_median_db']} dB, "
              f"Maximum {b['chunk_pegel_sprung_max_db']} dB (systematischer Anteil)")
        print(f"  Nahtsprung 2,5-s-Fenster  Median {b['naht_sprung_median_db']} dB, "
              f"Maximum {b['naht_sprung_max_db']} dB")
        print(f"  vergleichbare Pausen  Median {b['satzgrenze_sprung_median_db']} dB, "
              f"p95 {b['satzgrenze_sprung_p95_db']} dB (n={b['satzgrenzen_referenz_n']}, "
              f"Pausenlänge {b['referenz_pausenfenster_s'][0]}–"
              f"{b['referenz_pausenfenster_s'][1]} s)")
        print(f"  → Nähte {'AUFFÄLLIG' if b['naht_auffaellig'] else 'unauffällig'}")
        print(f"  Sprachanteil roh      {b['sprachanteil_pct']} % (Hüllkurvenschwelle)")
        print(f"  Sprachanteil vergl.   {b['sprachanteil_vergleichbar_pct']} % "
              f"(Lücken <1 s zugerechnet — so ist Formel §3 gemessen, "
              f"verlangt ≥ {cfg['sprachanteil_min_pct']} %)")
        print(f"  längste Pause         {b['laengste_pause_s']} s "
              f"(Grenze {cfg['laengste_pause_max_s']} s)")
        print(f"  Sprach-RMS            {b['sprach_rms_db']} dBFS, Peak {b['peak_dbfs']} dBFS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
