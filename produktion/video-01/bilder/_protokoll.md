# Prüfprotokoll Hauptlauf (Fortsetzung)

| Stapel | Motive | bestanden | durchgefallen |
|---|---|---|---|
| 1 | M02–M14 | 8/11 | M02, M09, M10 |
| 2 | M02, M09, M10, M15–M22 | 8/11 | M10, M16, M22 |
| 3 | M10, M16, M22, M23–M31 | **10/11** | M24 |

## Stapel 3 im Einzelnen

**Alle drei Nachläufe bestanden.** M10 zeigt die Marsch ohne Steg, ohne Hütte
und ohne Boot; M16 hat keine Buchstabenform mehr; M22 trägt nur noch ein
Signalobjekt. Der `KEIN_SIGNAL`-Zusatz wirkt in allen drei Fällen.

**Durchgefallen: M24** — verlangt ist der Blick *unter* die Wasseroberfläche
mit einer zweiten, älteren Bohlenlinie darunter. Geliefert ist eine Brücke von
der Seite über dem Wasser. Einzelfall, keine gemeinsame Ursache.

## Die Größenregel ist verstanden — M29 bestätigt die These

| Motiv | Vordergrund | Größenregel |
|---|---|---|
| **M08** | offene Moorfläche, keine Leitlinie | **greift** |
| M06 | Wasserlauf zieht diagonal durchs Bild | versagt |
| M62 | Straßenbett als Fluchtlinie zur Bildmitte | versagt |
| **M29** | **Grabungsschnitt als dominante Diagonale** | **versagt** |

**Befund für den Machart-Block künftiger Videos:** Die Größenangabe für eine
kleine Figur setzt sich nur durch, wenn das Bild keine dominante Leitlinie
enthält. Sobald eine Fluchtlinie, ein Weg oder ein Grabenrand durchs Bild
zieht, richtet das Modell die Figur daran aus und skaliert sie auf
Normalgröße — unabhängig davon, wie die Größenvorgabe formuliert ist (drei
Formulierungen geprüft: Bruchzahl, Beschreibung, Bildanteil).

**Konsequenz:** Wer eine kleine Figur braucht, muss den Bildaufbau ändern,
nicht den Prompt. Entweder die Leitlinie aus der Szene nehmen oder die
Figurengröße als gegeben hinnehmen.

## Stapel 6 — M47 (Nachlauf), M56–M61, M63–M66

**9 von 11 bestanden.** Verbrauch bis hier: 174 Credits von 500.

| Motiv | Befund |
|---|---|
| M47 | bestanden — die gehärtete Leerformel wirkt, keine Figur mehr |
| M57 | **durchgefallen** — soll Nacht sein, ist taghell. Der Kontrast zu M56 (Prozession am Tag) ist die Aussage des Paares; ohne ihn trägt die Stelle nicht |
| M64 | **durchgefallen** — drei türkise Objekte statt einem: Rasselstab, Wasserfläche, Grasbüschel |

Übrige acht ohne Beanstandung.

## Neuer, messbarer Prüfpunkt: die Signalfarbe

Bis hierher wurde Türkis nur nach Augenschein geprüft. `tuerkis.py` zählt es
jetzt: Farbabstand zu `#1BBFB0`, dann Zusammenhangskomponenten. Wichtig ist
die Dilatation vor dem Zählen — schwarze Konturlinien zerschneiden ein
einzelnes Objekt sonst in Teilstücke (das Reliefpanel in M57 zerfiel in zehn).

**Befund über alle 68 damals vorhandenen Bilder:** nur M64 verletzt die Regel
wirklich. Aber **zwölf Bilder tragen gar kein Türkis** — M01, M05, M08, M09,
M19, M20, M21, M26, M31, M34, M48, M84. Nächste Farbe zur Signalfarbe dort:
Grau im Abstand 118–133. Die Farbe fehlt also vollständig, sie ist nicht bloß
verschoben.

**Ursache, und sie liegt im Prompt, nicht am Modell.** Der SIGNAL-Block endet
mit: *„If no single object needs marking, the turquoise is absent from the
picture entirely."* Das ist ein ausdrücklicher Freibrief zum Weglassen. Das
Modell hat ihn genommen.

Die Anweisung lautete „genau ein türkises Objekt, nicht flächig" und zielte auf
**Übergebrauch**. Untergebrauch war nie festgelegt. Darum hier gemeldet und
nicht eigenmächtig nachgezogen — zwölf Neuläufe wären 24 Credits und ein
Eingriff in eine Stilfrage.

## Stapel 7 — M67–M71, M73–M78

**Abbruchschwelle erreicht. Der Bildlauf steht.**

| Motiv | Befund |
|---|---|
| M67 | **durchgefallen** — Saguaro-Kakteen in den Anden; dazu eine echte Bogenbrücke. Beides gehört nicht zu Inka-Peru |
| M69 | **durchgefallen** — weiche Verläufe und Schattierung statt flächiger Füllung, Konturstärke schwankt. Gegen den Kern des Machart-Blocks |
| M70 | **durchgefallen** — Saguaro und Opuntien in den Anden; die Szene verlangt drei Oberflächenabschnitte, geliefert ist ein Torbau |
| M71 | Grenzfall — die Route ist als Route kaum lesbar, milde Schattierung. Kein sauberer Fehlschlag |
| M77 | bestanden, trägt aber kein Türkis (siehe oben) |
| M78 | bestanden — die zeitlose Figurenfassung greift, Kleidung ohne Jahrhundert |

M68, M73, M74, M75, M76 ohne Beanstandung.

### Das Grundsätzliche daran

Die vier Beanstandungen sind **kein Zufall, sie sitzen alle im Anden-Block**.
M67–M71 sind die einzigen Motive dieses Stapels in Peru, und drei davon holen
sich nordamerikanische Wüstenflora. Der Prompt nennt Ort und Zeit („the Inca
empire in the Andes, around 1450 AD"), aber **keine Pflanzen** — und das Modell
füllt „Anden + trocken" mit dem, was es als Wüste kennt.

Das ist derselbe Mechanismus wie beim früheren Epochenfehler: was der Prompt
nicht benennt, rät das Modell aus der nächstliegenden Bildkonvention. Ein
Neulauf ohne benannte Flora holt sich denselben Fehler wieder.

### Was ein Neulauf bräuchte

1. Flora je Kulturraum benennen, nicht nur Ort und Zeit. Für die Anden:
   Puna-Gras, Polylepis, Agaven — **keine Säulenkakteen, keine Opuntien**.
2. Für Inka-Bauten den echten Bogen ausschließen; Inka mauern auskragend.
3. Den Flächenfüllungs-Satz für die Raumbilder verschärfen — M69 zeigt, dass
   er bei komplexem Gelände nachgibt.

### Messversuch, der nichts taugte

Ich habe versucht, die Stilabweichung zu messen statt zu behaupten: Anteil
exakt einfarbiger 3×3-Umgebungen, dann die Verteilung des lokalen Gradienten.
Beides trennt nicht. Die erste Kennzahl liegt bei **jedem** Bild bei 0 %, weil
der Generator ein schwaches Rauschen über alle Flächen legt. Die zweite misst
Szenendichte statt Schattierung: M12, längst angenommen, liegt bei 23,3 %
höher als das beanstandete M69 mit 18,1 %.

**Die Stilprüfung bleibt damit Augenschein.** Belastbar ist der Vergleich
zweier Ausschnitte bei gleicher Vergrößerung — M69 gegen M63 zeigt den
Unterschied eindeutig. Anders als bei der Signalfarbe gibt es hier keine Zahl,
die ich verantworten könnte.
