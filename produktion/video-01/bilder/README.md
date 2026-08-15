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
