# Farbtest — natürliche Farben statt Themenpaletten

> 15.08.2026. **14 Credits** (6 Motive + 1 Nachlauf). Sechs Motive aus dem
> fertigen Video 1, neu erzeugt unter der neuen Farbregel, damit sich alt und
> neu direkt vergleichen lassen. **Video 1 selbst wurde nicht angefasst.**

## Die Frage

Nach dem Wegfall des Türkis waren die drei gedämpften Themenpaletten das letzte
Element, das über alle 84 Motive hinweg band. Fallen sie auch weg — sehen die
Bilder dann noch nach **einem** Kanal aus?

## Was verglichen wurde

| Motiv | Was es abdeckt | alte Palette |
|---|---|---|
| **M08** | Moor, Somerset, Neolithikum | moor |
| **M45** | Wüste, Ägypten, Altes Reich | antike |
| **M56** | Babylon, glasierte Reliefwände | antike |
| **M67** | Anden, Inka | nord |
| **M76** | Schema, Straßenquerschnitt | antike |
| **M01** | Gegenwart, Haustür und Asphalt | nord |

Alle drei alten Paletten sind vertreten, dazu je ein Schema und eine
Gegenwartsszene.

## Befund: es hält

**Die Palette war nie das, was die Serie zusammenhielt.** In allen sechs neuen
Bildern kehren dieselben Dinge wieder, und zwar unverändert:

- gleichmäßig starke schwarze Kontur, keine Strichvariation
- vollständig flächige Füllung, harte kantige Formen
- derselbe Gesichtsbau — kleine Pupillenaugen, Pflichtbrauen, minimale Nase
- erwachsene Proportion, Kopf ~⅕
- **ein** harter flächiger Schatten je Bild, alle in einer Richtung

Das ist in M08, M56 und M01 an den Figuren direkt nachzusehen: es sind
erkennbar Leute aus derselben Bildwelt.

### Ein neues bindendes Element kam von selbst

**Der Himmel.** M08, M45, M56, M67 und M01 tragen jetzt dasselbe Blau. Die
alten Paletten waren gerade darauf angelegt, sich je Thema zu **unterscheiden**
— Moor gegen Antike gegen Nord waren drei getrennte Welten. Die natürliche
Regel gibt allen Außenszenen denselben Himmel und bindet damit an dieser Stelle
**stärker** als vorher, nicht schwächer.

### Gemessen

Sättigung im Mittel und Zahl unterscheidbarer Farbtöne, je 320 × 180:

| Motiv | Sättigung alt → neu | Farbtöne alt → neu |
|---|---|---|
| M08 Moor | 0,291 → **0,411** | 8 → **32** |
| M45 Wüste | 0,401 → 0,380 | 18 → **32** |
| M56 Babylon | 0,397 → **0,489** | 22 → 22 |
| M67 Anden | 0,198 → **0,449** | 21 → 21 |
| M76 Schema | 0,272 → 0,158 | 17 → 18 |
| M01 Gegenwart | 0,212 → 0,204 | 25 → 23 |

Der größte Sprung liegt bei den Landschaften — die Anden mehr als verdoppelt.
**M01 bewegt sich fast nicht** (0,212 → 0,204): die Gegenwartsszene war schon
vorher naturalistisch, die Palette hat ihr nie etwas genommen. M76 sinkt, weil
ein Diagramm auf ebenem Grund richtigerweise wenig Farbe trägt.

## Was zerfiel — und warum es mein Fehler war, nicht der Regel ihrer

**Die Schemabilder.** Der erste Farbsatz versprach allen 84 Prompts „the sky is
blue, foliage and grass are green". Der Straßenquerschnitt M76 holte sich das
prompt ab: blauer Himmel, Grasbüschel am Horizont — und war damit keine
Zeichnung mehr, sondern eine Ortsansicht. Dazu verlor er Inhalt: die vier
Steinlagen der linken Hälfte waren kaum noch auseinanderzuhalten, der
Kiesbelag der rechten fehlte.

Behoben durch Trennung in zwei Fassungen:

| | Raumbilder (62) | Schemabilder (22) |
|---|---|---|
| Materialien | echte Farbe | echte Farbe |
| Himmel, Vegetation | echte Farbe | **ausdrücklich keine** |
| Hintergrund | die Szene | ein ebenes Feld |

`M76-drei.png` zeigt alle drei Stände nebeneinander. Die dritte Fassung ist
**lesbarer als die ursprüngliche**: vier Steinlagen klar getrennt, Kiesbelag
wieder da.

## Dateien

| | |
|---|---|
| `M01.png` … `M76.png` | die sechs neuen Fassungen |
| `M76-mit-himmel.png` | M76 vor der Schema-Trennung, als Beleg |
| `M76-drei.png` | alt · ungetrennt · Schema-Farbsatz |
| `paar-MXX.png` | alt gegen neu in voller Größe |
| `raster-160x90.png` | alle zwölf in Briefmarkengröße |
| `vergleich.py` | erzeugt die Vergleiche und die Messung |

## Grenze dieses Tests

Sechs von 84 Motiven, ein Bild je Kulturraum, **keine Wiederholung**. Das
Modell streut; ein zweiter Lauf derselben sechs Prompts sähe anders aus. Der
Befund trägt für die Frage „hält die Serie zusammen" — er sagt nichts darüber,
wie zuverlässig ein einzelnes Motiv gerät.
