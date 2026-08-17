#!/usr/bin/env python3
"""Rechnet nach, was ffmpeg vf_zoompan.c je Frame tatsaechlich tut.

Massgeblich sind drei Zeilen aus output_single_frame():
    w = in->width  * (1.0 / zoom);   ->  int, abgeschnitten
    h = in->height * (1.0 / zoom);   ->  int, abgeschnitten
    x = av_clipd(dx, 0, iw - w);     ->  int, abgeschnitten
Der Ausschnitt rastet also auf ganze QUELLpixel ein - Groesse UND Lage.
`on` zaehlt in zoompan ab 1 (frame_count_in + 1).
"""
import math

W_OUT, H_OUT = 1920, 1080


def lauf(name, src_w, src_h, zoompan_w, zoompan_h, n, zoomziel,
         pan_anteil=0.0, einzeln=False):
    """Simuliert n Frames und misst die Rasterung in AUSGABE-Pixeln."""
    A = zoomziel - 1.0
    letzte = None
    breiten, lagen = set(), set()
    eingefroren = 0
    # Restfehler = gerastete Lage minus ideal glatte Lage, in Ausgabepixeln.
    # Das IST das Zittern: die eigentliche Fahrt steckt in der idealen Bahn,
    # was uebrig bleibt, ist der Saegezahn der Rundung.
    rest_pos, rest_skala = [], []
    for i in range(1, n + 1):
        on = i
        # gleiche Kosinus-Rampe wie in schritt5_video.py, hier einwegig
        rampe = (1 - math.cos(math.pi * on / n)) / 2
        z = 1.0 + A * rampe
        w_ideal = src_w / z
        w = int(w_ideal)
        h = int(src_h / z)
        x_ideal = (src_w - w_ideal) / 2 + pan_anteil * src_w * rampe
        x = int(max(0.0, min((src_w - w) / 2 + pan_anteil * src_w * rampe,
                             src_w - w)))
        breiten.add(w)
        lagen.add(x)
        massstab = W_OUT / w_ideal          # Quellpixel -> Ausgabepixel
        rest_pos.append((x - x_ideal) * massstab)
        # Rundung der Ausschnittsbreite -> Massstabsfehler, am Bildrand am
        # groessten (halbe Bildbreite Hebel)
        rest_skala.append((W_OUT / w - W_OUT / w_ideal) * w_ideal / 2)
        if letzte is not None and letzte == (w, x):
            eingefroren += 1
        letzte = (w, x)
    amp_pos = max(rest_pos) - min(rest_pos)
    amp_skala = max(rest_skala) - min(rest_skala)
    print(f"\n{name}")
    print(f"  Quelle {src_w}x{src_h}  ->  zoompan s={zoompan_w}x{zoompan_h}"
          f"  ->  Ausgabe {W_OUT}x{H_OUT}")
    print(f"  {n} Frames, Zoom 1,00 -> {zoomziel:.2f}"
          + (f", Schwenk {pan_anteil*100:.1f} % der Bildbreite" if pan_anteil else ""))
    print(f"  ein Quellpixel                  = {W_OUT/src_w:.3f} Ausgabepixel")
    print(f"  Ausschnittsbreiten              {len(breiten):5d} verschiedene "
          f"auf {n} Frames")
    print(f"  Ausschnittslagen                {len(lagen):5d} verschiedene "
          f"auf {n} Frames")
    print(f"  Frames ohne jede Aenderung      {eingefroren:5d} "
          f"= {100*eingefroren/(n-1):.1f} %   <- Standbild mitten in der Fahrt")
    print(f"  ZITTERN Lage   (Saegezahn)      {amp_pos:5.2f} Ausgabepixel")
    print(f"  ZITTERN Skala  (Bildrand)       {amp_skala:5.2f} Ausgabepixel")
    return eingefroren, amp_pos


print("=" * 74)
print("A  BISHERIGER WEG  (schritt5_video.py, Bild aus schritt4_bild.py)")
print("=" * 74)
# schritt4_bild.py skaliert JEDE Quelle vorab auf breite x hoehe = 1920x1080.
lauf("A1  Originalfall BibelTube: Atemzyklus 300 s, Faktor 1,04, 24 fps",
     1920, 1080, 1920, 1080, n=24 * 300, zoomziel=1.04)
lauf("A2  Derselbe Code auf eine 6-s-Einstellung angewandt (Zoom + Schwenk)",
     1920, 1080, 1920, 1080, n=144, zoomziel=1.08, pan_anteil=0.025)

print()
print("=" * 74)
print("B  KORREKTUR: Ueberabtastung, danach herunterskalieren")
print("=" * 74)
lauf("B1  Quelle 2752 nativ (nur 16:9 beschnitten), zoompan direkt auf 1920",
     2730, 1536, 1920, 1080, n=144, zoomziel=1.08, pan_anteil=0.025)
lauf("B2  Quelle 3x (5760), zoompan s=2880, danach lanczos auf 1920",
     5760, 3240, 2880, 1620, n=144, zoomziel=1.08, pan_anteil=0.025)
lauf("B3  Quelle 4x (7680), zoompan s=3840, danach lanczos auf 1920",
     7680, 4320, 3840, 2160, n=144, zoomziel=1.08, pan_anteil=0.025)

print()
print("=" * 74)
print("Faustregel")
print("=" * 74)
print("Zittern verschwindet, wenn BEIDE Bedingungen halten:")
print("  1. mehr ganzzahlige Rasterstufen als Frames  -> kein Standbild-Frame")
print("  2. eine Rasterstufe < ~0,3 Ausgabepixel      -> Sprung unsichtbar")
print("Bedingung 2 heisst: Quellbreite >= ~3x Ausgabebreite.")
