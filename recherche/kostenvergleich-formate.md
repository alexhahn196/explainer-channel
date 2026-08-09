# Kostenvergleich: drei Fremdformate gegen BibelTube

> **Stand 2026-08-07.** Reine Analyse, keine Generierung. Ausgegeben wurden
> **0 Credits** — alle Preise stammen aus `get_cost`, das kostenlos ist.
>
> Jede Zahl trägt eine Kennzeichnung: **[gemessen]** direkt erhoben ·
> **[hochgerechnet]** aus einer Stichprobe auf die volle Laufzeit skaliert ·
> **[unbekannt]** nicht ermittelbar, nicht geschätzt.

---

## 1. Die drei Kanäle

| | A — Wild Bird Survival | B — NextGen Manufacturing | C — Nebula Prophecy |
|---|---|---|---|
| Kanal-ID | `UCsYEZah0zh0XCIaOHrkh93Q` | `UCVBICP0SNaKk8iuWIyNSpWw` | `UCWQVu0eZccFkw3cwcJbUqJA` |
| Beigetreten | 2026-06-18 **[gemessen]** | 2025-11-08 **[gemessen]** | 2025-09-05 **[gemessen]** |
| Videos | 44 **[gemessen]** | 57 **[gemessen]** | 6 **[gemessen]** |
| Abonnenten | 20.900 | 146.000 | 92.800 |
| Kanal-Views gesamt | 12,3 Mio. | 30,2 Mio. | 15,5 Mio. |
| Referenzvideo | `oqC5OVJhSj0` | `tJ6G2lTo6xA` | `vy96cmv-2ck` |
| Laufzeit | **480 s** (8:00) | **988 s** (16:28) | **1220 s** (20:20) |
| Views des Referenzvideos | 2,27 Mio. | 5,32 Mio. | 10,41 Mio. |

**Kadenz.** Die Vorgabe nennt 5,75 / 1,25 / 0,75 Uploads pro Woche. Aus
Beitrittsdatum und Videozahl gerechnet ergibt sich **[gemessen]**: A 6,2/Wo
(44 Videos in 7,1 Wochen), B 1,5/Wo (57 in 38,9 Wochen), C **0,13/Wo**
(6 in 48 Wochen). Bei A und B liegen beide Werte nah beieinander; bei **C
klafft eine Lücke** — 0,75/Wo passt nicht zu 6 Videos in 48 Wochen. Die
Rechnung unten benutzt die vorgegebenen Werte, weil sie die *aktuelle* Kadenz
abbilden dürften; für C ist das die unsicherste Annahme des ganzen Dokuments.

### Materialquelle — die Kernfrage bei Kanal A

Die Kanalbeschreibung von A nennt **keine** Materialquelle. Die Beschreibung
des Referenzvideos wirbt mit „stunning **8K documentary realism**" — eine
Formulierung, die Realismus behauptet, statt reale Aufnahmen zu belegen.

Die Bildanalyse beantwortet es eindeutig **[gemessen, 3-Minuten-Fenster]**:

> „All 78 shots are **AI-generated video**. There is no real filmed footage,
> static images, or traditional 3D renders. […] birds often morph into the
> buffalo's skin, fish appear or disappear inconsistently, and the buffalo's
> movements lack natural weight and anatomical precision."

**Kanal A arbeitet mit KI-Video, nicht mit lizenziertem Tiermaterial.** Damit
ist er in Credits rechenbar. Inhaltlich passt das ins Bild: Das Video zeigt
hunderte Fische, die einen Büffel putzen, während Madenhacker oberhalb der
Wasserlinie arbeiten — eine Szene, die als echte Aufnahme kaum existiert.

Die beiden anderen Kanäle deklarieren sich selbst:

- **B:** „All visuals and animations are **100% synthetic, AI-generated**
  conceptual representations. No real footage of the construction sites or
  personnel was used." **[gemessen, Videobeschreibung]**
- **C:** „all crafted **entirely with AI tools**" **[gemessen,
  Kanalbeschreibung]**

---

## 2. Bildbedarf — gemessen und hochgerechnet

Je Kanal wurde ein **3-Minuten-Fenster aus der Mitte** analysiert.

| | A | B | C |
|---|---|---|---|
| Analysiertes Fenster | 180–360 s | 400–580 s | 500–680 s angefragt, **nur 500–528 s geliefert** |
| Fensterlänge | 180 s **[gemessen]** | 180 s **[gemessen]** | **28 s [gemessen]** |
| Schnitte im Fenster | 78 | 32 | 9 |
| **Mittlere Schnittlänge** | **2,31 s** | **5,62 s** | **3,11 s** |
| Wiederholung / Loop | keine | keine | keine |
| Einstufung durch die Bildanalyse | 78/78 KI-Video | 30/32 „real gefilmt", 1 KI, 1 3D-Render | 9/9 „real gefilmt" |

### Die Einstufung „real gefilmt" ist bei B und C nicht belastbar

Bei **C** stuft die Analyse neun Einstellungen als „real filmed footage"
ein und ergänzt: *„The mermaid tail motion appears physically real,
consistent with professional film production."* Das Video handelt von einer
**Lamia** — einem Schlangenwesen. Reale Filmaufnahmen davon gibt es nicht.
Die Einstufung ist hier **nachweislich falsch**, und der Kanal sagt selbst,
er arbeite ausschließlich mit KI.

Damit ist auch das B-Ergebnis entwertet: Wenn der Klassifikator hochwertige
KI-Bilder als „professionelle Filmproduktion" liest, dann sagt „30 von 32 real
gefilmt" bei B nichts über die Quelle aus — es sagt etwas über die Qualität.
**Belastbar bleibt aus diesen Läufen nur die Schnittzahl und die Schnittlänge**,
nicht die Typzuordnung. Für die Materialfrage zählen deshalb die
Selbstauskünfte der Kanäle, und die lauten bei B und C: vollständig KI.

Bei **A** stützen sich Selbstauskunft (keine) und Klassifikator (78/78 KI)
nicht gegenseitig — aber der Klassifikator nennt hier **konkrete Artefakte**
(morphende Vögel, verschwindende Fische, fehlendes Gewicht). Solche Befunde
sind das Gegenteil eines „sieht echt aus"-Fehlurteils und daher belastbar.

### Hochrechnung auf die volle Laufzeit

> **Ausdrücklich eine Hochrechnung.** Sie unterstellt, dass die Schnittfrequenz
> des Mittelfensters für das ganze Video gilt. Anfang und Ende sind bei solchen
> Formaten typischerweise schnittdichter (Hook) bzw. ruhiger (Abspann), die
> Zahlen sind also eher Unter- als Obergrenzen.

| | A | B | C |
|---|---|---|---|
| Laufzeit | 480 s | 988 s | 1220 s |
| ÷ mittlere Schnittlänge | 2,31 s | 5,62 s | 3,11 s |
| **Clips je Video [hochgerechnet]** | **209** | **176** | **393** |

Bei C beruht diese Zahl auf einem **28-Sekunden-Fenster** — ein Sechstel der
angefragten Stichprobe. Sie ist die schwächste Hochrechnung des Dokuments.

---

## 3. Skript und Ton

| | A | B | C |
|---|---|---|---|
| Transkript verfügbar | ja | ja | **nein [unbekannt]** |
| Wörter | **469 [gemessen]** | **1.946 [gemessen]** | **[unbekannt]** |
| Sprechtempo über die volle Laufzeit | 58,6 WPM | 118,2 WPM | **[unbekannt]** |
| Sprache endet bei | 6:43 von 8:00 | 16:24 von 16:28 | **[unbekannt]** |
| Sprachanteil | 84,0 % | 99,6 % | **[unbekannt]** |
| TTS-Zeichen nach unserer Formel | ~2.500 | ~10.372 | **[unbekannt]** |

Umrechnung Wörter → Zeichen mit dem an der eigenen Produktion gemessenen
Faktor **5,33 Zeichen je Wort** (Video 02: 30.821 Wörter → 164.283 Zeichen).

**A spricht auffällig wenig**: 469 Wörter auf 8 Minuten, und die letzten
77 Sekunden sind reine Bild- und Tonkulisse. Das Format trägt sich über Bilder,
nicht über Text — das Gegenteil unseres Formats.

**Was die TTS in Euro kostet, ist [unbekannt].** Fish Audio wird nicht über
Higgsfield-Credits abgerechnet, und `config.md` führt bewusst keinen Preis
(nur den Schlüssel als Umgebungsvariable). Für alle vier Formate fehlt diese
Position also gleichermaßen.

---

## 4. Preise — gemessen über `get_cost`

**Seedance 1.5 Pro, 1080p, 16:9** (nur 4, 8 und 12 s wählbar):

| Dauer | `get_cost` | je Sekunde |
|---|---|---|
| 4 s | **12 Credits** | 3,0 |
| 8 s | **24 Credits** | 3,0 |
| 12 s | **36 Credits** | 3,0 |

**Standbild** `nano_banana_2`, 16:9: **1,5 Credits** bei 1k, **2 Credits** bei
2k **[gemessen]**.

### Ein Preisunterschied, der die ganze Rechnung verschiebt

`get_cost` nennt für einen 12-Sekunden-Clip **36 Credits**. Abgerechnet wurden
für unsere Clips durchgängig **18 Credits** — belegt im Transaktionsprotokoll
(je 4 × −18 am 6. und 7. August). **Der Ist-Preis ist die Hälfte des
Listenpreises.** Vermutlich eine Vergünstigung des Ultra-Abos; die Ursache ist
aus den Werkzeugen nicht ableitbar und damit **[unbekannt]**.

Gerechnet wird unten mit dem **Ist-Faktor 0,5**, also 6 Credits je 4-s-Clip.
Ein Wettbewerber ohne diese Vergünstigung zahlte das Doppelte.

### Euro je Credit

| Weg | Preis | € je Credit |
|---|---|---|
| Ultra-Jahresabo | 99 €/Jahr für 3.000 Cr./Monat = 36.000 Cr. | **0,00275 €** |
| Top-up 4.000 Cr. | 190 € | **0,0475 €** |
| Top-up 2.000 Cr. | 95 € | 0,0475 € |
| Top-up 1.000 Cr. | 49 € | 0,0490 € |
| Top-up 500 Cr. | 26 € | 0,0520 € |

Der Abo-Preis ist **17-mal günstiger** — gilt aber nur für die ersten 3.000
Credits im Monat. Alles darüber sind Top-up-Credits. Für A, B und C liegt der
Monatsbedarf weit über 3.000, deshalb rechnet die Tabelle unten mit dem
**Top-up-Preis 0,0475 €**. Für BibelTube gilt das Gegenteil: 437 Credits im
Monat passen ins Abo.

---

## 5. Der Vergleich

Alle Videoclips zum günstigsten Tarif (4-s-Clips, ein Clip je Schnitt),
Ist-Preis, Top-up-Kurs.

| | **BibelTube** | A — Wild Bird | B — NextGen | C — Nebula |
|---|---|---|---|---|
| Laufzeit | **3,50 h** (12.600 s) | 480 s | 988 s | 1220 s |
| Mittlere Schnittlänge | **3.150 s** (4 Clips à 12 s, geloopt) | 2,31 s | 5,62 s | 3,11 s |
| Clips je Video | **4 [gemessen]** | 209 **[hochger.]** | 176 **[hochger.]** | 393 **[hochger.]** |
| Credits je Video | **72 [gemessen]** | 1.254 | 1.056 | 2.358 |
| € je Video (Top-up) | **3,42 €** | **59,56 €** | **50,16 €** | **112,00 €** |
| € je Video (Abo-Kurs) | **0,20 €** | 3,45 € | 2,90 € | 6,48 € |
| **€ je Minute Endprodukt** | **0,016 €** | **7,45 €** | **3,05 €** | **5,51 €** |
| Uploads/Woche | 1,4 (Plan: 5 Tage Abstand) | 5,75 | 1,25 | 0,75 |
| Videos/Monat | 6,1 | 24,9 | 5,4 | 3,2 |
| **Credits/Monat** | **437** | **31.246** | **5.720** | **7.664** |
| Umsatz/Monat | **[unbekannt]** — kein Video veröffentlicht | 17.107 $ | 45.159 $ | 51.450 $ |
| Bildkosten/Monat | **21 €** (im Abo enthalten) | **1.484 €** | **272 €** | **364 €** |
| Umsatz − Bildkosten | — | ~15.600 $ | ~44.900 $ | ~51.100 $ |

> Umsatzangaben stammen aus der Aufgabenstellung, nicht aus eigener Messung.
> Die Mischung aus $ (Umsatz) und € (Kosten) ist bewusst nicht umgerechnet —
> ein Wechselkurs wurde nicht erhoben und wäre **[unbekannt]**.

### Was daran auffällt

**Die Bildkosten sind bei allen dreien Rundungsfehler.** Selbst der teuerste
Kanal C gibt bei dieser Rechnung ~364 € im Monat für Bilder aus und nimmt
51.450 $ ein — **0,7 % vom Umsatz**. Bei A sind es 8,7 %, bei B 0,6 %. Wer
glaubt, KI-Videokosten seien die Hürde in diesem Geschäft, rechnet am Problem
vorbei.

**Unser Format ist 190- bis 460-mal günstiger je Minute** — aber das ist kein
Verdienst, sondern eine Formateigenschaft. Ein Einschlafvideo darf sich nicht
bewegen; ein Wildlife-Video muss es. Wir zahlen 4 Clips für 3,5 Stunden, weil
der Zuschauer die Augen zumachen soll. **Die Zahl belegt nicht, dass unser
Format besser ist — sie belegt, dass die beiden Formate nicht vergleichbar
produzieren.**

**Die eigentliche Größe ist Umsatz je Video, nicht Kosten je Video.** C macht
mit **6 Videos** 51.450 $/Monat. A braucht dafür 44 Videos und kommt auf ein
Drittel. Der Unterschied liegt nicht in der Produktion, sondern in RPM und
Zugkraft: A hat einen RPM von 1,55 (Angabe aus der Aufgabenstellung), also
einen Cent-Bereich je 1.000 Views.

---

## 6. Was in den Credits **nicht** steckt

Die Tabelle oben zählt ausschließlich Bildgenerierung. Nicht enthalten und für
alle vier Formate **[unbekannt]**:

- **Skriptarbeit.** B schreibt 1.946 Wörter recherchierten Fachtext je Video —
  Zahlen zu Caisson-Gewichten, Baukosten, Erdbebendaten. Ob das ein Mensch,
  ein Sprachmodell oder eine Mischung schreibt, ist von außen nicht sichtbar.
- **Recherche und Faktenprüfung.** Bei B der größte unsichtbare Posten.
- **Schnitt und Montage.** 209 bzw. 393 Clips zu einem Video zu fügen, ist
  Arbeitszeit — bei uns erledigt das die Pipeline, dort vermutlich nicht.
- **Musik- und Materiallizenzen.** B nennt InAudio als Musikquelle
  **[gemessen, Videobeschreibung]**; Preis unbekannt. A und C nennen nichts.
- **Sprachsynthese.** Siehe Abschnitt 3 — nicht in Credits abgerechnet.
- **Thumbnails.** Bei uns 2 Credits je Bild; bei den dreien unbekannt, aber
  gegenüber 200–400 Videoclips vernachlässigbar.
- **Verworfene Generierungen.** Unsere eigene Erfahrung: Für Video 04 waren
  **sechs** Standbilder nötig, um eines zu bekommen, das die Prüfliste besteht
  — ein Ausschuss von 67 %. Auf 209 oder 393 Clips hochgerechnet wäre das ein
  erheblicher Aufschlag, den keine Preisliste ausweist.

---

## 7. Offene Punkte

| Frage | Status |
|---|---|
| Warum kostet ein 12-s-Clip 18 statt der ausgewiesenen 36 Credits? | **[unbekannt]** — Werkzeuge geben keine Auskunft |
| Womit produziert B tatsächlich? Selbstauskunft „100 % KI" gegen Klassifikator „30/32 real" | **ungeklärt**, Klassifikator bei C widerlegt |
| C: Schnittlänge nur aus 28 s statt 180 s | Hochrechnung schwach, Wiederholung mit vollem Fenster nötig |
| C: Kadenz 0,75/Wo laut Vorgabe gegen 0,13/Wo aus Beitrittsdatum | widersprüchlich |
| C: Skriptlänge | **[unbekannt]**, kein Transkript |
| Wechselkurs $/€ | nicht erhoben |
| Lizenzkosten für Musik und Fremdmaterial | **[unbekannt]** bei allen dreien |
