# Stilvorschläge für einen englischsprachigen Erklärkanal

> **Stand 2026-08-07.** Fünf Stile × zwei feste Testszenen = 10 Standbilder.
> Keine Videoclips, keine Animation, kein Render.
> **Kosten: 20 Credits** (10 Bilder × 2 Cr., `nano_banana_2`, 16:9, 2k) —
> Preis vorab per `get_cost` bestätigt, keine Fehlschläge, kein Nachlauf nötig.

Modell und Weg nach `produktion/motive/README.md`: Higgsfield `nano_banana_2`
(die Plattform führt es als `nano_banana_flash` aus), 16:9, 2k.
**Letterbox-Kontrolle:** 9 von 10 Bildern ohne Balken, eines mit 11 px oben
(`stil-3-blaupause-szeneB`). Das ist deutlich besser als bei den
BibelTube-Nachtmotiven — die Balken scheinen an dunklen, fotorealistisch
angelegten Szenen zu hängen, nicht an grafischen.

## Warum diese fünf

Ausgewählt nach maximalem Abstand auf zwei Achsen: **Dimensionalität**
(flach → geschichtet → volumetrisch) und **Technik** (Vektor → Papier → Linie
→ Druck → fotografiertes Material). Bewusst *nicht* gewählt: Isometrische
Low-Poly-Dioramen (liegt dimensional neben Knetmasse), Redaktionelle Malerei
(technisch neben Siebdruck), Scherenschnitt (neben Papercut). Strichmännchen
waren ausgeschlossen; kein Stil zitiert einen bestehenden Kanal.

| | Stil | Achse |
|---|---|---|
| 1 | Flat-Vector, geometrisch | flach · Vektor |
| 2 | Papercut, geschichtete Papiercollage | Relief · Papier |
| 3 | Technische Blaupause auf dunklem Grund | flach · Linie |
| 4 | Retro-Siebdruck, begrenzte Palette, Korn | flach · Druck |
| 5 | Knetmasse / Claymation | volumetrisch · Material |

## Die Prompts im Wortlaut

Beide Szenen sind für alle Stile **wortgleich**; nur der Stilteil davor
wechselt. Jeder Prompt endet auf
`no text, no letters, no watermark, no logo, no signature.`

**Szene A** — `Subject: a person sitting at a desk at night, looking at a glowing phone screen, a cup beside them.`
**Szene B** — `Subject: a cutaway cross-section of a simple machine with visible gears, pipes and flowing arrows.`

| Stil | Stilteil des Prompts |
|---|---|
| 1 | `Flat vector illustration, bold geometric shapes, strictly solid colour areas with no gradients and no shading, clean hard edges, limited palette of five colours, generous empty space.` |
| 2 | `Layered papercut collage, cut paper shapes stacked in visible depth layers, soft drop shadows between layers, matte paper texture and fibrous torn edges, warm muted palette.` |
| 3 | `Technical blueprint drawing, thin precise white and cyan line work on a deep navy ground, cross-hatching, dimension lines and construction geometry, engineering draughtsman style, no fill colours.` |
| 4 | `Retro screen print poster, four ink colours only, visible halftone dots and paper grain, slight misregistration of the colour plates, flat inks, 1960s printed look.` |
| 5 | `Handmade plasticine claymation set, modelled clay figures and props with visible fingerprints and tool marks, soft studio lighting, shallow depth of field, stop-motion miniature look.` |

## Messwerte

Oberes Drittel = die Zone, in der bei unseren Thumbnails der Text sitzt.

| Stil | Szene | oberes Drittel p95 | Anteil > 140 | Gesamtmittel | Palette A≈B |
|---|---|---|---|---|---|
| Flat-Vector | A | 43,4 | 0,6 % | 48,9 | **4 %** |
| | B | 242,4 | 92,9 % | 199,6 | |
| Papercut | A | 86,1 | 0,6 % | 40,9 | **30 %** |
| | B | 216,2 | 59,1 % | 121,3 | |
| Blaupause | A | 51,8 | 2,1 % | 50,1 | **2 %** |
| | B | 92,4 | 4,0 % | 48,0 | |
| Siebdruck | A | 242,8 | 43,5 % | 139,6 | **23 %** |
| | B | 247,9 | 62,3 % | 166,9 | |
| Knetmasse | A | 82,7 | 0,5 % | 45,5 | **32 %** |
| | B | 229,6 | 62,6 % | 125,9 | |

**Die Spalte „Palette A≈B" ist mit Vorsicht zu lesen.** Sie ist die
Überschneidung der Farbhistogramme beider Szenen (160×90, 8 Stufen je Kanal).
Sie misst **Farbe, nicht Handschrift** — und beim Blaupausen-Stil, der mit
bloßem Auge die höchste Konsistenz zeigt, liefert sie mit 2 % den
niedrigsten Wert, weil Szene A einen helleren Navy-Grund hat als Szene B.
Das Zeichensystem — dünne weiße Linien, Maßlinien, Schraffuren — ist identisch,
davon sieht das Histogramm nichts. **Für die Bewertung unten zählt deshalb das
Zeichensystem, nicht diese Zahl.**

## Bewertung

### 1 — Flat-Vector

**Konsistenz: gut.** Palette (Navy, Rostrot, Creme, Senfgelb) trägt beide
Szenen sichtbar. Der Bruch liegt woanders: Szene A steht auf dunklem, Szene B
auf cremefarbenem Grund. Für einen Kanal wäre das per Vorgabe zu fixieren —
eine Zeile im Prompt, kein Stilproblem.
**Abstrakte Themen: stärkster der fünf.** Flache Vektorgrafik ist die
Muttersprache abstrakter Erklärinhalte — Pfeile, Blöcke, Diagramme brauchen
keinen Gegenstand.
**Thumbnail: nur bei dunklem Grund.** Szene A hat links eine große ruhige
Fläche (p95 43,4). Szene B ist mit 92,9 % hellen Pixeln im oberen Drittel als
Textträger unbrauchbar.
**Animierbar: am besten.** Getrennte Flächen ohne Textur, kein Korn, keine
Tiefenschärfe — das ist der Fall, den Bild-zu-Video am saubersten hält.
**Auffälligkeiten: keine.** Kein Text im Bild, Hände als Formen vereinfacht,
Flächen ruhig.

### 2 — Papercut

**Konsistenz: gut.** Beide Szenen zeigen dieselbe Technik unverkennbar —
geschichtetes Papier, ausgefranste Kanten, weiche Schlagschatten. Palette
überschneidet sich zu 30 %, der höchste belastbare Wert nach Knetmasse.
**Abstrakte Themen: schwach.** Papier braucht Gegenstände. Wirtschaft oder
Psychologie ginge nur über Metaphern, und die müsste jedes Mal jemand erfinden.
**Thumbnail: bedingt.** Szene A hat einen dunklen linken Streifen; Szene B ist
hell und randvoll.
**Animierbar: mittel.** Ebenen lassen sich parallax verschieben, aber die
Texturdichte erzeugt bei Bild-zu-Video Flimmern.
**Auffälligkeiten:** Szene B ist überladen — bei Feed-Größe ein Brei. Die
Hand am Telefon in A ist klein und vereinfacht, also unauffällig.

### 3 — Technische Blaupause

**Konsistenz: die höchste der fünf.** Beide Bilder sind ohne Zweifel
dasselbe Zeichensystem: dünne weiße und cyanfarbene Linien auf Navy, Maßlinien,
Schraffuren, Konstruktionsgeometrie. Dass die Figur in Szene A als technische
Zeichnung funktioniert, ist der eigentliche Beleg — der Stil trägt auch
Menschen, ohne zu kippen.
**Abstrakte Themen: schwach bis mittel.** Blaupause suggeriert Mechanik. Ein
Video über Inflation müsste sich als Systemdiagramm tarnen; das geht, ist aber
ein Umweg.
**Thumbnail: der einzige, bei dem BEIDE Szenen taugen.** Oberes Drittel p95
51,8 und 92,4, hell nur 2,1 % und 4,0 %. Alle anderen Stile liefern
mindestens eine unbrauchbare Szene.
**Animierbar: gut.** Linienaufbau, „sich zeichnende" Elemente und Schnitte
durch Ebenen sind die natürliche Bewegung dieses Stils.
**Auffälligkeiten:** Szene B ist sehr dicht; bei 160×90 vermutlich Rauschen.
Das eine Bild mit 11 px Restbalken.

### 4 — Retro-Siebdruck

**Konsistenz: Technik ja, Palette nein.** Halbtonraster, Papierkorn und der
leichte Plattenversatz sitzen in beiden Bildern. Aber A läuft auf Petrol und
Orange, B auf Magenta, Grün und Blau — nebeneinander im Feed wären das zwei
Kanäle. Reparierbar, indem die vier Druckfarben im Prompt festgenagelt werden.
**Abstrakte Themen: gut.** Plakatsprache kommt mit Abstraktion zurecht.
**Thumbnail: schlecht.** Beide Szenen haben ein helles oberes Drittel
(p95 242,8 und 247,9) — der einzige Stil, der bei beiden Szenen durchfällt.
**Animierbar: am schwierigsten.** Korn und Plattenversatz sind
Zufallsstrukturen; von Frame zu Frame neu gewürfelt ergeben sie Flimmern.
**Auffälligkeiten:** Szene A ist das atmosphärischste Einzelbild der ganzen
Reihe. Als Kanalstil trotzdem der riskanteste.

### 5 — Knetmasse

**Konsistenz: gut, mit dem höchsten Palettenwert (32 %).** Beide Bilder zeigen
dieselbe Materialwelt, Fingerabdrücke inklusive.
**Abstrakte Themen: der schwächste.** Alles muss als Objekt modelliert werden.
Ein Video über Zinseszins hätte nichts zu kneten.
**Thumbnail: bedingt.** A hat dunkle Zonen, B ist hell und unruhig.
**Animierbar: am schwierigsten neben Siebdruck.** Der Reiz von Stop-Motion ist
das Ruckeln von Hand — Bild-zu-Video erzeugt stattdessen flüssige Bewegung und
verliert genau das, was den Stil ausmacht.
**Auffälligkeiten:** In Szene B stehen zwei winzige Knetfiguren, die nicht
bestellt waren — der Prompt sagte nichts über Menschen. Kein Textmüll, keine
verformten Hände.

## Empfehlung

| Kriterium | Sieger |
|---|---|
| Konsistenz über Szenen | **Blaupause** |
| Abstrakte Themen | **Flat-Vector** |
| Thumbnail-Tauglichkeit | **Blaupause** (einziger mit zwei brauchbaren Szenen) |
| Animierbarkeit | **Flat-Vector** |
| Eigenständigkeit | Papercut, Knetmasse |

Es gewinnt keiner alles. **Blaupause** ist der sicherste Kanal-Stil — höchste
Wiedererkennung, dunkler Grund für Text, saubere Animationslogik — und
scheitert an abstrakten Themen. **Flat-Vector** ist das Gegenteil: trägt jedes
Thema und animiert am besten, muss aber per Vorgabe auf einen festen dunklen
Hintergrund gezwungen werden, sonst zerfällt der Kanal optisch.

Wenn der Kanal überwiegend „how X works" im wörtlichen Sinn macht — Maschinen,
Gebäude, Technik — ist Blaupause die stärkere Wahl. Sobald Wirtschaft,
Psychologie oder Gesellschaft dazukommen, ist Flat-Vector die einzige der fünf,
die nicht in Metaphernarbeit ausartet.

**Nicht getestet:** Animation. Alle Aussagen dazu sind Einschätzung aus den
Standbildern, keine Messung.
