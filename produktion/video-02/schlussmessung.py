#!/usr/bin/env python3
"""Schlussmessung ueber alle 66 Bilder von Video 2.

In config.md steht: die Serientoene gelten ab ihrer Einfuehrung, und
bereits erzeugte Bilder werden nicht blind neu gemacht, sondern am Ende
gemessen. Das ist diese Messung. Sie prueft je Gruppe, ob die Spanne
geschlossen ist, und nennt die Ausreisser.

Aufruf:  python3 schlussmessung.py
"""
from __future__ import annotations

import collections
import importlib.util
import pathlib

import numpy as np
from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
BILDER = HIER / "bilder"


def _lade(name: str, pfad: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, pfad)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


b = _lade("bildplan2", HIER / "bildplan2.py")
sp = _lade("szenenplan", HIER / "szenenplan.py")


def klein(mid: str, breite: int = 700) -> np.ndarray:
    im = Image.open(BILDER / f"{mid}.png").convert("RGB")
    return np.asarray(im.resize((breite, int(breite * im.height / im.width)))
                      ).astype(int)


def haeufigste(a: np.ndarray, maske: np.ndarray) -> tuple | None:
    px = a[maske]
    if len(px) < 300:
        return None
    zaehler = collections.Counter(map(tuple, px // 10 * 10))
    (farbe, _), = zaehler.most_common(1)
    return tuple(int(x) for x in farbe)


def gruppe(titel: str, motive, maske, grenze: int) -> list[str]:
    """Misst eine Gruppe und meldet, welche Motive aus der Spanne fallen."""
    werte = {}
    for mid in sorted(motive):
        a = klein(mid)
        farbe = haeufigste(a, maske(a))
        if farbe is not None:
            werte[mid] = farbe
    print(f"=== {titel}  ({len(werte)} von {len(motive)} messbar)")
    if len(werte) < 2:
        print("    zu wenige Messwerte\n")
        return []
    w = np.array(list(werte.values()))
    mitte = np.median(w, axis=0)
    ausreisser = []
    for mid, farbe in werte.items():
        abstand = int(np.abs(np.array(farbe) - mitte).max())
        marke = "  <-- Ausreisser" if abstand > grenze else ""
        if marke:
            ausreisser.append(f"{mid} ({abstand})")
        print(f"    {mid}: {farbe}  Abstand {abstand:>3}{marke}")
    print(f"    Median {tuple(int(x) for x in mitte)} · "
          f"Spanne R {w[:,0].min()}-{w[:,0].max()} "
          f"G {w[:,1].min()}-{w[:,1].max()} "
          f"B {w[:,2].min()}-{w[:,2].max()}")
    print()
    return ausreisser


def main() -> None:
    offen: dict[str, list[str]] = {}
    # M41 gehoert nicht in diese Gruppe, obwohl es ein Weltraummotiv ist:
    # sein Okular-Steckbrief verlangt AUSDRUECKLICH flaches dunkles
    # Neutralgrau ausserhalb des Kreises, und diese Flaeche ist groesser
    # als das Nachtblau darin. Die haeufigste dunkle Farbe ist dort also
    # das gewollte Grau. Das ist ein Messfehler, kein Bildfehler.
    offen["Dunkelgrund"] = gruppe(
        "DUNKELGRUND — Nachthimmel und Weltraum",
        b.DUNKELGRUND_MOTIVE - {"M41"},
        lambda a: a.max(axis=2) < 75, grenze=22)
    offen["Papier"] = gruppe(
        "PAPIERTON — Blatt, Seite, Platte",
        b.PAPIER_MOTIVE,
        lambda a: (a.min(axis=2) > 180) & (a.max(axis=2) - a.min(axis=2) < 45),
        grenze=22)
    offen["Messing"] = gruppe(
        "MESSINGTON — Instrumente",
        b.MESSING_MOTIVE,
        lambda a: ((a[..., 0] > 140) & (a[..., 0] - a[..., 2] > 75)
                   & (a[..., 1] - a[..., 2] > 40) & (a[..., 0] - a[..., 1] < 95)),
        grenze=35)
    offen["Leuchttisch"] = gruppe(
        "LEUCHTTISCH — Durchlicht",
        {m for m, d in sp.M.items() if d["licht"].startswith("Durchlicht:")},
        lambda a: a.mean(axis=2) > np.percentile(a.mean(axis=2), 99.0),
        grenze=22)
    offen["Wiederkehrende Figur"] = gruppe(
        "DER DAENE — Hautton",
        {"M20", "M23", "M26"},
        lambda a: ((a[..., 0] > 195) & (a[..., 0] - a[..., 2] > 52)
                   & (a[..., 0] - a[..., 2] < 115) & (a[..., 1] > a[..., 2])
                   & (a[..., 1] < a[..., 0] - 18) & (a[..., 2] > 85)),
        grenze=30)

    # Gemessen werden STERNE, nicht alles Helle. In M37 fuellt ein oranges
    # Sonnensegel ueber der blaugruenen Erdkante das halbe Bild — als
    # "helle Flaeche" gezaehlt kam das Motiv auf 81 % Farbanteil, obwohl
    # seine Sterne weisse Punkte sind. Darum nur kleine helle Flecken:
    # ein Stern ist klein, ein Satellit und eine Galaxie sind es nicht.
    from scipy import ndimage as _nd
    print("=== STERNFELDER — Anteil farbiger Sternpunkte "
          "(nur Flecken unter 3000 px)")
    for mid in sorted(b.STERNFELD_MOTIVE):
        a = np.asarray(Image.open(BILDER / f"{mid}.png").convert("RGB")
                       ).astype(int)
        hell = a.max(axis=2) > 120
        lab, n = _nd.label(hell)
        gross = np.zeros(n + 1, bool)
        for j, flaeche in enumerate(_nd.sum(hell, lab, range(1, n + 1)), 1):
            gross[j] = flaeche >= 3000
        hell &= ~gross[lab]
        px = a[hell]
        if len(px) < 50:
            print(f"    {mid}: keine Sternpunkte messbar")
            continue
        mx, mn = px.max(axis=1), px.min(axis=1)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
        anteil = float((sat > 0.25).mean()) * 100
        eigen = mid in {"M58", "M67"}   # Szene gibt eigene Farben vor
        marke = "  (Szenenfarbe)" if eigen else (
            "  <-- Ausreisser" if anteil > 15 else "")
        if marke.endswith("Ausreisser"):
            offen.setdefault("Sternfarbe", []).append(f"{mid} ({anteil:.0f} %)")
        print(f"    {mid}: {anteil:5.1f} % farbig{marke}")
    print()

    print("=== BILANZ")
    rest = {k: v for k, v in offen.items() if v}
    if not rest:
        print("    Keine Ausreisser. Alle gemessenen Gruppen sind geschlossen.")
    for k, v in rest.items():
        print(f"    {k}: {', '.join(v)}")


if __name__ == "__main__":
    main()
