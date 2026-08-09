#!/usr/bin/env python3
"""
Schritt 1 - Text.

Baut das vollstaendige Sprechskript eines Videos:

    Hook  ->  CTA 1  ->  CTA 2  ->  Eingangsgebet  ->  Korpus

Die Reihenfolge ist eine **Planungsentscheidung, kein Datenbefund**:
Formel §3 haelt ausdruecklich fest, dass ein festes Schema
Hook->CTA->Gebet->Lesung NICHT belegt ist. Belegt sind nur die Randbedingungen,
die diese Reihenfolge einhaelt: Sprache ab Sekunde 0-3 (n=24), hoechstens
2 CTA (Gewinner 0-2, tote Kanaele 4-7), und beide CTA laut Vorlage in den
ersten 60 Sekunden.

Bibeltext: World English Bible **British Edition** (WEBBE) ueber bible-api.com.
Nicht die klassische WEB - die uebersetzt den Gottesnamen als "Yahweh"
(Formel §4). Das wird hier nicht geglaubt, sondern geprueft.

Fuer die TTS wird "LORD" zu "Lord" normalisiert. Versalien liest das Modell
sonst als Buchstabenfolge. Das ist rein klanglich; der gelesene Text bleibt
woertlich (Formel §4: niemals paraphrasieren).

Aufruf:
    python3 produktion/pipeline/schritt1_text.py V1
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import arbeit, config, pfad          # noqa: E402
import vorlage                                       # noqa: E402

CACHE = pfad("produktion", "korpus", "text")

EINER = ["", "one", "two", "three", "four", "five", "six", "seven", "eight",
         "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
         "sixteen", "seventeen", "eighteen", "nineteen"]
ZEHNER = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
          "eighty", "ninety"]
ORDNUNGSZAHL = {"1": "First", "2": "Second", "3": "Third"}


def in_worten(n):
    """1..999 als englisches Zahlwort - fuer Kapitelansagen."""
    if n < 20:
        return EINER[n]
    if n < 100:
        r = ZEHNER[n // 10]
        return f"{r}-{EINER[n % 10]}" if n % 10 else r
    r = f"{EINER[n // 100]} hundred"
    return f"{r} {in_worten(n % 100)}" if n % 100 else r


def buchname(buch):
    """'1 peter' -> 'First Peter'."""
    teile = buch.split()
    if teile[0] in ORDNUNGSZAHL:
        return ORDNUNGSZAHL[teile[0]] + " " + " ".join(w.capitalize() for w in teile[1:])
    return " ".join(w.capitalize() for w in teile)


def ansage(ref):
    """Kapitelansage. Psalmen heissen 'Psalm N', alles andere 'Buch, chapter N'."""
    buch, nr = ref.rsplit(" ", 1)
    nr = int(nr)
    if buch == "psalms":
        return f"Psalm {in_worten(nr)}."
    return f"{buchname(buch)}, chapter {in_worten(nr)}."


# ------------------------------------------------------------------ Abruf

def hole(ref, uebersetzung, api, versuche=5):
    p = os.path.join(CACHE, re.sub(r"\W+", "_", ref) + f".{uebersetzung}.json")
    if os.path.exists(p):
        return ref, json.load(open(p, encoding="utf-8"))
    u = f"{api}/{urllib.parse.quote(ref)}?translation={uebersetzung}"
    for a in range(versuche):
        try:
            with urllib.request.urlopen(u, timeout=90) as r:
                d = json.load(r)
            if d.get("translation_id") != uebersetzung:
                raise RuntimeError(f"falsche Uebersetzung: {d.get('translation_id')}")
            verse = [{"v": int(v["verse"]), "k": int(v["chapter"]),
                      "text": " ".join(v["text"].split())} for v in d["verses"]]
            if not verse:
                raise RuntimeError("keine Verse")
            os.makedirs(CACHE, exist_ok=True)
            json.dump(verse, open(p, "w", encoding="utf-8"), ensure_ascii=False)
            return ref, verse
        except Exception as e:
            if a == versuche - 1:
                return ref, {"fehler": str(e)}
            time.sleep(1.5 * (a + 1))


# ---------------------------------------------------------- Normalisierung

VERSAL = re.compile(r"\b([A-Z]{2,})\b")


def normalisieren(text, protokoll):
    """Versalien fuer die TTS entschaerfen. Aendert keinen Wortlaut."""
    def ersetzen(m):
        w = m.group(1)
        protokoll[w] = protokoll.get(w, 0) + 1
        return w.capitalize()
    return VERSAL.sub(ersetzen, text)


# ------------------------------------------------------------------ Aufbau

def bauen(video, hook_variante=None):
    cfg = config()
    v = vorlage.lies(video)
    fehlt = vorlage.pruefe(v)
    if fehlt:
        raise SystemExit(f"{video}: Vorlage unvollstaendig: {fehlt}")

    plan = json.load(open(pfad("produktion", "korpus", "plan.json"), encoding="utf-8"))
    refs = plan[video]["refs"]

    hv = hook_variante or v.get("hook_empfohlen") or "a"
    if hv not in v["hook"]:
        raise SystemExit(f"{video}: Hook-Variante {hv} nicht in der Vorlage")

    # Die typografischen Anfuehrungszeichen der Vorlage sind Auszeichnung,
    # nicht Text - sie duerfen nicht in die TTS.
    segmente = []
    for absatz in v["hook"][hv]:
        segmente.append({"art": "rahmen", "rolle": f"hook_{hv}",
                         "text": vorlage._entkerne(absatz)})
    for i, c in enumerate(v["cta"], 1):
        segmente.append({"art": "rahmen", "rolle": f"cta{i}",
                         "text": vorlage._entkerne(c)})
    for absatz in v["gebet"]:
        segmente.append({"art": "rahmen", "rolle": "gebet",
                         "text": vorlage._entkerne(absatz)})

    print(f"{len(refs)} Kapitel holen ({cfg['uebersetzung'].upper()})…", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        geholt = dict(ex.map(lambda r: hole(r, cfg["uebersetzung"], cfg["bibel_api"]), refs))
    kaputt = {r: d["fehler"] for r, d in geholt.items() if isinstance(d, dict)}
    if kaputt:
        raise SystemExit(f"Kapitel nicht abrufbar: {kaputt}")

    protokoll = {}
    kapitel = []
    for ref in refs:
        start = len(segmente)
        segmente.append({"art": "ueberschrift", "ref": ref, "text": ansage(ref)})
        for vv in geholt[ref]:
            roh = vv["text"]
            t = normalisieren(roh, protokoll) if cfg.get("versalien_normalisieren", True) else roh
            # "text" geht an die TTS, "anzeige" in den Untertitel. Der
            # Untertitel ist sichtbarer, durchsuchbarer Text - dort gehoert
            # der WEBBE-Wortlaut hin ("LORD"), nicht die Aussprachehilfe.
            # capitalize() aendert die Laenge nicht, deshalb bleiben alle
            # Zeichenoffsets und die Wortzahl identisch.
            segmente.append({"art": "vers", "ref": ref, "vers": vv["v"],
                             "text": t, "anzeige": roh})
        kapitel.append({"ref": ref, "ansage": ansage(ref),
                        "von_segment": start, "bis_segment": len(segmente) - 1})

    # --- Kontrollen -------------------------------------------------
    for s in segmente:
        s.setdefault("anzeige", s["text"])
        if len(s["anzeige"]) != len(s["text"]):
            raise SystemExit(f"Normalisierung hat die Laenge geaendert: {s['text'][:60]!r}")
    volltext = " ".join(s["text"] for s in segmente)
    if "Yahweh" in volltext:
        raise SystemExit("Text enthaelt 'Yahweh' - das ist die klassische WEB, "
                         "nicht die WEBBE (Formel §4).")
    rest_versal = sorted(set(VERSAL.findall(volltext)))
    ziffern = sorted(set(re.findall(r"\b\d+\b", volltext)))

    woerter = len(volltext.split())
    zeichen = sum(len(s["text"]) for s in segmente)
    korpus_w = sum(len(s["text"].split()) for s in segmente if s["art"] != "rahmen")
    rahmen_w = woerter - korpus_w
    wpm = float(cfg["wpm_erwartet"])

    bericht = {
        "video": video,
        "titel": v["titel"],
        "hook_variante": hv,
        "kapitel_anzahl": len(refs),
        "segmente": len(segmente),
        "woerter_gesamt": woerter,
        "woerter_korpus": korpus_w,
        "woerter_rahmen": rahmen_w,
        "woerter_soll_vorlage": v["woerter_soll"],
        "abweichung_korpus_zur_vorlage": korpus_w - (v["woerter_soll"] or 0),
        "zeichen_tts": zeichen,
        "wpm_erwartet": wpm,
        "laufzeit_erwartet_h": round(woerter / wpm / 60, 3),
        "versalien_normalisiert": dict(sorted(protokoll.items(), key=lambda x: -x[1])),
        "versalien_uebrig": rest_versal,
        "ziffern_im_text": ziffern,
        "cta_anzahl": len(v["cta"]),
    }

    a = arbeit(video, "skript.json")
    json.dump({"bericht": bericht, "kapitel": kapitel, "segmente": segmente},
              open(a, "w", encoding="utf-8"), ensure_ascii=False)
    open(arbeit(video, "skript.txt"), "w", encoding="utf-8").write(
        "\n".join(s["text"] for s in segmente))
    return bericht, a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--hook", choices=["a", "b"], default=None)
    a = ap.parse_args()
    b, p = bauen(a.video, a.hook)
    cfg = config()

    print(f"\nSKRIPT {b['video']} — {b['titel']}")
    print(f"  Hook-Variante         {b['hook_variante']}")
    print(f"  Kapitel               {b['kapitel_anzahl']}")
    print(f"  Wörter gesamt         {b['woerter_gesamt']:,}".replace(",", "."))
    print(f"    davon Korpus        {b['woerter_korpus']:,}".replace(",", ".")
          + f"  (Vorlage: {b['woerter_soll_vorlage']:,}".replace(",", ".")
          + f", Abweichung {b['abweichung_korpus_zur_vorlage']:+})")
    print(f"    davon Rahmen        {b['woerter_rahmen']:,}".replace(",", "."))
    print(f"  Zeichen für die TTS   {b['zeichen_tts']:,}".replace(",", "."))
    print(f"  erwartete Laufzeit    {b['laufzeit_erwartet_h']:.2f} h "
          f"bei {b['wpm_erwartet']} WPM")

    von, bis = cfg["laufzeit_ziel_von_h"], cfg["laufzeit_ziel_bis_h"]
    h = b["laufzeit_erwartet_h"]
    lage = ("im Zielband" if von <= h <= bis else
            "ÜBER dem Zielband" if h > bis else
            "unter dem Zielband, aber über der harten Untergrenze"
            if h >= cfg["laufzeit_min_h"] else "UNTER der harten Untergrenze 3,0 h")
    print(f"  Zielband {von}–{bis} h  →  {lage}")
    if b["versalien_normalisiert"]:
        print(f"  Versalien normalisiert: {b['versalien_normalisiert']}")
    if b["versalien_uebrig"]:
        print(f"  ACHTUNG Versalien übrig: {b['versalien_uebrig']}")
    if b["ziffern_im_text"]:
        print(f"  Ziffern im Text (TTS prüfen): {b['ziffern_im_text']}")
    print(f"  geschrieben: {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
