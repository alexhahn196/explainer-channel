#!/usr/bin/env python3
"""Zweiter Zustand eines Zustandspaars, aus dem ersten montiert.

Ein Zustandspaar ist in szenen.md definiert als „exakt dasselbe Bild, eine
Sache anders". Stapel 1 hat gezeigt, dass sich das aus Text nicht herstellen
laesst: das Modell hat den ersten Zustand nie gesehen und zeichnet ein
anderes Bild mit aehnlichen Bestandteilen (M04/M05: andere Aermelfarbe,
andere Wandfarbe, Daumen wieder auf derselben Seite; M10/M11: ein voellig
anderes Sternfeld).

Bild zu Bild kommt naeher — der Hintergrund bleibt erhalten —, zeichnet den
bewegten Gegenstand aber neu. Im ersten Versuch brach dabei die Anatomie der
Hand, im zweiten aenderte sich der Armwinkel. Beides sind sichtbare zweite
Unterschiede, und beim Schnitt liest sich das als „er hat den Arm bewegt"
statt als „der Blick hat gewechselt".

Hier wird stattdessen gerechnet. Der bewegte Gegenstand wird im ersten Bild
freigestellt, die Luecke mit dem Untergrund geschlossen und derselbe
Pixelblock an der neuen Stelle wieder eingesetzt. Ergebnis: alles ausser dem
bewegten Gegenstand ist bitgleich, und der Gegenstand ist dieselbe Zeichnung,
nicht eine zweite. Genau das verlangt die Parallaxe — das nahe Ding springt,
der ferne Hintergrund steht still.

Aufruf:  python3 zustandspaare.py
"""
from __future__ import annotations

import pathlib

import numpy as np
from PIL import Image
from scipy import ndimage

HIER = pathlib.Path(__file__).resolve().parent
BILDER = HIER / "bilder"


def _fuellen(bild: np.ndarray, maske: np.ndarray,
             frei: np.ndarray, sigma: float = 90.0) -> np.ndarray:
    """Schliesst die Luecke mit dem fortgesetzten Untergrund.

    Die Flaechen sind laut Machart flach gefuellt, tragen aber einen
    schwachen Verlauf aus dem Modell. Ein Zeilenmittel oder eine
    zeilenweise Interpolation hinterlaesst darum einen sichtbaren Fleck in
    der Form des entfernten Gegenstands — beides gemessen und verworfen.
    Hier wird der Untergrund flaechig weitergerechnet: die freien Pixel
    werden gewichtet verschmiert (normalisierte Faltung), was den Verlauf
    in beiden Richtungen fortsetzt.
    """
    f = frei.astype(np.float64)
    zaehler = np.stack([ndimage.gaussian_filter(bild[..., k] * f, sigma)
                        for k in range(3)], axis=2)
    nenner = ndimage.gaussian_filter(f, sigma)
    glatt = zaehler / np.maximum(nenner, 1e-9)[..., None]
    aus = bild.copy()
    aus[maske] = np.clip(glatt[maske].round(), 0, 255).astype(np.uint8)
    return aus


def verschieben(quelle: pathlib.Path, ziel: pathlib.Path,
                saat: tuple[int, int], links_neu: int,
                grund: np.ndarray | None = None,
                toleranz: int = 10,
                schutz: tuple[tuple[int, int], ...] = ()) -> dict:
    """Verschiebt den Gegenstand unter `saat` waagerecht nach `links_neu`.

    saat      Punkt (y, x) im Gegenstand
    links_neu neuer linker Rand des Gegenstands in Pixeln
    grund     Farbe des Untergrunds; ohne Angabe der Median des Bildes
    schutz    Punkte (y, x) in Flaechen, die zum Hintergrund gehoeren, den
              Gegenstand aber beruehren und deshalb mit ihm zusammenhaengen.
              In M04 ist das die dunklere Wandflaeche oben rechts: sie hat
              denselben Ton wie der Schlagschatten des Arms und stoesst an
              ihn, wandert aber nicht mit — sie liegt auf der Wand.
    """
    a = np.asarray(Image.open(quelle).convert("RGB")).astype(np.uint8)
    ai = a.astype(int)
    if grund is None:
        grund = np.median(ai.reshape(-1, 3), axis=0)

    nicht_grund = np.abs(ai - grund).max(axis=2) > toleranz
    beweglich = nicht_grund.copy()
    for sy, sx in schutz:
        aehnlich = np.abs(ai - ai[sy, sx]).max(axis=2) < 26
        ls, _ = ndimage.label(aehnlich)
        if ls[sy, sx] == 0:
            raise SystemExit(f"{quelle.name}: Schutzpunkt {(sy, sx)} leer")
        beweglich &= ~(ls == ls[sy, sx])

    lab, _ = ndimage.label(beweglich)
    marke = lab[saat]
    if marke == 0:
        raise SystemExit(f"{quelle.name}: unter {saat} liegt kein Gegenstand")
    ding = ndimage.binary_dilation(lab == marke, iterations=2)

    # Anker fuer die Fuellung. Nicht einfach „alles, was nicht Grundfarbe
    # ist": die Flaechen tragen einen schwachen Verlauf aus dem Modell, und
    # mit der engen Toleranz gilt der halbe Himmel als gezeichnet. Dann
    # liegen die naechsten Anker weit weg und im dunkleren Randbereich —
    # die Luecke wird zu dunkel und der entfernte Stern bleibt als Schatten
    # stehen. Anker sind darum: deutlich Gezeichnetes meiden, den bewegten
    # Gegenstand mit Rand meiden, den Verlauf mitnehmen.
    gezeichnet = np.abs(ai - grund).max(axis=2) > 40
    frei = (~ndimage.binary_dilation(gezeichnet, iterations=4)
            & ~ndimage.binary_dilation(ding, iterations=6))

    ys, xs = np.where(ding)
    d = links_neu - xs.min()
    hg = _fuellen(a, ding, frei)
    neu = hg.copy()
    passt = xs + d < a.shape[1]
    neu[ys[passt], xs[passt] + d] = a[ys[passt], xs[passt]]
    Image.fromarray(neu).save(ziel)

    gleich = (np.abs(ai - neu.astype(int)).max(axis=2) == 0)
    return {"pixel": int(ding.sum()), "verschiebung": int(d),
            "unveraendert": round(float(gleich.mean()) * 100, 1),
            "kasten": (int(xs.min()), int(xs.max()),
                       int(ys.min()), int(ys.max()))}


# Die neun Zustandspaare der Szenenliste, nach dem sortiert, was sich
# zwischen den Zustaenden aendert:
#
#   VERSCHIEBUNG — derselbe Gegenstand an anderer Stelle. Hier montiert.
#     M04/M05  Daumen vor der Wand
#     M10/M11  naher Stern vor dem Sternfeld
#     M16/M17  die zwei Sternbilder im Okular fallen zusammen
#     M46/M47  der grosse Stern wird zu einem kleinen — als Verschiebung
#              loesbar, weil das Bild schon kleine Sterne enthaelt: einer
#              davon wird kopiert, statt den grossen zu skalieren. Skalieren
#              wuerde die Strichstaerke duenner machen und die Machart
#              brechen.
#
#   AENDERUNG DES GEGENSTANDS SELBST — hier hilft die Montage nicht, und
#   sie muss auch nicht: dass der Gegenstand neu gezeichnet wird, ist bei
#   diesen vier gerade der Inhalt. Bild zu Bild haelt dabei den
#   Hintergrund, und das genuegt.
#     M24/M25  die Scheibe wird zum Punkt
#     M33/M34  die Schublade schliesst sich
#     M42/M54  zwei Sprossen der Leiter brechen
#     M48/M49  die Punktreihe wird ein durchgehender Strich
#
#   AUS TEXT GELUNGEN, nichts zu tun:
#     M07/M08  dieselbe Strasse im Winter und im Sommer
#
#   NACHTRAG 16.08.2026 — ein Zustand, der nie als Paar geführt war:
#     M42/M64  Die Szenenliste kennt nur das Paar M42/M54. M64 zeigt aber
#              DIESELBE Leiter ein drittes Mal ("dieselbe Leiter, intakt —
#              aber die zweite Sprosse von unten ist eine andere"), ohne
#              Paareintrag. Frisch erzeugt kam darum keine Leiter-als-
#              Diagramm zurueck, sondern eine perspektivisch gezeichnete
#              HOLZLEITER — genau der Fehler, der bei M42 ausdruecklich
#              behoben worden war. Drei Motive auf denselben Gegenstand,
#              zwei davon verkettet: die Verkettung muss vollstaendig sein,
#              sonst faellt der dritte heraus.
def verschmelzen(quelle: pathlib.Path, ziel: pathlib.Path,
                 a_mitte: tuple[int, int], b_mitte: tuple[int, int],
                 grund: np.ndarray | None = None,
                 toleranz: int = 10, hell_ab: int | None = None,
                 rand: int = 2) -> dict:
    """Zwei gleiche Gegenstaende werden zu einem in der Mitte zwischen ihnen.

    M16 zeigt zwei getrennte Abbilder desselben Sterns, M17 dieselben
    beiden genau uebereinander — also ein einziger Punkt. Statt einen
    neuen Punkt zu zeichnen, wandert der eine auf die Mitte und der andere
    verschwindet: dann ist der verbliebene Punkt dieselbe Zeichnung wie in
    M16, nicht eine zweite.
    """
    a = np.asarray(Image.open(quelle).convert("RGB")).astype(np.uint8)
    ai = a.astype(int)
    if grund is None:
        grund = np.median(ai.reshape(-1, 3), axis=0)
    # In M16 liegen die beiden Sternabbilder INNERHALB der dunklen
    # Okularscheibe. Gegen den Grund abgegrenzt haengen Scheibe und Sterne
    # in einer Maske zusammen, und die Maske fasst 1,5 Mio. Pixel statt
    # 700. Darum in solchen Faellen ueber die Helligkeit trennen: gesucht
    # ist das Helle im Dunklen, nicht das Nichtgrundfarbene.
    if hell_ab is not None:
        traeger = np.asarray(Image.open(quelle).convert("L")) > hell_ab
    else:
        traeger = np.abs(ai - grund).max(axis=2) > toleranz
    lab, _ = ndimage.label(traeger)

    stuecke = []
    for mitte in (a_mitte, b_mitte):
        marke = lab[mitte]
        if marke == 0:
            raise SystemExit(f"{quelle.name}: unter {mitte} liegt nichts")
        # Der Rand muss den Lichtsaum mitnehmen. In M16 ist der Stern
        # bis r=10 hell, faellt bei r=20 auf 55 und erreicht den Ton
        # der Scheibe erst bei r=55; mit zwei Pixeln Rand blieben zwei
        # blaue Ringe an den alten Stellen stehen.
        stuecke.append(ndimage.binary_dilation(lab == marke,
                                               iterations=rand))
    beide = stuecke[0] | stuecke[1]

    # Der Untergrund der Sterne ist die Okularscheibe selbst, nicht der
    # Bildgrund: Anker sind darum alle Pixel der Scheibe ausser den Sternen.
    if hell_ab is not None:
        frei = ~ndimage.binary_dilation(traeger, iterations=8)
        frei &= ndimage.binary_dilation(beide, iterations=90)
    else:
        gezeichnet = np.abs(ai - grund).max(axis=2) > 40
        frei = (~ndimage.binary_dilation(gezeichnet, iterations=4)
                & ~ndimage.binary_dilation(beide, iterations=6))
    hg = _fuellen(a, beide, frei, sigma=40.0)

    ys, xs = np.where(stuecke[0])
    dx = (a_mitte[1] + b_mitte[1]) // 2 - int(round(xs.mean()))
    dy = (a_mitte[0] + b_mitte[0]) // 2 - int(round(ys.mean()))
    neu = hg.copy()
    passt = ((xs + dx >= 0) & (xs + dx < a.shape[1])
             & (ys + dy >= 0) & (ys + dy < a.shape[0]))
    neu[ys[passt] + dy, xs[passt] + dx] = a[ys[passt], xs[passt]]
    Image.fromarray(neu).save(ziel)
    gleich = (np.abs(ai - neu.astype(int)).max(axis=2) == 0)
    return {"pixel": int(beide.sum()), "verschiebung": (int(dy), int(dx)),
            "unveraendert": round(float(gleich.mean()) * 100, 1)}


def ersetzen(quelle: pathlib.Path, ziel: pathlib.Path,
             ziel_mitte: tuple[int, int], vorlage_mitte: tuple[int, int],
             grund: np.ndarray | None = None, toleranz: int = 10) -> dict:
    """Ein Gegenstand wird durch eine Kopie eines anderen aus DEMSELBEN Bild.

    M47 verlangt, dass der grosse Stern so klein wird wie die uebrigen.
    Ihn zu verkleinern hiesse, seine Kontur mitzuverkleinern — die
    Strichstaerke waere duenner als ueberall sonst und die Machart
    gebrochen. Stattdessen wird einer der vorhandenen kleinen Sterne an
    seine Stelle kopiert: dieselbe Zeichnung, dieselbe Strichstaerke.
    """
    a = np.asarray(Image.open(quelle).convert("RGB")).astype(np.uint8)
    ai = a.astype(int)
    if grund is None:
        grund = np.median(ai.reshape(-1, 3), axis=0)
    nicht_grund = np.abs(ai - grund).max(axis=2) > toleranz
    lab, _ = ndimage.label(nicht_grund)

    weg = ndimage.binary_dilation(lab == lab[ziel_mitte], iterations=2)
    vorlage = lab == lab[vorlage_mitte]
    if lab[ziel_mitte] == 0 or lab[vorlage_mitte] == 0:
        raise SystemExit(f"{quelle.name}: Saatpunkt liegt auf dem Grund")

    gezeichnet = np.abs(ai - grund).max(axis=2) > 40
    frei = (~ndimage.binary_dilation(gezeichnet, iterations=4)
            & ~ndimage.binary_dilation(weg, iterations=6))
    neu = _fuellen(a, weg, frei)

    vy, vx = np.where(vorlage)
    dy = ziel_mitte[0] - int(round(vy.mean()))
    dx = ziel_mitte[1] - int(round(vx.mean()))
    passt = ((vx + dx >= 0) & (vx + dx < a.shape[1])
             & (vy + dy >= 0) & (vy + dy < a.shape[0]))
    neu[vy[passt] + dy, vx[passt] + dx] = a[vy[passt], vx[passt]]
    Image.fromarray(neu).save(ziel)
    gleich = (np.abs(ai - neu.astype(int)).max(axis=2) == 0)
    return {"entfernt": int(weg.sum()), "eingesetzt": int(vorlage.sum()),
            "unveraendert": round(float(gleich.mean()) * 100, 1)}


def umfaerben(quelle: pathlib.Path, ziel: pathlib.Path,
              kasten: tuple[int, int, int, int], neu_farbe: tuple[int, int, int],
              dicker: int = 6) -> dict:
    """Ein Teil des Gegenstands bekommt eine andere Farbe und ein anderes Profil.

    M64 verlangt dieselbe Leiter mit einer sichtbar anderen zweiten Sprosse
    von unten. Frisch erzeugt kam dafuer eine perspektivische Holzleiter
    zurueck. Hier bleibt es dieselbe Zeichnung: nur die Fuellung der einen
    Sprosse wechselt und ihr Balken wird etwas hoeher.
    """
    a = np.asarray(Image.open(quelle).convert("RGB")).astype(np.uint8)
    ai = a.astype(int)
    y0, y1, x0, x1 = kasten
    feld = ai[y0:y1, x0:x1]
    # Alles, was in diesem Kasten nicht Papiergrund ist, ist die Sprosse.
    grund = np.median(ai.reshape(-1, 3), axis=0)
    sprosse = np.abs(feld - grund).max(axis=2) > 30
    if dicker:
        sprosse = ndimage.binary_dilation(sprosse, iterations=dicker)
    innen = sprosse & (feld.max(axis=2) > 90)   # Fuellung, nicht die Kontur
    neu = a.copy()
    block = neu[y0:y1, x0:x1]
    block[innen] = np.array(neu_farbe, np.uint8)
    neu[y0:y1, x0:x1] = block
    Image.fromarray(neu).save(ziel)
    gleich = (np.abs(ai - neu.astype(int)).max(axis=2) == 0)
    return {"umgefaerbt": int(innen.sum()),
            "unveraendert": round(float(gleich.mean()) * 100, 1)}


PAARE = [
    # erst, zweit, Saat im Gegenstand, neuer linker Rand, Schutzflaechen
    ("M04", "M05", (750, 900), 1500, ((100, 2600),)),
    ("M10", "M11", (755, 962), 2130, ()),
]


# Die drei Ableitungen, die keine Verschiebung sind, aber trotzdem ohne
# Neuzeichnen auskommen.
SONDERFAELLE = [
    ("verschmelzen", "M16", "M17", dict(a_mitte=(767, 1272),
                                        b_mitte=(767, 1479), hell_ab=170,
                                        rand=45)),
    ("ersetzen", "M46", "M47", dict(ziel_mitte=(778, 1375),
                                    vorlage_mitte=(251, 367))),
    ("umfaerben", "M42", "M64", dict(kasten=(655, 700, 1275, 1480),
                                     neu_farbe=(96, 116, 128))),
]


def main() -> None:
    for art, erst, zweit, kw in SONDERFAELLE:
        quelle = BILDER / f"{erst}.png"
        if not quelle.exists():
            print(f"{erst}: noch nicht erzeugt, übersprungen")
            continue
        ziel = BILDER / f"{zweit}-montage.png"
        m = globals()[art](quelle, ziel, **kw)
        werte = " · ".join(f"{k} {v}" for k, v in m.items())
        print(f"{erst} → {zweit} ({art}): {werte}")

    for erst, zweit, saat, links, schutz in PAARE:
        quelle = BILDER / f"{erst}.png"
        if not quelle.exists():
            print(f"{erst}: noch nicht erzeugt, übersprungen")
            continue
        ziel = BILDER / f"{zweit}-montage.png"
        m = verschieben(quelle, ziel, saat, links, schutz=schutz)
        print(f"{erst} → {zweit}: {m['pixel']:>8} px verschoben um "
              f"{m['verschiebung']:>5} px · {m['unveraendert']:>5} % des "
              f"Bildes unverändert")


if __name__ == "__main__":
    main()
