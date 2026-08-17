#!/usr/bin/env python3
"""Kantenspur: macht das Zittern in einem Standbild sichtbar.

Aus jedem Frame wird DIESELBE Bildzeile genommen und untereinander gelegt -
Zeit laeuft nach unten. Eine gleichmaessige Fahrt zeichnet eine glatte
Schraege, eine gerasterte Fahrt eine Treppe.
"""
import subprocess

import numpy as np

B, H = 1920, 1080
ZEILE = 300          # durch das Fenster - senkrechte Rahmenkanten
BREIT = 120          # so viele Spalten zeigen
LUPE = 5             # Vergroesserung, damit die Stufen sichtbar werden


def graustufen(pfad):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", pfad, "-f", "rawvideo",
                        "-pix_fmt", "gray", "-"], capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, B)


CLIPS = [("a  bisher", "probe-a-bisher.mp4"),
         ("b  korrigiert", "probe-b-korrigiert.mp4"),
         ("c  statisch", "probe-c-statisch.mp4")]

# Spaltenfenster dort waehlen, wo die Kanten am haertesten sind
erst = graustufen(CLIPS[0][1])[0, ZEILE].astype(np.float32)
g = np.abs(np.diff(erst))
summe = np.convolve(g, np.ones(BREIT), mode="valid")
x0 = int(np.argmax(summe))
print(f"Bildzeile {ZEILE}, Spalten {x0}-{x0+BREIT} (haerteste Kanten)")

spuren = []
for name, pfad in CLIPS:
    f = graustufen(pfad)
    spur = f[:, ZEILE, x0:x0 + BREIT].astype(np.float32)   # 144 x BREIT
    # Die Bildwelt ist dunkel; ohne Spreizung waere die Treppe nicht zu sehen.
    lo, hi = spur.min(), spur.max()
    spur = np.clip((spur - lo) / max(hi - lo, 1e-6) * 255, 0, 255).astype(np.uint8)
    spur = np.repeat(np.repeat(spur, LUPE, axis=1), 2, axis=0)
    spuren.append((name, spur))
    print(f"  {name:14s} {spur.shape[1]}x{spur.shape[0]}")

hoehe = spuren[0][1].shape[0]
trenner = np.full((hoehe, 8), 255, np.uint8)
bild = np.concatenate(
    [x for n, s in spuren for x in (s, trenner)][:-1], axis=1)
# oben Platz fuer die Beschriftung
kopf = np.full((26, bild.shape[1]), 255, np.uint8)
bild = np.concatenate([kopf, bild], axis=0)

roh = "kantenspur.raw"
bild.tofile(roh)
b, h = bild.shape[1], bild.shape[0]
beschriftung = []
x = 0
for name, s in spuren:
    beschriftung.append(f"drawtext=text='{name}':x={x + 6}:y=5:fontsize=16"
                        f":fontcolor=black")
    x += s.shape[1] + 8
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo",
                "-pix_fmt", "gray", "-s", f"{b}x{h}", "-i", roh,
                "-vf", ",".join(beschriftung), "-frames:v", "1",
                "kantenspur.png"], check=True)
print(f"\nkantenspur.png  {b}x{h}")
print("Zeit laeuft nach unten. Glatte Schraege = gleichmaessige Fahrt,")
print("Treppe = Zittern, senkrecht = Stillstand.")
