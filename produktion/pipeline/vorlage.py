#!/usr/bin/env python3
"""
vorlage.py - liest einen Video-Block aus produktion/videos-01-08.md.

Die Markdown-Datei bleibt damit die einzige Quelle fuer Titel, Gebet, Hook,
CTA, Thumbnail-Vorgabe, Beschreibung und Tags. Kein zweiter Satz derselben
Texte in einer JSON-Datei, der auseinanderlaufen kann.

Aufruf zur Kontrolle:
    python3 produktion/pipeline/vorlage.py          # alle 8 Bloecke pruefen
    python3 produktion/pipeline/vorlage.py V1       # einen Block ausgeben
"""
import json
import os
import re
import sys

from gemeinsam import pfad

QUELLE = pfad("produktion", "videos-01-08.md")


def _zitat(zeilen):
    """Blockzitat (> ...) zu Absaetzen zusammenfassen.

    Leerzeilen vor dem Zitat werden uebersprungen; die erste Zeile, die
    weder leer noch Zitat ist, beendet den Block.
    """
    absaetze, akt = [], []
    begonnen = False
    for z in zeilen:
        if not z.startswith(">"):
            if begonnen and z.strip():
                break
            if not z.strip():
                continue
            break
        begonnen = True
        inhalt = z[1:].strip()
        if inhalt:
            akt.append(inhalt)
        elif akt:
            absaetze.append(" ".join(akt))
            akt = []
    if akt:
        absaetze.append(" ".join(akt))
    return absaetze


def _entkerne(s):
    """Typografische Anfuehrungszeichen und Markdown-Reste entfernen."""
    s = s.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"^[„“\"']+|[”“\"']+$", "", s.strip())
    return s.strip()


def bloecke(quelle=QUELLE):
    txt = open(quelle, encoding="utf-8").read()
    teile = re.split(r"^# Video (\d\d)\s*$", txt, flags=re.M)
    aus = {}
    for i in range(1, len(teile), 2):
        aus[f"V{int(teile[i])}"] = teile[i + 1]
    return aus


def lies(video, quelle=QUELLE):
    roh = bloecke(quelle).get(video)
    if roh is None:
        raise SystemExit(f"Block {video} nicht in {quelle}")
    zeilen = roh.splitlines()
    d = {"video": video}

    m = re.search(r"\*\*Titel:\*\*\s*`(.+?)`", roh)
    d["titel"] = m.group(1) if m else None

    m = re.search(r"\*\*Textkorpus:\*\*\s*(.+)", roh)
    d["korpus_text"] = m.group(1).strip() if m else None

    m = re.search(r"\*\*Gemessen:\*\*\s*([\d.]+)\s*Wörter", roh)
    d["woerter_soll"] = int(m.group(1).replace(".", "")) if m else None

    m = re.search(r"\*\*Eigennamen-Test:\*\*\s*(.+)", roh)
    d["eigennamen_test"] = m.group(1).strip() if m else None

    # --- Abschnitte einsammeln -------------------------------------
    absch, name = {}, None
    for z in zeilen:
        if z.startswith("### "):
            name = z[4:].strip()
            absch[name] = []
        elif name:
            absch[name].append(z)

    gebet = next((v for k, v in absch.items() if k.startswith("Eingangsgebet")), [])
    d["gebet"] = _zitat(gebet)

    # --- Hook: Varianten (a) und (b) -------------------------------
    hook = absch.get("Hook", [])
    d["hook"] = {}
    d["hook_empfohlen"] = None
    akt = None
    puffer = []
    for z in hook + ["**(ende)**"]:
        m = re.match(r"\*\*\((a|b)\)", z.strip())
        if m or z.strip().startswith("**(ende)"):
            if akt:
                d["hook"][akt] = _zitat(puffer)
            puffer = []
            akt = m.group(1) if m else None
            if m and "verwenden" in z:
                d["hook_empfohlen"] = akt
        elif akt is not None:
            puffer.append(z)

    # --- CTA -------------------------------------------------------
    cta_roh = next((v for k, v in absch.items() if k.startswith("CTA")), [])
    d["cta"] = []
    akt = None
    for z in cta_roh:
        m = re.match(r"^\s*(\d)\.\s+(.*)$", z)
        if m:
            if akt:
                d["cta"].append(_entkerne(akt))
            akt = m.group(2)
        elif akt is not None and z.strip() and not z.startswith(("#", "**")):
            akt += " " + z.strip()
        elif akt and not z.strip():
            d["cta"].append(_entkerne(akt))
            akt = None
    if akt:
        d["cta"].append(_entkerne(akt))

    # --- Thumbnail -------------------------------------------------
    tn = absch.get("Thumbnail", [])
    tntxt = "\n".join(tn)
    m = re.search(r"\*\*Motiv:\*\*\s*(.+?)(?=\n\*\*|\Z)", tntxt, re.S)
    d["thumb_motiv"] = " ".join(m.group(1).split()) if m else None
    m = re.search(r"\*\*Text:\*\*\s*`(.+?)`", tntxt)
    d["thumb_text"] = m.group(1) if m else None

    # --- Beschreibung ----------------------------------------------
    besch = absch.get("Beschreibung", [])
    m = re.search(r"```\n(.*?)```", "\n".join(besch), re.S)
    d["beschreibung"] = m.group(1).rstrip() if m else None

    # --- Tags ------------------------------------------------------
    m = re.search(r"\*\*Tags:\*\*\s*((?:.|\n)*?)(?:\n\s*\n|\n---)", roh)
    d["tags"] = re.findall(r"`([^`]+)`", m.group(1)) if m else []

    return d


def pruefe(d):
    """Meldet fehlende Pflichtteile. Leere Liste = in Ordnung."""
    fehlt = []
    for feld in ("titel", "korpus_text", "woerter_soll", "beschreibung",
                 "thumb_motiv", "thumb_text"):
        if not d.get(feld):
            fehlt.append(feld)
    if not d["gebet"]:
        fehlt.append("gebet")
    if "a" not in d["hook"] or not d["hook"]["a"]:
        fehlt.append("hook a")
    if "b" not in d["hook"] or not d["hook"]["b"]:
        fehlt.append("hook b")
    if len(d["cta"]) != 2:
        fehlt.append(f"cta (gefunden {len(d['cta'])}, erwartet 2)")
    if len(d["tags"]) < 5:
        fehlt.append(f"tags (nur {len(d['tags'])})")
    return fehlt


def main():
    if len(sys.argv) > 1:
        d = lies(sys.argv[1])
        print(json.dumps(d, ensure_ascii=False, indent=1))
        f = pruefe(d)
        print("\nFEHLT:", f if f else "nichts")
        return 1 if f else 0
    schlecht = 0
    for v in [f"V{i}" for i in range(1, 9)]:
        d = lies(v)
        f = pruefe(d)
        schlecht += 1 if f else 0
        gw = sum(len(a.split()) for a in d["gebet"])
        print(f"{v}  Gebet {gw:>3} W · Hook a/b {len(d['hook'].get('a', []))}/"
              f"{len(d['hook'].get('b', []))} · CTA {len(d['cta'])} · "
              f"Tags {len(d['tags'])} · {'OK' if not f else 'FEHLT: ' + ', '.join(f)}")
        print(f"     {d['titel']}")
    return 1 if schlecht else 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
