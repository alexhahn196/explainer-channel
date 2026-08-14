# Sechs Kulturfiguren — Machart statt Gesicht, Testlauf 2026-08-14

> **Fortsetzung:** `lauf2-erwachsen/` — derselbe Auftrag mit erwachsen lesender
> Machart (Kopf ⅕ statt ⅓, kleinere Augen, Nase erlaubt, kein Glanzpunkt) plus
> einer Schlachtszene als Prüfung der Darstellungsfähigkeit. Der hier
> beschriebene Machart-Block ist damit **überholt**.

Kurskorrektur gegenüber dem Gesichtstest (N1–N6): Der Kanal hat **kein festes
Gesicht**. Das Video zeigt Menschen aus neun Kulturen, die sollen sich
unterscheiden. Zusammenhalten muss die **Machart** — Konturstärke,
Kopfproportion, Augenbauform, Zeichenduktus, flache Füllungen, keine Nase,
Mundstrich. Wie in einem Comic: alle Figuren verschieden, alle aus derselben
Feder.

**Kein Referenzbild.** Die Machart wird ausschließlich über den Prompt getragen
— das war die Bedingung des Tests. `medias` ist in allen sechs Jobs leer.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2`, 16:9, **2k** | **2 Credits** (exakt 2) |
| Erzeugt | 6 Bilder à 2k, 2752 × 1536 |
| **Verbraucht** | **12 Credits** |
| Kontostand vor dem Lauf | 2987,9 Credits (Plan ultra) |
| Fehlschläge, Nachläufe, Video, Render | keine |

**Modellsubstitution wieder aufgetreten:** angefordert `nano_banana_2`, gelaufen
sind alle sechs Jobs unter `nano_banana_flash` — wie schon in
`../stil-ink-varianten/`. Die Abrechnung entsprach dem Preflight. Das ist
insofern günstig, als N1/N2 ebenfalls auf *Flash* liefen: Der Vergleich mit dem
Gesichtstest ist damit nicht durch einen Modellwechsel verunreinigt.

## Der Machart-Block

In allen sechs Prompts **wortgleich**, vorne, vor Figur und Szene. Er ist die
Fortschreibung des N2-Blocks aus dem Gesichtstest (aus der Generierungshistorie
im Wortlaut zurückgeholt), erweitert um zwei Sätze: Linienstärke gilt
ausdrücklich auch für Hintergrund und Requisiten, und der Augenbau ist als
serienweit identisches Bauteil deklariert.

```
Flat 2D vector cartoon in the style of a limited-animation explainer video.
Clean uniform anti-aliased black outlines of constant medium weight - the same
line weight on figure, clothing, props and background alike; no sketchy lines,
no hand-drawn jitter, no crosshatching, no thick-thin variation in the outline.
Completely flat colour fills, no gradients, no shading, no rendering,
hard-edged shapes. Body build: oversized round head roughly one third of the
total body height, pill-shaped torso, thin stick limbs, simple mitten hands, no
nose. EYE BUILD, identical construction for every character in this series:
rounded white eye whites, each with one solid round dark pupil and one small
white catchlight dot in the upper left of the pupil; below the eyes one short
thin gently curved mouth line; no nose, no nostrils. Minimal symbolic
background built from a few large flat shapes, generous empty space, muted
era-appropriate colours. The whole figure is visible head to toe inside the
frame, standing on the ground line, not cropped.
```

Jeder Prompt endet mit `no text, no letters, no numbers, no watermark, no logo,
exactly one character.` (bei F4: `exactly one character and one horse.`)

**Nicht im Prompt:** Palette und Signalfarbe. Beides ist offen und wurde
bewusst nicht gesetzt — die Bilder tragen jeweils eine epochennahe gedeckte
Eigenfarbigkeit. Was hier an Farbzusammenhalt zu sehen ist, ist **nicht
gesteuert**.

## Was variiert wurde

| | Figur | Kopfform | Augen | Brauen | Haar / Bart | Alter, Geschlecht |
|---|---|---|---|---|---|---|
| **F1** | Moorbauer, Somerset, Steinzeit | breit rund | groß, ⅕ Kopfbreite, normaler Abstand | kurz, gerade, dick | schulterlang zottig, Kurzbart | mittelalt, m |
| **F2** | Ägyptische Steinträgerin, Altes Reich | länglich oval | mittel, ⅙, etwas weiter | dünn, gebogen | schwarz glatt unter Leinentuch | jung, w |
| **F3** | Babylonischer Priester, 6. Jh. v. Chr. | lang rechteckig | klein, ⅛, eng | schwer, gerade | kahl, langer Lockenbart | alt, m |
| **F4** | Persischer Reiterbote | rund-oval | groß, ⅕, weit auseinander | dünn, hoch gebogen | dunkle Locken unter Kappe, Kurzbart | jung, m |
| **F5** | Inka-Läuferin, Anden | breit rund | mittel, ⅙, weit | **keine** | zwei schwarze Zöpfe, Stirnband | jung, w |
| **F6** | Römischer Legionär | quadratisch kantig | klein, ⅐, eng | tief, gerade, dick | kurz unter Helm, rasiert | mittelalt, m |

## Befund: Sehen sie aus wie derselbe Kanal?

**Vier von sechs ja, zwei nein.** F1, F4, F5 und F6 lesen ohne Zögern als eine
Serie. F2 und F3 lesen als Gäste aus einer anderen Produktion.

### Das Bauteil, das bricht: die Kopfproportion

Das ist der eine Bruch, und er ist der schwerste, weil er auf jede Entfernung
sichtbar bleibt.

Der Machart-Block verlangt `oversized round head roughly one third of the total
body height`. Gehalten wird das bei F1, F4, F5, F6. Bei **F2** und **F3** ist
der Kopf auf etwa ein Fünftel der Körperhöhe geschrumpft, die Gliedmaßen sind
entsprechend lang — das sind erwachsen proportionierte Figuren, keine
kopflastigen. Nebeneinander gelegt (`_kontaktbogen.png`) sieht man zwei
Zeichensysteme: vier Chibis und zwei Erwachsene.

Der Auslöser ist erkennbar der Figurenblock, nicht der Machart-Block: F2 und F3
sind die beiden Figuren, deren Kopfform ich als *elongated oval* bzw. *long
narrow rectangular* beschrieben habe. Das Modell hat „länglicher Kopf" nicht als
Kopfform gelesen, sondern als **schlankere Figur insgesamt** — und die
Proportionsangabe aus dem Machart-Block überschrieben. Kopfform und
Kopfgröße sind für das Modell dasselbe Bauteil.

### Was hält

- **Konturstärke.** Über alle sechs Bilder gleich schwer, gleich gleichmäßig,
  ohne Druckwechsel — und, wie geprompt, auf Hintergrund und Requisiten
  dieselbe wie auf der Figur. Das ist die stabilste Größe im Lauf.
- **Augenbau.** Rundes weißes Auge, runde Vollpupille, ein Glanzpunkt — in
  allen sechs Gesichtern derselbe Bau. Größe und Abstand variieren wie
  bestellt, ohne dass die Bauform kippt.
- **Keine Nase.** Sechs von sechs.
- **Mundstrich.** Fünf von sechs ein dünner gebogener Strich.
- **Flache Füllungen**, große ruhige Flächen, Bodenlinie, viel Leerraum.
- **Brauen als Mimikbauteil** funktionieren: F1 und F6 wirken durch die tiefen
  geraden Brauen anders als F4 mit den hohen gebogenen. F5 ohne Brauen fällt
  nicht aus der Reihe.

### Kleinere Brüche, jeder für sich reparierbar

| Bild | Bruch | Bemerkung |
|---|---|---|
| **F3** | Augen **halb geschlossen** — ein Lidstrich schneidet das obere Auge ab, dazu hängende Brauen und ein **rechteckiger offener Mund** statt Strich | Der Gesamteindruck ist müde/traurig. Kommt vermutlich von „older man": das Modell übersetzt Alter in gesenkte Lider |
| **F2** | **Wimpern** an den Außenwinkeln, und die bestellten Brauen fehlen ganz | Das Modell tauscht Braue gegen Wimper, sobald die Figur weiblich ist — F5 hat weder noch |
| **F5** | **Wangenröte** — zwei Farbkreise, in keinem anderen Bild | Zusätzliches Bauteil, nicht bestellt |
| **F1** | Die freie Hand hat **fünf ausmodellierte Finger** statt der Fäustlingshand | Nicht verformt, aber ein anderes Bauteil. Die anderen fünf Bilder haben Fäustlinge mit Daumen |
| F2, F4, F5, F6 | **Ohren** gezeichnet, F1 und F3 nicht | Ohren sind im Machart-Block gar nicht geregelt — offenes Bauteil |
| alle | weiche **Verläufe** auf Haut, Himmel und Boden trotz `no gradients, no shading` | Derselbe Befund wie in `../stil-ink-varianten/` — das Verbot wird ignoriert |

### Das Offensichtliche, geprüft

- **Fehlende Figur:** keine. Sechs von sechs zeigen genau eine Figur, F4
  zusätzlich das bestellte Pferd.
- **Verformte Hände:** keine. Alle sechs im Prüfschnitt vergrößerten Hände
  (`_haende.png`) sind sauber gebaut. F1s Fünffingerhand ist korrekt
  gezeichnet, nur stilfremd.
- **Text im Bild:** keiner. Die Eckwinkel auf dem Legionärsschild und die
  Rosetten auf der babylonischen Ziegelwand sind Ornament, keine Zeichen.

## Was daraus für den nächsten Lauf folgt

1. **Kopfgröße von Kopfform trennen.** Die Proportion muss in den Figurenblock
   hinein und dort wiederholt werden, nicht nur im Machart-Block stehen — etwa
   „a long narrow head that is still one third of the total body height".
   Alternativ Kopfform gar nicht mehr benennen und nur über Frisur und Kinn
   unterscheiden.
2. **Lider und Wimpern ausdrücklich verbieten**, sonst kommen sie über „alt"
   und „weiblich" durch die Hintertür. Der Augenbau braucht ein
   `no eyelids, no eyelashes, eyes always fully open`.
3. **Fäustlingshand härter setzen** — `mitten hands with a thumb, never
   separate fingers`.
4. Ohren und Wangenröte entscheiden: rein ins Bauteilverzeichnis oder raus.

Ob eine feste Palette die verbleibende Streuung auffängt, ist mit diesem Lauf
**nicht beantwortet** — sie war nicht gesetzt.

## Dateien

| Datei | Inhalt |
|---|---|
| `f1-moorbauer.png` | Moorbauer, Somerset, Steinzeit |
| `f2-steintraegerin.png` | Ägyptische Steinträgerin, Altes Reich |
| `f3-priester.png` | Babylonischer Priester, 6. Jh. v. Chr. |
| `f4-reiterbote.png` | Persischer Reiterbote |
| `f5-laeuferin.png` | Inka-Läuferin, Anden |
| `f6-legionaer.png` | Römischer Legionär |
| `_kontaktbogen.png` | alle sechs nebeneinander, 3 × 2 |
| `_kontaktbogen-gesichter.png` | die sechs Köpfe auf gleiche Größe gebracht — darauf beruht das Urteil zum Augenbau |
| `_haende.png` | sechs Handausschnitte vergrößert — Prüfschnitt auf verformte Hände |

Alle Einzelbilder 2752 × 1536 px (16:9).

## Vorbehalte

- **Ein Bild je Figur.** Kein Wiederholungslauf. Ob F2 und F3 die Proportion
  systematisch brechen oder ob es ein Wurf war, ist damit nicht entschieden.
- Das Urteil ist **eine Sichtprüfung**, keine Messung — so beauftragt. Die
  Angaben „ein Drittel" und „ein Fünftel" der Körperhöhe sind Augenmaß am
  Kontaktbogen, nicht gemessen.
- **Keine Miniaturprüfung.** Ob die Machart bei 160 × 90 zusammenhält, ist hier
  nicht getestet — in den früheren Läufen war genau das der Punkt, an dem
  Varianten durchgefallen sind.
- **Keine Palette, keine Signalfarbe.** Beide Entscheidungen stehen aus; ein
  Teil des hier sichtbaren Zusammenhalts kann daran noch kippen.
- Neun Kulturen sind angekündigt, getestet sind sechs.

---

## Prompts im Wortlaut

Jeder Prompt = `<Machart-Block oben>` + `THIS CHARACTER: …` + `SCENE: …` +
Negativliste.

### F1 Moorbauer
```
THIS CHARACTER: a stocky middle-aged man with a broad round head and a warm
medium skin tone; two noticeably large eyes, each about one fifth of the head
width, set a normal distance apart; above them two short straight thick dark
brown eyebrows; untidy shoulder-length brown hair and a short brown beard. He
wears a rough animal-fur cape over a coarse undyed tunic, leather leg wraps,
bare feet, and holds a stone axe with a wooden handle in one mitten hand.
SCENE: a peat bog moor in Somerset in the Stone Age - flat bands of wet brown
peat and dull green moss, a few reed tufts, a simple line of wooden plank
trackway laid across the marsh behind him, low grey overcast sky.
```

### F2 Ägyptische Steinträgerin
```
THIS CHARACTER: a young woman with a slightly elongated oval head and a deep
warm brown skin tone; two medium-sized eyes, each about one sixth of the head
width, set a little wider apart than usual; above them two thin gently arched
dark eyebrows; straight black hair, mostly covered by a plain white linen
headcloth tied at the back. She wears a simple undyed white linen sheath dress
and is carrying a rectangular limestone block on one shoulder, both mitten
hands steadying it. SCENE: an Old Kingdom Egyptian quarry and building site -
flat sand-ochre ground, two large stacked limestone blocks, a wooden sledge, a
narrow band of Nile blue water and one palm at the far right, pale hot sky with
a plain sun disc.
```

### F3 Babylonischer Priester
```
THIS CHARACTER: an older man with a long narrow rectangular head and a light
olive skin tone; two small eyes, each about one eighth of the head width, set
close together; above them two heavy straight dark eyebrows; a long square dark
grey beard with rows of tight curls, no visible hair on the head. He wears a
long fringed woollen robe in deep madder red draped over one shoulder, and
stands upright with both mitten hands at his sides. SCENE: a temple terrace in
Babylon in the 6th century BC - a stepped ziggurat silhouette behind him, a flat
wall band of glazed deep blue brick with simple rosette shapes, a dark night sky
with a few plain star dots and a crescent moon.
```

### F4 Persischer Reiterbote
```
THIS CHARACTER: a young man with a round-oval head and a light olive skin tone;
two large eyes, each about one fifth of the head width, set noticeably wide
apart; above them two thin high arched dark eyebrows; dark curly hair showing at
the sides of a soft pointed felt cap, and a short trimmed dark beard. He wears a
knee-length belted riding tunic in dusty teal, loose trousers, soft boots and a
travel cloak, one mitten hand holding the reins of a small flat-drawn horse
standing beside him, a leather satchel at his hip. SCENE: the Persian royal road
- a broad flat dust-ochre road band running to the horizon, two low bare hill
shapes behind, a pale wide sky.
```

### F5 Inka-Läuferin
```
THIS CHARACTER: a young woman with a wide round head and a warm reddish-brown
skin tone; two medium-sized eyes, each about one sixth of the head width, set
wide apart; NO eyebrows at all; straight black hair in two braids, a narrow
woven headband across the forehead. She wears a short patterned tunic with
simple geometric bands in ochre, rust red and cream, plain sandals, and runs
forward with one leg lifted, a small pouch on her back. SCENE: a stone mountain
path in the Andes - a flat grey paved road band, stepped green agricultural
terraces on the left, two large angular snow-capped peak shapes behind, a clear
high-altitude sky.
```

### F6 Römischer Legionär
```
THIS CHARACTER: a middle-aged man with a square angular head and a pale medium
skin tone; two small eyes, each about one seventh of the head width, set close
together; above them two low straight thick dark eyebrows; cropped dark hair
just visible under the helmet, clean-shaven. He wears Roman segmented plate
armour in flat grey over a red tunic, a plain crested helmet, hobnailed sandals,
a rectangular red shield at his side held in one mitten hand and a javelin in
the other. SCENE: a Roman frontier fort - a straight flat paved road band, a
simple wooden palisade wall and one square gate tower behind him, flat green
field bands, plain daylight sky.
```
