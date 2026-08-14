#!/usr/bin/env python3
"""Erzeugt die ElevenLabs-Stimmproben fuer Video 1 und misst ihr Tempo.

Der Schluessel wird ausschliesslich aus der Umgebungsvariable
`ELEVENLABS_API_KEY` gelesen und nirgends gespeichert — dieselbe Regel wie
in `produktion/config.md` ("Kein API-Schluessel ... nie im Repository").

    export ELEVENLABS_API_KEY=...
    python3 proben_erzeugen.py

Warum kalibriert wird
---------------------
ElevenLabs kennt keinen WPM-Parameter. Es gibt nur `speed`, einen relativen
Faktor von 0.7 bis 1.2 auf das natuerliche Tempo der jeweiligen Stimme. Das
natuerliche Tempo ist von Stimme zu Stimme verschieden. Um ~219 WPM zu
treffen, misst dieses Skript deshalb zuerst jede Stimme bei `speed=1.0`
(Lauf K) und rechnet daraus den noetigen Faktor aus. Gemessen wird
anschliessend erneut am fertigen Audio — berichtet wird die *gemessene*
Zahl, nicht die angepeilte.

Gemessen wird doppelt:
  `dauer_sprache_s` — letzter Zeitstempel aus der Zeichen-Alignment-Antwort
                      der API, also das Ende des letzten gesprochenen
                      Zeichens (ohne Auslaufstille).
  `dauer_datei_s`   — Laenge der MP3 laut ffprobe (mit Auslaufstille).
Beide WPM-Werte stehen im Bericht, weil sie sich systematisch unterscheiden.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import time

import requests

API = "https://api.elevenlabs.io/v1"
HIER = pathlib.Path(__file__).resolve().parent

# --- Wahl der Einstellungen (Begruendung siehe README) ------------------------
MODELL = "eleven_multilingual_v2"       # laut Doku am stabilsten fuer Langform
MODELL_PHONEM = "eleven_turbo_v2"       # nur dieses wertet <phoneme>-Regeln aus
AUSGABE = "mp3_44100_128"

GRUNDEINSTELLUNG = {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,               # bewusst 0: Style veraendert das Tempo mit
    "use_speaker_boost": True,
}

# 2 maennlich, 2 weiblich. Auswahl nach Label `informative_educational` /
# Erzaehltauglichkeit und Akzent `american` (Zielmarkt US laut README).
STIMMEN = [
    ("Eric",    "maennlich"),
    ("Brian",   "maennlich"),
    ("Matilda", "weiblich"),
    ("Bella",   "weiblich"),
]

WPM_ZIEL = 219.0        # aus skript.md, Messtabelle
WPM_LANGSAM = 195.0     # "etwas langsamer" — rund 11 % unter dem Zielwert
SPEED_MIN, SPEED_MAX = 0.7, 1.2


def woerter(text: str) -> int:
    """Wortzahl nach derselben Regel wie die Messtabelle in skript.md."""
    return len(re.findall(r"[A-Za-z0-9']+", text))


def ffmpeg_pfad() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def dauer_datei(pfad: pathlib.Path) -> float:
    """Laenge der Audiodatei in Sekunden. ffprobe liegt dem Wheel nicht bei,
    darum wird die Dauer aus dem Fortschrittsprotokoll von ffmpeg gelesen."""
    out = subprocess.run(
        [ffmpeg_pfad(), "-i", str(pfad), "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    treffer = re.findall(r"time=(\d+):(\d+):(\d+\.\d+)", out)
    if not treffer:
        raise RuntimeError(f"Keine Dauer aus ffmpeg fuer {pfad.name}")
    h, m, s = treffer[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


class Client:
    def __init__(self, schluessel: str):
        self.s = requests.Session()
        self.s.headers["xi-api-key"] = schluessel

    def _hole(self, weg: str) -> dict:
        r = self.s.get(f"{API}{weg}", timeout=60)
        r.raise_for_status()
        return r.json()

    def tarif(self) -> dict:
        return self._hole("/user/subscription")

    def stimmen(self) -> list[dict]:
        return self._hole("/voices")["voices"]

    def lexikon_anlegen(self, pls: pathlib.Path, name: str) -> dict:
        r = self.s.post(
            f"{API}/pronunciation-dictionaries/add-from-file",
            files={"file": (pls.name, pls.read_bytes(), "application/xml")},
            data={"name": name},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def sprechen(self, voice_id: str, text: str, ziel: pathlib.Path, *,
                 modell: str, speed: float, lexika: list[dict] | None = None) -> dict:
        koerper = {
            "text": text,
            "model_id": modell,
            "voice_settings": {**GRUNDEINSTELLUNG, "speed": round(speed, 4)},
        }
        if lexika:
            koerper["pronunciation_dictionary_locators"] = lexika
        for versuch in range(4):
            r = self.s.post(
                f"{API}/text-to-speech/{voice_id}/with-timestamps",
                params={"output_format": AUSGABE},
                json=koerper, timeout=300,
            )
            if r.status_code == 200:
                break
            if r.status_code in (429, 500, 502, 503) and versuch < 3:
                time.sleep(2 ** versuch)
                continue
            raise RuntimeError(f"{r.status_code} {r.text[:400]}")
        d = r.json()
        ziel.write_bytes(base64.b64decode(d["audio_base64"]))
        enden = d["alignment"]["character_end_times_seconds"]
        return {
            "dauer_sprache_s": round(enden[-1], 3),
            "dauer_datei_s": round(dauer_datei(ziel), 3),
            "zeichen": len(text),
        }


def messen(eintrag: dict, text: str) -> dict:
    n = woerter(text)
    eintrag["woerter"] = n
    eintrag["wpm_sprache"] = round(n / eintrag["dauer_sprache_s"] * 60, 1)
    eintrag["wpm_datei"] = round(n / eintrag["dauer_datei_s"] * 60, 1)
    return eintrag


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--nur-kalibrieren", action="store_true",
                   help="nur Lauf K: natuerliches Tempo je Stimme messen")
    args = p.parse_args()

    schluessel = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not schluessel:
        print("ELEVENLABS_API_KEY ist nicht gesetzt.", file=sys.stderr)
        return 2

    text = (HIER / "testtext.txt").read_text(encoding="utf-8").strip()
    text_korr = (HIER / "testtext_korrigiert.txt").read_text(encoding="utf-8").strip()
    c = Client(schluessel)

    tarif = c.tarif()
    print(f"Tarif: {tarif.get('tier')}  —  "
          f"{tarif.get('character_count')}/{tarif.get('character_limit')} Zeichen verbraucht")

    nach_name = {v["name"].split(" - ")[0]: v for v in c.stimmen()}
    fehlend = [n for n, _ in STIMMEN if n not in nach_name]
    if fehlend:
        print(f"Stimmen nicht gefunden: {fehlend}", file=sys.stderr)
        return 3

    bericht: dict = {
        "modell": MODELL, "ausgabe": AUSGABE, "einstellungen": GRUNDEINSTELLUNG,
        "wpm_ziel": WPM_ZIEL, "wpm_langsam": WPM_LANGSAM,
        "tarif": {k: tarif.get(k) for k in
                  ("tier", "character_count", "character_limit",
                   "next_character_count_reset_unix")},
        "proben": [],
    }
    zeichen_gesamt = 0

    # --- Lauf K: natuerliches Tempo je Stimme -------------------------------
    print("\nLauf K — natuerliches Tempo bei speed=1.0")
    natuerlich: dict[str, float] = {}
    for name, geschlecht in STIMMEN:
        vid = nach_name[name]["voice_id"]
        ziel = HIER / f"k-{name.lower()}-speed100.mp3"
        m = messen(c.sprechen(vid, text, ziel, modell=MODELL, speed=1.0), text)
        natuerlich[name] = m["wpm_sprache"]
        zeichen_gesamt += m["zeichen"]
        m |= {"datei": ziel.name, "stimme": name, "geschlecht": geschlecht,
              "speed": 1.0, "lauf": "K", "korrektur": "keine"}
        bericht["proben"].append(m)
        print(f"  {name:<8} {m['wpm_sprache']:>6.1f} WPM (Sprache) / "
              f"{m['wpm_datei']:>6.1f} (Datei)")

    if args.nur_kalibrieren:
        (HIER / "messungen.json").write_text(
            json.dumps(bericht, indent=2, ensure_ascii=False), encoding="utf-8")
        return 0

    # --- Laeufe A/B: die beiden Zieltempi ------------------------------------
    for kuerzel, ziel_wpm in (("a", WPM_ZIEL), ("b", WPM_LANGSAM)):
        print(f"\nLauf {kuerzel.upper()} — Ziel {ziel_wpm:.0f} WPM")
        for name, geschlecht in STIMMEN:
            vid = nach_name[name]["voice_id"]
            speed = max(SPEED_MIN, min(SPEED_MAX, ziel_wpm / natuerlich[name]))
            pfad = HIER / f"{kuerzel}-{name.lower()}-{int(ziel_wpm)}wpm.mp3"
            m = messen(c.sprechen(vid, text, pfad, modell=MODELL, speed=speed), text)
            zeichen_gesamt += m["zeichen"]
            m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
                  "speed": round(speed, 4), "lauf": kuerzel.upper(),
                  "ziel_wpm": ziel_wpm, "korrektur": "keine",
                  "speed_gekappt": not (SPEED_MIN < ziel_wpm / natuerlich[name] < SPEED_MAX)}
            bericht["proben"].append(m)
            print(f"  {name:<8} speed={speed:.3f} -> {m['wpm_sprache']:>6.1f} WPM"
                  + ("   [Faktor gekappt]" if m["speed_gekappt"] else ""))

    # --- Lauf C: Aussprachekorrektur im Text ---------------------------------
    print(f"\nLauf C — Aussprachekorrektur im Text, Ziel {WPM_ZIEL:.0f} WPM")
    for name, geschlecht in STIMMEN:
        vid = nach_name[name]["voice_id"]
        speed = max(SPEED_MIN, min(SPEED_MAX, WPM_ZIEL / natuerlich[name]))
        pfad = HIER / f"c-{name.lower()}-{int(WPM_ZIEL)}wpm-korrigiert.mp3"
        m = messen(c.sprechen(vid, text_korr, pfad, modell=MODELL, speed=speed), text_korr)
        zeichen_gesamt += m["zeichen"]
        m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
              "speed": round(speed, 4), "lauf": "C", "korrektur": "Text (Respelling)"}
        bericht["proben"].append(m)
        print(f"  {name:<8} {m['wpm_sprache']:>6.1f} WPM")

    # --- Lauf D/E: Woerterbuch-Funktion --------------------------------------
    print("\nLauf D/E — Aussprachelexikon (PLS) ueber die API")
    lex = {}
    for art, datei in (("alias", "lexikon_alias.pls"), ("phoneme", "lexikon_phoneme.pls")):
        try:
            d = c.lexikon_anlegen(HIER / datei, f"video-01-{art}")
            lex[art] = {"pronunciation_dictionary_id": d["id"], "version_id": d["version_id"]}
            print(f"  {art}: angelegt, {d.get('version_rules_num')} Regeln, id={d['id']}")
        except Exception as e:  # Tarif- oder Rechtefrage — wird im Bericht vermerkt
            lex[art] = None
            bericht.setdefault("lexikon_fehler", {})[art] = str(e)[:300]
            print(f"  {art}: FEHLER {str(e)[:200]}")
    bericht["lexikon"] = lex

    name, geschlecht = STIMMEN[0]
    vid = nach_name[name]["voice_id"]
    speed = max(SPEED_MIN, min(SPEED_MAX, WPM_ZIEL / natuerlich[name]))
    for kuerzel, art, modell in (("d", "alias", MODELL), ("e", "phoneme", MODELL_PHONEM)):
        if not lex.get(art):
            continue
        pfad = HIER / f"{kuerzel}-{name.lower()}-{int(WPM_ZIEL)}wpm-lexikon-{art}.mp3"
        m = messen(c.sprechen(vid, text, pfad, modell=modell, speed=speed,
                              lexika=[lex[art]]), text)
        zeichen_gesamt += m["zeichen"]
        m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
              "speed": round(speed, 4), "lauf": kuerzel.upper(), "modell": modell,
              "korrektur": f"Lexikon ({art})"}
        bericht["proben"].append(m)
        print(f"  {art} auf {modell}: {m['wpm_sprache']:.1f} WPM -> {pfad.name}")

    tarif_neu = c.tarif()
    bericht["zeichen_gesamt_gesendet"] = zeichen_gesamt
    bericht["tarif_nachher"] = {k: tarif_neu.get(k) for k in
                                ("tier", "character_count", "character_limit")}
    bericht["zeichen_laut_konto"] = (tarif_neu.get("character_count", 0)
                                     - tarif.get("character_count", 0))
    (HIER / "messungen.json").write_text(
        json.dumps(bericht, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(bericht['proben'])} Proben, {zeichen_gesamt} Zeichen gesendet, "
          f"{bericht['zeichen_laut_konto']} laut Konto abgerechnet.")
    print("messungen.json geschrieben.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
