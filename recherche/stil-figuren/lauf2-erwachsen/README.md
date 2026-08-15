# Machart Kanal 2 — FINAL, Stand 2026-08-14

> **Der Machart-Block in diesem Dokument ist verbindlich.** Er gilt ab sofort
> für alle Figurenbilder von Kanal 2. Vorgänger: `../README.md` (Lauf 1,
> kindliche Proportion, **überholt**).

Fortschreibung von `../README.md`. Drei Aufträge, in dieser Reihenfolge
abgearbeitet:

1. **Die Machart darf nicht kindlich lesen.** Begründung ist geschäftlich, nicht
   ästhetisch: Chibi-Optik (großer Kopf, große runde Augen, keine Nase) erhöht
   das Risiko, dass YouTube den Kanal als „für Kinder gemacht" einstuft — das
   kostet personalisierte Werbung, Kommentare und RPM.
2. **Darstellungsfähigkeit prüfen.** Historische Themen verlangen Kampf,
   Verletzung, Tod. Trägt die Machart das, oder wird es unfreiwillig komisch?
   Dafür ein siebtes Bild: antike Schlachtszene, ernst und dokumentarisch.
3. **Vier Prompt-Härtungen** gegen die im Lauf beobachteten Ausfälle, geprüft an
   einem Nachlauf der zwei fehlerhaften Bilder.

Orientierung: *Unknown Frequencies* — flach und stilisiert, liest trotzdem
erwachsen.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2`, 16:9, **2k** | **2 Credits** |
| Hauptlauf | 7 Bilder = **14 Credits** |
| Nachlauf E3 + E6 mit Härtungen | 2 Bilder = **4 Credits** |
| **Summe dieses Dokuments** | **18 Credits** |
| Kontostand vor dem Hauptlauf | 2975,9 Credits |
| Fehlschläge | keine |

Modellsubstitution zum dritten und vierten Mal: angefordert `nano_banana_2`,
gelaufen unter `nano_banana_flash`. Abrechnung jeweils wie im Preflight.

---

## Der verbindliche Machart-Block

Steht am Anfang **jedes** Prompts, wortgleich. Danach folgen `THIS CHARACTER: …`
und `SCENE: …`, am Ende die Negativliste.

```
Flat 2D vector illustration in the style of a serious documentary explainer
video made for adults. Clean uniform anti-aliased black outlines of constant
medium weight - the same line weight on figures, clothing, props and background
alike; no sketchy lines, no hand-drawn jitter, no crosshatching, no thick-thin
variation in the outline. Completely flat colour fills, no gradients, no
shading, no rendering; hard-edged angular shapes with straight edges and clear
corners rather than soft rounded blobs. ADULT PROPORTIONS - the most important
rule: the head is about one fifth of the total body height and never larger than
one quarter; these are grown adults, not children, not chibi mascots, not cute
cartoon toys; shoulders clearly wider than the head, a visible neck, a defined
angular jaw, long straight limbs, simple flat hands with a thumb and a hint of
finger separation. Both arms are visible and attached to the body, and the hand
that holds or carries an object is drawn. Any description of head shape refers
to the outline of the skull only and never changes this head-to-body proportion.
FACE BUILD, identical construction for every character in this series: small
eyes, each about one tenth of the head width, a rounded white eye shape with one
solid dark pupil, fully open, no catchlight highlight, no eyelashes, no
half-closed lids, no wide staring doll eyes; EYEBROWS ARE MANDATORY on every
character, male and female alike - two clearly drawn brows sit above the eyes,
never omitted, never replaced by eyelashes; only their shape and weight vary,
and they carry the expression; a minimal nose indicated by one short straight
line or a small flat shadow shape; below it one short thin straight mouth line;
no cheek blush, no baby face. Minimal symbolic background built from a few large
flat shapes and generous empty space. FRAMING: a
single person, alone in the frame, full body visible, not cropped - head, both
hands and both feet inside the picture, no second figure, no mirrored duplicate.
Sober, restrained, documentary - never cute.
```

Negativliste am Prompt-Ende:

```
no text, no letters, no numbers, no watermark, no logo, exactly one person in the picture.
```

### Die einzige Stelle, die ausgetauscht werden darf

Der `FRAMING:`-Satz gilt für **Einzelfigurenbilder**. Bei Szenen mit mehreren
Figuren (Schlacht, Markt, Werkstatt) wird genau dieser Satz ersetzt durch:

```
FRAMING: figures are shown in full, not cropped at the edge of the frame.
```

Alles andere bleibt unverändert — auch bei Mehrfigurenszenen.

### Die vier Härtungen, die drinstehen

| # | Härtung | Wortlaut im Block | Grund |
|---|---|---|---|
| 1 | **Brauen sind Pflicht**, auch bei weiblichen Figuren; variabel ist nur die Form | `EYEBROWS ARE MANDATORY on every character, male and female alike … never replaced by eyelashes; only their shape and weight vary` | E5 wirkte ohne Brauen als einzige noch jugendlich; E2 hat die Brauen in zwei Läufen gegen Wimpern getauscht |
| 2 | **Brauen vor der Frisur** im Figurenblock nennen | im Figurenblock: erst Augen, dann `above them two … eyebrows`, **dann** Haar/Bart | zweimal derselbe Ausfall bei der weiblichen Figur mit Kopftuch |
| 3 | **Einzelfigur und Vollbild** | `FRAMING: a single person, alone in the frame, full body visible, not cropped - head, both hands and both feet inside the picture, no second figure, no mirrored duplicate` | E3 zeigte zwei Priester, beide unten angeschnitten |
| 4 | **Beide Arme sichtbar und angesetzt** | `Both arms are visible and attached to the body, and the hand that holds or carries an object is drawn` | E6 fehlte der Schildarm |

**Damit ist das Bauteil „Brauen ja/nein" aus dem Variationskatalog gestrichen.**
Es bleiben: Augengröße und -abstand, Brauenform, Kopfform (nur Schädelumriss),
Hautton, Haar, Bart, Alter, Geschlecht, Kleidung.

---

## Befund 1: Liest es erwachsen?

**Ja, bei sechs von sieben.** Der Proportionsbruch aus Lauf 1 ist weg: alle
Figuren stehen im selben Maßsystem, Kopf grob ein Sechstel der Körperhöhe,
Schultern breiter als der Kopf, Hals sichtbar. Nase in sieben von sieben. Keine
Wangenröte, keine Wimpern, keine Glanzpunkte.

Der stärkste Einzeleffekt kommt nicht von der Proportion, sondern von
**Augengröße plus Nase**: E1 Moorbauer und E6 Legionär sind dieselbe Figur in
derselben Szene wie in Lauf 1, geändert wurden im Gesicht nur diese beiden
Größen — und sie lesen jetzt als erwachsene Männer statt als Maskottchen.

**Die Ausnahme ist E5, die Inka-Läuferin.** Sie wirkt als einzige noch
jugendlich: größere Augen, rundes glattes Gesicht. Der Grund ist das Bauteil
„keine Brauen" — ohne Brauen fehlt der kantige obere Gesichtsabschluss, und das
Modell füllt die Lücke mit größeren Augen. Brauenlos und erwachsen schließen
sich in dieser Machart aus. Genau daraus folgt Härtung 1.

> **Achtung, offener Punkt:** `e5-laeuferin.png` stammt aus dem Hauptlauf und ist
> **nicht** nach dem finalen Block gebaut — die Figur hat keine Brauen, was der
> Block jetzt verbietet. Das Bild bleibt als Beleg für den Befund liegen, ist
> aber **kein gültiges Stilmuster**. Ein Nachlauf mit dem finalen Block kostet
> 2 Credits und ist nicht ausgeführt.

**Wichtige Einschränkung zum Geschäftsrisiko:** „Made for Kids" hängt nicht am
Zeichenstil allein, sondern an Thema, Titel, Thumbnail, Sprache und
Kanaleinstellung zusammen. Dieser Lauf senkt ein Signal, er räumt das Risiko
nicht ab.

## Befund 2: Trägt die Machart Kampf, Verletzung, Tod?

**Ja.** `e7-schlacht.png` wirkt an keiner Stelle unfreiwillig komisch.

Was den Ernst trägt:

- **Die Gesichter.** Kleine Augen, gerade Brauen, gerader Mundstrich — die
  Legionäre und die keltischen Krieger schauen grimmig und angespannt. Mit den
  Lauf-1-Augen (⅕ Kopfbreite, Glanzpunkt) wäre genau das gekippt: große
  glänzende Augen über einer Schildlinie lesen als Spielzeugsoldaten.
- **Der Gefallene** liegt still auf dem Rücken, Kopf zur Seite, Augen als zwei
  geschlossene Striche, Arm ausgestreckt, Schild flach daneben. Er wird nicht
  ausgestellt, er liegt einfach da — Bildsprache einer Museumstafel, nicht die
  eines Comics.
- **Der Verwundete** sitzt am Boden, Kopf gesenkt, Hand auf der Seite, ein
  dunkelroter Fleck auf der Tunika und einer am Oberarm. Kein Spritzer, keine
  Wunde im Detail, kein Schrei. Das reicht zum Erzählen und bleibt unterhalb
  dessen, was eine Altersfreigabe auslöst.
- **Kein Effektvokabular:** keine Bewegungslinien, kein Feuer, keine Heldenpose.

Was auffällt, aber den Ernst nicht bricht: Die Speere der zweiten Reihe liegen
kompositorisch quer über den Schilden und wirken teils angesetzt statt gehalten.
Kompositionsfehler, kein Stilproblem.

**Die eigentliche Frage ist damit beantwortet:** Die Machart trägt schwierige
Inhalte, seit die Augen klein und die Nase da ist. In Lauf 1 trug sie sie nicht.

## Befund 3: Haben die Härtungen gewirkt?

Nachlauf mit denselben zwei Figurenblöcken, nur der gehärtete Block davor.
**Beide Fehler sind weg:**

| Bild | vorher | nach der Härtung |
|---|---|---|
| **E3 Priester** | zwei Figuren, beide unten angeschnitten | **eine** Figur, ganzer Körper im Bild, beide Füße und beide Hände sichtbar, Brauen vorhanden |
| **E6 Legionär** | rechter Arm fehlte, Schild schwebte frei | **beide Arme angesetzt und gezeichnet**, linke Hand am Schildrand, rechte Hand am Speerschaft |

Die verworfenen Fassungen liegen als `_verworfen-*.png` im Ordner, damit der
Vergleich nachvollziehbar bleibt.

**Zwei Reste, die die Härtungen nicht erfassen** — beide im Rahmen, aber
benannt:

- **E3s Mund** ist wieder eine rechteckige Form im Bart statt eines dünnen
  Strichs. Der Bart scheint den Mundstrich zu verdrängen; das passiert jetzt
  zweimal bei derselben Figur.
- **Untere Lidstriche** treten bei E3 und E6 auf. Der Block verbietet
  *halbgeschlossene* Lider, nicht Lidlinien — die Augen sind offen, die Figuren
  wirken älter, nicht müde. Das ist hinnehmbar; wer es weghaben will, muss
  `no lower eyelid lines` ergänzen.
- **E6s linke Hand** liegt auf dem Schildrand statt an einem Griff. Arm und Hand
  sind da, die Härtung hat also geliefert, was sie sollte.

## Das Offensichtliche, geprüft (finaler Satz)

| Prüfpunkt | Befund |
|---|---|
| Falsche Figurenzahl | keine. Sieben von sieben zeigen die bestellte Figurenzahl |
| Fehlende Gliedmaßen | keine |
| Verformte Hände | keine. Die Hände tragen angedeutete Finger, auch im Schlachtbild |
| Anschnitt | keiner. Alle Einzelfiguren stehen vollständig im Bild |
| Text im Bild | keiner. Schildmotive und Wandrosetten sind Ornament |
| Sonstiges | weiche Verläufe trotz `no gradients` — vierter Lauf mit demselben Befund. Wer flache Flächen zwingend braucht, muss nachbearbeiten |

## Dateien

| Datei | Inhalt |
|---|---|
| `e1-moorbauer.png` … `e6-legionaer.png` | die sechs Figuren; **E3 und E6 aus dem gehärteten Nachlauf** |
| `e7-schlacht.png` | Testszene: antike Schlacht, dokumentarisch |
| `_kontaktbogen.png` | alle sieben nebeneinander (mit den neuen E3, E6) |
| `_kontaktbogen-gesichter.png` | sieben Köpfe auf gleiche Größe (bei E7 der Verwundete) |
| `_detail-e7-gefallener.png`, `_detail-e7-verwundeter.png` | Belege zur Darstellungsfähigkeit |
| `_verworfen-e3-doppelfigur.png` | E3 vor der Härtung: zwei Figuren, angeschnitten |
| `_verworfen-e6-ohne-arm.png` | E6 vor der Härtung: fehlender Schildarm |
| `_verworfen-e6-detail-schildarm.png` | Vergrößerung des fehlenden Arms |

Alle Einzelbilder 2752 × 1536 px (16:9).

## Vorbehalte

- **Ein Bild je Figur, ein einziges Schlachtbild, ein einziger Nachlauf.** Dass
  die Härtungen zweimal gegriffen haben, ist ein Beleg, keine Statistik.
- **Sechs Änderungen gleichzeitig** im Hauptlauf. Welcher Anteil des
  Erwachsen-Effekts von der Proportion, welcher von den Augen und welcher von
  der Nase kommt, ist nicht getrennt gemessen. Die Zuschreibung im Text ist eine
  Sichtbeurteilung.
- **E5 entspricht dem finalen Block nicht** (siehe oben).
- **Keine Miniaturprüfung.** Palette und Signalfarbe waren hier offen und sind
  es seit dem 15.08.2026 nicht mehr: beide **entfallen ersatzlos**, gefärbt wird
  in natürlichen Farben (siehe unten). Der Zusammenhalt hängt damit allein an
  Machart, Lichtführung und Figurenbau.
- **Kein Abgleich mit Unknown Frequencies am Bild** — der Vergleich lief gegen
  die Beschreibung, nicht gegen nebeneinandergelegte Standbilder.
- Die Aussage zum „Made for Kids"-Risiko ist eine Einschätzung zur Bildwirkung,
  keine Auskunft über die Einstufungspraxis von YouTube.

---

## Figurenblöcke im Wortlaut

Reihenfolge im Figurenblock ist verbindlich: **Alter und Körperbau →
Kopfproportion → Schädelumriss → Hautton → Augen → Brauen → Haar/Bart →
Kleidung → Haltung.** Die Brauen stehen vor der Frisur (Härtung 2).

### E3 Priester (gehärtete Fassung)
```
THIS CHARACTER: an older man, tall and upright, head one fifth of his body
height, long narrow skull outline, light olive skin tone; small eyes about one
twelfth of the head width, set close together, fully open and level; above them
two heavy straight dark eyebrows; below the eyes a long square dark grey beard
with rows of tight curls, and no visible hair on the head. He wears a long
fringed woollen robe in deep madder red draped over one shoulder; both arms hang
at his sides with both hands drawn, and both bare feet are inside the picture.
SCENE: a temple terrace in Babylon in the 6th century BC - a stepped ziggurat
silhouette behind him, a flat wall band of glazed deep blue brick with simple
rosette shapes, a dark night sky with a few plain star dots and a crescent moon.
```

### E6 Legionär (gehärtete Fassung)
```
THIS CHARACTER: a middle-aged man, solid and square-shouldered, head one fifth
of his body height, square angular skull outline with a heavy jaw, pale medium
skin tone; small eyes about one twelfth of the head width, set close together;
above them two low straight thick dark eyebrows; below them cropped dark hair
just visible under the helmet, clean-shaven. He wears Roman segmented plate
armour in flat grey over a red tunic, a plain crested helmet and hobnailed
sandals. Both arms are attached at the shoulders and fully drawn: his left arm
is bent and his left hand grips the handle of a rectangular red shield that
rests upright on the ground beside him, his right arm hangs straight and his
right hand holds a javelin planted on the ground. SCENE: a Roman frontier fort -
a straight flat paved road band, a simple wooden palisade wall and one square
gate tower behind him, flat green field bands, plain daylight sky.
```

### E1, E2, E4, E5 (aus dem Hauptlauf)

Entsprechen den Figurenblöcken aus `../README.md`, ergänzt um „of adult build"
und die wiederholte Proportionsangabe; E5 zusätzlich um „the lean athletic build
of a long-distance runner" und „her face set and concentrated". **Für die
Wiederverwendung müssen sie auf die Reihenfolge oben umgestellt werden** —
Brauen vor die Frisur, und bei E5 Brauen ergänzen.

### E7 Schlachtszene — Szenenteil im Wortlaut

```
SCENE: an ancient battlefield, treated as a sober historical reconstruction, not
as spectacle. On the right a Roman line of four legionaries in segmented armour
stands shoulder to shoulder behind locked rectangular shields, spears levelled,
faces set and grim under the helmets. On the left a looser group of three Celtic
warriors in checked trousers and cloaks, with oval shields and long spears,
braced for the impact. Between the two lines trampled grass and drifting dust.
In the foreground one fallen warrior lies motionless on his back on the ground,
his shield fallen flat beside him, one arm outstretched; next to him a second
man sits on the ground, head lowered, pressing one hand against a small dark red
wound mark on his side. Behind the lines a low ridge and a flat overcast grey
sky. Restrained and matter-of-fact: no blood spray, no wounds shown in detail,
no screaming faces, no heroic posing, no motion lines, no fire, no exaggeration.
It should read like a museum reconstruction plate, quiet and serious. no text,
no letters, no numbers, no watermark, no logo.
```


---

## Farbregel — entschieden am 15.08.2026

Der Block oben legt **Machart** fest, nicht Farbe. Für die Farbe gilt ab
Video 2:

**Alles wird so gefärbt, wie es in Wirklichkeit aussieht.** Himmel blau,
Vegetation grün, Gestein in seiner echten Farbe, Kleidung in den echten
Farbstoffen der jeweiligen Zeit. Keine Dämpfung, keine Palettenbeschränkung,
keine Signalfarbe.

Zwei Fassungen, weil Schemabilder keinen Himmel haben:

| | Raumbilder (62) | Schemabilder (22) |
|---|---|---|
| Wortlaut | `FARBEN` in `produktion/video-01/bildplan.py` | `FARBEN_SCHEMA` ebenda |
| Himmel, Vegetation | echte Farbe | **ausdrücklich keine** — Diagramm auf ebenem Grund |
| Materialien | echte Farbe | echte Farbe |

**Warum getrennt:** Im Testlauf bekam der Straßenquerschnitt M76 vom
gemeinsamen Farbsatz prompt blauen Himmel und Grasbüschel und war damit keine
Zeichnung mehr, sondern eine Ortsansicht.

**Was die Farbe nicht anfasst:** flächige Füllung, gleichmäßige Konturstärke,
harte flächige Schatten. Natürliche Farbe heißt naturalistischer Farbton, nicht
naturalistische Malweise — der letzte Satz beider Blöcke sagt das ausdrücklich.

**Beleg:** `recherche/farbtest-natuerlich/` — sechs Motive aus Video 1 in beiden
Fassungen nebeneinander, 14 Credits.
