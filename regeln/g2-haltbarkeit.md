# G2-Haltbarkeit — die etablierten Kanäle über die Zeit

> Erhebung 2026-08-11. **0 Higgsfield-Credits, keine Videosichtung, keine
> Transkripte.** Nur Metadaten-Endpunkte von NexLev
> (`youtube_channel_videos`, `youtube_video_details`, `youtube_channel_about`,
> `youtube_channel_playlists`).
>
> Kennzeichnung jeder Zahl:
> **[gemessen]** = direkt aus einem Tool-Ergebnis ·
> **[abgeleitet]** = von mir aus gemessenen Werten gerechnet oder rekonstruiert ·
> **[unbekannt]** = nicht ermittelbar.
>
> **n = 6 Kanäle. Jeder Befund dieses Dokuments ist eine Hypothese, kein
> Beweis.** Wo unten „Muster" steht, ist eine Beobachtung an bis zu sechs Fällen
> gemeint, von denen mehrere sich in Alter, Thema und Format unterscheiden.
>
> **Rohdaten:** [`regeln/daten/g2-videos.tsv`](daten/g2-videos.tsv) — alle 376
> Videos mit Datum, Views, Likes, Länge, Kategorie und Titel. Die Spalte
> `datum_guete` trennt `gemessen` (312) von `abgeleitet` (64). Jede Zahl dieses
> Berichts ist daraus nachrechenbar; die Datei ist zugleich die Basislinie für
> die Wiederholungsmessung.

## Warum diese Messung

Der Ink-Axen-Vergleich hat gezeigt, dass ein Momentaufnahme-Median nichts über
eine Formel aussagt: Axen sah im Juni wie der Gewinner aus und stürzte danach
ab. G2 ist die einzige Gruppe, bei der sich Haltbarkeit über mehrere Jahre
messen lässt. Gefragt war: Hält das Niveau? Steigt es mit dem Alter? Gibt es
Durchbruch-Videos? Und was haben die Überlebenden, das die Jungen nicht haben?

**Die kurze Antwort:** Von sechs Kanälen hält genau einer sein Niveau über
drei Jahre — Historically. Zwei sind vom eigenen Gipfel um Faktor 8 bis 12
gefallen, ohne dass sich in den Metadaten etwas geändert hätte. Zwei sind zu
jung für die Frage. Einer ist ein Ausreißer mit 24 Videos. Der Kanal, der
hält, ist zugleich der mit der mit Abstand niedrigsten Kadenz.

---

## Vorbemerkung 1: `regeln/messungen.md` existiert nicht

Der Auftrag verweist auf `regeln/messungen.md`. Diese Datei gibt es in diesem
Repository nicht — es gibt kein Verzeichnis `regeln/`, weder auf `main` noch
auf dem Arbeitsbranch. Die Kanal-IDs stammen deshalb aus dem Auftragstext; sie
decken sich mit der Belegkanal-Tabelle in
[`recherche/nischen-kanal-2.md`](../recherche/nischen-kanal-2.md). Diese Datei
ist die erste unter `regeln/`.

**Eine ID fehlte und wurde aufgelöst:** Professor Historian =
`UC35fL9KdO0OSC9CoQk5MLfg` [gemessen, über das in `nischen-kanal-2.md`
belegte Video `kC4hErBshbc`]. Der naheliegende Handle `@ProfessorHistorian`
führt zu einem *anderen, leeren* Kanal (`UCwlOn_2e84FHeQXo-weYSdg`,
1 Abonnent, 0 Videos) — nicht verwechseln.

## Vorbemerkung 2: Die Kanäle sind jünger, als ihr Alter sagt

Das im Auftrag genannte Alter ist das **Beitrittsdatum des Accounts**. Die
sichtbare Publikationsgeschichte ist bei drei von sechs Kanälen erheblich
kürzer [alles gemessen]:

| Kanal | Account seit | erstes sichtbares Video | Lücke | **Publikationsdauer** |
|---|---|---|---|---|
| History Mapped Out | 2023-02-27 | 2023-04-05 | 37 d | **40,2 Mon.** |
| Historically | 2023-03-08 | 2023-04-15 | 38 d | **39,8 Mon.** |
| quack doc | 2023-01-22 | **2024-03-09** | **412 d** | **29,0 Mon.** |
| Folks of Yore | 2024-09-22 | 2025-03-26 | 185 d | 16,5 Mon. |
| First Humans | 2025-05-24 | 2025-08-16 | 84 d | 11,8 Mon. |
| Professor Historian | **2007-04-04** | **2026-04-27** | 6.963 d | **3,4 Mon.** |

**Nur zwei der sechs Kanäle haben mehr als drei Jahre Publikationsgeschichte.**
quack doc, im Auftrag mit „3,5 J" geführt, veröffentlicht seit 29 Monaten.
Professor Historian, „2007 gegründet, später reaktiviert", hat 24 Videos aus
3,4 Monaten — der 19 Jahre alte Account trägt keine sichtbare Historie.

Ob die Lücken auf gelöschte Videos, private Videos oder eine echte Pause
zurückgehen, ist **[unbekannt]** — die API zeigt nur, was öffentlich steht.

---

# TEIL 1 · DIE KURVE

## Methodik

Je Kanal wurden **alle** Videos der Videos-Registerkarte paginiert
(376 Videos [gemessen]), dann je Video der exakte Veröffentlichungszeitpunkt
einzeln abgerufen. Long-Form = **Länge ≥ 180 s** (YouTube-Shorts-Grenze);
in dieser Gruppe fiel dabei kein einziges Video heraus — die sechs Kanäle
laden Shorts, wenn überhaupt, in die separate Shorts-Registerkarte.

**Warum der Einzelabruf nötig war:** Der Listen-Endpunkt liefert nur
Relativangaben („3 years ago") und rechnet daraus ein Datum *heute minus
3 Jahre*. Das erste Historically-Video liegt danach am 2023-08-11 — real ist
es der **2023-04-15**. Für Quartalsmediane ist die Listenangabe bei allem, was
älter als ein Jahr ist, unbrauchbar. Auch der NexLev-Index (`search_videos`)
scheidet aus: er trägt für vier verschiedene Historically-Videos denselben
`publishedAt` und veraltete View-Zahlen.

Alle Zeitstempel sind auf **UTC** normalisiert; die API liefert Ortszeit mit
Zeitzonen-Offset. Bei Videos nahe Mitternacht kann das Datum daher um einen Tag
von der YouTube-Anzeige abweichen.

**Abdeckung [gemessen]:** 312 von 376 Videos mit exaktem Zeitstempel. Die
fehlenden 64 sind ausschließlich History-Mapped-Out-Videos ab Position 71
(Kontingent `youtube_video_details` erschöpft: 300 Aufrufe/24 h, PRO-Tarif).
Ihre Daten sind **[abgeleitet]** — verankert am exakt gemessenen Datum von
Video #70 (2025-03-01), an der gemessenen Upload-Reihenfolge und an den
Monatslabels; die 18 Videos mit dem mehrdeutigen Label „1 year ago" wurden im
Fenster 2025-03-01 … 2025-09-11 gleichmäßig verteilt. Alle
History-Mapped-Out-Quartale ab **2025Q2 sind damit teilweise abgeleitet** und
unten mit `*` markiert.

---

## Historically — **Plateau, sehr hoch, leicht fallend**

`UCoZd78hRUdxxsuGiABuHF_A` · 1,33 Mio. Abos · 21 Long-Form-Videos ·
0,13 Uploads/Woche · Gesamtviews des Katalogs 49,5 Mio. [alles gemessen]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2023Q2 | 2 | 1.239.284 | 6,6 min |
| 2023Q3 | 2 | 1.481.672 | 10,6 min |
| 2023Q4 | 1 | 3.042.127 | 11,4 min |
| 2024Q1 | 1 | 4.004.549 | 28,5 min |
| 2024Q2 | 2 | 2.883.992 | 18,3 min |
| 2024Q3 | 1 | 1.160.624 | 18,3 min |
| 2024Q4 | 0 | — | — |
| 2025Q1 | 1 | 5.164.958 | 74,6 min |
| 2025Q2 | 3 | 1.820.808 | 15,3 min |
| 2025Q3 | 1 | 2.993.913 | 21,1 min |
| 2025Q4 | 2 | 1.642.146 | 18,7 min |
| 2026Q1 | 2 | 1.985.623 | 23,7 min |
| 2026Q2 | 3 | 1.224.658 | 31,2 min |

Jahresscheiben ab erstem Video: **1,81 Mio. → 2,88 Mio. → 1,95 Mio. →
1,22 Mio.** [gemessen]

```
Median je Quartal, log-Skala
 5M |                            ●
 4M |             ●
 3M |       ●              ●              ●
 2M |  ●  ●          ●        ●     ● ●●        ●
 1M |                    ●                 ●   ●   ●
    +--------------------------------------------------
     23Q2      24Q1      24Q4      25Q3      26Q2
```

**Form: Plateau.** Der Kanal startet mit dem ersten Video bei 638k und dem
zweiten bei 1,84 Mio. und liegt drei Jahre später immer noch zwischen 1,1 und
2,1 Mio. Es gibt kein Anlaufen, keinen Durchbruch, keinen Einbruch. Der stärkste
Sprung im 5er-Median ist **2,07×** (2024-02-29) — das ist bei 21 Videos
Rauschen, kein Bruch. Der stärkste Abwärtssprung ist 0,52×.

Die Abwärtsneigung im vierten Jahr (1,22 Mio. gegen 2,88 Mio. im zweiten) ist
sichtbar, aber innerhalb der Streuung: das größte Video des Kanals
(*The ENTIRE History of ROME*, 6,22 Mio.) liegt im April 2026, also **im
Abwärts-Jahr**.

**Kein Kanal der Gruppe ist so wenig von Ausreißern abhängig:** die drei
größten Videos tragen 31 % der Gesamtviews [abgeleitet aus gemessenen Werten].

---

## quack doc — **Sprung, Gipfel, fünf Quartale Abstieg, mögliche Erholung**

`UC2NRf0-PH8IiMq5uA5FHJnA` · 148.000 Abos · 126 Long-Form-Videos ·
1,00 Uploads/Woche über die Gesamtlaufzeit [alles gemessen]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2024Q1 | 2 | 13.868 | 8,2 min |
| 2024Q2 | 14 | 9.106 | 10,2 min |
| 2024Q3 | 6 | 16.778 | 9,7 min |
| **2024Q4** | 3 | **189.050** | **48,3 min** |
| 2025Q1 | 6 | 278.556 | 56,3 min |
| **2025Q2** | 16 | **325.030** | 68,2 min |
| 2025Q3 | 18 | 122.231 | 58,2 min |
| 2025Q4 | 21 | 57.180 | 46,9 min |
| 2026Q1 | 17 | 36.135 | 50,5 min |
| 2026Q2 | 17 | 26.373 | 49,0 min |
| 2026Q3 | 6 | 98.357 | 27,7 min |

```
Median je Quartal, log-Skala
300k|                 ●  ●
200k|            ●
100k|                       ●                    ●
 50k|                             ●
 30k|                                  ●   ●
 10k|  ● ●  ●
    +--------------------------------------------------
     24Q1  24Q3  25Q1  25Q3  26Q1  26Q3
```

**Form: Stufe hoch, dann langer Abstieg.** Der Median steigt vom Gipfel
(325.030 in 2025Q2) auf 26.373 in 2026Q2 — **Faktor 12,3 in fünf Quartalen**
[gemessen]. Das ist ein Absturz in derselben Größenordnung wie bei Axen, nur
über fünf Quartale statt über Wochen.

**Der letzte Punkt (2026Q3, 98.357) ist die einzige Erholungsspur der ganzen
Gruppe** — aber n = 6 Videos und das Quartal ist noch nicht zu Ende. Was sich
dort geändert hat, steht in Teil 2; es ist genau nicht mehr Serie, sondern
weniger.

---

## History Mapped Out — **Anstieg, Gipfel-Plateau, sechs Quartale Abstieg**

`UCtzvIHQyRDL2mtetu6ZWsvw` · 176.000 Abos · 134 Long-Form-Videos ·
0,77 Uploads/Woche [alles gemessen; Quartale ab 2025Q2 mit `*` sind teilweise
abgeleitet]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2023Q2 | 10 | 11.149 | 12,8 min |
| 2023Q3 | 9 | 33.772 | 13,8 min |
| 2023Q4 | 9 | 14.267 | 14,5 min |
| 2024Q1 | 9 | 58.033 | 15,4 min |
| 2024Q2 | 8 | 194.066 | 20,9 min |
| 2024Q3 | 9 | 245.943 | 21,9 min |
| **2024Q4** | 11 | **265.423** | 21,8 min |
| **2025Q1** | 8 | **269.075** | 26,4 min |
| 2025Q2 `*` | 8 | 192.000 | 27,8 min |
| 2025Q3 `*` | 11 | 174.000 | 22,3 min |
| 2025Q4 `*` | 12 | 79.000 | 24,9 min |
| 2026Q1 `*` | 12 | 52.000 | 26,5 min |
| 2026Q2 `*` | 11 | 62.000 | 25,6 min |
| 2026Q3 `*` | 7 | 33.000 | 28,1 min |

Jahresscheiben: **18.033 → 255.683 → 99.000 → 36.500** [teils abgeleitet]

```
Median je Quartal, log-Skala
300k|                    ● ● ●
200k|                 ●        ●
100k|                              ●
 50k|           ●                       ●  ●
 30k|     ●                                     ●
 10k|  ●     ●
    +--------------------------------------------------
     23Q2  23Q4  24Q2  24Q4  25Q2  25Q4  26Q2
```

**Form: umgekehrtes V.** Vier Quartale Anlauf, drei Quartale Gipfel
(2024Q3–2025Q1), dann sechs Quartale Abstieg auf ein Achtel. Die Kadenz bleibt
dabei konstant bei 0,65–0,92/Woche, die Länge steigt weiter von 13 auf 26 min.
**Der Kanal fällt, während er unverändert arbeitet.**

Auch hier ist die Basis breit — die drei größten Videos tragen nur 18 % der
Gesamtviews [abgeleitet]. Der Abstieg ist also kein Ausreißer-Artefakt,
sondern ein echter Niveauwechsel.

---

## First Humans — **steigend, mit hoher Streuung**

`UCAksyQw6LlPRw-rYhEPADMA` · 33.500 Abos · 50 Long-Form-Videos ·
0,99 Uploads/Woche [alles gemessen]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2025Q3 | 7 | 4.369 | 8,2 min |
| 2025Q4 | 8 | 14.090 | 8,2 min |
| 2026Q1 | 12 | 54.374 | 8,6 min |
| 2026Q2 | 14 | 37.901 | 8,8 min |
| 2026Q3 | 9 | 61.947 | 8,7 min |

**Form: steigend.** Faktor 14 über fünf Quartale (4.369 → 61.947), der letzte
Punkt ist der höchste. Der Kanal ist mit 11,8 Monaten Publikationsdauer aber **zu jung
für die Haltbarkeitsfrage** — er ist im selben Lebensalter, in dem quack doc
und History Mapped Out ebenfalls stiegen.

Streuung innerhalb der Quartale ist extrem: 2026Q2 reicht von 2.450 bis
2.344.087 [gemessen]. Die drei größten Videos tragen 52 % der Gesamtviews.

---

## Folks of Yore — **Ausreißer-getrieben, kein Niveau**

`UC10wjSicTht1rum3NF0H9WA` · 21.100 Abos · 21 Long-Form-Videos ·
0,30 Uploads/Woche [alles gemessen]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2025Q1 | 1 | 1.284 | 19,1 min |
| 2025Q2 | 5 | 1.871 | 19,9 min |
| 2025Q3 | 2 | 4.862 | 12,6 min |
| 2025Q4 | 1 | 2.358 | 26,2 min |
| **2026Q1** | 5 | **73.711** | 24,4 min |
| 2026Q2 | 5 | 8.413 | 20,9 min |
| 2026Q3 | 2 | 5.619 | 17,9 min |

**Form: Ausreißer-getrieben.** Ein einziges Quartal ragt heraus; danach fällt
der Median um Faktor 8,8 zurück. Die drei größten Videos tragen **87 %** der
Gesamtviews [abgeleitet] — der Kanal hat 1,18 Mio. Views, davon kommen
657.870 aus einem Video.

Das ist die Axen-Signatur: **ein Treffer, kein Niveau.**

---

## Professor Historian — **ein Treffer, danach Absturz**

`UC35fL9KdO0OSC9CoQk5MLfg` · 28.200 Abos · 24 Long-Form-Videos in 3,4 Monaten ·
1,65 Uploads/Woche [alles gemessen]

| Quartal | n | Median Views | Median Länge |
|---|---:|---:|---:|
| 2026Q2 | 15 | 32.117 | 15,5 min |
| 2026Q3 | 9 | **5.843** | 14,9 min |

Chronologie der ersten Wochen [gemessen]:
`2026-04-27` Start · `2026-05-03` **4.643.004** (*Ancient Technologies We Still
Can't Explain*) · `2026-05-10` 17.559 · `2026-05-26` 32.117 · `2026-06-10`
13.955 · `2026-07-22` 2.603 · `2026-08-08` 3.259

**Form: Ausreißer, dann Abstieg.** Das viertgrößte Video der ganzen Erhebung
liegt auf Position 3 dieses Kanals — sechs Tage nach dem ersten Upload. Der
5er-Median fällt danach von 222.304 auf 32.117 (0,14×) und weiter auf
niedrige vierstellige Werte. Das **Top-Video allein trägt 70 %** der
Gesamtviews des Kanals [abgeleitet].

Das ist derselbe Verlauf wie bei Axen — bei einem Kanal, dessen Account
19 Jahre alt ist. **Accountalter kauft kein Niveau.**

---

## Antworten auf die drei Kernfragen

### 1. Hatte einer einen Einbruch wie Axen — und hat er sich erholt?

**Ja, drei — und keiner hat sich erholt** [gemessen]:

| Kanal | Gipfel | Tiefpunkt | Faktor | Dauer |
|---|---|---|---|---|
| quack doc | 325.030 (2025Q2) | 26.373 (2026Q2) | **12,3×** | 5 Quartale |
| History Mapped Out | 269.075 (2025Q1) | 33.000 (2026Q3) | **8,2×** | 6 Quartale |
| Folks of Yore | 73.711 (2026Q1) | 5.619 (2026Q3) | 13,1× | 2 Quartale |
| Professor Historian | 222.304 (5er-Median) | 3.259 | 68× | 3 Monate |

**Was sich davor und danach änderte: nichts Messbares.** Das ist der
unbequemste Befund dieser Erhebung. An den Abwärtsbrüchen von quack doc
(2026-04-12) und History Mapped Out (2024-12-06) bleiben Länge, Kadenz,
Titelformel und Themengebiet praktisch identisch (Details in Teil 2). Die
Kanäle arbeiteten nach dem Absturz genauso weiter wie davor — und fielen
trotzdem.

**Die einzige Erholungsspur** ist quack doc in 2026Q3 (26.373 → 98.357,
n = 6, Quartal unvollständig). Was sich dort geändert hat: der Iceberg-Anteil
fiel von 97 % auf 57 %, und die **Nicht**-Iceberg-Videos erzielten in diesem
Zeitraum 79.853 Median gegen 28.707 für die Serie [gemessen]. Wenn das eine
Erholung ist, kommt sie vom *Verlassen* der Serie, nicht von ihr.

**Historically hatte nie einen Einbruch.**

### 2. Steigt der Median mit dem Kanalalter, oder lebt der Kanal von einer alten Erfolgsphase?

**Bei den beiden Kanälen mit über drei Jahren Historie: alte Erfolgsphase**
[gemessen].

| Kanal | Gipfel liegt im | Publikationsmonat | heutiges Niveau |
|---|---|---|---|
| History Mapped Out | 2024Q4–2025Q1 | Monat 18–23 | 12 % des Gipfels |
| quack doc | 2025Q2 | Monat 13–15 | 8 % des Gipfels (30 % in Q3) |
| Historically | kein Gipfel | — | 42 % des Zweitjahres-Medians |
| First Humans | 2026Q3 (aktuell) | Monat 12 | steigend |
| Folks of Yore | 2026Q1 | Monat 10 | 8 % des Gipfels |
| Professor Historian | Monat 1 | Monat 1 | 2,6 % |

**Muster [abgeleitet, n = 5 mit auswertbarer Historie]:** Der Gipfel liegt bei
allen Kanälen außer Historically im **ersten oder zweiten Lebensjahr**, nie im
laufenden. Kein Kanal dieser Gruppe wächst mit dem Alter. Der Median steigt
nicht mit dem Kanalalter — er steigt in den ersten 12–24 Monaten und fällt
danach.

**Die eine Ausnahme ist zugleich die eine Ausnahme bei der Kadenz.**
Historically fährt **0,13 Uploads/Woche** — ein Video alle acht Wochen. Alle
Kanäle mit Abstieg fahren 0,3 bis 1,65/Woche. Das ist ein Zusammenhang über
sechs Fälle, keine Kausalität; die naheliegende Gegenerklärung (Historically
hat 1,33 Mio. Abonnenten und damit eine Basis, die die anderen nicht haben)
ist mit diesen Daten **nicht ausschließbar**.

### 3. Gibt es ein Durchbruch-Video?

**Ja, bei drei von sechs — und in allen drei Fällen ändert sich mit dem Video
das Format, nicht das Thema** [gemessen]:

| Kanal | Datum | Video | Views | 5er-Median davor → danach |
|---|---|---|---|---|
| **quack doc** | **2024-08-16** | *The Most Bizarre Cults Iceberg Explained* | **552.637** | 9.191 → 419.686 (**45,7×**) |
| **History Mapped Out** | **2024-01-15** | *The Dutch Colonial Empire: Small Metropole, Big Ambitions* | **273.097** | 7.854 → 273.097 (**34,8×**) |
| **First Humans** | **2026-01-19** | *Ancient DNA Reveals Tutankhamun's Shocking Family Secret* | **388.180** | 7.659 → 194.796 (**25,4×**) |

Nicht als Durchbruch zu werten:

- **Folks of Yore**, 2026-01-23, *Your „Busy" Life Would Disgust an Ancient
  Roman*, **657.870 Views**, 5er-Median 2.358 → 73.711 (31,3×). Der Sprung
  ist da, das **Niveau hält nicht**: schon im Folgequartal steht der Median
  wieder bei 8.413. Ein Treffer, kein Durchbruch.
- **Professor Historian**, 2026-05-03, *Ancient Technologies We Still Can't
  Explain*, **4.643.004 Views**. Das Niveau des Kanals sinkt nach diesem
  Video, statt zu steigen.
- **Historically**: kein Durchbruch-Video. Der Kanal startet auf dem Niveau,
  auf dem er bleibt.

**Bei History Mapped Out ist der Durchbruch zweistufig** [gemessen]: das
Dutch-Colonial-Empire-Video reißt das Niveau hoch, die beiden Folgevideos
fallen auf 25.725 und 8.407 zurück, und erst *The Migration Period: How Europe
Was Born* (2024-02-21, **1.554.956**) verankert es. Aus einem einzelnen Sprung
lässt sich zum Zeitpunkt des Sprungs nicht ablesen, ob er trägt.

---

# TEIL 2 · WAS SICH AN DEN BRÜCHEN GEÄNDERT HAT

Je Bruch: die 5 Videos davor gegen die 5 danach. Nur Metadaten — Titel,
Länge, Thema, Abstände. Keine Transkripte, keine Sichtung.

## quack doc, 2024-08-16 — **hoch, 45,7×**: Formatwechsel

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 9.191 | **419.686** |
| Median Länge | **9,3 min** | **53,6 min** |
| Median Abstand | **8 Tage** | **24 Tage** |
| Titelmuster | frei | **„The Most *X* Iceberg Explained"** |
| Thema | Tribal Cults · Animals · Superpowers · Sterben je Epoche · Krieg je Epoche | Cults · Human Experiments · Diddy · Serial Killers · Torture |

**Drei Dinge ändern sich gleichzeitig: die Länge versechsfacht sich, der Titel
wird zur festen Wortformel — und die Kadenz sinkt auf ein Drittel.** Das Thema
bleibt, wo es war (dunkle Kuriositäten). Der Kanal hörte auf, dreimal die
Woche kurze Clips zu bauen, und fing an, alle drei Wochen eine Stunde zu
liefern.

Der Iceberg-Anteil je Halbjahr danach [gemessen]:

| Halbjahr | n | Iceberg | Median Iceberg | Median Rest |
|---|---:|---:|---:|---:|
| H1 2024-03 | 21 | 1 (5 %) | 552.637 | 9.132 |
| H2 2024-09 | 7 | 6 (86 %) | 304.368 | 8.948 |
| H3 2025-03 | 31 | 29 (94 %) | 251.684 | 63.861 |
| H4 2025-09 | 39 | 38 (97 %) | 61.987 | 13.788 |
| H5 2026-03 | 28 | 16 (57 %) | 28.707 | **79.853** |

Über den ganzen Katalog: 88 von 126 Videos tragen „Iceberg" im Titel,
Median **93.842** gegen **12.834** für den Rest — **7,3×** [gemessen]. Im
letzten Halbjahr kehrt sich das Verhältnis um.

## quack doc, 2026-04-12 — **runter, 0,17×**: nichts ändert sich

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 130.638 | **21.607** |
| Median Länge | 49,6 min | **50,0 min** |
| Median Abstand | 4 Tage | **4 Tage** |
| Titelmuster | Iceberg | **Iceberg** |
| Thema | Holocaust · Ancient Mysteries · Deadly Disease · Christianity · Ancient Civilizations | Cults · US War Crimes · CIA · Black Death · Reddit Confessions |

**Länge, Kadenz, Titelformel und Themenbreite sind vor und nach dem Absturz
identisch.** Aus den Metadaten ist nicht erkennbar, was passiert ist.

## History Mapped Out, 2024-01-15 — **hoch, 34,8×**: Themenverengung

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 7.854 | **273.097** |
| Median Länge | 14,8 min | 13,4 min |
| Median Abstand | 8 Tage | 12 Tage |
| Thema | Normandie · Piraterie (2 Teile) · Opiumkriege · Indien-Pakistan — **Weltgeschichte quer** | Niederländisches Kolonialreich · Alexander · Drittes Reich/Polen · Völkerwanderung · Zwischenkriegszeit — **Europa: Reiche, Völker, Dynastien** |

**Die Länge bleibt, die Kadenz sinkt leicht, das Themengebiet verengt sich.**
Der Kanal hört auf, jedes historische Thema zu bedienen, und wird zum
Europa-Kanal. Die Doppelpunkt-Formel („*Thema*: *Versprechen*") tragen später
**109 von 134 Videos (81 %)** [gemessen].

## History Mapped Out, 2024-12-06 — **runter, 0,21×**: nichts ändert sich

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 589.296 | **122.239** |
| Median Länge | 22,8 min | 25,9 min |
| Median Abstand | 7 Tage | 10 Tage |
| Thema | Papsttum · Erster Kreuzzug · Reconquista · Rosenkriege · Kelten | Dreißigjähriger Krieg · Anglo-Spanischer Krieg · Österreichischer Erbfolgekrieg · Italienkriege · Englischer Bürgerkrieg |

**Dasselbe Bild wie bei quack doc: die Arbeit bleibt gleich, die Wirkung geht.**
Wenn überhaupt etwas erkennbar ist, dann eine noch engere Verengung — von
gemischt europäischer Geschichte auf reine Kriegschronologie. Der Kanal
schrumpft sein Feld weiter, nachdem die Verengung ihn zuvor nach oben
getragen hatte.

## First Humans, 2026-01-19 — **hoch, 25,4×**: vom Thema zum Rätsel

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 7.659 | **194.796** |
| Median Länge | **8,2 min** | **8,2 min** |
| Median Abstand | 12 Tage | **8 Tage** |
| Titel | „Ancient DNA Reveals the Real Origins of *Volk*" | benanntes Rätsel: **Tutanchamun · Frozen Children · Dyatlov Pass · Göbekli Tepe · Skeleton E26** |

**Länge und Formel bleiben, die Kadenz steigt — und der Gegenstand wechselt
von einer Kategorie („Herkunft der Pikten") zu einem benannten Rätsel, das
Leute schon kennen.** Das ist genau der Anlassbindungs-Mechanismus aus
`README.md`: ein bekannter Aufhänger bringt die Suchanfragen, das Video
liefert den Stoff dahinter.

Bemerkenswert dagegen: die „Ancient DNA / Science reveals"-Formel trägt
31 von 50 Titeln, erzielt aber **0,6×** des Medians der übrigen Videos
[gemessen]. Die Serie ist bei diesem Kanal ein Nachteil, der Rätselaufhänger
der Vorteil.

## Folks of Yore, 2026-01-23 — **hoch, 31,3×**: Adressatenwechsel

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 2.358 | **73.711** |
| Median Länge | 15,1 min | **24,4 min** |
| Median Abstand | **30 Tage** | **15 Tage** |
| Titel | *„What It Was Actually Like to Live in a Medieval Castle"* — Beschreibung der Vergangenheit | *„**Your** ‚Busy' Life Would Disgust an Ancient Roman"* · *„**Why You** Wake Up at 3 AM Every Night"* — **zweite Person, Gegenwart** |
| Thema | Mittelalter | Antike als Spiegel der Gegenwart |

**Der Titel wechselt vom Bericht über die Vergangenheit zum Urteil über den
Zuschauer.** Dazu Länge +62 %, Kadenz verdoppelt. Der Kanal beschreibt in
seiner eigenen Kanalbeschreibung genau das: „Analyzing modern life through
the lens of history" — der Bruch ist der Moment, in dem die Titel das auch
tun.

Das Niveau hielt trotzdem nicht (siehe oben).

## Professor Historian, 2026-05-26 — **runter, 0,14×**: nichts ändert sich

| | davor (5) | danach (5) |
|---|---|---|
| Median Views | 222.304 | **32.117** |
| Median Länge | 15,1 min | 16,7 min |
| Median Abstand | 4 Tage | 3 Tage |
| Titel | Superlativformel („The Most TERRIFYING…") | Superlativformel („The Most EVIL…") |

Der Kanal produziert unverändert weiter und beschleunigt sogar. Das
4,6-Mio.-Video war ein Einzelereignis, kein Niveau.

## Der gemeinsame Nenner von Teil 2

**Aufwärtsbrüche haben sichtbare Ursachen in den Metadaten. Abwärtsbrüche
haben keine.** Bei allen drei echten Durchbrüchen ändern sich Länge, Kadenz
oder Titelbauform messbar. Bei allen drei Abstürzen ändert sich nichts.

Das heißt für die Praxis: **Ein Aufstieg ist rekonstruierbar und damit
planbar. Ein Absturz ist es nicht** — jedenfalls nicht aus dem, was von außen
sichtbar ist.

---

# TEIL 3 · DIE ÜBERLEBENSFRAGE

## Themenbreite — bleiben sie bei einem Thema?

Titelklassifikation über Schlagwortcluster, Mehrfachzuordnung möglich
[gemessen; die Heuristik trifft nicht jeden Titel — die Spalte „klassifiziert"
zeigt, wie viel erfasst ist]:

| Kanal | klassifiziert | stärkster Cluster | Anteil | zweitstärkster |
|---|---|---|---|---|
| **Historically** | 13/21 | Krieg/Militär | **29 %** | Antike 10 % |
| quack doc | 49/126 | Krankheit/Tod | 12 % | Religion/Okkult 11 % |
| **History Mapped Out** | 93/134 | Krieg/Militär | **44 %** | Mittelalter 14 % |
| First Humans | 41/50 | Wissenschaft/DNA | **76 %** | Antike 40 % |
| Folks of Yore | 17/21 | Mittelalter / Alltag | 38 % / 38 % | Antike 29 % |
| Professor Historian | 19/24 | Antike | 46 % | Herrscher 29 % |

**Befund [abgeleitet]:** Es gibt kein gemeinsames Muster. Der einzige Kanal
mit stabilem Niveau (Historically) ist auch der **breiteste** — kein Cluster
über 29 %, und die 21 Titel reichen von Wu Zetian über Heisenberg und die
Weltwunder bis zur Geschichte Roms. Der Kanal mit der stärksten Verengung
(History Mapped Out, 44 % Krieg) ist derjenige, der am längsten fällt — und
seine Verengung war ursprünglich der Grund für seinen Aufstieg.

**Themenverengung wirkt in dieser Gruppe wie ein Aufstiegs-, nicht wie ein
Haltbarkeitsmittel.** Das ist eine Hypothese aus n = 2 Aufstiegen und n = 1
Abstieg.

## Serienbildung — gibt es wiederkehrende Formate?

Playlists je Kanal [gemessen]:

| Kanal | Playlists | größte Serie |
|---|---:|---|
| History Mapped Out | **17** | „Greatest Empires That Shaped the World" (17) · „Medieval Kingdoms of Europe" (16) · „History on Map" (16) |
| Folks of Yore | 4 | „Our World vs Theirs" (13) |
| Historically | 3 | „Facts" (19), „Historically Shorts!" (31), „Specials" (2) |
| quack doc | 3 | „The Craziest Icebergs" (2), „Iceberg Videos" (3), „Disturbing Iceberg Videos" (1) |
| Professor Historian | 1 | „History Explained" (25) |
| First Humans | 1 | „Ancient DNA" (28) |

**Alle sechs haben mindestens eine Serie. Der Effekt ist nicht einheitlich**
[gemessen, Median der Serienvideos gegen den Rest desselben Kanals]:

| Kanal | Serie über den Titel | Anteil | Faktor gegen Rest |
|---|---|---:|---:|
| quack doc | „Iceberg" | 70 % | **7,3×** |
| Professor Historian | „1 Hour of …" | 12 % | 5,4× (n = 3) |
| quack doc | „What it was like…" | 3 % | 2,2× |
| History Mapped Out | „History of …" | 25 % | 1,4× |
| History Mapped Out | Doppelpunkt-Formel | 81 % | **0,9×** |
| **First Humans** | „Ancient DNA/Science reveals" | 62 % | **0,6×** |
| Folks of Yore | „History of …" | 14 % | 0,5× (n = 3) |
| **Historically** | *kein Muster ≥ 3 Videos* | — | — |

**Der klarste Befund des ganzen Berichts zur Serienfrage:** Die
quack-doc-Iceberg-Serie ist der einzige messbare Serienvorteil in der Gruppe
— und derselbe Kanal ist um Faktor 12 gefallen, *während* der Serienanteil
von 94 % auf 97 % stieg. Bei First Humans ist die eigene Serienformel
schlechter als der Rest des Katalogs. Und der einzige haltbare Kanal,
Historically, hat **überhaupt keine wiederkehrende Titelformel** — kein
Muster trifft bei ihm auch nur drei der 21 Titel.

Zur Frage aus dem Auftrag, ob es mehr Iceberg-artige Serien gibt: **nein.**
Die Iceberg-Serie ist ein Einzelfall in dieser Gruppe. Was die anderen haben,
sind thematische Playlists (History Mapped Out) oder eine
Sammel-Playlist über den ganzen Katalog (Professor Historian, First Humans) —
keine Reihe mit eigener Zugkraft.

## Längenentwicklung — werden die Videos länger?

Median-Länge im ersten gegen das letzte Halbjahr [gemessen; History Mapped Out
letztes Halbjahr teils abgeleitet]:

| Kanal | erstes HJ | letztes HJ | Entwicklung |
|---|---:|---:|---|
| Historically | 8,9 min | **31,2 min** | **+250 %** |
| quack doc | 9,3 min | **48,9 min** | **+426 %** (Gipfel 62,3) |
| History Mapped Out | 13,0 min | **25,7 min** | **+98 %** |
| Folks of Yore | 17,2 min | 21,7 min | +26 % |
| First Humans | 8,2 min | 8,7 min | +6 % |
| Professor Historian | 15,2 min | — | zu kurz |

**Das ist der konsistenteste Befund der Erhebung: fünf von fünf auswertbaren
Kanälen werden länger, vier davon deutlich.** Und zugleich der klarste Beleg
dafür, dass Länge nicht Erfolg ist: quack doc und History Mapped Out
verlängerten *während* ihres Abstiegs weiter.

**Direkte Folgerung für die eigene Konfiguration:** Der Zielkorridor aus
`README.md` ist **8–15 Minuten**. Von den sechs Kanälen liegt heute genau
einer darin — **First Humans mit 8,7 min**, der jüngste mit steigender Kurve.
Professor Historian (15,2 min) liegt am Rand und stürzt ab. Die vier anderen
liegen bei 21 bis 49 Minuten. **Kein etablierter Kanal dieser Gruppe
veröffentlicht heute im 8–15-Minuten-Band.**

## Kadenzentwicklung — steigt oder fällt sie?

Uploads/Woche je Halbjahr [gemessen]:

| Kanal | H1 | H2 | H3 | H4 | H5 | H6 | H7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Historically | 0,15 | 0,08 | 0,12 | 0,04 | 0,15 | 0,15 | 0,12 |
| quack doc | 0,81 | 0,27 | 1,19 | 1,50 | 1,08 | | |
| History Mapped Out | 0,73 | 0,69 | 0,65 | 0,73 | 0,73 | 0,92 | 0,69 |
| First Humans | 0,73 | 1,19 | | | | | |
| Folks of Yore | 0,31 | 0,19 | 0,31 | | | | |
| Professor Historian | 0,92 `†` | | | | | | |

`†` Die Halbjahreswerte teilen durch volle 26 Wochen und **untertreiben ein
noch laufendes Halbjahr**. Professor Historian existiert erst 14,6 Wochen; über
die tatsächliche Laufzeit sind es **1,65 Uploads/Woche** [gemessen]. Dasselbe
gilt abgeschwächt für die jeweils letzte Spalte jeder Zeile.

**Kein gemeinsames Muster.** Historically hält 0,12–0,15 über sieben Halbjahre
konstant. History Mapped Out hält 0,65–0,92 konstant. quack doc schwankt stark
(der Einbruch auf 0,27 in H2 fällt mit dem Formatwechsel auf Stundenlänge
zusammen). First Humans beschleunigt.

**Was auffällt, ist nicht die Entwicklung, sondern das Niveau:** Historically
fährt ein Fünftel bis ein Zehntel der Kadenz aller anderen — und ist der
einzige ohne Abstieg.

---

# WAS ALLE ÜBERLEBENDEN TEILEN

Ehrlich beantwortet: **wenig.** Die Frage unterstellt, dass es eine Gruppe
„Überlebende" gibt. Nach dieser Messung besteht sie aus **einem** Kanal.

| Merkmal | Historically | quack doc | History Mapped Out | First Humans | Folks of Yore | Prof. Historian |
|---|---|---|---|---|---|---|
| Niveau hält | **✅ 3,3 J** | ❌ −12× | ❌ −8× | ⬜ zu jung | ❌ −13× | ❌ −68× |
| Publikationsdauer | 39,8 Mon. | 29,0 | 40,2 | 11,8 | 16,5 | 3,4 |
| Kadenz | **0,13/Wo** | 1,00 | 0,77 | 0,99 | 0,30 | 1,65 |
| Serienformel | **keine** | Iceberg 7,3× | Doppelpunkt 0,9× | DNA 0,6× | schwach | schwach |
| Themenbreite | **breit** | breit | eng (44 % Krieg) | eng (76 % DNA) | mittel | eng (46 % Antike) |
| Top-3-Anteil an Views | 31 % | 23 % | 18 % | 52 % | 87 % | 87 % |
| Länge heute | 31 min | 49 min | 26 min | 9 min | 22 min | 15 min |
| Durchbruch-Video | keins | ja | ja (2-stufig) | ja | nein | nein |

Was **alle sechs** tatsächlich teilen [gemessen]:

1. **Sie werden länger.** Fünf von fünf auswertbaren.
2. **Sie haben mindestens eine Playlist-Serie.** Sechs von sechs — aber der
   Effekt reicht von 7,3× bis 0,5×.
3. **Sie bleiben bei Geschichte.** Kein Kanal wechselt die Nische. Innerhalb
   der Nische wandern alle.

Was die **drei mit tragfähigem Fundament** (Historically, quack doc, History
Mapped Out) von den drei ausreißergetragenen unterscheidet [abgeleitet]:
Ihre drei größten Videos tragen **18–31 %** der Gesamtviews. Bei First Humans,
Folks of Yore und Professor Historian sind es **52–87 %**. Das ist die
sauberste Trennlinie der Erhebung und sie lässt sich schon nach 20 Videos
messen — **lange bevor man weiß, ob ein Kanal hält.**

---

# WAS DAVON ÜBERTRAGBAR IST

Für einen Kanal mit **0,5 Uploads/Woche, 8–15 min, Alltagsfragen an die
Vergangenheit**:

### 1. Die niedrige Kadenz hat einen Beleg — genau einen

Historically ist der einzige Kanal der Gruppe mit vergleichbarer Kadenz
(0,13/Wo gegen geplante 0,5/Wo) und der einzige ohne Abstieg. Das stützt die
Planung. **Es ist ein einziger Fall**, und die naheliegende Gegenerklärung
(1,33 Mio. Abonnenten tragen ein Plateau, das 0,13/Wo allein nicht erzeugt)
lässt sich mit diesen Daten nicht ausschließen. Übertragbar als *Ermutigung,
nicht als Beweis*.

### 2. Der Zielkorridor 8–15 min steht gegen den Trend der Nische

Fünf von fünf Kanälen verlängern, vier auf über 20 Minuten. **Nur der jüngste
Kanal der Gruppe liegt heute im geplanten Band** — und er steigt. Zwei
Lesarten, beide zulässig:

- *Die Nische wandert nach oben, 8–15 min ist ein auslaufendes Format.*
- *8–15 min ist die Einstiegslänge; die Verlängerung ist etwas, das etablierte
  Kanäle tun, weil sie es können — sie ist Folge des Erfolgs, nicht Ursache.*

Die zweite Lesart wird davon gestützt, dass **alle Verlängerungen den Abstieg
nicht aufhielten**. Praktische Konsequenz: bei 8–15 min starten wie geplant,
aber die Länge als offene Variable führen und nicht als Konfigurationskonstante
behandeln.

### 3. Serienbildung ist kein Haltbarkeitsmittel

Der Auftrag fragte, ob es mehr Iceberg-artige Serien gibt. **Nein.** Und die
eine Serie, die messbar wirkt, hat ihren Kanal nicht gehalten: der
Iceberg-Anteil stieg auf 97 %, während der Median um Faktor 12 fiel; die
Erholungsspur in 2026Q3 kommt aus den **Nicht**-Iceberg-Videos. Bei First
Humans schneidet die eigene Serienformel **schlechter** ab als der Rest.
Historically hält ohne jede Titelformel.

Für die eigene Planung heißt das: eine wiederkehrende Reihe ist erlaubt, aber
sie ersetzt keine Videoqualität, und ein hoher Serienanteil ist eher ein
Warnsignal als ein Ziel. Das widerspricht der Titelanker-Regel aus dem
BibelTube-Repo — dort ist die wiederkehrende Wortformel Erfolgsmerkmal. **Für
diesen Kanal gilt sie nicht.**

### 4. Der Durchbruch-Mechanismus, der zweimal funktioniert hat

In beiden übertragbaren Fällen (quack doc, First Humans) war der Durchbruch
ein **Formatwechsel bei gleichbleibendem Thema** — nicht ein Themenwechsel:

- quack doc: Länge ×5,8, Kadenz ÷3, feste Titelformel. Thema unverändert.
- First Humans: Länge unverändert, Kadenz ×1,5, **Gegenstand von der Kategorie
  zum benannten Rätsel** (Tutanchamun, Dyatlov-Pass, Göbekli Tepe).

Der First-Humans-Fall ist der direkt übertragbare: **ein bekannter Aufhänger
bringt die Suchanfragen, das Video liefert den zeitlosen Stoff dahinter** —
das ist wörtlich die Bauform aus `README.md`, hier zum ersten Mal mit einem
Vorher-Nachher-Beleg (7.659 → 194.796). Der Themenkalender in
`recherche/themen-erklaerkanal.md` arbeitet bereits so.

Der Folks-of-Yore-Fall ist der zweite übertragbare Hebel und passt zur eigenen
Bauform: **Titel in der zweiten Person mit Gegenwartsbezug**
(*„Your ‚Busy' Life Would Disgust an Ancient Roman"*, 657.870) statt
Beschreibung der Vergangenheit (*„What It Was Actually Like to…"*, 1.871).
Faktor 31 im 5er-Median. Dass das Niveau danach nicht hielt, entwertet den
Titelbefund nicht — es zeigt nur, dass ein Titel ein Video trägt und keinen
Kanal.

### 5. Die Frühwarnzahl: Top-3-Anteil

Ab etwa 20 Videos lässt sich messen, ob ein Kanal ein Fundament oder nur
Treffer hat. **Unter 35 % Top-3-Anteil = getragen. Über 50 % = ein Treffer,
kein Niveau.** Diese Zahl hätte Axen und Folks of Yore als das erkannt, was
sie sind, ohne auf den Absturz zu warten. Sie sollte im eigenen Kanal ab
Video 20 mitlaufen.

### 6. Was nicht übertragbar ist

**Der Abstieg lässt sich nicht vermeiden, indem man etwas anders macht** —
jedenfalls nicht aus diesen Daten heraus. An beiden großen Abstürzen blieben
Länge, Kadenz, Titelformel und Thema unverändert. Wer aus dieser Erhebung eine
Regel „so verhindert man den Abfall" ableitet, liest etwas hinein, das nicht
gemessen wurde.

---

# WAS OFFEN BLEIBT

### Messtechnische Vorbehalte

- **View-Zahlen sind kumulativ, nicht altersnormalisiert.** Ein Video aus
  2024Q4 hatte 21 Monate Zeit, eines aus 2026Q3 einen Monat. **Jede
  fallende Kurve dieses Berichts ist dadurch systematisch überzeichnet.**
  Drei Gegenargumente, warum die Abstiege trotzdem echt sind: (a) Historically
  zeigt trotz desselben Effekts *keinen* Abstieg; (b) First Humans steigt
  gegen den Effekt; (c) ein Faktor 12 über fünf Quartale ist zu groß für
  reine Nachlaufakkumulation. Wie groß der Alterseffekt genau ist, bleibt
  **[unbekannt]** — dafür bräuchte es `get_daily_analytics` auf fremde
  Kanäle, was die API nicht hergibt.
- **64 von 376 Datumsangaben sind [abgeleitet]** (History Mapped Out ab
  Position 71). Betroffen sind alle HMO-Quartale ab 2025Q2. Die
  Upload-*Reihenfolge* ist auch dort gemessen, nur der Tag ist rekonstruiert.
  Auf Halbjahresebene ist der Fehler klein, auf Quartalsebene kann er einzelne
  Videos über eine Grenze schieben. Nachholbar: 300 weitere
  `youtube_video_details`-Aufrufe stehen nach 24 h wieder zur Verfügung.
- **Das jeweils letzte Quartal (2026Q3) ist unvollständig** — es endet am
  Erhebungstag. Insbesondere die quack-doc-Erholung (n = 6) steht auf dünner
  Basis.
- **Kein Kanal wurde gesichtet, kein Transkript gelesen.** Alle Aussagen über
  Themen und Formate stammen aus Titeln, Längen und Playlist-Namen. Was
  inhaltlich im Video passiert, ist **[unbekannt]**.
- **Die Themenklassifikation ist eine Schlagwort-Heuristik** und erfasst je
  nach Kanal 39 % bis 82 % der Titel. Die Prozentzahlen sind Größenordnungen,
  keine Messwerte.
- **Abonnentenzahlen und Gesamtviews sind Momentaufnahmen vom 2026-08-11.**

### Inhaltlich offen

1. **Warum fallen quack doc und History Mapped Out?** Aus den Metadaten nicht
   beantwortbar. Kandidaten, alle ungeprüft: Sättigung des Themas,
   Algorithmuswechsel, sinkende Thumbnail-/Titelqualität, Konkurrenz durch
   KI-Massenware, Ermüdung der Serie. Was davon zutrifft, ist **[unbekannt]**.
2. **Trägt Historically wegen der Kadenz oder wegen der Marke?** Nicht
   trennbar bei n = 1. Ein Test wäre ein zweiter Kanal mit ≤0,2/Wo und
   kleiner Abonnentenbasis — in dieser Gruppe existiert er nicht.
3. **Ist der Gipfel im 2. Lebensjahr ein Nischenmuster oder ein Zufall?**
   Zwei Fälle. Mit sechs bis acht weiteren Kanälen aus der
   History-Explainer-Nische wäre das prüfbar — die Kanalliste aus
   `recherche/nischen-kanal-2.md` (Mapped History, Ollie Bye) böte zwei
   Kandidaten mit 5,9 bzw. 12 Jahren Historie.
4. **Hält First Humans?** Der Kanal steht heute genau dort, wo quack doc im
   Monat 12 stand. Eine Wiederholung dieser Messung in sechs Monaten wäre der
   billigste Erkenntnisgewinn dieses ganzen Berichts.
5. **Was ist mit den Shorts?** Historically hat eine Shorts-Playlist mit 31
   Videos, die hier bewusst nicht erhoben wurde. Ob Shorts zur Haltbarkeit
   beitragen, ist **[unbekannt]**.

### Nächster sinnvoller Schritt

Die Messung in **sechs Monaten** (2027-02) wiederholen, mit denselben sechs
Kanälen plus Mapped History und Ollie Bye. Drei Fragen wären dann
beantwortbar, die es heute nicht sind: ob quack docs Erholung trägt, ob First
Humans in dieselbe Kurve läuft, und ob Historically sein Plateau ins vierte
Jahr trägt. Kosten: 0 Credits, etwa 400 API-Aufrufe, verteilt auf zwei Tage
wegen des Tageskontingents.
