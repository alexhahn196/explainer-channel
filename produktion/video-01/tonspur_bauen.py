#!/usr/bin/env python3
"""Setzt die 17 Absatzdateien zu einer Tonspur zusammen.

Zwischen den Absaetzen steht eine Atempause. Sie ist noetig, weil jeder Absatz
einzeln gerendert wurde und daher hart an seinem letzten Laut endet — ohne
Pause klebten die Kapitel aneinander.

Zusammengesetzt wird ueber PCM, nicht durch Aneinanderhaengen der MP3-Dateien:
MP3-Rahmen haben am Anfang und Ende Polster, die beim blossen Verketten als
Knacken hoerbar werden. Einmal dekodieren, im Speicher fuegen, einmal kodieren.

Nebenprodukt ist `_zeitplan.json` — der Startzeitpunkt jedes Absatzes in der
fertigen Spur. Die Montage haengt daran.
"""
from __future__ import annotations

import json
import pathlib
import subprocess

import imageio_ffmpeg
import numpy as np

HIER = pathlib.Path(__file__).resolve().parent
TON = HIER / "ton"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
RATE = 44100

# Atempause zwischen zwei Absaetzen. Innerhalb eines Absatzes setzt die Stimme
# ihre Satzpausen selbst; hier geht es nur um die Fuge.
PAUSE_S = 0.42


def lade(p: pathlib.Path) -> np.ndarray:
    roh = subprocess.run(
        [FFMPEG, "-v", "error", "-i", str(p), "-f", "s16le", "-acodec",
         "pcm_s16le", "-ac", "1", "-ar", str(RATE), "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(roh, dtype=np.int16).astype(np.float32) / 32768.0


def main() -> None:
    teile = sorted(TON.glob("absatz-*.mp3"))
    if len(teile) != 17:
        raise SystemExit(f"{len(teile)} Absaetze gefunden, erwartet 17")

    pause = np.zeros(int(PAUSE_S * RATE), dtype=np.float32)
    stuecke, plan, pos = [], [], 0.0
    for i, p in enumerate(teile):
        a = lade(p)
        plan.append({"absatz": i + 1, "start_s": round(pos, 3),
                     "dauer_s": round(len(a) / RATE, 3)})
        stuecke.append(a)
        pos += len(a) / RATE
        if i + 1 < len(teile):
            stuecke.append(pause)
            pos += PAUSE_S

    spur = np.concatenate(stuecke)
    spitze = float(np.abs(spur).max())
    print(f"Spitzenpegel vor Normalisierung: {20*np.log10(spitze):.2f} dBFS")
    # Auf -1 dBFS bringen, damit die Montage Kopfraum hat und nichts clippt.
    spur = spur * (10 ** (-1.0 / 20) / spitze)

    ziel = TON / "tonspur.mp3"
    subprocess.run(
        [FFMPEG, "-v", "error", "-y", "-f", "f32le", "-ar", str(RATE), "-ac", "1",
         "-i", "-", "-codec:a", "libmp3lame", "-b:a", "128k", str(ziel)],
        input=spur.astype(np.float32).tobytes(), check=True)

    (TON / "_zeitplan.json").write_text(
        json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")

    dauer = len(spur) / RATE
    woerter = len((HIER / "sprechtext.txt").read_text(encoding="utf-8").split())
    print(f"tonspur.mp3  {dauer:.2f} s = {int(dauer//60)}:{dauer%60:05.2f}  "
          f"{ziel.stat().st_size/1024/1024:.2f} MB")
    print(f"{woerter} Woerter · {woerter/dauer*60:.1f} WPM ueber die ganze Spur")


if __name__ == "__main__":
    main()
