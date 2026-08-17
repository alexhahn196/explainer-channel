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
# Die IDs stehen fest, weil der Schluessel das Recht `voices_read` nicht hat.
# Es sind die Standardstimmen aus dem oeffentlichen Katalog (/v1/voices ohne
# Schluessel), abgerufen am 2026-08-14.
STIMMEN = [
    ("Eric",    "maennlich", "cjVigY5qzO86Huf0OWal"),
    ("Brian",   "maennlich", "nPczCjzI2devNBz1zQrb"),
    ("Matilda", "weiblich",  "XrExE9yKIg1WjnnlVkGX"),
    ("Bella",   "weiblich",  "hpp4J3VqNfWAUOO0d1Us"),
]

WPM_ZIEL = 219.0        # aus skript.md, Messtabelle
WPM_LANGSAM = 195.0     # "etwas langsamer" — rund 11 % unter dem Zielwert
SPEED_MIN, SPEED_MAX = 0.7, 1.2

TOLERANZ_WPM = 4.0      # als getroffen gilt eine Abweichung unter 4 WPM
MAX_SCHRITTE = 3        # so viele Anlaeufe je Stimme und Zieltempo

# Fester Seed fuer JEDE Anfrage. Ohne ihn ist die Ausgabe nicht reproduzierbar:
# vier identische Anfragen an dieselbe Stimme ergaben 163,9 / 167,8 / 173,1 /
# 186,9 WPM — 23 WPM Spanne, Standardabweichung 10,05. Mit festem Seed liefert
# dieselbe Anfrage exakt dasselbe Tempo (dreimal 177,2 WPM). Erst dadurch wird
# die Tempo-Annaeherung unten ueberhaupt sinnvoll, weil sie sonst Rauschen
# statt einer Kennlinie verfolgt.
SEED = 4242
ANKER = (1.0, 1.2)      # Stuetzstellen der Kennlinie je Stimme


def interpoliere(punkte: list[tuple[float, float]], ziel: float) -> float:
    """Naechster `speed`-Versuch fuer ein Zieltempo.

    `speed` wirkt **nicht** linear: gemessen liefert speed=1.2 je nach Stimme
    das 1,25- bis 1,38-fache des natuerlichen Tempos. Ein einmaliges
    `ziel / natuerlich` verfehlt das Ziel darum deutlich. Stattdessen wird
    zwischen zwei bereits gemessenen Punkten interpoliert (Sekante) und, wo
    das Ziel ausserhalb liegt, aus den beiden naechstgelegenen extrapoliert.
    """
    def kappe(s: float) -> float:
        # Am Anschlag exakt einrasten. Die Kennlinie ist gestuft: gemessen
        # liefert speed=1.1999 bei Matilda 205,2 WPM, speed=1.2000 dagegen
        # 219,5 WPM — 14,3 WPM Sprung fuer 0,0001 Parameterunterschied. Ein
        # per Interpolation knapp verfehlter Anschlag landet also auf der
        # falschen Stufe.
        s = max(SPEED_MIN, min(SPEED_MAX, s))
        for anschlag in (SPEED_MIN, SPEED_MAX):
            if abs(s - anschlag) < 1e-3:
                return anschlag
        return s

    p = sorted(set(punkte))
    if len(p) == 1:
        s0, w0 = p[0]
        return kappe(s0 * ziel / w0)
    for (s0, w0), (s1, w1) in zip(p, p[1:]):
        if (w0 - ziel) * (w1 - ziel) <= 0 and w1 != w0:
            return kappe(s0 + (ziel - w0) * (s1 - s0) / (w1 - w0))
    nah = sorted(p, key=lambda x: abs(x[1] - ziel))[:2]
    (s0, w0), (s1, w1) = nah
    if w1 == w0:
        return kappe(s0)
    return kappe(s0 + (ziel - w0) * (s1 - s0) / (w1 - w0))


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

    def tarif(self) -> dict | None:
        """Tarif- und Zeichenstand. Braucht das Recht `user_read`; fehlt es,
        wird None geliefert und der Zeichenverbrauch nur selbst gezaehlt."""
        try:
            return self._hole("/user/subscription")
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                return None
            raise

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
                 modell: str, speed: float, lexika: list[dict] | None = None,
                 seed: int | None = None) -> dict:
        koerper = {
            "text": text,
            "model_id": modell,
            "voice_settings": {**GRUNDEINSTELLUNG, "speed": round(speed, 4)},
        }
        if lexika:
            koerper["pronunciation_dictionary_locators"] = lexika
        if seed is not None:
            koerper["seed"] = seed
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


def treffe_tempo(c: "Client", vid: str, text: str, ziel_wpm: float,
                 punkte: list[tuple[float, float]], pfad: pathlib.Path,
                 modell: str) -> tuple[dict, list[dict]]:
    """Erzeugt so lange neu, bis das gemessene Tempo nahe genug am Ziel liegt.

    Liefert die letzte Messung und den Verlauf. Die Datei unter `pfad` ist
    danach die des letzten Anlaufs. `punkte` wird um jede neue Messung
    ergaenzt, damit spaetere Zieltempi derselben Stimme davon profitieren.
    """
    verlauf: list[dict] = []
    versucht: list[float] = []
    m: dict = {}
    for _ in range(MAX_SCHRITTE):
        speed = round(interpoliere(punkte, ziel_wpm), 4)
        if any(abs(speed - s) < 1e-4 for s in versucht):
            break               # Interpolation bewegt sich nicht mehr
        versucht.append(speed)
        m = messen(c.sprechen(vid, text, pfad, modell=modell, speed=speed,
                                  seed=SEED), text)
        m["speed"] = speed
        punkte.append((speed, m["wpm_sprache"]))
        verlauf.append({"speed": speed, "wpm": m["wpm_sprache"],
                        "abweichung": round(m["wpm_sprache"] - ziel_wpm, 1)})
        if abs(m["wpm_sprache"] - ziel_wpm) <= TOLERANZ_WPM:
            break
        if speed <= SPEED_MIN or speed >= SPEED_MAX:
            break               # Regelbereich ausgeschoepft
    return m, verlauf


def punkte_aus_bericht(pfad: pathlib.Path, wortzahl: int) -> dict[str, list[tuple[float, float]]]:
    """Bereits gemessene (speed, wpm)-Paare je Stimme aus einem frueheren Lauf.

    Nur Proben mit derselben Wortzahl, also demselben Text, und ohne Lexikon —
    sonst waeren die Punkte nicht vergleichbar.
    """
    if not pfad.exists():
        return {}
    try:
        alt = json.loads(pfad.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    # Punkte aus einem Lauf mit anderem (oder ohne) Seed sind unbrauchbar:
    # ohne festen Seed streut dasselbe Tempo um bis zu 23 WPM.
    if alt.get("seed") != SEED:
        return {}
    raus: dict[str, list[tuple[float, float]]] = {}
    for p in alt.get("proben", []):
        if p.get("woerter") != wortzahl or p.get("korrektur") != "keine":
            continue
        if "speed" not in p or "wpm_sprache" not in p:
            continue
        raus.setdefault(p["stimme"], []).append((p["speed"], p["wpm_sprache"]))
    return raus


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
    if tarif:
        print(f"Tarif: {tarif.get('tier')}  —  "
              f"{tarif.get('character_count')}/{tarif.get('character_limit')} "
              f"Zeichen verbraucht")
    else:
        print("Tarif nicht lesbar (Schluessel ohne Recht `user_read`) — "
              "Zeichen werden nur selbst gezaehlt.")

    bericht: dict = {
        "modell": MODELL, "ausgabe": AUSGABE, "einstellungen": GRUNDEINSTELLUNG,
        "wpm_ziel": WPM_ZIEL, "wpm_langsam": WPM_LANGSAM, "seed": SEED,
        "tarif": {k: tarif.get(k) for k in
                  ("tier", "character_count", "character_limit",
                   "next_character_count_reset_unix")} if tarif else None,
        "proben": [],
    }
    zeichen_gesamt = 0

    # Punkte aus einem frueheren Lauf uebernehmen, damit die Annaeherung nicht
    # bei null anfaengt und keine Zeichen doppelt verbraucht werden.
    punkte = punkte_aus_bericht(HIER / "messungen.json", woerter(text))
    if punkte:
        print("Vorhandene Messpunkte je Stimme: "
              + ", ".join(f"{k}:{len(v)}" for k, v in sorted(punkte.items())))

    # --- Lauf K: Kennlinie je Stimme an zwei Stuetzstellen -------------------
    print(f"\nLauf K — Kennlinie bei speed={ANKER[0]} und {ANKER[1]} (seed={SEED})")
    for name, geschlecht, vid in STIMMEN:
        for anker in ANKER:
            ziel = HIER / f"k-{name.lower()}-speed{int(anker*100)}.mp3"
            bekannt = [w for s, w in punkte.get(name, []) if abs(s - anker) < 1e-4]
            if bekannt and ziel.exists():
                continue
            m = messen(c.sprechen(vid, text, ziel, modell=MODELL,
                                  speed=anker, seed=SEED), text)
            zeichen_gesamt += m["zeichen"]
            punkte.setdefault(name, []).append((anker, m["wpm_sprache"]))
            m |= {"datei": ziel.name, "stimme": name, "geschlecht": geschlecht,
                  "speed": anker, "lauf": "K", "korrektur": "keine"}
            bericht["proben"].append(m)
        pk = dict(punkte[name])
        spanne = pk[ANKER[1]] / pk[ANKER[0]]
        print(f"  {name:<8} {pk[ANKER[0]]:>6.1f} WPM @{ANKER[0]}  ->  "
              f"{pk[ANKER[1]]:>6.1f} WPM @{ANKER[1]}   "
              f"(Faktor {spanne:.3f} bei speed-Faktor {ANKER[1]/ANKER[0]:.2f})")

    if args.nur_kalibrieren:
        (HIER / "messungen.json").write_text(
            json.dumps(bericht, indent=2, ensure_ascii=False), encoding="utf-8")
        return 0

    # --- Laeufe A/B: die beiden Zieltempi ------------------------------------
    speed_a: dict[str, float] = {}
    for kuerzel, ziel_wpm in (("a", WPM_ZIEL), ("b", WPM_LANGSAM)):
        print(f"\nLauf {kuerzel.upper()} — Ziel {ziel_wpm:.0f} WPM "
              f"(Toleranz ±{TOLERANZ_WPM:.0f})")
        for name, geschlecht, vid in STIMMEN:
            pfad = HIER / f"{kuerzel}-{name.lower()}-{int(ziel_wpm)}wpm.mp3"
            m, verlauf = treffe_tempo(c, vid, text, ziel_wpm,
                                      punkte.setdefault(name, []), pfad, MODELL)
            zeichen_gesamt += m["zeichen"] * len(verlauf)
            abw = m["wpm_sprache"] - ziel_wpm
            erreicht = abs(abw) <= TOLERANZ_WPM
            if kuerzel == "a":
                speed_a[name] = m["speed"]
            m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
                  "lauf": kuerzel.upper(), "ziel_wpm": ziel_wpm,
                  "korrektur": "keine", "anlaeufe": len(verlauf),
                  "verlauf": verlauf, "ziel_erreicht": erreicht,
                  "speed_am_anschlag": m["speed"] >= SPEED_MAX or m["speed"] <= SPEED_MIN}
            bericht["proben"].append(m)
            print(f"  {name:<8} {len(verlauf)} Anlauf/-e, speed={m['speed']:.3f}"
                  f" -> {m['wpm_sprache']:>6.1f} WPM ({abw:+.1f})"
                  + ("" if erreicht else "   [Ziel NICHT erreicht]")
                  + ("   [speed am Anschlag]" if m["speed_am_anschlag"] else ""))

    # --- Lauf C: Aussprachekorrektur im Text ---------------------------------
    print(f"\nLauf C — Aussprachekorrektur im Text, speed wie Lauf A")
    for name, geschlecht, vid in STIMMEN:
        pfad = HIER / f"c-{name.lower()}-{int(WPM_ZIEL)}wpm-korrigiert.mp3"
        m = messen(c.sprechen(vid, text_korr, pfad, modell=MODELL,
                              speed=speed_a[name], seed=SEED), text_korr)
        zeichen_gesamt += m["zeichen"]
        m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
              "speed": speed_a[name], "lauf": "C",
              "korrektur": "Text (Respelling)"}
        bericht["proben"].append(m)
        print(f"  {name:<8} speed={speed_a[name]:.3f} -> {m['wpm_sprache']:>6.1f} WPM")

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

    name, geschlecht, vid = STIMMEN[0]
    speed = speed_a[name]
    for kuerzel, art, modell in (("d", "alias", MODELL), ("e", "phoneme", MODELL_PHONEM)):
        if not lex.get(art):
            continue
        pfad = HIER / f"{kuerzel}-{name.lower()}-{int(WPM_ZIEL)}wpm-lexikon-{art}.mp3"
        m = messen(c.sprechen(vid, text, pfad, modell=modell, speed=speed,
                              lexika=[lex[art]], seed=SEED), text)
        zeichen_gesamt += m["zeichen"]
        m |= {"datei": pfad.name, "stimme": name, "geschlecht": geschlecht,
              "speed": round(speed, 4), "lauf": kuerzel.upper(), "modell": modell,
              "korrektur": f"Lexikon ({art})"}
        bericht["proben"].append(m)
        print(f"  {art} auf {modell}: {m['wpm_sprache']:.1f} WPM -> {pfad.name}")

    tarif_neu = c.tarif()
    bericht["zeichen_gesamt_gesendet"] = zeichen_gesamt
    bericht["tarif_nachher"] = {k: tarif_neu.get(k) for k in
                                ("tier", "character_count", "character_limit")} \
        if tarif_neu else None
    bericht["zeichen_laut_konto"] = (
        tarif_neu.get("character_count", 0) - tarif.get("character_count", 0)
        if tarif and tarif_neu else None)
    (HIER / "messungen.json").write_text(
        json.dumps(bericht, indent=2, ensure_ascii=False), encoding="utf-8")
    laut_konto = bericht["zeichen_laut_konto"]
    print(f"\n{len(bericht['proben'])} Proben, {zeichen_gesamt} Zeichen gesendet, "
          + (f"{laut_konto} laut Konto abgerechnet." if laut_konto is not None
             else "Kontostand nicht lesbar."))
    print("messungen.json geschrieben.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
