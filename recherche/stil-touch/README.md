# Sechs Zusätze zur Machart — Testlauf 2026-08-14

Der Machart-Block aus `../stil-figuren/lauf2-erwachsen/README.md` bleibt
unverändert die Basis. Dieser Lauf **ergänzt** ihn um je einen Zusatz und
ersetzt nichts. Gesucht ist ein wiederkehrendes **Element**, das jemand beim
Zusehen bemerkt — nicht eine schönere Zeichnung. Vorbilder: der Bruch zwischen
gerendertem Thumbnail und flachem Videoinneren plus die immer gleichen weißen
Augen bei *Unknown Frequencies*, die Vögel bei *Kurzgesagt*.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2`, 16:9, **2k** | **2 Credits** |
| 6 Richtungen × 2 Motive + 2 Vergleichsbilder | 14 Bilder |
| **Verbraucht** | **28 Credits** |
| Kontostand vor dem Lauf | 2957,9 Credits |
| Fehlschläge, Nachläufe | keine |

Modellsubstitution wie in allen bisherigen Läufen: angefordert `nano_banana_2`,
gelaufen unter `nano_banana_flash`.

## Aufbau

Zwei feste Motive, in allen sieben Zeilen wortgleich:

- **A** — `a Mesopotamian labourer in a simple linen wrap carrying a basket of
  stones on a dirt track` (Figur, Alltag, Nahbereich)
- **B** — `a wide landscape with an ancient road going to the horizon`
  (keine Figur, Weite, Leerraum)

Jeder Prompt: `<Machart-Block>` + `THIS CHARACTER` (nur A) + `SCENE` +
`ADDITION - …` + Negativliste. Die **Basis-Zeile** hat keinen `ADDITION`-Absatz
und ist der Vergleichspunkt.

### Drei Entscheidungen, die für den Test getroffen werden mussten

1. **Z4 kollidiert mit der Negativliste.** Handschriftliche Notizen und
   Maßzahlen einerseits, `no letters, no numbers` andererseits schließen
   einander aus. Für Z4 — und nur dort — sind die beiden Verbote entfernt und
   durch `no printed type, no title, no caption` ersetzt; die Handschrift ist
   ausdrücklich als unleserlich beschrieben. Derselbe Konflikt ist in
   `../stile-erklaerkanal-2/` schon einmal aufgetreten (S5 Schulwandkarte).
2. **Z5 Begleiter: ein Haussperling.** Er folgt der menschlichen Siedlung seit
   dem Neolithikum, kommt in allen neun Kulturen und in jeder Alltagsszene
   glaubwürdig vor und bleibt klein genug, das Bild nicht zu übernehmen. Die
   naheliegende Alternative wäre ein Hund — größer, auffälliger, in Rasse und
   Größe schwerer konstant zu halten.
3. **Z6 braucht die Signalfarbe**, die noch offen ist. Vorläufig gefahren wird
   das Türkis `#1BBFB0` aus den Gesichtstests. Fällt die Entscheidung anders,
   muss Z6 neu beurteilt werden.

---

## Die Basis, ohne Zusatz

Zwei Bilder ohne jede Ergänzung. A zeigt den Träger vor einer Lehmziegelmauer,
zwei Dattelpalmen rechts, drei waagerechte Erdbänder. B zeigt die Straße als
Fluchtpunktkeil zwischen zwei Hügelketten, mit Steinen und Grasbüscheln.
Beide sind randlos, flach, ohne Textur, ohne Schatten und ohne ein einziges
Element, das jemand wiedererkennen könnte — genau das ist die Lücke, die die
sechs Richtungen füllen sollen.

## Z1 Material

Das ganze Bild sitzt auf einem sichtbaren Blatt: Faserung, dunkle Sprenkel und
fleckige Verfärbungen liegen gleichmäßig über Figur, Flächen und Leerraum, und
der warme Papierton scheint durch alle hellen Füllungen durch.

Das Modell hat in beiden Bildern zusätzlich den **Blattrand mitgezeichnet** — in
A eine gerissene Büttenkante rundum, in B einen umlaufenden Rahmen mit
Passepartout: Das Ergebnis ist ein fotografiertes Blatt, kein randloses
Vollformat.

Die Farbigkeit zieht dabei kräftig Richtung Papier, in B bis fast zur
Entsättigung — dieselbe Zeichnung liest deutlich blasser als in der Basiszeile.

## Z2 Druckfehler

An der Figur liegt eine zweite Farbebene um ein bis zwei Millimeter versetzt:
auf einer Seite steht ein schmaler Farbrand über die schwarze Kontur hinaus, auf
der anderen blitzt der Untergrund durch.

In A bleibt der Effekt sehr zurückhaltend — an Kontur, Lendentuch und Korb in
der Großansicht sichtbar, im Vorbeischauen kaum; der Hintergrund ist wie
bestellt sauber im Register geblieben.

In B gibt es keine Figur, auf die die Regel greifen könnte: statt eines
Versatzes hat das Modell ein breites weißes Band über den Horizont gelegt — die
Richtung erzeugt in figurenlosen Bildern etwas anderes als bestellt.

## Z3 Lichtquelle

Beide Bilder haben genau eine sichtbare Quelle, die tief stehende Sonne, und
alles wirft harte, flächige Schatten in genau einem dunkleren Ton, ohne Verlauf
und ohne weiche Kante.

Die Schatten laufen in einer Richtung und geben Figur, Steinen und Mauer eine
Standfläche, die die Basis nicht hat; in A ist der Schattenwurf des Trägers das
größte einzelne Element im Bild.

Die Gesamtstimmung kippt dabei wärmer und dunkler als in der Basiszeile, und der
Zusatz ist der einzige im Lauf, der in beiden Motiven gleich stark wirkt,
obwohl in B keine Figur vorkommt.

## Z4 Randnotiz

Rund um die Szene stehen Pfeile, Maßstriche mit Endbalken, Zahlen und
Handschrift in einer einzigen sepiafarbenen Tinte; die Szene selbst bleibt
unberührt.

Beide Bilder haben dafür **einen Rahmen bekommen**: Die Szene ist nach innen
gerückt und füllt das 16:9-Format nicht mehr aus — die Notizen brauchen einen
Rand, und den nimmt sich das Modell vom Bild.

Die Handschrift ist außerdem **nicht unleserlich geblieben**, obwohl ausdrücklich
so bestellt: Sie schreibt englische Wörter aus dem Prompt ab — `head height skul
outline`, `excavation-notebook`, `two-date palm`, dazu Zahlen wie `1034 m` und
`450 m`.

## Z5 Begleiter

Ein Haussperling sitzt in beiden Bildern links unten auf einem Stein, in
derselben Konturstärke und derselben flachen Füllsprache wie alles andere.

Er ist in A und B gleich groß, gleich gefärbt und in fast gleicher Haltung — und
das ohne Referenzbild, allein über die Textbeschreibung.

Am Rest des Bildes ändert er nichts: Palette, Konturen, Aufbau und Leerraum
bleiben identisch zur Basiszeile, es kommt genau ein Objekt hinzu.

## Z6 Zeitschicht

Hinter der antiken Szene stehen Strommasten mit durchhängenden Kabeln, ein
Plattenbau und ein Straßenschild als reine Türkis-Umrisse ohne Füllung.

In A sitzt die zweite Schicht sauber hinter der Figur und lässt sie unberührt;
in B ist sie größer geraten und färbt zusätzlich Hügelrücken und Himmel
türkisgrün ein, sodass die zweite Zeit dort nicht mehr nur Umriss ist.

Die Signalfarbe ist damit im Bild an genau eine Sache gebunden und kommt
nirgendwo sonst vor — in beiden Motiven ist Türkis die einzige kalte Farbe.

---

## Das Offensichtliche, geprüft

| Prüfpunkt | Befund |
|---|---|
| **Fehlende Figur** | keine. Alle sieben A-Bilder zeigen genau eine Figur; alle sieben B-Bilder sind wie bestellt menschenleer |
| **Verformte Hände** | keine. In allen sieben A-Bildern sind Korbhand und freie Hand sauber gebaut (`_figurenstreifen.png`) |
| **Text im Bild** | nur in **Z4**, dort auftragsgemäß — aber als lesbare englische Wörter statt als unleserliche Handschrift. In den anderen zwölf Bildern kein Text |
| **Anschnitt** | Z1-B und beide Z4-Bilder sind nicht randlos: Blattkante bzw. Rahmen rücken die Szene nach innen |
| Sonstiges | weiche Verläufe treten weiter auf (Himmel, Boden), trotz `no gradients` — fünfter Lauf mit demselben Befund |

## Dateien

| Datei | Inhalt |
|---|---|
| `z0-basis-A.png`, `z0-basis-B.png` | Vergleichspunkt ohne Zusatz |
| `z1-material-A/B.png` | Z1 Material |
| `z2-druckfehler-A/B.png` | Z2 Druckfehler |
| `z3-lichtquelle-A/B.png` | Z3 Lichtquelle |
| `z4-randnotiz-A/B.png` | Z4 Randnotiz |
| `z5-begleiter-A/B.png` | Z5 Begleiter |
| `z6-zeitschicht-A/B.png` | Z6 Zeitschicht |
| `_kontaktbogen.png` | alle vierzehn, Zeilen Basis → Z6, links Motiv A, rechts Motiv B |
| `_figurenstreifen.png` | die sieben A-Figuren nebeneinander — Prüfschnitt auf Hände und Figurenzahl |

Alle Einzelbilder 2752 × 1536 px (16:9).

## Vorbehalte

- **Ein Bild je Richtung und Motiv.** Bildmodelle streuen; ein zweiter Lauf
  desselben Prompts kann anders ausfallen. Nichts hier beruht auf einer Serie.
- **Zwei Motive.** Ob ein Zusatz über neun Kulturen, Innenräume, Nachtszenen und
  Schemabilder trägt, ist damit nicht geprüft.
- **Keine Miniaturprüfung**, kein Feed-Test, keine Animationsprüfung. Gerade bei
  Z2 (Versatz) und Z1 (Korn) ist das erheblich: Beides sind Strukturen, die von
  Frame zu Frame neu gewürfelt flimmern können.
- **Z6 fährt eine vorläufige Signalfarbe.** Die Entscheidung steht aus.
- **Z4 läuft mit veränderter Negativliste**, ist also nicht unter denselben
  Bedingungen entstanden wie die anderen fünf.
- Der Sperling in Z5 ist mein Vorschlag, keine Vorgabe.
- Keine Rangliste, keine Empfehlung, keine Messwerte — so beauftragt.

---

## Die Zusätze im Wortlaut

Jeder Text wird als eigener Absatz hinter `SCENE:` gehängt.

### Z1 Material
```
ADDITION - SURFACE: the entire picture sits on a visible physical surface.
Coarse handmade paper: irregular fibres, small dark specks and flecks, uneven
mottling and faint stains spread across the whole frame including the empty
areas, with a slightly rough deckled feel. The drawing itself stays completely
flat and unshaded - only the material underneath carries texture, and the warm
paper tone shows through the lighter colour fills.
```

### Z2 Druckfehler
```
ADDITION - PRINT MISREGISTRATION: cheap newsprint printing error. A second flat
colour layer is shifted about one to two millimetres away from the black
linework, so a thin band of colour sticks out past the outline on one side of
the figure and a thin sliver of bare background shows on the other side. The
offset is the same direction and the same distance everywhere it occurs. This
misregistration applies ONLY to the figure and the objects the figure carries -
the background shapes stay perfectly registered inside their outlines.
```

### Z3 Lichtquelle
```
ADDITION - ONE LIGHT SOURCE: exactly one light source is visible in the picture,
the low sun. Everything it strikes casts a hard flat shadow: each shadow is a
solid shape in one single darker tone of the surface it falls on, with straight
or simply curved edges, no gradient, no blur, no soft falloff, no ambient
shading. All shadows run in the same direction, away from the light. The lit
sides stay completely flat and unshaded.
```

### Z4 Randnotiz
```
ADDITION - FIELD NOTEBOOK MARGIN NOTES: in the empty margin areas along the
edges of the picture there are handwritten excavation-notebook annotations, all
in one single ink colour, dark sepia, and all in the same fine loose
handwriting: thin hand-drawn arrows pointing from the margin towards parts of
the scene, small measurement ticks and thin dimension lines with end bars, a few
scribbled numerals, and short strokes of quick illegible handwriting. The
handwriting is deliberately not legible. The annotations stay near the edges and
never cover the scene itself.
```
Negativliste bei Z4: `no printed type, no title, no caption, no watermark, no logo.`

### Z5 Begleiter
```
ADDITION - RECURRING COMPANION: one small brown house sparrow is present in the
picture, drawn in exactly the same flat outlined style as everything else,
roughly the size of a fist, plain brown and grey with a short beak. It is not
the subject of the picture and it reacts to nothing: it simply perches or hops
somewhere off to one side, going about its own business. Exactly one sparrow, no
flock.
```

### Z6 Zeitschicht
```
ADDITION - SECOND TIME LAYER: faintly present behind the ancient scene, standing
in the same place but in the present day, a modern silhouette is drawn as a thin
flat outline in signal turquoise #1BBFB0 with no fill at all: electricity pylons
with slack cables, a plain concrete apartment block, a road sign on a post. This
second layer sits behind everything else, is drawn only in that one turquoise
outline colour, overlaps nothing important, casts no shadow and does not
interact with the ancient scene. It is quiet and easy to miss.
```

### Die zwei Motive im Wortlaut

**A**
```
THIS CHARACTER: a middle-aged labourer of adult build, head one fifth of his
body height, oval skull outline, medium olive-brown skin tone; small eyes about
one tenth of the head width, set a normal distance apart; above them two
straight dark eyebrows; below them short dark hair and a short dark beard. He
wears a simple undyed linen wrap around his hips, bare feet, and carries a woven
basket of rough stones on one shoulder, both hands steadying it, walking along
the track. SCENE: a dirt track in Mesopotamia - flat bands of dry ochre earth, a
low mudbrick wall behind him, two date palms at the right, pale hot sky.
```

**B** (mit der Mehrfiguren-Fassung des `FRAMING:`-Satzes aus dem Machart-Block)
```
SCENE: a wide landscape with an ancient road going to the horizon - a broad flat
earth road band narrowing to a vanishing point, low bare hills on both sides, a
few scattered rocks, a wide pale sky. No people in the picture.
```
