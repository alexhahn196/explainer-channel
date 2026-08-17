# Video 2 — Abschlussbericht

> Stand 17.08.2026. Das Video ist fertig montiert und geprüft.
> **Nichts wurde zu YouTube hochgeladen.**

## Das Ergebnis

| | |
|---|---|
| Datei | `video-02.mp4`, **144,2 MB**, MD5 `0f8d29e369313381f084b17f72c4ff5b` |
| Laufzeit | **10:16,2** — 159 Einstellungen aus 66 Motiven |
| Bild | 1920×1080, 30 fps, H.264, mittlere Bitrate 1.799 kb/s |
| Ton | AAC 154 kb/s, 44,1 kHz, mono |
| Stimme | ElevenLabs **Eric** `cjVigY5qzO86Huf0OWal`, `eleven_multilingual_v2` |
| **Seed** | **4242** |
| `speed` | 1,1955 · stability 0,5 · similarity_boost 0,75 · style 0,0 |
| Gemessenes Tempo | **202,0 WPM** über die ganze Spur (2.071 Wörter) |
| TTS-Zeichen | **11.235** gesendet in 24 Absätzen (Grenze war 20.000) |
| Bilder | **66 von 66**, `nano_banana_2` → substituiert zu `nano_banana_flash`, 16:9, 2k |
| **Credits** | **222 von 500** |
| Schema-Anteil | **10,1 %** der Laufzeit (Schranke jetzt 12 %) |

Die Videodatei liegt **im Repository**, in vier Teilen unter
[`produktion/auslieferung/`](../auslieferung/) — zusammensetzen mit
`sh zusammensetzen.sh`, das Skript prüft die Prüfsumme.

Der erste Weg war ein Dateihoster, und er hat nicht getragen: der Link
`gofile.io/d/L5O1u46m` war **nach wenigen Stunden tot** („this content does not
exist"), obwohl GoFile beim Hochladen denselben MD5 zurückgemeldet hatte. Die
Übertragung war korrekt, die Aufbewahrung nicht. Ein Link, der verfällt, ist
keine Sicherung.

## Was geprüft wurde, und wie

| Prüfung | Ergebnis |
|---|---|
| Bild zu Schnittplan (53 Stichproben) | **53/53** treffen, 6 davon auf dem Zustandspartner |
| Verankerung am gesprochenen Wort | **159/159** Einstellungen, keine nicht gefunden |
| Versatz Ton gegen Bild | **0,24 s** |
| Dekodierlauf über die ganze Datei | fehlerfrei |
| Aussprache, 24 Stellen, zwei Erkenner | **0 Fehlformen**, 5 abweichend, 1 überhört — alle sechs per Dauermessung als Wort gesprochen |
| Serientöne über alle 66 Bilder | keine Ausreißer in fünf Farbgruppen und den Sternfeldern |
| Personenwörter in figurenlosen Prompts | 43 Prompts, 0 Treffer |
| Pflanzenwörter in vegetationsfreien Prompts | 53 Prompts, 0 Treffer |
| Risikovokabular in Szenentexten | 66 Prompts, 0 unfreigegebene Treffer |
| Versalien in Bildbeschreibungen | 66 Prompts, 0 Treffer |

Einzelheiten zur Aussprache in [`aussprache-qa.md`](aussprache-qa.md).

## Was in diesem Video anders gemacht wurde als in Video 1

**Die Erzählform.** Video 1 erklärte Vorgänge; Video 2 zeigt, was ein Mensch
dabei tat. Der Schema-Anteil fiel damit von 26 % auf 10,1 % — und das war
keine Sparmaßnahme, sondern die Folge: ein Vorgang, den jemand ausführt,
braucht kein Diagramm. Die verworfene Erklärfassung liegt als
`skript-erklaerform.md` daneben.

**Die Zustandspaare.** Neun Paare zeigen „dasselbe Bild, eine Sache anders".
Aus Text ist das nicht herstellbar — das Modell hat den ersten Zustand nie
gesehen. Sieben davon entstehen jetzt durch Rechnen (`zustandspaare.py`):
freistellen, Lücke schließen, denselben Pixelblock versetzt einsetzen. Beim
Daumenpaar bleiben Haken, Türrahmen und Wandfläche **zu 100,0 % bitgleich**.
Vier weitere, bei denen sich der Gegenstand selbst ändert, kommen über Bild zu
Bild — dort ist das Neuzeichnen ja der Inhalt.

**Die Steckbriefe.** 24 Motive tragen die Beschreibung eines Dings, das
mehrfach vorkommt: die Wohnstraße, drei Sternwarten, der Mauerquadrant, das
Okularfeld, der Mond, die Lupe, der Bleistift, die Kerze, ein Schreibtisch,
und der eine Mensch, der dreimal auftritt. Ohne sie liefen sie auseinander,
messbar: derselbe Mann kam mit drei Hauttönen zurück, dieselbe Sternwarte
einmal als roter Backsteinbau und einmal als cremefarbenes Häuschen.

## Was schiefging und was daraus zu lernen ist

### Eine Ursache, sieben Erscheinungsformen

Jeder Bildfehler dieses Videos ging auf **ein Wort im Prompt zurück, das etwas
benannte, was im Bild nicht sein sollte** — nie auf eine fehlende Anweisung im
Bildinhalt.

| Stelle | nannte | Schaden |
|---|---|---|
| Epochensatz | `Clothing, tools` | M01 kam mit zwei Personen in Kleidung um 1900 zurück, obwohl „no people in this picture at all" dastand |
| Farbsatz | `foliage and grass are green`, `The sky is blue` | M24 verlangte die Nahaufnahme eines Sterns und kam als Tageslandschaft: 60 % blauer Himmel, 22 % grün |
| Strichstärkenregel | `figures, clothing, props` | zweiter Auslöser für dieselben Figuren |
| Florazeile | `without leaves`, `als Silhouette` | belaubte Kronen, wo kahles Astwerk verlangt war — dreimal, in drei Ausbaustufen der Regel |
| Schema-Farbsatz | `timber the colour of that wood` | die Leiter als Holzleiter, obwohl sie ein Sinnbild ist |
| Szenentext | `a two-euro coin` | eine lesbare **2** und das Wort **EURO** auf der Münze, in zwei Motiven |
| Durchlichtblock | `the sheet` | zwei der fünf Motive zeigen eine Glasplatte, kein Blatt |

**Verneinen zählt als Nennen.** „no palms", „without leaves", „no wood grain"
schreiben Palme, Laub und Holz in den Prompt. **Beispielreihen sind
Inventarlisten:** „every surface — rock, stone blocks, earth, water" war als
Illustration einer Regel gemeint und wurde als Bestandsangabe gelesen.

### Und die Gegenrichtung: ein fehlender Satz ist so teuer wie ein falscher

Das war der zweite Befund, und er fällt beim Lesen des Prompts nicht auf —
dort steht ja nichts Falsches. Er fällt erst beim **Messen der Bilder** auf.

| Eigenschaft | gemessene Spanne, bevor sie festgelegt war |
|---|---|
| Sternfarbe | 0,0 % / 60,3 % / 81,2 % farbige Sternpunkte in drei Sternfeldern |
| Sterngröße | M29s Sterne fünfmal so groß wie M36s |
| Galaxienfarbe | weiß-blau gegen regenbogenfarben |
| Grundton dunkler Bilder | (0,0,0) reines Schwarz bis (48,48,60) |
| Papierton | neutral bis rosastichig bis gelblich |
| Metallton | dunkler Ocker bis leuchtendes Gold bis blasser Sand |
| Leuchttischfarbe | zwei warmcreme, einer cyan |
| wiederkehrende Figur | drei Hauttöne für einen Mann |

Beide Hälften der Regel stehen jetzt in `config.md`.

### Wo der Anweisungsteil der Szene widersprach

Zweimal verbot der Anweisungsteil, was die Szene verlangte. **M06** ist ein
Gesicht in Nahsicht, und derselbe Prompt sagte „no head, no face". **M43**
verlangt mehrere Frauen und einen Mann an der Tür, und derselbe Prompt sagte
„no second figure" — dort hat das Verbot gewonnen und eine einzige Frau
geliefert. Bei M03 und M27 hat das Modell dasselbe Verbot übergangen und die
Gruppe gezeichnet. **Welche Seite gewinnt, ist Zufall.**

### Wo das Messen das Auge schlug — und wo das Auge das Messen

**Für das Messen:** Bei M25 hatte ich behauptet, der Punkt sei gegenüber der
Scheibe verrutscht. Die Messung sagte dx = 0, dy = −9 — ich hatte die
Kontaktkopie falsch abgelesen.

**Gegen das Messen:** Die Prüfung `pruefe_video.py` meldete drei Fehlzuordnungen,
alle drei waren Messfehler. Das Farbhistogramm ist bei vierzehn Sternfeldern
blind — sie sind alle weiße Punkte auf demselben Tiefblau. Nach dem
Helligkeitsraster gemessen kam die richtige Zuordnung auf +0,763, die
gemeldete auf −0,026. Und Zustandspaare sind per Konstruktion nicht
unterscheidbar; wo der Paarpartner gewinnt, ist das Bild richtig und die
Zuordnung nur nicht entscheidbar.

**Der wichtigste Fall:** Die Aussprache-QA meldete `SEF-ee-id` als
abweichend — der Erkenner schrieb „SFEID", wie eine buchstabierte Abkürzung.
Bei acht Vorkommen des Kernbegriffs wäre das ein hörbarer Fehler durchs ganze
Video. Entschieden hat es die **Dauer**: 0,59 bis 0,88 s für drei Silben, wo
sieben benannte Buchstaben 1,5 bis 2 s bräuchten. Ein Fehlschlag des Erkenners
belegt keinen Aussprachefehler.

### Was mir bei der Buchführung durchfiel

**M40 und M69** waren bei der Stapelplanung nie erzeugt worden — aufgefallen
erst bei der Schlussmessung. Bei der Montage hätten sie den Lauf blockiert.
Und ich hatte die abgeleiteten Zustände zweimal falsch gezählt (sechs statt
neun). Beides sind Fehler in meiner Liste, nicht in der Arbeit.

## Der Schnitt sitzt am Wort, nicht am Rechenwert

**159 von 159 Einstellungen** sind am gesprochenen Wort verankert; bei Video 1
waren fünf nicht auffindbar. Der Plan rechnete mit 219 WPM und 9:20; die Stimme
liefert 202 WPM und 10:16. Die Differenz von 54,8 s verteilt sich dorthin, wo
tatsächlich länger gesprochen wird — nicht gleichmäßig.

Daraus folgen zwei Werte, die jetzt in `config.md` stehen:

* **Respellings kosten rund 5 % Tempo** (214,3 WPM im Stimmentest ohne, 205,3
  im Skript mit 24 Korrekturen), die Atempausen weitere 1,6 %.
* **Die Einstellungslänge 2,4–6,0 s ist ein Planungswert, kein
  Prüfkriterium.** 14 von 159 Einstellungen stehen über 6,0 s, die längste bei
  8,95 s. Geprüft wird nur die Untergrenze, und die nur mit Vorbild: alle 22
  Einstellungen unter 2,4 s haben ihr Motiv oder ihren Paarpartner daneben.

## Was offen bleibt

**Zweitebenen und Clips.** 16 Motive sind für getrennte Ebenen vorgesehen und
in der Szenenliste als solche geführt; Video 1 hatte sechs Clips. Beides ist
**bewusst nicht gemacht**: eine Fassung nur mit Standbildern und Kamerafahrten
zeigt erst, wo Bewegung wirklich fehlt. Die Entscheidung fällt am fertigen
Schnitt.

**Betonung und Vokalqualität** der Eigennamen sind mit dieser Methode nicht
prüfbar und werden nicht behauptet. Siehe `aussprache-qa.md`.

**Der Titel** ist nicht gegen Alternativen getestet; der Kanal hat keine
gemessene Titelregel.

**M63** ist das einzige Bild der Reihe mit starker Farbigkeit — ein
Fleckenmuster in Blau, Orange und Weiß. Das ist die Konvention für eine
Falschfarbenkarte der Hintergrundstrahlung und inhaltlich richtig, fällt aber
aus dem Farbklang der übrigen 65. Ob das trägt, entscheidet das Sehen.
