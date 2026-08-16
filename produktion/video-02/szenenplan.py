#!/usr/bin/env python3
"""Erzeugt die Szenentabelle fuer Video 2 aus dem Sprechtext.

Warum generiert und nicht getippt
---------------------------------
Bei Video 1 war die Szenenliste von Hand geschrieben, und drei Fehler fielen
erst beim Bildlauf auf: fehlende Epochenzeile, fehlende Lichtquelle, ein
Framing-Fall zu wenig. Hier steht jedes Motiv als Datensatz mit PFLICHTFELDERN
— fehlt eines, bricht das Skript ab, bevor eine Zeile Markdown entsteht.

Die Einstellungen sind ueber ihren VOLLEN Wortlaut definiert. Das Skript
prueft, dass die Aneinanderreihung aller Einstellungen exakt den Sprechtext
ergibt — kein Wort doppelt, keines verloren.
"""
from __future__ import annotations

import json
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
WPM = 219
KURZ_AB = 2.4   # darunter nur mit Vorbild (gleiches Motiv oder Paarpartner)
LANG_AB = 6.0   # darueber steht das Bild zu lange

# Namen, die im Skript vorkommen und deren Traeger im Bild erscheinen. Sie
# duerfen in keinem Bildtext stehen — siehe Pruefung in main().
PERSONEN = ("Kopernikus", "Copernicus", "Tycho", "Brahe", "Bessel",
            "Henderson", "Struve", "Piazzi", "Leavitt", "Henrietta",
            "Hertzsprung", "Hubble", "Baade", "Sandage", "Freedman",
            "Riess")

# ---------------------------------------------------------------- Motive ----
# Pflichtfelder je Motiv:
#   szene   Bildbeschreibung (der SCENE-Teil des Prompts)
#   licht   "sichtbar: <Quelle>" ODER "Schatten: <Richtung>" ODER "Schema"
#   ort     Epoche und Ort — auch bei figurenlosen Motiven
#   framing "ganz" | "ohne" | "teil"   (teil = Koerperteil-Nahaufnahme)
#   flora   Pflanzen/Bauweise, wo orts- oder epochengebunden; "—" wenn keine
# Optional: schema=True, ebenen=True, paar="<Partnermotiv>", schutz="<Name des Moments>",
#           diagramm="D<n>: <was ohne Beschriftung zu sehen ist>"
M: dict[str, dict] = {}


def m(mid, szene, licht, ort, framing, flora="—", **kw):
    M[mid] = dict(szene=szene, licht=licht, ort=ort, framing=framing,
                  flora=flora, **kw)


# --- Absatz 1: die Leere, dann die Antwort -----------------------------------
m("M01", "Aufsicht von unten in einen Nachthimmel voller Sterne, einer davon "
         "etwas heller als die übrigen; unten im Bild die dunkle Silhouette "
         "einer Dachkante", "sichtbar: die Sterne selbst, sonst nichts",
  "Gegenwart, eine Wohnstraße bei Nacht", "ohne", ebenen=True)
m("M02", "Dieselbe Person von hinten, klein, den Kopf in den Nacken gelegt, "
         "vor dem Sternhimmel; um sie herum nichts als leerer Raum",
  "sichtbar: die Sterne", "Gegenwart, dieselbe Straße", "ganz",
  schutz="Die Klammer — erstes und letztes Bild", ebenen=True)
# M02 kehrt am Schluss wieder — als identisches Bild, nicht als zweites
# Motiv. Die Klammer traegt nur, wenn der Ausschnitt derselbe ist; ein
# nachgebautes Gegenstueck waere sichtbar ein anderes Bild.
m("M03", "Vier gleich große Figurenumrisse nebeneinander; über JEDER stehen "
         "eine Sonne und ein Stern übereinander. Bei dreien hängt die Sonne "
         "tiefer, bei der vierten hängt der Stern tiefer", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-A: Ohne Beschriftung lesbar, weil der Abstand selbst die "
           "Aussage ist. Wichtig: beide Himmelskörper müssen über JEDER "
           "Figur stehen — bekäme die vierte nur den Stern und die anderen "
           "nur die Sonne, gäbe es nichts zu vergleichen und die eine "
           "Abweichung wäre unsichtbar.")
m("M04", "Sechs Figurenumrisse in einer Reihe, über jedem eine leere "
         "Gedankenblase; fünf Blasen sind völlig leer, in der sechsten "
         "stehen ein Stern und eine kurze Maßlinie darunter", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-B: Fünf leere Blasen, eine gefüllte. Leer = keine Antwort, "
           "Stern mit Maßlinie = eine Entfernung genannt. Ohne Text "
           "verständlich, und die Fünf-zu-Eins ist abzählbar.")
m("M05", "Ein Raster aus hundert gleichen Punkten, drei davon deutlich "
         "dunkler und größer", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, diagramm="D-C: Drei von hundert, rein durch Abzählbarkeit.")
m("M06", "Das Parallaxendreieck: die Erdbahn als flache Ellipse, die Erde an "
         "zwei gegenüberliegenden Punkten, von beiden je eine lange gestrichelte "
         "Sichtlinie zu einem nahen Stern; der Winkel zwischen den Linien als "
         "schmaler Keil; dahinter ein Feld ferner Sterne", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True, schutz="Die Antwort: das Dreieck",
  diagramm="D1 — DAS Grundbild. Ohne Beschriftung lesbar, weil zwei "
           "Standpunkte, zwei Linien und ein Keil die ganze Aussage sind. "
           "Keine Winkelmaße, keine Achsen, keine Buchstaben nötig. "
           "BEDINGUNG: der nahe Stern muss deutlich größer und heller "
           "sein als das Feld dahinter. Geht er darin unter, scheint "
           "der Keil an einem Hintergrundstern zu sitzen, und das Bild "
           "zeigt die falsche Messung.")
m("M07", "Eine Raumsonde und eine Radarschüssel nebeneinander, beide von "
         "einem breiten diagonalen Balken durchgestrichen", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-D: Durchstrichener Gegenstand — die geläufigste "
           "Verneinungsgeste, ohne Text eindeutig.")
# Kein M08: der Daumen steht von der ersten Einstellung an vor der Wand mit
# dem Bildhaken. Ein Vorbild ohne Haken haette den Bezugspunkt erst
# eingefuehrt, wenn er schon gebraucht wird — der Sprung waere gegen nichts
# gemessen.

# --- Absatz 2: der Daumen-Trick ----------------------------------------------
m("M09", "Derselbe Daumen vor derselben Wand, der Daumen sitzt links von "
         "einem Bildhaken an der Wand", "Schatten: hart von links",
  "Gegenwart, dasselbe Zimmer", "teil", paar="M10")
m("M10", "Exakt dieselbe Aufnahme, aber der Daumen sitzt jetzt rechts vom "
         "Bildhaken — Bildausschnitt und Kameraposition identisch",
  "Schatten: hart von links", "Gegenwart, dasselbe Zimmer", "teil", paar="M09")
m("M11", "Zwei Augen im Profil, von jedem geht eine Linie zu einem nahen "
         "Gegenstand und weiter auf eine Rückwand; die beiden Treffpunkte auf "
         "der Wand liegen auseinander", "Schema", "zeitlos, reine Zeichnung",
  "ohne", schema=True,
  diagramm="D2: Zwei Augen, zwei Linien, zwei Treffpunkte. Der Versatz ist "
           "die Aussage und braucht keine Beschriftung.")
m("M12", "Die Sonne in der Mitte, die Erdbahn als Ellipse darum, die Erde "
         "einmal links und einmal rechts auf der Bahn; zwischen den beiden "
         "Erden eine gerade Verbindungslinie quer durch die Bahn", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-E: Zwei Erden auf einer Bahn, eine Strecke dazwischen. Die "
           "Länge trägt die Stimme, nicht das Bild.")
m("M13", "Ein rechteckiger Bildausschnitt des Sternhimmels, ein Stern darin "
         "links von zwei Hintergrundsternen", "sichtbar: die Sterne",
  "zeitlos, Blick ins All", "ohne", paar="M14")
m("M14", "Derselbe Ausschnitt, derselbe Himmel — nur der eine Stern sitzt "
         "jetzt rechts von den beiden Hintergrundsternen",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne", paar="M13")
m("M15", "Zwei Sterne über einer gemeinsamen Grundlinie: der nahe mit einem "
         "weiten Doppelpfeil-Versatz, der ferne mit einem winzigen; die "
         "Sichtlinien laufen jeweils zu denselben zwei Standpunkten", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D4 ERSETZT: Statt der Hyperbel d = 1/p zwei nebeneinander "
           "gestellte Fälle. Eine Kurve ohne Achsenbeschriftung wäre "
           "bedeutungslos — zwei Sterne mit großem und kleinem Versatz sind "
           "ohne ein einziges Zeichen verständlich.")

# --- Absatz 3: 295 Jahre -----------------------------------------------------
m("M16", "Ein waagerechter Zeitstrahl, ganz links ein Markierungsstrich, ganz "
         "rechts ein zweiter, dazwischen eine sehr lange leere Strecke",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-F: Die Leere zwischen zwei Marken IST die Aussage. Ohne "
           "Jahreszahlen lesbar; die Zahl trägt die Stimme.")

# --- Absatz 4: Kopernikus und Tycho ------------------------------------------
m("M17", "Ein Mann in Talar und Barett des 16. Jahrhunderts beugt sich über "
         "einen Tisch, auf dem eine Armillarsphäre steht; er schiebt eine "
         "kleine Kugel von der Mitte an den Rand",
  "sichtbar: eine Kerze auf dem Tisch",
  "Frauenburg im Ermland, 1543", "ganz", person=True,
  flora="Innenraum, keine Vegetation; spätgotische Fensternische, "
        "Holzbalkendecke", ebenen=True)
m("M18", "Derselbe Sternhimmel zweimal übereinander im selben Bild, die obere "
         "Hälfte gegen die untere deutlich seitlich versetzt, dazwischen ein "
         "schmaler Zwischenraum", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, paar="M18b",
  diagramm="D-G: Zwei Himmel, gegeneinander verschoben — die erwartete "
           "Schwankung. Ohne Text verständlich, weil der Versatz selbst der "
           "Inhalt ist.")
m("M18b", "Exakt dasselbe Bild, derselbe Ausschnitt, dieselben zwei Himmel — "
          "nur liegt jeder Stern der oberen Hälfte jetzt genau über seinem "
          "Gegenstück in der unteren, ohne jeden Versatz",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M18",
  diagramm="D-Gb: Zustand B. Das AUSBLEIBEN der Schwankung ist der Inhalt "
           "des Satzes und lässt sich nur als zweiter Zustand zeigen — auf "
           "dem Bild der erwarteten Schwankung stehenzubleiben, während die "
           "Stimme sagt, dass niemand eine sah, hätte das Gegenteil "
           "behauptet.")
m("M19", "Ein bärtiger Mann in Wams und Halskrause steht an einem großen "
         "Mauerquadranten aus Messing, dem Auge an der Visiereinrichtung; "
         "kein Fernrohr im Bild",
  "sichtbar: der Nachthimmel durch eine offene Dachluke",
  "Uraniborg auf der Insel Ven, um 1580", "ganz", person=True,
  flora="Innenraum einer Sternwarte, Backsteinnischen, keine Vegetation",
  ebenen=True)
m("M20", "Dieselbe Visiereinrichtung in Nahaufnahme, die Skala daneben, der "
         "Zeiger steht exakt auf einem Teilstrich und rührt sich nicht",
  "Schatten: hart von oben rechts",
  "Uraniborg auf der Insel Ven, um 1580", "teil")
m("M21", "Ein Ringplanet auf halber Bildhöhe, davon nach rechts eine "
         "gestrichelte Strecke; ganz rechts, weit dahinter, ein einzelner "
         "Stern — die Strecke dazwischen vielfach länger", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-H: Zwei Abstände im Größenverhältnis. Der Faktor trägt die "
           "Stimme; das Bild zeigt nur, dass der zweite ungleich größer ist.")
m("M22", "Extreme Nahaufnahme eines einzelnen Sterns, wie ihn ein bloßes Auge "
         "sieht: eine kleine runde Scheibe mit weichem Rand",
  "sichtbar: der Stern selbst", "zeitlos, Blick zum Nachthimmel", "ohne",
  paar="M25")
m("M23", "Größenvergleich nebeneinander: links eine kleine Sonne, rechts eine "
         "Kugel, die ein Vielfaches davon misst und über den Bildrand hinaus "
         "angedeutet ist", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-I: Zwei Kreise im Größenverhältnis, der größere angeschnitten. "
           "Ohne Beschriftung lesbar.")
m("M24", "Derselbe Mann an seinem Quadranten wendet sich ab; im Hintergrund "
         "eine ruhende Erdkugel auf einem Sockel",
  "sichtbar: eine Öllampe an der Wand",
  "Uraniborg auf der Insel Ven, um 1580", "ganz", person=True,
  flora="Innenraum, keine Vegetation")
m("M25", "Dieselbe Nahaufnahme desselben Sterns, aber die Scheibe ist "
         "verschwunden: ein winziger harter Punkt, umgeben von einem feinen "
         "Ring aus Beugungslicht", "sichtbar: der Stern selbst",
  "zeitlos, Blick zum Nachthimmel", "ohne", paar="M22")
m("M26", "Zwei Kreisflächen nebeneinander, die linke groß, die rechte ein "
         "kaum sichtbarer Punkt", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D6: Der Größenunterschied allein. Der Faktor tausend ist im Bild "
           "nicht abzählbar — die Stimme nennt ihn, das Bild zeigt nur, dass "
           "es sehr viel weniger ist.")
m("M27", "Ein Fernrohr auf einem Holzstativ, daneben mehrere Männer in "
         "Perücken und Rockschößen, die sich über eine Zeichnung beugen",
  "sichtbar: ein Fenster mit Tageslicht",
  "eine europäische Sternwarte, um 1700", "ganz",
  flora="Innenraum, Stuckdecke, keine Vegetation")

# --- Absatz 5: der Wettlauf --------------------------------------------------
m("M28", "Eine flache Landkarte Europas mit drei markierten Punkten weit "
         "auseinander, von jedem geht eine dünne Linie nach oben zu je einem "
         "eigenen Stern", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-J: Drei Orte, drei Sterne, drei Linien. Ohne Ortsnamen "
           "verständlich, weil die Dreizahl die Aussage ist.")

# --- Absatz 6: Bessel --------------------------------------------------------
m("M29", "Ein klassizistisches Sternwartengebäude mit Kuppel bei Nacht, "
         "davor kahle Bäume und eine gepflasterte Straße",
  "sichtbar: der Mond über der Kuppel",
  "Königsberg in Ostpreußen, 1838", "ohne",
  flora="norddeutsche Stadtbäume ohne Laub — Linden und Kastanien; "
        "Backstein und Putz, keine Palmen, keine Nadelbäume", ebenen=True)
m("M30", "Nahaufnahme einer runden Objektivlinse, die exakt durch die Mitte "
         "durchgesägt ist; die eine Hälfte sitzt fest, die andere ist auf "
         "einer feinen Gewindeschraube seitlich verschoben",
  "Schatten: hart von rechts", "Königsberg in Ostpreußen, 1838", "teil")
m("M31", "Blick durch ein Okular: zwei getrennte Sternabbilder nebeneinander "
         "im runden Gesichtsfeld", "sichtbar: die Sterne im Gesichtsfeld",
  "Königsberg in Ostpreußen, 1838", "ohne", paar="M32")
m("M32", "Dasselbe runde Gesichtsfeld, dieselbe Lage — die beiden "
         "Sternabbilder liegen jetzt genau übereinander und bilden einen Punkt",
  "sichtbar: die Sterne im Gesichtsfeld",
  "Königsberg in Ostpreußen, 1838", "ohne", paar="M31")
m("M33", "Ein Sternfeld, in dem ein unscheinbarer Doppelstern durch eine "
         "kurze Spur markiert ist, die seinen Weg gegenüber den Nachbarn zeigt",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne")
m("M34", "Ein Mann in hochgeschlossenem Rock des frühen 19. Jahrhunderts "
         "sitzt am Okular eines großen Refraktors und dreht mit der rechten "
         "Hand eine Mikrometerschraube",
  "sichtbar: eine abgeschirmte Öllampe neben dem Instrument",
  "Königsberg in Ostpreußen, 1838", "ganz", person=True,
  flora="Innenraum einer Kuppel, Holzdielen, keine Vegetation", ebenen=True)
m("M35", "Ein Kreissektor, aus dem ein einzelner haarfeiner Ausschnitt "
         "herausgehoben und daneben stark vergrößert gezeigt wird", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D3a: Ein Tortenstück und seine Lupe. Dass es 3.600 Teile sind, "
           "sagt die Stimme — das Bild zeigt nur, wie dünn eines davon ist.")
m("M36", "Eine Münze im Vordergrund und dieselbe Münze am fernen Ende einer "
         "schnurgeraden Landstraße, dort nur noch ein Pünktchen", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D3b: Dasselbe Ding nah und fern. Die Entfernung trägt die "
           "Stimme; das Bild zeigt die Schrumpfung.")
m("M37", "Ein Lichtstrahl als lange durchgehende Linie zwischen zwei Sternen, "
         "an der Linie eine einzelne Kerbe kurz hinter dem Startpunkt",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-K: Eine Strecke mit einer einzigen Kerbe nahe dem Anfang — "
           "ein Jahr gegen die ganze Reise. Ohne Text lesbar.")
m("M38", "Zwei senkrechte Balken nebeneinander auf gemeinsamer Grundlinie, "
         "der rechte etwa ein Zehntel höher als der linke", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-L: Zwei Balken, geringer Höhenunterschied. Genau das ist die "
           "Aussage — Bessel lag knapp daneben.")

# --- Absatz 7: Henderson und Struve ------------------------------------------
m("M39", "Ein weißes Sternwartengebäude mit flachem Dach auf einem "
         "Hügelrücken, dahinter ein Tafelberg und offenes Meer",
  "sichtbar: die tief stehende Sonne über dem Meer",
  "Royal Observatory am Kap der Guten Hoffnung, 1833", "ohne",
  flora="Fynbos des Kaps — silbriges Buschwerk, Proteen, niedrige "
        "Hartlaubsträucher; ausdrücklich keine Palmen, keine Akazien, "
        "keine Wüstenpflanzen", ebenen=True)
m("M40", "Nahaufnahme: eine Hand legt ein beschriebenes Blatt in eine "
         "Schreibtischschublade und schiebt sie zu; kein Gesicht im Bild",
  "Schatten: hart von links", "Kapstadt, 1833", "teil")
m("M41", "Ein niedriges verputztes Observatorium mit Holzverschalung in einer "
         "winterlichen Landschaft, davor eine Schlittenspur im Schnee",
  "sichtbar: der Mond hinter dünnen Wolken",
  "Dorpat im Baltikum, 1837", "ohne",
  flora="baltische Winterlandschaft — Birken und Kiefern ohne Laub, "
        "Schneedecke; keine Laubbäume in Blatt", ebenen=True)
m("M42", "Zwei sehr kurze waagerechte Striche übereinander, fast gleich lang, "
         "der Unterschied kaum auszumachen", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M43",
  diagramm="D-M: Zwei fast gleiche Längen. Dass sie fast gleich sind, IST "
           "die Aussage — kein Zahlenwert nötig.")
m("M43", "Dasselbe Bild, dieselbe Anordnung — nur der obere Strich ist jetzt "
         "auf die doppelte Länge gewachsen und ragt weit über den unteren "
         "hinaus", "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  paar="M42",
  diagramm="D-N: Zustand B zu M42. Der Sprung ist ohne Beschriftung "
           "unmittelbar sichtbar.")
m("M44", "Drei gleich große Rahmen nebeneinander, in jedem eine "
         "Figurensilhouette; über allen dreien schwebt derselbe Siegerkranz, "
         "keiner ist hervorgehoben", "Schema", "zeitlos, reine Zeichnung",
  "ohne", schema=True,
  diagramm="D-O: Drei gleichrangige Rahmen, ein Kranz über allen. Zeigt "
           "'kein eindeutiger Erster' ohne ein einziges Wort.")

# --- Absatz 8: die Grenze der Geometrie --------------------------------------
m("M45", "Ein weites Sternfeld mit vielen hundert Punkten; nur etwa sechzig "
         "davon tragen einen kleinen Ring", "sichtbar: die Sterne",
  "zeitlos, Blick ins All", "ohne")
m("M46", "Ein Satellit mit aufgeklapptem Sonnensegel über der gekrümmten "
         "Erdkante, im Hintergrund Sterne",
  "Schatten: hart von rechts, scharfe Licht-Schatten-Kante am Rumpf und am Sonnensegel; die Sonne selbst bleibt außerhalb des Bildes",
  "Erdumlaufbahn, um 1990", "ohne", ebenen=True)
m("M47", "Sechs gleiche Punkte in einer Reihe, einer davon von einem engen "
         "Ring umschlossen, die anderen fünf von weiten, unscharfen Ringen",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-P: Enger Ring = sicher, weiter Ring = unsicher. Die "
           "Ringgröße als Fehlerbalken, ohne Achse und ohne Zahl.")
m("M48", "Ein kompakterer Satellit mit zylindrischem Sonnenschild vor dem "
         "schwarzen All, weit von der Erde entfernt",
  "Schatten: hart von links, scharfe Kante am Sonnenschild; die Sonne selbst bleibt außerhalb des Bildes",
  "Lagrangepunkt hinter der Erde, 2015", "ohne", ebenen=True)
m("M49", "Eine Münze im Vordergrund, dahinter der Mond, und weit dahinter "
         "noch einmal dieselbe Münze als kaum sichtbarer Punkt", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D3c: Die Münze zum dritten Mal, jetzt mit dem Mond als "
           "Zwischenmarke. Der Mond ist das einzige Maß, das jeder kennt.")
m("M50", "Aufsicht auf eine Spiralgalaxie, die die ganze Bildbreite "
         "einnimmt; in einem äußeren Arm ein einzelner heller Punkt, um ihn "
         "herum eine schwach ausgeleuchtete Scheibe, die nur einen kleinen "
         "Teil der Galaxie bedeckt", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-Q: Eine kleine ausgeleuchtete Scheibe in einer großen "
           "Galaxie. Das Größenverhältnis ist die ganze Aussage und braucht "
           "keine Zahl.")
m("M51", "Ein scharfer, klar begrenzter Punkt auf der einen Bildseite und ein "
         "verwaschener, ausgefranster Fleck auf der anderen; der Versatz "
         "zwischen zwei Lagen des Flecks verschwindet in seiner eigenen "
         "Unschärfe", "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-R: Scharf gegen unscharf, und der Versatz kleiner als die "
           "Unschärfe. Der Kernsatz des Absatzes, rein bildlich.")

# --- Absatz 9: die Leiter ----------------------------------------------------
m("M52", "Eine Leiter, die schräg in einen Sternhimmel hinaufführt; die "
         "unterste Sprosse steht auf einem kleinen Dreieck, die Sprossen "
         "darüber werden nach oben hin länger", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True, schutz="Die Leiter, zum ersten Mal",
  diagramm="D10 — die zweite Schlüsselgrafik. Ohne Beschriftung lesbar: "
           "eine Leiter steht auf dem Dreieck von M06. Die Rückbindung an "
           "das Grundbild ist die ganze Aussage.")
m("M53", "Nahaufnahme zweier Hände über einer großen Glasplatte auf einem "
         "Leuchttisch; die eine Hand hält eine Lupe, die andere notiert mit "
         "einem Bleistift; kein Gesicht im Bild",
  "sichtbar: der Leuchttisch von unten",
  "Harvard College Observatory, Massachusetts, um 1910", "teil")

# --- Absatz 10: Leavitt ------------------------------------------------------
m("M54", "Ein langer heller Arbeitsraum, an mehreren Tischen sitzen Frauen in "
         "hochgeschlossenen Blusen und langen Röcken über Glasplatten gebeugt; "
         "an der Tür ein Mann im Anzug, der einen Plattenkasten hereinreicht",
  "sichtbar: hohe Sprossenfenster auf der linken Seite",
  "Harvard College Observatory, Massachusetts, 1908 bis 1912", "ganz",
  flora="Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation",
  ebenen=True)
m("M55", "Eine Frau in dunkler Bluse sitzt allein am Leuchttisch, den Blick "
         "auf die Platte gesenkt, eine Lupe in der Hand; um sie herum Stapel "
         "weiterer Platten",
  "sichtbar: der Leuchttisch von unten",
  "Harvard College Observatory, Massachusetts, um 1910", "ganz", person=True,
  flora="Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation",
  ebenen=True)
m("M56", "Eine unregelmäßige Sternwolke, deutlich abgesetzt vom umgebenden "
         "Himmel, mit einem dichten Kern und ausgefransten Rändern",
  "sichtbar: die Wolke selbst", "zeitlos, Blick ins All", "ohne", ebenen=True)
m("M57", "Ein einzelner Stern in einem Sternfeld, groß und hell",
  "sichtbar: der Stern selbst", "zeitlos, Blick ins All", "ohne", paar="M58")
m("M58", "Dasselbe Sternfeld, derselbe Ausschnitt — der eine Stern ist auf "
         "einen kleinen matten Punkt zusammengefallen",
  "sichtbar: der Stern selbst", "zeitlos, Blick ins All", "ohne", paar="M57")
m("M59", "Ein Feld aus Punkten, die sich sichtbar entlang zweier paralleler "
         "gerader Linien anordnen; die Linien steigen beide von links unten "
         "nach rechts oben", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, paar="M62",
  diagramm="D8 — Leavitts eigene Abbildung. Ohne Achsenbeschriftung "
           "verständlich, weil die Botschaft die AUSRICHTUNG ist: Punkte "
           "fallen auf Geraden, also gibt es eine Regel. Was auf den Achsen "
           "steht, sagt die Stimme.")
m("M60", "Zwei gleiche Lampen, die linke nah und grell, die rechte weit weg "
         "und schwach; von beiden geht dieselbe Anzahl Strahlen aus", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-S: Gleiche Lampe, unterschiedlich hell, weil unterschiedlich "
           "weit. Die Strahlenzahl macht die Gleichheit sichtbar — ohne Text.")
m("M61", "Eine Reihe derselben Lampe, von links nach rechts immer kleiner und "
         "matter, darunter eine Maßleiste, deren Abstände nach rechts "
         "zunehmen", "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-T: Abnehmende Helligkeit gegen zunehmende Strecke. Die "
           "Übersetzung Helligkeit → Entfernung, rein grafisch.")

# --- Absatz 11: der fehlende Nullpunkt ---------------------------------------
m("M62", "Dasselbe Punktfeld mit denselben zwei Geraden wie zuvor — aber die "
         "senkrechte Achse ist ein blanker Strich ohne einen einzigen "
         "Teilstrich", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, paar="M59", schutz="Der fehlende Nullpunkt",
  diagramm="D9 — der fehlende Nullpunkt. **Genau hier ist die Textlosigkeit "
           "ein Vorteil**: eine Achse ohne Teilung ist ohne Beschriftung "
           "verständlicher als mit. Zustand B zu M59, identischer Ausschnitt.")
m("M63", "Dreizehn Sterne über eine Fläche verstreut, von jedem geht ein "
         "kurzer Pfeil aus; die Pfeile zeigen in verschiedene Richtungen, "
         "aber ein dicker Sammelpfeil in der Mitte fasst sie zu einer "
         "gemeinsamen Richtung zusammen", "Schema", "zeitlos, reine Zeichnung",
  "ohne", schema=True,
  diagramm="D-U: Dreizehn Einzelpfeile, ein Mittelwertpfeil. Zeigt das "
           "Poolen ohne ein einziges Wort — und dass es ein Mittel ist, "
           "keine Einzelmessung.")

# --- Absatz 12: Unterschrift und Nobelbrief ----------------------------------
m("M64", "Nahaufnahme eines Schriftstücks, auf dem unten rechts eine große "
         "geschwungene Unterschrift steht und oben links eine viel kleinere; "
         "die Schrift ist als reines Liniengekritzel angedeutet, keine "
         "lesbaren Buchstaben", "Schatten: hart von links oben",
  "Harvard College Observatory, 1912", "teil")
m("M65", "Ein leerer Schreibtisch am Fenster, darauf ein ungeöffneter "
         "Briefumschlag; der Stuhl davor ist leer und leicht zurückgeschoben",
  "sichtbar: das Fenster mit fahlem Tageslicht",
  "Harvard, Massachusetts, 1925", "ohne", ebenen=True,
  flora="Innenraum; was durch das Fenster zu sehen ist, sind kahle "
        "Laubbäume Neuenglands — keine Palmen, keine immergrünen Hecken")

# --- Absatz 13: Sprosse auf Sprosse ------------------------------------------
m("M66", "Dieselbe Leiter wie zuvor, jetzt von der Seite: jede Sprosse ruht "
         "sichtbar auf zwei Streben, die von der Sprosse darunter aufsteigen",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D10b: Die Leiter im Konstruktionsschnitt. Dass jede Sprosse auf "
           "der vorigen ruht, ist rein baulich sichtbar.")
m("M67", "Dieselbe Leiter, an der untersten Sprosse ein kleiner Riss; "
         "derselbe Riss wiederholt sich an jeder Sprosse darüber, nach oben "
         "hin immer breiter", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D11: Ein Riss, der sich nach oben verbreitert. "
           "Fehlerfortpflanzung ohne Formel und ohne Text.")

# --- Absatz 14: der Bruch ----------------------------------------------------
m("M68", "Dieselbe Leiter, zwei Sprossen sind durchgebrochen und hängen "
         "schief herab", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, schutz="Die gebrochenen Sprossen",
  diagramm="D-V: Gebrochene Sprossen. Die Wiedererkennung derselben Leiter "
           "trägt den Beat; ohne Text eindeutig.")

# --- Absatz 15: erster Bruch -------------------------------------------------
m("M69", "Ein Mann in Tweedjacke sitzt am Okular "
         "eines sehr großen Spiegelteleskops in einer Kuppel",
  "sichtbar: der Nachthimmel durch den offenen Kuppelspalt",
  "Mount-Wilson-Observatorium, Kalifornien, 1929", "ganz", person=True,
  flora="Innenraum einer Kuppel, Stahlfachwerk, keine Vegetation", ebenen=True)
m("M70", "Ein Feld kleiner Spiralgalaxien, von einem gemeinsamen Mittelpunkt "
         "nach außen strebend; die äußeren tragen längere Bewegungsspuren als "
         "die inneren", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-W: Längere Spur = schneller. Die Zunahme nach außen ist ohne "
           "Beschriftung ablesbar.")
m("M71", "Dasselbe Galaxienfeld, aber alle Bewegungsspuren zeigen nach innen, "
         "und die Galaxien sind auf einen dichten Punkt zusammengelaufen",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-X: Der Film rückwärts. Zusammenlaufen statt auseinander — "
           "ohne Text als Umkehrung lesbar.")
m("M72", "Zwei senkrechte Balken nebeneinander, fast exakt gleich hoch; der "
         "linke trägt oben ein kleines Sternsymbol, der rechte eine kleine "
         "Erdkugel", "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  paar="M73",
  diagramm="D13 KORRIGIERT: 1929 waren beide Balken fast gleich hoch — das "
           "ist der historisch richtige Stand, nicht der oft gezeigte "
           "Faktor-2-Widerspruch. Die Symbole ersetzen die Beschriftung.")
m("M73", "Dieselben zwei Balken, dieselbe Anordnung — der rechte mit der "
         "Erdkugel ist jetzt deutlich höher als der linke mit dem Stern",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M72",
  diagramm="D13b: Zustand B. Die Erde überragt das Universum — der Widerspruch "
           "wird rein durch Balkenhöhe erzählt.")
m("M74", "Ein Punktfeld, durch das zunächst eine einzige Gerade läuft; im "
         "selben Bild spaltet sie sich nach rechts in zwei getrennte Geraden "
         "auf, jede mit ihrer eigenen Punktgruppe", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D12: Aus einer Geraden werden zwei. Direkter Rückgriff auf M59 — "
           "dieselbe Bildsprache, jetzt verdoppelt.")
m("M75", "Ein Saal mit Reihenbestuhlung, vorn ein Mann am Rednerpult vor einer "
         "hellen Projektionsfläche, die Zuhörer beugen sich vor",
  "sichtbar: der Projektionsstrahl von hinten",
  "Rom, Tagung der Internationalen Astronomischen Union, 1952", "ganz", person=True,
  flora="Innenraum, Marmorpilaster und hohe Fenster, keine Vegetation",
  ebenen=True)
m("M76", "Eine Kugel mit Sternen darin, daneben dieselbe Kugel im doppelten "
         "Durchmesser", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-Y: Zwei Kugeln, klares Größenverhältnis. Verdopplung ohne Text.")
m("M77", "Nahaufnahme einer Fotoplatte: an einer Stelle ein einzelner scharfer "
         "Punkt, direkt daneben ein Fleck, der bei näherem Hinsehen aus vielen "
         "dicht gedrängten Punkten und diffusem Leuchten besteht",
  "Durchlicht: die Platte wird von hinten durchleuchtet, die Quelle liegt hinter ihr und ist nicht im Bild",
  "Kalifornien, 1958", "teil")
m("M78", "Links eine kleine Kugel, rechts dieselbe Kugel weit größer; quer "
         "über den Durchmesser der großen liegen sieben Abdrücke der kleinen "
         "in einer Reihe, die ihn genau ausfüllen",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-Z: Der Faktor sieben als abzählbare Kette quer durch die "
           "große Kugel. Eine Reihe von sieben WACHSENDEN Kugeln wäre die "
           "naheliegende Lösung und wäre falsch gelesen worden — sie zeigt "
           "sieben Schritte, nicht das Verhältnis sieben zu eins. Hier ist "
           "abzählbar, was die Stimme sagt.")

# --- Absatz 16: zweiter Bruch ------------------------------------------------
m("M79", "Ein kleiner dichter Sternhaufen aus wenigen hellen Sternen, von "
         "zartem Nebel umgeben, am Nachthimmel über einer Baumsilhouette",
  "sichtbar: die Sterne des Haufens",
  "Gegenwart, Blick vom Boden", "ohne",
  flora="mitteleuropäische Laubbäume als Silhouette", ebenen=True)
m("M80", "Ein Maßstab, an dem zwei Zeiger sitzen: der linke deutlich weiter "
         "unten als der rechte; zwischen beiden eine auffällige Lücke",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M81",
  diagramm="D-AA: Zwei Zeiger, eine Lücke. Der Abstand ist die Aussage.")
m("M81", "Derselbe Maßstab, dieselben zwei Zeiger — der linke ist jetzt zum "
         "rechten hinaufgewandert, beide stehen dicht beieinander", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M80",
  diagramm="D-AB: Zustand B. Die Lücke ist geschlossen, der Satellit hat "
           "nachgegeben.")
m("M82", "Mehrere große Parabolantennen auf freiem Feld, alle in dieselbe "
         "Richtung geneigt", "Schatten: hart von rechts, lange Schatten "
         "über den Boden", "Gegenwart, ein Antennenfeld im Hochland des "
  "amerikanischen Südwestens", "ohne",
  flora="trockenes Steppengras, niedrige Beifußbüsche, ferne kahle "
        "Bergrücken; keine Bäume, keine Kakteen", ebenen=True)

# --- Absatz 17: der offene Streit --------------------------------------------
m("M83", "Ein feinkörniges Fleckenmuster über die ganze Bildfläche, dahinter "
         "ein kleiner Satellit im Profil", "sichtbar: das Muster leuchtet "
         "selbst", "Lagrangepunkt, 2013", "ohne", ebenen=True)
m("M84", "Dieselbe Leiter wie zuvor, jetzt mit drei deutlich abgesetzten "
         "Sprossen: unten ein Dreieck, in der Mitte eine pulsende Lampe, oben "
         "ein aufplatzender Stern", "Schema", "zeitlos, reine Zeichnung",
  "ohne", schema=True,
  diagramm="D10c: Die Leiter mit ihren drei Stufen als Symbolen. Jedes "
           "Symbol wurde vorher eingeführt — deshalb ohne Text lesbar.")
m("M85", "Zwei waagerechte Fehlerbalken übereinander auf gemeinsamer Achse, "
         "deren Enden sich nicht berühren; zwischen ihnen eine klare Lücke. "
         "Am linken Ende des oberen sitzt eine feinfleckige Scheibe, am "
         "linken Ende des unteren eine kleine Leiter",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-AC: Zwei Balken, die sich nicht überlappen. Die Lücke IST die "
           "Signifikanz — ohne Sigma-Zeichen und ohne Zahl. Die beiden "
           "Symbole sagen ohne ein Wort, wessen Balken welcher ist, und "
           "bereiten die Symbolschrift von M87 vor.")
m("M86", "Dieselbe Leiter, aber die mittlere Sprosse ist gegen eine andere "
         "ausgetauscht: statt der pulsenden Lampe sitzt dort ein großer "
         "roter Stern", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-AD: Dieselbe Leiter, eine andere Sprosse. Der Austausch ist "
           "der Kern des Streits und rein bildlich zu zeigen.")
m("M87", "Sieben waagerechte Fehlerbalken untereinander auf einer gemeinsamen "
         "senkrechten Achse. Am linken Ende jedes Balkens sitzt ein kleines "
         "Symbol: beim obersten eine feinfleckige Scheibe, bei drei weiteren "
         "ein großer roter Stern, bei den unteren drei eine pulsende Lampe. "
         "Die Balken mit Scheibe und rotem Stern überlappen sich; die drei "
         "mit der Lampe liegen weiter rechts und berühren die obere Gruppe "
         "nicht", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, schutz="Die sieben Fehlerbalken",
  diagramm="D14 — der wichtigste Befund des Videos als Bild, und der "
           "schwierigste Fall der ganzen Liste. Sieben unbeschriftete Balken "
           "allein zeigen ZWEI HAUFEN — und damit genau das Früh-gegen-Spät-"
           "Bild, das das Skript ausdrücklich verwirft. Ohne Beschriftung "
           "richtig lesbar wird es erst durch die Symbole am Balkenende: die "
           "Fleckenscheibe (aus M83), der rote Riesenstern (aus M86) und die "
           "pulsende Lampe (aus M84) sind alle vorher eingeführt. Dann liest "
           "das Auge, was die Aussage ist: die Trennlinie läuft NICHT "
           "zwischen Scheibe und Leiter, sondern zwischen den beiden "
           "Leitersprossen — der rote Stern steht bei der Scheibe, nicht bei "
           "der Lampe. Ohne diese Symbole ist das Diagramm nicht bloß "
           "unverständlich, sondern irreführend.")
m("M88", "Zwei Galaxien nebeneinander, von beiden geht je eine Messlinie zu "
         "einem gemeinsamen Nullpunkt; die beiden Linien sind praktisch gleich "
         "lang", "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D-AE: Zwei gleich lange Messlinien. Zeigt die Übereinstimmung, "
           "die dem Streit widerspricht.")
m("M89", "Eine solide Leiter, die fest steht — und an ihrem Fuß zwei Hände, "
         "die um einen einzelnen Nagel ringen; keine Gesichter im Bild",
  "Schatten: hart von links", "zeitlos, sinnbildlich", "teil",
  diagramm="Kein Schema: Raumbild mit Körperteil-Framing. Die Leiter aus den "
           "Schemata taucht hier als Gegenstand auf — bewusster Bruch, damit "
           "der Schlusspunkt des Absatzes greifbar wird.")

# --- Absatz 18: Schluss ------------------------------------------------------
m("M90", "Das Parallaxendreieck aus dem Anfang, unverändert: Erdbahn, zwei "
         "Standpunkte, zwei Sichtlinien, ein Keil", "Schema",
  "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D1-Reprise. Identisch zu M06 — die Wiedererkennung ist der Zweck.")
m("M91", "Die Leiter und das Dreieck zusammen in einem Bild: das Dreieck "
         "unten, die Leiter darauf, oben verliert sie sich in einem Sternfeld",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True,
  diagramm="D10d: Beide Schlüsselgrafiken vereint. Nur verständlich, WEIL "
           "beide vorher einzeln eingeführt wurden.")
m("M92", "Nahaufnahme: dieselben zwei Hände wie am Leuchttisch, die eine "
         "notiert mit dem Bleistift eine kurze Linie, direkt daneben eine "
         "zweite, kürzere Linie", "sichtbar: der Leuchttisch von unten",
  "Harvard College Observatory, um 1910", "teil")
m("M93", "Ein einzelner Punkt mit einem waagerechten Fehlerbalken darunter, "
         "sonst nichts im Bild", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D-AF: Ein Wert, ein Fehlerbalken. Das Schlussbild des Gedankens "
           "— die zweite Zahl neben der ersten, ohne ein Wort.")
# Kein M94: der Schluss greift auf M02 zurueck, dasselbe Bild.


# ------------------------------------------------------------ Einstellungen --
# (Wortlaut, Motiv, Fahrt). Der Wortlaut muss den Sprechtext exakt kacheln.
FAHRTEN = {"Zoom rein", "Zoom raus", "Schwenk links", "Schwenk rechts", "statisch"}
E: list[tuple[str, str, str]] = [
 # Absatz 1
 ("Look up tonight and pick a star. Any star you like.", "M01", "Zoom rein"),
 ("Now ask yourself: how far away is that thing?", "M01", "statisch"),
 ("If you draw a blank, you're in good company.", "M02", "Zoom raus"),
 ("In a survey of more than three thousand people,", "M03", "Zoom raus"),
 ("one in four said the stars are closer to us than the Sun.", "M03", "Zoom rein"),
 ("Asked to put a number on the nearest star, five out of six students wouldn't even guess.", "M04", "Schwenk rechts"),
 ("Of those who did, only one in five landed in the right range", "M05", "Zoom rein"),
 ("— about three people in a hundred.", "M05", "statisch"),
 ("So how do astronomers know? Here's the answer, right away: with a triangle.", "M06", "Zoom rein"),
 ("No probe flies out there. No radar comes back.", "M07", "statisch"),
 ("You measure an angle, twice, half a year apart — and geometry does the rest.", "M06", "Schwenk rechts"),
 # Absatz 2
 ("And you already own the trick. Hold up your thumb at arm's length. Shut your left eye.", "M09", "Zoom rein"),
 ("Now swap eyes. Your thumb jumps against the wall", "M10", "statisch"),
 ("— because each of your eyes looks from its own spot.", "M11", "Zoom rein"),
 ("Two viewpoints, one shift: that's how you see depth.", "M11", "statisch"),
 ("To do the same with a star, you need two viewpoints as far apart as you can get them.", "M12", "Zoom raus"),
 ("The farthest pair you will ever own is this: the Earth in January, and the Earth in July.", "M12", "Schwenk rechts"),
 ("Two points of your planet's orbit, three hundred million kilometres apart.", "M12", "Zoom rein"),
 ("Photograph a near star from both. Against the sea of far stars behind it,", "M13", "statisch"),
 ("it jumps — just like your thumb did.", "M14", "statisch"),
 ("Half of that jump, as an angle, is called the parallax.", "M06", "Zoom rein"),
 ("One clean rule ties it to distance: the smaller the jump, the farther the star.", "M15", "Schwenk rechts"),
 # Absatz 3
 ("Simple? You'd think so. The catch: from the idea to the first published jump took two hundred and ninety-five years.", "M16", "Zoom raus"),
 # Absatz 4
 ("Copernicus set the Earth moving in 1543, and the objection came at once:", "M17", "Zoom rein"),
 ("if we ride a moving platform, the stars should sway", "M18", "Schwenk rechts"),
 ("— and nobody saw any sway.", "M18b", "statisch"),
 ("The sharpest eyes of that century belonged to Tycho Brahe,", "M19", "Zoom rein"),
 ("a Danish noble who charted the sky, with no telescope, more finely than anyone alive.", "M19", "Schwenk links"),
 ("He looked. Nothing. Then he did the maths on that nothing:", "M20", "Zoom rein"),
 ("to hide from his instruments, the stars would have to sit seven hundred times farther out than Saturn.", "M21", "Zoom raus"),
 ("Worse: to his eye, every bright star showed a tiny round disk.", "M22", "Zoom rein"),
 ("A disk that wide, pushed that far out, means a star of monstrous size — dwarfing the Sun.", "M23", "Zoom raus"),
 ("Too absurd to accept, he judged, and kept the Earth still.", "M24", "statisch"),
 ("His logic was sound. His premise was not.", "M24", "Zoom rein"),
 ("The disks are not real. Air and eye wrap every point of light in blur,", "M25", "statisch"),
 ("and what Tycho measured was the blur.", "M22", "Zoom rein"),
 ("The largest true star disk in our night sky is about a thousand times smaller than what he saw.", "M26", "Zoom raus"),
 ("It took until around 1700 to accept the disks as an illusion", "M27", "Zoom rein"),
 ("— an \"optick fallacy,\" as it was put back then.", "M27", "Schwenk rechts"),
 ("Tycho wasn't sloppy. He measured what a human eye can see — it just wasn't the star.", "M22", "Zoom rein"),
 # Absatz 5
 ("The hunt ran on — into the 1830s, when it became a race.", "M28", "Zoom raus"),
 ("Three men, three cities, three stars.", "M28", "Schwenk rechts"),
 # Absatz 6
 ("In Königsberg, Friedrich Bessel had a new tool: a telescope", "M29", "Zoom rein"),
 ("whose main lens was cut clean in half, one half sliding on a fine screw.", "M30", "Zoom rein"),
 ("Slide it until two star images meet, read the screw,", "M31", "statisch"),
 ("and you've read an angle no eye could split.", "M32", "statisch"),
 ("He aimed at a dim star called 61 Cygni — picked because it crawls across the sky unusually fast.", "M33", "Schwenk rechts"),
 ("An Italian, Giuseppe Piazzi, had spotted that hurry in 1792 — a fast star is usually a near one.", "M33", "Zoom rein"),
 ("Through 1837 and 1838 Bessel measured; then he published:", "M34", "Zoom rein"),
 ("a jump of about a third of an arcsecond.", "M34", "statisch"),
 ("An arcsecond — take one degree, cut it into three thousand six hundred slices, keep one.", "M35", "Zoom rein"),
 ("Bessel's angle is a two-euro coin seen from seventeen kilometres.", "M36", "Zoom raus"),
 ("From it he got a distance of ten point four light-years", "M37", "Zoom raus"),
 ("— a light-year being the stretch light crosses in one year, nine and a half trillion kilometres.", "M37", "Schwenk rechts"),
 ("Today's value for that star: eleven point four. With a sawn lens and a screw,", "M38", "statisch"),
 ("he came within a tenth of the truth.", "M38", "Zoom rein"),
 # Absatz 7
 ("But he wasn't first to measure. Five years before, at the Cape of Good Hope,", "M39", "Zoom raus"),
 ("Thomas Henderson had caught the jump of a bright southern star, Alpha Centauri", "M39", "Schwenk links"),
 ("— and put the result in a drawer. Earlier claims of a parallax had been shot down;", "M40", "Zoom rein"),
 ("the story handed down says he didn't trust his own numbers.", "M40", "statisch"),
 ("He published in 1839 — second, for want of nerve.", "M40", "Zoom raus"),
 ("And in Dorpat, Wilhelm Struve had measured Vega and landed close to today's value", "M41", "Zoom rein"),
 ("— 0.125 arcseconds, against the modern 0.129. Then Bessel doubted Struve's data,", "M42", "Zoom rein"),
 ("and Struve revised his good number to nearly double. Away from the truth.", "M43", "statisch"),
 ("Colleagues stopped trusting his numbers.", "M43", "Zoom raus"),
 ("So who was first? Pick your rule. First to measure: Henderson.", "M44", "statisch"),
 ("First to make the full case in print: Bessel.", "M44", "Schwenk rechts"),
 ("First to print any number at all: arguably Struve. The books give all three answers — side by side.", "M44", "Zoom raus"),
 # Absatz 8
 ("You'd think it gets easy after that. It doesn't. The angles are brutal.", "M45", "Zoom raus"),
 ("By 1900 — sixty years on — astronomers had collected about sixty parallaxes in total.", "M45", "Zoom rein"),
 ("Sixty known distances, in a galaxy of billions.", "M45", "Schwenk rechts"),
 ("The real jump came when measuring left the ground.", "M46", "Zoom raus"),
 ("A satellite called Hipparcos pinned down 118,000 stars in the 1990s", "M46", "Schwenk rechts"),
 ("— though only about one in six of them with an error under ten percent.", "M47", "Zoom rein"),
 ("Then came Gaia, a European craft that scanned the sky from 2013 to 2025 and measured more than a billion stars.", "M48", "Schwenk links"),
 ("At its sharpest — on paper — its angle is that same two-euro coin,", "M49", "Zoom raus"),
 ("now seen from 759,000 kilometres, twice as far as the Moon.", "M49", "Zoom rein"),
 ("Still: the triangle runs out inside our own galaxy.", "M50", "Zoom raus"),
 ("The Milky Way spans some 87,000 light-years, give or take a few thousand", "M50", "Schwenk rechts"),
 ("— and for most stars, Gaia's sharp reach covers a slice of that.", "M50", "Zoom rein"),
 ("Past it, the jump drowns in noise. No bigger telescope changes the base of the triangle", "M51", "Zoom rein"),
 ("— and past a point, the jump is smaller than the blur.", "M51", "statisch"),
 # Absatz 9
 ("Everything farther — every other galaxy, the deep sky — stands on something else. A ladder.", "M52", "Zoom raus"),
 ("And its second rung was built by a woman paid thirty cents an hour.", "M53", "Zoom rein"),
 # Absatz 10
 ("Harvard, 1908 to 1912. Henrietta Leavitt worked in a room of women", "M54", "Zoom raus"),
 ("hired to read glass photographs of the sky", "M54", "Schwenk rechts"),
 ("— plates taken by the men who ran the telescopes, and brought in for the women to measure.", "M54", "Zoom rein"),
 ("Her plates showed the Small Magellanic Cloud, a small companion galaxy of ours.", "M56", "Zoom raus"),
 ("On them she found stars that pulse: they brighten, fade, and brighten again,", "M57", "statisch"),
 ("on a steady beat of days or weeks.", "M58", "statisch"),
 ("We now call them Cepheids.", "M57", "Zoom rein"),
 ("Across twenty-five of them, she found the pattern: the slower the beat, the brighter the star.", "M55", "Zoom rein"),
 ("On her chart, the points fell along two clean straight lines.", "M59", "Zoom raus"),
 ("And she wrote down, herself, what it meant: these stars all sit at roughly the same distance from us", "M55", "statisch"),
 ("— they share the Cloud — so the beat apparently tracks how much light a star truly puts out.", "M56", "Zoom rein"),
 ("Hold on to that — it unlocks the deep universe.", "M59", "Zoom rein"),
 ("Read a Cepheid's rhythm, and you know its true brightness.", "M60", "statisch"),
 ("Compare that with how faint it looks, and the dimming hands you the distance.", "M61", "Schwenk rechts"),
 ("Astronomers call that a standard candle: a lamp whose true output you know.", "M60", "Zoom rein"),
 # Absatz 11
 ("Hers could be read across millions of light-years. One catch — and she named it too.", "M61", "Zoom raus"),
 ("Her chart had no scale. No one knew the distance to the Cloud itself,", "M62", "Zoom rein"),
 ("so her law gave only ratios: this star is four times farther than that one.", "M62", "statisch"),
 ("Four times what?", "M62", "Zoom raus"),
 ("She wrote that she hoped parallaxes would be measured for a few stars of this kind.", "M55", "Zoom rein"),
 ("A year on, Ejnar Hertzsprung found a rough scale — not by one clean triangle,", "M63", "Zoom raus"),
 ("but by pooling the slow drift of thirteen nearby Cepheids.", "M63", "Zoom rein"),
 # Absatz 12
 ("Her paper ran under her director's signature; its first line records that it was \"prepared by Miss Leavitt\".", "M64", "Schwenk links"),
 ("In 1925, a Swedish mathematician wrote to her about putting her name up for the Nobel Prize", "M65", "Zoom rein"),
 ("— not knowing she had been dead for four years.", "M65", "statisch"),
 # Absatz 13
 ("Mark that shape — everything since is built the same way: rung two stands on rung one.", "M66", "Zoom raus"),
 ("Cepheids are calibrated by parallax.", "M66", "Zoom rein"),
 ("The rungs above — exploding stars, whole galaxies — are calibrated by Cepheids.", "M66", "Schwenk rechts"),
 ("Every rung inherits the reach of the one below. And every rung inherits its errors.", "M67", "Zoom rein"),
 # Absatz 14
 ("And the errors came. The ladder has snapped twice, in public.", "M68", "Zoom rein"),
 # Absatz 15
 ("First break. In 1929, Edwin Hubble used Cepheid distances", "M69", "Zoom rein"),
 ("to show that the galaxies flee from us — the farther, the faster.", "M70", "Zoom raus"),
 ("The universe expands; run that film backwards, and you get an age.", "M71", "Zoom rein"),
 ("His rate gave: not quite two billion years. Awkward, even then", "M72", "statisch"),
 ("— geologists put the Earth itself at around two billion.", "M72", "Zoom rein"),
 ("By the mid-fifties it turned absurd: the Earth's true age came in at four and a half billion", "M73", "statisch"),
 ("— older than the universe around it.", "M73", "Zoom rein"),
 ("Part of the fault lay on Leavitt's rung. There are two families of pulsing stars,", "M74", "Zoom raus"),
 ("with two different rulers, and mixing them had shrunk the cosmos.", "M74", "Schwenk rechts"),
 ("Walter Baade pulled them apart and announced it in Rome, in 1952", "M75", "Zoom rein"),
 ("— at a stroke, the universe doubled. Still too small.", "M76", "Zoom raus"),
 ("In 1958, Allan Sandage found that Hubble had also mistaken glowing gas clouds for bright stars.", "M77", "Zoom rein"),
 ("The rate fell again, and the universe came out comfortably older than the Earth.", "M73", "Zoom raus"),
 ("Total correction, first to last: about a factor of seven.", "M78", "Schwenk rechts"),
 # Absatz 16
 ("Second break, closer to home. The Pleiades — the little cluster you can spot with bare eyes.", "M79", "Zoom rein"),
 ("Hipparcos, the trusted satellite, put it at about 390 light-years.", "M80", "statisch"),
 ("Nearly every other method said 435 to 445.", "M80", "Zoom rein"),
 ("For seventeen years, the field's best instrument disagreed with everyone else", "M80", "Zoom raus"),
 ("— about one of the nearest clusters in the sky. In 2014, radio telescopes settled it:", "M82", "Schwenk rechts"),
 ("444 light-years, give or take four — the satellite was wrong.", "M81", "Zoom rein"),
 # Absatz 17
 ("And today, the ladder is in its third fight", "M84", "Zoom raus"),
 ("— this one still open. Two numbers for how fast the universe grows.", "M85", "statisch"),
 ("From the oldest light there is, the Planck satellite reads 67.4, with an error of half a point.", "M83", "Zoom rein"),
 ("From the ladder — parallax, to Cepheids, to exploding stars that all flare to nearly the same true brightness —", "M84", "Schwenk rechts"),
 ("a team called SH0ES reads 73.0, plus or minus one.", "M85", "Zoom rein"),
 ("A five-sigma difference, in their own words: far too large to be chance.", "M85", "Zoom raus"),
 ("You'll hear that sold as the early universe against today's.", "M83", "Zoom raus"),
 ("But here's what that framing skips. A second team climbed the same ladder", "M86", "statisch"),
 ("with a different second rung — red giant stars instead of Cepheids,", "M86", "Zoom rein"),
 ("with the new James Webb telescope in the mix —", "M86", "Schwenk rechts"),
 ("and read 67.8 to 70.4, depending on the sample and the method.", "M87", "Zoom raus"),
 ("Their own verdict: no new physics needed.", "M87", "statisch"),
 ("Same universe. Same ladder. Different rung — different answer.", "M87", "Zoom rein"),
 ("And the strangest part: both teams agree on the distances to the very same galaxies, to about one percent.", "M88", "Zoom rein"),
 ("The stars are not the quarrel.", "M88", "statisch"),
 ("The quarrel is over which exploding stars to hang the scale on.", "M89", "Zoom raus"),
 ("The ladder holds; the argument is about the nail. Nobody yet knows which side is right.", "M89", "Zoom rein"),
 # Absatz 18
 ("So — how do we know how far away the stars are?", "M90", "Zoom raus"),
 ("For the near ones: a triangle. Your thumb trick, stretched across the Earth's orbit,", "M90", "Zoom rein"),
 ("sharpened until a coin past the Moon is an easy target.", "M49", "Zoom rein"),
 ("For the far ones: a ladder of light. A rhythm", "M91", "Zoom raus"),
 ("read off glass plates for thirty cents an hour,", "M53", "Zoom rein"),
 ("nailed to the triangle, broken twice, patched twice, and argued over right now.", "M91", "Zoom rein"),
 ("One in four of the people asked thinks the stars hang closer than the Sun.", "M03", "Zoom rein"),
 ("The nearest one sits so deep that its light spends four years on the road to you.", "M37", "Zoom rein"),
 ("But that number is no guess, and never was. Someone caught its jump.", "M90", "Zoom raus"),
 ("Someone read its beat. And beside every distance, they wrote a second number:", "M92", "statisch"),
 ("how far off it might be. That second number is the honest answer.", "M93", "Zoom rein"),
 ("We don't just know how far the stars are.", "M02", "Zoom raus"),
 ("We know how well we know it — and exactly where we don't.", "M02", "Zoom rein"),
]


BILD_2K = 2.0     # per get_cost gemessen, siehe KOSTEN_STAND
CLIP_4S = 12.0
EURO_ULTRA = 0.033
EURO_NACHKAUF = 0.049
KOSTEN_STAND = "2026-08-16"


def absatz_je_einstellung(rein: str, zeilen: list[dict]) -> list[int]:
    """Ordnet jede Einstellung dem Absatz zu, in dem ihr erstes Wort steht."""
    grenzen, n = [], 0
    for abs_ in [a for a in rein.split("\n\n") if a.strip()]:
        n += len(abs_.split())
        grenzen.append(n)
    out, w = [], 0
    for z in zeilen:
        out.append(next(i for i, g in enumerate(grenzen, 1) if w < g) )
        w += z["woerter"]
    return out


def schreibe_md(zeilen: list[dict], rein: str, kum: float) -> None:
    ab = absatz_je_einstellung(rein, zeilen)
    schema = [k for k, v in M.items() if v.get("schema")]
    welt = [k for k, v in M.items() if not v.get("schema")]
    eb = [k for k, v in M.items() if v.get("ebenen")]
    schutz = [k for k, v in M.items() if v.get("schutz")]
    pers = [k for k, v in M.items() if v.get("person")]
    paare = sorted({tuple(sorted((k, v["paar"])))
                    for k, v in M.items() if v.get("paar")})
    d = [z["dauer"] for z in zeilen]
    s_zeit = sum(z["dauer"] for z in zeilen if M[z["motiv"]].get("schema"))
    s_ein = sum(1 for z in zeilen if M[z["motiv"]].get("schema"))
    fig = sum(1 for z in zeilen if M[z["motiv"]]["framing"] in ("ganz", "teil"))
    wfr = {f: sum(1 for k in welt if M[k]["framing"] == f)
           for f in ("ganz", "ohne", "teil")}

    A = len(M) * BILD_2K
    B = A + len(eb) * BILD_2K
    C = B + len(schutz) * CLIP_4S
    ALLES = len(zeilen) * CLIP_4S

    def z2(x: float, n: int = 2) -> str:
        """Deutsches Dezimalkomma — das Dokument ist deutsch."""
        return f"{x:.{n}f}".replace(".", ",")

    def kurz(t: str, n: int = 84) -> str:
        t = " ".join(t.split())
        return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"

    def mmss(x: float) -> str:
        return f"{int(x//60)}:{x%60:04.1f}".replace(".", ",")

    def eur(c: float) -> str:
        return z2(c * EURO_ULTRA) + " | " + z2(c * EURO_NACHKAUF)

    L: list[str] = []
    w = L.append
    w("# Szenenliste — Video 2, „How Do We Know How Far Away the Stars Are?"
      "\"\n")
    w("> **Erzeugt aus `szenenplan.py`, nicht getippt.** Jedes Motiv ist ein\n"
      "> Datensatz mit Pflichtfeldern; fehlt eines, bricht der Generator ab,\n"
      "> bevor eine Zeile Markdown entsteht. Der Wortlaut jeder Einstellung\n"
      "> wird gegen `skript.md` geprüft — die Aneinanderreihung aller\n"
      "> Einstellungen muss den Sprechtext exakt ergeben.\n"
      "> **0 Credits verbraucht**, keine Bildgenerierung; Preise nur per\n"
      f"> `get_cost`-Preflight am {KOSTEN_STAND}.\n")

    w("## Wie zu lesen\n")
    w("- **Motiv** = ein zu generierendes Bild. Mehrere Einstellungen mit\n"
      "  demselben Motiv teilen sich **ein** Bild und unterscheiden sich nur\n"
      "  durch die Kamerafahrt.\n"
      "- **Fahrt** = was `ffmpeg` über dem Standbild fährt: `Zoom rein`,\n"
      "  `Zoom raus`, `Schwenk links`, `Schwenk rechts`, `statisch`.\n"
      "- **Licht** ist Pflichtfeld und kennt genau drei Formen: `sichtbar:`\n"
      "  (die Quelle steht **im Bild**), `Schatten:` (Quelle außerhalb, aber\n"
      "  eindeutig gerichteter harter Schatten), `Durchlicht:`. Bei Video 1\n"
      "  konnten 27 von 62 Raumbildern die Quelle physisch nicht zeigen, weil\n"
      "  der Plan sie nie verlangt hatte. Der Generator lehnt jetzt jede\n"
      "  Zeile ab, die eine Quelle als sichtbar deklariert und sie im selben\n"
      "  Satz aus dem Bild schiebt.\n"
      "- **Ort** nennt Epoche und Ort, auch bei figurenlosen Motiven.\n"
      "- **Flora** ist bedingt formuliert: eine Grenze dessen, was hier\n"
      "  wachsen darf, keine Aufforderung, Pflanzen hinzuzufügen.\n"
      "- **Framing** dreifach: `ganz` (Ganzfigur), `ohne` (keine Figur),\n"
      "  `teil` (Körperteil-Nahaufnahme).\n"
      "- **Zustandspaar** = zwei Bilder derselben Komposition in zwei\n"
      "  Zuständen. Spart kein Bild, aber die Wiedererkennung ist der Grund,\n"
      "  warum eine Einstellung kürzer als drei Sekunden stehen darf.\n"
      "- **Ebenen** = Vorder- und Hintergrund werden getrennt generiert,\n"
      "  damit `ffmpeg` sie unterschiedlich schnell bewegen kann.\n")

    w("## Stilbindung\n")
    w("Gilt für jeden Prompt, ohne Ausnahme:\n\n"
      "- **V2-Machart** aus `stil-figuren/lauf2-erwachsen/README.md`,\n"
      "  erwachsene Figuren, **Z3-Lichtführung**.\n"
      "- **Kein Türkis, keine Themenpalette.** Beides ist am 15.08.2026\n"
      "  ersatzlos entfallen; die Farbwelt ist natürlich.\n"
      "- **Getrennte Farbsätze.** Weltbilder tragen den Naturfarbsatz,\n"
      "  Schemata den Schemafarbsatz — kein Himmel, keine Vegetation, ein\n"
      "  ruhiger einfarbiger Grund. Bei Video 1 war das eine Regel für alle,\n"
      "  und ein Diagramm bekam prompt blauen Himmel und Gras.\n"
      "- **Kein Text im Bild.** `no text, no letters, no watermark, no logo`.\n"
      "  Wo eine Zahl tragen muss, trägt sie die Stimme.\n")

    w("## Entscheidung: die historischen Personen\n")
    w(f"Sieben Motive zeigen eine historisch belegte Person ({', '.join(pers)}).\n"
      "**Alle sieben sind Epochenfiguren ohne Portraitähnlichkeit.** Sie sind\n"
      "über Kleidung, Haltung, Gerät und Ort beschrieben, nie über ein\n"
      "Gesicht. Kein Bildtext nennt einen Namen — der Generator prüft das und\n"
      "bricht ab, wenn doch einer darin steht, denn ein Name im Prompt ist\n"
      "die Anweisung, ein Gesicht zu treffen.\n\n"
      "Zwei Merkmale sind dabei bewusst weggelassen worden: Tycho Brahes\n"
      "Metallnase und Hubbles Pfeife. Beide sind das eine Attribut, an dem\n"
      "eine Figur aufhört, „ein Astronom dieser Zeit\" zu sein, und anfängt,\n"
      "eine bestimmte Person zu sein. Die Epoche tragen Halskrause und\n"
      "Mauerquadrant beziehungsweise Tweed und Spiegelteleskop ohnehin.\n")

    w("## Szenentabelle\n")
    w("| # | ab | s | Motiv | Fahrt | Wortlaut |")
    w("|---:|---:|---:|---|---|---|")
    letzter = 0
    for z, a in zip(zeilen, ab):
        if a != letzter:
            w(f"| | | | | | **— Absatz {a} —** |")
            letzter = a
        t = z["text"].replace("|", "\\|")
        w(f'| {z["nr"]} | {mmss(z["start"])} | '
          f'{z2(z["dauer"],1)} | {z["motiv"]} | {z["fahrt"]} | {t} |')
    w("")

    w("## Motivkatalog\n")
    w("Der `szene`-Text ist der `SCENE:`-Teil des Prompts, nicht der ganze\n"
      "Prompt — das Stilgerüst kommt davor, die Ausschlussklausel danach.\n")
    for k, v in M.items():
        marken = []
        if v.get("schema"):
            marken.append("Schema")
        if v.get("person"):
            marken.append("Epochenfigur")
        if v.get("paar"):
            marken.append(f"Zustandspaar mit {v['paar']}")
        if v.get("ebenen"):
            marken.append("getrennte Ebenen")
        if v.get("schutz"):
            marken.append("**geschützter Moment**")
        n = sum(1 for z in zeilen if z["motiv"] == k)
        w(f"**{k}** · {n} Einstellung{'en' if n != 1 else ''}"
          + (" · " + " · ".join(marken) if marken else ""))
        w(f"- Bild: {' '.join(v['szene'].split())}")
        w(f"- Licht: {' '.join(v['licht'].split())}")
        w(f"- Ort: {v['ort']}")
        if v["flora"] != "—":
            w(f"- Flora: {' '.join(v['flora'].split())}")
        w(f"- Framing: {v['framing']}")
        if v.get("diagramm"):
            w(f"- Ohne Beschriftung: {' '.join(v['diagramm'].split())}")
        w("")

    w("## Die Diagramme ohne Beschriftung\n")
    w(f"Alle {len(schema)} Schemata sind einzeln daraufhin geprüft worden, ob\n"
      "sie ohne ein einziges Zeichen lesbar sind; das Urteil steht bei jedem\n"
      "im Motivkatalog. Sieben haben die Prüfung **nicht** bestanden und sind\n"
      "geändert worden, bevor dieser Plan stand:\n")
    w("| Motiv | Was nicht funktionierte | Was jetzt dasteht |")
    w("|---|---|---|")
    w("| **M87** | Sieben unbeschriftete Fehlerbalken zeigen zwei Haufen — "
      "also genau das Früh-gegen-Spät-Bild, das das Skript widerlegt. Das "
      "Diagramm war nicht bloß unverständlich, es hätte das Gegenteil "
      "behauptet. | Jeder Balken trägt am Ende ein Symbol, das vorher "
      "eingeführt wurde: Fleckenscheibe, roter Riesenstern, pulsende Lampe. "
      "Damit liest das Auge die Trennlinie dort, wo sie verläuft — zwischen "
      "den beiden Leitersprossen. |")
    w("| **M85** | Zwei Balken ohne Kennung; welcher wessen ist, hing allein "
      "am Schnitt. | Dieselben zwei Symbole, Scheibe und Leiter. |")
    w("| **M78** | Sieben wachsende Kugeln zeigen sieben **Schritte**, nicht "
      "den **Faktor** sieben. | Eine kleine und eine große Kugel; über den "
      "Durchmesser der großen liegen sieben Abdrücke der kleinen. |")
    w("| **M15** | Die Hyperbel *d = 1/p* ist ohne Achsenbeschriftung "
      "bedeutungslos. | Zwei Sterne nebeneinander, einer mit weitem, einer "
      "mit winzigem Versatz. |")
    w("| **M03** | Drei Figuren hatten nur eine Sonne, die vierte nur einen "
      "Stern — es gab nichts zu vergleichen. | Über **jeder** Figur stehen "
      "beide; bei dreien hängt die Sonne tiefer, bei der vierten der Stern. |")
    w("| **M04** | Der eine, der geraten hat, trug einen *fragenden* Kopf — "
      "das ist keine Antwort. | Sechs Gedankenblasen, fünf leer, in der "
      "sechsten ein Stern mit einer Maßlinie. |")
    w("| **M18** | Auf dem Bild der erwarteten Schwankung stehen zu bleiben, "
      "während die Stimme sagt, dass niemand eine sah, behauptet das "
      "Gegenteil. | Zustandspaar M18/M18b: erst der Versatz, dann seine "
      "Abwesenheit. |")
    w("")
    w("**Der schwierigste Fall ist nicht das Parallaxendiagramm.** M06 trägt\n"
      "sich ohne Beschriftung, weil zwei Standpunkte, zwei Sichtlinien und\n"
      "ein Keil die ganze Aussage sind — es braucht keine Winkelmaße. Die\n"
      "eine Bedingung: der nahe Stern muss sichtbar größer und heller sein\n"
      "als das Feld dahinter, sonst sitzt der Keil scheinbar am falschen\n"
      "Punkt. Schwierig sind die **Fehlerbalken**, weil dort erstmals nicht\n"
      "eine Form, sondern eine Zuordnung getragen werden muss.\n\n"
      "**Einmal ist die Textlosigkeit ein Vorteil:** M62, der fehlende\n"
      "Nullpunkt. Eine Achse ohne einen einzigen Teilstrich sagt genau das,\n"
      "was Leavitts Gesetz fehlte — mit Beschriftung wäre es schwerer zu\n"
      "sehen, nicht leichter.\n")

    w("## Zustandspaare\n")
    w("| Paar | Zustand A | Zustand B |")
    w("|---|---|---|")
    for a, b in paare:
        w(f"| {a} / {b} | {kurz(M[a]['szene'])} | {kurz(M[b]['szene'])} |")
    w("")

    w("## Getrennte Ebenen\n")
    w(f"**{len(eb)} von {len(M)} Motiven**: " + ", ".join(eb) + ".\n")

    w("## Die geschützten Momente\n")
    w("| Moment | Einstellungen | Motiv | Dauer |")
    w("|---|---|---|---:|")
    for k in schutz:
        ein = [z for z in zeilen if z["motiv"] == k]
        w(f"| {M[k]['schutz']} | {', '.join(str(z['nr']) for z in ein)} "
          f"| {k} | {z2(sum(z['dauer'] for z in ein),1)} s |")
    w("")

    w("## Zahlen\n")
    w("| Größe | Wert |")
    w("|---|---|")
    w(f"| Einstellungen | **{len(zeilen)}** |")
    w(f"| Gesamtlaufzeit | {mmss(kum)} |")
    w(f"| Mittlere Dauer | **{z2(sum(d)/len(d))} s** (Ziel 3–5 s) |")
    w(f"| Spanne | {z2(min(d),1)} – {z2(max(d),1)} s |")
    w(f"| unter 3 s | {sum(1 for x in d if x < 3)} — jede davon auf demselben "
      "Motiv wie die Einstellung davor oder auf dessen Paarpartner |")
    w(f"| über 5 s | {sum(1 for x in d if x > 5)}, davon über 6 s: "
      f"{sum(1 for x in d if x > LANG_AB)} |")
    w(f"| **Motive (zu generierende Bilder)** | **{len(M)}** |")
    w(f"| Einstellungen je Motiv | {z2(len(zeilen)/len(M))} im Mittel |")
    w(f"| Mehrfach genutzte Motive | {sum(1 for k in M if sum(1 for z in zeilen if z['motiv']==k)>1)}"
      f" → **{len(zeilen)-len(M)} Bilder gespart** |")
    w(f"| Schemata | {len(schema)} Motive ({len(schema)/len(M)*100:.0f} %) · "
      f"{s_ein} Einstellungen ({s_ein/len(zeilen)*100:.0f} %) · "
      f"**{s_zeit/kum*100:.0f} % der Laufzeit** |")
    w(f"| Weltbilder | {len(welt)} — Framing ganz {wfr['ganz']} · "
      f"ohne {wfr['ohne']} · teil {wfr['teil']} |")
    w(f"| Zustandspaare | {len(paare)} |")
    w(f"| Motive mit getrennten Ebenen | {len(eb)} |")
    w(f"| Epochenfiguren | {len(pers)} |")
    w(f"| Einstellungen mit Figur oder Körperteil | {fig} ({fig/len(zeilen)*100:.0f} %) |")
    w("")

    w("## Kosten\n")
    w(f"Preise per `get_cost` gemessen am {KOSTEN_STAND}, unverändert "
      "gegenüber Video 1:\n")
    w("| Posten | Credits |")
    w("|---|---:|")
    w(f"| Standbild `nano_banana_2`, 16:9, **2k** | **{z2(BILD_2K,1)}** |")
    w("| Standbild 1k | 1,5 |")
    w(f"| Clip Seedance 1.5 Pro, 1080p, 4 s | {CLIP_4S:.0f} |")
    w("")
    w("| Variante | Credits | € Ultra | € Nachkauf |")
    w("|---|---:|---:|---:|")
    w(f"| **A — alle Motive als Standbild, ffmpeg bewegt** | **{A:.0f}** | {eur(A)} |")
    w(f"| **B — A plus getrennte Ebenen** | **{B:.0f}** | {eur(B)} |")
    w(f"| **C — B plus {len(schutz)} echte Clips für die geschützten Momente** "
      f"| **{C:.0f}** | {eur(C)} |")
    w(f"| zum Vergleich: alle {len(zeilen)} Einstellungen als Clip | "
      f"{ALLES:.0f} | {eur(ALLES)} |")
    w("")
    w("**Euro-Grundlage.** Das Konto läuft auf **Ultra**: 3.000 Credits im\n"
      "Monat, 99 € im Monat bei Jahreszahlung — also **0,033 € je Credit**.\n"
      "Ein Nachkauf kostet 0,049 € je Credit (1.000 Credits für 49 €).\n\n"
      "> **Achtung, Abweichung zu Video 1.** `produktion/video-01/szenen.md`\n"
      "> rechnet mit 0,00275 € je Credit und liest die 99 € als Jahrespreis.\n"
      "> Das ist um den Faktor zwölf zu niedrig. Video 1 bleibt auf Wunsch\n"
      "> unverändert; die Zahl hier ist die richtige.\n")
    w(f"**Variante C liegt bei {C:.0f} Credits** — unter der vereinbarten\n"
      f"Abbruchschwelle von 500 und bei {C/3000*100:.0f} % des "
      "Monatskontingents.\n")

    # Wechsel und laengste reine Schema-Strecke — der Schema-Anteil allein
    # sagt noch nicht, ob das Video kalt wird; die Klumpung sagt es.
    laeufe, akt, dauer_lauf = [], None, 0.0
    for z in zeilen:
        ist = bool(M[z["motiv"]].get("schema"))
        if ist != akt:
            if akt is not None:
                laeufe.append((akt, dauer_lauf))
            akt, dauer_lauf = ist, 0.0
        dauer_lauf += z["dauer"]
    laeufe.append((akt, dauer_lauf))
    wechsel = len(laeufe) - 1
    max_schema = max(x for k, x in laeufe if k)

    w("## Was diese Fassung nicht leistet\n")
    w(f"- **Der Schema-Anteil ist hoch und bleibt es.** {s_zeit/kum*100:.0f} % "
      "der Laufzeit\n"
      "  sind Zeichnung, gegenüber 26 % bei Video 1. Das folgt aus dem Thema —\n"
      "  ein Winkel, eine Leiter und ein Fehlerbalken lassen sich nicht\n"
      f"  fotografieren. Abgefedert ist es nur über den Wechsel: {wechsel} "
      "Übergänge\n"
      "  zwischen Zeichnung und Welt, längste reine Schema-Strecke "
      f"{z2(max_schema,1)} s.\n"
      "  Ob das reicht, ist eine Frage an das fertige Video, nicht an den Plan.\n"
      f"- **Die Figurenquote ist niedrig.** {fig/len(zeilen)*100:.0f} % der "
      "Einstellungen zeigen eine\n"
      "  Figur oder ein Körperteil, gegen 32 % bei Video 1. Derselbe Grund.\n"
      "- **Die Diagramm-Prüfung ist ein Urteil, keine Messung.** Ob ein Bild\n"
      "  ohne Beschriftung verständlich ist, lässt sich vor der Generierung\n"
      "  nicht messen; die Notizen im Motivkatalog sind begründete\n"
      "  Einschätzungen. Bei Video 1 waren es die Bilder, die dem Auge\n"
      "  durchgingen und erst der Messung auffielen — hier ist es umgekehrt,\n"
      "  und es bleibt offen.\n"
      "- **Kein Bildtext heißt auch: keine Achsen.** Bei M59, M62 und M87\n"
      "  hängt das Verständnis daran, dass die Stimme im selben Moment sagt,\n"
      "  was auf den Achsen stünde. Verschiebt sich der Schnitt gegen den\n"
      "  Ton, bricht genau das.\n")

    w("## Anschluss\n")
    w("1. Stichprobenlauf über 8–10 Motive, darunter **M06, M15, M87** — die\n"
      "   drei, an denen die Textlosigkeit am ehesten scheitert.\n"
      "2. Bei Freigabe: die restlichen Motive in Stapeln, danach die\n"
      f"   {len(eb)} zweiten Ebenen, zuletzt die {len(schutz)} Clips.\n"
      "3. `szenenplan.json` liefert `montage.py` Wortlaut, Motiv und Fahrt je\n"
      "   Einstellung; die Dauern hier sind aus 219 WPM gerechnet und werden\n"
      "   beim Schnitt durch die echten ElevenLabs-Zeichenzeiten ersetzt.\n")

    (HIER / "szenen.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    soll = (HIER.parent.parent / "produktion" / "video-02" / "skript.md")
    t = soll.read_text(encoding="utf-8")
    mm = re.search(r"^## Sprechtext\s*\n(.*?)^---\s*$", t, re.S | re.M)
    rein = re.sub(r"\s*\[(?:[WLA]\d*|A)\]", "", mm.group(1).strip())
    ziel = " ".join(rein.split())

    # 1. Deckt die Einstellungsliste den Sprechtext exakt?
    gebaut = " ".join(" ".join(x[0].split()) for x in E)
    if gebaut != ziel:
        for i, (a, b) in enumerate(zip(gebaut.split(), ziel.split())):
            if a != b:
                print(f"ABWEICHUNG ab Wort {i}: gebaut {a!r} vs. soll {b!r}")
                print("  gebaut:", " ".join(gebaut.split()[max(0,i-8):i+8]))
                print("  soll  :", " ".join(ziel.split()[max(0,i-8):i+8]))
                break
        raise SystemExit(f"Textabdeckung falsch: {len(gebaut.split())} statt "
                         f"{len(ziel.split())} Woerter")

    # 2. Pflichtfelder je Motiv
    for mid, d in M.items():
        for feld in ("szene", "licht", "ort", "framing", "flora"):
            if not d.get(feld):
                raise SystemExit(f"{mid}: Feld {feld} fehlt")
        if d["framing"] not in ("ganz", "ohne", "teil"):
            raise SystemExit(f"{mid}: Framing {d['framing']!r} unbekannt")
        # Historische Personen erscheinen als Figuren ihrer Epoche, nicht
        # als Portraits. Der Name darf im Bildtext nicht auftauchen: er
        # waere die Anweisung, ein Gesicht zu treffen, und von Leavitt und
        # Bessel gibt es Aufnahmen, die getroffen werden koennten.
        for n in PERSONEN:
            if n in d["szene"]:
                raise SystemExit(f"{mid}: Bildtext nennt {n} — Personen "
                                 "werden nur über Kleidung, Haltung, "
                                 "Gerät und Epoche beschrieben")
        if d.get("schema") and not d["licht"].startswith("Schema"):
            raise SystemExit(f"{mid}: Schema, aber Licht {d['licht']!r}")
        # Nur drei Formen sind erlaubt, und "sichtbar" heisst: die Quelle
        # steht IM Bild. Bei Video 1 konnten 27 von 62 Raumbildern die
        # Quelle physisch nicht zeigen, weil das im Plan nie verlangt war.
        if not d.get("schema"):
            if not d["licht"].startswith(("sichtbar:", "Schatten:",
                                          "Durchlicht:")):
                raise SystemExit(f"{mid}: Licht {d['licht']!r} — erlaubt "
                                 "sind nur 'sichtbar:', 'Schatten:', "
                                 "'Durchlicht:'")
            if (d["licht"].startswith("sichtbar:")
                    and "außerhalb" in d["licht"]):
                raise SystemExit(f"{mid}: Quelle als sichtbar deklariert, "
                                 "liegt aber außerhalb des Bildes")
        if d.get("schema") and not d.get("diagramm"):
            raise SystemExit(f"{mid}: Schema ohne Diagramm-Pruefung")
    for mid, fahrt in ((x[1], x[2]) for x in E):
        if mid not in M:
            raise SystemExit(f"Einstellung nutzt unbekanntes Motiv {mid}")
        if fahrt not in FAHRTEN:
            raise SystemExit(f"{mid}: Fahrt {fahrt!r} unbekannt")
    for mid, d in M.items():
        if d.get("paar") and d["paar"] not in M:
            raise SystemExit(f"{mid}: Partner {d['paar']} fehlt")
        if d.get("paar") and M[d["paar"]].get("paar") != mid:
            raise SystemExit(f"{mid}/{d['paar']}: Paar nicht wechselseitig")
    ungenutzt = sorted(set(M) - {x[1] for x in E})
    if ungenutzt:
        raise SystemExit(f"Motive ohne Einstellung: {ungenutzt}")

    # 3. Zeiten
    zeilen, kum = [], 0.0
    for nr, (txt, mid, fahrt) in enumerate(E, 1):
        w = len(txt.split())
        dauer = w / WPM * 60
        zeilen.append(dict(nr=nr, text=txt, motiv=mid, fahrt=fahrt,
                           woerter=w, start=kum, dauer=dauer))
        kum += dauer
    # 4. Schnittrhythmus. Eine Einstellung braucht so lange, wie das Auge
    #    braucht, um ein NEUES Bild zu lesen — 3 bis 5 s. Kuerzer darf sie
    #    nur sein, wenn gar kein neues Bild kommt: entweder dasselbe Motiv
    #    wie zuvor (nur die Kamera bewegt sich weiter) oder der Partner
    #    eines Zustandspaars (das Auge liest nur den Unterschied). Beide
    #    Faelle sind der Grund, warum es die Paare ueberhaupt gibt.
    kurz = []
    for i, z in enumerate(zeilen):
        if z["dauer"] >= KURZ_AB:
            continue
        vor = zeilen[i - 1]["motiv"] if i else None
        if vor == z["motiv"] or M[z["motiv"]].get("paar") == vor:
            continue
        kurz.append(f'{z["nr"]} {z["dauer"]:.1f}s {z["motiv"]} '
                    f'(davor {vor}) {z["text"][:52]!r}')
    lang = [f'{z["nr"]} {z["dauer"]:.1f}s {z["motiv"]} {z["text"][:52]!r}'
            for z in zeilen if z["dauer"] > LANG_AB]
    if kurz or lang:
        for x in kurz:
            print("ZU KURZ, ohne Vorbild:", x)
        for x in lang:
            print("ZU LANG:", x)
        raise SystemExit(f"Schnittrhythmus: {len(kurz)} zu kurz, "
                         f"{len(lang)} zu lang")

    (HIER / "szenenplan.json").write_text(
        json.dumps({"einstellungen": zeilen, "motive": M}, indent=1,
                   ensure_ascii=False), encoding="utf-8")

    d = [z["dauer"] for z in zeilen]
    schema = [k for k, v in M.items() if v.get("schema")]
    ebenen = [k for k, v in M.items() if v.get("ebenen")]
    paare = sorted({tuple(sorted((k, v["paar"]))) for k, v in M.items() if v.get("paar")})
    schutz = [k for k, v in M.items() if v.get("schutz")]
    fr = {f: [k for k, v in M.items() if v["framing"] == f] for f in ("ganz", "ohne", "teil")}
    mehrfach = {k for k in M if sum(1 for x in E if x[1] == k) > 1}
    e_fig = sum(1 for x in E if M[x[1]]["framing"] in ("ganz", "teil"))

    print(f"Einstellungen {len(E)} · Motive {len(M)} · Laufzeit "
          f"{int(kum//60)}:{kum%60:04.1f}")
    print(f"Dauer Mittel {sum(d)/len(d):.2f} s · Spanne {min(d):.1f}–{max(d):.1f} s"
          f" · unter 3 s: {sum(1 for x in d if x < 3)} · über 5 s: "
          f"{sum(1 for x in d if x > 5)} · über 8 s: {sum(1 for x in d if x > 8)}")
    # Der Zuschauer zaehlt keine Motive, er sitzt die Laufzeit ab. Also
    # zaehlt der Schema-Anteil nach Sekunden, nicht nach Motiven.
    s_zeit = sum(z["dauer"] for z in zeilen if M[z["motiv"]].get("schema"))
    s_ein = sum(1 for z in zeilen if M[z["motiv"]].get("schema"))
    welt = {k: v for k, v in M.items() if not v.get("schema")}
    wfr = {f: sum(1 for v in welt.values() if v["framing"] == f)
           for f in ("ganz", "ohne", "teil")}
    print(f"Schemata {len(schema)} = {len(schema)/len(M)*100:.0f} % der Motive"
          f" · {s_ein}/{len(E)} Einstellungen = {s_ein/len(E)*100:.0f} %"
          f" · {s_zeit/kum*100:.0f} % der Laufzeit")
    print(f"Framing — ganz {len(fr['ganz'])} · ohne {len(fr['ohne'])} · teil {len(fr['teil'])}")
    print(f"  davon Weltbilder ({len(welt)}): ganz {wfr['ganz']} · "
          f"ohne {wfr['ohne']} · teil {wfr['teil']}")
    laengste = sorted(zeilen, key=lambda z: -z["dauer"])[:3]
    print("Längste: " + " | ".join(f'{z["dauer"]:.1f}s {z["motiv"]}' for z in laengste))
    pers = [k for k, v in M.items() if v.get("person")]
    print(f"Zustandspaare {len(paare)} · Ebenen {len(ebenen)} · "
          f"geschützt {len(schutz)} · Epochenfiguren {len(pers)}")
    print(f"Mehrfach genutzte Motive {len(mehrfach)} → {len(E)-len(M)} Bilder gespart")
    print(f"Einstellungen mit Figur oder Körperteil: {e_fig} = {e_fig/len(E)*100:.0f} %")

    schreibe_md(zeilen, rein, kum)
    print("szenen.md geschrieben")


if __name__ == "__main__":
    main()
