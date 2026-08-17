# Wirkt ein Anlass?

> Erhebung 2026-08-17. **0 Credits, keine Videosichtung, keine Transkripte.**
>
> Der Terminplan in [`recherche/themen-erklaerkanal.md`](../recherche/themen-erklaerkanal.md)
> steht auf der Annahme, dass ein Anlass — Kinostart, Jubiläum, Raumsonde —
> Suchanfragen erzeugt, von denen das Video profitiert, **auch wenn der Titel
> den Anlass nicht nennt**. Die Datei sagt über ihre eigene Annahme: *„Ob ein
> Anlass tatsächlich Suchvolumen erzeugt, wurde nicht geprüft — die
> Wirkungsannahme stützt sich allein auf das Shadow-of-the-Gods-Muster
> (n = 1 Kanal)."*
>
> **Antwort in zwei Sätzen: Die Annahme zerfällt in zwei Behauptungen. Die
> prüfbare (B1) fällt an ihrem eigenen einzigen Beleg durch; die tragende (B2)
> ist aus öffentlichen Daten nicht entscheidbar — und zwar aus einem Grund, der
> sich nicht durch bessere Daten beheben lässt.**

Nachrechenbar mit [`regeln/daten/anlass_kodierung.py`](daten/anlass_kodierung.py)
über [`recherche/daten/shadow_of_the_gods.json`](../recherche/daten/shadow_of_the_gods.json)
und [`regeln/daten/themen_korpus.tsv`](daten/themen_korpus.tsv). Methode
wortgleich aus `themen_test.py`: kanalintern, Median mit Merkmal gegen Median
ohne, ein Kanal zählt nur bei ≥ 3 Videos je Gruppe, Zufallstest durch Mischen
der Views **innerhalb** des Kanals, 10.000 Runden, Seed 20260817.

---

# B1 — „Anlassnennung im Titel wirkt"

## Die Kodierregel, vorab festgelegt

Der Auftragstext fasst unter „Anlass" zusammen: *Marke, Film, Regisseur,
Studio, laufende Produktion*. Das sind zwei verschiedene Dinge, und sie werden
deshalb **getrennt** gerechnet:

| Stufe | Regel |
|---|---|
| **A — Anlass im engen Sinn** | Der Titel nennt eine zum Uploadzeitpunkt **laufende oder unmittelbar bevorstehende** fremde Produktion oder deren Urheber. Nur das entspricht dem Anlassbegriff der Themendatei, wo ein Anlass ein datierbares Ereignis ist. |
| **B — Fremdmarke im weiten Sinn** | Der Titel nennt **irgendeine** fremde Marke, ein Studio, eine Franchise oder eine IP-Figur — unabhängig davon, ob dazu gerade etwas erscheint. |

Grenzfälle, wie entschieden:

| Fall | A | B | Begründung |
|---|:-:|:-:|---|
| „Nolan" | ✅ | ✅ | Regisseur der Odyssee-Verfilmung, Kinostart 17.07.2026 — zum Uploadzeitpunkt laufend |
| „Hollywood" | ❌ | ✅ | Branchenbegriff, keine datierbare Produktion; bei diesem Kanal eine Floskel |
| „Marvel", „Disney" | ❌ | ✅ | Kein benannter aktueller Film; Bezug sind Filme von 1997 bzw. 2017 |
| „Percy Jackson" | ❌ | ✅ | Serie lief 2026, aber der Titel nennt keinen Termin. Konservativ als A-nein geführt; Gegenrechnung unten |
| „the Odyssey" ohne Nolan | ❌ | ❌ | Bezeichnet das antike Epos. Sonst wäre jeder Stoffname eine Anlassnennung |
| Goku, Beerus, Gojo, Kratos | ❌ | ✅ | Franchise ohne benannten Termin |

**Diese Kodierung ist nicht blind** [Offenlegung]. Die Abrufzahlen lagen beim
Kodieren vor — sie kamen mit demselben API-Aufruf. Das ist der Unterschied zu
[`themenwahl-test.md`](themenwahl-test.md), dessen Klassifikation nachweislich
vor dem View-Join entstand (Commit `8ae6ad0`). Der Befund hier ist entsprechend
**schwächer zu gewichten**. Als Gegenmaßnahme ist die Regel rein lexikalisch —
eine Wortliste im Skript, für alle 38 bzw. 429 Titel gleich angewandt, nicht
je Titel nach Gefühl entschieden.

## Shadow of the Gods, 38 Videos [gemessen]

`UC7OMVRiJcIqoIHoC4u7lIsw`, 13.800 Abonnenten, Stand 2026-08-17. Die API meldet
`videosCount` 31; die Vereinigung von Vorwärts- und Rückwärtsliste ergibt **38**.
Gerechnet ist mit den 38 gefundenen.

### Stufe A — die Behauptung, auf der der Terminplan steht

**Nicht auswertbar.** Das Merkmal trifft auf **2 von 38 Titeln** zu:

| Datum | Views | Titel |
|---|---:|---|
| 2026-07-17 | 227.000 | The Odyssey Nolan Won't Show You |
| 2026-07-27 | 18.000 | The Agamemnon Nolan Won't Show You |

Zwei Videos reichen für keinen Median-Vergleich (Schwelle: 3 je Gruppe). Das
ist der zentrale Befund dieses Abschnitts: **Der einzige Beleg der ganzen
Liste kann die Behauptung, die auf ihn gestützt wird, selbst nicht tragen.**

Die Gegenrechnung mit „Percy Jackson" als Stufe A ergibt drei Videos —
16.000, 18.000 und 227.000 Views — und damit:

| | Median | Faktor |
|---|---:|---:|
| Stufe A erweitert (3 Videos) | 18.000 | **1,29×** |
| Rest (35 Videos) | 14.000 | |

**1,29× aus drei Videos, von denen eines das drittbeste des Kanals ist.** Das
ist keine Wirkung, das ist ein Median aus drei Zahlen.

### Stufe B — jede Fremdmarke

Hier ist das Merkmal häufig: **28 von 38 Titeln**.

| Lauf | Faktor | n mit / ohne | p |
|---|---:|---|---:|
| alle 38 Videos | **3,31×** | 28 / 10 | 0,041 |
| nur älter als 90 Tage | 2,26× | 17 / 4 | 0,446 |
| ohne bestes Video je Gruppe | 3,33× | 27 / 9 | 0,046 |

Die **Ausreißerprüfung besteht der Befund** — anders als der
`selbsterfahren`-Befund in `themenwahl-test.md`, der genau daran zerbrach.
Gestrichen wurden „The Real Achilles Hollywood Was Too Afraid to Show You"
(439.000) und „Apollo Wasn't the Sun God" (15.000); der Faktor bleibt bei 3,33×.

**Trotzdem trägt er nicht, aus drei Gründen:**

**1. Die Alterskontrolle bricht ihn.** Über 90 Tage fällt der Faktor auf 2,26×
bei p = 0,446 — und die Vergleichsgruppe besteht dann aus **vier** Videos. Das
ist dieselbe Struktur, die in `themenwahl-test.md` als „kein Effekt, sondern
eine Beschreibung von zwei Ausreißern" verworfen wurde.

**2. Ein Kanal ist kein Richtungstest.** `themenwahl-test.md` verlangt
Konsistenz über Kanäle; auswertbar ist hier **genau ein** Kanal. Damit hat B1
dieselbe Schwäche wie `benanntes_raetsel` dort: *„nur ein auswertbarer Kanal,
und das ist der Kanal, aus dem das Merkmal stammt. Zirkulär."*

**3. Das Merkmal misst vermutlich etwas anderes.** Die zehn Titel **ohne**
Fremdmarke sind:

| Views | Titel |
|---:|---|
| 15.000 | Apollo Wasn't the Sun God — He Was Something Far Darker |
| 12.000 | From Mortal… to God's Scribe — The Origin of Metatron |
| 9.300 | What Happened to Odysseus After the Odyssey? |
| 9.200 | Azazel: The Fallen Angel Who Taught Humanity to Kill |
| 7.300 | Thor and Loki Were Never Brothers |
| 6.000 | Valhalla Was Never the Viking Paradise |
| 4.800 | The Dark Truth Behind Rome's Founding |
| 4.600 | Midas Turned His Daughter Into Gold...This Is Why. |
| 4.500 | The Minotaur Wasn't Born a Monster. They Lied to You. |
| 1.500 | Anubis: The Judge of Souls |

Metatron, Azazel, Midas, Anubis, Valhalla — das sind die **weniger bekannten
Figuren**. Die Marken-Gruppe koppelt dagegen fast durchweg eine Mythenfigur an
einen Anker, den der Zuschauer schon kennt. Der Vergleich lautet damit eher
**„bekannte gegen unbekannte Figur"** als „mit gegen ohne Anlass".

**Dazu eine Datumsschieflage:** Median-Uploaddatum der Marken-Gruppe
2026-05-17, der Vergleichsgruppe 2026-06-17. Die Marken-Gruppe ist im Mittel
einen Monat älter und hatte länger Zeit, Views zu sammeln. Ein Teil der 3,31×
ist Alter, nicht Merkmal — wie viel, ist **[unbekannt]**.

## Dasselbe Merkmal über den 429-Video-Korpus

| Stufe | Titel mit Merkmal | auswertbar |
|---|---:|---|
| A | **0 von 429** | nein |
| B | **1 von 429** | nein |

Der eine Treffer: *„The Disturbing Extinct Disney Iceberg Explained"* (quack
doc, 36.135 Views).

Das ist selbst ein Befund, und er stützt eine Beobachtung, die in
`themen-erklaerkanal.md` bereits steht: *„die anderen fünf fahren ausschließlich
zeitlose Alltagsfragen ohne Anlassbezug."* **Neun Kanäle mit 429 Videos, und
die Anlassnennung kommt praktisch nicht vor.** Die Bauform ist eine Eigenart
von Shadow of the Gods, keine Praxis der Nische.

## Urteil B1

**Die prüfbare Hälfte der Annahme ist nicht bestätigt.**

- **Stufe A** — die Behauptung, die der Terminplan braucht — ist **an ihrem
  einzigen Beleg nicht prüfbar** (2 von 38 Titeln) und liefert in der
  großzügigsten Auslegung 1,29× aus drei Videos.
- **Stufe B** zeigt 3,31×, hält der Ausreißerprüfung stand, **fällt aber bei
  der Alterskontrolle** (2,26×, p = 0,446), beruht auf einem einzigen Kanal und
  misst plausibler die Bekanntheit der Figur als den Anlass.
- Über 429 Videos aus neun Kanälen ist das Merkmal **nicht vorhanden**.

Nach den Maßstäben, die sich `themenwahl-test.md` selbst gesetzt hat —
Richtungskonsistenz über Kanäle, Ausreißerprüfung, Alterskontrolle,
Blindkodierung — besteht B1 **keinen** davon vollständig und zwei davon
gar nicht.

---

# B2 — „Der Anlass wirkt auch ohne Nennung im Titel"

Das ist die Behauptung, auf der der Terminplan tatsächlich steht: alle 47
Titel sind bewusst **zeitlos formuliert, ohne Anlassnennung**. B1 sagt über sie
nichts aus.

## Warum die Datumsauflösung nicht der Blocker ist

Die Themendatei vermutet, die gerundeten `publishDate`-Werte machten den Test
unmöglich. Das stimmt für die NexLev-Daten, aber nicht für den Korpus
[gemessen]:

| Datumsgüte | Videos |
|---|---:|
| gemessen (exakt) | **312** |
| abgeleitet | 64 |
| nur relativ | 53 |

312 exakt datierte Videos mit 31 verschiedenen Monatstagen — das reicht für
eine ±7-Tage-Auflösung. **Der Blocker liegt woanders.**

## Warum der Test trotzdem keine Aussage liefern kann

Ein solcher Test braucht eine **Vergleichsgruppe**: Videos, die *nicht* in der
Nähe eines passenden Ereignisses erschienen sind. Diese Gruppe existiert
praktisch nicht. Der Kalender in `themen-erklaerkanal.md` führt **22 belegte
Ereignisse pro Jahr**. Anteil aller Kalendertage, die dann innerhalb eines
Fensters um mindestens eines dieser Ereignisse liegen [abgeleitet]:

| Fenster | Anteil aller Tage „anlassnah" |
|---|---:|
| ± 7 Tage | 57,7 % |
| ± 14 Tage | 82,7 % |
| ± 30 Tage | **98,1 %** |

Bei dem Vorlauf, mit dem der Terminplan selbst arbeitet — V7 liegt 25 Tage vor
dem Anlass, V3 fünf Wochen davor — sind praktisch **alle** Videos anlassnah.
Wer den Kalender enger fasst, verliert die Fälle, die der Plan gerade nutzen
will; wer ihn weiter fasst, hat keine Nullgruppe mehr.

Dazu kommt der eigentliche Kern: **man sieht einem Titel nicht an, ob sein
Thema wegen eines Ereignisses gewählt wurde.** Ein Video über Wüstenwasser im
Dezember 2026 kann eine Dune-Kopplung sein oder ein Zufall. Diese Information
existiert nur beim Urheber.

## Urteil B2

**Nicht entscheidbar aus öffentlichen Daten** — und zwar nicht wegen der
Datenqualität, sondern weil der Test keine Nullgruppe hat und die
Absichtsinformation außerhalb der Daten liegt. Bessere Datumsangaben ändern
daran nichts.

Ein Ersatzmaß wird hier **nicht** gebildet. Ein Befund aus einem Test ohne
Vergleichsgruppe wäre keine schwache Evidenz, sondern gar keine.

## Testdesign für den eigenen Kanal — und was es kostet

Messbar ist B2 nur dort, wo die Absicht bekannt ist: **am eigenen Kanal**, wo
für jedes Video feststeht, ob es an einen Anlass gekoppelt wurde.

**Aufbau:** Videos abwechselnd mit und ohne Anlasskopplung veröffentlichen,
Zuordnung vor der Themenwahl festgelegt und schriftlich fixiert. Vergleichswert
ist der Median der Views nach einer festen Standzeit — **90 Tage nach
Veröffentlichung**, für alle gleich, damit das Alter herausfällt. Auswertung
kanalintern, wie in `themenwahl-test.md`.

**Wie viele Videos das braucht.** Die Streuung innerhalb eines Kanals ist der
begrenzende Faktor. Über die neun Korpuskanäle gemessen [gemessen]:

| Kanal | n | sd(log Views) | entspricht |
|---|---:|---:|---|
| Historically | 21 | 0,60 | 1,8× je Standardabweichung |
| Mapped History | 26 | 1,35 | 3,9× |
| History Mapped Out | 134 | 1,40 | 4,0× |
| quack doc | 126 | 1,45 | 4,3× |
| Folks of Yore | 21 | 1,72 | 5,6× |
| Ink Explainer | 13 | 1,74 | 5,7× |
| First Humans | 50 | 1,88 | 6,5× |
| Professor Historian | 24 | 1,93 | 6,9× |
| Axen | 14 | 2,49 | 12,1× |

Median **sd = 1,72**. Damit die Trennschärfe, Mann-Whitney zweiseitig,
α = 0,05, 3.000–4.000 Simulationen je Zelle [abgeleitet]:

| Videos je Gruppe | gesamt | Dauer bei 1 Video/14 Tage | Effekt ab 80 % Trennschärfe |
|---:|---:|---|---:|
| 10 | 20 | 0,8 Jahre | **erst ab 10,3×** |
| 15 | 30 | 1,2 Jahre | erst ab 6,6× |
| 25 | 50 | 1,9 Jahre | erst ab 4,2× |
| 40 | 80 | **3,1 Jahre** | erst ab 3,1× |

**Realistische Einschätzung: der Test ist bei dieser Kadenz nicht zu machen.**
Eine Stichprobe von zehn je Gruppe — knapp zehn Monate Produktion — findet
einen Effekt erst, wenn er den Median **verzehnfacht**. Ein Anlasseffekt dieser
Größe wäre in den Fremdkanaldaten längst aufgefallen; dort ist er nicht.
Für die Größenordnung, um die es realistisch geht (1,5× bis 3×), bräuchte es
drei Jahre und achtzig Videos.

**Was daraus folgt:** Wer B2 beantwortet haben will, bevor der Kalender darauf
gebaut wird, wird nicht bedient. Die Frage ist mit den verfügbaren Mitteln
weder von außen noch von innen in vertretbarer Zeit zu klären. Das ist ein
Ergebnis, kein Zwischenstand.

---

# Was offen bleibt

- **B1 Stufe B ist nicht sauber getestet, sondern nur nicht widerlegt.** Ein
  Kanal, nicht blind kodiert, mit Datumsschieflage. Sauber wäre: dasselbe
  Merkmal an einem Satz **anlassnennender** Kanäle prüfen, die bei der
  Definition keine Rolle gespielt haben — davon liegt keiner im Repo.
- **Die Trennung zwischen „Fremdmarke" und „bekannte Figur" ist nicht
  gemessen**, nur plausibel gemacht. Sie ließe sich prüfen, indem man die
  Bekanntheit der Mythenfigur unabhängig kodiert und beide Merkmale
  gegeneinander stellt. Bei 38 Videos in einem Kanal wird das nicht tragen.
- **Der Alterseffekt bei Shadow of the Gods ist [unbekannt].** Die
  Datumswerte sind dort auf Monatsraster gerundet (fünf Bündel auf dem 17.),
  eine feinere Alterskorrektur ist damit nicht möglich.
- **Die eigene Kanalstreuung ist [unbekannt].** Die sd = 1,72 stammt aus
  fremden Kanälen. Der eigene Kanal hat noch kein Video und kein Konto.
- **Ob ein Anlass Suchvolumen erzeugt, ist damit weiterhin ungeprüft** — nur
  ist jetzt gezeigt, dass die vorhandenen Daten es nicht klären können, statt
  dass es niemand versucht hätte.
