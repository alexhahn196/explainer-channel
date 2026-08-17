# Ink Explainer gegen Axen — ein natürliches Experiment

> Erhebung vom **2026-08-10**, **0 Credits**. Kostenlose Werkzeuge:
> `youtube_video_details` (26×), `youtube_channel_outliers` (2×),
> `get_bulk_video_transcripts` (26 Transkripte), `youtube_video_comments` (3×).
> Keine Videosichtung, kein `watch_youtube_video_and_ask`.
>
> **n = 2 Kanäle. Jeder Befund hier ist eine Hypothese, kein Beweis.**
> Zwei Kanäle können sich in beliebig vielen Größen unterscheiden, ohne dass
> eine davon die Ursache ist. Was hier steht, ist eine Liste von Kandidaten
> für eine Erklärung — geordnet danach, wie gut die Zahlen sie stützen.
>
> Kennzeichnung: **[gemessen]** = direkt aus Tool-Ergebnis oder eigener
> Rechnung · **[abgeleitet]** = eigene Deutung gemessener Werte ·
> **[unbekannt]** = nicht ermittelbar.
>
> Aus den Transkripten wird **kein Text zitiert** — der Bericht enthält
> ausschließlich Zahlen und Kategorien. Das Messskript steht in
> `regeln/daten/skriptanatomie_inkaxen.py`.

## Die Frage hat sich verschoben

Der Auftrag ging von einem stabilen Unterschied aus: Ink 196.000 Median gegen
Axen 25.000, Faktor 8. Die Erhebung aller 26 Videos zeigt, dass es diesen
stabilen Unterschied nicht gibt. **Axen war einmal der erfolgreichere Kanal
und ist dann eingebrochen.**

| Kanal | Videos 1–6 (Median) | Videos 8–13 (Median) | Richtung |
|---|---|---|---|
| Ink Explainer | 167.372 | **426.305** | **× 2,5 aufwärts** |
| Axen | **495.396** | 17.264 | **÷ 29 abwärts** |

[gemessen, exakte Viewzahlen aus `youtube_video_details`]

Axens erste sechs Videos schlagen Inks erste sechs um Faktor 3. Der Faktor 8
zugunsten Inks entsteht erst durch das, was danach passiert ist. Die
eigentliche Frage lautet deshalb nicht „was macht Ink besser", sondern:
**was hat Axen zwischen Mai und Juni verändert?**

---

## 1. Was sich messbar unterscheidet

### 1.1 Der Verlauf — der stärkste Einzelbefund

Alle 26 Videos, chronologisch, nur Viewzahlen [gemessen]:

| # | Ink (Datum → Views) | Axen (Datum → Views) |
|---|---|---|
| 1 | 04-27 → 322.726 | 04-28 → 1.129.121 |
| 2 | 04-28 → 7.268 | 04-28 → 26.792 |
| 3 | 05-07 → 26.088 | 05-04 → **3.173.355** |
| 4 | 05-11 → 137.724 | 05-05 → 261.576 |
| 5 | 05-16 → 783.622 | 05-27 → 9.956 |
| 6 | 05-26 → 197.020 | 05-30 → 729.215 |
| 7 | 06-04 → 248.943 | 06-03 → 24.268 |
| 8 | 06-14 → 902.989 | 06-05 → 12.130 |
| 9 | 06-23 → 671.648 | 06-11 → 113.722 |
| 10 | 07-03 → **1.206.485** | 06-18 → 25.880 |
| 11 | 07-16 → 180.962 | 06-26 → 22.399 |
| 12 | 07-25 → 20.867 | 08-03 → 6.850 |
| 13 | 08-07 → 10.430 | 08-08 → 4.105 |

Axens letztes Video über 100.000 Views stammt vom **11. Juni**. Danach sieben
Videos in Folge unter 26.000. Inks letzte drei Videos sind jung (25, 16 und
3 Tage); bei Videos, die älter als 30 Tage sind, liegt Inks Median bei
**285.834**, Axens bei **26.792** [gemessen].

### 1.2 Perspektivpronomen — was Axen weggelassen hat

Je 1.000 Wörter, Median über je sechs Videos [gemessen]:

| | Ink früh | Ink spät | Axen früh | Axen spät | Axen Änderung |
|---|---|---|---|---|---|
| zweite Person (you) | 27,3 | 23,4 | 22,8 | **14,8** | **−35 %** |
| erste Person Plural (we) | 4,2 | 7,2 | 12,6 | **6,0** | **−52 %** |
| unbestimmt (one, people) | 14,6 | 14,9 | 15,5 | **10,9** | −30 % |
| dritte Person (they) | 18,3 | 17,8 | 19,0 | **14,7** | −23 % |

**Bei Axen fallen alle vier Perspektivmarker gleichzeitig.** Bei Ink bleiben
sie stabil oder steigen. Das ist der einzige Skriptwert, der sich in beiden
Kanälen gegenläufig entwickelt.

### 1.3 Der Einstieg — wo der Abstand am größten ist

Zweite Person je 1.000 Wörter, aufgeschlüsselt nach Fünfteln der Laufzeit
[gemessen]:

| | 1. Fünftel | 2. | 3. | 4. | 5. |
|---|---|---|---|---|---|
| Ink früh | **52,0** | 1,8 | 15,5 | 20,7 | 44,6 |
| Ink spät | **42,5** | 14,0 | 17,5 | 18,2 | 22,1 |
| Axen früh | **37,3** | 10,8 | 22,7 | 13,4 | 19,9 |
| Axen spät | **17,4** | 20,0 | 8,6 | 6,2 | 9,8 |

Axens Einstieg verliert mehr als die Hälfte seiner Zuschaueransprache
(37,3 → 17,4). Ink hält den Einstieg auf dem 2,4-fachen von Axens spätem Wert.
In den Fünfteln 3 bis 5 liegt Axen spät bei einem Drittel bis der Hälfte von
Ink [gemessen].

### 1.4 Weitere Skriptwerte

Mediane [gemessen]:

| Wert | Ink früh | Ink spät | Axen früh | Axen spät |
|---|---|---|---|---|
| Wörter je Video | 1.358 | 2.339 | 1.273 | 1.643 |
| Dauer (s) | 443 | 626 | 397 | 577 |
| Sprechtempo (WPM) | 190,5 | **218,5** | 188,0 | 186,5 |
| Satzlänge (Wörter, Satzproxy) | 7,0 | 7,0 | 6,0 | 6,0 |
| Wörter unter 7 Zeichen | 80,1 % | **82,2 %** | 77,0 % | 76,4 % |
| Kernfrage fällt bei … % der Laufzeit | 10,4 | 33,1 | 25,1 | 19,3 |
| Antwortmarker bei … % | 21,5 | **5,4** | 7,0 | 9,6 |

Beide Kanäle haben ihre Videos verlängert (Ink +72 % Wörter, Axen +29 %). Ink
hat dabei das **Tempo erhöht** (190 → 219 WPM) und den **Wortschatz weiter
vereinfacht** (80,1 → 82,2 % kurze Wörter); Axen beides nicht.

Inks späte Videos setzen den Antwortmarker im Median bei 5,4 % der Laufzeit —
die Frage wird also fast sofort beantwortet und der Rest entfaltet sie. Bei
sechs von sechs späten Ink-Videos liegt der Antwortmarker im ersten Drittel;
bei Axen spät in fünf von sechs, mit einem Ausreißer im letzten Drittel
[gemessen].

### 1.5 Kanalkategorie und Beschreibung

| | Ink Explainer | Axen |
|---|---|---|
| YouTube-Kategorie aller 13 Videos | **People & Blogs** | **Education** |
| Kanalbeschreibung | 5 Sätze, nennt Quellenpflicht ausdrücklich | 1 Satz („Topics I find Interesting") |
| Beschreibungslänge Treffer (Zeichen) | 4.589 | 2.140 |
| gesponserte Videos (13) | 1 | 3 |

[gemessen]. Axen hat drei Videos mit Sponsorenblock (Planet Wild, Shortform ×2),
alle drei nach dem 11. Juni — also im eingebrochenen Zeitraum. Ink hat eines
(World of Warships, 25. Juli, 20.867 Views).

### 1.6 Kommentare

Nur drei Videos erhoben (siehe Einschränkung unten), je 20 Top-Kommentare
von Hand kategorisiert [gemessen]:

| | Ink Treffer (1,21 Mio.) | Axen Treffer (3,17 Mio.) | Axen spät (25.880) |
|---|---|---|---|
| Kommentare gesamt | 1.100 | **6.600** | 144 |
| Kommentare je 1.000 Views | 0,91 | **2,08** | 5,56 |
| höchste Like-Zahl eines Kommentars | 2.000 | **22.000** | 22 |
| Lob am Inhalt | 6 | 3 | 6 |
| Weiterdenken / Selbstbezug | 3 | **9** | 4 |
| **KI-Kritik am Skript** | **4** (Likes 506/271/112/19) | **0** | **0** |
| Faktenkorrektur | 1 | 0 | 0 |
| Konten mit Kanal-Namensmuster | 0 | 0 | **16 von 20** |

Zwei Dinge fallen auf:

1. **Axens Treffer erzeugt mehr als doppelt so viel Kommentarvolumen je View
   wie Inks Treffer**, und der meistgelikte Kommentar dort hat elfmal so viele
   Likes. Die Kommentare beziehen sich überwiegend auf die eigene
   Lebenssituation der Zuschauer (Arbeit, Erschöpfung, Wochenarbeitszeit).
2. **Bei Inks Treffer sind 4 der 20 Top-Kommentare KI-Kritik am Skript**, mit
   zusammen über 900 Likes. Bei Axen taucht diese Kritik in keinem der beiden
   erhobenen Videos auf.

Beim späten Axen-Video stammen **16 von 20 Top-Kommentaren von Konten, deren
Name dem Explainer-Kanalmuster folgt** — der Kanalbetreiber weist im
angepinnten Kommentar selbst darauf hin, dass Nachahmerkonten mit
automatisierten Kommentaren aufgetreten sind. Die hohe Kommentarquote dieses
Videos (5,56 je 1.000 Views) ist deshalb **kein Zuschauersignal**.

---

## 2. Was sich gleicht

Diese Größen trennen die Kanäle **nicht** — hier lohnt keine weitere Suche:

| Größe | Ink | Axen |
|---|---|---|
| Videoanzahl | 13 | 13 |
| Kanalalter | 4,0 Mon. | 3,4 Mon. |
| Abonnenten | 47.900 | 53.900 |
| Videolänge Median | 8:24 | 8:33 |
| Uploads/Woche | 0,74 | 0,88 |
| Thumbnail-Stil | Strichfiguren, gelb/weiße Versalien | identisch |
| Versalhöhe Median | 16,5 % | 16,2 % |
| Quellenangaben | ja | ja |
| Frageform im Titel | 85 % | 77 % |
| **Like-Rate (Median)** | **2,00 %** | **2,92 %** |
| Outlier ≥ 1,5× | 4 (max 3,3×) | 3 (max **7,3×**) |

Zwei davon sprechen sogar **für** Axen: die höhere Like-Rate über alle 13
Videos und der stärkere Einzel-Outlier (7,3× gegen 3,3×).

### Die Thementaxonomie trennt nicht

Alle 26 Titel klassifiziert nach Gegenstand, Zeitbezug, Wissensvoraussetzung
und Selbsterfahrung [gemessen, Klassifikation von Hand, Schema in
`regeln/daten/inkaxen_taxonomie.json`]:

| Merkmal | Ink | Axen |
|---|---|---|
| Vorwissen nötig | 1 von 13 | 1 von 13 |
| Selbsterfahrung ja / teilweise / nein | 6 / 4 / 3 | 6 / 4 / 3 |
| Urzeit-Bezug | 9 | 7 |
| Alltagshandlung als Gegenstand | 6 | 4 |

**Die Verteilungen sind praktisch identisch.** Die Hypothese des Auftrags —
Ink wähle systematisch andere Themen — wird von den Daten nicht gestützt.

### Aber: innerhalb beider Kanäle trennt die Taxonomie sehr wohl

Nur Videos älter als 30 Tage, Median-Views [gemessen]:

| Merkmal | Ink | Axen |
|---|---|---|
| Zeitbezug Urzeit | 671.648 (n=7) | 495.396 (n=6) |
| Zeitbezug zeitlos | 197.020 (n=1) | 68.060 (n=2) |
| Zeitbezug heute | 72.496 (n=2) | 19.461 (n=2) |
| Zeitbezug benannte Epoche | — | 9.956 (n=1) |
| **kein Vorwissen nötig** | **322.726** (n=9) | **70.257** (n=10) |
| **Vorwissen nötig** | **7.268** (n=1) | **9.956** (n=1) |

**Bei beiden Kanälen ist das Video, das Vorwissen verlangt, das schwächste
reife Video des Kanals** — bei Ink „IKEA Effect" (7.268), bei Axen „Napoleon"
(9.956). Und bei beiden fällt der Median mit der Entfernung von der Urzeit.

Zur ausdrücklichen Frage des Auftrags: **Ink hat kein einziges Video über eine
benannte historische Person.** Axen hat eines — und es ist sein schwächstes
reifes Video [gemessen].

---

## 3. Beste Erklärung für den Unterschied

Geordnet nach Stützung durch die Daten.

### Kandidat 1: Axen hat die Zuschaueransprache aufgegeben [abgeleitet]

Der einzige Skriptwert, der sich bei Axen deutlich und bei Ink gegenläufig
verändert hat, ist die Perspektive. Alle vier Pronomengruppen fallen, die
Ansprache im ersten Fünftel halbiert sich. Die frühen Axen-Videos, die
funktionierten, lagen bei 37,3 Ansprachen je 1.000 Wörter im Einstieg — die
späten bei 17,4.

Dazu passt der Kommentarbefund: Axens großer Treffer erzeugte massenhaft
Kommentare mit **Selbstbezug**. Ein Skript, das den Zuschauer nicht mehr
anspricht, erzeugt diesen Selbstbezug schwerer.

**Dagegen spricht:** Die Reihenfolge ist nicht gesichert. Es ist genauso
möglich, dass Axen nach dem Einbruch die Ansprache reduziert hat, statt
umgekehrt. Und Axens spätes Video mit der höchsten Ansprache im zweiten
Fünftel (20,0) lief trotzdem nicht.

### Kandidat 2: Der Einbruch ist ein Algorithmus-Ereignis, kein Skript-Ereignis [abgeleitet]

Der Bruch liegt scharf zwischen dem 11. und dem 18. Juni: davor 113.722 Views,
danach sieben Videos unter 26.000. Ein so scharfer Schnitt ist mit einer
allmählichen Skriptveränderung schwer zu erklären.

Was zeitlich zusammenfällt [gemessen]: Axens erstes gesponsertes Video
(11. Juni, Planet Wild) ist zugleich das letzte über 100.000 Views. Die beiden
weiteren Sponsorenvideos liegen im eingebrochenen Zeitraum. Ob YouTube
gesponserte Videos anders ausspielt, ist von außen **[unbekannt]**.

Ebenfalls zeitlich passend: das Auftreten der Nachahmerkonten, das der
Kanalbetreiber im Juli selbst dokumentiert. Ob deren automatisierte Kommentare
die Auslieferung beeinflusst haben, ist **[unbekannt]**.

### Kandidat 3: Inks Anstieg ist ein Lerneffekt [abgeleitet]

Ink hat zwischen früh und spät drei Dinge gleichzeitig verändert: Videos
länger (+72 % Wörter), Tempo schneller (190 → 219 WPM), Wortschatz einfacher
(80,1 → 82,2 % kurze Wörter), und den Antwortmarker von 21,5 % auf 5,4 % der
Laufzeit vorgezogen. Alle vier Bewegungen zeigen in dieselbe Richtung: **mehr
Inhalt, schneller geliefert, früher aufgelöst.**

**Dagegen spricht:** Das sind vier gleichzeitige Änderungen bei sechs Videos.
Welche davon wirkt — oder ob überhaupt eine — lässt sich mit n = 6 nicht
trennen.

### Was die Erklärung *nicht* ist

- **Nicht das Thema.** Die Taxonomie-Verteilungen sind praktisch identisch.
- **Nicht das Thumbnail.** Stil, Versalhöhe und Aufbau sind ununterscheidbar.
- **Nicht die Titelform.** 85 % gegen 77 % Frageform.
- **Nicht die Quellenarbeit.** Beide zitieren, Axen sogar formal sauberer
  strukturiert.
- **Nicht das Engagement der Zuschauer.** Axens Like-Rate ist höher.
- **Nicht die Kadenz, nicht die Länge, nicht das Alter, nicht die Abozahl.**

---

## 4. Was davon übertragbar wäre

Für den eigenen Kanal — als Hypothesen zu prüfen, nicht als Regeln:

1. **Zweite Person im ersten Fünftel hoch halten.** Der Wert, der Axens
   Absturz begleitet, ist der Einstieg. Ink liegt dort bei 42–52 Ansprachen je
   1.000 Wörter. Das ist maschinell messbar und ließe sich als Prüfschritt in
   die Pipeline nehmen — analog zu `qa_namen.py`.
2. **Kein Vorwissen im Titel voraussetzen.** Der einzige Befund, der in
   beiden Kanälen gleich zeigt: Das Video, dessen Titel einen Namen oder
   Fachbegriff kennt, ist das schwächste. Das deckt sich mit der
   Titelregel aus `recherche/themen-erklaerkanal.md` (kein Anlassname im Titel).
3. **Urzeit schlägt benannte Epoche.** In beiden Kanälen fällt der Median mit
   der Entfernung von der Urzeit. Für die Anlassplanung heißt das: der Stoff
   hinter dem Anlass sollte möglichst weit zurückreichen.
4. **Die Frage früh beantworten.** Inks starke Phase setzt den Antwortmarker
   bei 5,4 % der Laufzeit. Aufschieben scheint nicht zu tragen.

**Nicht übertragbar, weil nicht belegt:** Tempo (219 WPM), Videolänge und
Wortschatzvereinfachung — alle drei ändern sich bei Ink gleichzeitig, keine
lässt sich isolieren.

---

## 5. Was offen bleibt

- **Die Kausalrichtung.** Ob Axens Skriptänderung den Einbruch verursacht hat
  oder eine Reaktion darauf war, ist mit diesen Daten **[unbekannt]**. Dafür
  bräuchte man die Analytics des Kanals.
- **Was am 11.–18. Juni geschah.** Der Bruch ist scharf; die Erhebung findet
  drei zeitgleiche Kandidaten (erstes Sponsoring, Nachahmerkonten,
  Skriptänderung) und kann keinen davon ausschließen.
- **Retention.** Die entscheidende Größe für die Auslieferung ist die
  Wiedergabedauer. Sie ist von außen **[unbekannt]** — kein kostenloses
  Werkzeug liefert sie.
- **Ob Inks späte Videos halten.** Drei der 13 sind jünger als 30 Tage. Der
  Anstieg 167k → 426k stützt sich auf Videos, die noch wachsen können.
- **Die KI-Kritik.** Bei Inks stärkstem Video kritisieren 4 von 20
  Top-Kommentaren das Skript als KI-generiert — trotzdem ist es das
  erfolgreichste Video des Kanals. Ob solche Kritik der Reichweite schadet,
  lässt sich hier **nicht** beantworten.
- **Teil 4 ist unvollständig.** Beauftragt waren je Kanal drei starke und zwei
  schwache Videos (10 insgesamt). Erhoben wurden **drei** — Inks Treffer,
  Axens Treffer und ein spätes Axen-Video. Die sieben übrigen stehen aus; die
  Kommentarbefunde oben sind entsprechend dünn.

## Rohdaten

| Datei | Inhalt |
|---|---|
| `regeln/daten/inkaxen_videos.json` | alle 26 Videos: Views, Likes, exaktes Datum, Länge, Kategorie |
| `regeln/daten/inkaxen_anatomie.json` | Skriptanatomie je Video (Kernfrage, Antwort, Pronomen, Fünftel, Satzlänge) |
| `regeln/daten/inkaxen_taxonomie.json` | Thementaxonomie aller 26 Titel mit Klassifikationsschema |
| `regeln/daten/inkaxen_kommentare.json` | Kommentarkategorien der drei erhobenen Videos |
| `regeln/daten/inkaxen_outliers.json` | Outlier-Scores beider Kanäle |
| `regeln/daten/skriptanatomie_inkaxen.py` | Messskript, wiederholbar |

Aufruf des Messskripts:

```
python3 skriptanatomie_inkaxen.py <bulk-transcript-datei> [...] > anatomie.json
```

Es liest die JSON-Ausgabe von `get_bulk_video_transcripts` und gibt
ausschließlich Kennzahlen aus — **keinen Transkripttext**.
