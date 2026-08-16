# Stichprobenlauf Video 2 — 16.08.2026

> **10 Credits** (5 Motive à 2,0). 5 von 5 technisch erfolgreich, 0 Fehlschläge.
> Kontostand vorher 2.639,9. **Der Hauptlauf ist nicht gestartet** — drei der
> fünf Bilder haben inhaltlich nicht bestanden.

## Was geprüft wurde

| Motiv | Warum in der Stichprobe |
|---|---|
| **M06** | Parallaxendreieck — das Grundbild des ganzen Videos |
| **M15** | ersetzt die Hyperbel *d = 1/p*; Ersatz muss ohne Achsen tragen |
| **M87** | sieben Fehlerbalken; trägt den wichtigsten Befund des Videos |
| **M52** | die Leiter — kehrt in **sieben** Motiven wieder (M52, M66, M67, M68, M84, M86, M91) |
| **M55** | einziges Weltbild; ohne eines lässt sich die Kanalfrage nicht prüfen |

## Ergebnis je Bild

### M87 — bestanden, ohne Einschränkung

Der Fall, um den ich am meisten besorgt war, ist der beste der Stichprobe.
Sieben Balken, kein Zeichen Text, keine Zahl. Die Symbole am linken Ende
funktionieren genau wie vorgesehen: die Fleckenscheibe oben, darunter drei
rote Riesensterne, unten drei pulsende Lampen — und die Trennlinie verläuft
**zwischen den Lampen und allem anderen**, nicht zwischen Scheibe und Leiter.
Das ist die Aussage des Skripts, rein grafisch getragen.

Einziger Mangel: die drei unteren Balken sind nicht an der gemeinsamen
senkrechten Linie ausgerichtet, sondern nach rechts abgesetzt. Behebbar.

### M06 — bestanden mit einem Fehler

Zwei Erden auf einer Bahn, die Sonne dazwischen, zwei gestrichelte Sichtlinien
zu einem Stern, der deutlich größer und heller ist als das Feld dahinter — die
Bedingung aus dem Motivkatalog ist erfüllt, und das Bild liest sich ohne ein
einziges Zeichen.

**Der Keil fehlt.** Statt eines Winkelmaßes an der Spitze kam ein gelber
Lichtstreifen entlang der linken Sichtlinie — der liest sich als Lichtstrahl,
nicht als gemessener Winkel. Genau das Element, das „du misst einen Winkel"
trägt, ist nicht da.

### M15 — durchgefallen, und der Fehler ist meiner

Im Bild steht **Text**: „WIDE" und „VERY SMALL", groß und in Versalien.

Die Wörter stammen aus meinem eigenen Prompt. Ich hatte im SCENE-Teil
`a WIDE double-headed arrow` und `a VERY SMALL double-headed arrow`
geschrieben — Versalien zur Betonung. Das Modell hat sie als Beschriftung
gelesen und ins Bild gesetzt, obwohl das Textverbot zweimal im Prompt steht.

**Die Lehre gilt für alle 52 Schemata:** Versalien gehören in den
Anweisungsteil des Prompts, nie in die Bildbeschreibung. Was in der
Szenenbeschreibung großgeschrieben neben einem zeichenbaren Ding steht, landet
als Schriftzug daneben. Der Rest des Bildes ist ebenfalls unbrauchbar — die
beiden Pfeile sitzen nicht an einer gemeinsamen Grundlinie, und im Hintergrund
liegen zwei bedeutungslose beige Kreisflächen.

### M52 — durchgefallen, und das ist der teuerste Befund

Die Leiter kam als **naturalistische Holzleiter in Perspektive**: runde
Sprossen mit Verlaufsschattierung, Holzmaserung, nach oben fluchtend und
ausgeblendet. Verlangt waren flache Füllung ohne Verlauf und keine Tiefe.
Dazu drei Sachfehler: die Sprossen werden nach oben **kürzer** statt länger,
das Dreieck am Fuß ist ein winziger roter Keil ohne Bezug zu M06, und der
Hintergrund ist ein fast schwarzes Sternfeld.

Das trifft nicht ein Bild, sondern **sieben** — die Leiter ist nach dem
Dreieck die zweite Schlüsselgrafik und trägt den ganzen Mittel- und
Schlussteil.

### M55 — Figur bestanden, Ausführung nicht

Gut: erwachsene Proportion, der Gesichtsbau der Serie (kleine Augen mit einer
dunklen Pupille, Brauen, minimale Nase, kurzer Mundstrich), Kleidung und
Frisur um 1910 richtig, Leuchttisch und Plattenstapel da. Keine
Portraitähnlichkeit — die Entscheidung für Epochenfiguren trägt.

Nicht gut: **weiche Verläufe** an Bluse, Lupe und Tischglühen, obwohl
`FLAT FILL, NO EXCEPTIONS` im Prompt steht. Und die **Lichtregel ist
ignoriert**: der Leuchttisch glüht zwar, beleuchtet aber ihr Gesicht nicht von
unten; die Figur ist konventionell von vorn ausgeleuchtet. Der Blick geht
außerdem an der Platte vorbei ins Bild statt darauf.

## Die Kanalfrage — gemessen

Der Verdacht war, dass Diagramm und Weltbild optisch auseinanderfallen. Das
tun sie, aber nicht dort, wo erwartet: **Machart, Konturstärke und Figurenbau
halten. Was auseinanderfällt, ist der Bildgrund.**

| | Helligkeit | dunkle Fläche |
|---|---:|---:|
| **Video 2, Stichprobe** | | |
| M52 Leiter | 32 | 90 % |
| M55 Leuchttisch | 69 | 56 % |
| M06 Dreieck | 72 | 3 % |
| M15 zwei Sterne | 215 | 0 % |
| M87 Fehlerbalken | 239 | 0 % |
| **Video 1, dieselbe Farbwelt, abgenommen** | | |
| M08 Moor | 90 | 36 % |
| M67 Anden | 116 | 3 % |
| M01 Haustür | 108 | 9 % |
| M45 Wüste | 117 | 12 % |
| M56 Babylon | 129 | 4 % |
| M76 Schema | 172 | 0 % |

Video 1 liegt in einem Band von 90 bis 172 — Weltbilder unten, das eine Schema
oben. Die Stichprobe streut von 32 bis 239, also über fast die ganze Skala.
Drei verschiedene Gründe in drei Diagrammen: dunkelblau (M06), fast weiß
(M87), fast schwarz (M52). Nebeneinander sieht das nach drei Sendungen aus,
nicht nach einer.

**Die Ursache ist das Thema.** Astronomie zieht jedes Diagramm auf schwarzen
Weltraumgrund, weil das die geläufige Bildkonvention ist. Video 1 hatte dieses
Problem nicht, weil Straßenquerschnitte keinen Nachthimmel nahelegen.

**Die Regel, die das löst:** Dunkelheit ist eine Eigenschaft eines Ortes bei
Nacht, nicht eines Diagramms. Schemata stehen ausnahmslos auf **einem** hellen
neutralen Grund — dem, auf dem M87 und Video 1s M76 schon stehen. Sterne
werden dort als dunkle Punkte auf hellem Grund gezeichnet, nicht als weiße auf
schwarzem; das ist die Konvention gedruckter Sternkarten und seit
Jahrhunderten lesbar. Nachtbilder der Welt (M01, M29, M79) dürfen dunkel
bleiben — Video 1 hatte solche auch.

## Was vor dem Hauptlauf zu ändern ist

1. **Versalien raus aus jedem SCENE-Text.** Betonung nur noch im
   Anweisungsteil.
2. **Ein einziger Schema-Grund**, hell und neutral, für alle 52 Schemata;
   schwarzer Weltraumgrund im Diagramm ausdrücklich verboten.
3. **Flachheit für Schemata schärfen** — die Leiter braucht den Satz, dass sie
   als flaches Sinnbild in Seitenansicht gezeichnet wird, ohne Fluchtpunkt,
   ohne Rundung, ohne Maserung.
4. **M06 braucht den Winkel als eigenes Element**, benannt als kleiner
   ausgefüllter Kreissektor an der Spitze zwischen den beiden Linien — nicht
   als „Keil" entlang einer Linie.
5. **M52 sachlich nachziehen**: Sprossen nach oben länger, das Dreieck am Fuß
   so groß und so gebaut wie in M06.
6. **Lichtregel bei Figuren nachschärfen** — „von unten" muss am Gesicht
   sichtbar werden, sonst ist die Quelle nur Dekoration.

Erst danach die verbleibenden 88 Motive.


---

# Zweiter und dritter Lauf — 16.08.2026

> Weitere **12 Credits** (6 + 4 + 2). Verbrauch der Stichprobe insgesamt
> **22 Credits** statt der angesagten 16 — die Mehrkosten sind dreimal M15,
> siehe unten. Ein technischer Fehlschlag (M15, zweiter Lauf), unter der
> Abbruchschwelle von drei.

## Die Grundregel wirkt, und zwar vollständig

| | erster Lauf | nach der Regel |
|---|---:|---:|
| M06 | 72 (3,1 % dunkel) | **240** (0,1 %) |
| M15 | 215 (0,2 %) | **233** (1,2 %) |
| M52 | 32 (90,0 %) | **232** (0,1 %) |
| M87 | 239 (0,4 %) | 239 (0,4 %) |

Vorher streuten die Schemata von 32 bis 239, also über fast die ganze Skala.
Jetzt liegen alle vier zwischen 232 und 240, mit höchstens 1,2 % dunkler
Fläche. Das ist ein geschlossener Satz — enger als das Band von Video 1
(90–172), und das ist richtig so, denn dort sind Weltbilder mitgezählt.

## Je Bild

**M06 — bestanden.** Der Winkel erscheint jetzt als das, was er ist: ein
gefüllter Kreissektor an der Spitze zwischen den beiden gestrichelten Linien,
das übliche Zeichen einer Geometriezeichnung. Kein Lichtstrahl mehr, kein
Leuchten. Sterne als dunkle Punkte auf Papiergrund, der nahe Stern deutlich
größer als das Feld. Ein Restfehler: die beiden Erdkugeln sitzen vorn und
hinten auf der Bahnellipse, während die Sichtlinien an deren seitlichen Enden
beginnen — die zwei Standpunkte sind also nicht dieselben Punkte wie die zwei
Erden. Die Aussage trägt trotzdem; im Hauptlauf mit einem Satz zu beheben.

**M52 — bestanden, im dritten Anlauf.** Der zweite Anlauf brachte den hellen
Grund und die Flachheit, aber die Sprossen blieben gleich lang und die Leiter
stand *neben* der Dreiecksspitze. Gelöst, indem die Leiter selbst zum Keil
wurde: die Holme laufen unten in einem Punkt zusammen und stehen Spitze auf
Spitze auf dem Dreieck. Damit ist beides zwangsläufig richtig — jede Sprosse
ist länger als die darunter, und der Fuß sitzt auf dem Dreieck aus M06.

**M15 — Bildidee sitzt, Ausführung nicht.** Der Textfehler ist weg. Die
Konstruktion mit Sichtlinien war das Problem: sie erzeugte ein Dreieck mit
drei Pfeilen, bei dem nicht zu sehen war, welcher Pfeil zu welchem Stern
gehört. Ersetzt durch die einfachere Fassung — jeder Stern zweimal an seinen
beiden scheinbaren Orten, Doppelpfeil dazwischen, links weit, rechts eng.
Diese Fassung ist ohne ein Zeichen lesbar.

**Aber das Modell zeichnet reproduzierbar ein Geisterbild dazu:** über der
sauberen Reihe steht eine zweite, verwaschene, halbtransparente Reihe
derselben Sterne. Zwei Versuche mit zwei verschieden formulierten Prompts,
zweimal derselbe Artefakt — auch mit ausdrücklichem `no ghosted or duplicated
copies` und `every shape is drawn exactly once`. Das ist kein Zufallsfehler.
Vermutlich löst die Anweisung, dasselbe Ding an zwei Orten zu zeigen, im
Modell eine Doppelbelichtung aus.

## Was daraus in die Regeln gewandert ist

Alles in `produktion/video-01/bildplan.py`, damit es für alle künftigen Videos
gilt und nicht nur für dieses:

- **`FARBEN_SCHEMA`** trägt jetzt die Grundregel: ein einziger heller
  neutraler Grund, nie schwarz, nie Nachthimmel, nie Weltraum — auch dann
  nicht, wenn das Diagramm vom Himmel handelt; Sterne als dunkle Punkte nach
  Art gedruckter Sternkarten.
- **`FARBEN_SCHEMA`** trägt ausserdem die Füllregel. Der dritte M52-Lauf kam
  als reine Strichzeichnung ohne Fläche zurück und fiel damit in die andere
  Richtung aus dem Satz. „Ink on paper" heißt nicht „nur Kontur".
- **`pruefe_szene()`** bricht ab, wenn ein Wort in der Bildbeschreibung in
  Versalien steht. Alle 84 Szenen aus Video 1 laufen sauber durch; der
  bekannte Fehlerfall `a WIDE arrow` wird gefangen.
- **`FRAMING_SITZEND`** für sitzende Einzelfiguren. In `szenenplan.py` sind
  M34, M55 und M69 als `sitzend=True` markiert.

## Offen

**M15.** Die Bildidee ist geprüft und trägt; das Geisterbild ist ein
Modellverhalten, das sich zweimal nicht wegformulieren ließ. Drei Wege, keiner
davon entschieden:

1. Im Hauptlauf mitlaufen lassen und beim Prüfdurchgang neu ziehen — der
   Artefakt könnte bei anderem Seed ausbleiben.
2. Die Bildidee ändern, sodass kein Ding zweimal vorkommt: statt zweier
   Positionen je Stern eine Strecke mit zwei Endmarken.
3. Das Motiv streichen und M06 die Aussage mittragen lassen.

**M06.** Erdkugeln an die Enden der Sichtlinien.
