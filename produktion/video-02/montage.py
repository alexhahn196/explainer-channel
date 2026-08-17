#!/usr/bin/env python3
"""Rendert aus schnittplan.json und den Motivbildern das fertige Video.

Aus produktion/video-01/montage.py uebernommen. Geaendert sind nur der
Ausgabename und der Nachhall am Schluss: ABSPANN_S war bei Video 1 an der
fertigen Spur gemessen (letzter hoerbarer Laut bei 538,093 s) und muss fuer
Video 2 an dessen Spur neu gemessen werden. Bis dahin steht hier derselbe
Wert, ausdruecklich als Platzhalter.

Kamerafahrt ueber ein Standbild
-------------------------------
Jede Einstellung ist ein Standbild mit einer Bewegung darueber — die Machart
des Vorbilds. Umgesetzt wird das nicht mit `zoompan`: dessen Versatz rechnet in
ganzen Pixeln, wodurch eine langsame Fahrt sichtbar ruckelt. Stattdessen
schneidet `crop` mit zeitabhaengigen Ausdruecken ein wanderndes Fenster aus dem
hochskalierten Bild, und `scale` bringt es auf 1920x1080. Der Zuschnitt bleibt
dabei durchgehend groesser als das Ziel, also wird nie hochgerechnet.

Die Bilder liegen mit 2752x1536 vor, also reichlich ueber Full HD. Das Fenster
kann daher bis zu 12 % wandern oder zoomen, ohne an Schaerfe zu verlieren.

Laufzeit und Ton
----------------
Die Einstellungslaengen stehen fest in schnittplan.json, verankert am
tatsaechlich gesprochenen Wort. Das Video ist damit von sich aus synchron; der
Ton wird am Ende nur noch daruntergelegt, nicht gedehnt oder verschoben.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import imageio_ffmpeg

HIER = pathlib.Path(__file__).resolve().parent
BILDER = HIER / "bilder"
TON = HIER / "ton" / "tonspur.mp3"
BAU = HIER / "_bau"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

BREITE, HOEHE, FPS = 1920, 1080, 30
HUB = 0.12          # wie weit Zoom und Schwenk hoechstens gehen
RAND = 0.02         # Sicherheitsrand, damit der Zuschnitt nie ans Bild stoesst

# Nachhall am Schluss. Der Wert stammt aus Video 1, wo er an der fertigen
# Spur gemessen wurde: der letzte hoerbare Laut endete bei 538,093 s, das
# Bild bei 538,100 s. Ohne den Zuschlag bricht das Video auf der letzten
# Silbe ab. Fuer Video 2 ist er UNGEMESSEN und darum ein Platzhalter — nach
# dem ersten Lauf an der eigenen Spur nachmessen.
ABSPANN_S = 1.4


def fahrt_kette(fahrt: str, bilder: int) -> str:
    """Baut die zoompan-Kette fuer eine Kamerafahrt.

    Erster Versuch lief ueber `crop` mit zeitabhaengiger Breite. Das kann
    ffmpeg nicht: `crop` legt seine Ausgabegroesse beim Aufbau der Filterkette
    einmal fest, nur x und y duerfen je Bild wandern. Jede Zoomfahrt brach
    darum mit "Error when evaluating the expression" ab.

    `zoompan` kann es, rechnet seinen Versatz aber in ganzen Pixeln des
    Eingangsbildes — bei einer langsamen Fahrt sieht man das als Ruckeln.
    Darum wird das Bild vorher auf die doppelte Zielbreite gebracht: ein
    ganzer Pixel dort ist ein halber im Ergebnis, und die Fahrt laeuft glatt.
    """
    n = max(2, bilder)
    p = f"on/{n - 1}"                       # 0 … 1 ueber die Einstellung
    if fahrt == "Zoom rein":
        z, x = f"1+{HUB}*{p}", "iw/2-(iw/zoom/2)"
    elif fahrt == "Zoom raus":
        z, x = f"{1 + HUB}-{HUB}*{p}", "iw/2-(iw/zoom/2)"
    elif fahrt == "Schwenk rechts":
        z, x = f"{1 + HUB / 2}", f"(iw-iw/zoom)*{p}"
    elif fahrt == "Schwenk links":
        z, x = f"{1 + HUB / 2}", f"(iw-iw/zoom)*(1-{p})"
    else:                                    # statisch
        z, x = f"{1 + HUB / 2}", "iw/2-(iw/zoom/2)"
    return (f"scale={BREITE * 2}:-2:flags=lanczos,"
            f"zoompan=z='{z}':x='{x}':y='ih/2-(ih/zoom/2)':"
            f"d={n}:s={BREITE}x{HOEHE}:fps={FPS},"
            f"setsar=1,format=yuv420p")


def rendere(s: dict) -> pathlib.Path | None:
    bild = BILDER / f"{s['motiv']}.png"
    ziel = BAU / f"{s['nr']:03d}.mp4"
    if ziel.exists():
        return ziel
    if not bild.exists():
        return None
    dauer = max(0.2, float(s["dauer_s"]))
    bilder = max(2, round(dauer * FPS))
    kette = fahrt_kette(s["fahrt"], bilder)
    cmd = [FFMPEG, "-v", "error", "-y", "-loop", "1", "-i", str(bild),
           "-vf", kette, "-frames:v", str(bilder), "-r", str(FPS),
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", str(ziel)]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        print(f"  Einstellung {s['nr']} ({s['motiv']}): "
              f"{r.stderr.decode('utf-8','replace')[:200]}", flush=True)
        return None
    return ziel


def main() -> None:
    plan = json.loads((HIER / "schnittplan.json").read_text(encoding="utf-8"))
    nur = None
    if "--bis" in sys.argv:
        nur = int(sys.argv[sys.argv.index("--bis") + 1])
        plan = [s for s in plan if s["nr"] <= nur]
    if "--neu" in sys.argv and BAU.exists():
        shutil.rmtree(BAU)
    BAU.mkdir(exist_ok=True)

    fehlt = sorted({s["motiv"] for s in plan
                    if not (BILDER / f"{s['motiv']}.png").exists()})
    if fehlt:
        print(f"Ohne Bild, werden uebersprungen: {fehlt}")
    if plan and not nur:
        plan[-1] = dict(plan[-1], dauer_s=plan[-1]["dauer_s"] + ABSPANN_S)

    with ThreadPoolExecutor(max_workers=4) as pool:
        teile = list(pool.map(rendere, plan))

    fertig = [(s, t) for s, t in zip(plan, teile) if t]
    print(f"{len(fertig)}/{len(plan)} Einstellungen gerendert")
    if len(fertig) < len(plan):
        print("UNVOLLSTAENDIG — es fehlen Bilder. Kein Endvideo.")

    liste = BAU / "liste.txt"
    liste.write_text("".join(f"file '{t.name}'\n" for _, t in fertig),
                     encoding="utf-8")
    ziel = HIER / ("video-02-probe.mp4" if nur else "video-02.mp4")
    laenge = sum(s["dauer_s"] for s, _ in fertig)
    # Ton mit Stille verlaengern, damit der Nachhall stehen bleibt.
    cmd = [FFMPEG, "-v", "error", "-y", "-f", "concat", "-safe", "0",
           "-i", str(liste), "-i", str(TON),
           "-filter_complex", f"[1:a]apad=pad_dur={ABSPANN_S + 0.5}[a]",
           "-map", "0:v:0", "-map", "[a]",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-shortest", "-movflags", "+faststart", str(ziel)]
    subprocess.run(cmd, check=True, cwd=BAU)
    mb = ziel.stat().st_size / 1024 / 1024
    print(f"{ziel.name}  {laenge:.1f} s = {int(laenge//60)}:{laenge%60:04.1f}  {mb:.1f} MB")


if __name__ == "__main__":
    main()
