# Drei Varianten des Unknown-Frequencies-Stils

> Lauf 2026-08-13. Grundlage: [`recherche/stil-unknown-frequencies.md`](../stil-unknown-frequencies.md).
> **12 Bilder, 24,0 Credits verbraucht** (Guthaben 3.105,9 → 3.081,9, gemessen).
> Keine Videos, keine Renders.

## Kosten [gemessen, `get_cost` 2026-08-13]

| Posten | Wert |
|---|---|
| `nano_banana_2`, 16:9, **1k** | 1,5 Credits/Bild |
| `nano_banana_2`, 16:9, **2k** | **2,0 Credits/Bild** |
| 12 Bilder in 2k, Vorhersage | 24,0 Credits |
| **tatsächlich abgebucht** | **24,0 Credits** |

2k gewählt, weil das Hauptmerkmal des Originals die **Linienqualität** ist
(gleichmäßig, anti-aliased, konstante Stärke) — bei 1k nicht beurteilbar.

**Abweichung, die festgehalten gehört:** Angefordert wurde `nano_banana_2`,
die Aufträge kamen als `nano_banana_flash` zurück. Der Preis blieb bei den
vorhergesagten 2,0 Credits. Ob das eine serverseitige Umleitung oder ein
Aliasname ist, ist **unbekannt** — für die Vergleichbarkeit der drei Varianten
untereinander ist es folgenlos, sie liefen alle über dasselbe Modell.

## Was die drei Varianten unterscheiden

Jede ändert **genau eine** Sache gegenüber der Stilkarte.

| | Änderung |
|---|---|
| **V1** | nichts — Stilkarte so genau wie möglich, als Referenzpunkt |
| **V2** | **nur die Palette**: Tintenindigo `#1F3A5F`, warmes Bernstein `#E0A93B`, Papierweiß `#F2EDE3` statt der Erdtöne |
| **V3** | **nur ein Zusatzelement**: ein durchgehendes Zeitleisten-Band mit Teilstrichen am unteren Bildrand |

### Das wiederkehrende Element für V3 — drei Kandidaten, einer gewählt

1. **Zeitleisten-Band am unteren Rand** — schmaler Streifen mit regelmäßigen Teilstrichen. ✅ **gewählt**
2. **Randfigur** — kleine wiederkehrende Beobachter-Silhouette am Bildrand.
3. **Papierrand mit Klebestreifen** — jede Szene als aufgepinnte Seite gerahmt.

**Begründung für (1):** Es ist das einzige, das alle vier Testszenen gleich gut
überlebt. Eine Beobachterfigur müllt die Sachszene (Maschinenschnitt) und die
Abstraktszene (Geld zwischen Händen) zu und braucht für Wiedererkennbarkeit ein
Referenzbild, das ein Textmodell nicht stabil reproduziert. Ein Rahmen frisst
Bildfläche, die bei 8–15-Minuten-Erklärvideos für Grafik gebraucht wird. Ein
Zeitstrahl kostet ~6 % Bildhöhe, ist bei 160×90 noch sichtbar und passt
inhaltlich zu einem Geschichts-Erklärkanal.

---

## Bewertung

### 1. Konsistenz über die vier Szenen — wichtigstes Kriterium [gemessen]

Streuung der Kennwerte über A/B/C/D. **Kleiner = konsistenter.**

| Variante | Palettenabstand innerhalb | Kanten SD | Objekte SD | Farbfläche SD | Sättigung SD |
|---|---:|---:|---:|---:|---:|
| V1 | 8,72 | 0,0194 | 12,0 | 0,043 | **0,015** |
| V2 | **5,32** | 0,0198 | 21,8 | **0,021** | 0,076 |
| V3 | 8,48 | **0,0166** | 13,9 | 0,035 | 0,052 |

**Zusammengefasster Schwankungsindex** (Mittel der z-Werte aller fünf Maße):

| Rang | Variante | Index |
|---|---|---:|
| 1 | **V3** | **−0,159** |
| 2 | **V1** | **+0,036** |
| 3 | V2 | +0,123 |

Kein Maß hat V3 an der Spitze — aber V3 ist bei keinem Maß Letzter. V2 ist
Erster bei Farbe und Letzter bei Objektzahl und Sättigung; V1 umgekehrt.
**V3 ist die ausgeglichenste Variante, nicht die in irgendeiner Einzeldisziplin beste.**

### 2. Trägt der Stil abstrakte Themen? [gesehen, Szene C]

| Variante | Urteil |
|---|---|
| V1 | **ja.** Zwei Figuren, dazwischen ein Bogen aus Münzen und Scheinen. Der Hintergrund bleibt aber gegenständlich (Stadt, Bäume) — die Abstraktion trägt allein der Münzbogen. |
| V2 | **ja, am deutlichsten.** Der Hintergrund wird selbst abstrakt: geschichtete Winkelflächen statt Landschaft, die Hände sind groß und grafisch. Die einzige der drei, bei der die Machart auf Abstraktion umschaltet statt sie zu dekorieren. |
| V3 | **ja.** Bogen aus Währungszeichen in Rot, Hintergrund gegenständlich wie V1. |

Alle drei tragen es. **V2 trägt es am besten** — und das ist bemerkenswert,
weil V2 nur die Palette ändern sollte: Die eingeschränkte Dreifarbigkeit zwingt
das Modell offenbar zu flächigerer, abstrakterer Komposition. Ein
unbeabsichtigter Nebeneffekt der Palettenänderung, kein geplantes Merkmal.

### 3. Bei 160×90 noch als DIESER Stil erkennbar? [gesehen, `_mini/`]

| Variante | Urteil |
|---|---|
| V1 | **ja, aber unauffällig.** Liest als „irgendein flacher Vektor-Erklärstil". Die runden hellen Köpfe tragen die Wiedererkennung, sonst nichts. |
| V2 | **ja, am stärksten.** Indigo/Bernstein ist auf einen Blick unterscheidbar, auch neben anderen Miniaturen. |
| V3 | **ja.** Der Teilstrich-Streifen bleibt als helles Band mit Struktur sichtbar und ist das einzige Element, das man in allen vier Miniaturen wiederfindet. |

### 4. Abstand zum Original [gemessen, Lab, größer = weiter weg]

| Variante | zur Videopalette | zur Thumbnailpalette |
|---|---:|---:|
| V1 | **8,20** | 12,19 |
| V3 | 9,45 | 12,88 |
| V2 | **17,14** | 15,39 |

- **V2 ist eindeutig bestanden** — mehr als doppelter Palettenabstand zu V1.
- **V3 ist bestanden, aber nicht über die Farbe.** Der Abstand 9,45 gegen 8,20
  ist zu klein, um zu zählen; unterschieden wird V3 **strukturell** durch den
  Streifen, der in allen vier Szenen sitzt.
- **V1 ist der Referenzpunkt und wird auf Unterscheidbarkeit nicht bewertet** —
  es war seine Aufgabe, nah dranzubleiben. Ein Klon ist es trotzdem nicht:
  Unknown Frequencies fährt in jedem Bild großen Bildtext, im Videoinneren
  dünnere Strichgliedmaßen und meist gar keinen Mund, und die Thumbnails
  brechen bewusst in schwer gerenderte Malerei. Nichts davon ist in V1.
  **Wer wirklich klonen wollte, müsste den Bruch nachbauen, nicht den Vektor.**

### 5. Dichteunterschied Person gegen Sache [gemessen]

Personenszenen = A (Schreibtisch) und C (Hände). Sachszenen = B (Maschine) und
D (Landschaft).

| Variante | Kanten P → S | Objekte P → S | Farbfläche P → S | Sättigung P → S |
|---|---:|---:|---:|---:|
| V1 | 0,0354 → 0,0514 = **1,45×** | 32 → 36 = 1,09× | 0,562 → 0,609 = 1,08× | 0,214 → 0,237 = 1,11× |
| V2 | 0,0485 → 0,0802 = **1,66×** | 44 → 65 = 1,48× | 0,564 → 0,573 = 1,02× | 0,351 → 0,387 = 1,10× |
| V3 | 0,0551 → 0,0827 = **1,50×** | 46 → 64 = 1,39× | 0,576 → 0,626 = 1,09× | 0,288 → 0,213 = **0,74×** |

**Der Befund aus dem letzten Lauf bestätigt sich — aber nur zur Hälfte:**

- **„Sachszenen geraten dichter" gilt in 3 von 3 Varianten**, Kantendichte
  1,45× bis 1,66×, Objektzahl bis 1,48×. Das ist ein robuster Effekt.
- **„Sachszenen geraten bunter" gilt nicht.** Farbflächenanteil bewegt sich um
  1,02–1,09×, also praktisch gar nicht; bei der Sättigung dreht V3 das
  Vorzeichen sogar um (0,74×). Was im letzten Lauf als „bunter" gelesen wurde,
  ist wahrscheinlich **dichter** gewesen — mehr Objekte auf gleicher Fläche
  wirken farbiger, ohne dass mehr Farbfläche da wäre.

### 6. Sichtbare Fehler [gesehen]

| Bild | Fehler |
|---|---|
| **V1-B** | **Die Figur fehlt komplett.** Das einzige der 12 Bilder ohne Figur — im Original trägt jedes einzelne Thumbnail eine. Ausgerechnet der Referenzpunkt verliert in der Sachszene das wichtigste Stilmerkmal. |
| **V3-D** | Die Figur driftet zu **normalen Proportionen** (Wanderer mit Rucksack von hinten), der überproportionierte Kopf ist weg. |
| **V3-A** | Kopffarbe wechselt zu **Hautton** statt des cremeweißen Kopfes der anderen drei Szenen. |
| **V3, alle** | Die **Teilung des Streifens schwankt** — Szene A grob, C und D fein (siehe `_v3-streifen-probe.png`). Das Element sitzt, seine Ausführung ist nicht stabil. |
| **V2-B** | Zwei Figuren statt einer; V1-B hatte keine. Die Figurenzahl je Szene ist über die Varianten nicht kontrolliert. |

---

## Antwort auf die Schlussfrage

**Die zwei Varianten, die am wenigsten zwischen den Szenen schwanken:**

### 1. V3 (Index −0,159) · 2. V1 (Index +0,036)

Das ist ausdrücklich **unabhängig davon, welche am besten aussieht**. Nach
Augenschein ist V2 die interessanteste — eigenständigste Handschrift, beste
Abstraktionsleistung, stärkste Erkennbarkeit bei 160×90 — und sie ist zugleich
die **unruhigste** der drei: höchste Objektzahl-Streuung (21,8 gegen 12,0) und
höchste Sättigungsstreuung (0,076 gegen 0,015).

Für einen Kanal mit alle 14 Tage einem Video über Jahre hinweg ist Konsistenz
das teurere Gut als Eigenständigkeit. Wenn eine der drei weiterverfolgt wird,
spricht die Messung für **V3** — sie hält die Machart am ruhigsten und bringt
das wiederkehrende Element mit, dessen Ausführung allerdings noch über ein
Referenzbild fixiert werden müsste, wie schon bei der Laternenfigur in
`recherche/stil-ink-varianten/`.

**Nicht entschieden.** Diese Datei misst, sie wählt nicht aus.

---

## Prompts im Wortlaut

Allen vier Szenen wurde wörtlich angehängt:
`no text, no letters, no watermark, no logo, no signature.`

### Gemeinsamer Stilblock (V1 und V3)

```
Flat 2D vector cartoon in the style of a limited-animation explainer video.
Clean uniform anti-aliased black outlines of constant medium weight; no sketchy
lines, no hand-drawn jitter, no crosshatching. Any figure has an oversized round
head, a minimal face of two small solid black dot eyes and a thin simple mouth,
no nose; a pill-shaped torso, thin stick limbs and simple mitten hands. The
background is noticeably more detailed than the figures: layered flat shapes
with a faint paper grain and light stipple texture. Muted earthy palette - olive
drab #6B704C, slate grey #708090, warm tan #94795A, pale parchment #F5F5DC, one
single deep red accent #B22222. Flat colour fills, no gradients on the figures,
hard-edged shapes.
```

### V2 — ersetzt den Palettensatz durch

```
Restricted three-colour palette - ink indigo #1F3A5F, warm amber #E0A93B,
off-white paper #F2EDE3 - plus the black outlines. No olive, no military green,
no slate grey, no brown.
```

### V3 — ergänzt den Stilblock um

```
RECURRING ELEMENT: along the entire bottom edge of the image runs a thin
horizontal measuring strip - a narrow band carrying regular small vertical tick
marks like a ruler or a timeline, drawn in the same black line weight, spanning
the full width of the image.
```

### Die vier Testszenen

```
SCENE: a person sitting at a desk at night, looking at a glowing phone screen, a cup beside them.
SCENE: a cutaway cross-section of a simple machine with gears, pipes and arrows.
SCENE: an abstract idea: money flowing between two hands.
SCENE: a wide landscape with a road going to the horizon.
```

---

## Dateien

| Datei | Inhalt |
|---|---|
| `v1-szeneA…D.png` | V1, 2752×1536 |
| `v2-szeneA…D.png` | V2, 2752×1536 |
| `v3-szeneA…D.png` | V3, 2752×1536 |
| `_kontaktbogen.png` | alle 12, 3 Zeilen × 4 Spalten |
| `_mini/*-160x90.png` | Kleintest je Bild |
| `_mini/kontaktbogen-160x90.png` | Kleintest gesamt |
| `_v3-streifen-probe.png` | unteres Fünftel aller V3-Szenen, für die Streifenprüfung |
| `_bewertung.py` | das Messskript, läuft ohne Argumente |
| `_messwerte.txt` | die Rohausgabe der Messung |
