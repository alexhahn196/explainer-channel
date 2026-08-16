# Bildlauf Video 1 — Stapel 1 (10 von 84)

> Lauf 15.08.2026. **20 Credits** (`nano_banana_2` angefordert, als
> `nano_banana_flash` gelaufen — vierte Substitution in Folge, Abrechnung wie
> im Preflight: 2,0 Cr/Bild bei 16:9, 2k). Kontostand vorher 2.879,9 · nachher
> **2.859,9**.
>
> **Lauf gestoppt. 5 von 10 sind Fehlschläge, drei davon aus einer gemeinsamen
> Ursache, die alle 84 Motive beträfe.** Die restlichen 74 sind nicht gelaufen.

Kontaktbogen: [`_kontaktbogen-1600.png`](_kontaktbogen-1600.png) — obere Reihe
M01 · M06 · M55 · M62 · M84, untere Reihe M12 · M25 · M49 · M72 · M53.

## Auswahl der zehn

Als Belastungsprobe zusammengestellt, nicht als Reihenfolge: alle drei
Themenpaletten, Schema gegen Raumbild, Einzel- gegen Mehrfigur, und die beiden
Motive, die im Stichprobenlauf vom 14.08. durchgefallen waren (M55, M62).

## Prüfergebnis

| Motiv | Figur | Brauen | Kopf ⅕ | genau 1 Licht | Hände | kein Text | nicht angeschnitten | Urteil |
|---|---|---|---|---|---|---|---|---|
| **M01** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **bestanden** ¹ |
| **M06** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **Fehlschlag** ² |
| **M55** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **bestanden** |
| **M62** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** | **Fehlschlag** ³ |
| **M84** | ✓ | ✓ | ✓ | **✗** | ✓ | ✓ | ✓ | **Fehlschlag** ⁴ |
| **M12** | – | – | – | ✓ | – | ✓ | ✓ | **bestanden** |
| **M25** | – | – | – | Schema | – | ✓ | ✓ | **bestanden** |
| **M49** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✗** | **Fehlschlag** ⁵ |
| **M72** | ✓ | ✓ | ✓ | **✗** | **✗** | ✓ | ✓ | **Fehlschlag** ⁶ |
| **M53** | – | – | – | ✓ | – | ✓ | ✓ | **bestanden** |

¹ Kamerawinkel weicht ab: `szenen.md` verlangt **Aufsicht**, geliefert ist Frontalsicht.
² Die Figur trägt **modernes Hemd und Hose in einer urzeitlichen Szene**; außerdem steht sie groß im Bild statt „klein am linken Rand".
³ **Füße unten angeschnitten** · Kleidung ist **ägyptisch (Nemes-Kopftuch, Schendyt) in Chaco Canyon** · Figur groß in der Mitte statt klein am Rand.
⁴ **Lichtquelle nicht im Bild** — Schatten laufen einheitlich, aber Z3 verlangt eine *sichtbare* Quelle · die Figur **sieht nicht in die Kamera**, wie die Szene verlangt.
⁵ Die Figur am **linken Bildrand ist angeschnitten** — der Mehrfiguren-FRAMING-Satz verlangt ausdrücklich das Gegenteil.
⁶ **Moderne Schiebermütze und Jacke auf einer Inka-Treppe um 1450** · beide Hände mit **gespreizten, klauenartigen Fingern** statt „a hint of finger separation" · **kein Schlagschatten** trotz Z3.

## Die gemeinsame Ursache — mein Fehler im Promptbau

**Drei der fünf Fehlschläge (M06, M62, M72) sind Epochenfehler, und sie gehen
auf eine Auslassung in `bildplan.py` zurück: Die Spalte `Epoche/Ort` aus
`szenen.md` steht nicht im Prompt.**

Der Figurenblock sagt nur „of the era described in the scene". Die
SCENE-Beschreibungen nennen die Kultur aber meist gar nicht — M72 heißt bloß
„a stone stairway climbs a steep slope". Ohne Epochenangabe rät das Modell,
und es rät nach der Palette: Antike-Palette → Ägypten (deshalb der Nemes in
Chaco Canyon), sonst → Gegenwart.

**Betroffen wären alle 84 Motive**, nicht nur diese drei. `szenen.md` führt die
Epoche für jedes einzelne (Somerset 3807 v. Chr., Campemoor, Babylon 569 v.
Chr., Chaco ~1000 n. Chr., Anden ~1450 n. Chr., Rom 312 v. Chr. …) — die Daten
liegen vor, sie waren nur nicht im Prompt.

## Was sonst noch auffiel

- **Figurengröße wird nicht befolgt.** Wo `szenen.md` „die Figur klein am Rand"
  verlangt (M06, M62), steht sie groß und mittig. Die Geisterkopf-Härtung aus
  dem Stichprobenlauf hat dagegen **gewirkt** — keine schwebenden Köpfe, keine
  gespiegelte Komposition.
- **M55 ist geheilt.** Die Umformulierung aus dem Stichprobenlauf (Figur im
  Profil am Rand statt Rückenansicht) liefert genau das Gewünschte.
- **Anschnitt trotz Härtung.** Der FRAMING-Satz verbietet ihn ausdrücklich,
  M62 und M49 verletzen ihn trotzdem.
- **Die geratene dritte Palette** (Nachtblau/Waldgrün/Zinngrau) trägt in M72
  und M84 farblich, liest aber nicht andin — was in M72 vom Epochenfehler
  überlagert wird und dort nicht getrennt beurteilbar ist.
- **Türkis sitzt richtig**, wo es gebraucht wird: der Jahresring in M12, das
  Tor in M53 und M55.

## Nächster Schritt — nicht ausgeführt

Ein Nachlauf der fünf Fehlschläge wäre sinnlos, solange die Epochenangabe
fehlt: dieselben Prompts erzeugen dieselben Fehler. Vorgeschlagene Korrektur an
`bildplan.py`, **vor** dem Nachlauf und vor den restlichen 74:

1. `Epoche/Ort` aus `szenen.md` wörtlich in den Prompt aufnehmen, als
   `PERIOD AND PLACE: …` vor dem Figurenblock.
2. Bei Motiven mit „Figur klein": Bildanteil ausdrücklich vorgeben
   (`the figure is small, no more than one sixth of the frame height`).
3. Anschnittverbot verschärfen: `all figures complete, nothing touching the
   frame edge`.
4. Handregel verschärfen: `mitten-like hands, fingers only hinted, never spread
   apart` — gegen die Klauenhände in M72.

Kosten des Nachlaufs: 5 Bilder = 10 Credits. Gesamtlauf danach 74 × 2 = 148
Credits. Zusammen mit den bereits verbrauchten 20 bleibt das mit **178
Credits** deutlich unter der Grenze von 500.

---

# Nachlauf der fünf Fehlschläge — 15.08.2026

**10 Credits** (5 Bilder à 2,0). Kontostand 2.859,9 → **2.849,9**. Gesamt für
Video 1 bisher **30 Credits**. Die v1-Fassungen liegen zum Vergleich in
[`_v1/`](_v1), Gegenüberstellung: [`_vorher-nachher.png`](_vorher-nachher.png).

## Was vorher geprüft wurde

Die vier Korrekturen sind vor dem Nachlauf an **allen 84** Prompts geprüft, nicht
nur an den fünf:

| Korrektur | Abdeckung |
|---|---|
| 1 · `PERIOD AND PLACE` | 49/84 Prompts · fehlt bei 32 ohne Figur (unkritisch) und **3 mit Figur** (gemeldet, siehe unten) |
| 2 · Figurengröße | bei allen 4 Motiven vorhanden, die „klein" verlangen · nirgends fälschlich gesetzt |
| 3 · Anschnittverbot | bei allen 26 Figurenmotiven |
| 4 · Handregel | bei allen 26 Figurenmotiven |
| 5 · Lichtregel | 35 sichtbar + 27 außerhalb + 22 Diagramm = 84/84, keins doppelt · harte Schattenregel in allen 62 Raumbildern |

Die Jahreszahlen der Epochenzeile sind **aus `skript.md` übernommen**, nicht
erfunden: Sweet Track 3807 v. Chr., Campemoor „rund sechseinhalbtausend Jahre",
Ägypten „vor etwa 4.500 Jahren", Babylon 569 v. Chr., Persien um 500 v. Chr.,
Chaco „etwa tausend Jahre zurück", Inka um 1450, Via Appia 312 v. Chr.

## Die Lichtregel — warum sie präzisiert wurde

Von den 62 Raumbildern kann die Quelle bei **27 (44 %) physisch nicht im Bild
sein**: Nahaufnahmen, Aufsichten, Luftbilder — und M02, wo `szenen.md`
ausdrücklich „kein Horizont" vorschreibt. Die Z3-Regel hätte dort 27-mal
reißen müssen. Präzisiert auf: **sichtbare Quelle, wo sie ins Bild passt, sonst
eindeutig gerichteter harter Schatten aus derselben einen Richtung.** Der harte,
flächige, verlauffreie Schatten — der eigentliche Bildeffekt von Z3 — ist in
beiden Fassungen unverändert gefordert.

## Motive ohne Epochenangabe in `szenen.md` — zu entscheiden

**A · Mit Figur, müssen entschieden werden (3):**

| Motiv | Spalte | Szene |
|---|---|---|
| **M41** | `Schema` | Die Figur schreitet den Zeitstrahl ab — abstrakt, Epoche offen |
| **M48** | `Detail` | Eine Hand auf versteinertem Holz — Zusammenhang ist Ägypten, steht aber nicht da |
| **M78** | `zeitlos` | Händler auf der alten Bohlenstraße — laut Skript bewusst zeitlos |

**B · Ohne Figur, aber epochengebundener Gegenstand (11):** M12, M17, M18, M20,
M31, M39, M42, M47, M77, M79, M80. Hier entscheidet die Epoche über Werkzeugform
und Bauart — etwa ob M18 Steinbeil und Holzkeil zeigt oder modernes Gerät, und
ob M47 ägyptisches Basaltpflaster wird.

**C · Abstrakte Schemata und Karten (21):** brauchen keine Epoche.

## Prüfergebnis des Nachlaufs

| Motiv | Fehler in v1 | jetzt |
|---|---|---|
| **M06** | modernes Hemd in urzeitlicher Szene | **Epoche geheilt** — Tunika, Ledergurt, Steinbeil · Schlagschatten korrekt |
| **M62** | ägyptischer Nemes in Chaco · Füße angeschnitten | **beides geheilt** — Pueblo-Tracht, Vollbild · Schlagschatten korrekt |
| **M84** | keine Lichtquelle · sieht nicht in die Kamera | **Kamerablick geheilt** · Lichtregel greift |
| **M49** | Figur am linken Rand angeschnitten | **geheilt** — drei vollständige Figuren · Schatten korrekt |
| **M72** | moderne Mütze auf Inka-Treppe · Klauenhände | **beides geheilt** — Andentracht, saubere Hände |

**Alle fünf ursprünglichen Fehler sind behoben.** Vier Punkte sind neu oder
geblieben:

### 1. Die Figurengrößen-Regel wirkt nicht (M06, M62)

`no more than one sixth of the picture height` steht im Prompt, die Figur nimmt
trotzdem rund die halbe Bildhöhe ein. Beide Motive verlangen laut `szenen.md`
„die Figur klein". Die Geisterkopf-Härtung wirkt weiterhin — keine schwebenden
Köpfe, keine Spiegelung — aber die Größenangabe wird ignoriert.

### 2. Der Schlagschatten fehlt bei M72 und M84

Beide zeigen keinen gerichteten Schatten der Figur. Bei M06, M62 und M49 sitzt
er korrekt. Der Unterschied: dort steht die Figur auf einer offenen Fläche, hier
auf einer Treppe (M72) beziehungsweise auf gemustertem Baugrund (M84).

### 3. Das Signaltürkis wird flächig statt punktuell gesetzt

| Motiv | Türkis sitzt auf |
|---|---|
| M06 | Beilklinge **und** Wasserflächen — zwei Stellen statt einer |
| M62 | zwei lange Streifen entlang beider Wegränder |
| M49 | dem **Basaltblock** — Basalt ist dunkel, nicht türkis |

Die Regel sagt „marks the one element the shot is about". Sie wird als
Farbfläche gelesen, nicht als Markierung.

### 4. Zwei Sachfehler, die den Inhalt betreffen

- **M49: der Schlitten hat Räder.** `szenen.md` verlangt einen Holzschlitten,
  und das Skript baut seine Kernaussage genau darauf auf — „The wheel is not the
  parent of the road". Ein Räderwagen in der Ägypten-Szene widerspricht dem
  Video an seiner wichtigsten Stelle.
- **M84: die Figur ist zum Bauarbeiter geworden** — Warnweste, Schutzhelm,
  Baustelle mit schwerem Gerät. M01 und M83 zeigen einen gewöhnlichen Passanten.
  Die Schlusseinstellung ist die Klammer zur Eröffnung; sie bricht.

## Stand

**Die zehn sitzen noch nicht.** Der Lauf ist gestoppt, die restlichen 74 sind
nicht gelaufen.

---

# Zweiter Nachlauf — 15.08.2026

**10 Credits.** Kontostand 2.849,9 → **2.839,9**. Gesamt für Video 1: **40 Credits**.
v2-Fassungen in [`_v2/`](_v2), Gegenüberstellung [`_v2-vs-v3.png`](_v2-vs-v3.png).

## Rad-Prüfung über alle 84 Motive

`szenen.md` **benennt** ein Rad, einen Wagen oder ein Zugtier in 11 Motiven —
dort ist es Absicht: M03 (moderne Fahrzeuge), M04/M05 (das Speichenrad als eine
der drei falschen Antworten), M38/M39/M82 (die gefundenen Wagenachsen),
M40/M41/M42 (Rad auf dem Zeitstrahl), M58 (persischer Reiter, Pferde sind dort
korrekt), M61 (durchgestrichenes Rad), M71 („kein Rad und kein Zugtier").

Das eigentliche Risiko ist umgekehrt: **37 weitere Motive liegen in Kulturen,
die laut `skript.md` kein Rad hatten oder es hier nicht benutzten.** Dort kann
das Modell eines hinzuerfinden, wie es bei M49 geschehen ist.

| Kultur | Beleg im Skript | betroffene Motive |
|---|---|---|
| Chaco | „The people there had no wheel, no horse, no ox" | M60, M62, M63, M64, M65, M66 |
| Anden | „had no wheel and no animal to pull a cart" | M67, M69, M70, M72 |
| Nordwesteuropäisches Moor | „built roads for some twenty centuries before anything rolled on one" | M06–M24, M27–M34, M37, M81 |
| Ägypten | „Crews hauled basalt blocks down it", Transport per Boot | M45–M51 |

Alle 44 (37 + die 7 neu zugeordneten Detail-Motive) tragen jetzt: *„This culture
has no wheeled transport at all: no wheels, no carts, no wagons, no barrows, no
chariots and no draught animals anywhere in the picture."* Bei den 12 Motiven,
in denen das Rad die Aussage trägt, steht der Satz **nicht** — geprüft, keine
Kollision.

## Ergebnis des zweiten Nachlaufs

| Motiv | vorher offen | jetzt |
|---|---|---|
| **M84** | Bauarbeiter, kein Schlagschatten | **bestanden** — gewöhnlicher Passant mit Schiebermütze wie in M01, Blick in die Kamera, harter Schlagschatten |
| **M72** | kein Schlagschatten | **bestanden** — Schatten fällt klar auf die Felswand, Türkis nur am Stirnband |
| **M06** | Größe, Türkis zweifach | Türkis **auf genau einem Objekt** (Anhänger), Schatten korrekt · **Größe weiterhin nicht befolgt** |
| **M62** | Größe, Türkis als Randstreifen | Türkis **auf genau einem Objekt** (Anhänger am Gürtel), Schatten korrekt, Vollbild · **Größe weiterhin nicht befolgt** |
| **M49** | Räder, Türkis auf Basalt | **Räder weg** — Schlitten auf losen Rundhölzern · **Türkis in mehreren Pflanzen** · **vier Figuren statt drei** |

### Die Größenregel greift auch in der dritten Fassung nicht

| Lauf | Formulierung | Ergebnis |
|---|---|---|
| 1 | nur der Szenentext („die Figur klein am Rand") | Figur groß und mittig |
| 2 | `no more than one sixth of the picture height` | unverändert groß |
| 3 | `a small distant element, the landscape dominates, roughly the lower quarter` | unverändert groß |

Drei Formulierungen, dreimal dasselbe Ergebnis. **Nach der Vorabentscheidung
gilt damit: die vier betroffenen Motive (M06, M08, M29, M62) laufen mit
normaler Figurengröße.** Die Geisterkopf-Härtung wirkt in allen drei Läufen
weiter — keine schwebenden Köpfe, keine gespiegelte Komposition.

### Die Türkis-Verschärfung wirkt — außer bei M49

In M06, M62 und M72 sitzt das Türkis nach der Verschärfung auf **genau einem**
Gegenstand. In M49 nicht: dort steht es in mehreren Pflanzen am Bildrand,
obwohl die Regel Vegetation ausdrücklich ausschließt. Der Unterschied ist
vermutlich, dass M49 als einziges dieser Bilder überhaupt Pflanzen im
Vordergrund hat.

### M49 — der kritische Fehler ist behoben, zwei neue sind da

**Die Räder sind weg.** Der Block liegt auf einem flachen Holzschlitten, der
über lose Rundhölzer gleitet — genau das, was das Skript beschreibt. Der
Widerspruch zur Kernaussage ist damit aufgelöst.

Offen bleiben zwei Punkte:
- **Türkis in der Vegetation**, mehrfach.
- **Vier Figuren statt drei.** Der Prompt sagt „three haulers in a line";
  im Bild stehen vier Personen, davon eine Frau in weißem Kleid, die nicht
  zieht und im Szenentext nicht vorkommt.

## Stand

**Neun von zehn sitzen.** Offen ist allein **M49**.

---

# M49, dritter Nachlauf — bestanden

**2 Credits.** Kontostand 2.839,9 → **2.837,9**. Gesamt Video 1: **42 Credits**.

Zwei Änderungen: die Figurenzahl hart gesetzt („exactly three men and no one
else … there is no fourth person anywhere in the picture") und der
Szenentext um „bare open desert road, no plants, no shrubs, no palms and no
grass" ergänzt. Dazu trägt M49 als einziges Motiv jetzt `KEIN_SIGNAL` —
die Türkisregel erlaubt Abwesenheit ausdrücklich, aber ohne den Satz sucht
sich das Modell einen Träger, und in diesem Bild waren das die Pflanzen.

| Prüfpunkt | Ergebnis |
|---|---|
| Figurenzahl | **genau drei**, alle am selben Seil, keine vierte Person |
| Räder | **keine** — flacher Holzschlitten auf losen Rundhölzern |
| Türkis | **abwesend**, wie vorgegeben |
| Anschnitt | alle drei vollständig im Bild |
| Brauen · Hände · Text | ✓ · ✓ · kein Text |
| Schlagschatten | hart, einheitlich nach links, auch unter dem Block |
| Epoche | Altes Reich — Schendyt, rasierte Köpfe, Pyramiden im Hintergrund |

## Stand: alle zehn sitzen

| Motiv | Fassung | Anmerkung |
|---|---|---|
| M01 · M55 · M12 · M25 · M53 | v1 | seit dem ersten Lauf unverändert bestanden |
| M06 · M62 | v3 | Figurengröße nach Vorabentscheidung als normal hingenommen |
| M72 · M84 | v3 | vollständig bestanden |
| M49 | v4 | vollständig bestanden |

Die früheren Fassungen liegen in `_v1/`, `_v2/` und `_v3/`.

---

# Hauptlauf Stapel 1 (M02–M14) — gestoppt

**22 Credits** (11 Bilder). Kontostand 2.837,9 → **2.815,9**. Gesamt Video 1: **64 Credits**.

## Bestehensquote: 8 von 11

| bestanden | durchgefallen |
|---|---|
| M03 · M04 · M05 · M07 · M08 · M11 · M13 · M14 | **M02 · M09 · M10** |

- **M02** — Türkis auf **zwei** Stellen der Asphaltfläche statt auf einer.
- **M09** — zeigt eine **ganze stehende Figur** statt der verlangten Nahaufnahme
  eines im Moorwasser versinkenden Stiefels.
- **M10** — die Marschlandschaft **vor** dem Bau zeigt bereits einen fertigen
  Bohlensteg und Hütten. Beides steht nicht im Szenentext und widerspricht der
  Stelle im Skript.

## Die gemeinsame Ursache: FRAMING gegen Nahaufnahme

`FRAMING_EINZEL` verlangt bei **jedem** Figurenmotiv wörtlich *„full body
visible, not cropped — head, both hands and both feet inside the picture"*.
Bei M09 lautet die Szene aber *„close view of bog ground: a boot sinks to the
shaft"* — ein Stiefel, kein Mensch. Die beiden Vorgaben widersprechen sich, und
das Modell folgt der stärkeren: es baut eine ganze Figur.

**Fünf Motive sind betroffen**, vier davon noch nicht gelaufen:

| Motiv | Szene zeigt | Status |
|---|---|---|
| **M09** | einen Stiefel | durchgefallen |
| **M19** | die Hände der Figur beim Pflocksetzen | noch nicht gelaufen |
| **M33** | eine Hand, die eine Kurve zeichnet | noch nicht gelaufen |
| **M48** | eine Hand auf versteinertem Holz | noch nicht gelaufen |
| **M83** | moderne Schuhe am Wegrand | noch nicht gelaufen |

Ohne Korrektur fallen die vier übrigen mit derselben Begründung durch. Nötig
ist ein dritter FRAMING-Fall für Körperteil-Aufnahmen: *„this is a close view of
a part of the body only — a hand, a foot, a boot; do not draw the whole person,
do not add a face"*.

## Die Größenregel — erster echter Befund

**Bei M08 greift sie.** Die Figur steht klein in der Moorfläche, etwa ein
Viertel der Bildhöhe, dem Bildraum klar untergeordnet — genau wie beschrieben.
Das ist das erste Mal in vier Läufen, dass die Regel sichtbar wirkt.

| Motiv | Größenregel greift |
|---|---|
| M06 | nein (drei Läufe) |
| M62 | nein (drei Läufe) |
| **M08** | **ja** |
| M29 | noch nicht gelaufen |

Der Unterschied zu M06 und M62: M08 hat keinen dominanten Vordergrund und keine
Fluchtlinie, an der sich das Modell orientiert. Bei M29 wird sich zeigen, welche
der beiden Lagen die Regel bestimmt.

---

# Hauptlauf Stapel 2 (M02, M09, M10, M15–M22)

**22 Credits.** Kontostand 2.815,9 → **2.793,9**. Gesamt: **86 Credits**.

## Bestehensquote: 8 von 11 — unter der Abbruchschwelle

| bestanden | durchgefallen |
|---|---|
| M02 · M09 · M15 · M17 · M18 · M19 · M20 · M21 | **M10 · M16 · M22** |

**Der FRAMING-Fix wirkt.** M09 zeigt nur Stiefel und Unterschenkel, M19 nur
Hände und Unterarme — beide ohne Kopf, ohne Gesicht, ohne stehende Figur. Genau
das war die gemeinsame Ursache aus Stapel 1.

**Die Epochenzeile wirkt sichtbar bei M18:** Steinbeil mit Holzschaft,
Holzkeil, Holzschlegel — kein Metall, kein modernes Gerät. Das war der Fall,
an dem sich die Zuordnung entscheiden sollte.

Die drei Fehlschläge haben **keine gemeinsame Ursache**, es sind Einzelfälle:

- **M10** — die Landschaft ist jetzt frei von Steg und Hütten, wie verlangt,
  aber es liegt ein **türkises Boot** im Wasser. Ein Boot ist ein gebautes
  Ding und widerspricht „untouched wetland before anything was ever built".
- **M16** — das türkise Element auf der Karte liest sich als **Buchstabe „P"**,
  was gegen `no letters` verstößt; außerdem trägt die Karte die Lage
  Insel-links/Höhenrücken-rechts nur schwach.
- **M22** — **zwei türkise Objekte** statt einem: ein Pfosten am Weg und ein
  kleiner Gegenstand rechts unten.
