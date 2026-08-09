#!/usr/bin/env python3
"""
loop_animation.py - macht aus einem Serien-Standbild einen nahtlosen
60-Sekunden-Loop.

Warum kein KI-Videoclip: Ein 3,5-Stunden-Video wiederholt einen kurzen Clip
weit über tausendmal. Jede Naht, die nicht exakt schliesst, wird zum
Dauer-Sprung - und Bewegung ist das Einzige im Bild. Deshalb sind hier ALLE
Bewegungen deterministische Funktionen der Zeit, deren Frequenzen ganzzahlige
Vielfache von 1/ZYKLUS sind: f(t + ZYKLUS) == f(t) exakt, Frame 0 und
Frame N sind bitidentisch berechenbar.

Ebenen (je nach Variante):
  - Lichtpuls     multiplikativ auf der Warmlicht-Maske, drei überlagerte
                  Sinuswellen -> unregelmässig wirkendes Atmen
  - Glut          drei räumliche Rauschfelder im Feuerkern, sinusförmig
                  überblendet
  - Funken        Partikel mit Perioden, die 60 teilen; Helligkeit
                  sin(pi*u)^1.5 -> an beiden Lebensenden null, das Wrap-Ende
                  ist unsichtbar
  - Rauch         vertikal kachelbares Rauschband, scrollt ganzzahlig oft
                  pro Zyklus, seitliches Pendeln
  - Wiegen        sinusförmige Horizontalverschiebung (cv2.remap) mit
                  ortsabhängiger Phase, Amplitude wächst zur Kronenspitze
  - Wasser        Glitzern der hellsten Speckle im Wasserrechteck mit
                  x/y-abhängiger Phase
  - Sterne        Funkeln der Sternpunkte (Hochpass-Anteil), Phase je Stern
  - Nebel         horizontal kachelbares Band, driftet 1x pro Zyklus

Alles bewusst SEHR dezent - der Zuschauer soll einschlafen. Im Zweifel weniger.

Aufruf:
    python3 produktion/pipeline/loop_animation.py V3
    python3 produktion/pipeline/loop_animation.py V1 --nur-pruefen
"""
import argparse
import json
import os
import subprocess
import sys
import time

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import pfad  # noqa: E402

ZYKLUS = 60.0
FPS = 24
N = int(ZYKLUS * FPS)
W, H = 1920, 1080
TAU = 2 * np.pi

# --------------------------------------------------------------- Varianten
# Rechtecke (x0,y0,x1,y1) im 1920x1080-Raster, nach Sichtung der Standbilder.
VARIANTEN = {
    "V1": dict(  # Fels + grosser Mond tief am Horizont
        licht="mond", puls_amp=0.018,
        sterne=True, himmel_y=520,
        funken=False, rauch=False, glut=False,
        wiegen=None, wasser=None, nebel=None,
    ),
    "V2": dict(  # Seeufer + Öllampe, Nebel überm Wasser
        licht="flamme", puls_amp=0.05,
        sterne=True, himmel_y=200,
        funken=False, rauch=False, glut=False,
        wiegen=None,
        wasser=(0, 220, 1920, 560),
        nebel=(0, 240, 1920, 430),
    ),
    "V3": dict(  # Baum + grosses Lagerfeuer
        licht="feuer", puls_amp=0.06,
        sterne=True, himmel_y=520,
        funken=True, rauch=True, glut=True,
        wiegen=dict(rechteck=(40, 0, 1560, 640), fuss_y=620, amp_px=2.2),
        wasser=None, nebel=None,
    ),
    "V4": dict(  # Wegrand + grosse Laterne
        licht="flamme", puls_amp=0.05,
        sterne=True, himmel_y=480,
        funken=False, rauch=False, glut=False,
        wiegen=dict(rechteck=(0, 760, 700, 1080), fuss_y=760, amp_px=1.0,
                    kopfueber=True),   # Gras: Amplitude wächst nach UNTEN
        wasser=None, nebel=None,
    ),
}


def _blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


# ------------------------------------------------------------ Vorbereitung

def licht_finden(base):
    """Zentrum und Ausdehnung der warmen Lichtquelle aus dem Bild selbst."""
    warm = np.clip(base[..., 0] - base[..., 2], 0, None) * (lum(base) / 255)
    warm = _blur(warm, 9)
    schwelle = np.percentile(warm, 99.5)
    ys, xs = np.nonzero(warm >= schwelle)
    cx, cy = float(xs.mean()), float(ys.mean())
    r = float(max(xs.std(), ys.std())) * 2.5 + 30
    return (cx, cy, r), warm


def glow_maske(base, warm):
    """0..1-Maske: Lichtquelle plus alles, was sie anleuchtet."""
    m = warm / (warm.max() + 1e-6)
    m = _blur(m, 25) * 2.2
    return np.clip(m, 0, 1).astype(np.float32)


def stern_karte(base, himmel_y):
    """Hochpass-Anteil der Sternpunkte plus Zufallsphase je Sternregion.

    Sterne sind KUEHLE Lichtpunkte (Blau >= Rot). Ohne diese Bedingung
    wuerden warme Blattspitzen und Glutpartikel im Himmelband mitfunkeln.
    """
    L = lum(base)
    hoch = np.clip(L - _blur(L, 5), 0, None)
    kuehl = base[..., 2] >= base[..., 0] - 6
    maske = np.zeros_like(L, bool)
    maske[:himmel_y] = (hoch[:himmel_y] > np.percentile(hoch[:himmel_y], 99.6)) \
        & kuehl[:himmel_y]
    delta = np.where(maske, hoch, 0).astype(np.float32)
    rnd = np.random.RandomState(7)
    grob = rnd.uniform(0, TAU, (18, 32)).astype(np.float32)
    phase = cv2.resize(grob, (W, H), interpolation=cv2.INTER_NEAREST)
    freq = 2 + (cv2.resize(rnd.uniform(0, 4, (18, 32)).astype(np.float32),
                           (W, H), interpolation=cv2.INTER_NEAREST)).astype(np.int32)
    return delta, phase, freq.astype(np.float32)


def rausch_felder(form, saat, n=3, sigma=10):
    rnd = np.random.RandomState(saat)
    aus = []
    for i in range(n):
        f = rnd.randn(*form).astype(np.float32)
        f = _blur(f, sigma)
        f /= (np.abs(f).max() + 1e-6)
        aus.append(f)
    return aus


def kachelbares_rauschen(h, w, saat, sigma=14, vertikal=True):
    """Rauschen, das in einer Achse exakt kachelt (fuer Rauch/Nebel-Scroll)."""
    rnd = np.random.RandomState(saat)
    f = rnd.randn(h, w).astype(np.float32)
    # 3-fach stapeln, blurren, Mitte nehmen -> nahtlose Kachel
    if vertikal:
        g = _blur(np.tile(f, (3, 1)), sigma)[h:2 * h]
    else:
        g = _blur(np.tile(f, (1, 3)), sigma)[:, w:2 * w]
    g -= g.min()
    g /= (g.max() + 1e-6)
    return g


def funken_bauen(cx, cy, saat=11, anzahl=12):
    rnd = np.random.RandomState(saat)
    perioden = [10, 12, 15, 20, 12, 15, 10, 20, 15, 12, 20, 10]
    p = []
    for i in range(anzahl):
        p.append(dict(
            T=float(perioden[i % len(perioden)]),
            off=rnd.uniform(0, 60),
            x0=cx + rnd.uniform(-28, 28),
            y0=cy + rnd.uniform(-12, 8),
            hoehe=rnd.uniform(90, 170),
            drift=rnd.uniform(-14, 22),
            wobf=int(rnd.choice([2, 3, 4])),
            wobamp=rnd.uniform(4, 9),
            wobph=rnd.uniform(0, TAU),
            gr=rnd.uniform(1.4, 2.4),
            heiss=rnd.uniform(0.55, 1.0),
        ))
    return p


# ------------------------------------------------------------------ Frames

class Renderer:
    def __init__(self, variante, bilddatei):
        self.cfg = VARIANTEN[variante]
        self.variante = variante
        base = np.asarray(Image.open(bilddatei).convert("RGB"), np.float32)
        assert base.shape == (H, W, 3), base.shape
        self.base = base
        (self.lx, self.ly, self.lr), warm = licht_finden(base)
        self.glow = glow_maske(base, warm)
        if self.cfg["sterne"]:
            self.sdelta, self.sphase, self.sfreq = stern_karte(base, self.cfg["himmel_y"])
        if self.cfg["glut"]:
            x0, y0 = int(self.lx - self.lr), int(self.ly - self.lr * 0.8)
            x1, y1 = int(self.lx + self.lr), int(self.ly + self.lr * 0.8)
            self.gbox = (max(0, y0), max(0, x0), min(H, y1), min(W, x1))
            gb = self.gbox
            kern = warm[gb[0]:gb[2], gb[1]:gb[3]]
            self.gkern = np.clip(kern / (kern.max() + 1e-6) * 1.6, 0, 1)[..., None]
            self.gfelder = rausch_felder(kern.shape, saat=21)
        if self.cfg["funken"]:
            self.funken = funken_bauen(self.lx, self.ly - 10)
        if self.cfg["rauch"]:
            self.rh, self.rw = 560, 240
            self.rtex = kachelbares_rauschen(self.rh, self.rw, saat=31)
            ay = np.linspace(0, 1, self.rh)[:, None]
            fade = np.clip(ay * 3, 0, 1) * np.clip((1 - ay) * 1.6, 0, 1)
            ax = np.abs(np.linspace(-1, 1, self.rw))[None, :]
            self.ralpha = (fade * np.clip(1 - ax, 0, 1) * 0.05).astype(np.float32)
        if self.cfg["wasser"]:
            x0, y0, x1, y1 = self.cfg["wasser"]
            L = lum(base)
            gl = np.zeros((H, W), np.float32)
            reg = L[y0:y1, x0:x1]
            hoch = np.clip(reg - _blur(reg, 4), 0, None)
            kuehl = base[y0:y1, x0:x1, 2] >= base[y0:y1, x0:x1, 0] - 6
            m = (hoch > np.percentile(hoch, 99.0)) & kuehl
            gl[y0:y1, x0:x1] = np.where(m, hoch, 0)
            self.gldelta = gl
            xs = np.arange(W, dtype=np.float32)[None, :]
            ys = np.arange(H, dtype=np.float32)[:, None]
            self.glphase = (xs * 0.045 + ys * 0.11).astype(np.float32)
        if self.cfg["nebel"]:
            x0, y0, x1, y1 = self.cfg["nebel"]
            self.ntex = kachelbares_rauschen(y1 - y0, W, saat=41, sigma=30,
                                             vertikal=False)
            ay = np.sin(np.linspace(0, np.pi, y1 - y0))[:, None].astype(np.float32)
            self.nalpha = 0.035 * ay
            self.nbox = (y0, y1)
        wg = self.cfg["wiegen"]
        if wg:
            x0, y0, x1, y1 = wg["rechteck"]
            self.wbox = (y0, x0, y1, x1)
            hh, ww = y1 - y0, x1 - x0
            ys = np.arange(y0, y1, dtype=np.float32)[:, None]
            if wg.get("kopfueber"):
                ramp = np.clip((ys - wg["fuss_y"]) / max(1, (y1 - wg["fuss_y"])), 0, 1)
            else:
                ramp = np.clip((wg["fuss_y"] - ys) / max(1, wg["fuss_y"] - y0), 0, 1)
            self.wamp = (ramp ** 1.4 * wg["amp_px"]).astype(np.float32)
            xs = np.arange(x0, x1, dtype=np.float32)[None, :]
            self.wphase = (xs * 0.011).astype(np.float32)
            gx, gy = np.meshgrid(np.arange(ww, dtype=np.float32),
                                 np.arange(hh, dtype=np.float32))
            self.wgx, self.wgy = gx, gy
            # weiche Kante, damit der Rand des Rechtecks nicht "reisst"
            rand = np.ones((hh, ww), np.float32)
            k = 40
            rand[:, :k] *= np.linspace(0, 1, k)[None, :]
            rand[:, -k:] *= np.linspace(1, 0, k)[None, :]
            rand[:k, :] *= np.linspace(0, 1, k)[:, None]
            rand[-k:, :] *= np.linspace(1, 0, k)[:, None]
            self.wrand = rand

    # ------------------------------------------------------------------
    def frame(self, t):
        """Ein Frame zur Zeit t (Sekunden). Exakt periodisch in ZYKLUS."""
        cfg = self.cfg
        out = self.base

        wg = cfg["wiegen"]
        if wg:
            y0, x0, y1, x1 = self.wbox
            sw = (0.62 * np.sin(TAU * 2 * t / ZYKLUS + self.wphase)
                  + 0.38 * np.sin(TAU * 5 * t / ZYKLUS + 1.7 + self.wphase * 1.6))
            dx = (self.wamp * sw * self.wrand).astype(np.float32)
            mx = self.wgx + dx
            reg = cv2.remap(self.base[y0:y1, x0:x1], mx, self.wgy,
                            cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            out = self.base.copy()
            out[y0:y1, x0:x1] = reg
        else:
            out = self.base.copy()

        # Lichtpuls
        a = cfg["puls_amp"]
        puls = (0.55 * np.sin(TAU * 3 * t / ZYKLUS + 1.1)
                + 0.30 * np.sin(TAU * 7 * t / ZYKLUS + 2.4)
                + 0.15 * np.sin(TAU * 13 * t / ZYKLUS + 4.0))
        out *= (1 + self.glow * (a * puls))[..., None]

        # Glut
        if cfg["glut"]:
            y0, x0, y1, x1 = self.gbox
            w1 = 0.5 + 0.5 * np.sin(TAU * 5 * t / ZYKLUS)
            w2 = 0.5 + 0.5 * np.sin(TAU * 9 * t / ZYKLUS + 2.1)
            w3 = 0.5 + 0.5 * np.sin(TAU * 16 * t / ZYKLUS + 4.4)
            s = w1 + w2 + w3
            feld = (w1 * self.gfelder[0] + w2 * self.gfelder[1]
                    + w3 * self.gfelder[2]) / s
            out[y0:y1, x0:x1] *= (1 + 0.10 * self.gkern * feld[..., None])

        # Funken (additiv, Leben endet mit Helligkeit 0 -> nahtloser Wrap)
        if cfg["funken"]:
            for p in self.funken:
                u = ((t + p["off"]) % p["T"]) / p["T"]
                hell = (np.sin(np.pi * u) ** 1.5) * p["heiss"]
                if hell < 0.02:
                    continue
                x = (p["x0"] + p["drift"] * u
                     + p["wobamp"] * np.sin(TAU * p["wobf"] * u + p["wobph"]))
                y = p["y0"] - p["hoehe"] * (u ** 0.85)
                xi, yi = int(round(x)), int(round(y))
                r = max(2, int(round(p["gr"])))
                if not (r < xi < W - r and r < yi < H - r):
                    continue
                yy, xx = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32)
                fleck = np.exp(-(xx ** 2 + yy ** 2) / (0.55 * p["gr"] ** 2))
                farbe = np.array([255, 120 + 90 * p["heiss"], 40], np.float32)
                out[yi - r:yi + r + 1, xi - r:xi + r + 1] += \
                    (hell * 0.85) * fleck[..., None] * farbe[None, None]

        # Rauch
        if cfg["rauch"]:
            x0 = int(self.lx - self.rw / 2 + 10)
            y1 = int(self.ly - 18)
            y0 = y1 - self.rh
            versch = int((t / 30.0) * self.rh) % self.rh      # 2 Loops je Zyklus
            tex = np.roll(self.rtex, versch, axis=0)
            pend = 6 * np.sin(TAU * 2 * t / ZYKLUS + 0.8)
            xs = int(round(pend))
            a2 = self.ralpha * (0.75 + 0.25 * np.sin(TAU * 3 * t / ZYKLUS + 2.2))
            al = (a2 * tex)[..., None]
            xa, xb = x0 + xs, x0 + xs + self.rw
            ya, yb = max(0, y0), y1
            ha = ya - y0
            reg = out[ya:yb, xa:xb]
            reg *= (1 - al[ha:])
            reg += al[ha:] * np.array([150, 160, 175], np.float32)[None, None]

        # Wasser-Glitzern
        if cfg["wasser"]:
            mod = 0.45 * np.sin(TAU * 4 * t / ZYKLUS + self.glphase)
            out += (self.gldelta * mod)[..., None]

        # Nebel-Drift
        if cfg["nebel"]:
            y0, y1 = self.nbox
            versch = int((t / ZYKLUS) * W) % W                # 1 Loop je Zyklus
            tex = np.roll(self.ntex, versch, axis=1)
            al = (self.nalpha * tex)[..., None]
            reg = out[y0:y1]
            reg *= (1 - al)
            reg += al * np.array([120, 135, 160], np.float32)[None, None]

        # Sterne
        if cfg["sterne"]:
            mod = 0.32 * np.sin(TAU * self.sfreq * t / ZYKLUS + self.sphase)
            out += (self.sdelta * mod)[..., None]

        return np.clip(out, 0, 255).astype(np.uint8)


# ----------------------------------------------------------------- Encoden

def rendern(variante, bilddatei, ziel, preset="slow", crf=28):
    r = Renderer(variante, bilddatei)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
           "-pix_fmt", "yuv420p",
           "-x264-params", f"keyint={FPS*10}:min-keyint={FPS*10}:scenecut=0",
           "-an", ziel]
    t0 = time.time()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(N):
        p.stdin.write(r.frame(i / FPS).tobytes())
        if (i + 1) % 240 == 0:
            print(f"    {i+1}/{N} Frames  ({time.time()-t0:.0f}s)", flush=True)
    p.stdin.close()
    p.wait()
    if p.returncode != 0:
        raise SystemExit("ffmpeg-Fehler")
    return r, time.time() - t0


def pruefen(r, ziel, variante):
    """Nahtpruefung: Determinismus, Wrap-Schritt, 3x-Rendering, Bitrate."""
    import tempfile
    b = {}

    # 1) f(0) und f(60) muessen bitidentisch sein
    f0, f60 = r.frame(0.0), r.frame(ZYKLUS)
    b["determinismus_max_diff"] = int(np.abs(f0.astype(int) - f60.astype(int)).max())

    # 2) Wrap-Schritt gegen normale Frame-Schritte
    fN = r.frame((N - 1) / FPS)
    wrap = float(np.abs(fN.astype(np.float32) - f0.astype(np.float32)).mean())
    rnd = np.random.RandomState(3)
    normal = []
    for _ in range(12):
        i = int(rnd.randint(1, N - 1))
        a = r.frame(i / FPS).astype(np.float32)
        c = r.frame((i + 1) / FPS).astype(np.float32)
        normal.append(float(np.abs(a - c).mean()))
    b["wrap_schritt_mad"] = round(wrap, 4)
    b["normaler_schritt_mad_median"] = round(float(np.median(normal)), 4)
    b["normaler_schritt_mad_max"] = round(float(np.max(normal)), 4)
    b["wrap_unauffaellig"] = bool(wrap <= np.max(normal) * 1.2)

    # 3) 3x hintereinander per Bitstrom-Kopie, Naehte dekodieren
    with tempfile.TemporaryDirectory() as td:
        lst = os.path.join(td, "l.txt")
        open(lst, "w").write(f"file '{ziel}'\n" * 3)
        drei = os.path.join(td, "drei.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat",
                        "-safe", "0", "-i", lst, "-c", "copy", drei], check=True)
        def dekod_paar(ts):
            """Zwei aufeinanderfolgende dekodierte Frames um Zeitpunkt ts."""
            o = os.path.join(td, "p%d.png")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error",
                            "-ss", f"{ts - 1/FPS:.5f}", "-i", drei,
                            "-frames:v", "2", "-start_number", "0", o],
                           check=True)
            a = np.asarray(Image.open(os.path.join(td, "p0.png")), np.float32)
            c = np.asarray(Image.open(os.path.join(td, "p1.png")), np.float32)
            return float(np.abs(c - a).mean())

        # Fair vergleichen. Zwei Basislinien:
        #  - Schritte OHNE Keyframe: reine Bewegung + P-Frame-Rauschen
        #  - Schritte UEBER interne Keyframes (alle 10 s, keyint=240):
        #    der normale "Refresh-Sprung" des Encoders, den JEDER
        #    x264-Stream traegt.
        # Die Loop-Naht ist genau so ein Keyframe-Uebergang. Sie ist dann
        # in Ordnung, wenn sie von den internen Keyframe-Schritten nicht
        # zu unterscheiden ist - kleiner kann sie physikalisch nicht werden.
        glatt = [dekod_paar(ts) for ts in (7.3, 22.6, 41.9, 95.0, 151.4)]
        kf = [dekod_paar(ts) for ts in (10.0, 30.0, 50.0, 80.0, 110.0)]
        b["dekodiert_glatt_mad_median"] = round(float(np.median(glatt)), 4)
        b["dekodiert_keyframe_mad_median"] = round(float(np.median(kf)), 4)
        b["dekodiert_keyframe_mad_max"] = round(float(np.max(kf)), 4)
        b["naht1_schritt_mad"] = round(dekod_paar(ZYKLUS), 4)
        b["naht2_schritt_mad"] = round(dekod_paar(2 * ZYKLUS), 4)
        b["naehte_unauffaellig"] = bool(
            max(b["naht1_schritt_mad"], b["naht2_schritt_mad"])
            <= b["dekodiert_keyframe_mad_max"] * 1.25)

    # 4) Bitrate
    gr = os.path.getsize(ziel)
    b["dauer_s"] = ZYKLUS
    b["groesse_mb"] = round(gr / 1e6, 2)
    b["bitrate_kbps"] = round(gr * 8 / ZYKLUS / 1000, 1)
    b["hochgerechnet_3_5h_gb"] = round(gr * (3.5 * 3600 / ZYKLUS) / 1e9, 2)
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("variante", choices=list(VARIANTEN))
    ap.add_argument("--preset", default="slow")
    ap.add_argument("--nur-pruefen", action="store_true", dest="nur_pruefen")
    a = ap.parse_args()

    bild = pfad("produktion", "motive", f"motiv-{a.variante}.png")
    ordner = pfad("produktion", "motive", "loops")
    os.makedirs(ordner, exist_ok=True)
    ziel = os.path.join(ordner, f"loop-{a.variante}.mp4")

    if a.nur_pruefen:
        r = Renderer(a.variante, bild)
        dauer = None
    else:
        print(f"  {a.variante}: rendere {N} Frames…", flush=True)
        r, dauer = rendern(a.variante, bild, ziel, preset=a.preset)
        print(f"  kodiert in {dauer:.0f}s → {ziel}", flush=True)

    b = pruefen(r, ziel, a.variante)
    if dauer is not None:
        b["renderzeit_s"] = round(dauer, 1)
    json.dump(b, open(os.path.join(ordner, f"qa-{a.variante}.json"), "w"),
              indent=1)
    print(f"\nLOOP {a.variante}")
    print(f"  f(0) == f(60)         max. Pixeldifferenz {b['determinismus_max_diff']} "
          f"({'bitidentisch' if b['determinismus_max_diff'] == 0 else 'ABWEICHUNG'})")
    print(f"  Wrap-Schritt          {b['wrap_schritt_mad']} (mittl. |Δ|/Pixel)")
    print(f"  normaler Schritt      Median {b['normaler_schritt_mad_median']}, "
          f"Max {b['normaler_schritt_mad_max']}")
    print(f"  → Naht {'unauffällig' if b['wrap_unauffaellig'] else 'AUFFÄLLIG'}")
    print(f"  3x dekodiert: Nähte   {b['naht1_schritt_mad']} / {b['naht2_schritt_mad']}")
    print(f"    Basis glatt         {b['dekodiert_glatt_mad_median']} (Median) · "
          f"interne Keyframes {b['dekodiert_keyframe_mad_median']} (Median), "
          f"{b['dekodiert_keyframe_mad_max']} (Max)")
    print(f"    → Naht vom internen Keyframe-Refresh "
          f"{'nicht unterscheidbar' if b['naehte_unauffaellig'] else 'UNTERSCHEIDBAR — AUFFÄLLIG'}")
    print(f"  Größe                 {b['groesse_mb']} MB / 60 s "
          f"→ {b['bitrate_kbps']} kbit/s")
    print(f"  hochgerechnet 3,5 h   {b['hochgerechnet_3_5h_gb']} GB (nur Bildspur)")
    if dauer is not None:
        print(f"  Renderzeit            {b['renderzeit_s']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
