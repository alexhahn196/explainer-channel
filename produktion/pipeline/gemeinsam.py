#!/usr/bin/env python3
"""
gemeinsam.py - Konfiguration und Audio-Hilfen fuer alle Pipeline-Schritte.

Die Konfiguration kommt aus produktion/config.md. Bewusst aus einer
Markdown-Datei und nicht aus einer .py oder .json: die Werte sollen
lesbar und kommentiert an genau einer Stelle stehen. Der ini-Block darin
ist maschinenlesbar.
"""
import os
import re
import subprocess

import numpy as np

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG = os.path.join(WURZEL, "produktion", "config.md")
SR = 44100


def _wandeln(v):
    if v in ("ja", "true", "yes"):
        return True
    if v in ("nein", "false", "no"):
        return False
    try:
        return int(v)
    except ValueError:
        pass
    try:
        return float(v)
    except ValueError:
        return v


def config(pfad=CONFIG):
    """Liest den ```ini-Block aus config.md."""
    txt = open(pfad, encoding="utf-8").read()
    bloecke = re.findall(r"```ini\n(.*?)```", txt, re.S)
    if not bloecke:
        raise SystemExit(f"{pfad}: kein ```ini-Block gefunden")
    cfg = {}
    for zeile in "\n".join(bloecke).splitlines():
        zeile = zeile.split("#", 1)[0].strip()
        if not zeile or "=" not in zeile:
            continue
        k, v = zeile.split("=", 1)
        cfg[k.strip()] = _wandeln(v.strip())
    pflicht = ["stimme_id", "tts_modell", "prosody_speed", "pegel_stimme_dbfs",
               "pegel_bett_dbfs", "bett_datei", "fps", "breite", "hoehe"]
    fehlt = [k for k in pflicht if k not in cfg]
    if fehlt:
        raise SystemExit(f"{pfad}: fehlende Werte {fehlt}")
    return cfg


def pfad(*teile):
    return os.path.join(WURZEL, *teile)


def ordner(video):
    """Arbeitsordner eines Videos, z.B. produktion/video-01/."""
    p = pfad("produktion", f"video-{int(video[1:]):02d}")
    os.makedirs(p, exist_ok=True)
    return p


def arbeit(video, *teile):
    """Zwischenstaende, die nicht ins Repository gehoeren."""
    p = pfad("produktion", "arbeit", f"video-{int(video[1:]):02d}", *teile[:-1])
    os.makedirs(p, exist_ok=True)
    return os.path.join(p, teile[-1]) if teile else p


# ---------------------------------------------------------------- Audio

RAHMEN_S = 0.02          # 20-ms-Rahmen, nicht ueberlappend
SCHWELLE_FAKTOR = 0.15   # Anteil des 95. Perzentils der Huellkurve


def rms_db(x):
    x = np.asarray(x, dtype=np.float64)
    if x.size == 0:
        return -120.0
    return float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12))


def rahmen(x, sr, rahmen_s=RAHMEN_S):
    """Mittlerer Betrag und RMS je 20-ms-Rahmen eines Signalstuecks."""
    w = max(1, int(rahmen_s * sr))
    n = (len(x) // w) * w
    if n == 0:
        return np.zeros(0, np.float32), np.zeros(0, np.float32), w
    b = x[:n].reshape(-1, w).astype(np.float32)
    return np.abs(b).mean(axis=1), np.sqrt((b ** 2).mean(axis=1)), w


def rahmen_datei(datei, rahmen_s=RAHMEN_S, block=1 << 22):
    """Rahmenweise Huellkurve einer ganzen Datei, ohne sie zu laden.

    Bei 3,4 Stunden sind das 546 Millionen Samples - eine Faltung darueber
    ist nicht rechenbar. Deshalb nicht ueberlappende Rahmen und ein
    Blockleser: der Speicherbedarf bleibt konstant, die Kosten linear.
    """
    import soundfile as sf
    env, rmsf = [], []
    with sf.SoundFile(datei) as f:
        sr = f.samplerate
        w = max(1, int(rahmen_s * sr))
        blk = (block // w) * w
        peak = 0.0
        while True:
            y = f.read(blk, dtype="float32", always_2d=True)
            if len(y) == 0:
                break
            y = y.mean(axis=1)
            peak = max(peak, float(np.abs(y).max()))
            e, r, _ = rahmen(y, sr, rahmen_s)
            env.append(e)
            rmsf.append(r)
    return (np.concatenate(env) if env else np.zeros(0, np.float32),
            np.concatenate(rmsf) if rmsf else np.zeros(0, np.float32),
            sr, w, peak)


def sprach_maske_env(env, faktor=SCHWELLE_FAKTOR):
    return env > (faktor * np.percentile(env, 95))


def sprach_maske(x, sr, schwelle=SCHWELLE_FAKTOR, rahmen_s=RAHMEN_S):
    """Sprachmaske auf Samplerasterebene - nur fuer kurze Stuecke."""
    e, _, w = rahmen(x, sr, rahmen_s)
    if e.size == 0:
        return np.zeros(len(x), bool)
    m = np.repeat(sprach_maske_env(e, schwelle), w)
    return np.concatenate([m, np.zeros(len(x) - len(m), bool)])


def sprach_rms_db(x, sr):
    e, r, _ = rahmen(x, sr)
    if e.size == 0:
        return rms_db(x)
    m = sprach_maske_env(e)
    if m.sum() < 5:
        return rms_db(x)
    return float(20 * np.log10(np.sqrt((r[m].astype(np.float64) ** 2).mean()) + 1e-12))


def pausen_aus_maske(m, rahmen_s, min_s=0.25):
    """Startzeit und Laenge aller Pausen ab min_s, aus einer Rahmenmaske."""
    if m.size == 0:
        return []
    d = np.diff(np.concatenate([[True], m, [True]]).astype(np.int8))
    starts = np.flatnonzero(d == -1)
    enden = np.flatnonzero(d == 1)
    lang = (enden - starts) * rahmen_s >= min_s
    return [(float(s * rahmen_s), float((e - s) * rahmen_s))
            for s, e in zip(starts[lang], enden[lang])]


def pausen(x, sr, schwelle=SCHWELLE_FAKTOR, min_s=0.25):
    e, _, _ = rahmen(x, sr)
    return pausen_aus_maske(sprach_maske_env(e, schwelle), RAHMEN_S, min_s)


def ffprobe(datei, feld="format=duration"):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", feld,
         "-of", "default=nw=1:nk=1", datei],
        capture_output=True, text=True, check=True)
    return r.stdout.strip()


def dauer_s(datei):
    return float(ffprobe(datei))


def hms(sekunden):
    s = int(round(sekunden))
    return f"{s // 3600}:{(s % 3600) // 60:02d}:{s % 60:02d}"
