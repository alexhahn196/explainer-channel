# Stilkonflikt Video 1 — Bildgenerierung blockiert

> Aufgenommen am 15.08.2026 beim Zusammenführen der Branches, **vor** dem
> ersten Bildauftrag. 0 Credits verbraucht.

## Der Befund in einem Satz

**Drei Dokumente nennen sich „V2" und beschreiben drei unvereinbare Macharten.**
`szenen.md` bindet alle 84 Motive an die älteste davon.

## Die drei Linien

| | Kopf | Gesicht | Palette | Referenz-Element |
|---|---|---|---|---|
| **A — Balkenkopf**<br>`stil-uf-element/` | **⅓** der Körperhöhe, überproportioniert rund | **Indigo-Balken** über der Augenregion, keine Nase | Dreifarbig fest: Indigo `#1F3A5F`, Bernstein `#E0A93B`, Papierweiß `#F2EDE3` | ja, `ab1406ea-…` |
| **B — V2 mit Augen**<br>`stil-uf-augen/` | ⅓, unverändert rund | gezeichnete **Augen** statt Balken, weiterhin **keine Nase** | Themenpalette + Signaltürkis `#1BBFB0` | **verworfen** |
| **C — Erwachsene Machart**<br>`stil-figuren/lauf2-erwachsen/` | **⅕**, nie über ¼ | **kleine Augen mit Pupille, Pflichtbrauen, Nase** | „gedämpfte epochengerechte Farben" | nein |

**A und C widersprechen sich in jedem Punkt**, der die Figur ausmacht:
Kopfproportion ⅓ gegen ⅕, Balken gegen Augen-mit-Brauen, feste Dreifarbigkeit
gegen epochengerechte Töne. **B liegt dazwischen** und verwirft ausdrücklich das
Element aus A („Der Balkenkopf `ab1406ea` ist verworfen und wird nicht
weiterverwendet"), behält aber den überproportionierten Kopf aus A.

## Zeitachse — C ist die jüngste Entscheidung

| Uhrzeit 14.08. | Dokument | Inhalt |
|---|---|---|
| 11:21 | `szenen.md` | 139 Einstellungen, 84 Motive — **alle an Linie A gebunden** |
| 12:06 | `stichprobe/` | 14 Bilder, 28 Credits — prüft **Linie A** an Video-01-Motiven, 11/11 halten |
| 14:23 | `stil-figuren/lauf2-erwachsen/` | **Linie C** als FINAL markiert |
| 15:18 | `stil-archiv.md` | erklärt **C + Z3-Lichtquelle + Signaltürkis** für verbindlich |

Das Stilarchiv ist das jüngste Dokument und deckt sich mit der Anweisung:
**Linie C plus Z3.** Damit ist die Stilfrage selbst entschieden — `szenen.md`
ist an dieser Stelle schlicht überholt.

## Was daraus folgt — und was offen bleibt

### 1. Der Stichprobenlauf ist entwertet

Die 28 Credits am 14.08. haben **Linie A** geprüft, nicht C. Für die gewählte
Machart gibt es **keine** Erprobung an Video-01-Motiven. Der Prüfpunkt nach den
ersten zehn Bildern ist damit die einzige Absicherung — und wichtiger als
geplant.

### 2. Zwei bekannte Ausfälle sind ungeklärt

Die Stichprobe fand zwei produktionsuntaugliche Ansichten in Linie A:

| Motiv | Ausfall in Linie A |
|---|---|
| **M55** Rückenansicht | Modell dreht die Figur frontal statt von hinten |
| **M62 / M29** Figur klein im Bild | zwei riesige „Geisterköpfe" am Himmel, Komposition gespiegelt |

Ob diese Ausfälle an der Machart hingen oder am Motiv, ist **nicht geprüft**.
Linie C hat eine eigene Rahmen-Härtung („no second figure, no mirrored
duplicate"), die genau auf den zweiten Fall zielt — sie könnte ihn beheben.
Beide Motive gehören in die ersten zehn Bilder.

### 3. Die Spalte `Elem` in `szenen.md` wird gegenstandslos

Sie markiert, wo das Balkenkopf-Element eingebettet werden muss. Ohne Linie A
hat sie keine Funktion mehr. Die betroffenen Motive brauchen stattdessen eine
Figurenbeschreibung nach dem `THIS CHARACTER:`-Schema aus Linie C.

### 4. Offene Frage: welche Palette?

Hier reicht das Archiv nicht aus.

- `szenen.md` schreibt die feste Dreifarbigkeit aus Linie A vor.
- `stil-archiv.md` nennt „Signalfarbe Türkis `#1BBFB0`, drei Themenpaletten".
- Der Machart-Block aus Linie C sagt nur „gedämpfte epochengerechte Farben" und
  nennt **keine** Signalfarbe.
- Die drei Themenpaletten sind in `stil-uf-augen/` definiert — Moor, Antike/Wüste
  und eine dritte, zu der das Dokument selbst schreibt: **„die dritte Palette
  oben ist geraten"**, kein Auftrag.
- **Nicht getestet:** die Signalfarbe gegen zwei der drei Paletten. Generiert
  wurde nur die Moor-Palette — und zwar in Linie B, nicht in C.

Video 1 spannt neun Kulturen von Somerset über Ägypten und Babylon bis zu den
Anden. Drei Paletten decken das nicht offensichtlich ab, und welche Epoche
welche bekommt, steht nirgends.

### 5. Die Lichtquelle fehlt in `szenen.md` fast vollständig

Z3 verlangt genau eine sichtbare Quelle je Bild mit harten flächigen Schatten in
einer Richtung. In `szenen.md`: **0 Treffer für „Schatten", 1 für „Sonne"**. Die
Lichtquelle ist also für praktisch alle 84 Motive zu ergänzen — machbar, aber es
ist eine inhaltliche Festlegung je Motiv (Richtung, Tageszeit, innen/außen), die
den Bildeindruck bestimmt.

## Was ich brauche, um weiterzumachen

Die Stilfrage ist entschieden (Linie C + Z3). Blockierend ist allein die
**Farbfrage** — sie steht in jedem der 84 Prompts und lässt sich nicht
nachträglich ändern, ohne alle Bilder neu zu erzeugen.
