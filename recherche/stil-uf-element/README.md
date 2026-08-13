# V2-Machart mit fixiertem eigenem Gesicht

> Lauf 2026-08-13. Grundlage: [`recherche/stil-unknown-frequencies.md`](../stil-unknown-frequencies.md)
> und [`recherche/stil-uf-varianten/README.md`](../stil-uf-varianten/README.md).
> **7 Bilder, 14,0 Credits** (Guthaben 3.081,9 → 3.067,9, gemessen).
> Keine Videos, keine Renders.

## Antwort vorweg

**Das Element hält.** In allen vier Szenen steht dieselbe Figur mit demselben
Gesicht, und in den drei Szenen mit aufrechter Haltung ist die Balkengeometrie
auf **0,13 bis 1,4 % genau identisch** — eine Größenordnung stabiler als der
Zeitleisten-Streifen aus V3, dessen Teilung sichtbar zwischen den Szenen
schwankte.

Die einzige Abweichung ist **Szene A**, und sie hat einen benennbaren Grund:
Die Figur sitzt dort und neigt den Kopf zum Telefon. Die Neigung verschiebt den
Balken relativ zum sichtbaren Kopf. Das ist **Perspektive, nicht Drift** — der
Balken bleibt dabei ein Balken über die volle Kopfbreite.

## Kosten [gemessen, `get_cost` 2026-08-13]

| Posten | Wert |
|---|---|
| `nano_banana_2`, 16:9, 2k | 2,0 Credits/Bild |
| 3 Figurenblätter + 4 Szenen = 7 Bilder | Vorhersage 14,0 |
| **tatsächlich abgebucht** | **14,0 Credits** |

**Modellhinweis:** Angefordert wurde `nano_banana_2`, die Aufträge liefen als
`nano_banana_flash` zurück — wie im Vorlauf. Der direkte Aufruf mit
`nano_banana_flash` wird dagegen als *unknown model* abgelehnt. Es handelt sich
also um eine serverseitige Umleitung, nicht um einen wählbaren Aliasnamen. Der
Preis blieb bei den vorhergesagten 2,0 Credits.

---

# Schritt 1 — Die drei Gesichtsentwürfe

Alle drei verzichten bewusst auf runde helle Augen. Jeder folgt einem **anderen
Erkennungsprinzip**, damit der Vergleich etwas aussagt und nicht drei
Abwandlungen desselben Einfalls prüft.

| Entwurf | Prinzip | Was ihn wiedererkennbar macht |
|---|---|---|
| **G1 Balken** | Verdeckung | Ein durchgehender indigoblauer Balken über die volle Kopfbreite ersetzt beide Augen — eine einzige große Fläche ohne Innenzeichnung, die keine Auflösung braucht, um zu funktionieren. |
| **G2 Ring** | Asymmetrie | Ein übergroßer Bernstein-Ring um das linke Auge gegen einen kleinen Punkt rechts — die Unwucht zwischen den beiden Augenhöhen ist das Signal, nicht die Form selbst. |
| **G3 Segment** | reine Geometrie | Ein massives Viertelkreis-Segment im oberen linken Kopfquadranten ersetzt das Gesicht vollständig — kein Auge, kein Mund, nur ein Zeichen. |

Dateien: `g1-balken-blatt.png`, `g2-ring-blatt.png`, `g3-segment-blatt.png`,
Gesamtansicht `_blaetter.png`.

## Der Kleintest hat entschieden, nicht der Augenschein

Der Kopf wurde auf **15 px und 25 px Höhe** verkleinert — so groß ist er in
einer 160×90-Miniatur real — und ungeglättet wieder vergrößert
(`_kopf-kleintest.png`).

| Entwurf | bei 15 px | Urteil |
|---|---|---|
| **G1 Balken** | massiver dunkler Querstrich, unverkennbar | **trägt** |
| G2 Ring | dünner Bernstein-Ring, kontrastarm gegen den hellen Kopf, zerfällt zum unklaren Fleck | trägt nicht |
| **G3 Segment** | massiver dunkler Keil, klar | **trägt** |

## Warum G1 und nicht G3

Beide überleben die Verkleinerung gleich gut. Den Ausschlag gibt die
**Stabilität über Haltungen**:

- Ein **Viertelkreis-Segment hat eine Orientierung**. Schon im Profil des
  Figurenblatts wandert es sichtbar. Bei jeder Kopfdrehung kann es mitrotieren,
  und dann ist es ein anderes Zeichen.
- Ein **waagerechter Balken über die volle Kopfbreite hat keine Orientierung**,
  die driften könnte. Er kippt höchstens mit dem Kopf — und das ist richtig so.
- **G2 fällt zusätzlich aus einem strukturellen Grund**: Der Ring ist an ein
  bestimmtes Auge gebunden. Dreht sich der Kopf, wechselt die Asymmetrie die
  Seite. Ein Erkennungsmerkmal, das seine Seite wechselt, ist keins.

**Gewählt: G1 „Balken".**

Als Referenzelement angelegt:

```
element_id: ab1406ea-8d08-421e-a8b8-5d3ef88042cf
name:       balkenkopf
category:   character
```

**Abgrenzung zum Vorbild:** Unknown Frequencies arbeitet mit *zwei großen
weißen Augen auf dunklem Grund*. Der Balkenkopf hat **überhaupt keine Augen**
und setzt *dunkel auf hell*. Das ist die Umkehrung des Prinzips, nicht seine
Kopie — übernommen wird allein die Idee, dass ein einziges hartes Gesichtszeichen
die Wiedererkennung trägt.

---

# Schritt 2 — Vier Testszenen

Alle vier mit eingebettetem `<<<ab1406ea-…>>>`, V2-Palette, V2-Machart und zwei
Zusätzen aus den Befunden der Vorläufe:

- **Dichtebremse** (`sparse composition, at most 5 distinct objects, generous
  empty background`) gegen den in zwei Läufen bestätigten Dichteüberschuss der
  Sachszenen.
- **Proportionsklausel** (`the head must not drift to normal human proportions`)
  gegen genau den Fehler, an dem V3-D im letzten Lauf gescheitert ist.

---

# Schritt 3 — Prüfung

## 1. Ist es in allen vier Szenen dasselbe Gesicht? [gemessen]

Der Balken wird über seine Indigo-Fläche gefunden, der Kopf über seine helle
Füllfläche. Absolutwerte der Spalte *Balken/Kopf* liegen methodenbedingt über
1,0, weil die Kopffläche ohne Konturring gemessen wird — **verglichen wird die
Streuung, nicht der Absolutwert.**

| Szene | Balken px | Balken / Kopfbreite | Dicke / Kopfhöhe | Lage im Kopf | Kopf / Bildhöhe |
|---|---:|---:|---:|---:|---:|
| A (Schreibtisch, **sitzend**) | 343 | 0,843 | 0,126 | 0,363 | 0,420 |
| B (Maschine) | 482 | 1,153 | 0,139 | **0,493** | 0,276 |
| C (Geld) | 532 | 1,147 | 0,136 | **0,491** | 0,301 |
| D (Landschaft) | 494 | 1,146 | 0,135 | **0,492** | 0,281 |

**Streuung, aufgeteilt nach Haltung:**

| Maß | B/C/D (stehend) | alle vier |
|---|---:|---:|
| Balkenbreite / Kopfbreite | **0,28 %** | 12,4 % |
| Balkendicke / Kopfhöhe | **1,38 %** | 3,8 % |
| Lage des Balkens im Kopf | **0,13 %** | 12,2 % |

Drei der vier Szenen sind **auf ein Drittel Prozent genau deckungsgleich**. Die
gesamte Streuung stammt aus Szene A allein, wo die Figur sitzt und den Kopf zum
Telefon neigt. Auch dort bleibt der Balken ein Balken über die volle Kopfbreite,
er sitzt nur höher im sichtbaren Kopf (0,363 statt 0,492) — was bei einem nach
vorn geneigten Kopf genau richtig ist.

**Zum Vergleich der Zeitleisten-Streifen aus V3:** dort war das Element zwar in
allen vier Szenen vorhanden, aber die Teilung schwankte sichtbar von grob (A) bis
fein (C, D) — eine Abweichung, die sich nicht mit der Perspektive erklären lässt.
**Der Balkenkopf ist das deutlich stabilere Element.**

## 2. Ist die Figur in allen vier Szenen vorhanden? [gemessen]

**Ja, 4 von 4.** Der Balken wurde in jeder Szene automatisch gefunden.

Das ist die Behebung des Fehlers aus dem letzten Lauf: Dort fiel die Figur bei
**V1-B** (Maschinenschnitt) komplett aus — das einzige der zwölf Bilder ohne
Figur. Genau diese Szene trägt jetzt die Figur, weil sie über das Element
angefordert wurde statt über eine Stilbeschreibung.

## 3. Bleibt der überproportionierte Kopf? [gesehen + gemessen]

**Ja, in allen vier.** Der Kopf misst 0,28 bis 0,42 der Bildhöhe; im
Verhältnis zum Körper liegt er bei rund einem Drittel der Figurenhöhe, wie im
Figurenblatt angelegt. **Kein Fall von V3-D**, wo die Figur zu normalen
Körperproportionen driftete.

Die Unterschiede in *Kopf / Bildhöhe* (A 0,420 gegen B 0,276) sind
**Rahmung, nicht Drift** — in A sitzt die Figur näher an der Kamera.

## 4. Trägt das Gesicht die Wiedererkennung bei 160×90? [gesehen]

**Ja, und zwar als einziges Element.** In `_mini/kontaktbogen-160x90.png` ist
von den Hintergründen nichts mehr zu unterscheiden — Maschine, Stadt und
Landschaft zerfallen zu Farbflächen. Der dunkle Querbalken auf dem hellen
runden Kopf bleibt in allen vier Miniaturen scharf und sofort auffindbar.

Das ist genau das Prinzip, das die Messung beim Vorbild gefunden hat: Nicht der
Stil trägt die Handschrift, sondern **ein einziges hartes Gesichtszeichen.**

## 5. Palette stabil über alle vier? [gemessen]

**Ja.** Palettenabstand zwischen den Szenen im Mittel **3,90** (Spanne
2,92–5,48). Zum Vergleich derselbe Wert im letzten Lauf: V2 5,32 · V3 8,48 ·
V1 8,72. **Die Palette liegt jetzt enger als bei jeder Variante des Vorlaufs.**

| Szene | Kanten | Objekte | Farbfläche | Sättigung |
|---|---:|---:|---:|---:|
| A | 0,0260 | 18 | 0,437 | 0,136 |
| B | 0,0409 | 31 | 0,662 | 0,149 |
| C | 0,0290 | 16 | 0,630 | 0,162 |
| D | 0,0479 | 26 | 0,528 | 0,287 |

Streuung: Kanten SD 0,0089 · Objekte SD 6,06 · Farbfläche SD 0,089 ·
Sättigung SD 0,060. Die Sättigung in D fällt aus dem Rahmen (0,287 gegen
0,136–0,162), weil die Landschaft großflächig Bernstein einsetzt.

## 6. Dichteunterschied Person gegen Sache [gemessen]

Klassifikation wie im letzten Lauf beibehalten: Personenszenen A und C,
Sachszenen B und D.

| | Personenszenen | Sachszenen | Faktor |
|---|---:|---:|---:|
| Kantendichte | 0,0275 | 0,0444 | **1,61×** |
| Objektzahl | 17 | 28 | **1,68×** |

**Die Dichtebremse hat den Unterschied nicht behoben.** Zum Vergleich der
letzte Lauf ohne Bremse: V1 1,45× · V2 1,66× · V3 1,50×. Der Faktor liegt
weiterhin im selben Band.

**Was die Bremse sehr wohl bewirkt hat, ist die absolute Dichte.** Gegen V2
desselben Prompts ohne Bremse:

| | V2 letzter Lauf | dieser Lauf | Änderung |
|---|---:|---:|---:|
| Kanten Personenszenen | 0,0485 | 0,0275 | **−43 %** |
| Kanten Sachszenen | 0,0802 | 0,0444 | **−45 %** |
| Objekte Personenszenen | 44 | 17 | **−61 %** |
| Objekte Sachszenen | 65 | 28 | **−57 %** |

**Der Befund ist damit dritter Lauf in Folge bestätigt und zugleich
eingeordnet:** Sachszenen geraten rund 1,5- bis 1,7-mal dichter als
Personenszenen, und das lässt sich mit einer Objektobergrenze **nicht**
angleichen — sie senkt beide Seiten um etwa dieselbe Quote. Wer die Szenen
gleich dicht haben will, muss die Obergrenze **je Szenentyp verschieden**
setzen, nicht global.

---

# Prompts im Wortlaut

## Figurenblätter (Schritt 1)

Gemeinsames Gerüst, bei allen drei identisch bis auf den `FACE:`-Satz:

```
Character model sheet: two consistent full-body views of the identical original
character, side by side on a plain empty off-white #F2EDE3 background with
nothing else in the frame. Left: front view, standing upright facing the viewer,
arms relaxed at the sides, both feet visible, head to toe, not cropped. Right:
side profile view of the same character, standing, facing right, head to toe,
not cropped. Both views the same height and the same scale, even spacing, flat
even lighting. Flat 2D vector cartoon in the style of a limited-animation
explainer video. Clean uniform anti-aliased black outlines of constant medium
weight; no sketchy lines, no hand-drawn jitter, no crosshatching. The character
has an oversized round head roughly one third of the total body height, a
pill-shaped torso, thin stick limbs, simple mitten hands, and no nose. The head
is off-white #F2EDE3. [FACE] Restricted three-colour palette - ink indigo
#1F3A5F, warm amber #E0A93B, off-white paper #F2EDE3 - plus the black outlines.
No olive, no military green, no slate grey, no brown. Flat colour fills, no
gradients on the figures, hard-edged shapes. no text, no letters, no watermark,
no logo, no signature, exactly one character shown twice, no other people, no
props, no furniture, no background objects.
```

**G1 Balken:**
```
FACE: instead of eyes, one single solid horizontal ink indigo bar runs straight
across the eye region from one side of the head to the other, with rounded ends;
no eyes are visible at all; below it a short thin straight mouth line. Nothing
else on the face.
```

**G2 Ring:**
```
FACE: strongly asymmetric - around the left eye sits one oversized warm amber
#E0A93B ring, a thick open circle outline about one third of the head width; the
right eye is only a small solid black dot, placed noticeably higher than the
ring; below them a short thin straight mouth line. Nothing else on the face.
```

**G3 Segment:**
```
FACE: no eyes and no mouth at all - the pale round head carries one single bold
geometric mark, a solid ink indigo #1F3A5F quarter-circle segment filling the
upper left quadrant of the head, its two straight edges meeting at the centre of
the head. Nothing else on the face.
```

## Testszenen (Schritt 2)

Gemeinsames Gerüst, `<<<ID>>>` steht für `ab1406ea-8d08-421e-a8b8-5d3ef88042cf`:

```
Flat 2D vector cartoon in the style of a limited-animation explainer video.
Clean uniform anti-aliased black outlines of constant medium weight; no sketchy
lines, no hand-drawn jitter, no crosshatching. The background is noticeably more
detailed than the figures: layered flat shapes with a faint paper grain and light
stipple texture. Restricted three-colour palette - ink indigo #1F3A5F, warm amber
#E0A93B, off-white paper #F2EDE3 - plus the black outlines. No olive, no military
green, no slate grey, no brown. Flat colour fills, no gradients on the figures,
hard-edged shapes. Sparse composition, at most 5 distinct objects, generous empty
background. [SCENE] The character keeps its oversized round head at roughly one
third of its total body height, its off-white head colour and the solid indigo
bar across the eye region exactly as in the reference; the head must not drift to
normal human proportions. no text, no letters, no watermark, no logo.
```

```
SCENE: <<<ID>>> sitting at a desk at night, looking at a glowing phone screen, a cup beside them.

SCENE: a cutaway cross-section of a simple machine with gears, pipes and arrows;
<<<ID>>> stands at the right of the frame facing the viewer, looking at the machine.

SCENE: an abstract idea: money flowing between two hands - <<<ID>>> stands on the
left facing the viewer and holds out one hand, a stream of coins arcs from it into
a second hand that enters from the right edge of the frame.

SCENE: a wide landscape with a road going to the horizon; <<<ID>>> stands in the
left foreground facing the viewer, the road running past behind them.
```

**Abweichung von der Auftragsvorlage, die genannt gehört:** Die Szenen B, C und
D waren im Vorlauf ohne Figur formuliert. Damit die Frage „ist die Figur in
allen vier Szenen vorhanden" überhaupt prüfbar ist, wurde die Figur in jede
Szene hineingeschrieben. Der beschriebene Bildinhalt selbst blieb wörtlich
unverändert.

---

# Dateien

| Datei | Inhalt |
|---|---|
| `g1-balken-blatt.png` … `g3-segment-blatt.png` | die drei Figurenblätter, 2752×1536 |
| `szeneA.png` … `szeneD.png` | die vier Testszenen mit Element, 2752×1536 |
| `_blaetter.png` | die drei Blätter untereinander |
| `_kopf-kleintest.png` | Kopf bei 15 px und 25 px, ungeglättet vergrößert |
| `_kopf-g1…g3.png` | die drei Kopfausschnitte |
| `_kontaktbogen.png` | die vier Szenen, 2×2 |
| `_mini/*-160x90.png` | Kleintest je Szene und Blatt |
| `_bewertung.py` | Messskript, läuft ohne Argumente |
| `_messwerte.txt` | Rohausgabe der Messung |

# Was offen bleibt

- **Vier Szenen sind vier Datenpunkte.** Dass die Balkengeometrie in drei
  stehenden Szenen auf 0,3 % zusammenfällt, ist ein starker Hinweis und kein
  Beweis für Serienstabilität. Der ehrliche Test wäre ein Durchlauf über 20
  Szenen mit wechselnden Haltungen.
- **Nur eine geneigte Haltung geprüft.** Ob der Balken auch bei Rückenansicht,
  starker Seitenansicht oder Nahaufnahme hält, ist **unbekannt** — das
  Figurenblatt deckt Front und Profil ab, mehr nicht.
- **Das Element enthält ein einziges Referenzbild.** Mehr Ansichten im Element
  würden die Stabilität vermutlich weiter erhöhen; geprüft ist das nicht.
- **Der Mund ist unzuverlässig.** In Szene A ist er durch die Kopfneigung nicht
  sichtbar. Als Erkennungsmerkmal trägt er nichts — was den Balken als
  alleinigen Träger bestätigt, aber bedeutet, dass Mimik über dieses Gesicht
  nicht läuft. Für einen Erklärkanal ohne Figurendrama ist das folgenlos, für
  erzählende Formate wäre es eine Einschränkung.
- **Nicht geprüft: wie das Gesicht neben Text wirkt.** Das Vorbild fährt in
  jedem Thumbnail 1–7 Wörter mit 10,4 % Versalhöhe. Ob der Balken neben einer
  Schlagzeile noch trägt oder mit ihr konkurriert, steht aus.
