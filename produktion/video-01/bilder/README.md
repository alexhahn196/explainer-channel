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
