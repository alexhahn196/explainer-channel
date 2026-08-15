#!/usr/bin/env python3
"""Vertont sprechtext.txt mit ElevenLabs nach den Werten aus entscheidungen.md.

Warum abschnittsweise und nicht in einem Stueck
-----------------------------------------------
`eleven_multilingual_v2` nimmt rund 10.000 Zeichen je Anfrage. Der Sprechtext
liegt mit gut 10.100 Zeichen darueber, eine einzelne Anfrage waere also nicht
sicher. Absatzweise zu rendern hat ausserdem einen Nutzen fuer die Montage:
jeder Absatz bekommt eine eigene, gemessene Laufzeit.

Damit die Uebergaenge nicht abgehackt klingen, bekommt jede Anfrage den
vorherigen und den folgenden Absatz als `previous_text` / `next_text` mit. Die
werden nicht gesprochen, steuern aber die Satzmelodie am Rand.

Der Seed ist Pflicht (entscheidungen.md): ohne ihn streut die Laufzeit
derselben Anfrage um bis zu 23 WPM und jede Einstellungslaenge aus szenen.md
waere hinfaellig.

Der Schluessel steht ausschliesslich in ELEVENLABS_API_KEY, nie im Repository.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HIER = pathlib.Path(__file__).resolve().parent
ZIEL = HIER / "ton"
API = "https://api.elevenlabs.io/v1/text-to-speech"

STIMME = "cjVigY5qzO86Huf0OWal"          # Eric
MODELL = "eleven_multilingual_v2"
SEED = 4242
FORMAT = "mp3_44100_128"
EINSTELLUNGEN = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": True,
    "speed": 1.1955,
}
# config.md nennt tts_parallel = 12. Fuer ElevenLabs ist das zu hoch, das
# Konto vertraegt 5 gleichzeitige Anfragen.
PARALLEL = 5


def schluessel() -> str:
    k = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not k:
        raise SystemExit("ELEVENLABS_API_KEY ist nicht gesetzt.")
    return k


def absaetze() -> list[str]:
    t = (HIER / "sprechtext.txt").read_text(encoding="utf-8").strip()
    return [a.strip() for a in t.split("\n\n") if a.strip()]


def eine_anfrage(i: int, teile: list[str], key: str) -> dict:
    nutzlast = {
        "text": teile[i],
        "model_id": MODELL,
        "seed": SEED,
        "voice_settings": EINSTELLUNGEN,
        "previous_text": teile[i - 1] if i > 0 else None,
        "next_text": teile[i + 1] if i + 1 < len(teile) else None,
    }
    nutzlast = {k: v for k, v in nutzlast.items() if v is not None}
    url = f"{API}/{STIMME}/with-timestamps?output_format={FORMAT}"
    daten = json.dumps(nutzlast).encode("utf-8")
    letzter = None
    for versuch in range(4):
        try:
            req = urllib.request.Request(
                url, data=daten,
                headers={"xi-api-key": key, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                antwort = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            letzter = f"HTTP {e.code}: {e.read()[:300].decode('utf-8', 'replace')}"
            if e.code not in (429, 500, 502, 503, 504):
                raise SystemExit(f"Absatz {i+1}: {letzter}")
            time.sleep(2 ** versuch * 2)
        except Exception as e:                                   # Netzfehler
            letzter = str(e)
            time.sleep(2 ** versuch * 2)
    else:
        raise SystemExit(f"Absatz {i+1} nach 4 Versuchen: {letzter}")

    import base64
    mp3 = base64.b64decode(antwort["audio_base64"])
    (ZIEL / f"absatz-{i+1:02d}.mp3").write_bytes(mp3)
    al = antwort.get("alignment") or antwort.get("normalized_alignment") or {}
    (ZIEL / f"absatz-{i+1:02d}.json").write_text(
        json.dumps({"text": teile[i], "alignment": al}, ensure_ascii=False),
        encoding="utf-8")
    ende = max(al.get("character_end_times_seconds") or [0.0])
    print(f"  Absatz {i+1:2d}  {len(teile[i]):5d} Zeichen  {ende:6.2f} s  "
          f"{len(mp3)/1024:7.1f} kB", flush=True)
    return {"nr": i + 1, "zeichen": len(teile[i]), "dauer_s": ende}


def main() -> None:
    key = schluessel()
    ZIEL.mkdir(exist_ok=True)
    teile = absaetze()
    gesamt = sum(len(t) for t in teile)
    print(f"Zu sendende Zeichen: {gesamt} in {len(teile)} Absaetzen "
          f"(Grenze 20.000)")
    if gesamt > 20000:
        raise SystemExit("Ueber der Grenze — Lauf gestoppt.")
    if "--trocken" in sys.argv:
        for i, t in enumerate(teile, 1):
            print(f"  Absatz {i:2d}  {len(t):5d} Zeichen  {t[:60]}…")
        return

    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        ergebnis = list(pool.map(lambda i: eine_anfrage(i, teile, key),
                                 range(len(teile))))

    ergebnis.sort(key=lambda e: e["nr"])
    dauer = sum(e["dauer_s"] for e in ergebnis)
    woerter = sum(len(t.split()) for t in teile)
    (ZIEL / "_absaetze.json").write_text(
        json.dumps(ergebnis, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nSumme der Absaetze: {dauer:.2f} s = {int(dauer//60)}:{dauer%60:05.2f}")
    print(f"Woerter {woerter} · gemessen {woerter/dauer*60:.1f} WPM")


if __name__ == "__main__":
    main()
