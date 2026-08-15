# Offener Stand des Bildlaufs

**Erzeugt: 79 von 84.** Verbraucht: **196 Credits** von der Grenze 500.

Der Lauf steht an der vereinbarten Abbruchschwelle (mehr als drei Fehlschläge
in einem Stapel). Er wird **nicht** von allein fortgesetzt.

## Noch nie erzeugt (5)

M79 M80 M81 M82 M83

## Erzeugt, aber durchgefallen (5)

| Motiv | Grund | Vorschlag |
|---|---|---|
| M57 | soll Nacht sein, ist taghell — der Tag/Nacht-Kontrast zu M56 ist die Aussage des Paares | Szenentext ist bereits verschärft (`bildplan.py`), nur noch neu erzeugen |
| M64 | drei türkise Objekte statt einem | Träger benannt (`SIGNAL_TRAEGER`), nur noch neu erzeugen |
| M67 | Saguaro-Kakteen in den Anden, dazu eine echte Bogenbrücke | braucht die Flora-Regel, siehe unten |
| M69 | weiche Verläufe statt flächiger Füllung, schwankende Konturstärke | braucht schärfere Flächenregel |
| M70 | Saguaro und Opuntien in den Anden; Szene verlangt drei Oberflächenabschnitte, geliefert ist ein Torbau | braucht die Flora-Regel |

M71 ist ein Grenzfall (Route kaum als Route lesbar) und zählt hier nicht als
Fehlschlag.

## Der gemeinsame Nenner der Anden-Fehler

M67–M71 sind die einzigen Peru-Motive des Stapels, und drei davon holen sich
nordamerikanische Wüstenflora. Der Prompt nennt Ort und Zeit, aber **keine
Pflanzen** — und was der Prompt nicht benennt, rät das Modell aus der
nächstliegenden Bildkonvention. Genau derselbe Mechanismus wie beim früheren
Epochenfehler.

**Ein Neulauf ohne benannte Flora holt sich denselben Fehler wieder.** Nötig:

1. Flora je Kulturraum benennen. Anden: Puna-Gras, Polylepis, Agaven —
   ausdrücklich **keine Säulenkakteen, keine Opuntien**.
2. Für Inka-Bauten den echten Bogen ausschließen (Inka mauern auskragend).
3. Den Flächenfüllungs-Satz für Raumbilder verschärfen.

Das sind drei Eingriffe in `bildplan.py`, die **alle 84 Prompts** berühren —
darum liegen sie beim Auftraggeber und nicht bei mir.

## Kosten eines vollständigen Nachlaufs

10 Bilder (5 fehlende + 5 durchgefallene) = **20 Credits**, Endstand 216 von
500. Käme die Flora-Regel und würde man die übrigen Peru-Motive vorsorglich
mitziehen, wären es 6 weitere = 12 Credits.

## Neu und nutzbar: die Signalfarbe ist jetzt messbar

`tuerkis.py` zählt zusammenhängende Türkisflächen statt sie zu schätzen.
Wichtig ist die Dilatation vor dem Zählen — schwarze Konturlinien zerschneiden
ein einzelnes Objekt sonst in Teilstücke.

Befund über alle 79 Bilder: **nur M64 verletzt die Regel.** Aber **zwölf Bilder
tragen gar kein Türkis** (M01, M05, M08, M09, M19, M20, M21, M26, M31, M34,
M48, M84, dazu M77). Ursache ist ein Satz, den ich selbst in den SIGNAL-Block
geschrieben hatte: *„If no single object needs marking, the turquoise is absent
from the picture entirely."* Ein ausdrücklicher Freibrief zum Weglassen.

Die Anweisung lautete „genau ein türkises Objekt" und zielte auf Übergebrauch;
Untergebrauch war nie festgelegt. **Offene Entscheidung**, keine Eigenmacht:
Freibrief streichen und die dreizehn Bilder nachziehen (26 Credits) — oder so
lassen.

## Zwei Generatorfehler nebenbei behoben

- Zeitlose Motive mit Figur (M41, M78) verwiesen auf eine Epochenzeile, die es
  dort gar nicht gibt („dressed for the period named above" — es stand keine
  da). Neu: `FIGUR_ZEITLOS` beschreibt Kleidung ohne Jahrhundert. M78 zeigt,
  dass es greift; M41 lag schon fertig auf der Platte und wurde nicht ersetzt.
- M64 bekommt über `SIGNAL_TRAEGER` einen benannten Signalträger.

## So geht es weiter

`python3 bildplan.py` schreibt `bildplan.json`; daraus je Motiv das Feld
`prompt` an `generate_image_batch` (nano_banana_2, 16:9, 2k, 2,0 Credits je
Bild), Stapel zu höchstens 11.

Prüfliste je Bild: Figur vorhanden wo vorgesehen · Brauen · Kopf etwa ⅕ ·
genau eine Lichtquelle beziehungsweise gerichteter harter Schatten · keine
verformten Hände · kein Text · nicht angeschnitten · **genau ein türkises
Objekt** (jetzt messbar) · **Flora und Bauweise passen zum Kulturraum** (neu,
aus dem Anden-Befund).
