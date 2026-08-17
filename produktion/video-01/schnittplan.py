#!/usr/bin/env python3
"""Bindet die 139 Einstellungen aus szenen.md an die tatsaechliche Tonspur.

Das Problem, das hier geloest wird
----------------------------------
Die Laengen in szenen.md sind auf 219 WPM gerechnet, Gesamtlaufzeit 8:34. Die
fertige Spur laeuft 8:58 — rund 24 Sekunden laenger. Die Einstellungen einfach
gleichmaessig zu strecken waere falsch: die Schnitte sind auf Satzgrenzen
gesetzt, und gestreckt liege jeder Schnitt ein Stueck neben seinem Satz, am
Ende um mehrere Sekunden.

Stattdessen wird jede Einstellung an ihrem eigenen Text verankert. szenen.md
nennt zu jeder Einstellung den Wortlaut ("Look down the … road under you."),
und aus den ElevenLabs-Zeitmarken ist bekannt, wann jedes einzelne Zeichen
gesprochen wird. Der Schnitt sitzt damit auf dem Wort, zu dem er gehoert — die
24 Sekunden verteilen sich von selbst dorthin, wo tatsaechlich laenger
gesprochen wird.

Die Zeitmarken stammen aus `/with-timestamps`, nicht aus der Spracherkennung:
sie kommen vom Erzeuger selbst und sind damit exakt, nicht geschaetzt.
"""
from __future__ import annotations

import json
import pathlib
import re
import unicodedata

HIER = pathlib.Path(__file__).resolve().parent
TON = HIER / "ton"

FAHRTEN = {"Zoom rein", "Zoom raus", "Schwenk links", "Schwenk rechts", "statisch"}


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
    zeilen = (HIER / "szenen.md").read_text(encoding="utf-8").splitlines()
    raus = []
    for z in zeilen:
        if not z.startswith("|"):
            continue
        f = [x.strip() for x in z.strip().strip("|").split("|")]
        if len(f) < 7 or not f[0].isdigit():
            continue
        motiv = re.sub(r"[^A-Z0-9]", "", f[4])
        fahrt = f[6] if f[6] in FAHRTEN else "statisch"
        raus.append({"nr": int(f[0]), "text": f[1], "dauer_soll_s": float(
            re.sub(r"[^0-9.]", "", f[3]) or 0), "motiv": motiv, "fahrt": fahrt})
    return raus


def finde(kette: str, teil: str, ab: int) -> int:
    """Sucht `teil` ab Position `ab`; faellt auf die globale Suche zurueck."""
    i = kette.find(teil, ab)
    return i if i >= 0 else kette.find(teil)


def main() -> None:
    text, zeiten = zeitachse()
    kette = schluessel(text)
    # Abbildung: Position in der bereinigten Kette -> Index im Originaltext
    zurueck = [i for i, c in enumerate(text) if schluessel(c)]
    assert len(zurueck) == len(kette)

    sch = einstellungen()
    print(f"{len(sch)} Einstellungen aus szenen.md · "
          f"{len(set(s['motiv'] for s in sch))} Motive")

    # szenen.md zitiert den Text in der Schreibung des Skripts, gesprochen wird
    # aber die korrigierte Fassung. Fuenf Einstellungen beginnen genau auf einer
    # ersetzten Stelle ("3807 BC …", "Pr 31, they …", "Chaco Canyon …") und
    # waeren sonst nicht auffindbar. Dieselbe Ersetzungstabelle anwenden.
    import sprechtext
    ersetzungen = sprechtext.ZAHLEN + sprechtext.GEMESSEN + sprechtext.UNGEPRUEFT

    cursor, ungenau = 0, []
    for s in sch:
        roh = s["text"]
        for alt, neu in ersetzungen:
            roh = roh.replace(alt, neu)
        teile = [t.strip() for t in roh.split("…")]
        anfang = schluessel(teile[0])[:18]
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
    kurz = [s for s in gut if s["dauer_s"] < 1.0]
    lang = [s for s in gut if s["dauer_s"] > 9.0]
    print(f"verankert: {len(gut)}/{len(sch)} · nicht gefunden: {ungenau}")
    print(f"Laufzeit laut Verankerung: {gesamt:.2f} s")
    print(f"Summe Soll aus szenen.md:  {sum(s['dauer_soll_s'] for s in sch):.1f} s")
    if kurz:
        print(f"unter 1 s ({len(kurz)}): {[(s['nr'], s['dauer_s']) for s in kurz]}")
    if lang:
        print(f"ueber 9 s ({len(lang)}): {[(s['nr'], s['dauer_s']) for s in lang]}")

    (HIER / "schnittplan.json").write_text(
        json.dumps(sch, indent=1, ensure_ascii=False), encoding="utf-8")
    fehlt = sorted({s["motiv"] for s in gut}
                   - {p.stem for p in (HIER / "bilder").glob("M*.png")})
    print(f"Motive ohne Bild: {fehlt if fehlt else 'keine'}")


if __name__ == "__main__":
    main()
