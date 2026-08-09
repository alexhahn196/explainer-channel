# Stilvarianten nach Ink Explainer — Testlauf 2026-08-08

Ableitungen aus `recherche/stil-ink-explainer.md`. Ziel: **die Technik
übernehmen, nicht den Kanal klonen.** Jede Variante ändert genau *eine* Sache
gegenüber der Stilkarte, damit der Unterschied messbar bleibt.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2` 16:9 **1k** | 1 Credit (exakt 1,5) |
| Preflight `get_cost`, `nano_banana_2` 16:9 **2k** | **2 Credits** |
| Erzeugt | 8 Bilder à 2k |
| **Verbraucht** | **16 Credits** (Kontostand 265,9 → 249,9) |
| Kein Video, kein Render | 0 zusätzliche Credits |

**Modellsubstitution:** Angefordert wurde `nano_banana_2`, die Jobs liefen unter
`nano_banana_flash`. Die Abrechnung entsprach trotzdem exakt dem Preflight
(8 × 2 = 16 Credits). Für einen späteren Produktionslauf ist zu prüfen, ob
`nano_banana_2` direkt adressierbar ist — die hier gezeigte Linienqualität
stammt von *Flash*, nicht vom angefragten Modell.

## Die zwei festen Testszenen

- **Szene A:** *a person sitting at a desk at night, looking at a glowing phone
  screen, a cup beside them* — Figur, Innenraum, Nachtlicht
- **Szene B:** *a cutaway cross-section of a simple machine with visible gears,
  pipes and flowing arrows* — Schema, Technik, keine Figur

Beide Szenen prüfen dasselbe: Hält der Stil, wenn das Motiv vom Gegenständlichen
ins Abstrakte kippt? Jeder Prompt endet mit `no text, no letters, no watermark,
no logo.`

## Was jede Variante ändert

| Variante | geänderte Größe | alles andere |
|---|---|---|
| **REF** | nichts — reine Stilkarte, dient als Kontrolle | — |
| **V1 Palette** | statt Ink Explainers 10-Farben-Bedeutungspalette **nur drei Farben**: Indigo `#1F2A5C`, Ocker `#E0A020`, Kreideweiß `#F4F1EA` | wie Stilkarte |
| **V2 Tuschefeder** | statt gleichmäßiger Kontur eine **Federlinie** mit Druckwechsel, Tintenpunkten an Ecken, gebrochenen Zügen | Palette der Stilkarte |
| **V3 Laterne** | Stilkarte **plus ein wiederkehrendes Bildelement** in jedem Bild | wie Stilkarte |

### Die drei Elementvorschläge für V3

Auftragsgemäß drei Kandidaten; **getestet wurde a)**.

**a) Die Laternenfigur** *(getestet)* — eine kleine schwarze Silhouette links
unten, von hinten gesehen, hält eine runde Laterne mit warmem Halo und blickt in
die Szene. Stellvertreter des Zuschauers. Getestet, weil sie vor gegenständlichen
*und* vor abstrakten Motiven funktioniert und das Kurzgesagt-Prinzip am
saubersten prüft: Die Handschrift entsteht durch die Figur, nicht durch einen
Filter.

**b) Das Zeitband** — ein dünner waagerechter Strich mit Teilstrichen am unteren
Bildrand, auf dem die Szene aufsitzt; eine Marke wandert von Bild zu Bild. Für
einen Geschichtskanal trägt das doppelt: Ort im Video *und* Ort in der Zeit.
Nachteil: nah an einem Rahmen, also näher am Filter als am Element.

**c) Der Messrahmen** — jede Szene steht in einem handgezogenen Rahmen mit
Eckwinkeln und kleinem Maßstabsbalken, wie eine Tafel aus einem Grabungsbericht.
Passt zum Quellenanspruch aus `nischen-kanal-2.md` („all sources cited"), ist
aber am wenigsten figürlich und damit am ehesten übersehbar.

---

## Bewertung

Vier Kriterien, Konsistenz zuerst. Farbanteile [gemessen] per Median-Cut-Quantisierung
über beide Bilder einer Variante.

| Kriterium | REF (Kontrolle) | **V1 Palette** | V2 Tuschefeder | V3 Laterne |
|---|---|---|---|---|
| **1. Konsistenz A ↔ B** | 🔴 **bricht** — A ist dunkel (`#3A2F2A` 39 % + `#4B525F` 34 %), B cremehell (`#FEFBED` 47 %). Zwei verschiedene Welten | 🟢 **stark** — beide auf demselben Off-White (A 75 %, B 65 % `#F3EFE6`/`#F4F0E9`), dieselben drei Farben, in **beiden** dieselbe dünne schwarze Bodenlinie (nicht geprompt, emergent) | 🔴 **bricht** — A zu **94 %** leere Cremefläche, B dicht gefüllt mit gesättigten Primärfarben. Nur die Linie hält | 🟡 **mittel** — Element sitzt in beiden links unten, aber A weiß, B blassblau (`#F3F7FD` 57 %) |
| **2. Trägt abstrakte Themen?** | 🟡 B beweist, dass Schemata gehen; A und B wirken aber wie zwei Kanäle | 🟢 **ja** — die Dreifarbigkeit erzwingt Bedeutungsfarbe statt Abbildung, das trägt Schema wie Szene | 🔴 A trägt fast keine Information — 94 % Leerfläche ist keine Reduktion, sondern eine leere Seite | 🟢 **ja** — ein Beobachter funktioniert vor jedem Motiv |
| **3. Bei 160×90 noch DIESER Stil?** | 🔴 nein — die zwei Miniaturen lesen nicht als ein Kanal | 🟢 **ja, am deutlichsten** — das Indigo-Ocker-Paar ist auf jeder Größe sofort da | 🔴 **nein** — Druckwechsel und Tintenpunkte verschwinden restlos; A ist als Miniatur nahezu leer | 🟢 **ja** — die schwarze Silhouette mit gelbem Halo überlebt die Verkleinerung als einziges verbindendes Merkmal |
| **4. Abstand zum Original** | ⚫ **null, per Definition** — es *ist* der Klon (als Kontrolle beabsichtigt) | 🟢 **hoch** — er fährt 10+ Bedeutungsfarben, wir drei | 🟡 groß in der Großansicht, **null im Thumbnail** | 🟡 **nur durch das Element** — nimmt man die Laterne weg, bleibt REF |
| **Urteil** | Kontrolle, keine Variante | **empfohlen** | durchgefallen | bedingt — Element ja, Ausführung noch nicht |

### Warum V2 durchgefallen ist

Zwei Gründe, einer davon methodisch:

1. **Die Federlinie überlebt die Verkleinerung nicht.** Der ganze Sinn der
   Variante — Linienqualität — ist bei 160×90 unsichtbar. Ein Merkmal, das nur
   in der Großansicht existiert, ist für einen Kanal, der über Thumbnails
   gefunden wird, wertlos.
2. **Sie ändert nicht genau eine Sache.** Szene B ist ungefragt auch in der
   Palette gekippt: statt der gedeckten Stilkartenfarben erscheinen gesättigte
   Primärtöne (Rot, Gelb, Blau, Grün nebeneinander). Damit ist der Vergleich
   verdorben — man sieht nicht mehr, was die Linie bewirkt hat und was die Farbe.

### Warum V3 nur bedingt besteht

Das Element funktioniert — es ist bei 160×90 in **beiden** Bildern erkennbar und
ist dort das einzige, was A und B verbindet. Genau das war die Hypothese.

Aber **es ist noch nicht dieselbe Figur**: In Szene A ist die Laternensilhouette
kopflastig-chibi wie die Hauptfigur, in Szene B eine realistisch proportionierte
erwachsene Gestalt. Ein Wiedererkennungselement, das seine Proportionen
zwischen zwei Bildern wechselt, ist noch kein Wiedererkennungselement. Für den
Produktionseinsatz müsste die Figur als **Referenzbild** in den Prompt gegeben
werden (`medias`), nicht als Textbeschreibung.

---

## Empfehlung

**V1 als Basis, das Element aus V3 darauf.** V1 löst die Konsistenz — das
wichtigste Kriterium — und ist als einzige Variante auf jeder Größe vom Original
unterscheidbar. V3 liefert die Handschrift, die V1 fehlt: Die Dreifarbigkeit ist
ein *Filter*, und Filter kann jeder nachbauen; die Laternenfigur ist ein
*Element*, und das ist der Kurzgesagt-Weg.

Diese Kombination ist **nicht getestet** — sie wäre der nächste Lauf (2 Bilder,
4 Credits), und die Laternenfigur müsste dabei über ein Referenzbild fixiert
werden statt über Text.

## Produktionsbefunde für die Pipeline

- **„no gradients, no shading" wird ignoriert** [gemessen, 8 von 8 Bildern].
  Trotz ausdrücklichen Verbots erzeugt das Modell weiche Verläufe: Telefonschein
  in Szene A, Zahnradschattierung und Schlagschatten in Szene B. Wer flache
  Flächen braucht, muss nachbearbeiten oder das Verbot anders formulieren.
- **„no text, no letters" wird eingehalten** [gemessen, 8 von 8]. Kein Bild
  enthält Buchstaben. Nur Symbole (Häkchen, X in REF-B) treten auf.
- **Szenentyp verschiebt den Stil stärker als der Prompt ihn hält.** In *allen*
  vier Varianten ist Szene B dichter, bunter und detailreicher als Szene A. Das
  ist die eigentliche Konsistenzgefahr für die Pipeline: nicht der Stilprompt,
  sondern der **Motivtyp**. Ein Produktionsprompt braucht eine ausdrückliche
  Dichtevorgabe (etwa „maximal sechs Bauteile, keine Detailverzahnung").
- **V1 hat eine Bodenlinie erfunden** — ein dünner schwarzer Horizontalstrich am
  unteren Bildrand, in beiden Szenen, obwohl nirgends geprompt. Ein
  brauchbarer Zufall: genau der Typ Element, den Vorschlag b) („Zeitband")
  bewusst setzen würde.

## Dateien

| Datei | Inhalt |
|---|---|
| `ref-szeneA.png`, `ref-szeneB.png` | Kontrolle nach reiner Stilkarte |
| `v1-palette-szeneA.png`, `v1-palette-szeneB.png` | V1 — Dreifarbenpalette |
| `v2-tuschefeder-szeneA.png`, `v2-tuschefeder-szeneB.png` | V2 — Federlinie |
| `v3-laterne-szeneA.png`, `v3-laterne-szeneB.png` | V3 — Laternenfigur |
| `_mini/*-160x90.png` | die acht Bilder auf Thumbnailgröße |
| `_mini/kontaktbogen-160x90.png` | alle acht Miniaturen auf einem Blatt (Zeilen: REF, V1, V2, V3) |

Alle Bilder 2752 × 1536 px (16:9).

---

## Prompts im Wortlaut

### REF — Szene A
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Human figures are simplified:
large round head, two dot eyes, one short line for a mouth, thin stick limbs,
chibi proportions, no detailed face. Thin black arrows mark movement. Muted
limited palette: brown #6B4226, dark brown #3B312B, slate grey #4B5563, light
blue #BFDBFE, deep blue #0066CC, green #22C55E, red #EF4444, orange #F97316,
yellow #FACC15, cream #FDF5E6, white #FFFFFF. Clean, high clarity. Scene: a
person sitting at a desk at night, looking at a glowing phone screen, a cup
beside them. no text, no letters, no watermark, no logo.
```

### REF — Szene B
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Thin black arrows mark
movement and flow. Muted limited palette: brown #6B4226, dark brown #3B312B,
slate grey #4B5563, light blue #BFDBFE, deep blue #0066CC, green #22C55E, red
#EF4444, orange #F97316, yellow #FACC15, cream #FDF5E6, white #FFFFFF. Clean,
high clarity, diagrammatic. Scene: a cutaway cross-section of a simple machine
with visible gears, pipes and flowing arrows. no text, no letters, no watermark,
no logo.
```

### V1 — Szene A
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Human figures are simplified:
large round head, two dot eyes, one short line for a mouth, thin stick limbs,
chibi proportions, no detailed face. Thin black arrows mark movement. STRICTLY
THREE COLOURS ONLY: deep indigo #1F2A5C, warm ochre #E0A020, chalk off-white
#F4F1EA, plus the black outlines. No other hue anywhere in the image, no blues
other than the indigo, no greens, no reds. Clean, high clarity. Scene: a person
sitting at a desk at night, looking at a glowing phone screen, a cup beside
them. no text, no letters, no watermark, no logo.
```

### V1 — Szene B
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Thin black arrows mark
movement and flow. STRICTLY THREE COLOURS ONLY: deep indigo #1F2A5C, warm ochre
#E0A020, chalk off-white #F4F1EA, plus the black outlines. No other hue anywhere
in the image, no greens, no reds. Clean, high clarity, diagrammatic. Scene: a
cutaway cross-section of a simple machine with visible gears, pipes and flowing
arrows. no text, no letters, no watermark, no logo.
```

### V2 — Szene A
```
Flat 2D explainer illustration. Every contour is drawn with a dip-pen ink nib:
strong pressure variation, thick where a stroke begins and hairline where it
lifts, small ink pools at corners and at stroke ends, occasional broken or
doubled contour line, slightly wobbly hand-inked quality. Colour fills stay
completely flat, no gradients, no shading, no hatching. Minimal symbolic
background, generous empty space. Human figures are simplified: large round
head, two dot eyes, one short line for a mouth, thin limbs, chibi proportions,
no detailed face. Thin inked arrows mark movement. Muted limited palette: brown
#6B4226, dark brown #3B312B, slate grey #4B5563, light blue #BFDBFE, deep blue
#0066CC, green #22C55E, red #EF4444, orange #F97316, yellow #FACC15, cream
#FDF5E6, white #FFFFFF. Scene: a person sitting at a desk at night, looking at a
glowing phone screen, a cup beside them. no text, no letters, no watermark, no
logo.
```

### V2 — Szene B
```
Flat 2D explainer illustration. Every contour is drawn with a dip-pen ink nib:
strong pressure variation, thick where a stroke begins and hairline where it
lifts, small ink pools at corners and at stroke ends, occasional broken or
doubled contour line, slightly wobbly hand-inked quality. Colour fills stay
completely flat, no gradients, no shading, no hatching. Minimal symbolic
background, generous empty space. Thin inked arrows mark movement and flow.
Muted limited palette: brown #6B4226, dark brown #3B312B, slate grey #4B5563,
light blue #BFDBFE, deep blue #0066CC, green #22C55E, red #EF4444, orange
#F97316, yellow #FACC15, cream #FDF5E6, white #FFFFFF. Diagrammatic. Scene: a
cutaway cross-section of a simple machine with visible gears, pipes and flowing
arrows. no text, no letters, no watermark, no logo.
```

### V3 — Szene A
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Human figures are simplified:
large round head, two dot eyes, one short line for a mouth, thin stick limbs,
chibi proportions, no detailed face. Thin black arrows mark movement. Muted
limited palette: brown #6B4226, dark brown #3B312B, slate grey #4B5563, light
blue #BFDBFE, deep blue #0066CC, green #22C55E, red #EF4444, orange #F97316,
yellow #FACC15, cream #FDF5E6, white #FFFFFF. RECURRING SIGNATURE ELEMENT: in
the lower-left corner stands a small solid black silhouette of a person seen
from behind, holding up a round lantern that glows with a warm yellow halo; the
silhouette is exactly one eighth of the image height and looks into the scene.
Scene: a person sitting at a desk at night, looking at a glowing phone screen, a
cup beside them. no text, no letters, no watermark, no logo.
```

### V3 — Szene B
```
Flat 2D explainer illustration, polished whiteboard-animation look. Uniform
medium-weight black outlines of constant thickness, no tapering, no brush
texture. Completely flat colour fills, no gradients, no shading, no rendering.
Minimal symbolic background, generous empty space. Thin black arrows mark
movement and flow. Muted limited palette: brown #6B4226, dark brown #3B312B,
slate grey #4B5563, light blue #BFDBFE, deep blue #0066CC, green #22C55E, red
#EF4444, orange #F97316, yellow #FACC15, cream #FDF5E6, white #FFFFFF. RECURRING
SIGNATURE ELEMENT: in the lower-left corner stands a small solid black
silhouette of a person seen from behind, holding up a round lantern that glows
with a warm yellow halo; the silhouette is exactly one eighth of the image
height and looks into the scene. Diagrammatic. Scene: a cutaway cross-section of
a simple machine with visible gears, pipes and flowing arrows. no text, no
letters, no watermark, no logo.
```

## Vorbehalte

- **Ein Bild je Variante und Szene.** Bildmodelle streuen; ein zweiter Lauf mit
  identischem Prompt kann anders ausfallen. Die Konsistenzurteile beruhen auf
  **je einem Paar**, nicht auf einer Serie.
- **Kein direkter Bildvergleich mit dem Original.** Kriterium 4 („Abstand zum
  Original") wurde gegen die **Stilkarte** geurteilt, nicht gegen
  nebeneinandergelegte Standbilder von Ink Explainer.
- Die Farbanteile stammen aus einer Quantisierung auf sechs Farben bei 200×112 px
  — sie messen Flächendominanz, nicht die exakte Palette.
- Die Miniaturbeurteilung erfolgte am Kontaktbogen (160×90 mit Nearest-Neighbor
  auf 320×180 vergrößert), nicht auf einem echten YouTube-Feed.
- Die Stilkarte selbst beruht auf zwei 90-Sekunden-Fenstern — siehe die
  Vorbehalte dort.
