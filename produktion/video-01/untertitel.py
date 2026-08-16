#!/usr/bin/env python3
"""Schreibt untertitel.srt aus den ElevenLabs-Zeitmarken.

Die Zeiten stammen aus `/with-timestamps`, also vom Erzeuger der Stimme selbst
und nicht aus einer Spracherkennung — sie sind damit exakt und muessen nicht
nachgeprueft werden.

Umbrochen wird nach Lesbarkeit, nicht nach Satzgrenzen: hoechstens zwei Zeilen,
hoechstens 42 Zeichen je Zeile, mindestens eine und hoechstens sechs Sekunden
Standzeit. Der Umbruch sucht die naechste Satz- oder Klauselgrenze und weicht
nur dann auf eine Wortgrenze aus, wenn sonst die Laenge riss.

Die Umschreibungen aus dem Sprechtext gehoeren NICHT in den Untertitel — dort
steht die richtige Schreibung. "Deemer" wird also wieder zu "Dümmer".
"""
from __future__ import annotations

import json
import pathlib

HIER = pathlib.Path(__file__).resolve().parent
TON = HIER / "ton"

MAX_ZEILE = 42
MAX_ZEILEN = 2
MIN_STAND = 1.0
MAX_STAND = 6.0


def zeitachse() -> list[tuple[str, float, float]]:
    """(Zeichen, Start, Ende) fuer den ganzen Text."""
    plan = json.loads((TON / "_zeitplan.json").read_text(encoding="utf-8"))
    raus = []
    for e in plan:
        d = json.loads((TON / f"absatz-{e['absatz']:02d}.json").read_text(encoding="utf-8"))
        al, off = d["alignment"], e["start_s"]
        for c, a, b in zip(al["characters"],
                           al["character_start_times_seconds"],
                           al["character_end_times_seconds"]):
            raus.append((c, off + a, off + b))
        raus.append((" ", raus[-1][2], raus[-1][2]))
    return raus


def rueck_umschreibung(s: str) -> str:
    """Macht die Aussprache-Umschreibungen fuer die Anzeige rueckgaengig."""
    import sprechtext
    for alt, neu in (sprechtext.GEMESSEN + sprechtext.UNGEPRUEFT
                     + sprechtext.ZAHLEN):
        s = s.replace(neu, alt)
    return s


def bloecke(zeichen: list[tuple[str, float, float]]) -> list[dict]:
    """Teilt die Zeichenfolge in Untertitelblöcke."""
    raus, i, n = [], 0, len(zeichen)
    while i < n:
        while i < n and zeichen[i][0].isspace():
            i += 1
        if i >= n:
            break
        start = zeichen[i][1]
        # so weit gehen, wie Laenge und Standzeit es zulassen
        grenze = MAX_ZEILE * MAX_ZEILEN
        j, letzte_satz, letzte_wort = i, -1, -1
        while j < n and (j - i) < grenze and (zeichen[j][2] - start) < MAX_STAND:
            c = zeichen[j][0]
            if c in ".!?":
                letzte_satz = j
            elif c in ",;:—" or c.isspace():
                letzte_wort = j
            if c in ".!?" and (zeichen[j][2] - start) >= MIN_STAND:
                break
            j += 1
        ende_idx = (letzte_satz if letzte_satz > i
                    else letzte_wort if letzte_wort > i else min(j, n - 1))
        text = "".join(z[0] for z in zeichen[i:ende_idx + 1]).strip()
        if text:
            raus.append({"text": text, "von": start,
                         "bis": zeichen[ende_idx][2]})
        i = ende_idx + 1
    # Standzeiten glaetten: nie unter MIN_STAND, nie ueber den naechsten Beginn
    for k, b in enumerate(raus):
        naechster = raus[k + 1]["von"] if k + 1 < len(raus) else b["bis"] + 1
        b["bis"] = max(b["bis"], min(b["von"] + MIN_STAND, naechster - 0.05))
    return raus


def umbrich(t: str) -> str:
    if len(t) <= MAX_ZEILE:
        return t
    woerter, zeilen, akt = t.split(), [], ""
    for w in woerter:
        if akt and len(akt) + 1 + len(w) > MAX_ZEILE:
            zeilen.append(akt)
            akt = w
        else:
            akt = f"{akt} {w}".strip()
    if akt:
        zeilen.append(akt)
    return "\n".join(zeilen[:MAX_ZEILEN])


def zeit(s: float) -> str:
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    sek, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{sek:02d},{ms:03d}"


def main() -> None:
    b = bloecke(zeitachse())
    zeilen = []
    for k, e in enumerate(b, 1):
        zeilen.append(f"{k}\n{zeit(e['von'])} --> {zeit(e['bis'])}\n"
                      f"{umbrich(rueck_umschreibung(e['text']))}\n")
    (HIER / "untertitel.srt").write_text("\n".join(zeilen), encoding="utf-8")
    lang = [e for e in b if len(e["text"]) > MAX_ZEILE * MAX_ZEILEN]
    kurz = [e for e in b if e["bis"] - e["von"] < MIN_STAND - 0.01]
    print(f"untertitel.srt · {len(b)} Bloecke · "
          f"letzter endet {b[-1]['bis']:.1f} s")
    print(f"ueber {MAX_ZEILE * MAX_ZEILEN} Zeichen: {len(lang)} · "
          f"unter {MIN_STAND} s Standzeit: {len(kurz)}")


if __name__ == "__main__":
    main()
