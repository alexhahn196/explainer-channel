#!/usr/bin/env python3
"""
kamerafahrt.py - der Standardweg fuer Kamerafahrten. Ab hier baut sie
niemand mehr von Hand.

WARUM ES DIESES MODUL GIBT (2026-08-17)
=======================================
Der frueher direkt in schritt5_video.py gebaute Filter hat sichtbar
gezittert - pixelweise Spruenge, am staerksten bei flachen Grafiken mit
harten Konturen, also bei genau unserer Bildwelt.

Ursache, nachgemessen: `vf_zoompan.c` rundet den Ausschnitt auf ganze
QUELLpixel, Groesse UND Lage:

    w = in->width  * (1.0 / zoom);      /* int */
    h = in->height * (1.0 / zoom);      /* int */
    x = av_clipd(dx, 0, in->width - w); /* int */

Die Zoomstufe ist eine Fliesskommazahl, der Ausschnitt, den sie
beschreibt, ist es nicht. Die Fahrt steht also still und springt dann um
einen ganzen Quellpixel weiter. Verschaerft wurde das dadurch, dass
schritt4_bild.py jede Quelle vorab auf die Ausgabegroesse herunterrechnete:
danach war ein Quellpixel gleich einem Ausgabepixel, und zoompan zog den
Ausschnitt wieder hoch.

Gemessen an einer 6-s-Einstellung: **0,998 px Ruckeln** - genau der eine
Quellpixel. Beim BibelTube-Originalfall (Faktor 1,04 ueber 300 s) waren
**99,0 % aller Frames exakte Standbilder**.

LOESUNG: UEBERABTASTEN, DANN HERUNTERSKALIEREN
==============================================
    Quelle, beliebige Groesse
      -> EINMAL scale=<4x>:flags=lanczos      Rasterstufe faellt auf 1/4 Pixel
      -> loop                                 der teure Schritt laeuft nur einmal
      -> zoompan s=<2x>                       rechnet auf doppelter Groesse
      -> scale=<1x>:flags=lanczos             mittelt den Restsprung weg

Ergebnis derselben Einstellung: **0,148 px Ruckeln**, und die Kontur ist am
Ende der Fahrt 7,5 % haerter als vorher, weil herunter- statt hochskaliert
wird.

WAS DABEI WOVON ABHAENGT - der Punkt, an dem man sich leicht irrt
=================================================================
Entscheidend fuer das Zittern ist NICHT die Aufloesung der Quelldatei,
sondern die Aufloesung dessen, was zoompan zu sehen bekommt. Die
Ueberabtastung stellt das her, und zwar unabhaengig von der Quelle:

    Quelle 2752 px, ueberabgetastet auf 7680 -> 0,148 px Ruckeln
    Quelle 1920 px, ueberabgetastet auf 7680 -> 0,146 px Ruckeln  (gemessen)

Beide gleich ruhig. Die kleinere Quelle ist nur **weicher** (Kantenschaerfe
0,885 gegen 0,917 am Ende der Fahrt), nicht unruhiger.

Daraus folgen zwei getrennte Regeln, die man nicht vermengen darf:

  ZITTERN    zoompan braucht >= 3x Ausgabebreite am Eingang.
             Erledigt UEBERABTASTUNG = 4, immer, ohne Zutun.
  SCHAERFE   Die Quelldatei sollte >= Ausgabebreite x groesster Zoomfaktor
             sein, sonst rechnet die Fahrt am Ende echtes Detail hoch.
             Bei 1920 px Ausgabe und Zoom 1,08 sind das 2074 px.
             Unsere Bilder kommen mit 2752 px - passt.

Eine zu kleine Quelle ist also ein Schaerfe-, kein Zitterproblem. Darauf
prueft quelle_pruefen().

Zwei einfachere Fassungen sind geprueft und schlechter (Messwerte in
recherche/kamerafahrt-proben/README.md): zoompan direkt auf die Ausgabe
statt ueber die Zwischengroesse ruckelt mit 0,250 px und ist 15 % weicher -
der interne Bicubic von zoompan taugt nicht als 4:1-Verkleinerer.

zoompan hat KEINE Flags-Option (`ffmpeg -h filter=zoompan`: nur
zoom/z, x, y, d, s, fps). Der interne Skalierer ist auf SWS_BICUBIC
festgenagelt. Bessere Interpolation gibt es nur UM den Filter herum -
deshalb die Zwischengroesse und das lanczos danach.

NICHT WIEDER EINBAUEN
=====================
  - zoompan direkt auf ein Bild in Ausgabegroesse  -> zittert um 1 px
  - die Quelle vor der Fahrt kleinrechnen          -> nimmt die Reserve weg
  - zoompan direkt auf die Endgroesse rechnen      -> ruckelt und ist weich

Aufruf zur Kontrolle:
    python3 produktion/pipeline/kamerafahrt.py bild.png probe.mp4 \
        --dauer 6 --zoom-bis 1.08 --schwenk 0.7
"""
import argparse
import os
import subprocess
import sys

# Was zoompan zu sehen bekommt, wird auf das Vierfache der Ausgabebreite
# gebracht: eine Rasterstufe ist dann 0,25 Ausgabepixel.
UEBERABTASTUNG = 4
# Unter dem Dreifachen wird der Sprung wieder sichtbar (0,33 px). Gemessen.
# Gilt fuer den EINGANG von zoompan, nicht fuer die Quelldatei.
MINDESTFAKTOR = 3
# zoompan rechnet auf das Doppelte der Ausgabe, danach lanczos auf 1x.
ZWISCHENFAKTOR = 2

assert UEBERABTASTUNG >= MINDESTFAKTOR, (
    "UEBERABTASTUNG unter MINDESTFAKTOR abgesenkt - dann zittert es wieder.")

ARTEN = ("statisch", "fahrt", "atemzyklus")


def _rampe(n, art):
    """Bewegungsverlauf ueber n Frames. zoompan zaehlt `on` ab 1.

    fahrt       einwegig, Steigung an beiden Enden null - bei 3-4 s
                Einstellungen setzt die Fahrt damit weich am Schnitt an
    atemzyklus  voller Zyklus, beginnt und endet bei 1,0 mit Steigung null
                und ist deshalb exakt schleifenfaehig (Kanal-1-Technik)

    Das `on-1` ist nicht kosmetisch. Mit blossem `on` beginnt die Bewegung
    erst beim zweiten Frame, und die beiden Faelle brechen unterschiedlich:
      fahrt       erreicht den Zielzoom nie ganz
      atemzyklus  Naht beim Schleifen 4,6-mal so gross wie ein normaler
                  Frameschritt (gemessen, 0,33 gegen 0,07 von 255)
    Nenner deshalb: der Zyklus teilt durch n, damit Frame n wieder Frame 0
    ist; die einwegige Fahrt durch n-1, damit der letzte Frame das Ziel
    trifft.
    """
    if art == "atemzyklus":
        return f"(1-cos(2*PI*(on-1)/{n}))/2"
    return f"(1-cos(PI*(on-1)/{max(n - 1, 1)}))/2"


def filterkette(dauer_s, fps, breite, hoehe, art="fahrt",
                zoom_von=1.0, zoom_bis=1.06, schwenk_x=0.0, schwenk_y=0.0,
                ueberabtastung=UEBERABTASTUNG):
    """Die vollstaendige -vf Kette von der Quelldatei bis zum Ausgabeformat.

    schwenk_x/-y laufen von -1 bis +1 und bedeuten: wie weit der Ausschnitt
    bis zum Ende des Bildes an den Rand des VERFUEGBAREN Wegs wandert. 0
    bleibt mittig. Der verfuegbare Weg entsteht erst durch den Zoom - ein
    reiner Schwenk braucht deshalb einen konstanten Zoom ueber 1,0.
    """
    if art not in ARTEN:
        raise ValueError(f"art muss eine von {ARTEN} sein, nicht {art!r}")
    n = max(1, int(round(dauer_s * fps)))

    # Schritt 1: auf 16:9 in Ausgabegroesse bringen - ohne zu verzerren.
    zuschnitt = (f"scale={breite}:{hoehe}"
                 f":force_original_aspect_ratio=increase:flags=lanczos,"
                 f"crop={breite}:{hoehe}")
    if art == "statisch":
        # Kein zoompan, kein Zwischenformat: ein einziger Abtastschritt.
        # Das ist das schaerfste Bild, das aus der Quelle zu holen ist.
        # `loop` muss trotzdem sein - ohne es liefert ein Standbild genau
        # einen Frame, und -frames:v kann keine erfinden.
        return (f"{zuschnitt},loop=loop={n - 1}:size=1:start=0,"
                f"fps={fps},format=yuv420p")

    if abs(zoom_von - 1.0) < 1e-9 and abs(zoom_bis - 1.0) < 1e-9 and (
            schwenk_x or schwenk_y):
        raise ValueError(
            "Schwenk ohne Zoom ist nicht moeglich: der Ausschnitt fuellt bei "
            "Zoom 1,0 das ganze Bild, es gibt keinen Weg zu schwenken. "
            "Fuer einen reinen Schwenk zoom_von = zoom_bis > 1,0 setzen.")

    gross_b, gross_h = breite * ueberabtastung, hoehe * ueberabtastung
    zwischen_b, zwischen_h = breite * ZWISCHENFAKTOR, hoehe * ZWISCHENFAKTOR
    r = _rampe(n, art)
    z = (f"{zoom_von:.6f}" if abs(zoom_bis - zoom_von) < 1e-9
         else f"{zoom_von:.6f}+{zoom_bis - zoom_von:.6f}*{r}")
    x = f"(iw-iw/zoom)*(0.5+{schwenk_x / 2:+.6f}*{r})"
    y = f"(ih-ih/zoom)*(0.5+{schwenk_y / 2:+.6f}*{r})"

    return (
        # einmal ueberabtasten - die teure Skalierung laeuft genau hier,
        f"scale={gross_b}:{gross_h}"
        f":force_original_aspect_ratio=increase:flags=lanczos,"
        f"crop={gross_b}:{gross_h},"
        # ... und `loop` haelt das Ergebnis fest, statt es je Frame neu zu
        # rechnen. Deshalb braucht der Weg keine Zwischendatei.
        f"loop=loop={n - 1}:size=1:start=0,"
        f"zoompan=z='{z}':x='{x}':y='{y}'"
        f":d=1:s={zwischen_b}x{zwischen_h}:fps={fps},"
        f"scale={breite}:{hoehe}:flags=lanczos,format=yuv420p")


def quelle_pruefen(bild, breite, zoom_bis=1.06, streng=False):
    """Warnt, wenn die Quelle zu klein fuer eine SCHARFE Fahrt ist.

    Nicht zu verwechseln mit dem Zittern: das ist durch die Ueberabtastung
    erledigt, egal wie gross die Quelle ist (gemessen, siehe Kopf dieser
    Datei). Hier geht es nur um Schaerfe. Am Ende der Fahrt zeigt das Bild
    einen Ausschnitt von Quellbreite/zoom_bis - liegt der unter der
    Ausgabebreite, wird echtes Detail hochgerechnet.
    """
    aus = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", bild],
        capture_output=True, text=True, check=True).stdout.strip()
    qb, qh = (int(v) for v in aus.split(",")[:2])
    noetig = int(-(-breite * max(zoom_bis, 1.0) // 1))       # aufgerundet
    if qb < noetig:
        text = (f"{os.path.basename(bild)} ist {qb}x{qh}. Bei {breite} px "
                f"Ausgabe und Zoom bis {zoom_bis:.2f} zeigt das letzte Bild "
                f"nur noch {int(qb / max(zoom_bis, 1.0))} echte Pixel Breite "
                f"- ab {noetig} px Quellbreite bliebe die Fahrt scharf. "
                f"Sie zittert deswegen NICHT, sie wird nur weicher.")
        if streng:
            raise SystemExit(f"FEHLER: {text}")
        print(f"  WARNUNG: {text}", file=sys.stderr)
        return False
    return True


def bauen(bild, ziel, dauer_s, cfg, art="fahrt", zoom_von=1.0, zoom_bis=1.06,
          schwenk_x=0.0, schwenk_y=0.0, crf=None, preset=None, gop=None):
    """Eine Einstellung rendern. Gibt die Zahl der Frames zurueck."""
    fps = int(cfg["fps"])
    breite, hoehe = int(cfg["breite"]), int(cfg["hoehe"])
    n = max(1, int(round(dauer_s * fps)))
    if art != "statisch":
        quelle_pruefen(bild, breite, zoom_bis=max(zoom_von, zoom_bis))
    vf = filterkette(dauer_s, fps, breite, hoehe, art=art, zoom_von=zoom_von,
                     zoom_bis=zoom_bis, schwenk_x=schwenk_x,
                     schwenk_y=schwenk_y)
    cmd = ["ffmpeg", "-y", "-loglevel", "error",
           "-framerate", str(fps), "-i", bild,
           "-vf", vf, "-frames:v", str(n), "-r", str(fps),
           "-c:v", "libx264",
           "-preset", str(preset or cfg.get("video_preset", "medium")),
           "-crf", str(int(crf if crf is not None else cfg["video_crf"])),
           "-pix_fmt", "yuv420p", "-an"]
    if gop:
        cmd += ["-g", str(int(gop))]
    subprocess.run(cmd + [ziel], check=True)
    return n


def selbsttest(bild, cfg, dauer_s=2.0):
    """Prueft, was eine Sichtkontrolle nicht sieht: Laenge und Bildzahl.

    Ein Standbild liefert ohne `loop` genau EINEN Frame, und -frames:v kann
    keine erfinden - der Clip ist dann 0,04 s lang statt der bestellten
    Dauer. Beim Bauen dieses Moduls genau so passiert. Fuer eine Montage,
    in der 159 Einstellungen auf eine feste Tonspur treffen, waere das
    fatal und in der Vorschau eines einzelnen Clips kaum zu bemerken.
    """
    import tempfile
    fps = int(cfg["fps"])
    soll = int(round(dauer_s * fps))
    faelle = [("statisch", 1.0, 1.0, 0.0), ("fahrt", 1.0, 1.06, 0.0),
              ("fahrt", 1.08, 1.08, 1.0), ("atemzyklus", 1.0, 1.04, 0.0)]
    fehler = 0
    with tempfile.TemporaryDirectory() as tmp:
        for art, zv, zb, sx in faelle:
            ziel = os.path.join(tmp, f"{art}-{zv}-{zb}-{sx}.mp4")
            bauen(bild, ziel, dauer_s, cfg, art=art, zoom_von=zv,
                  zoom_bis=zb, schwenk_x=sx, crf=28, preset="ultrafast")
            aus = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-count_frames", "-show_entries",
                 "stream=nb_read_frames,width,height",
                 "-show_entries", "format=duration",
                 "-of", "default=nw=1:nk=1", ziel],
                capture_output=True, text=True, check=True).stdout.split()
            b, h, frames, dauer = (int(aus[0]), int(aus[1]), int(aus[2]),
                                   float(aus[3]))
            ok = (frames == soll and abs(dauer - dauer_s) < 1.0 / fps
                  and (b, h) == (int(cfg["breite"]), int(cfg["hoehe"])))
            fehler += not ok
            print(f"  {'ok  ' if ok else 'FEHL'} art={art:11s} "
                  f"zoom {zv:.2f}->{zb:.2f} schwenk {sx:+.1f}   "
                  f"{b}x{h}  {frames}/{soll} Frames  {dauer:.3f}/{dauer_s:.3f} s")
    print(f"\n  {len(faelle) - fehler} von {len(faelle)} bestanden")
    return fehler


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("bild")
    ap.add_argument("ziel", nargs="?")
    ap.add_argument("--selbsttest", action="store_true",
                    help="alle Arten bauen und Laenge/Bildzahl pruefen")
    ap.add_argument("--dauer", type=float, default=6.0)
    ap.add_argument("--art", choices=ARTEN, default="fahrt")
    ap.add_argument("--zoom-von", type=float, default=1.0, dest="zoom_von")
    ap.add_argument("--zoom-bis", type=float, default=1.06, dest="zoom_bis")
    ap.add_argument("--schwenk", type=float, default=0.0, dest="schwenk_x",
                    help="-1 bis +1, waagerecht")
    ap.add_argument("--schwenk-hoch", type=float, default=0.0,
                    dest="schwenk_y", help="-1 bis +1, senkrecht")
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--breite", type=int, default=1920)
    ap.add_argument("--hoehe", type=int, default=1080)
    ap.add_argument("--crf", type=int, default=16)
    a = ap.parse_args()
    cfg = {"fps": a.fps, "breite": a.breite, "hoehe": a.hoehe,
           "video_crf": a.crf, "video_preset": "slow"}
    if a.selbsttest:
        return 1 if selbsttest(a.bild, cfg) else 0
    if not a.ziel:
        ap.error("ziel fehlt (oder --selbsttest verwenden)")
    n = bauen(a.bild, a.ziel, a.dauer, cfg, art=a.art, zoom_von=a.zoom_von,
              zoom_bis=a.zoom_bis, schwenk_x=a.schwenk_x,
              schwenk_y=a.schwenk_y)
    print(f"  {a.ziel}  {n} Frames, {a.dauer:.3f} s, art={a.art}, "
          f"{os.path.getsize(a.ziel)/1e6:.2f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
