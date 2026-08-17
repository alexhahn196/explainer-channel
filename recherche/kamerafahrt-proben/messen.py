#!/usr/bin/env python3
"""Misst das Zittern in den fertigen Clips - am dekodierten Bild, also an
dem, was der Zuschauer wirklich sieht.

Zwei Groessen je Frameuebergang:
  |D|  mittlere Pixeldifferenz zum Vorframe  -> wie viel bewegt sich ueberhaupt
  dx   Bildversatz in Pixeln, subpixelgenau  -> WIE es sich bewegt

Zittern zeigt sich nicht an der Groesse der Bewegung, sondern an ihrer
Unregelmaessigkeit: eingefrorene Frames, dann ein Sprung.
"""
import subprocess
import sys

import numpy as np

B, H = 1920, 1080
FENSTER = (slice(H // 2 - 256, H // 2 + 256), slice(B // 2 - 448, B // 2 + 448))


def frames(pfad):
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", pfad, "-f", "rawvideo",
         "-pix_fmt", "gray", "-"], capture_output=True, check=True)
    a = np.frombuffer(p.stdout, np.uint8)
    return a.reshape(-1, H, B).astype(np.float32)


def versatz(a, b):
    """Subpixelgenauer Versatz b->a per Phasenkorrelation + Parabelscheitel."""
    a = a - a.mean()
    b = b - b.mean()
    fenster = np.hanning(a.shape[0])[:, None] * np.hanning(a.shape[1])[None, :]
    A = np.fft.rfft2(a * fenster)
    Bf = np.fft.rfft2(b * fenster)
    R = A * np.conj(Bf)
    R /= np.abs(R) + 1e-9
    k = np.fft.irfft2(R, a.shape)
    iy, ix = np.unravel_index(np.argmax(k), k.shape)

    def scheitel(m, c, p):                      # Parabel durch drei Punkte
        n = 2 * (m - 2 * c + p)
        return 0.0 if abs(n) < 1e-12 else (m - p) / n

    dx = ix + scheitel(k[iy, (ix - 1) % k.shape[1]], k[iy, ix],
                       k[iy, (ix + 1) % k.shape[1]])
    dy = iy + scheitel(k[(iy - 1) % k.shape[0], ix], k[iy, ix],
                       k[(iy + 1) % k.shape[0], ix])
    if dx > k.shape[1] / 2:
        dx -= k.shape[1]
    if dy > k.shape[0] / 2:
        dy -= k.shape[0]
    return dx, dy


def pruefen(name, pfad):
    f = frames(pfad)
    d = np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))
    med = float(np.median(d))
    # "eingefroren" = Bewegung unter einem Viertel des Normalmasses
    frost = int((d < 0.25 * med).sum()) if med > 1e-6 else len(d)
    vx = np.array([versatz(f[i + 1][FENSTER], f[i][FENSTER])[0]
                   for i in range(len(f) - 1)])
    # Ruckeln = wie stark die Geschwindigkeit von Frame zu Frame springt,
    # gemessen gegen ihren eigenen glatten Verlauf (gleitendes Mittel, 9)
    kern = np.ones(9) / 9
    glatt = np.convolve(vx, kern, mode="same")
    rest = vx[4:-4] - glatt[4:-4]

    print(f"\n{name}")
    print(f"  Frames                          {len(f)}")
    print(f"  |D| Median / Max                {med:6.3f} / {d.max():6.3f}")
    print(f"  |D| Max/Median                  {d.max()/max(med,1e-6):6.2f}"
          f"        <- 1 = voellig gleichmaessig")
    print(f"  eingefrorene Frames             {frost:4d} von {len(d)}"
          f"  = {100*frost/len(d):.1f} %")
    print(f"  Versatz je Frame  min / max     {vx.min():+6.3f} / {vx.max():+6.3f} px")
    print(f"  RUCKELN (Streuung um den"
          f"\n          glatten Verlauf)        {rest.std():6.3f} px"
          f"        <- das ist das Zittern")
    return med, frost, rest.std()


if __name__ == "__main__":
    print("=" * 74)
    print("Gemessen am dekodierten Bild der drei Probeclips")
    print("=" * 74)
    for n, p in [("(a) bisheriger Weg", "probe-a-bisher.mp4"),
                 ("(b) Korrektur: Ueberabtastung 4x, dann herunterskaliert",
                  "probe-b-korrigiert.mp4"),
                 ("(c) statisch", "probe-c-statisch.mp4")]:
        pruefen(n, p)
    print()
