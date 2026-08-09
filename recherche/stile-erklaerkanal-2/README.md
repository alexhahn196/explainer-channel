# Stilvorschläge, zweiter Lauf — radikal spezifiziert

> **Stand 2026-08-07.** Sechs Stile × zwei feste Testszenen = 12 Standbilder.
> Keine Videoclips, keine Animation, kein Render.
> **Kosten: 24 Credits** (12 × 2 Cr., `nano_banana_2`, 16:9, 2k) — Preis vorab
> per `get_cost` bestätigt, **kein Fehlschlag, kein Nachlauf**.
>
> Der erste Lauf (`../stile-erklaerkanal/`) war zu generisch. Hier steht der
> Stiltext **wörtlich** im Prompt, mit harten Beschränkungen: feste Farbzahl,
> benannte Drucktechnik, benanntes Material.

## Die Prompts im Wortlaut

Szenen wortgleich zum ersten Lauf, damit beide Läufe vergleichbar bleiben.
Jeder Prompt: `<Stiltext>. Subject: <Szene>. no text, no letters, no
watermark, no logo, no signature.`

**Szene A** — `a person sitting at a desk at night, looking at a glowing phone screen, a cup beside them`
**Szene B** — `a cutaway cross-section of a simple machine with visible gears, pipes and flowing arrows`

| | Stiltext (wörtlich im Prompt) |
|---|---|
| **S1** Risograph | `risograph print, exactly three spot inks (fluorescent pink, teal, black), visible misregistration of 1-2mm between layers, coarse halftone dot texture, flat paper white, no gradients, slight ink smudging` |
| **S2** Kupferstich | `19th century copperplate engraving, dense cross-hatching and stipple only, no solid fills, black ink on aged cream paper, scientific plate composition, extremely fine linework` |
| **S3** Konstruktivismus | `1920s Soviet constructivist poster, hard diagonal composition, exactly three colours (red, black, off-white), heavy geometric shapes, photomontage fragments, no perspective realism` |
| **S4** Filzdiorama | `handmade felt and cardboard diorama photographed with a macro lens, visible fabric fibres and glue, soft studio lighting, shallow depth of field, tilt-shift miniature look` |
| **S5** Schulwandkarte | `1950s classroom wall chart, matte muted palette, flat didactic illustration, numbered callout circles and thin leader lines, slight paper fold creases, printed on canvas-backed poster stock` |
| **S6** Röntgen | `x-ray radiograph aesthetic, luminous white edges on deep blue-black, translucent overlapping layers, thin technical annotation lines, no solid surfaces` |

## Messwerte

`oD p95` = 95. Perzentil der Luminanz im oberen Drittel (Textzone).
`Palette` = Überschneidung der Farbhistogramme A↔B. `Δ Mittel` = Differenz der
Gesamthelligkeit zwischen A und B — **das ist das Schwankungsmaß**.

| Stil | Sz | Balken | oD p95 | hell > 140 | Mittel | Palette A≈B | Δ Mittel |
|---|---|---|---|---|---|---|---|
| S1 Risograph | A | 0/0 | 240,3 | 60,4 % | 141,7 | **50 %** | **45,4** |
| | B | 0/0 | 241,9 | 81,4 % | 187,1 | | |
| S2 Kupferstich | A | 0/0 | 244,8 | 71,5 % | 169,5 | **65 %** | **33,3** |
| | B | 0/0 | 254,0 | 89,3 % | 202,8 | | |
| S3 Konstruktivismus | A | 0/0 | 224,0 | 14,1 % | 59,8 | **52 %** | **54,4** |
| | B | 0/0 | 236,8 | 47,9 % | 114,2 | | |
| S4 Filzdiorama | A | 0/0 | 158,1 | 6,2 % | 58,2 | **47 %** | **59,2** |
| | B | 0/0 | 233,4 | 46,4 % | 117,5 | | |
| S5 Schulwandkarte | A | 0/0 | 254,0 | 24,1 % | 116,8 | **34 %** | **73,8** |
| | B | 0/0 | 253,1 | 87,1 % | 190,6 | | |
| S6 Röntgen | A | 40/0 | 145,2 | 5,3 % | 45,9 | **73 %** | **11,7** |
| | B | 87/81 | 195,2 | 9,9 % | 57,6 | | |

Letterbox-Balken nur bei S6 (40 px bzw. 87/81 px) — mit `motiv_zuschnitt.py`
entfernbar, aber der einzige Stil im Lauf, der sie überhaupt erzeugt.

## Bewertung

### S1 Risograph

**Schwankung: mittel** (Palette 50 %, Δ Mittel 45,4). Das Farbpaar Pink/Teal
trägt beide Szenen, aber A ist ein dunkler Innenraum, B eine helle Fläche.
**160×90: übersteht es gut.** Das Rasterkorn verschwindet, aber die
Duotonfarbe bleibt — und die ist der eigentliche Erkennungsträger. Bei
Feed-Größe liest man sofort „dieser Kanal".
**Abstrakte Themen: gut.** Plakative Duotonflächen brauchen keinen Gegenstand.
**Thumbnail: schlecht.** Beide Szenen haben ein helles oberes Drittel
(p95 240 und 242, hell 60 % und 81 %).
**Animierbar: schwer.** Der Versatz zwischen den Druckplatten ist eine
Zufallsstruktur; von Frame zu Frame neu gewürfelt flimmert er.
**Auffälligkeiten:** Der Papierrand ist mitgeneriert — das Bild zeigt ein
fotografiertes Blatt, nicht eine Vollformatgrafik. Für einen Kanal müsste das
per Prompt raus.

### S2 Kupferstich

**Schwankung: gering** (Palette 65 %, Δ Mittel 33,3) — der zweitbeste Wert.
Beide Bilder sind unverkennbar dasselbe Stichsystem auf gealtertem Cremepapier.
**160×90: fällt durch.** Das ist der klare Verlierer im Feed-Test. Die feine
Schraffur mittelt sich zu Grau, Szene B wird zu einem beigen Fleck. Was den
Stil ausmacht — die Linienführung — ist bei Thumbnail-Größe physikalisch weg.
**Abstrakte Themen: schwach.** Und schlimmer: **der Stil schreibt die Vorgabe
um.** In Szene A ist aus dem leuchtenden Telefon ein Buch im Licht einer
Öllampe geworden. Ein Kupferstich von 1850 kennt kein Smartphone, und das
Modell löst den Widerspruch zugunsten des Stils. Für einen Kanal über moderne
Themen ist das disqualifizierend.
**Thumbnail: schlecht** (p95 244,8 und 254,0).
**Animierbar: schwer** — feine Linien flackern bei Bild-zu-Video stark.

### S3 Konstruktivismus

**Schwankung: mittel nach Zahlen** (Palette 52 %, Δ Mittel 54,4), **nach Auge
deutlich besser.** Rot/Schwarz/Creme mit harten Diagonalen ist in beiden
Bildern dieselbe Sprache; der Zahlenunterschied kommt daher, dass A
rotdominant und B weißdominant ist.
**160×90: übersteht es am besten von allen sechs.** Große Flächen, drei
Farben, harte Kanten — bei Feed-Größe sofort als derselbe Kanal lesbar.
**Abstrakte Themen: der stärkste im Lauf.** Konstruktivismus ist als Sprache
für Abstraktes erfunden worden; Wirtschaft und Gesellschaft sind sein
Heimatgebiet.
**Thumbnail: der beste im Lauf.** Szene A hat mit 14,1 % hellen Pixeln im
oberen Drittel und Gesamtmittel 59,8 große ruhige dunkle Flächen. B ist mit
47,9 % grenzwertig.
**Animierbar: gut.** Geometrische Flächen lassen sich schieben und drehen.
**Auffälligkeiten:** Szene B ist randvoll — bei Feed-Größe an der Grenze zum
Muster. Die Fotomontage-Fragmente bringen Gesichter ins Bild, die niemand
bestellt hat.

### S4 Filzdiorama

**Schwankung: hoch** (Palette 47 %, Δ Mittel 59,2, Δ Kontrast 67,6 — der
höchste Kontrastsprung im Lauf). A ist ein dunkelblaues Zimmer, B eine grüne
Außenszene. Dasselbe Material, zwei Welten.
**160×90: übersteht es**, aber als „Miniatur", nicht als *dieser* Kanal.
**Abstrakte Themen: der schwächste.** Alles muss als Objekt genäht werden.
**Thumbnail: Szene A ja** (p95 158,1, hell 6,2 %), B nein.
**Animierbar: am schwersten.** Der Reiz ist die reale Materialität; KI-Video
glättet genau das weg.
**Auffälligkeiten:** handwerklich das überzeugendste Einzelbild — Filzfasern,
Pappkanten, Klebespuren sitzen. Als Serie trotzdem unruhig.

### S5 Schulwandkarte

**Schwankung: die höchste im Lauf** (Palette 34 %, Δ Mittel 73,8). A steht auf
Dunkelgrün, B auf Creme — im Feed nebeneinander zwei Kanäle.
**160×90: übersteht es**, und die nummerierten Kreise sind ein starker
Wiedererkennungsanker, selbst wenn die Ziffern zu Punkten werden.
**Abstrakte Themen: gut.** Das Lehrtafel-Vokabular — Kreis, Leitlinie,
Beschriftung — ist für Erklären gebaut.
**Thumbnail: schlecht** (p95 254,0 und 253,1).
**Animierbar: gut.** Nacheinander aufpoppende Callouts sind die natürliche
Bewegung dieses Stils.
**Auffälligkeiten: Der Stiltext widerspricht der Szenenvorgabe.** „numbered
callout circles" verlangt Ziffern, „no text, no letters" verbietet sie. Das
Modell hat sich für die Ziffern entschieden — nachvollziehbar, aber der
Konflikt steckt im Auftrag, nicht im Ergebnis. Wer diesen Stil nimmt, muss
sich entscheiden.

### S6 Röntgen

**Schwankung: die mit Abstand geringste** — Palette **73 %**, Δ Mittel nur
**11,7**. Beide Bilder sind leuchtende weiße Linien auf fast schwarzem
Blaugrund, ohne jeden Bruch.
**160×90: übersteht es sehr gut.** Weiß auf Schwarz ist der kontrastreichste
mögliche Fall; bei Feed-Größe bleibt die Silhouette stehen.
**Abstrakte Themen: mittel.** „Durchleuchten" ist eine tragfähige Metapher für
Analyse und Zerlegung — aber alles Nichtgegenständliche muss erst in ein
Objekt übersetzt werden.
**Thumbnail: sehr gut.** Oberes Drittel p95 145,2 und 195,2, helle Pixel nur
5,3 % und 9,9 % — nach S3 der zweitbeste Textträger, und der einzige neben S3,
bei dem **beide** Szenen dunkel genug sind.
**Animierbar: gut.** Durchfahrten, Ebenenwechsel und aufleuchtende Linien sind
die Eigenbewegung dieses Stils.
**Auffälligkeiten:** der einzige Stil mit Letterbox-Balken (40 px bzw. 87/81
px). In Szene A ist die Person konsequenterweise ein Skelett — inhaltlich
richtig, aber für einen Alltagskanal möglicherweise zu kalt.

## Die zwei Stile, die am wenigsten schwanken

Gefragt war ausdrücklich die geringste Schwankung, unabhängig vom Aussehen.
Nach beiden Maßen — Palettenüberschneidung und Helligkeitsdifferenz — lautet
die Antwort:

| Rang | Stil | Palette A≈B | Δ Mittel |
|---|---|---|---|
| **1** | **S6 Röntgen** | **73 %** | **11,7** |
| **2** | **S2 Kupferstich** | **65 %** | **33,3** |

Zum Vergleich der Rest: S3 52 % / 54,4 · S1 50 % / 45,4 · S4 47 % / 59,2 ·
S5 34 % / 73,8.

**Wichtige Einschränkung zu Platz 2.** Kupferstich schwankt wenig, ist aber
trotzdem **unbrauchbar** — er zerfällt bei 160×90 zu Grau und schreibt die
Szenenvorgabe um (aus dem Telefon wurde eine Öllampe). Geringe Schwankung und
Brauchbarkeit sind zwei verschiedene Dinge; die Frage war nach dem ersten, und
die Antwort lautet Röntgen und Kupferstich.

**Wäre Brauchbarkeit das Kriterium**, hieße die Antwort **S6 Röntgen und
S3 Konstruktivismus**: beide überstehen den Feed-Test, beide haben in
mindestens einer Szene eine dunkle Textzone, beide sind animierbar. S3
schwankt nach Zahlen mittelmäßig, weil sich die Flächenverteilung von Rot und
Weiß zwischen den Szenen dreht — das Formenvokabular bleibt identisch, und
davon sieht das Histogramm nichts.

**Nicht getestet:** Animation. Alle Aussagen dazu sind Einschätzung aus den
Standbildern.
