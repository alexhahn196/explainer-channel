# V2 mit Augen und Themenpalette — drei Augenentwürfe zur Wahl

> Lauf 2026-08-14. Grundlage: [`stil-uf-varianten/README.md`](../stil-uf-varianten/README.md)
> (V2-Machart) und [`stil-unknown-frequencies.md`](../stil-unknown-frequencies.md)
> (Palettenregel). **3 Figurenblätter, 8,0 Credits** — 6 geplant, ein Auftrag blieb
> hängen und wurde neu gestellt. Keine Videos, keine Renders.
>
> **Offener Punkt:** Der Auftrag bricht nach „Antike/Wueste" ab. Das dritte Thema ist
> unbekannt; die dritte Palette unten ist ein **Vorschlag von mir**, kein Auftrag.
> Auch die Ablage war nicht mehr genannt — ich habe `recherche/stil-uf-augen/` gewählt.

## Was bleibt, was sich ändert

**Unverändert aus V2** — Machart, Figurensprache, überproportionierter Kopf, flache
Flächen, klare Konturen:

```
Flat 2D vector cartoon in the style of a limited-animation explainer video.
Clean uniform anti-aliased black outlines of constant medium weight; no sketchy
lines, no hand-drawn jitter, no crosshatching. Any figure has an oversized round
head, a pill-shaped torso, thin stick limbs and simple mitten hands, no nose. The
background is noticeably more detailed than the figures: layered flat shapes with
a faint paper grain and light stipple texture. Flat colour fills, no gradients on
the figures, hard-edged shapes.
```

**Zwei Änderungen:**

1. Der Satz `a minimal face of two small solid black dot eyes` wird durch einen der
   drei Augenentwürfe unten ersetzt. Der Balkenkopf
   `ab1406ea-8d08-421e-a8b8-5d3ef88042cf` ist verworfen und wird nicht weiterverwendet.
2. Der Satz `Restricted three-colour palette - ink indigo, warm amber, off-white` fällt
   ersatzlos weg. An seine Stelle tritt eine **Themenpalette plus eine konstante
   Signalfarbe**.

---

# Die Signalfarbe: Signaltürkis `#1BBFB0`

Begründung aus der gemessenen Regel: Gedämpfte Erdtöne liegen ausnahmslos im
Farbtonbereich **20° bis 110°** (Rot–Orange–Gelb–Grün). Eine Signalfarbe, die von
*keiner* Themenpalette geschluckt wird, muss deutlich außerhalb liegen. Zusätzlich muss
sie **hell** sein: Bei 2 px Augengröße verlieren dunkle Töne ihre Farbe und werden zu
Grau, helle behalten sie.

| Kandidat | Farbton | L\* | Urteil |
|---|---:|---:|---|
| **Signaltürkis `#1BBFB0`** | **175°** | **~70** | **gewählt** |
| Bernstein `#E0A93B` (aus V2) | 38° | 74 | mitten im Erdton-Bereich — geht in jeder Wüstenpalette unter |
| Tintenindigo `#1F3A5F` (aus V2) | 213° | 25 | Farbton gut, aber zu dunkel: wird beim Verkleinern zu Grau |
| Rot `#B22222` (Lösung des Vorbilds) | 0° | 41 | funktioniert, ist aber deren Signal, nicht unseres |

Türkis liest historisch als **Patina, Fayence-Glasur, Kupferoxid** — es wirkt in einer
Geschichtsszene nicht wie ein Fremdkörper, kommt aber in keiner Erdpalette natürlich vor.

---

# Die Themenpaletten

Regel: **gedämpfte Erdtöne nach Thema, plus genau eine konstante Signalfarbe über alle
Videos.** Die Signalfarbe ist in jeder Palette dieselbe und wird sparsam gesetzt.

## 1. Urzeit / Moor — Somerset Levels, Niedersachsen

| Rolle | Hex | |
|---|---|---|
| Moorschwarz, nasses Holz | `#241C16` | dunkelster Ton, auch Konturen |
| Torfbraun | `#4A3B2A` | Kleidung, Erde |
| Nassmoos | `#5B6B4A` | Vegetation |
| Schilfocker | `#A8894E` | Reet, trockenes Gras, Leder |
| Nebelgrau über Wasser | `#B9BDB4` | Dunst, Himmel |
| Bleiches Leinen, Knochen | `#E6DFCF` | Haut, Stoff, hellste Fläche |
| **Signaltürkis** | **`#1BBFB0`** | **konstant** |

## 2. Antike / Wüste

| Rolle | Hex | |
|---|---|---|
| Tiefer Schatten | `#3A3026` | dunkelster Ton, auch Konturen |
| Terrakotta | `#A85E3C` | Gefäße, Dachziegel, Stoff |
| Verbranntes Ocker | `#8A6A2F` | Lehmziegel, Staub |
| Sand | `#D9C49A` | Boden, Wände |
| Kalkstein | `#C9BFA8` | Architektur |
| Ausgebleichtes Leinen | `#EDE4D2` | Kleidung, hellste Fläche |
| **Signaltürkis** | **`#1BBFB0`** | **konstant** |

## 3. *(Thema unbekannt — Vorschlag: Mittelalter / Nordeuropäischer Winter)*

**Das ist geraten.** Der Auftrag bricht vor dem dritten Thema ab. Sobald es feststeht,
wird diese Tabelle ersetzt.

| Rolle | Hex | |
|---|---|---|
| Nachtblau | `#26313A` | dunkelster Ton, auch Konturen |
| Waldgrün | `#3F4A38` | Vegetation, Wolle |
| Eichenholz | `#6B4F35` | Balken, Gerät |
| Gedämpftes Krapprot | `#7A3B2E` | Tuch, Akzent |
| Zinngrau | `#9AA0A2` | Metall, Winterhimmel |
| Talg, Rauch | `#DED3B8` | Licht, hellste Fläche |
| **Signaltürkis** | **`#1BBFB0`** | **konstant** |

---

# Die drei Augenentwürfe

Alle drei auf demselben Figurenblatt-Gerüst erzeugt (Front und Profil, gleiche Größe,
leerer Grund), alle in der Moor-Palette, damit die neue Palettenregel gleich mit sichtbar
ist. Dateien: `e1-tropfenauge-blatt.png`, `e2-ringauge-blatt.png`,
`e3-leuchtauge-blatt.png`, Gesamtansicht `_blaetter.png`.

## E1 — Tropfenauge

Heller Kopf, zwei große dunkle Tropfenformen, leicht nach innen gekippt, je ein kleiner
heller Glanzpunkt. Setzt allein auf **Fläche und Helligkeitskontrast**; die Signalfarbe
kommt im Gesicht nicht vor.

```
FACE: two large dark teardrop-shaped eyes in bog near-black #241C16, each about
one fifth of the head width, tilted slightly inward at the top, each carrying one
small pale catchlight dot; below them one short thin straight mouth line. Nothing
else on the face. The head is pale linen #E6DFCF.
```

## E2 — Ringauge

Heller Kopf, jedes Auge ein Ring: dicker dunkler Außenring, Iris in Signaltürkis, kleine
dunkle Pupille. Trägt die Signalfarbe **im Gesicht** und bleibt trotzdem auf einem hellen
Kopf.

```
FACE: each eye is a bold concentric ring - a thick dark #241C16 outer ring about
one quarter of the head width, filled inside with signal turquoise #1BBFB0, and a
small solid dark pupil at the very centre; the two rings sit wide apart; below them
one short thin straight mouth line. Nothing else on the face. The head is pale
linen #E6DFCF.
```

## E3 — Leuchtauge

Der ganze Kopf ist dunkel, darauf zwei große Augen in Signaltürkis mit dunkler Pupille,
Mundstrich ebenfalls türkis. Dieselbe **Struktur** wie beim Vorbild (hell auf dunkel),
aber mit unserer Farbe statt Weiß.

```
FACE: the whole head is filled bog near-black #241C16; on it sit two large glowing
signal turquoise #1BBFB0 eyes, each about one quarter of the head width, rounded,
each with a small dark pupil; below them one short thin straight mouth line in the
same turquoise. Nothing else on the face, no visible skin.
```

---

# Der Kleintest

`_kopf-kleintest.png` — Kopf auf **15 px, 25 px und 40 px** Höhe verkleinert und
ungeglättet wieder vergrößert. 15 px ist die reale Kopfgröße in einer
160×90-Feedminiatur.

| | bei 15 px | bei 25 px |
|---|---|---|
| **E1 Tropfenauge** | zwei dunkle Flecken; **die Kopfkontur verschwindet fast ganz** — eine dünne dunkle Linie auf hellem Kopf vor hellem Grund verliert ihren Kontrast | erkennbar, aber weich |
| **E2 Ringauge** | Türkis kommt durch: zwei helle Punkte mit dunklem Rand, Kopfkontur schwach | klar als Ringe lesbar |
| **E3 Leuchtauge** | **mit Abstand am stärksten**: der dunkle Kopf bleibt als geschlossene Masse stehen, die türkisen Augen sitzen hell darauf | unverkennbar |

Der Befund hinter E1s Schwäche ist allgemein und gilt für jeden Entwurf mit hellem Kopf:
**Bei 15 px trägt nicht die Augenform, sondern der Helligkeitsunterschied zwischen Kopf
und Augen — und zusätzlich der zwischen Kopf und Hintergrund.** E3 gewinnt beide
Kontraste auf einmal, E2 nur den ersten, E1 keinen von beiden zuverlässig.

**Preis von E3:** Ein durchgehend dunkler Kopf heißt kein Hautton, keine Mimik über die
Gesichtsfläche und dieselbe Grundstruktur wie beim Vorbild — hell auf dunkel. Das ist
näher am Original als E1 und E2, auch wenn die Farbe eine andere ist.

---

# Dateien

| Datei | Inhalt |
|---|---|
| `e1-tropfenauge-blatt.png` … `e3-leuchtauge-blatt.png` | die drei Figurenblätter, 2752×1536 |
| `_blaetter.png` | die drei untereinander |
| `_kopf-kleintest.png` | Kopf bei 15, 25 und 40 px, ungeglättet vergrößert |
| `_kopf-e1…e3.png` | die drei Kopfausschnitte |
| `_blaetter-160x90.png` | die drei Blätter als echte Miniaturen |

# Was offen ist

- **Das dritte Thema.** Der Auftrag bricht ab; die dritte Palette oben ist geraten.
- **Die Entscheidung.** Kein Entwurf ist gewählt — das ist ausdrücklich deine Wahl.
- **Kein Referenzelement angelegt.** Erst nach der Wahl sinnvoll, sonst wird ein
  verworfener Entwurf fixiert.
- **Nicht getestet: die Augen vor echtem Szenenhintergrund.** Das Figurenblatt steht auf
  leerem hellem Grund. Vor einem dunklen Moorhintergrund kehren sich die
  Kontrastverhältnisse teilweise um — E1 und E2 könnten dort besser dastehen als im
  Kleintest, E3 schlechter.
- **Nicht getestet: die Signalfarbe gegen die anderen zwei Paletten.** Generiert wurde
  nur die Moor-Palette.
