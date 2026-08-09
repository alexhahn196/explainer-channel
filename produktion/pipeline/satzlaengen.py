#!/usr/bin/env python3
"""
satzlaengen.py - misst den laengsten "Satz" je Video.

Warum das noetig ist: Schritt 2 chunkt nur an Satzenden und bricht ab, wenn
ein einzelner Satz laenger ist als `chunk_max_zeichen`. Der Satztrenner
teilt an . ! ? — Verse, die auf ein Semikolon enden, gelten deshalb als ein
einziger langer Satz. Psalm 136 (23 Semikolon-Verse, 1827 Zeichen) hat den
V02-Lauf genau daran gestoppt.

Diese Messung faehrt denselben Trenner ueber die fertigen Skripte und meldet
je Video den laengsten Satz. Sie kostet nichts: kein TTS-Aufruf, keine
Credits, sie liest nur die von Schritt 1 erzeugten skript.json.

Aufruf:
    python3 produktion/pipeline/satzlaengen.py V1 V2 V3 V4 V5 V6 V7 V8
"""
import json
import os
import sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)

from gemeinsam import arbeit, config, pfad  # noqa: E402
from schritt2_tts import saetze_mit_offset  # noqa: E402


def messen(video):
    p = arbeit(video, "skript.json")
    if not os.path.exists(p):
        return None
    skript = json.load(open(p, encoding="utf-8"))
    volltext = " ".join(s["text"] for s in skript["segmente"])
    saetze = [s for s, _, _ in saetze_mit_offset(volltext)]
    laengen = sorted((len(s) for s in saetze), reverse=True)
    laengster = max(saetze, key=len)
    # Herkunft des laengsten Satzes: das Segment, in dem er beginnt
    herkunft, pos = None, 0
    start = volltext.index(laengster)
    for s in skript["segmente"]:
        if pos <= start < pos + len(s["text"]) + 1:
            herkunft = s.get("ref") or s.get("art")
            break
        pos += len(s["text"]) + 1
    return {
        "video": video,
        "saetze": len(saetze),
        "laengster_satz_zeichen": laengen[0],
        "zweitlaengster": laengen[1] if len(laengen) > 1 else 0,
        "top5": laengen[:5],
        "herkunft": herkunft,
        "anfang": laengster[:80],
    }


def main():
    videos = sys.argv[1:] or [f"V{n}" for n in range(1, 9)]
    grenze = int(config()["chunk_max_zeichen"])
    aus, ueber = [], []
    print(f"Grenze aus config.md: chunk_max_zeichen = {grenze}\n")
    print(f"{'Video':6s} {'Sätze':>7s} {'längster':>9s} {'zweiter':>8s}  "
          f"{'Herkunft':22s} Urteil")
    for v in videos:
        b = messen(v)
        if b is None:
            print(f"{v:6s}   — kein skript.json (Schritt 1 noch nicht gelaufen)")
            continue
        ok = b["laengster_satz_zeichen"] <= grenze
        b["passt"] = ok
        if not ok:
            ueber.append(b)
        aus.append(b)
        print(f"{v:6s} {b['saetze']:7d} {b['laengster_satz_zeichen']:9d} "
              f"{b['zweitlaengster']:8d}  {str(b['herkunft']):22s} "
              f"{'passt' if ok else 'ZU LANG'}")

    ziel = pfad("produktion", "korpus", "satzlaengen.json")
    json.dump({"grenze": grenze, "videos": aus}, open(ziel, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\ngeschrieben: {ziel}")
    if ueber:
        print(f"\n{len(ueber)} Video(s) über der Grenze:")
        for b in ueber:
            print(f"  {b['video']}: {b['laengster_satz_zeichen']} Zeichen aus "
                  f"{b['herkunft']} — {b['anfang']!r}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
