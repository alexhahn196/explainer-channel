# RESERVE — nicht für Kanal 2. Vorgemerkt für einen späteren Kanal. Stand 14.08.2026.

Der Stil ist gut und wird aufbewahrt, aber er kommt für Kanal 2 (Erklärkanal)
nicht zum Einsatz. Was ihn ausmacht: Die Farbe steckt im Putz statt auf ihm —
matte kreidige Flächen, weiche Pinselkanten, kein Tuschestrich, Craquelé über
dem ganzen Bild, ausgearbeitete Gesichter und Faltenwurf, Figuren im Raum. Der
Träger der Signalfarbe ist **das teure Pigment**: Genau ein Gegenstand je Bild
ist türkis gemalt, und zwar der, um den es geht — eine Regel, die materialecht
ist (Ägyptisch Blau war das teuerste Pigment einer Werkstatt) und die auch dort
trägt, wo keine Szene ist: im Schema färbt sie eine Schicht, im Detail eine
Schnur. Der **Ernsttest ist bestanden** (Bild 10, Schlachtszene: der Gefallene
liegt still, der Verwundete hat einen dunklen Fleck, niemand posiert), und
**Detail und Schema tragen ebenfalls** (Bild 8, zwei Hände an der Eichenbohle;
Bild 9, Straßenquerschnitt ohne jede Beschriftung). Zwei Dinge sind vor einem
späteren Einsatz zu klären: **Die offene Schwäche ist die Feed-Größe** — bei
160 × 90 verschwindet das Craquelé restlos, und damit genau der
Materialcharakter, der die Richtung ausmacht; was überlebt, ist allein die
Signalfarbe (in 9 von 10 Bildern noch als Fleck erkennbar), wer den Stil
einsetzt, braucht also eine eigene Thumbnail-Lösung. Und **drei Bilder hatten
angeschnittene Figuren trotz Vorgabe** (Bild 5, 6 und die Randfiguren in Bild
10) — die Rahmen-Härtung aus dem Figurenlauf
(`../stil-figuren/lauf2-erwachsen/README.md`, Härtung 3) ist in diesen Block
noch nicht eingearbeitet.

Der verbindliche Stil für Kanal 2 steht in
`../stil-figuren/lauf2-erwachsen/README.md`.

---

# Fresko ohne Fehlstellen — Breitentest, 2026-08-14

S3 aus `../stil-runde-5/` ist gewählt. Die abgeplatzten Stellen entfallen
**ersatzlos** — sie waren dort das Erkennungsmerkmal. Was bleibt: Farbe im Putz
statt auf ihm, matte kreidige Flächen, weiche Pinselkanten, Craquelé über allem,
kein Tuschestrich, ausgearbeitete Gesichter und Faltenwurf, Figuren im Raum.

Der Block ist der S3-Block **im Wortlaut**, mit zwei Eingriffen:

1. Der Halbsatz zu den Fehlstellen ist gestrichen.
2. An seiner Stelle steht ein ausdrückliches Verbot, damit die Abplatzungen
   nicht durch die Hintertür zurückkommen: `The paint layer is complete and
   intact - no flaking, no losses, no missing patches, no bare plaster showing,
   no chips, no holes.`

Craquelé und die Tagesnaht (`giornata`-Naht) bleiben stehen — beides ist
Oberfläche, keine Fehlstelle.

## Kosten [gemessen]

| Posten | Wert |
|---|---|
| Preflight `get_cost`, `nano_banana_2`, 16:9, **2k** | **2 Credits** |
| Erzeugt | 10 Bilder |
| **Verbraucht** | **20 Credits** |
| Kontostand vor dem Lauf | 2899,9 Credits |
| Fehlschläge, Nachläufe | keine |

Modellsubstitution wie in allen Läufen: angefordert `nano_banana_2`, gelaufen
unter `nano_banana_flash`.

## Der neue Träger der Signalfarbe: das teure Pigment

Mit der Fehlstelle fällt der bisherige Träger weg. Vorschlag, in allen zehn
Bildern gleich umgesetzt:

> **Genau ein Gegenstand je Bild ist türkis gemalt — und zwar der, um den es im
> Bild geht.** Sonst ist nirgends Türkis im Bild.

Im Prompt steht das so:

```
RECURRING ELEMENT: exactly one object in the picture is painted with the single
expensive pigment the workshop owned, turquoise #1BBFB0 - the object the picture
is about. It is the only turquoise anywhere in the image; everything else stays
inside the muted earth palette.
```

Drei Gründe für genau diesen Träger:

- **Er ist materialecht.** Ägyptisch Blau und Fayence-Türkis waren die teuersten
  Pigmente der Antike; eine Werkstatt setzte sie sparsam und an genau einer
  Stelle ein. Die Regel ist also nicht aufgesetzt, sondern die Praxis selbst.
- **Er arbeitet inhaltlich.** Die Signalfarbe zeigt, worauf der Satz zeigt — sie
  ist Lesehilfe, nicht Dekoration, und in einem Erklärkanal damit funktional.
- **Er trägt auch ohne Szene.** Im Schema (Bild 9) färbt er eine Schicht, im
  Detail (Bild 8) eine Schnur, in der Schlachtszene (Bild 10) den Schild neben
  dem Gefallenen.

Was in welchem Bild den Träger stellt, steht unten bei den Prompts.

## Was in jedem Bild auffällt

| Nr. | Motiv | Ein Satz |
|---|---|---|
| **1** | Mesopotamischer Träger | Der türkise Korb ist so gesättigt, dass er den Blick vor dem Gesicht fängt — und das Bild sitzt in einem mitgemalten Steinrahmen, ist also nicht randlos. |
| **2** | Landstraße | Der Meilenstein trägt die Farbe glaubwürdig, wirkt aber als einziger Gegenstand in einer menschenleeren Weite eher wie ein gesetztes Zeichen als wie ein Fundstück. |
| **3** | Römischer Legionär | Die Szene sitzt als schmale Insel in der Bildmitte, links und rechts steht leerer Putz; das Schildzeichen trägt das Türkis sauber, ist aber das kleinste Vorkommen im Lauf. |
| **4** | Moorbauer | Das polierte Beil liest sofort als Jadeitklinge, und der Nebel gibt dem Fresko eine kalte, fast graue Palette, die kein anderes Bild hat. |
| **5** | Ägyptische Steinträgerin | Der Fayence-Kragen sitzt genau richtig — die Figur ist dafür unten angeschnitten, ab der Hüfte fehlt sie. |
| **6** | Babylonischer Priester | Die eine türkise Rosette in der Reihe der ockerfarbenen ist der ruhigste Signalfarbeneinsatz im Lauf; die Figur ist dafür unten vom Rahmen abgeschnitten. |
| **7** | Inka-Läuferin | Das Stirnband ist der kleinste Träger und verschwindet als erster bei Verkleinerung; das Bild ist zugleich das farbigste im Lauf. |
| **8** | Hände legen eine Eichenbohle | Detail trägt: zwei gealterte Hände, Torfwasser, Craquelé bis ins Holz — und die türkise Schnur macht aus einer Nahaufnahme ohne Gesicht trotzdem ein Bild mit Thema. |
| **9** | Querschnitt Straßenaufbau | Das Schema funktioniert ganz ohne Beschriftung: fünf Schichten unterscheiden sich allein über Korn und Farbe, und die türkise Sandschicht liest wie eine Markierung im Profil. |
| **10** | Schlachtszene | Der Ernsttest hält — der Gefallene liegt still, der Verwundete hat einen dunklen Fleck auf der Tunika, niemand posiert; die Figuren an beiden Bildrändern sind angeschnitten. |

## Das Offensichtliche, geprüft

| Prüfpunkt | Befund |
|---|---|
| **Fehlende Figur** | keine. Die sieben Figurenbilder zeigen je genau eine Figur, Bild 8 auftragsgemäß nur zwei Hände, Bild 2 und 9 sind wie bestellt menschenleer, Bild 10 zeigt die bestellte Gruppe |
| **Verformte Hände** | keine. Sechs Hände im Prüfschnitt (`_handpruefung.png`) sind sauber gebaut, auch die ausgestreckte Hand des Gefallenen und die zwei Nahaufnahme-Hände in Bild 8 |
| **Text im Bild** | keiner, in keinem der zehn Bilder — auch nicht im Schema, das am ehesten Beschriftung provoziert hätte |
| **Angeschnittene Figuren** | **drei Fälle**: Bild 5 (Frau ab Hüfte abgeschnitten), Bild 6 (Priester ab Oberschenkel abgeschnitten), Bild 10 (die Randfiguren links und rechts). Bild 5 und 6 verstoßen gegen `figures are shown complete, not cropped` |
| Fehlstellen | **keine**, in keinem Bild — das Verbot hat gegriffen. Craquelé ist überall da |
| Nicht randlos | Bild 1 und 6 haben einen mitgemalten Rahmen aus Stein bzw. Putz; Bild 3 lässt links und rechts große leere Putzflächen stehen |

### Bei 160 × 90

Die Miniaturen liegen unter `_mini/`, alle zehn zusammen auf
`_mini/kontaktbogen-160x90.png` (dreifach mit Nearest-Neighbor vergrößert, damit
die Feed-Größe beurteilbar bleibt).

Was in der Verkleinerung passiert: Das Craquelé verschwindet restlos — der
Materialcharakter, der die Richtung ausmacht, ist bei Feed-Größe **nicht mehr
da**. Was bleibt, ist die Signalfarbe: Korb, Meilenstein, Beilklinge, Kragen,
Rosette, Schnur, Sandschicht und der Schild in der Schlachtszene sind bei
160 × 90 alle noch als türkiser Fleck erkennbar. Das Stirnband in Bild 7 ist der
einzige Träger, der die Verkleinerung nicht übersteht; das Schildzeichen in
Bild 3 ist grenzwertig. Die Rahmen in Bild 1 und 6 lesen als dunkle Kante um das
Bild.

## Dateien

| Datei | Inhalt |
|---|---|
| `f01-traeger.png` … `f10-schlacht.png` | die zehn Motive |
| `_kontaktbogen.png` | alle zehn, zwei Spalten × fünf Zeilen |
| `_mini/*-160x90.png` | die zehn Bilder auf Thumbnailgröße |
| `_mini/kontaktbogen-160x90.png` | alle zehn Miniaturen auf einem Blatt |
| `_handpruefung.png` | sechs Handausschnitte vergrößert |

Alle Einzelbilder 2752 × 1536 px (16:9).

## Vorbehalte

- **Ein Bild je Motiv.** Kein Wiederholungslauf; ob die Anschnitte in Bild 5 und
  6 systematisch sind oder Würfe, ist nicht entschieden.
- Die Beurteilung ist **eine Sichtprüfung**, keine Messung — so beauftragt.
- **Keine Animationsprüfung.** Craquelé ist eine Feinstruktur; bei Bild-zu-Video
  kann sie von Frame zu Frame neu gewürfelt flimmern. Das ist für einen
  Videokanal der offene Punkt, den dieser Lauf nicht beantwortet.
- Die Miniaturbeurteilung erfolgte am Kontaktbogen, nicht in einem echten
  YouTube-Feed.
- **Signalfarbe weiterhin vorläufig** (`#1BBFB0`). Fällt die Entscheidung
  anders aus, ändert sich am Träger nichts — nur der Farbwert.
- Keine Rangliste — so beauftragt.

---

## Der Stilblock im Wortlaut

Steht am Anfang jedes der zehn Prompts, wortgleich.

```
A wall painting in true fresco: mineral pigment soaked into lime plaster, matte
and slightly chalky, laid on with a loaded brush in flat areas with visible
brush drag and softly irregular contours. There is no ink linework at all -
every edge is a painted edge. The plaster wall itself is part of the picture:
fine craquelure over the whole surface and a faint horizontal seam where two
days of work meet. The paint layer is complete and intact - no flaking, no
losses, no missing patches, no bare plaster showing, no chips, no holes. Earth
pigments burnt into the surface: red ochre, yellow ochre, terre verte, bone
black, lime white, muted and dusty. The figures are adult and grave, with
worked-out faces and drapery folds, standing in real space; never cute, never
childlike. Figures are shown complete, not cropped at the edge of the frame.
RECURRING ELEMENT: exactly one object in the picture is painted with the single
expensive pigment the workshop owned, turquoise #1BBFB0 - the object the picture
is about. It is the only turquoise anywhere in the image; everything else stays
inside the muted earth palette.
```

Negativliste am Ende: `no text, no letters, no numerals, no watermark, no logo`
— bei Einzelfiguren zusätzlich `exactly one person in the picture`, bei Bild 9
zusätzlich `no labels, no arrows`.

Bei den figurenlosen Bildern (2, 9) entfallen die beiden Figurensätze, bei Bild
8 stehen sie als `Adult hands, worked out in real anatomy, grave and
unsentimental` da.

## Motive und Signalfarbträger im Wortlaut

| Nr. | `SUBJECT:` | `THE TURQUOISE OBJECT:` |
|---|---|---|
| 1 | a Mesopotamian labourer carrying a heavy basket of stones on his shoulder, walking along a dirt field track, a low mudbrick wall and two date palms behind him | the woven basket of stones he carries |
| 2 | a wide landscape with an ancient road running to the horizon between low bare hills, scattered rocks along the verges, a wide empty sky. No people in the picture | a single upright milestone standing beside the road in the foreground |
| 3 | a Roman legionary in segmented armour and a crested helmet standing on a paved road, a large rectangular shield at his side and a spear held upright, a wooden fort palisade behind him | the painted device on the face of his shield |
| 4 | a Stone Age bog farmer in Somerset standing on wet moorland in low mist, wearing rough fur and hide clothing and leather leg wraps, holding a hafted stone axe, reed tufts and dark peat pools around him, a pale grey sky | the polished stone blade of his axe |
| 5 | an Egyptian woman of the Old Kingdom carrying a rectangular limestone block on her shoulder, in a plain undyed linen dress and a linen headcloth, standing at the edge of the desert with stacked cut blocks and a wooden sledge behind her, pale hot sky | the faience bead collar around her neck |
| 6 | an elderly Babylonian priest in a long fringed woollen robe with a long square curled beard, standing upright in front of a glazed brick wall with rosette panels, a stepped ziggurat behind him, evening sky | one single glazed rosette in the brick wall |
| 7 | an Inca woman running along a stone mountain path in the Andes, wearing a short tunic with woven geometric bands and simple sandals, terraced slopes and snow peaks behind her, clear high sky | the woven headband across her forehead |
| 8 | a close-up of two weathered adult hands lowering a split oak plank onto wet peat ground, seen from just above; reed stalks and dark peat water around the plank, no faces, no other figures | the twisted cord looped around the end of the oak plank |
| 9 | a cutaway cross-section through the build-up of a Roman road, cut straight down like a trench wall and seen from the side: the flat paved slab surface on top, then a layer of packed gravel, then a layer of rubble stones, then a bed of sand, then the undisturbed subsoil at the bottom, each layer clearly separated and drawn to different grain sizes, with a shallow drainage ditch at one side. No people in the picture | the bed of sand layer, painted turquoise throughout |
| 10 | an ancient battlefield treated as a sober historical reconstruction, not as spectacle. On the right a short line of Roman legionaries stands behind locked shields with spears levelled, faces set and grim; on the left a looser group of warriors with oval shields braced for the impact. In the foreground one fallen warrior lies motionless on his back, one arm outstretched, his shield fallen flat beside him; near him a second man sits on the ground, head lowered, one hand pressed to a dark stain on his tunic. Trampled grass, a low ridge, an overcast sky. Restrained and matter-of-fact: no blood spray, no wounds in detail, no screaming faces, no heroic posing, no motion lines, no fire, no exaggeration | the shield lying on the ground beside the fallen warrior |
