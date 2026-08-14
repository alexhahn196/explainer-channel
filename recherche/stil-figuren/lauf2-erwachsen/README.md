# Lauf 2: dieselbe Machart, erwachsen gelesen — 2026-08-14

Fortschreibung von `../README.md`. Zwei Aufträge in einem Lauf:

1. **Die Machart darf nicht kindlich lesen.** Begründung ist geschäftlich, nicht
   ästhetisch: Chibi-Optik (großer Kopf, große runde Augen, keine Nase) erhöht
   das Risiko, dass YouTube den Kanal als „für Kinder gemacht" einstuft — das
   kostet personalisierte Werbung, Kommentare und RPM.
2. **Darstellungsfähigkeit prüfen.** Historische Themen verlangen Kampf,
   Verletzung, Tod. Trägt die Machart das, oder wird es unfreiwillig komisch?
   Dafür ein siebtes Bild: antike Schlachtszene, ernst und dokumentarisch.

Orientierung: *Unknown Frequencies* — flach und stilisiert, liest trotzdem
erwachsen.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2`, 16:9, **2k** | **2 Credits** |
| Erzeugt | 7 Bilder à 2k, 2752 × 1536 |
| **Verbraucht** | **14 Credits** |
| Kontostand vor dem Lauf | 2975,9 Credits |
| Fehlschläge, Nachläufe | keine |

Modellsubstitution zum dritten Mal: angefordert `nano_banana_2`, gelaufen unter
`nano_banana_flash`. Abrechnung wie im Preflight.

## Was am Machart-Block geändert wurde

Sechs Änderungen auf einmal — gegen die sonstige Ein-Variable-Regel des Repos,
aber „liest erwachsen" ist ein Bündel und kein Einzelmerkmal.

| Bauteil | Lauf 1 | Lauf 2 |
|---|---|---|
| Kopf : Körperhöhe | ⅓ | **⅕, ausdrücklich nie größer als ¼** |
| Augengröße | bis ⅕ der Kopfbreite | **~⅒, bei F3 und F6 ¹⁄₁₂** |
| Glanzpunkt im Auge | Pflichtbauteil | **entfällt ganz** |
| Nase | verboten | **kurzer Strich oder flacher Schattenfleck** |
| Formensprache | rund, weich | **kantig, gerade Kanten, harte Ecken** |
| Körperbau | Kugelkopf, Stäbchenglieder, Fäustlinge | **Schultern breiter als der Kopf, sichtbarer Hals, kantiger Kiefer, flache Hände mit angedeuteter Fingertrennung** |
| Verbote neu | — | **keine Wangenröte, keine Wimpern, keine halbgeschlossenen Lider, kein Babygesicht, „never cute"** |

Dazu die Reparatur des Proportionsbruchs aus Lauf 1: der Block sagt jetzt
ausdrücklich, dass jede Kopfform-Angabe **nur den Schädelumriss** meint und die
Kopf-zu-Körper-Proportion nicht verändert; F2 und F3 wiederholen die Proportion
zusätzlich im Figurenblock.

Der vollständige Block steht unten im Wortlaut.

## Befund 1: Liest es erwachsen?

**Ja, bei sechs von sieben.** Der Proportionsbruch aus Lauf 1 ist weg: alle
Figuren stehen jetzt im selben Maßsystem, Kopf grob ein Sechstel der
Körperhöhe, Schultern breiter als der Kopf, Hals sichtbar. Die Nase ist in
sieben von sieben da. Kein Bild zeigt Wangenröte, keine Wimpern, keine
Glanzpunkte.

Der stärkste Einzeleffekt kommt nicht von der Proportion, sondern von der
**Augengröße plus Nase**. Dieselbe Figur, dieselbe Kleidung, dieselbe Szene wie
in Lauf 1 — F1 Moorbauer und F6 Legionär lesen jetzt als erwachsene Männer statt
als Maskottchen, und geändert wurden im Gesicht nur diese beiden Größen.

**Die Ausnahme ist E5, die Inka-Läuferin.** Sie ist die einzige Figur, die noch
jugendlich wirkt: Ihre Augen sind sichtbar größer geraten als die der anderen
sechs, das Gesicht ist rund und glatt geblieben. Der Grund ist erkennbar das
Bauteil „keine Brauen" — ohne Brauen fehlt der obere kantige Abschluss des
Gesichts, und das Modell füllt die Lücke mit größeren Augen. **Brauenlos und
erwachsen schließen sich in dieser Machart offenbar aus.** Das Bauteil
„Brauen ja/nein" sollte deshalb aus dem Variationskatalog gestrichen und auf
„Brauen immer, Form variabel" gesetzt werden.

Ein zweiter, schwächerer Rest: **E2 hat wieder keine Brauen bekommen**, obwohl
dünne gerade Brauen bestellt waren — derselbe Ausfall wie in Lauf 1, wieder bei
der weiblichen Figur mit Kopftuch. Das ist jetzt zweimal dasselbe Muster und
sollte als Modellverhalten behandelt werden, nicht als Zufall.

**Wichtige Einschränkung zum Geschäftsrisiko:** Die Einstufung „Made for Kids"
hängt nicht am Zeichenstil allein, sondern an Thema, Titel, Thumbnail, Sprache
und Kanaleinstellung zusammen. Dieser Lauf senkt ein Signal, er räumt das Risiko
nicht ab.

## Befund 2: Trägt die Machart Kampf, Verletzung, Tod?

**Ja.** `e7-schlacht.png` wirkt an keiner Stelle unfreiwillig komisch.

Was den Ernst trägt:

- **Die Gesichter.** Kleine Augen, gerade Brauen, gerader Mundstrich — die
  Legionäre und die keltischen Krieger schauen grimmig und angespannt. Bei
  Lauf-1-Augen (⅕ Kopfbreite, Glanzpunkt) wäre genau das gekippt: große
  glänzende Augen über einer Schildlinie lesen als Spielzeugsoldaten.
- **Der Gefallene** liegt still auf dem Rücken, Kopf zur Seite, Augen als zwei
  geschlossene Striche, Arm ausgestreckt, Schild flach daneben. Er wird nicht
  ausgestellt, er liegt einfach da. Das ist die Bildsprache einer
  Museumstafel, nicht die eines Comics.
- **Der Verwundete** sitzt am Boden, Kopf gesenkt, Hand auf der Seite, ein
  dunkelroter Fleck auf der Tunika und einer am Oberarm. Kein Spritzer, keine
  Wunde im Detail, kein Schrei. Das reicht, um zu erzählen, dass er getroffen
  ist, und bleibt unterhalb dessen, was eine Altersfreigabe auslöst.
- **Kein Effektvokabular:** keine Bewegungslinien, kein Feuer, keine Heldenpose,
  keine Zuspitzung.

Was auffällt, aber den Ernst nicht bricht: Die Speere der zweiten Reihe liegen
kompositorisch quer über den Schilden und wirken teils angesetzt statt gehalten.
Das ist ein Kompositionsfehler, kein Stilproblem.

**Damit ist die eigentliche Frage beantwortet:** Die Machart trägt schwierige
Inhalte, seit die Augen klein und die Nase da ist. Sie trug sie in Lauf 1 nicht.

## Das Offensichtliche, geprüft

| Prüfpunkt | Befund |
|---|---|
| **Falsche Figurenzahl** | **E3 Priester zeigt ZWEI Figuren**, obwohl `exactly one character` im Prompt steht. Beide sind zusätzlich **am unteren Bildrand abgeschnitten** (Beine ab Knie fehlen), obwohl der Block „head to toe, not cropped" verlangt. Das Bild ist als Figurenblatt unbrauchbar |
| **Fehlende Gliedmaßen** | **E6 Legionär: der rechte Arm fehlt.** Der Schild steht frei neben ihm, ohne Hand, ohne Arm — nur die Schulterplatte, dann Schild. Im Kleinen unauffällig, in der Vergrößerung (`_detail-e6-schildarm.png`) eindeutig |
| **Verformte Hände** | keine. Die Hände tragen jetzt angedeutete Finger, sauber gebaut — auch im Schlachtbild (Speerhände, die Hand des Verwundeten, die offene Hand des Gefallenen) |
| **Text im Bild** | keiner. Die Schildmotive (gelbe Flügel- und Sichelformen, Buckel) und die Rosetten an der babylonischen Wand sind Ornament |
| **Sonstiges** | Weiche Verläufe treten weiter auf (Himmel in E1, E4, Boden in E2), trotz `no gradients`. Dritter Lauf mit demselben Befund |

Zwei Bilder haben also einen harten Fehler: **E3** (Doppelfigur, angeschnitten)
und **E6** (fehlender Arm). Beide sind Modellrauschen, kein Fehler der
Machart-Beschreibung — ein Nachlauf derselben zwei Prompts kostet 4 Credits und
ist **nicht** ausgeführt, weil dafür kein Auftrag vorlag.

## Empfehlung für den Machart-Block

1. **„Brauen ja/nein" streichen.** Brauen werden Pflichtbauteil, variabel ist
   nur die Form. Begründung: E5.
2. **Brauenausfall bei verhüllten Frauenköpfen absichern** — Brauen im
   Figurenblock nochmals nennen und vor die Frisur ziehen. Begründung: E2 in
   beiden Läufen.
3. **`exactly one character` verstärken** — der Zusatz wurde in E3 ignoriert;
   „a single person, alone in the frame, no second figure, no mirrored copy"
   ist der nächste Versuch.
4. **Gliedmaßen-Ansage ergänzen** — „both arms visible and attached, the hand
   that carries an object is drawn". Begründung: E6.
5. Kopfproportion, Augengröße, Nase und Kantigkeit **unverändert übernehmen** —
   sie tun genau das, wofür sie eingesetzt wurden.

## Dateien

| Datei | Inhalt |
|---|---|
| `e1-moorbauer.png` … `e6-legionaer.png` | dieselben sechs Figuren wie in Lauf 1, erwachsene Machart |
| `e7-schlacht.png` | Testszene: antike Schlacht, dokumentarisch |
| `_kontaktbogen.png` | alle sieben nebeneinander |
| `_kontaktbogen-gesichter.png` | sieben Köpfe auf gleiche Größe gebracht (bei E7 der Verwundete) |
| `_detail-e6-schildarm.png` | Beleg für den fehlenden Arm |
| `_detail-e7-gefallener.png`, `_detail-e7-verwundeter.png` | Belege zur Darstellungsfähigkeit |

Alle Einzelbilder 2752 × 1536 px (16:9).

## Vorbehalte

- **Ein Bild je Figur, ein einziges Schlachtbild.** Ob die Machart Kampf
  *zuverlässig* trägt, ist mit einem Bild nicht entschieden — nur, dass sie es
  kann.
- **Sechs Änderungen gleichzeitig.** Welcher Anteil des Erwachsen-Effekts von
  der Proportion, welcher von den Augen und welcher von der Nase kommt, ist
  nicht getrennt gemessen. Die Zuschreibung im Text („Augen plus Nase tragen
  am meisten") ist eine Sichtbeurteilung, keine Messung.
- **Keine Miniaturprüfung**, keine Palette, keine Signalfarbe — alles offen.
- **Kein Abgleich mit Unknown Frequencies am Bild.** Der Vergleich lief gegen
  die Beschreibung, nicht gegen nebeneinandergelegte Standbilder.
- Die Aussage zum „Made for Kids"-Risiko ist eine Einschätzung zur Bildwirkung,
  keine Auskunft über die tatsächliche Einstufungspraxis von YouTube.

---

## Prompts im Wortlaut

Jeder der sieben Prompts beginnt mit diesem Block, wortgleich (bei E7 fehlen die
Wörter `generous empty space` und `head to toe`, weil die Szene mehrere Figuren
zeigt):

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
finger separation. Any description of head shape refers to the outline of the
skull only and never changes this head-to-body proportion. FACE BUILD, identical
construction for every character in this series: small eyes, each about one
tenth of the head width, a rounded white eye shape with one solid dark pupil,
fully open, no catchlight highlight, no eyelashes, no half-closed lids, no wide
staring doll eyes; a minimal nose indicated by one short straight line or a
small flat shadow shape; below it one short thin straight mouth line; no cheek
blush, no baby face. Eyebrows, where the character has them, are drawn and carry
the expression. Minimal symbolic background built from a few large flat shapes,
generous empty space, muted era-appropriate colours. Figures are shown in full,
head to toe, not cropped at the edge of the frame. Sober, restrained,
documentary - never cute.
```

Die sechs Figurenblöcke entsprechen denen aus `../README.md`, ergänzt um
„of adult build" und die wiederholte Proportionsangabe; E5 zusätzlich um „the
lean athletic build of a long-distance runner" und „her face set and
concentrated".

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
