# Stapel 1 gestoppt — 16.08.2026

> **24 Credits** (12 Motive à 2,0). 12 von 12 technisch erfolgreich, 0
> API-Fehlschläge. **3 inhaltliche Fehlschläge — der Lauf ist gestoppt.**
> Kontostand 2.579,9. Von 236 Credits der Variante C sind 24 verbraucht.

Die Abbruchregel nennt „mehr als 3 Fehlschläge". Es sind genau 3 — aber
alle drei haben eine gemeinsame Ursache, und es sind **zwei verschiedene**
davon. Beide treffen nicht diese zwölf Bilder, sondern den Plan als
Ganzes. Weiterlaufen hätte sie 66-mal wiederholt.

## Ursache 1 — Zustandspaare lassen sich nicht aus Text erzeugen

**Betrifft 9 der 66 Motive**, darunter die Kernmechanik des Videos.

Ein Zustandspaar ist definiert als „exakt dasselbe Bild, eine Sache
anders". Der Prompt für den zweiten Zustand sagt das auch wörtlich —
aber das Modell hat den ersten Zustand nie gesehen. Es erzeugt ein
*anderes* Bild mit ähnlichen Bestandteilen.

**M04 / M05, der Daumensprung.** M04: blauer Ärmel, Arm von rechts,
Daumen links vom Haken. M05: **grüner** Ärmel, Arm von **links**, andere
Wandfarbe — und der Daumen steht wieder **links** vom Haken. Der Sprung,
auf dem das halbe Video steht, findet nicht statt.

**M10 / M11, der Sternsprung.** Das Sternfeld ist ein völlig anderes.
Dazu zwei eigene Fehler in M11: die beiden Hintergrundsterne sind **dunkel
ausgefüllt** statt schwach weiß (das Modell las „fainter" als „dunkler"),
und der Ausschnitt ist als **gerahmter Bildschirm mit Fuß** gezeichnet —
„a rectangular patch of the night sky" wurde als rechteckiger Gegenstand
gelesen.

**M07 / M08 hat funktioniert** — dieselbe Straße im Winter und im
Sommer, erkennbar dieselbe Häuserzeile. Das zeigt, woran es liegt: eine
Beschreibung, die für sich stark genug ist, konvergiert von allein. Ein
Daumen an einer leeren Wand und ein Sternfeld sind es nicht.

**Der Weg, der gehen würde:** `nano_banana_2` nimmt laut Modellkatalog ein
Eingangsbild an (`medias`, Rolle `image`, Tag `image-to-image`). Der
zweite Zustand wird dann nicht neu erzeugt, sondern aus dem ersten
abgeleitet — dieselbe Datei als Vorlage, im Prompt nur die eine Änderung.
**Ungeprüft**, ob die Machart dabei erhalten bleibt.

## Ursache 2 — „Clothing" im Prompt eines Bildes ohne Menschen

**Betrifft 43 der 66 Motive.**

Jeder Prompt trägt den Epochensatz: *„Clothing, tools, architecture and
vegetation all belong to that period and place and to no other."* Er
stammt aus Video 1, wo fast jedes Bild eine Figur hatte. In dieser Fassung
haben **43 Motive keine Figur** — und der Satz nennt trotzdem Kleidung.

**M01** ist das Ergebnis: verlangt war ein Blick von unten in den
Nachthimmel, Dachkante am unteren Rand, ausdrücklich *„no people in this
picture at all"*. Zurück kam eine Straßenszene mit **zwei Personen** —
und zwar in Kleidung um 1900, mit Schubkarre und altem Fahrrad, obwohl
„a present-day residential street" dasteht.

Der Satz hat also doppelt geschadet: er hat Figuren herbeigerufen, und
mit dem Wort „Clothing" die Epoche an die Kleidung gebunden statt an die
Architektur — worauf das Modell eine historische wählte.

Das ist derselbe Mechanismus wie bei der Handschrift: **ein Wort im
Prompt, das etwas benennt, was nicht im Bild sein soll.** Nur diesmal
nicht in der Szenenbeschreibung, sondern im Anweisungsteil.

## Was in Ordnung war

M02 (Person von hinten unter Sternen, Gegenwart, Nacht liest als Nacht),
M03 (Passanten, einer zeigt nach oben), M06, M07, M08, M09, M12 — das
Parallaxendreieck kam so zurück wie im Stichprobenlauf freigegeben.
M04 und M10 sind je für sich richtig; sie scheitern nur als Paar.

## Vorschlag

1. Epochensatz nach Framing trennen: mit Figur wie bisher, ohne Figur
   nur „Architecture and vegetation belong to …" — ohne das Wort
   Kleidung.
2. Zustandspaare über Bild-zu-Bild erzeugen. Erst an **einem** Paar
   prüfen (M04 → M05, 2 Credits), ob die Machart erhalten bleibt.
3. M01 und M11 neu, mit korrigierten Prompts.

Erst danach die restlichen 54 Motive.
