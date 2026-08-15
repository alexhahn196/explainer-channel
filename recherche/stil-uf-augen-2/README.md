# Normale Augen im V2-Stil — drei Feinvarianten zur Wahl

> Lauf 2026-08-14. **6 Bilder, 12,0 Credits** (2,0 je Bild, `get_cost` vorab gemessen).
> Keine Videos, keine Renders. Keine Messung, keine Rangliste, keine Empfehlung —
> die Wahl liegt beim Auftraggeber.

Die drei Entwürfe aus [`stil-uf-augen/`](../stil-uf-augen/) sind verworfen. Der Grund
steht dort implizit in den Zahlen: Die damalige Vorgabe „bei 15 px Kopfhöhe erkennbar"
belohnt genau die überzeichneten Lösungen — dunkler Kopf, Leuchtaugen, Ringe —, weil bei
15 px nur noch Helligkeitsflächen zählen. **Die Vorgabe ist gestrichen.** Im Thumbnail
steht die Figur groß im Bild; der Kopf hat dort keine 15 px.

## Was gleich bleibt

V2-Machart unverändert, dazu in allen drei Varianten identisch:

- warmer heller Hautton `#E8C4A0` für Kopf und Hände — **kein dunkler Kopf**
- überproportionierter runder Kopf, etwa ein Drittel der Figurenhöhe
- gleiche Konturstärke, flache Füllungen, harte Kanten, keine Nase
- ein kurzer, leicht geschwungener Mundstrich
- je ein kleiner weißer Glanzpunkt im Auge
- Kleidung in der Moor-Palette: Torfbraun `#4A3B2A`, Schilfocker `#A8894E`,
  Nassmoos `#5B6B4A`, dazu eine kleine Gürtelschnalle in Signaltürkis `#1BBFB0`

Die Türkis-Schnalle ist aus dem Vorlauf mitgenommen und **nicht Teil dieser
Entscheidung** — sie steht nur mit im Bild, damit die Blätter untereinander
vergleichbar bleiben.

## Was sich unterscheidet

Nur die drei Achsen aus dem Auftrag. Alles andere ist Wort für Wort derselbe Prompt.

| | Augengröße | Pupillenform | Augenbrauen |
|---|---|---|---|
| **N1 Rund** | mittel, ca. ⅙ Kopfbreite | runde Vollpupille | keine |
| **N2 Groß mit Brauen** | groß, ca. ⅕ Kopfbreite | runde Vollpupille | **ja**, zwei kurze leicht geschwungene |
| **N3 Klein, Ovalpupille** | klein, ca. ⅛ Kopfbreite | **hochovale** Pupille | keine |

## Die Gesichtssätze im Wortlaut

Nur dieser eine Satz unterscheidet die drei Prompts.

**N1 Rund**
```
FACE: two medium-sized rounded white eyes, each about one sixth of the head width,
each with a solid round dark pupil and one small white catchlight; no eyebrows;
below them one short thin gently curved mouth line.
```

**N2 Groß mit Brauen**
```
FACE: two noticeably large rounded white eyes, each about one fifth of the head
width, each with a solid round dark pupil and one small white catchlight; above
them two short, slightly curved dark eyebrows set a little apart from the eyes,
giving the face expression; below them one short thin gently curved mouth line.
```

**N3 Klein, Ovalpupille**
```
FACE: two smaller rounded white eyes, each about one eighth of the head width,
each with a tall vertical oval dark pupil and one small white catchlight; no
eyebrows; below them one short thin gently curved mouth line.
```

## Gemeinsamer Stilblock

```
Flat 2D vector cartoon in the style of a limited-animation explainer video. Clean
uniform anti-aliased black outlines of constant medium weight; no sketchy lines, no
hand-drawn jitter, no crosshatching. The character has an oversized round head
roughly one third of the total body height, a pill-shaped torso, thin stick limbs,
simple mitten hands, and no nose. Flat colour fills, no gradients on the figures,
hard-edged shapes. Warm light skin tone #E8C4A0 for head and hands. The face is
friendly, calm and immediately readable as a face, not as a symbol; ordinary drawn
cartoon eyes capable of expression. [FACE] Clothing in a muted bog palette: peat
brown #4A3B2A tunic, reed ochre #A8894E belt, wet moss #5B6B4A leggings, one small
signal turquoise #1BBFB0 belt buckle. no text, no letters, no numbers, no watermark,
no logo, exactly one character shown twice, no other people, no props, no furniture,
no background objects.
```

Die Nahaufnahmen benutzen denselben Block mit ausgetauschter Kompositionszeile:
`Head-and-shoulders close-up portrait … the oversized round head filling most of the
frame, centred, on a plain empty pale linen #EFE9DC background`.

## Dateien

| Datei | Inhalt |
|---|---|
| `n1-rund-blatt.png` · `n1-rund-gesicht.png` | N1, Figurenblatt und Nahaufnahme, je 2752×1536 |
| `n2-gross-brauen-blatt.png` · `n2-gross-brauen-gesicht.png` | N2 |
| `n3-klein-ovalpupille-blatt.png` · `n3-klein-ovalpupille-gesicht.png` | N3 |
| `_blaetter.png` | die drei Figurenblätter untereinander |
| `_gesichter.png` | die drei Gesichter nebeneinander |

## Offen

Kein Entwurf ist gewählt, kein Referenzelement angelegt — beides erst nach der
Entscheidung. Ebenfalls noch offen aus dem Vorlauf: das dritte Thema für die
Palettenliste (der damalige Auftrag brach nach „Antike/Wüste" ab).
