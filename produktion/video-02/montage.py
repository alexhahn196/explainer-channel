#!/usr/bin/env python3
"""Rendert aus schnittplan.json und den Motivbildern das fertige Video.

Aus produktion/video-01/montage.py uebernommen. Geaendert sind nur der
Ausgabename und der Nachhall am Schluss: ABSPANN_S war bei Video 1 an der
fertigen Spur gemessen (letzter hoerbarer Laut bei 538,093 s) und muss fuer
Video 2 an dessen Spur neu gemessen werden. Bis dahin steht hier derselbe
Wert, ausdruecklich als Platzhalter.

Kamerafahrt ueber ein Standbild
-------------------------------
Jede Einstellung ist ein Standbild mit einer Bewegung darueber - die Machart
des Vorbilds. Gebaut wird die Bewegung **nicht mehr hier**, sondern in
produktion/pipeline/kamerafahrt.py; dieses Skript sagt nur noch, WELCHE
Fahrt eine Einstellung bekommt.

  NEU 2026-08-17. Vorher stand die Filterkette hier und brachte das Bild
  auf die doppelte Zielbreite (3840), bevor `zoompan` darauf lief. Das war
  der richtige Gedanke, aber zu knapp bemessen: `zoompan` rastet den
  Ausschnitt auf ganze QUELLpixel, und bei 3840 px Eingang ist ein
  Quellpixel immer noch ein halber Ausgabepixel. Der Standardweg tastet
  vierfach ueber (7680), rechnet `zoompan` auf 3840 und reduziert erst
  danach mit lanczos auf 1920 - Restsprung 0,25 statt 0,5 Ausgabepixel,
  gemessen 0,150 gegen 0,998 px beim ungeschuetzten Weg. Begruendung und
  Messwerte: recherche/kamerafahrt-proben/README.md.

  Zwei weitere Unterschiede zur alten Fassung, beide beabsichtigt:
  - Die Rampe laeuft als Kosinus statt linear. Die Fahrt ist damit am
    Schnitt am langsamsten und setzt weich an, statt hart loszulaufen.
  - Der 16:9-Zuschnitt geschieht jetzt VOR der Fahrt. Die alte Kette
    skalierte 2752x1536 (Seitenverhaeltnis 1,792) auf 3840x2143 und liess
    `zoompan` daraus 16:9 machen - das quetschte das Bild um 0,8 % in der
    Breite. Jetzt wird beschnitten statt gequetscht.

Statisch bei Figuren
--------------------
Zeigt ein Motiv einen Menschen - ganz, als Kopf oder als Hand bei der
Arbeit -, laeuft die Einstellung ohne Bewegung. Eine Fahrt ueber eine
gezeichnete Figur mit harten Konturen ist die Stelle, an der jede
Restunruhe am ehesten auffaellt, und die Figur gewinnt nichts dadurch.
Welches Motiv eine Figur zeigt, steht nicht in einer Liste hier, sondern
wird aus dem FRAMING-Absatz von bildplan2-prompts.json gelesen - derselben
Quelle, aus der die Bilder erzeugt wurden.

Laufzeit und Ton
----------------
Die Einstellungslaengen stehen fest in schnittplan.json, verankert am
tatsaechlich gesprochenen Wort. Das Video ist damit von sich aus synchron;
der Ton wird am Ende nur noch daruntergelegt, nicht gedehnt oder verschoben.
"""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HIER = pathlib.Path(__file__).resolve().parent
BILDER = HIER / "bilder"
TON = HIER / "ton" / "tonspur.mp3"
BAU = HIER / "_bau"
PROMPTS = HIER / "bildplan2-prompts.json"

sys.path.insert(0, str(HIER.parent / "pipeline"))
import kamerafahrt                                              # noqa: E402

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ModuleNotFoundError:
    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

BREITE, HOEHE, FPS = 1920, 1080, 30
HUB = 0.12          # wie weit Zoom und Schwenk hoechstens gehen
RUHE = 1 + HUB / 2  # Zoom einer unbewegten Einstellung: Mitte des Hubs,
                    # damit der Ausschnitt ueber den Schnitt gleich bleibt

# Nachhall am Schluss. Der Wert stammt aus Video 1, wo er an der fertigen
# Spur gemessen wurde: der letzte hoerbare Laut endete bei 538,093 s, das
# Bild bei 538,100 s. Ohne den Zuschlag bricht das Video auf der letzten
# Silbe ab. Fuer Video 2 ist er UNGEMESSEN und darum ein Platzhalter - nach
# dem ersten Lauf an der eigenen Spur nachmessen.
ABSPANN_S = 1.4

CRF, PRESET = 18, "veryfast"

# Formulierungen aus dem FRAMING-Absatz der Bildprompts, die einen
# dargestellten Menschen ankuendigen. "one part of a body only" ist eine
# Hand oder ein Fuss gross im Bild - auch das ist eine Figur.
FIGUR_MARKER = ("a single person", "several people", "one head only",
                "one part of a body only")


def figurmotive(pfad=PROMPTS):
    """Motive, die einen Menschen zeigen - aus den Bildprompts gelesen."""
    if not pfad.exists():
        return set()
    prompts = json.loads(pfad.read_text(encoding="utf-8"))
    treffer = set()
    for motiv, text in prompts.items():
        m = re.search(r"FRAMING:(.*?)(?:ADDITION|COLOUR|\Z)", text, re.S)
        rahmen = " ".join(m.group(1).split()) if m else ""
        if any(k in rahmen for k in FIGUR_MARKER):
            treffer.add(motiv)
    return treffer


def fahrtwerte(fahrt: str) -> dict:
    """Uebersetzt die Fahrtangabe des Schnittplans in kamerafahrt-Werte.

    Die Bewegung ist dieselbe wie in der alten Fassung: Zoom ueber den
    vollen Hub, Schwenk ueber den ganzen verfuegbaren Weg (-1 bis +1) bei
    festem Zoom in der Hubmitte.
    """
    if fahrt == "Zoom rein":
        return dict(art="fahrt", zoom_von=1.0, zoom_bis=1 + HUB)
    if fahrt == "Zoom raus":
        return dict(art="fahrt", zoom_von=1 + HUB, zoom_bis=1.0)
    if fahrt == "Schwenk rechts":
        return dict(art="fahrt", zoom_von=RUHE, zoom_bis=RUHE,
                    schwenk_von=-1.0, schwenk_bis=1.0)
    if fahrt == "Schwenk links":
        return dict(art="fahrt", zoom_von=RUHE, zoom_bis=RUHE,
                    schwenk_von=1.0, schwenk_bis=-1.0)
    return dict(art="statisch", zoom_von=RUHE)


def rendere(s: dict) -> pathlib.Path | None:
    bild = BILDER / f"{s['motiv']}.png"
    ziel = BAU / f"{s['nr']:03d}.mp4"
    if ziel.exists():
        return ziel
    if not bild.exists():
        return None
    dauer = max(0.2, float(s["dauer_s"]))
    cfg = {"fps": FPS, "breite": BREITE, "hoehe": HOEHE,
           "video_crf": CRF, "video_preset": PRESET}
    try:
        kamerafahrt.bauen(str(bild), str(ziel), dauer, cfg,
                          crf=CRF, preset=PRESET, **fahrtwerte(s["fahrt_neu"]))
    except subprocess.CalledProcessError as e:
        print(f"  Einstellung {s['nr']} ({s['motiv']}): {e}", flush=True)
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

    # Figurenregel anwenden. Der Schnittplan bleibt unangetastet - die
    # Entscheidung steht in fahrt_neu daneben, damit sie nachlesbar ist.
    figuren = figurmotive()
    umgestellt = 0
    for s in plan:
        mit_figur = s["motiv"] in figuren
        s["fahrt_neu"] = "statisch" if mit_figur else s["fahrt"]
        umgestellt += s["fahrt_neu"] != s["fahrt"]
    benutzt = {s["motiv"] for s in plan}
    print(f"Figurenregel: {len(benutzt & figuren)} von {len(benutzt)} "
          f"verwendeten Motiven zeigen einen Menschen, "
          f"{umgestellt} Einstellungen dadurch auf statisch umgestellt")

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
