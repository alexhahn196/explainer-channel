# Vergleichskanäle: Treffer der letzten 90 Tage

**Stand 17.08.2026** — Datenabzug über NexLev, 0 Credits.
Reproduzierbar mit `python3 recherche/daten/pruefe_vergleichskanaele.py`.
Rohdaten: [`daten/vergleichskanaele_videos.json`](daten/vergleichskanaele_videos.json),
Ergebnis: [`daten/vergleichskanaele_bewertet.json`](daten/vergleichskanaele_bewertet.json).

Keine Trendsuche. Abgefragt wurden die sechs benannten Kanäle direkt über ihre
Kanal-ID; es kommt nichts in die Auswertung, was nicht von einem dieser Kanäle
stammt.

## Wie gemessen wurde

| | |
|---|---|
| Kanäle | 6, per ID abgerufen |
| Videos abrufbar | 170 (Katalog, soweit die API ihn hergibt) |
| davon im Fenster | 119 |
| **Treffer** | **28** |
| Trefferschwelle | ≥ 3× Median des **eigenen** Kanals |

**Median statt Mittelwert.** Bei Mogo trägt ein einzelnes Video 398.000 von
insgesamt rund 1,0 Mio. Views im Fenster. Jeder Mittelwert wäre von genau den
Ausreißern bestimmt, die gefunden werden sollen — der Kanal läge dann per
Konstruktion über seinem eigenen Schnitt.

**Das Fenster ist unschärfer als „90 Tage" klingt.** NexLev liefert kein
Uploaddatum, sondern rechnet das relative YouTube-Label zurück: aus
„3 months ago" wird 2026-05-17. Der Bucket „3 months ago" liegt damit
rechnerisch 92 Tage zurück, tatsächlich aber irgendwo zwischen etwa 75 und 105
Tagen. Er ist mitgenommen — ein Schnitt bei exakt 90 Tagen würde einen Bucket
zerteilen, dessen Innenauflösung die Quelle gar nicht hat. Betroffen sind vor
allem die vier Ink-Explainer- und vier Axen-Videos vom 17.05., darunter der
größte Einzelwert der ganzen Erhebung (Axen, 3,2 Mio.).

**Zwei Kataloge sind größer als ihre eigene Zählung.** YouTube meldet für
Banana Explains und Mogo je 31 Videos; das Zusammenführen von Vorwärts- und
Rückwärtsliste ergibt 38 bzw. 35. Gerechnet wurde mit den tatsächlich
gefundenen Videos.

## Treffer je Kanal

### Ink Explainer — 50.100 Abos, Median 215.000

Alle 13 Videos liegen im Fenster; der Kanal ist jünger als das Fenster selbst.
Der Median ist deshalb kein Ruhewert, sondern der Median einer Startphase.

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| 5,6× | 1.200.000 | 17.07. | What Did Ancient Humans Do When It Rained All Week? |
| 4,3× | 933.000 | 17.06. | Why Are We the Only Human Species Left? |
| 3,7× | 796.000 | 17.05. | When Did Ancient Humans Start Drinking Alcohol? |
| 3,2× | 684.000 | 17.07. | How Did Ancient Humans Travel the World? |

### Axen — 56.200 Abos, Median 23.000

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| **139,1×** | 3.200.000 | 17.05. | What Did Ancient Humans Do all Day Before Jobs Existed? |
| 47,8× | 1.100.000 | 17.05. | How Did Ancient Humans Survive the World's Deadliest Predators? |
| 33,6× | 773.000 | 17.06. | How Did Ancient Humans Survive Deadly Winters? |
| 11,4× | 263.000 | 17.05. | How Did Ancient Humans Have Privacy? |
| 5,3× | 123.000 | 17.06. | Why Does the OCEAN Get Creepier the Deeper You Go? |

Die fünf jüngsten Axen-Videos (August, 2.900–9.300 Views) liegen sämtlich
**unter** dem Median. Der Kanal hat seine Treffer im Mai/Juni, nicht jetzt.

### Banana Explains — 4.330 Abos, Median 4.000

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| **115,8×** | 463.000 | 17.07. | Where Do You Go Under Anesthesia? |
| 70,5× | 282.000 | 17.07. | Why Do Wild Animals Ask Humans for Help? |
| 27,2× | 109.000 | 17.07. | How Did Ancient Humans Survive Mosquitoes? |
| 12,2× | 49.000 | 17.07. | Why Do Spiders Terrify Us? |
| 8,0× | 32.000 | 17.07. | What Happens During Lucid Dreaming? |
| 3,8× | 15.000 | 17.07. | When Did Ancient Humans Discover Salt? |
| 3,2× | 13.000 | 17.07. | How Did Ancient Humans Survive Predators? |
| 3,0× | 12.000 | 20.07. | How Did Ancient Humans Survive Extreme Heat? |

Der kleinste Kanal der Auswertung hat die höchste Trefferquote (8 von 38) und
zugleich das schwächste Video überhaupt (121 Views). Bei einem Median von 4.000
ist die 3×-Schwelle mit 12.000 Views leicht zu reißen — die Faktoren dieses
Kanals sind nicht mit denen von Ink Explainer vergleichbar.

### Mogo — 2.710 Abos, Median 3.100

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| **128,4×** | 398.000 | 17.07. | Why Don't We Eat Other Animal Eggs? |
| 51,0× | 158.000 | 17.07. | How Did Ancient Humans Survive Endless Rain? |
| 39,0× | 121.000 | 17.07. | Why Do Animals Save Humans? |
| 34,2× | 106.000 | 17.07. | Why Do Ancient Humans Have Different Blood Types? |
| 14,5× | 45.000 | 03.08. | Do Wild Animals See Humans As Weak? |
| 10,3× | 32.000 | 17.06. | When Did Ancient Humans Actually Start Smoking? |
| 7,4× | 23.000 | 03.08. | What Did Ancient Humans Do During the 100.000 Missing Years? |
| 4,2× | 13.000 | 27.07. | Why Can't You Remember Being a Baby? |
| 3,2× | 9.800 | 20.07. | How Did Wild Cats Become Human Pets? |

### Folks of Yore — 21.200 Abos, Median 5.850

Nur 7 der 22 Videos liegen im Fenster. Genau **ein** Treffer:

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| 45,8× | 268.000 | 17.06. | Why Friendship Today Looks Nothing Like It Did for the Ancients |

Die beiden größten Videos des Kanals (658.000 und 101.000) stammen vom Februar
und liegen außerhalb des Fensters.

### Unknown Frequencies — 57.000 Abos, Median 210.000

Genau **ein** Treffer:

| Faktor | Views | Datum | Titel |
|---:|---:|---|---|
| 5,2× | 1.100.000 | 27.07. | The ENTIRE Story of The Odyssey Explained |

Der Kanal ist der einzige der sechs, der **nicht** „ancient humans" macht,
sondern Kriegsgeschichte und Stoffnacherzählung. Der Odyssee-Treffer ist der
Ausbruch aus dem WW2-Kern des Kanals; die Fortsetzung (Trojanischer Krieg,
05.08., 198.000) liegt mit 0,94× bereits wieder unter dem Median.

## Gibt es ein gemeinsames Muster?

Der Blick auf die 28 Treffer legt drei Muster nahe: fast alles ist eine Frage,
fast alles beginnt mit How/Why/What, und „ancient humans" steht überall. Nur:
das gilt für die Nische insgesamt. Die richtige Frage ist nicht, wie häufig ein
Merkmal in den Treffern ist, sondern ob es dort **häufiger** ist als bei den 91
Videos desselben Fensters, die keine Treffer wurden.

| Merkmal | Treffer | Rest | Lift | p | Urteil |
|---|---:|---:|---:|---:|---|
| Fragetitel (endet auf ?) | 89 % | 71 % | 1,25× | 0,042 | fällt durch |
| beginnt How/Why/What/… | 96 % | 77 % | 1,25× | 0,013 | fällt durch |
| „ancient" im Titel | 57 % | 47 % | 1,21× | 0,242 | fällt durch |
| „human(s)" im Titel | 71 % | 54 % | 1,33× | 0,075 | fällt durch |
| „ancient human(s)" | 54 % | 42 % | 1,28× | 0,189 | fällt durch |
| **Tier-Thema** | 32 % | 11 % | **2,93×** | 0,012 | fällt durch |
| Zuschauer-Körper (you/we) | 18 % | 13 % | 1,35× | 0,366 | fällt durch |
| **„surviv…"** | 21 % | 4 % | **4,87×** | 0,011 | fällt durch |
| Versalien-Wort | 7 % | 10 % | 0,72× | 0,784 | fällt durch |

Neun Merkmale geprüft, Bonferroni-Schwelle also 0,05/9 = 0,0056. **Kein
einziges Merkmal hält.** Die beiden auffälligsten — Tier-Thema und „survive" —
liegen bei p ≈ 0,01: einzeln betrachtet wären sie signifikant, aber bei neun
Versuchen ist ein Wert dieser Größe zu erwarten, ohne dass etwas dahintersteckt.
Die Frageform, die im Treffer-Set so dominant aussieht, hat einen Lift von
1,25× — sie ist der Normalzustand der Nische, kein Erfolgsmerkmal.

Was inhaltlich sichtbar ist, aber die Prüfung nicht besteht:

- **Alltagsbedürfnis in der Vorzeit** — Regen, Winter, Hitze, Mücken, Salz,
  Privatsphäre, „den ganzen Tag vor den Jobs". Das ist der Kern der Nische, und
  genau deshalb trennt es nichts: die Nicht-Treffer sehen genauso aus.
- **Tiere im Verhältnis zum Menschen** — die größten Videos von Mogo und Banana
  sind keine Vorzeitfragen, sondern Tierfragen („Eggs", „Ask Humans for Help",
  „See Humans As Weak", „Spiders"). Der stärkste Lift der Tabelle nach
  „survive", und der einzige, der auch inhaltlich eine eigene Gruppe bildet.
- **Der eigene Körper als Rätsel** — Anesthesia (463.000), Lucid Dreaming,
  Blood Types, „Remember Being a Baby". Bei Banana ist das größte Video kein
  Vorzeitthema, sondern eine Frage an den Zuschauer selbst.

### Die Gegenprobe

Dasselbe Thema, verschiedene Kanäle, im selben Fenster:

| Thema | Spanne | bestes / schwächstes |
|---|---:|---|
| Raubtiere | **282×** | Axen 47,8× ↔ Axen 0,17× |
| Regen | 144× | Mogo 51,0× ↔ Mogo 0,35× |
| Winter | 39× | Axen 33,6× ↔ Mogo 0,87× |
| Rauchen | 9× | Mogo 10,3× ↔ Ink Explainer 1,17× |
| Langeweile | 7× | Banana 1,70× ↔ Mogo 0,25× |
| Toilette | 5× | Mogo 2,48× ↔ Banana 0,50× |
| Alkohol | 4× | Ink Explainer 3,70× ↔ Mogo 0,84× |
| Heirat | 2× | Mogo 0,77× ↔ Banana 0,33× |

Die Zeile „Raubtiere" ist der schärfste Fall: **derselbe Kanal**, dasselbe
Thema, zwei Videos — 47,8× und 0,17×, ein Verhältnis von 282. Beim Winter
liegen vier Kanäle mit derselben Frage zwischen 33,6× und 0,87×. Bei zwei
Themen (Heirat, Toilette) ist das Thema auf *keinem* Kanal ein Treffer.

Das Thema erklärt das Ergebnis also nicht. Was übrig bleibt — Thumbnail,
Veröffentlichungszeitpunkt, Empfehlungsstrom, Kanalzustand — ist mit dieser
Erhebung nicht messbar.

## Gegen unsere 42 Themen

Methode wortgleich aus `pruefe_fragen.py`: Funktionswörter raus, einfaches
Stemming, Grenze 50 %. Damit sind die Zahlen mit `fragen_bewertet.json`
vergleichbar.

**Gegen die 28 Treffer: 0 von 42 über 50 %.** Der höchste Wert ist F33 mit
exakt 50,0 % — und der ist ein Artefakt: geteilt werden nur „what" und „human",
also reine Frageform. Keine unserer Fragen liegt inhaltlich an einem der neuen
Treffer.

**Gegen alle 119 Videos im Fenster: 2 von 42 über 50 %** — beide gegen
Videos, die durchgefallen sind:

| Frage | Ähnlichkeit | nächstes Video | dessen Leistung |
|---|---:|---|---|
| F38 How Did Ancient Egyptians Tell the Time? | **80,0 %** | Mogo: How Did Ancient Humans Tell Time? | **0,09×** (272 Views) |
| F18 How Did Desert Peoples Find Water? | **60,0 %** | Banana: How Did Ancient Humans Find Safe Water? | **0,16×** (638 Views) |
| F24 How Did Sailors Cross the Sea Without Maps? | 50,0 % | Mogo: How Did Ancient Humans Cross Oceans Without Ships? | 0,81× (2.500) |
| F23 Did the Trojan War Actually Happen? | 50,0 % | UF: The Entire Story of The Trojan War & Iliad | 0,94× (198.000) |

Das Video, dem F38 mit 80 % am nächsten kommt, ist mit 272 Views das
zweitschwächste Video im gesamten Fenster (schwächer ist nur Banana mit 121).
Die Titelprüfung misst Nähe zu
**veröffentlichten** Titeln, nicht zu erfolgreichen — die beiden Warnungen sagen
also, dass die Frage schon jemand gestellt hat, und nicht, dass sie trägt. Im
Gegenteil: bei beiden ist sie nachweislich nicht getragen.

**Eine Lücke der Methode, die hier zum ersten Mal beißt.** Wortüberlappung sieht
keine Stoffverwandtschaft. Der Odyssee-Treffer von Unknown Frequencies
(1,1 Mio., 5,2×) hat mit unserem **F22 „Who Was Homer, Really?" eine Ähnlichkeit
von 0,0 %** — kein einziges gemeinsames Inhaltswort, obwohl es derselbe Stoff
ist. Dasselbe bei F24 (Seefahrt) und F25 (griechisches Jenseits), beide 0,0 %
gegen die Homer-Videos. Die Null ist dort kein Freibrief, sondern ein blinder
Fleck. Wer F22/F23/F24/F25 terminiert, sollte wissen, dass Unknown Frequencies
diesen Stoff im Juli/August gerade abgeräumt hat — F23 ist mit 50 % das einzige,
was die Wortmethode davon überhaupt bemerkt.

## Vorbehalt

**Ein Treffer bei einem anderen Kanal sagt nichts darüber, ob dieselbe Frage bei
uns trägt.** Der blinde Test über 429 Videos hat gezeigt, dass kein
Themenmerkmal Views vorhersagt, und diese Erhebung widerspricht dem nicht — sie
wiederholt es an neuem Material: neun Titelmerkmale geprüft, keines hält der
Korrektur für Mehrfachtests stand; dasselbe Thema streut auf demselben Kanal um
den Faktor 282.

Dazu kommt, dass die Kanäle nicht vergleichbar sind. Ein 3×-Treffer bei Banana
Explains sind 12.000 Views, bei Ink Explainer 645.000. Die Faktoren stehen
nebeneinander in einer Tabelle, messen aber nicht dasselbe.

Was diese Auswertung leisten kann, ist enger: Sie sagt, **welche Titel in den
letzten 90 Tagen bereits vergeben sind** — und sie meldet mit F38 und F18 zwei
unserer Fragen, die inzwischen fast wörtlich bei einem anderen Kanal stehen.
Das ist ein Besetzungsbefund, kein Erfolgsbefund. Er ändert nichts an der
Terminierung der 42 Fragen; er ändert höchstens die Titelformulierung von F38
und F18.
