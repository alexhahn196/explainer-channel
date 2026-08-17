#!/usr/bin/env python3
"""Bindet die 159 Einstellungen aus szenenplan.json an die tatsaechliche Tonspur.

Das Problem, das hier geloest wird
----------------------------------
Die Laengen in szenenplan.json sind auf 219 WPM gerechnet, Gesamtlaufzeit
9:20,0. Der Sprechtext laeuft bei der gemessenen Stimme (ElevenLabs Eric,
214,3 WPM) auf 9:39,8 hinaus — rund zwanzig Sekunden mehr. Und das ist nur
eine Schaetzung; die wirkliche Laenge steht erst fest, wenn die Spur da ist.

Die Einstellungen gleichmaessig zu strecken waere falsch: die Schnitte sitzen
auf Satzgrenzen, und gestreckt liegt jeder Schnitt ein Stueck neben seinem
Satz, am Ende um mehrere Sekunden. Stattdessen wird jede Einstellung an
ihrem eigenen Text verankert. szenenplan.json nennt zu jeder Einstellung den
Wortlaut, und aus den ElevenLabs-Zeitmarken ist bekannt, wann jedes einzelne
Zeichen gesprochen wird. Der Schnitt sitzt damit auf dem Wort, zu dem er
gehoert — der Unterschied verteilt sich von selbst dorthin, wo tatsaechlich
laenger gesprochen wird.

Unterschied zu Video 1
----------------------
Dort musste der Wortlaut je Einstellung aus der Tabelle in szenen.md
zurueckgelesen werden, mit allen Tuecken einer Markdown-Tabelle. Hier steht
er in szenenplan.json, also in der Quelle selbst — kein Parsen einer
Darstellung, und die Textkachelung ist ohnehin schon gegen skript.md
geprueft.

Aufruf:  python3 schnittplan.py      (setzt ton/ voraus)
"""
from __future__ import annotations

import json
import pathlib
import re
import unicodedata

HIER = pathlib.Path(__file__).resolve().parent
TON = HIER / "ton"

# Die Einstellungslaengen, die auffaellig sind und gemeldet werden.
KURZ_S = 1.0
LANG_S = 9.0


def zeitachse() -> tuple[str, list[float]]:
    """Der gesprochene Text als eine Zeichenkette plus Startzeit je Zeichen."""
    plan = json.loads((TON / "_zeitplan.json").read_text(encoding="utf-8"))
    text, zeiten = [], []
    for eintrag in plan:
        n = eintrag["absatz"]
        d = json.loads((TON / f"absatz-{n:02d}.json").read_text(encoding="utf-8"))
        al = d["alignment"]
        off = eintrag["start_s"]
        text.append(d["text"])
        zeiten.extend(off + t for t in al["character_start_times_seconds"])
        if n < len(plan):
            # Die Fuge zwischen zwei Absaetzen bekommt einen Platzhalter, damit
            # Textindex und Zeitindex deckungsgleich bleiben.
            text.append("\n\n")
            ende = off + al["character_end_times_seconds"][-1]
            zeiten.extend([ende, ende])
    return "".join(text), zeiten


def schluessel(s: str) -> str:
    """Nur Buchstaben und Ziffern, klein — fuer den Textvergleich."""
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z0-9]", "", s.lower())


def einstellungen() -> list[dict]:
    """Die 159 Einstellungen aus der Quelle, nicht aus der Darstellung."""
    d = json.loads((HIER / "szenenplan.json").read_text(encoding="utf-8"))
    return [{"nr": e["nr"], "text": e["text"], "motiv": e["motiv"],
             "fahrt": e["fahrt"], "dauer_soll_s": round(e["dauer"], 3)}
            for e in d["einstellungen"]]


def finde(kette: str, teil: str, ab: int) -> int:
    """Sucht `teil` ab Position `ab`; faellt auf die globale Suche zurueck."""
    i = kette.find(teil, ab)
    return i if i >= 0 else kette.find(teil)


def main() -> None:
    if not (TON / "_zeitplan.json").exists():
        raise SystemExit(
            "ton/_zeitplan.json fehlt — erst tonspur.py laufen lassen "
            "(braucht ELEVENLABS_API_KEY).")

    text, zeiten = zeitachse()
    kette = schluessel(text)
    zurueck = [i for i, c in enumerate(text) if schluessel(c)]
    assert len(zurueck) == len(kette)

    sch = einstellungen()
    print(f"{len(sch)} Einstellungen aus szenenplan.json · "
          f"{len(set(s['motiv'] for s in sch))} Motive")

    # szenenplan.json zitiert den Text in der Schreibung des Skripts,
    # gesprochen wird aber die korrigierte Fassung. Einstellungen, die genau
    # auf einer ersetzten Stelle beginnen ("In 1543 a book …", "Gaia, a
    # European craft …"), waeren sonst nicht auffindbar. Dieselbe
    # Ersetzungstabelle anwenden.
    import sprechtext
    ersetzungen = sprechtext.ZAHLEN + sprechtext.NAMEN

    cursor, ungenau = 0, []
    for s in sch:
        roh = s["text"]
        for alt, neu in ersetzungen:
            roh = roh.replace(alt, neu)
        anfang = schluessel(roh)[:18]
        pos = finde(kette, anfang, cursor) if anfang else -1
        if pos < 0:
            ungenau.append(s["nr"])
            s["start_s"] = None
            continue
        s["start_s"] = round(zeiten[zurueck[pos]], 3)
        cursor = pos + max(1, len(anfang) // 2)

    # Ende jeder Einstellung = Anfang der naechsten; die letzte laeuft aus.
    gesamt = zeiten[-1]
    for i, s in enumerate(sch):
        if s["start_s"] is None:
            continue
        naechste = next((sch[j]["start_s"] for j in range(i + 1, len(sch))
                         if sch[j]["start_s"] is not None), None)
        s["ende_s"] = round(naechste if naechste is not None else gesamt, 3)
        s["dauer_s"] = round(s["ende_s"] - s["start_s"], 3)

    gut = [s for s in sch if s.get("dauer_s")]
    kurz = [s for s in gut if s["dauer_s"] < KURZ_S]
    lang = [s for s in gut if s["dauer_s"] > LANG_S]
    soll = sum(s["dauer_soll_s"] for s in sch)
    print(f"verankert: {len(gut)}/{len(sch)} · nicht gefunden: {ungenau}")
    print(f"Laufzeit laut Verankerung: {gesamt:.2f} s = "
          f"{int(gesamt // 60)}:{gesamt % 60:04.1f}")
    print(f"Summe Soll aus szenenplan:  {soll:.1f} s = "
          f"{int(soll // 60)}:{soll % 60:04.1f}")
    print(f"Unterschied: {gesamt - soll:+.1f} s")
    if kurz:
        print(f"unter {KURZ_S} s ({len(kurz)}): "
              f"{[(s['nr'], s['dauer_s']) for s in kurz]}")
    if lang:
        print(f"ueber {LANG_S} s ({len(lang)}): "
              f"{[(s['nr'], s['dauer_s']) for s in lang]}")

    (HIER / "schnittplan.json").write_text(
        json.dumps(sch, indent=1, ensure_ascii=False), encoding="utf-8")
    fehlt = sorted({s["motiv"] for s in gut}
                   - {p.stem for p in (HIER / "bilder").glob("M*.png")})
    print(f"Motive ohne Bild: {fehlt if fehlt else 'keine'}")
    if ungenau:
        raise SystemExit(
            f"{len(ungenau)} Einstellungen ohne Anker — der Schnittplan ist "
            "unvollstaendig und darf so nicht in die Montage.")


if __name__ == "__main__":
    main()
