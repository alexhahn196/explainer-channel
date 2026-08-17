#!/usr/bin/env python3
"""Spracherkennung ueber alle Stimmproben, mit Wortzeitstempeln.

Zweck: objektive Belege dafuer, WIE die Stolperstellen aus `aussprache.md`
tatsaechlich gesprochen wurden. Die Erkennung hoert nicht wie ein Mensch,
aber sie ist unbestechlich in einem Punkt — sie kennt den Sollwert nicht.
Wenn ein Erkenner "Dummer" schreibt, wo "Dümmer" stehen sollte, ist das ein
Beleg fuer die in `aussprache.md` benannte Fehlform, kein Geschmacksurteil.

Zwei Modelle, damit ein einzelner Erkennerfehler nicht als Befund durchgeht.
Ergebnis nach `asr_ergebnis.json`.
"""
from __future__ import annotations

import json
import pathlib
import sys

from faster_whisper import WhisperModel

WAV = pathlib.Path("/tmp/wav")
ZIEL = pathlib.Path(__file__).resolve().parent / "asr_ergebnis.json"
MODELLE = ("small", "medium")


def lauf(modell: str) -> dict:
    m = WhisperModel(modell, device="cpu", compute_type="int8")
    raus = {}
    for wav in sorted(WAV.glob("*.wav")):
        segs, _ = m.transcribe(str(wav), language="en", word_timestamps=True,
                               beam_size=5)
        woerter, text = [], []
        for s in segs:
            text.append(s.text.strip())
            for w in (s.words or []):
                woerter.append({"wort": w.word.strip(),
                                "von": round(w.start, 3),
                                "bis": round(w.end, 3)})
        raus[wav.stem] = {"text": " ".join(text), "woerter": woerter}
        print(f"  {modell}/{wav.stem}: {len(woerter)} Woerter", flush=True)
    return raus


if __name__ == "__main__":
    alles = {}
    for modell in MODELLE:
        print(f"Modell {modell} ...", flush=True)
        alles[modell] = lauf(modell)
    ZIEL.write_text(json.dumps(alles, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\n{ZIEL} geschrieben.")
