# Schreibstil — Unknown Frequencies

> Erhebung vom **2026-08-15**, **0 Credits**, keine Videosichtung.
> Kanal `UCm1yxl_4qMbStLHpHQu6xWg` (@unknownfrequencies-tv), 56.200 Abos,
> **16 Videos**, **5.341.005 Views**, seit 26.10.2024, Land US.
> Werkzeuge: `youtube_channel_about` (1×), `youtube_channel_videos` (1×),
> `get_bulk_video_subtitles` / `get_video_subtitle` (16 Untertitelspuren),
> `get_bulk_video_transcripts` (1×, nur zur Methodenprüfung).
>
> **Aus den Transkripten wird kein Text zitiert.** Der Bericht enthält
> ausschließlich Zahlen, Anteile und Beschreibungen. Das Messskript steht in
> `recherche/daten/uf_schreibstil_messen.py`.
>
> Kennzeichnung: **[gemessen]** = direkt aus Tool-Ergebnis oder eigener
> Rechnung · **[abgeleitet]** = Deutung gemessener Werte · **[unbekannt]** =
> nicht ermittelbar.

## Vorbemerkung: wo die Bezugsdateien liegen

**Erledigt am 16.08.2026.** Bei der Erhebung lagen vier der genannten Dateien
nur auf nicht zusammengeführten Branches, und die Verweise unten liefen ins
Leere. Seit dem Merge aller offenen Branches
(`regeln/ink-vs-axen.md`, `regeln/daten/skriptanatomie_inkaxen.py`,
`produktion/video-01/skript.md`, `recherche/stil-unknown-frequencies.md`)
liegen sie hier, und alle Verweise in diesem Bericht greifen.

Die Bildwelt-Messung hält ausdrücklich fest: *„Kein Ton, keine Sprache, kein
Skript"*. Der Text war tatsächlich nie vermessen. Die Sprechweise ist es
inzwischen — soweit möglich — ebenfalls:
[`recherche/sprechweise-unknown-frequencies.md`](sprechweise-unknown-frequencies.md).

## Methodenprüfung: sind die Werte mit Ink/Axen vergleichbar?

`skriptanatomie_inkaxen.py` wurde **unverändert importiert** und mit denselben
Funktionen (`segmente`, `messen`, `titel_kernwoerter`, dieselben Pronomen- und
Antwortmarker-Regexe) auf die 16 Transkripte angewandt. Die epistemischen
Marker stammen aus der kalibrierten Wortliste in
`regeln/daten/skript_metriken.py`.

Die Transkripte wurden über die signierten Untertitel-URLs geladen, nicht über
`get_bulk_video_transcripts`. **Gegenprobe an Video 1** (`EhT6IhuZQp4`):
beide Wege liefern **213 Segmente, identische `startMs`-Werte
(400, 3439, 5680, …), identischen Text, identisches Schlusssegment**
[gemessen]. Der Satzproxy hängt an den Segmentgrenzen — diese Prüfung war
die Bedingung dafür, die Werte überhaupt neben Ink und Axen stellen zu dürfen.
Sie ist bestanden.

**Vier Einschränkungen bleiben:**

1. **Der Kernfrage-Wert ist hier weitgehend gegenstandslos.** Er sucht das
   Titel-Fragewort. Unknown Frequencies hat **0 von 16 Titeln mit Fragezeichen**
   (Ink: 85 % Frageform, Axen: 77 %); nur 3 Titel beginnen mit einem Fragewort.
   Bei **6 von 16** Videos ist der Wert gar nicht messbar [gemessen]. Er steht
   der Vollständigkeit halber in der Tabelle und trägt keine Aussage.
2. **Die Veröffentlichungsdaten sind monatsgenau**, nicht taggenau — sie
   stammen aus `publishedTimeText`. Die **Reihenfolge** ist zuverlässig.
3. **ASR-Transkripte schreiben Eigennamen falsch.** Die Personenzählung in
   Teil 3 ist deshalb eine Größenordnung, keine exakte Zahl.
4. **Die epistemischen Werte für Ink und Axen** stammen aus einer anderen
   Teilerhebung (je ein Treffer- und ein schwaches Video), nicht aus dem
   Median über 13 Videos. Nur eingeschränkt vergleichbar.

---

# TEIL 1 — Die 16 Transkripte, vermessen

## 1.1 Der Befund, der alles andere ordnet: der Kanal hat zwei Skriptformen

Die Werte streuen nicht zufällig. Sie zerfallen in **zwei Gruppen**, und die
Trennlinie ist das Format, nicht die Zeit [gemessen]:

- **POV-Form (9 Videos)** — „POV: You're…", „Your Life as Every … Rank",
  „What It Was Like…", „…from the Soldier's Perspective", „What 24 Hours…"
- **Chronik-Form (7 Videos)** — „The ENTIRE History of…", „The Entire Story
  of…", „The Reason…", „Evolution of…"

Der Unterschied in der Zuschaueransprache beträgt **Faktor 10**:

| Größe | POV (n=9) | Chronik (n=7) |
|---|---:|---:|
| **zweite Person je 1.000 Wörter** | **74,7** | **7,4** |
| Fragezeichen-Sätze gesamt | 5 | 87 |
| benannte Personen je Video (Median) | 6 | 19 |
| Satzlänge Median (echte Interpunktion) | 7,0 | 9,0 |
| Sätze unter 5 Wörtern | 29,4 % | 16,6 % |
| Wörter je Video (Median) | 1.697 | 2.249 |

Die Formen laufen zeitlich **parallel**, nicht nacheinander: Video 8 ist
Chronik, 9 und 10 sind wieder POV. Erst ab Video 11 überwiegt die Chronik.
Wer „den Schreibstil von Unknown Frequencies" übernehmen will, muss zuerst
entscheiden, **welchen der beiden**.

## 1.2 Einzelwerte, alle 16 Videos

Reihenfolge = Uploadreihenfolge. `du/wir/man/sie` = Perspektivpronomen je
1.000 Wörter. Satzlänge = ASR-Satzproxy (mit Ink/Axen vergleichbar).
`epi` = epistemische Marker je 1.000 Wörter [alle Werte gemessen].

| # | Form | Titelkurz | Views | Wörter | s | WPM | Kernfr. % | Antw. % | Drittel | du | wir | man | sie | Satz | kurz % | epi |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | POV | U.S. Soldier | 396k | 1.504 | 537 | 168 | 34,5 | 21,3 | erstes | **103,1** | 0,7 | 3,3 | 9,3 | 7 | 85,2 | 0,7 |
| 2 | POV | German Rank | 992k | 1.436 | 541 | 159 | 18,5 | 43,1 | zweites | 95,4 | 0,0 | 2,8 | 26,5 | 6 | 79,3 | 0,0 |
| 3 | POV | German Soldier | 774k | 1.983 | 721 | 165 | 3,9 | 31,7 | erstes | 74,6 | 0,5 | 6,6 | 30,8 | 7 | 82,6 | 0,0 |
| 4 | POV | British Rank | 315k | 1.697 | 604 | 169 | 12,1 | 1,7 | erstes | 83,7 | 1,2 | 5,3 | 14,1 | 7 | 78,5 | 0,0 |
| 5 | POV | Japanese Rank | 97k | 1.513 | 568 | 160 | 3,0 | 57,5 | zweites | **105,8** | 0,0 | 3,3 | 16,5 | 7 | 81,4 | 0,7 |
| 6 | POV | Iwo Jima | 222k | 1.942 | 733 | 159 | — | 35,5 | zweites | 46,9 | 2,6 | 7,2 | 14,9 | 6 | 78,4 | 0,0 |
| 7 | POV | WW1 Trench | 144k | 1.900 | 644 | 177 | 43,6 | 24,0 | erstes | 74,7 | 0,5 | 4,7 | 8,9 | 7 | 86,0 | 1,1 |
| 8 | Chr | ENTIRE WW1 | 549k | 2.024 | 753 | 161 | — | 0,8 | erstes | 10,9 | 6,9 | 6,4 | 12,4 | 7 | 79,4 | 0,0 |
| 9 | POV | Japanese Sailor | 47k | 1.743 | 594 | 176 | 10,7 | 25,3 | erstes | 39,6 | 0,6 | 8,0 | 13,2 | 7 | 82,7 | 0,6 |
| 10 | POV | Vietnam | 19k | 1.655 | 540 | 184 | — | 16,2 | erstes | 66,5 | 0,0 | 6,6 | 5,4 | 7 | 82,9 | 0,0 |
| 11 | Chr | Deadliest Battle | 140k | 2.427 | 855 | 170 | 2,6 | 2,1 | erstes | 7,4 | 4,9 | 7,0 | 11,1 | 6 | 79,2 | 0,0 |
| 12 | Chr | Bulge | 46k | 2.027 | 722 | 168 | 0,7 | 53,6 | zweites | **1,5** | 3,5 | 2,5 | 12,3 | 7 | 77,6 | 0,0 |
| 13 | Chr | ENTIRE WW2 | 293k | 2.249 | 823 | 164 | — | 0,8 | erstes | 4,9 | **10,7** | 8,9 | 12,0 | 6 | 78,9 | 0,4 |
| 14 | Chr | Odyssey | **1.100k** | 2.348 | 789 | 179 | — | 1,0 | erstes | 8,9 | 3,4 | 11,5 | 20,0 | 7 | 84,7 | 0,9 |
| 15 | Chr | Trojan War | 183k | 2.395 | 795 | 181 | — | 1,8 | erstes | 9,6 | 2,1 | 11,7 | 8,4 | 7 | 81,7 | 0,4 |
| 16 | Chr | Greek Soldier | 12k | 1.857 | 665 | 168 | 7,3 | 79,5 | drittes | 4,3 | 5,9 | 5,9 | 8,6 | 6 | 76,0 | **6,5** |

Video 16 ist **3 Tage alt** — seine 12k sind kein Ergebnis, sondern ein
Zwischenstand.

## 1.3 Mediane

| Größe | alle 16 | POV (9) | Chronik (7) |
|---|---:|---:|---:|
| Wörter je Video | 1.921 | 1.697 | 2.249 |
| Dauer (s) | 693 | 594 | 789 |
| **Sprechtempo (WPM)** | **168** | **168** | **168** |
| Kernfrage bei … % | 9,0 | 12,1 | 2,6 |
| Antwortmarker bei … % | 22,6 | 25,3 | **1,8** |
| zweite Person (du) | 43,2 | **74,7** | 7,4 |
| erste Person Plural (wir) | 1,6 | 0,5 | 4,9 |
| unbestimmt (man) | 6,5 | 5,3 | 7,0 |
| dritte Person (sie) | 12,4 | 14,1 | 12,0 |
| Satzlänge (ASR-Proxy) | 7,0 | 7,0 | 7,0 |
| Wörter unter 7 Zeichen | 80,4 % | 82,6 % | 79,2 % |
| **epistemische Marker /1.000 W** | **0,2** | **0,0** | **0,4** |

**Antwortmarker im ersten Drittel: 11 von 16** (POV 6/9, Chronik 5/7).

## 1.4 Aufbau in Fünfteln

Wörter je Fünftel, Median — das Sprechtempo ist über die Laufzeit **fast
konstant**, der Text ist gleichmäßig verteilt [gemessen]:

| | 1. | 2. | 3. | 4. | 5. |
|---|---:|---:|---:|---:|---:|
| alle 16 (Anteil) | 20,8 % | 20,5 % | 20,1 % | 19,8 % | 18,9 % |
| POV (Wörter) | 348 | 341 | 347 | 341 | 310 |
| Chronik (Wörter) | 468 | 448 | 424 | 449 | 445 |

Zweite Person je 1.000 Wörter je Fünftel [gemessen]:

| | 1. | 2. | 3. | 4. | 5. |
|---|---:|---:|---:|---:|---:|
| alle 16 | 55,4 | 42,4 | 40,1 | 26,2 | 36,3 |
| **POV** | **76,0** | **93,8** | **67,3** | **76,2** | **60,4** |
| Chronik | 6,1 | 8,4 | 2,4 | 6,2 | 5,9 |

Das ist der auffälligste Verlaufsbefund: **die POV-Form baut die Ansprache
nicht ab.** Sie liegt im letzten Fünftel bei 60,4 — höher als Inks bester
Einstiegswert. Ink und Axen fallen beide nach dem ersten Fünftel steil ab
(Ink früh 52,0 → 1,8; Axen spät 17,4 → 20,0 → 8,6).

Zahlenangaben je Fünftel, Median: alle 16 `[12, 9,5, 10, 8, 10]` — ebenfalls
gleichmäßig, kein Zahlen-Cluster am Anfang [gemessen].

---

# TEIL 2 — Vergleich mit Ink Explainer, Axen und Video 1

Ink- und Axen-Werte aus `regeln/ink-vs-axen.md` §1.2–1.4 (Mediane über je
6 Videos). Eigene Werte aus `produktion/video-01/skript.md`, Sprechtext ohne
Quellen-IDs, 1.875 Wörter.

## 2.1 Die Tabelle

| Größe | UF POV | UF Chronik | Ink früh | Ink spät | Axen früh | Axen spät | Video 1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Wörter | 1.697 | 2.249 | 1.358 | 2.339 | 1.273 | 1.643 | 1.875 |
| Dauer (s) | 594 | 789 | 443 | 626 | 397 | 577 | 514¹ |
| **WPM** | **168** | **168** | 190,5 | **218,5** | 188,0 | 186,5 | 219¹ |
| **zweite Person** | **74,7** | 7,4 | 27,3 | 23,4 | 22,8 | 14,8 | 13,9 |
| erste Person Plural | 0,5 | 4,9 | 4,2 | 7,2 | 12,6 | 6,0 | 4,3 |
| unbestimmt (man) | 5,3 | 7,0 | 14,6 | 14,9 | 15,5 | 10,9 | 14,9 |
| dritte Person (sie) | 14,1 | 12,0 | 18,3 | 17,8 | 19,0 | 14,7 | 16,0 |
| Satzlänge (ASR-Proxy) | 7,0 | 7,0 | 7,0 | 7,0 | 6,0 | 6,0 | —² |
| Wörter unter 7 Zeichen | 82,6 % | 79,2 % | 80,1 % | 82,2 % | 77,0 % | 76,4 % | **90,9 %** |
| Antwortmarker bei … % | 25,3 | **1,8** | 21,5 | 5,4 | 7,0 | 9,6 | 13,2³ |
| **epistemisch /1.000 W** | **0,0** | **0,4** | 3,7⁴ | — | 0,6⁴ | — | **2,1** |
| zweite Person, 1. Fünftel | 76,0 | 6,1 | 52,0 | 42,5 | 37,3 | 17,4 | **42,7** |
| zweite Person, 5. Fünftel | **60,4** | 5,9 | 44,6 | 22,1 | 19,9 | 9,8 | 13,3 |

¹ gerechnet mit dem Zielwert 219 WPM, nicht gemessen — Video 1 ist nicht vertont.
² Der ASR-Satzproxy ist auf Skripttext mit echter Interpunktion nicht anwendbar. Auf gleicher Grundlage (echte Interpunktion) gemessen: **UF POV 7,0 · UF Chronik 9,0 · Video 1 11,0** Wörter je Satz.
³ Position des ersten **Antwortmarker-Wortes** („because", „the reason"…). Die inhaltliche Antwort steht laut Messtabelle des Skripts bei 5,7 % — sie ist ohne Markerwort formuliert und wird vom Regex nicht erfasst.
⁴ aus `regeln/daten/skript.json`, je ein Treffervideo — kein Median, siehe Methodenprüfung.

## 2.2 Wo Unknown Frequencies deutlich abweicht

**1. Das Sprechtempo ist das langsamste aller vier Kanäle.** 168 WPM gegen
Inks 218,5 in der starken Phase — **23 % langsamer** [gemessen]. Auffällig ist
die Konstanz: alle 16 Videos liegen zwischen 159 und 184 WPM, unabhängig von
Form, Länge und Datum. Das ist der einzige Wert, der über den gesamten Katalog
praktisch unverändert bleibt.

**2. Die Zuschaueransprache in der POV-Form ist dreimal so hoch wie bei Ink**
(74,7 gegen 23,4) und **baut sich nicht ab** (5. Fünftel 60,4 gegen Inks 22,1).
Das ist der größte Einzelunterschied im ganzen Vergleich.

**3. Epistemische Marker sind praktisch bei null.** POV-Median **0,0** — in
5 von 9 POV-Videos kommt **kein einziger** Unsicherheitsmarker vor [gemessen].
Ink liegt beim Treffervideo bei 3,7, unser Video 1 bei 2,1. Unknown Frequencies
behauptet ohne Absicherung. Die einzige Ausnahme ist Video 16 mit 6,5 — dem
bislang schwächsten Video, allerdings erst 3 Tage alt.

**4. Die Chronik-Form beantwortet die Frage sofort:** Antwortmarker im Median
bei **1,8 %** der Laufzeit, gegen Inks bereits sehr frühe 5,4 %. In **4 der
7** Chronik-Videos fällt der Marker vor der 2-%-Marke, also im
Eröffnungsabschnitt. Die beiden Ausreißer (53,6 % und 79,5 %) sind die
Videos 12 und 16 — zugleich die beiden viewschwächsten Chronik-Videos, wobei
Video 16 erst 3 Tage alt ist. Bei n = 7 ist das ein Hinweis, kein Befund.

**5. Keine Frageform im Titel.** 0 von 16 gegen Ink 85 % und Axen 77 %.

**6. Deutlich weniger unbestimmte Perspektive** („one", „people"): 5,3–7,0
gegen 10,9–15,5 bei Ink und Axen. Unknown Frequencies redet nicht über
„die Menschen", sondern über *dich* oder über *ihn*.

## 2.3 Wo er den anderen gleicht

- **Satzlänge im ASR-Proxy: 7,0** — exakt Inks Wert, in beiden Formen
  [gemessen]. Der Wert trennt hier nichts.
- **Kurzwortanteil 79–83 %** — mitten im Feld (Ink 80,1–82,2 %,
  Axen 76,4–77,0 %).
- **Videolänge und Wortzahl** liegen im selben Korridor wie Inks späte Phase
  (2.249 gegen 2.339 Wörter).
- **Die Antwort fällt früh:** 11 von 16 im ersten Drittel — dieselbe Richtung
  wie Inks starke Phase.
- **Beide haben ihre Videos verlängert.** UF von 1.504 (Video 1) auf 2.395
  (Video 15) Wörter, +59 %; Ink +72 %. Nur hat UF dabei das Tempo **nicht**
  erhöht, Ink schon.

## 2.4 Wo unser Video-1-Skript steht

Unser Skript liegt bei fast jeder Größe **näher an Ink als an Unknown
Frequencies** — das war so beabsichtigt, die Zielwerte stammen aus dem
Ink-Axen-Vergleich. Drei Abweichungen von *beiden*:

- **Kurzwortanteil 90,9 %** — höher als jeder gemessene Kanal (Maximum sonst
  82,6 %). Deutlich außerhalb des Referenzbereichs.
- **Satzlänge 11,0** gegen UF 7,0/9,0 (gleiche Messgrundlage). Unsere Sätze
  sind rund die Hälfte länger; der Anteil sehr kurzer Sätze liegt bei 13,5 %
  gegen 29,4 % in der POV-Form.
- **Epistemische Marker 2,1** — zwischen Ink (3,7) und UF (0,0–0,4), und das
  ist die von der eigenen Recherche verlangte Seite.

Der Anspracheverlauf ist die auffälligste Parallele zu Ink und der klarste
Gegensatz zu UF: **42,7 → 0,0 → 8,0 → 5,3 → 13,3.** Wir sprechen den
Zuschauer im ersten Fünftel an und dann fast nicht mehr — genau Inks Muster.
Die POV-Form hält stattdessen 60–94 über die ganze Laufzeit.

---

# TEIL 3 — Das Unmessbare: die Erzählweise

Jede Beobachtung mit Häufigkeit. Kein Transkripttext.

## 3.1 Erzählt er chronologisch oder springt er?

**Überwiegend streng vorwärts, in beiden Formen — die Chronik springt mehr.**

| | POV (9) | Chronik (7) |
|---|---:|---:|
| genannte Jahreszahlen (Summe) | 41 | 67 |
| **Rücksprünge** (Jahr kleiner als das vorige) | **7** | **14** |
| Anteil Rücksprünge (Median) | 14,3 % | 20,6 % |
| Rückblenden-Marker (Summe) | 9 | 23 |
| Rückblenden-Marker (Median je Video) | 1 | 3 |

Fünf der neun POV-Videos haben **null Rücksprünge** [gemessen]. Vier von ihnen
sind zusätzlich durch **38 „Level"-Marken** in eine aufsteigende Leiter
gegliedert (9, 9, 10, 10 Marken) — ein streng monotoner Aufbau, der von der
untersten zur obersten Stufe durchläuft und nie zurückkehrt.

Die Chronik-Form springt doppelt so oft zurück und benutzt dreimal so viele
Rückblenden-Marker. Sie erzählt aber ebenfalls vom Anfang zum Ende — die
Sprünge sind Einschübe innerhalb einer vorwärtslaufenden Linie, keine
verschachtelte Konstruktion. Das stärkste Gegenbeispiel ist Video 16 mit
**5 Rücksprüngen bei 15 Jahreszahlen** (35,7 %).

## 3.2 Gibt es einen Erzähler mit Haltung?

**Der Erzähler ist als Person fast abwesend, bezieht aber am Schluss Position.**

| | alle 16 | POV | Chronik |
|---|---:|---:|---:|
| erste Person Singular je 1.000 W (Median) | **1,5** | 0,7 | 1,8 |
| Haltungsmarker je 1.000 W (Median) | **0,5** | 0,5 | 0,8 |
| Haltungsmarker gesamt | 21 | 7 | 14 |
| Imperative der Zuwendung (Summe) | 38 | 31 | 7 |

Zum Vergleich: die zweite Person liegt bei 43,2. Das Verhältnis „du" zu „ich"
beträgt über alle 16 Videos rund **29 : 1** [gemessen]. In **4 von 16** Videos
kommt die erste Person Singular **gar nicht** vor.

Einschränkung [unsicher]: In den drei Videos mit den höchsten Ich-Werten
(22, 15, 14 Treffer) ist aus dem ASR-Text **nicht trennbar**, ob „I" dem
Erzähler oder einer wiedergegebenen Figurenrede gehört. Gerade die
Mythologie-Videos enthalten viel Figurenrede. Die Zahl ist eine Obergrenze.

Haltung entsteht also nicht durch laufende Meinungswörter. Was stattdessen
messbar ist: das Muster „Das ist / Das war …" trifft **13-mal in 7 von 16
Videos** [gemessen] — eine kategorische Setzung statt einer Begründung.
Dass diese Sätze bevorzugt am Schluss stehen, ist **[abgeleitet]** aus dem
Schlussbefund in 3.5 (Wertungssatz statt CTA) und hier **nicht eigens
positionsgenau gemessen**.

## 3.3 Wie führt er Personen ein?

| | alle 16 | POV | Chronik |
|---|---:|---:|---:|
| benannte Personen je Video (Median) | 10 | **6** | **19** |
| Personen mit Rollen-Apposition (Median) | 2 | 1 | 5 |
| Summe benannter Personen | 185 | 54 | 131 |

**In der POV-Form ist die Hauptperson der Zuschauer selbst** — sie hat keinen
Namen. Namen tauchen dort als Nebenfiguren auf, im Median 6 je Video, davon
nur 1 mit erklärender Apposition.

Die Chronik-Form arbeitet mit **dreimal so vielen benannten Personen** und
führt im Median **5 davon mit Rollen-Apposition** ein (Name, Komma, Funktion —
oder „ein General namens X"). Das ist die Standardform; Personen werden also
überwiegend **funktional** eingeführt, nicht biografisch.

Einschränkung: ASR schreibt Eigennamen falsch, gezählt wurden nur Namen mit
mindestens zwei Vorkommen. Größenordnung, keine exakte Zahl.

## 3.4 Werden Fragen gestellt und offen gelassen?

**In der POV-Form so gut wie gar nicht. In der Chronik-Form ständig — und die
Mehrheit bleibt ohne Antwortmarker.**

| | alle 16 | POV | Chronik |
|---|---:|---:|---:|
| Fragezeichen-Sätze gesamt | 92 | **5** | **87** |
| davon ohne Antwortmarker in ~200 Wörtern | **59** | 3 | 56 |
| Anteil offen | **64 %** | — | 64 % |
| Median je Video | 1,5 | **0** | **13** |

Neun POV-Videos enthalten zusammen **5 Fragezeichen** — sechs von ihnen
**keines**. Die Chronik-Form stellt im Median 13 Fragen je Video.

Verteilung über die Fünftel (Chronik): `[23, 18, 12, 22, 12]` [gemessen].
Die Fragen sind **gleichmäßig über die Laufzeit gestreut**, nicht am Anfang
gebündelt. Sie sind damit **keine Leitfrage**, sondern **Abschnittsscharniere**:
gefragt wird alle paar Minuten neu, um den nächsten Abschnitt zu öffnen. Dass
64 % ohne Antwortmarker bleiben, heißt nicht, dass sie unbeantwortet bleiben —
es heißt, dass die Antwort **ohne Signalwort** folgt.

## 3.5 Wie enden die Videos?

**Ohne Handlungsaufforderung, mit einem wertenden Schlusssatz — bis die
Chronik-Form ab Upload 11 damit bricht.**

| | alle 16 | POV | Chronik |
|---|---:|---:|---:|
| Videos ohne jede CTA | **11 von 16** | **9 von 9** | 2 von 7 |
| Videos mit CTA im letzten Zehntel | 5 von 16 | **0 von 9** | 5 von 7 |
| Wörter im letzten Zehntel (Median) | 182 | 144 | 214 |
| Fragezeichen im letzten Zehntel | 6 | **0** | 6 |
| zweite Person je 1.000 W im letzten Zehntel | 16,1 | **37,4** | 9,3 |
| Jahreszahl im letzten Zehntel (Median) | 1 | 1 | 1 |

Drei Befunde:

1. **Kein einziges POV-Video endet mit einer Aufforderung.** Kein
   „abonnieren", kein „kommentiert", kein Verweis aufs nächste Video —
   in allen 9 POV-Videos **null** CTA-Treffer über die gesamte Laufzeit
   [gemessen].
2. **Die POV-Form hält die Anrede bis zum letzten Satz** — 37,4 je 1.000
   Wörter im Schlusszehntel, viermal so hoch wie in der Chronik. Der Rahmen
   wird nie verlassen.
3. **Die CTA ist eine Neuerung der letzten Wochen und betrifft nur die
   Chronik-Form.** Die ersten 10 Uploads enthalten keine einzige. Ab
   Video 11 erscheint sie in 5 von 6 Chronik-Videos, ab Video 13 in
   **identischem Wortlaut** (Verweis auf eine Audiofassung, 4 Videos)
   [gemessen]. Video 11 schließt stattdessen mit einer Verabschiedungsformel.
   Die beiden Chronik-Videos ohne CTA sind die Uploads 8 und 12.

Der Schluss selbst ist typischerweise ein **verdichteter Wertungssatz**, oft
als Satzfragment. Was dazu gemessen ist: 24,0 % aller Sätze des Kanals haben
weniger als 5 Wörter, in der POV-Form 29,4 %; das Schlusszehntel enthält im
Median 182 Wörter und in der POV-Form **null** Fragezeichen [gemessen].

## 3.6 Gibt es wiederkehrende Satzbauformen?

**Ja — und zwar je Form eine eigene, sehr enge.** Anteile an allen Sätzen der
Gruppe (POV: 1.975 Sätze, Chronik: 1.429 Sätze; echte Interpunktion):

| Bauform | POV | Chronik |
|---|---:|---:|
| Satz beginnt mit „you" | **22,23 %** | 0,63 % |
| „You're / You are …" | **4,30 %** | 0,35 % |
| „You don't / can't / won't …" | **2,23 %** | 0,07 % |
| Satz beginnt mit „your" | 4,56 % | 0,07 % |
| Satz beginnt mit einer Zahl | **3,59 %** | 1,12 % |
| Satz beginnt mit „but" | 0,96 % | **4,06 %** |
| Satz beginnt mit „and" | 0,56 % | **3,22 %** |
| Fragesatz | 0,25 % | **5,67 %** |
| **Anapher** (Satz beginnt wie der vorige) | **14,7 %** | 4,4 % |

Zwei harte Formeln:

**Die Chronik-Eröffnung.** 6 von 7 Chronik-Videos beginnen mit einer großen
Zahl oder einem Superlativ; **5 von 7** hängen daran eine Umkehrung des Typs
„…aber das Ganze passierte, weil…" mit einer kleinen, beiläufigen Ursache.
Bei 4 Videos folgt zusätzlich eine kurze Bestätigungsfloskel („Ja, wirklich").
Kein einziges POV-Video eröffnet so — dort steht in 0 von 9 Fällen eine große
Zahl oder ein Superlativ im Eröffnungsabschnitt [gemessen].

**Die POV-Eröffnung.** Direkt in der zweiten Person, mit einer konkreten Zahl
(Alter, Uhrzeit, Datum, Entfernung): **9 von 9** POV-Videos enthalten eine
Ziffer in den ersten 35 Wörtern [gemessen]. Vier der neun setzen zusätzlich
eine „Level 1"-Marke als erste Wortgruppe.

Die **Anapher ist das auffälligste Stilmittel überhaupt**: in der POV-Form
beginnt fast jeder siebte Satz mit demselben Wort wie sein Vorgänger. Das ist
der gemessene Kern dessen, was beim Hören als Rhythmus wirkt.

---

# TEIL 4 — Was übertragbar ist

Unser Gegenstand sind Alltagsfragen und Wissenschaft; Krieg ist im README
ausdrücklich ausgeschlossen. Die Trennung folgt der Frage, **woran die Wirkung
hängt** — an der Form oder am Stoff.

## 4.1 Themenunabhängig übertragbar

1. **Die Chronik-Eröffnung.** „Große Folge — aber ausgelöst durch eine
   winzige Ursache." Belegt in 5 von 7 Chronik-Videos. Diese Figur ist
   vollständig stofffrei und passt auf Alltagsfragen und Wissenschaft
   unverändert. Sie deckt sich mit unserem Zielwert „Antwort früh": die
   Chronik setzt den Antwortmarker im Median bei **1,8 %** der Laufzeit.
2. **Die Anapher als Rhythmusmittel.** 14,7 % (POV) bzw. 4,4 % (Chronik)
   gegen **8,3 % in unserem Video-1-Skript** (11 von 133 Sätzen) [gemessen].
   Wir liegen zwischen den beiden Formen; nach oben ist Luft. Wiederholte
   Satzanfänge sind maschinell zählbar und ließen sich als Prüfwert in die
   Pipeline nehmen — analog zu `satzlaengen.py`.
3. **Kurze Sätze und Fragmente.** 24 % aller Sätze des Kanals liegen unter
   5 Wörtern (POV 29,4 %), unser Skript bei 13,5 %; Satzlänge 7,0/9,0 gegen
   unsere 11,0. Ein konkreter, messbarer Korrekturweg — und der einzige
   Punkt, an dem unser Skript in beide Vergleichsrichtungen abweicht.
4. **Fragen als Abschnittsscharniere statt als Leitfrage.** Gleichverteilt
   über die Fünftel `[23, 18, 12, 22, 12]`. Wir haben 6 Fragezeichen in
   1.875 Wörtern — das ist dieselbe Größenordnung wie ein Chronik-Video und
   ohne Themenbezug übertragbar.
5. **Schluss ohne CTA, mit Wertungssatz.** 11 von 16 Videos, 9 von 9 in der
   POV-Form. Kostet nichts und ist stoffunabhängig. Einschränkung: der Kanal
   selbst geht seit Video 11 den umgekehrten Weg und setzt in der Chronik-Form
   wieder eine CTA — ob das seiner Reichweite geschadet hat, ist [unbekannt].
6. **Gleichmäßiges Tempo und gleichmäßige Textverteilung.** 159–184 WPM über
   alle 16 Videos, Fünftel-Anteile zwischen 18,9 % und 20,8 %. Kein
   Spannungsbogen über die Wortdichte — das ist eine Produktionsentscheidung,
   keine Stoffeigenschaft. **Achtung:** 168 WPM widerspricht unserem
   Zielwert 219 WPM aus dem Ink-Vergleich. Beide Werte sind unbelegt als
   Ursache; hier stehen zwei erfolgreiche Kanäle gegeneinander.

## 4.2 Funktioniert nur bei Kriegsthemen (oder Stoffen mit Rolle und Einsatz)

1. **Die POV-Form als Ganzes.** 74,7 Ansprachen je 1.000 Wörter tragen, weil
   es eine **Rolle zum Einnehmen** gibt, deren Einsatz das eigene Leben ist.
   Für „Wer baute die ersten Straßen?" existiert diese Rolle nicht. Wer sie
   erzwingt, bekommt keine Versetzung, sondern eine Behauptung.
2. **Die „Level 1…N"-Leiter.** 38 Marken in 4 Videos. Sie braucht eine
   **echte Hierarchie mit steigendem Einsatz**. Auf Alltagsstoffe übertragbar
   nur als äußere Gliederung („jede Stufe von X") — die Wirkung kommt aber
   aus der Sterblichkeit, nicht aus der Nummerierung.
3. **Zahlen als Dauerbestandteil.** Median 10–13 Zahlen je Fünftel, in der
   POV-Form 3,59 % aller Sätze beginnen mit einer Zahl. Bei Kriegsstoffen sind
   das Verlust-, Sold- und Stückzahlen mit unmittelbarer Bedeutung. Bei
   Alltagsfragen fehlt dieser Zahlenvorrat meist.
4. **Der bleierne Schlusssatz.** Er zieht seine Wirkung aus dem Ausgang der
   Geschichte. Ein Straßenbau-Video hat keinen entsprechenden Ausgang.

**Ein Gegenbeleg in eigener Sache:** Der Kanal hat sich in den letzten drei
Uploads **selbst vom Kriegsthema entfernt** — Odyssee, Trojanischer Krieg,
griechische Soldaten. Das Odyssee-Video ist mit **1,1 Mio. Views das
erfolgreichste des Kanals**. Die Chronik-Form trägt also nachweislich über den
Kriegsstoff hinaus. Wie weit, ist [unbekannt]: Video 15 liegt bei 183k,
Video 16 bei 12k und ist 3 Tage alt.

## 4.3 Was unserem Ton widerspräche

1. **Epistemische Marker bei 0,0.** Das ist der schärfste Gegensatz. In
   5 von 9 POV-Videos kommt **kein einziger** Unsicherheitsmarker vor. Unser
   Video-1-Skript liegt bei 2,1 und die eigene Recherche verlangt
   ausdrücklich, alles als „[umstritten]" Markierte hörbar unsicher zu
   formulieren. **Diese Ersparnis ist nicht übernehmbar** — sie ist der Preis,
   den Unknown Frequencies für seine Geschlossenheit zahlt.
2. **Keine hörbare Quellenarbeit.** Ink und Axen zitieren beide; unser Skript
   trägt 53 Quellen-Tags auf 1.875 Wörter. Unknown Frequencies weist Quellen
   nur in der Kanalbeschreibung aus.
3. **19 benannte Personen je Chronik-Video.** Der Ink-Axen-Vergleich fand in
   **beiden** Kanälen, dass das Video mit Vorwissensanspruch das schwächste
   reife Video war. Eine Namensdichte in dieser Höhe arbeitet gegen die
   Titelregel aus `recherche/themen-erklaerkanal.md`.
4. **Benannte Personen und Krieg** sind im README ausdrücklich ausgeschlossen.
   Das betrifft nicht den Stil, aber jede direkte Nachahmung der Stoffwahl.
5. **Der Kurzwortanteil ist kein Ziel mehr.** Wir liegen bei 90,9 % und damit
   über allen vier Vergleichskanälen (Maximum 82,6 %). Von Unknown Frequencies
   ist in dieser Größe nichts zu holen — eher ist zu prüfen, ob unser Wert zu
   hoch ist.

---

# VORBEHALT

**Ein übernommener Stil garantiert nichts.**

Im Ink-Axen-Vergleich (`regeln/ink-vs-axen.md` §2) waren die beiden Kanäle in
elf gemessenen Größen **nicht unterscheidbar**: Videoanzahl, Kanalalter,
Abonnenten, Videolänge, Kadenz, Thumbnail-Stil, Versalhöhe, Quellenangaben,
Frageform im Titel, Thementaxonomie und Satzlänge. Zwei Größen sprachen sogar
**für** Axen — die Like-Rate (2,92 % gegen 2,00 %) und der stärkste
Einzel-Outlier (7,3× gegen 3,3×).

Axens Median fiel trotzdem von 495.396 auf 17.264 Views, **Faktor 29 abwärts**.
Ink stieg im selben Zeitraum von 167.372 auf 426.305.

Für diesen Bericht heißt das dreierlei:

1. **n = 1 Kanal.** Alles hier Gemessene beschreibt Unknown Frequencies, nicht
   „erfolgreiche Erklärkanäle". Zwei Kanäle können sich in beliebig vielen
   Größen unterscheiden, ohne dass eine davon die Ursache ist — bei einem
   Kanal gibt es nicht einmal einen Vergleichspunkt.
2. **Die Richtung ist nicht bestimmbar.** Unknown Frequencies weicht in vier
   Größen deutlich von Ink ab (Tempo 168 statt 218,5; Ansprache 74,7 statt
   23,4; epistemische Marker 0,0 statt 3,7; keine Frageform im Titel). Beide
   Kanäle sind erfolgreich. Welche dieser Abweichungen hilft, welche schadet
   und welche folgenlos ist, lässt sich **[unbekannt]** nicht entscheiden.
3. **Die entscheidende Größe fehlt weiterhin.** Retention, CTR und
   Traffic-Quellen sind für Fremdkanäle nicht beobachtbar; die
   Methodikprüfung hält fest, dass **69,2 % der Streuung innerhalb der
   Kanäle** liegen — also genau dort, wo von außen nichts messbar ist.
   Auch die 16 Videos hier streuen von 12k bis 1,1 Mio. Views bei nahezu
   identischen Skriptwerten.

Alles in Teil 4 ist **Hypothese zum Prüfen, nicht Regel**.

## Was nicht gemessen wurde

- **Kein Video gesehen, kein Ton gehört.** Stimme, Musik, Schnitt, Bildtext
  und ihr Zusammenspiel mit dem Text sind nicht erfasst. Die Bildwelt steht
  in `recherche/stil-unknown-frequencies.md`; beide Messungen wurden **nicht**
  gegeneinander geprüft.
- **Keine Kommentare erhoben.** Der Ink-Axen-Vergleich fand dort den
  Bot-Befund, der ein Signal vergiftete — hier ist dieser Test offen.
- **Keine Outlier-Scores, keine Monetarisierung, kein RPM.**
- **Die Veröffentlichungsdaten sind monatsgenau.** Eine Bruchstelle im
  Zeitverlauf, wie sie bei Axen zwischen dem 11. und 18. Juni sichtbar war,
  wäre mit dieser Auflösung **nicht** auffindbar.
- **Die Zuordnung POV/Chronik stammt von mir** [abgeleitet], aus Titel und
  gemessenen Werten. Sie ist nicht vom Kanal ausgewiesen.
- **Video 16 ist 3 Tage alt.** Jede Aussage über seine 12k Views und seinen
  auffälligen Ausreißerwert (6,5 epistemische Marker) ist verfrüht.

## Rohdaten

| Datei | Inhalt |
|---|---|
| `recherche/daten/uf_videos.json` | alle 16 Videos: Titel, Länge, Views, Monat, Segmentzahl |
| `recherche/daten/uf_skript_anatomie.json` | Skriptanatomie je Video (Kernfrage, Antwort, Pronomen, Fünftel, Satzlänge, epistemische Marker) |
| `recherche/daten/uf_erzaehlweise.json` | Erzählmerkmale je Video (Chronologie, Personen, Fragen, Schluss) |
| `recherche/daten/uf_schreibstil_messen.py` | Messskript, wiederholbar — gibt ausschließlich Zahlen aus |

Keine dieser Dateien enthält Transkripttext.
