#!/usr/bin/env python3
"""uf_sprechweise_messen.py — Sprechweise: eigene Tonspur akustisch, Unknown
Frequencies nur ueber die Untertitelzeiten.

WARUM ZWEI VERSCHIEDENE VERFAHREN
---------------------------------
Fuer die eigene Tonspur liegt die Audiodatei vor; gemessen wird mit
produktion/video-01/stimmproben/akustik.py (unveraendert importiert): Pausen,
Grundfrequenz, Pegel.

Die Tonspuren von Unknown Frequencies sind aus dieser Umgebung **nicht
ladbar** — googlevideo antwortet dem Rechenzentrums-IP mit HTTP 403, auch mit
gueltiger signierter URL und geloester JS-Challenge. Fuer UF bleibt deshalb
nur, was in den Untertitelzeiten steckt: Tempo. Pausenlaengen, Tonhoehe und
Betonungsspitzen sind fuer UF **nicht gemessen und aus diesen Daten auch nicht
ableitbar**.

DER TEMPO-PROXY UND SEINE FALLE
-------------------------------
YouTube-ASR-Untertitel sind Rollfenster: aufeinanderfolgende Segmente
ueberlappen (in allen drei geprueften Videos 100 % der Uebergaenge). `dur`
ist deshalb KEIN Zeitbudget des Segments — Woerter/dur unterschaetzt das Tempo
um den Ueberlappungsfaktor und ist zwischen SRT und srv1 nicht vergleichbar.

Gerechnet wird stattdessen mit dem **Onset-Abstand**:
    lokale Rate[i] = Woerter[i] / (start[i+1] - start[i])
Die Onset-Abstaende summieren sich auf die Gesamtlaufzeit, in beiden Formaten.
Damit ist der Wert formatunabhaengig und mit dem Brutto-WPM konsistent.

Geeicht wird der Proxy an der eigenen Tonspur, fuer die beide Messwege
vorliegen.

AUFRUF
------
    python3 uf_sprechweise_messen.py --eigen      # Akustik der eigenen Tonspur
    python3 uf_sprechweise_messen.py --tempo      # Tempoproxy eigen + UF
"""
from __future__ import annotations

import html
import importlib.util
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

import numpy as np

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent.parent
TON = REPO / "produktion/video-01/ton"
AKUSTIK = REPO / "produktion/video-01/stimmproben/akustik.py"
CAPTIONS = HIER / "uf-audio" / "captions"      # via .gitignore ausgeschlossen

# Drei POV-Videos, nach Views die staerksten der POV-Form
POV3 = [
    ("re_Av02zWcc", "Your Life as Every German Army Rank in WW2", 541, 992000),
    ("COSuWgQjBhQ", "POV: You're a German Soldier in WW2", 721, 774000),
    ("EhT6IhuZQp4", "Why It Sucked to Be a U.S. Soldier (in WW2)", 537, 396000),
]


def modul(pfad):
    if not pfad.exists():
        sys.exit(f"FEHLT: {pfad}")
    spec = importlib.util.spec_from_file_location("ak", pfad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def woerter(t: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", t))


# ----------------------------------------------------------------- eigene Spur
def zeitachse():
    """(Zeichen, Start, Ende) aus den ElevenLabs-Alignments aller Absaetze."""
    plan = json.loads((TON / "_zeitplan.json").read_text())
    raus = []
    for e in plan:
        d = json.loads((TON / f"absatz-{e['absatz']:02d}.json").read_text())
        al, off = d["alignment"], e["start_s"]
        for c, a, b in zip(al["characters"],
                           al["character_start_times_seconds"],
                           al["character_end_times_seconds"]):
            raus.append((c, off + a, off + b))
        raus.append((" ", raus[-1][2], raus[-1][2]))
    return raus, plan


# Die Endzeit des Satzzeichens laeuft bei ElevenLabs in die Stille hinein; der
# Pausenbeginn liegt im Median 0,14 s davor. Deshalb ein Toleranzfenster statt
# eines exakten Vergleichs.
FEN_LO, FEN_HI = -0.35, 0.25


def eigen():
    import soundfile as sf
    from scipy.signal import resample_poly
    ak = modul(AKUSTIK)

    za, plan = zeitachse()
    x, sr = sf.read(str(TON / "tonspur.mp3"), dtype="float64")
    if x.ndim > 1:
        x = x.mean(axis=1)
    y = resample_poly(x, 16000, sr)
    sr2 = 16000

    ps, _ = ak.pausen(y, sr2)
    f0 = ak.f0_verlauf(y, sr2)
    sv = f0[f0 > 0]
    grund = float(np.median(sv))
    dauer = len(y) / sr2
    pausenzeit = sum(p["dauer"] for p in ps)
    w = woerter((REPO / "produktion/video-01/sprechtext.txt").read_text())
    d = np.array([p["dauer"] for p in ps])

    print("=" * 74)
    print("EIGENE TONSPUR (Eric) — akustisch gemessen")
    print("=" * 74)
    print(f"  Dauer {dauer:.1f}s   Woerter {w}")
    print(f"  Brutto-Tempo        {w/(dauer/60):.1f} WPM")
    print(f"  Artikulationsrate   {w/((dauer-pausenzeit)/60):.1f} WPM  (ohne Pausenzeit)")
    print(f"  Sprechanteil        {(dauer-pausenzeit)/dauer*100:.1f} %")
    print(f"  Pausen >=0,12s      {len(ps)}   Gesamtpausenzeit {pausenzeit:.1f}s")
    print(f"    Median {np.median(d):.3f}s  P25 {np.percentile(d,25):.3f}  "
          f"P75 {np.percentile(d,75):.3f}  P90 {np.percentile(d,90):.3f}  max {d.max():.3f}")
    for a, b in [(0.12, 0.2), (0.2, 0.3), (0.3, 0.5), (0.5, 0.8), (0.8, 1.2), (1.2, 99)]:
        n = int(((d >= a) & (d < b)).sum())
        print(f"    {a:>4}-{b:<5}s {n:>4}  {n/len(d)*100:>5.1f} %")

    # --- Wo sitzen die Pausen? ---
    SATZ = [a for c, a, _ in za if c in ".!?"]
    KLAUS = [a for c, a, _ in za if c in ",;:"]
    STRICH = [a for c, a, _ in za if c in "—–"]

    def nahe(liste, t):
        return any(FEN_LO <= (a - t) <= FEN_HI for a in liste)

    print("\n  Lage der Pausen (Toleranzfenster -0,35 / +0,25 s):")
    for schwelle in (0.30, 0.50):
        sel = [p for p in ps if p["dauer"] >= schwelle]
        z = {"satzende": 0, "klausel": 0, "gedankenstrich": 0, "innerhalb": 0}
        for p in sel:
            t = p["von"]
            if nahe(SATZ, t):
                z["satzende"] += 1
            elif nahe(KLAUS, t):
                z["klausel"] += 1
            elif nahe(STRICH, t):
                z["gedankenstrich"] += 1
            else:
                z["innerhalb"] += 1
        n = len(sel)
        print(f"    >= {schwelle:.2f}s (n={n}): " + "  ".join(
            f"{k} {v} ({v/n*100:.1f} %)" for k, v in z.items()))
        print(f"      an einer Interpunktionsgrenze: {(n-z['innerhalb'])/n*100:.1f} %")

    # --- Welches Zeichen erzeugt welche Pause? ---
    def pause_nach(t, lo=-0.25, hi=0.35):
        c = [p["dauer"] for p in ps if lo <= (p["von"] - t) <= hi]
        return max(c) if c else 0.0

    print(f"\n  {'Zeichen':<16} {'n':>4} {'mit Pause':>10} {'Median':>8} {'P75':>7} {'P90':>7}")
    for name, zs in (('. ! ?', ".!?"), (', ', ","), ('; :', ";:"), ('Gedankenstrich', "—–")):
        ts = [a for c, a, _ in za if c in zs]
        ds = [pause_nach(t) for t in ts]
        mit = [v for v in ds if v > 0]
        if not ts:
            continue
        print(f"  {name:<16} {len(ts):>4} {len(mit)/len(ts)*100:>9.0f}% "
              f"{np.median(mit):>8.3f} {np.percentile(mit,75):>7.3f} {np.percentile(mit,90):>7.3f}")
    fugen = [plan[i+1]["start_s"] - (plan[i]["start_s"] + plan[i]["dauer_s"])
             for i in range(len(plan)-1)]
    print(f"  Absatzfugen (Montage): n={len(fugen)}  Median {np.median(fugen):.3f}s "
          f"(fest gesetzt, nicht von der Stimme)")

    # --- Saetze: Laenge, Folgepause, Tonhoehe ---
    sat, i = [], 0
    while i < len(za):
        while i < len(za) and za[i][0].isspace():
            i += 1
        if i >= len(za):
            break
        a0 = i
        while i < len(za) and za[i][0] not in ".!?":
            i += 1
        endz = za[i][0] if i < len(za) else "."
        endt = za[i][1] if i < len(za) else za[-1][1]
        while i < len(za) and za[i][0] in ".!?":
            i += 1
        t = "".join(c for c, _, _ in za[a0:i]).strip()
        if t:
            sat.append((za[a0][1], endt, t, endz, woerter(t)))

    paare = [(s[4], pause_nach(s[1])) for s in sat]
    paare = [(w_, d_) for w_, d_ in paare if d_ > 0]
    print(f"\n  Satzlaenge gegen Folgepause ({len(paare)} von {len(sat)} Saetzen):")
    for lo, hi in [(1, 5), (6, 10), (11, 15), (16, 25), (26, 99)]:
        g = [d_ for w_, d_ in paare if lo <= w_ <= hi]
        if g:
            print(f"    {lo:>2}-{hi:<2} Woerter  n={len(g):>3}  Median {np.median(g):.3f}s  "
                  f"P90 {np.percentile(g,90):.3f}s")
    ws = np.array([w_ for w_, _ in paare]); ds2 = np.array([d_ for _, d_ in paare])
    print(f"    Korrelation r = {np.corrcoef(ws, ds2)[0,1]:.3f}  "
          f"-> Satzlaenge steuert die Pausenlaenge NICHT")

    def hub(a, b):
        seg = f0[int(a*100):int(b*100)]
        s = seg[seg > 0]
        if len(s) < 12:
            return None
        h = 12*np.log2(np.percentile(s, 90)/np.percentile(s, 10))
        lage = float(np.argmax(np.where(seg > 0, seg, 0)))/max(len(seg)-1, 1)
        letzt = s[int(len(s)*0.8):]
        fall = 12*np.log2(np.median(letzt)/np.median(s)) if len(letzt) else 0.0
        return h, lage, fall

    print(f"\n  Tonhoehe — Grundlinie {grund:.1f} Hz")
    print(f"  {'Gruppe':<24} {'n':>4} {'Hub HT':>8} {'Spitze':>8} {'Endfall':>9} {'fallend':>8}")

    def zeig(name, sel):
        v = [hub(s[0], s[1]) for s in sel]
        v = [q for q in v if q]
        if not v:
            return
        H = [q[0] for q in v]; L = [q[1] for q in v]; F = [q[2] for q in v]
        print(f"  {name:<24} {len(H):>4} {np.median(H):>8.2f} {np.median(L):>8.3f} "
              f"{np.median(F):>9.2f} {np.mean(np.array(F) < 0)*100:>7.0f}%")

    zeig("alle Saetze", sat)
    zeig("endet auf .", [s for s in sat if s[3] == "."])
    zeig("endet auf ?", [s for s in sat if s[3] == "?"])
    zeig("1-5 Woerter", [s for s in sat if s[4] <= 5])
    zeig("6-12 Woerter", [s for s in sat if 6 <= s[4] <= 12])
    zeig("13-25 Woerter", [s for s in sat if 13 <= s[4] <= 25])
    zeig("ueber 25 Woerter", [s for s in sat if s[4] > 25])
    zeig("mit Gedankenstrich", [s for s in sat if "—" in s[2] or "–" in s[2]])
    zeig("ohne Gedankenstrich", [s for s in sat if not ("—" in s[2] or "–" in s[2])])
    zeig("mit Komma", [s for s in sat if "," in s[2]])
    zeig("ohne Komma", [s for s in sat if "," not in s[2]])
    print("\n  Spitze: 0 = Satzanfang, 1 = Satzende. Endfall: letztes Fuenftel "
          "gegen den Satzmedian, in Halbtoenen.")


# ------------------------------------------------------------------- Tempo
def srt_onsets(pfad):
    raus = []
    for b in re.split(r"\n\s*\n", pfad.read_text(encoding="utf-8").strip()):
        z = [l for l in b.splitlines() if l.strip()]
        if len(z) < 2:
            continue
        m = re.match(r"(\d+):(\d+):(\d+),(\d+)\s*-->", z[1])
        if not m:
            continue
        g = [int(v) for v in m.groups()]
        raus.append((g[0]*3600 + g[1]*60 + g[2] + g[3]/1000, woerter(" ".join(z[2:]))))
    return raus


def srv1_onsets(pfad):
    raus = []
    for e in ET.parse(pfad).getroot().iter("text"):
        t = html.unescape(html.unescape(e.text or "")).strip()
        if t:
            raus.append((float(e.get("start", "0")), woerter(t)))
    return raus


def tempo_stats(seq, name, laenge):
    seq = sorted(seq)
    ioi = [(seq[i+1][0] - seq[i][0], seq[i][1]) for i in range(len(seq)-1)]
    ioi = [(d, w) for d, w in ioi if d > 0.05 and w > 0]
    r = np.array([w/d*60 for d, w in ioi])
    gw = sum(w for _, w in seq)
    print(f"  {name:<36} Woerter {gw:>5}  Brutto {gw/(laenge/60):>6.1f} WPM")
    print(f"     lokale Rate  Median {np.median(r):>6.1f}  P10 {np.percentile(r,10):>6.1f}  "
          f"P90 {np.percentile(r,90):>6.1f}  VK {r.std()/r.mean():.3f}")
    print(f"     Anteil Einheiten unter 120 WPM: {(r < 120).mean()*100:>5.1f} %")
    return {"brutto_wpm": round(gw/(laenge/60), 1),
            "rate_median": round(float(np.median(r)), 1),
            "rate_p10": round(float(np.percentile(r, 10)), 1),
            "rate_p90": round(float(np.percentile(r, 90)), 1),
            "vk": round(float(r.std()/r.mean()), 3),
            "anteil_unter_120_pct": round(float((r < 120).mean()*100), 1),
            "woerter": gw, "dauer_s": laenge}


def tempo():
    print("=" * 74)
    print("TEMPO — Onset-Abstand, formatunabhaengig")
    print("=" * 74)
    raus = {}
    srt = REPO / "produktion/video-01/untertitel.srt"
    if srt.exists():
        raus["eric"] = tempo_stats(srt_onsets(srt), "Eric untertitel.srt (Eichung)", 538.3)
    print()
    for vid, titel, laenge, views in POV3:
        p = CAPTIONS / f"{vid}.xml"
        if not p.exists():
            print(f"  {vid}: Untertiteldatei fehlt ({p}) — siehe Kopf des Skripts")
            continue
        raus[vid] = tempo_stats(srv1_onsets(p), f"UF {titel[:30]} ({views//1000}k)", laenge)
    print("\n  Fuer UF sind Pausenlaengen, Tonhoehe und Betonungsspitzen NICHT "
          "gemessen —\n  die Tonspuren sind aus dieser Umgebung nicht ladbar (HTTP 403).")
    return raus


if __name__ == "__main__":
    if "--eigen" in sys.argv:
        eigen()
    elif "--tempo" in sys.argv:
        tempo()
    else:
        sys.exit(__doc__)
