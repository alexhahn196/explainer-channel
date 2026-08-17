# Sagt die Themenwahl die Views vorher?

> Erhebung 2026-08-11. **0 Credits, keine Videosichtung, keine Transkripte.**
> Korpus: 429 Long-Form-Videos aus 9 Kanälen der History-Explainer-Nische.
>
> **Antwort in einem Satz: Nein. Keines der sieben geprüften Themenmerkmale
> sagt die Abrufzahlen vorher.**
>
> Das ist kein „wir haben nichts gefunden, also ist da vielleicht doch was" —
> für ein Merkmal (`vorwissen`) ist der Test stark genug, um einen Effekt der
> Größe 3× auszuschließen. Für die übrigen sechs ist er zu schwach, um
> überhaupt etwas zu zeigen. Beide Fälle stehen unten getrennt.

## Nachweis der Blindheit

Die Klassifikation liegt im Commit **`8ae6ad0`** — er enthält die
Merkmalszuordnung aller 429 Titel und **keine einzige Abrufzahl**. Erst danach
wurden die Views dazugeholt. Zwei Dateien belegen das Verfahren:

- [`regeln/daten/themen_blind_vorlage.tsv`](daten/themen_blind_vorlage.tsv) —
  nur `kanal_id`, `video_id`, `titel`; zufällig gemischt mit festem Seed
  20260811, also reproduzierbar und ohne Erfolgssortierung.
- [`regeln/daten/themen_klassifikation.tsv`](daten/themen_klassifikation.tsv) —
  das Ergebnis, mit Gütespalte.

Nachrechenbar sind die Zahlen unten mit
[`regeln/daten/themen_test.py`](daten/themen_test.py) über
[`regeln/daten/themen_korpus.tsv`](daten/themen_korpus.tsv) — beide im Repo,
das Skript läuft ohne Argumente und ohne Netzzugriff. Es gibt rohe,
**unkorrigierte** p-Werte aus; die Korrekturen stehen nur hier im Bericht.

**Ein Vorbehalt, der genannt werden muss:** Ich selbst war für diesen Korpus
*nicht* blind — die Top- und Flop-Videos der sechs G2-Kanäle standen aus der
vorangegangenen Haltbarkeitsmessung bereits fest. Die Klassifikation habe ich
deshalb nicht selbst vorgenommen, sondern an **zwei unabhängige Bewerter ohne
jede Kenntnis dieser Untersuchung** übergeben, die ausschließlich die gemischte
Titelliste sahen. Die 48 in mindestens einem Merkmal strittigen Titel entschied
ein dritter, ebenfalls blinder Bewerter.

Übereinstimmung der beiden unabhängigen Bewerter [gemessen]:

| Merkmal | Übereinstimmung | uneinig |
|---|---:|---:|
| benannte_person | 100,0 % | 0 |
| benanntes_raetsel | 100,0 % | 0 |
| frageform | 100,0 % | 0 |
| selbsterfahren | 99,5 % | 2 |
| koerper_alltag | 98,1 % | 8 |
| zeitbezug | 95,6 % | 19 |
| vorwissen | 94,9 % | 22 |

381 der 429 Titel waren in **allen sieben** Merkmalen unstrittig. Die Kodierung
ist damit reliabel genug, dass ein fehlender Effekt nicht auf Kodierrauschen
geschoben werden kann.

## Korpus

| Quelle | Videos | Datumsgüte |
|---|---:|---|
| `regeln/daten/g2-videos.tsv` (committet) | 376 | 312 exakt, 64 abgeleitet |
| Ink Explainer `UCpgrEMx8diLrw7YNQ6r3uUw` (nacherhoben) | 13 | relativ |
| Axen `UC_7R-sfi7bi8dkzmSlBdUVw` (nacherhoben) | 14 | relativ |
| Mapped History `UCInfdX6B8ej4f2zge4fVuWw` (nacherhoben) | 26 | relativ |
| **Summe** | **429** | |

**Von den drei im Auftrag genannten Quellen lag nur eine im Repo.** Die
Ink/Axen-Daten und die G1/G3-Listen sind hier nie committet worden — sie
stammen aus Sitzungen gegen andere Repositories. Ich habe die drei fehlenden
Kanäle aus den in `recherche/nischen-kanal-2.md` dokumentierten IDs neu
erhoben; alle drei Listen sind gegen `videosCount` der API auf
Vollständigkeit geprüft [gemessen]. Ink Explainer 13 + Axen 14 = 27 statt der
genannten 26, weil Axen zwei Stunden vor der Erhebung ein weiteres Video
veröffentlicht hat.

Kanäle mit mindestens 10 Videos — nur diese gehen in den Test ein:

| Kanal | n | Median Views |
|---|---:|---:|
| History Mapped Out | 134 | 95.000 |
| quack doc | 126 | 61.801 |
| First Humans | 50 | 47.716 |
| Mapped History | 26 | 14.000 |
| Professor Historian | 24 | 18.160 |
| Historically | 21 | **1.899.027** |
| Folks of Yore | 21 | 6.397 |
| Axen | 14 | 25.000 |
| Ink Explainer | 13 | 197.000 |

---

# Ergebnis je Merkmal

Der Test läuft **kanalintern**: je Kanal Median mit Merkmal gegen Median ohne,
dann der Median dieser Verhältnisse über die Kanäle. Ein Kanal zählt nur mit,
wenn er in **beiden** Gruppen mindestens 3 Videos hat — sonst ist der Median
nicht definiert. Der Zufallstest mischt die Views **innerhalb jedes Kanals**
und wiederholt das 10.000-mal (die vorgegebenen 100 Durchläufe reichen nur für
eine p-Auflösung von 0,01; die Größenordnung ist dieselbe).

## Alle 429 Videos

| Merkmal | Richtung | Faktor kanalintern | Faktor gepoolt | gleiche Richtung | p (Effekt) | p (Konsistenz) |
|---|---|---:|---:|---:|---:|---:|
| zeitbezug = heute | niedriger | 0,34× | 0,19× | 2 von 3 | **0,014** | 1,000 |
| zeitbezug = urzeit | höher | 4,08× | 0,83× | 2 von 3 | **0,041** | 1,000 |
| vorwissen | höher | 1,70× | 1,70× | 4 von 6 | 0,064 | 0,687 |
| benanntes_raetsel | höher | 3,86× | 0,85× | 1 von 1 | 0,082 | 1,000 |
| selbsterfahren | höher | 1,68× | 1,26× | **4 von 4** | 0,211 | 0,127 |
| frageform | höher | 2,79× | 2,88× | 2 von 2 | 0,353 | 0,492 |
| koerper_alltag | niedriger | 0,71× | 0,37× | 3 von 6 | 0,360 | 1,000 |
| zeitbezug = benannte_epoche | höher | 1,28× | 1,38× | 3 von 6 | 0,377 | 1,000 |
| benannte_person | niedriger | 0,94× | 1,06× | 2 von 3 | 0,865 | 1,000 |
| zeitbezug = zeitlos | höher | 1,01× | 1,06× | 4 von 7 | 0,961 | 1,000 |

## Nur Videos älter als 90 Tage (Alterskontrolle, 329 Videos)

| Merkmal | Richtung | Faktor kanalintern | Faktor gepoolt | gleiche Richtung | p (Effekt) | p (Konsistenz) |
|---|---|---:|---:|---:|---:|---:|
| selbsterfahren | höher | 7,12× | 0,67× | 2 von 2 | **0,0002** | 0,518 |
| vorwissen | höher | 1,78× | 1,85× | 4 von 6 | 0,065 | 0,688 |
| benanntes_raetsel | höher | 7,10× | 0,72× | 1 von 1 | 0,101 | 1,000 |
| zeitbezug = urzeit | **niedriger** | **0,15×** | 0,39× | 1 von 1 | 0,114 | 1,000 |
| zeitbezug = benannte_epoche | höher | 1,75× | 1,76× | 3 von 5 | 0,120 | 1,000 |
| zeitbezug = heute | niedriger | 0,54× | 0,16× | 2 von 3 | 0,356 | 1,000 |
| zeitbezug = zeitlos | niedriger | 0,84× | 0,94× | 2 von 4 | 0,578 | 1,000 |
| koerper_alltag | niedriger | 0,82× | 0,28× | 1 von 2 | 0,708 | 1,000 |
| benannte_person | niedriger | 0,90× | 1,47× | 2 von 3 | 0,819 | 1,000 |
| frageform | — | — | — | **0 Kanäle auswertbar** | — | — |

Die Alterskontrolle ändert die Kanalzusammensetzung stark: Ink Explainer, Axen
und Professor Historian fallen ganz heraus (sie haben 3, 4 und 5 Videos über
90 Tage), First Humans schrumpft von 50 auf 33.

---

# Die drei Gegenproben

## 1. Der Zufallstest — das entscheidende Kriterium

Deine Vorgabe war: **ein Merkmal, das in 8 von 10 Kanälen dieselbe Richtung
zeigt, ist belastbar.** Dieser Test ist mit diesem Korpus gar nicht erst
erreichbar — je Merkmal sind **1 bis 7 Kanäle** auswertbar, nie 10. Der Grund
ist die Seltenheit der Merkmale: `benannte_person` trifft auf 25 von 429
Titeln zu, `frageform` auf 22, `heute` auf 25. In den meisten Kanälen kommen
davon keine 3 Stück vor.

**Kein einziges Merkmal besteht den Richtungstest.** Die beste
Richtungskonsistenz ist 4 von 4 (`selbsterfahren`, alle Videos) — und selbst
die entsteht in 12,7 % der Zufallsdurchläufe von allein. Alle anderen liegen
bei p ≥ 0,49. Bei vier Kanälen ist „alle vier zeigen dieselbe Richtung" schlicht
kein seltenes Ereignis.

## 2. Mehrfachvergleiche — nur ein Test überlebt, und der trägt nicht

19 Effekt-Tests wurden gerechnet. Bei α = 0,05 sind rein zufällig etwa ein
Treffer zu erwarten; gefunden wurden drei mit p < 0,05. Nach Holm-Korrektur
(familienweise α = 0,05) bleibt **genau einer** übrig:

| Lauf | Merkmal | p roh | Holm-Schwelle | Urteil |
|---|---|---:|---:|---|
| ≥90 d | selbsterfahren | 0,0002 | 0,0026 | **signifikant** |
| alle | zeitbezug = heute | 0,0141 | 0,0028 | nicht signifikant |
| alle | zeitbezug = urzeit | 0,0414 | 0,0029 | nicht signifikant |
| alle | vorwissen | 0,0643 | 0,0031 | nicht signifikant |
| … 15 weitere | | ≥ 0,065 | | nicht signifikant |

**Woraus besteht dieser eine Befund?** Aus elf Videos in zwei Kanälen
[gemessen]:

| Kanal | Views | Titel |
|---|---:|---|
| quack doc | **1.836.957** | What Dying From Every Deadly Disease Feels Like |
| quack doc | **1.505.065** | The Most Deadly Diseases Iceberg Explained |
| quack doc | 26.261 | The Disturbing Sleep & Dream Iceberg Explained |
| quack doc | 18.663 | The Most Brutal Surgeries In Human History |
| Folks of Yore | **657.870** | Your „Busy" Life Would Disgust an Ancient Roman |
| Folks of Yore | 101.666 | Why Ancients Treasured Sadness and Modernity Forbids It |
| Folks of Yore | 73.711 | The Ancient Greeks Wouldn't Recognize What We Call Love |
| Folks of Yore | 12.234 | What Ancient Romans Understood About FAILURE… |
| Folks of Yore | 8.413 | Your Doomscrolling Was Diagnosed 1.700 Years Ago |
| Folks of Yore | 8.357 | Why You Wake Up at 3 AM Every Night |
| Folks of Yore | 1.871 | What It Was Actually Like to Live in a Medieval Castle |

Bei quack doc besteht die Merkmalsgruppe aus **vier** Videos, von denen zwei
das Nr.-1- und das Nr.-4-Video des Kanals sind. Der Median dieser vier liegt
per Konstruktion zwischen 1,5 Mio. und 26.261 — eine Zahl, die durch ein
einziges anderes Video um den Faktor 50 springen würde. In beiden Kanälen
enthält die Merkmalsgruppe das jeweils erfolgreichste Video des Kanals
überhaupt. **Das ist kein Effekt, das ist eine Beschreibung von zwei
Ausreißern.**

## 3. Vorzeichenstabilität — ein Merkmal dreht sich um

| Merkmal | alle Videos | nur ≥ 90 Tage | stabil? |
|---|---:|---:|---|
| **zeitbezug = urzeit** | **4,08×** | **0,15×** | **NEIN** |
| zeitbezug = zeitlos | 1,01× | 0,84× | NEIN (aber ≈ 1) |
| selbsterfahren | 1,68× | 7,12× | ja |
| benanntes_raetsel | 3,86× | 7,10× | ja |
| vorwissen | 1,70× | 1,78× | ja |
| zeitbezug = benannte_epoche | 1,28× | 1,75× | ja |
| zeitbezug = heute | 0,34× | 0,54× | ja |
| koerper_alltag | 0,71× | 0,82× | ja |
| benannte_person | 0,94× | 0,90× | ja |

`zeitbezug = urzeit` kippt von **4,08× (höher)** auf **0,15× (niedriger)** —
ein Vorzeichenwechsel um mehr als eine Größenordnung, ausgelöst allein davon,
dass zwei Kanäle aus dem Test fallen. In der Gesamtrechnung tragen ihn Axen
(8,44×) und Ink Explainer (4,08×), beides Kanäle mit fast ausschließlich
Videos unter 90 Tagen. Bleibt nur First Humans übrig, zeigt es 0,28×. Das ist
das Lehrbuchbeispiel dafür, dass hier Kanäle verglichen werden und keine
Themen.

---

# Warum die Kanaltrennung die Antwort verändert hat

Deine Vorgabe, kanalintern statt gepoolt zu rechnen, war die richtige
Entscheidung — sie kehrt bei vier Merkmalen das Ergebnis um [gemessen]:

| Merkmal | gepoolt | kanalintern | Deutung |
|---|---:|---:|---|
| benanntes_raetsel | 0,85× | 3,86× | gepoolt unsichtbar, weil es fast nur bei einem kleinen Kanal vorkommt |
| zeitbezug = urzeit | 0,83× | 4,08× | dito |
| selbsterfahren (≥90 d) | 0,67× | 7,12× | dito |
| koerper_alltag | 0,37× | 0,71× | gepoolt dreimal so stark wie real |

Der gepoolte Wert misst überwiegend, **welcher Kanal ein Merkmal benutzt**,
nicht ob es wirkt. Zwischen dem schwächsten und dem stärksten Kanalmedian
liegt Faktor **297** (Folks of Yore 6.397 gegen Historically 1.899.027) — mehr
als jeder gemessene Merkmalseffekt. Wer gepoolt rechnet, misst hauptsächlich
diesen Abstand.

Zugleich zeigt die Varianzzerlegung, dass auch der Kanal nicht die Hauptrolle
spielt: von der Streuung der log-Views liegen **30,8 % zwischen** den Kanälen
und **69,2 % innerhalb** [abgeleitet]. Der größte Teil der Unterschiede
besteht also zwischen Videos **desselben** Kanals — und genau diesen Teil
erklärt keines der sieben Titelmerkmale zuverlässig.

---

# Trennschärfe: Null-Befund oder blinder Test?

Entscheidend für die Deutung: Hätte der Test einen Effekt überhaupt gefunden?
Prüfung durch Simulation — Views innerhalb jedes Kanals mischen (damit jeder
echte Effekt zerstört ist), dann die Videos mit Merkmal künstlich mit Faktor
f multiplizieren, dann derselbe Test. Anteil der Läufe mit p < 0,05
[gemessen, 60–80 Simulationen je Zelle]:

**Alle Videos**

| Merkmal | ausw. Kanäle | f = 1,5 | f = 2 | f = 3 | f = 5 |
|---|---:|---:|---:|---:|---:|
| **vorwissen** | 6 | 30 % | **74 %** | **99 %** | 100 % |
| benannte_person | 3 | 11 % | 36 % | 70 % | 98 % |
| koerper_alltag | 6 | 9 % | 25 % | 56 % | 86 % |
| selbsterfahren | 4 | 14 % | 28 % | 54 % | 84 % |
| benanntes_raetsel | 1 | 11 % | 21 % | 35 % | 59 % |
| frageform | 2 | 2 % | 5 % | 14 % | 21 % |

**Nur ≥ 90 Tage**

| Merkmal | ausw. Kanäle | f = 1,5 | f = 2 | f = 3 | f = 5 |
|---|---:|---:|---:|---:|---:|
| vorwissen | 6 | 24 % | 62 % | 98 % | 100 % |
| koerper_alltag | 2 | 10 % | 25 % | 55 % | 80 % |
| selbsterfahren | 2 | 7 % | 22 % | 53 % | 82 % |
| benannte_person | 3 | 2 % | 15 % | 55 % | 89 % |
| benanntes_raetsel | 1 | 4 % | 6 % | 18 % | 42 % |
| frageform | 0 | — | — | — | — |

**Das trennt den Bericht in zwei Aussagen:**

- **`vorwissen` ist echt geprüft und echt negativ.** Der Test hätte eine
  Verdreifachung mit 99 % Wahrscheinlichkeit gefunden und eine Verdopplung mit
  74 %. Gefunden wurde 1,70× bei p = 0,064 und 4 von 6 Kanälen. **Ein Effekt
  der Größenordnung 3× existiert hier nicht.** Ob ein Effekt von 1,5× existiert,
  bleibt offen — dafür reicht die Trennschärfe (30 %) nicht.
- **Die anderen sechs sind nicht geprüft, sondern nur nicht gefunden.**
  Bei `frageform` hätte selbst eine Verdreifachung nur in 14 % der Fälle
  Signifikanz erzeugt; bei ≥90 Tagen ist das Merkmal in **keinem** Kanal
  auswertbar. Ein Nicht-Befund dort ist keine Information.

---

# Der Zirkularitätsvorbehalt

Zwei der sieben Merkmale sind **aus denselben Videos abgeleitet, die sie jetzt
vorhersagen sollen.** In `regeln/g2-haltbarkeit.md` waren die beiden
Durchbrüche:

- First Humans, 2026-01-19, *Ancient DNA Reveals Tutankhamun's Shocking Family
  Secret* — dort beschrieben als Wechsel „von der Kategorie zum benannten
  Rätsel".
- Folks of Yore, 2026-01-23, *Your „Busy" Life Would Disgust an Ancient Roman*
  — dort beschrieben als Wechsel zu Gegenwartsbezug und Selbsterfahrung.

Die Merkmalsdefinitionen im Auftrag zitieren genau diese Fälle
(„Tutanchamun, Roanoke" gegen „Herkunft der Pikten"). Damit gilt:

- **`benanntes_raetsel` ist in genau einem Kanal auswertbar — First Humans.**
  Dem Kanal, aus dem die Definition stammt. Es gibt zu diesem Merkmal **null
  unabhängige Evidenz**; der 3,86× beziehungsweise 7,10× ist die
  Wiedergabe der Beobachtung, aus der das Merkmal gebaut wurde.
- **`selbsterfahren`** wird im signifikanten Lauf zur Hälfte von genau dem
  Folks-of-Yore-Video getragen, aus dem der Begriff stammt.

Ein Merkmal an den Daten zu prüfen, aus denen es abgeleitet wurde, ist kein
Test. Sauber wäre: die beiden Merkmale an einem **neuen** Kanalsatz prüfen,
der bei der Definition keine Rolle gespielt hat.

---

# Klare Aussage

## Welche Themenmerkmale sagen Views vorher?

**Keines.**

Kein Merkmal besteht den Richtungstest über die Kanäle (bestes Ergebnis 4 von
4 bei p = 0,127; deine Schwelle von 8 aus 10 ist mit diesem Korpus nicht
einmal erreichbar). Kein Merkmal überlebt die Mehrfachvergleichskorrektur
außer einem, der auf elf Videos aus zwei Kanälen beruht und in beiden das
Top-Video des Kanals enthält. Ein Merkmal dreht bei der Alterskontrolle das
Vorzeichen um mehr als eine Größenordnung.

Im Einzelnen:

| Merkmal | Urteil |
|---|---|
| **vorwissen** | **kein Effekt der Größe 3× vorhanden** — gut geprüft, negativ. Tendenz leicht positiv (1,7×), aber nur 4 von 6 Kanälen und p = 0,064 in beiden Läufen. |
| **benannte_person** | kein Effekt sichtbar (0,90–0,94×), Trennschärfe mittel. Wer benannte Personen meidet, verliert nach dieser Messung nichts. |
| **benanntes_raetsel** | **nicht testbar** — nur ein auswertbarer Kanal, und das ist der Kanal, aus dem das Merkmal stammt. Zirkulär. |
| **selbsterfahren** | **einziger formal signifikanter Befund, aber nicht belastbar** — 2 Kanäle, 11 Videos, beide Gruppen enthalten das Top-Video ihres Kanals, Richtungstest p = 0,52. |
| **koerper_alltag** | kein Effekt (0,71–0,82×), Richtung uneinheitlich (3 von 6). Der gepoolte Wert von 0,37× ist ein Kanalgrößen-Artefakt. |
| **zeitbezug** | kein Effekt. `urzeit` kippt von 4,08× auf 0,15×, `zeitlos` liegt bei 1,01×, `benannte_epoche` bei 1,28× mit 3 von 6 Kanälen. |
| **frageform** | **nicht testbar** — 22 von 429 Titeln, 2 auswertbare Kanäle bei allen Videos, 0 bei der Alterskontrolle, Trennschärfe 5 % bei Verdopplung. |

## Was das für den eigenen Kanal heißt

**Die Themenwahl auf Titelebene ist nach dieser Messung kein Hebel — aber
auch nicht widerlegt als einer.** Praktisch:

1. **Titelmerkmale nicht als Auswahlkriterium für den Themenkalender
   verwenden.** Der Kalender in `recherche/themen-erklaerkanal.md` steht auf
   Anlassbindung und Belegbarkeit; diese Messung liefert keinen Grund, ihn nach
   „Selbsterfahrung" oder „Frageform" umzusortieren.
2. **Der Umkehrschluss gilt aber auch:** Es gibt keinen gemessenen Grund,
   Alltags- und Körperthemen zu bevorzugen — die Bauform „Alltagsfrage an die
   Vergangenheit" aus `README.md` bekommt aus diesen Daten **keine
   Bestätigung**. `koerper_alltag` liegt bei 0,71× und uneinheitlich.
3. **Was in der Vorgängermessung als Durchbruch-Mechanismus erschien, hält dem
   Test nicht stand.** Die beiden Durchbruchvideos von First Humans und Folks
   of Yore sind Einzelfälle; als Merkmal über 429 Videos ist von ihnen nichts
   übrig.
4. **69 % der Streuung liegt zwischen Videos desselben Kanals.** Was diesen
   Anteil erklärt, ist mit Titelmetadaten nicht erreichbar — Thumbnail,
   Veröffentlichungszeitpunkt, Empfehlungsdynamik und die tatsächliche
   Videoqualität stehen alle außerhalb dieses Korpus.

---

# Was offen bleibt

- **Der Korpus ist zu klein für seltene Merkmale.** Fünf der sieben Merkmale
  kommen bei unter 8 % der Titel vor. Um sie zu prüfen, bräuchte es entweder
  deutlich mehr Kanäle oder eine gezielte Stichprobe, die das Merkmal
  anreichert.
- **Views sind kumulativ.** Die Alterskontrolle (≥90 Tage) mildert das, löst
  es nicht: ein Video von 2023 hatte drei Jahre Zeit, eines von Mai 2026 drei
  Monate. Der verbleibende Alterseffekt ist **[unbekannt]**.
- **64 der 429 Datumsangaben sind abgeleitet** (History Mapped Out ab Position
  71, aus `regeln/daten/g2-videos.tsv` übernommen), 53 weitere haben nur
  Relativangaben. Betroffen ist ausschließlich die 90-Tage-Grenze, nicht die
  Views.
- **Titel sind nicht Themen.** Klassifiziert wurde der Titel, nicht das Video.
  Ein Video über Schlaf mit einem Titel ohne Schlafbezug zählt hier als
  `selbsterfahren = nein`. Ob die Merkmale am Videoinhalt gemessen anders
  wirken, ist **[unbekannt]** — dafür wären Transkripte nötig.
- **Thumbnails fehlen vollständig.** Sie sind der wahrscheinlichste Kandidat
  für die 69 % unerklärte Streuung innerhalb der Kanäle und in dieser Erhebung
  gar nicht erfasst.
- **Der Test misst Median-Verhältnisse, keine Wechselwirkungen.** Ob
  `selbsterfahren` in Kombination mit `zeitbezug = heute` wirkt, während
  keines allein wirkt, ist mit n = 429 und 9 Kanälen nicht prüfbar.

## Nächster sinnvoller Schritt

Wenn die Frage weiterverfolgt werden soll, ist der billigste Weg **nicht**
mehr Merkmale, sondern **mehr Kanäle**: Ein Korpus aus 30 bis 40
History-Explainer-Kanälen mit je ≥ 20 Videos brächte den Richtungstest
erstmals in den Bereich, für den er gedacht war (8 von 10 Kanälen). Kosten:
0 Credits, etwa 40 `youtube_channel_videos`-Aufrufe plus eine Kodierrunde.
Erst dann lohnt sich der Blick auf seltene Merkmale.

Alternativ — und mit höherem erwartetem Ertrag — die Streuung **innerhalb**
eines Kanals angehen, wo 69 % der Varianz sitzt: dieselben sieben Merkmale
gegen Thumbnail-Merkmale und Veröffentlichungszeitpunkt antreten lassen, an
einem einzigen großen Kanal (History Mapped Out, 134 Videos, oder quack doc,
126).
