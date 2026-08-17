#!/usr/bin/env python3
"""Szenenplan fuer Video 2 — NEU GEBAUT am 16.08.2026 fuer die Erzaehlfassung.

Der alte Plan (84→93 Motive, in der Git-Historie) war an der Erklaerform
gebaut: 52 Schemata, 58 % der Laufzeit Zeichnung. Die Erzaehlfassung
verlangt Szenen statt Diagramme — dieser Plan ist von Grund auf neu, nicht
angepasst.

Was er erzwingt (alles Pruefungen, keine Merkregeln):
  * Der Wortlaut aller Einstellungen kachelt den Sprechtext exakt.
  * Pflichtfelder je Motiv: szene, licht, ort, framing, flora.
  * Licht kennt drei Formen; "sichtbar" heisst: die Quelle steht IM Bild.
  * Kein Personenname im Bildtext; keine Versalien in der Bildbeschreibung
    (pruefe_szene aus bildplan.py — die M15-Lehre).
  * Einstellungen unter 2,4 s nur auf demselben Motiv oder dessen
    Paarpartner; keine ueber 6 s.
  * NEU: Schema-Anteil hoechstens 10 % der Laufzeit (Bildvorgabe der
    Erzaehlfassung; die Erklaerform lag bei 58 %, Video 1 bei 26 %).

Vier Schemata bleiben: das Parallaxendreieck (M12) und die Leiter in drei
Zustaenden (M42 intakt, M54 gebrochen, M64 Sprosse getauscht) — beide
Formen sind im Stichprobenlauf freigegeben. Alles andere ist Welt.
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re

HIER = pathlib.Path(__file__).resolve().parent
WPM = 219
KURZ_AB = 2.4   # darunter nur mit Vorbild (gleiches Motiv oder Paarpartner)
LANG_AB = 6.0   # darueber steht das Bild zu lange
SCHEMA_MAX = 0.10  # Anteil der Laufzeit, hart

# Versalien-Pruefung aus dem zentralen Prompt-Modul (Lehre aus M15).
_spec = importlib.util.spec_from_file_location(
    "bildplan", HIER.parent / "video-01" / "bildplan.py")
_bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_bp)
pruefe_szene = _bp.pruefe_szene

# Namen aus dem Skript, deren Traeger im Bild erscheinen. Kein Bildtext
# darf sie nennen — Epochenfiguren ohne Portraitaehnlichkeit.
PERSONEN = ("Kopernikus", "Copernicus", "Tycho", "Brahe", "Bessel",
            "Henderson", "Struve", "Piazzi", "Leavitt", "Henrietta",
            "Hertzsprung", "Hubble", "Baade", "Sandage", "Freedman",
            "Riess")

M: dict[str, dict] = {}


def m(mid, szene, licht, ort, framing, flora="—", **kw):
    M[mid] = dict(szene=szene, licht=licht, ort=ort, framing=framing,
                  flora=flora, **kw)


# Handschrift in Nahaufnahmen. Als Beschreibung formuliert, nicht als
# Verbot: bei Video 1 wurde "keine lesbare Schrift" zweimal zu lesbarer
# Handschrift, die Promptwoerter abschrieb, Tippfehler eingeschlossen.
# Beschrieben wird darum, was auf dem Papier LIEGT — Tintenspur und
# Zeilenrhythmus —, nicht, was fehlen soll.
# NACHGEZOGEN 16.08.2026 nach dem zweiten Stichprobenlauf. Die erste
# Fassung beschrieb "Bögen und Schleifen", "flüssig", "gruppiert zu
# Wortlängen" — Vokabular der Schreibschrift. Das Modell schrieb daraufhin
# echte englische Wörter, darunter genau die Wörter des Prompts: loops,
# word, ink, trace. Dieselbe Falle wie bei Video 1, nur eine Ebene tiefer:
# nicht das Verbot war das Problem, sondern die BESCHREIBUNG, die nach
# Schrift klang.
#
# M68 hat im selben Lauf sauber bestanden. Seine Formulierung nannte keine
# Bögen, keine Schleifen, keine Wortlängen, sondern kurze gleichmäßige
# Striche in Gruppen. Diese Formulierung ist jetzt die Vorlage: die
# Handschrift wird als MARKIERUNG beschrieben, nicht als Schrift.
SCHRIFT = ("auf dem Blatt stehen dichte waagerechte Reihen kurzer, "
           "gleichmäßig geneigter Striche von immer derselben Höhe, in "
           "kleinen Gruppen von drei bis acht Strichen mit schmalen Lücken "
           "dazwischen; alle Striche sind gleich lang, keiner ist "
           "geschwungen, keiner trägt Ober- oder Unterlänge, und keine "
           "Gruppe wiederholt eine andere")

FLORA_STRASSE = ("mitteleuropäische Stadtbäume als dunkle Silhouetten — "
                 "Linden, Ahorn; keine Palmen, keine Nadelwaldkulisse")

# --- Die Strasse des Zuschauers (Klammer) ------------------------------------
m("M01", "Aufsicht von unten in einen Nachthimmel voller Sterne, einer "
         "davon doppelt so breit gezeichnet wie die übrigen; unten die "
         "dunkle Dachkante einer Wohnstraße",
  "sichtbar: die Sterne selbst", "Gegenwart, eine Wohnstraße bei Nacht",
  "ohne", flora=FLORA_STRASSE, ebenen=True)
m("M02", "Eine Person von hinten, klein im Bild, den Kopf in den Nacken "
         "gelegt, vor dem Sternhimmel; um sie herum leerer Straßenraum",
  "sichtbar: die Sterne", "Gegenwart, dieselbe Straße", "ganz",
  flora=FLORA_STRASSE, schutz="Die Klammer — erstes und letztes Bild",
  ebenen=True)
m("M03", "Ein abendlicher Stadtplatz, mehrere Passanten; die meisten heben "
         "die Schultern oder schütteln den Kopf, einer zeigt nach oben in "
         "den Himmel", "sichtbar: eine Straßenlaterne mitten im Bild",
  "Gegenwart, ein Stadtplatz am Abend", "ganz",
  flora="einzelne beschnittene Platanen am Platzrand", ebenen=True)

# --- Der Daumen --------------------------------------------------------------
m("M04", "Nahaufnahme: ein ausgestreckter Arm, der Daumen hochgereckt, "
         "dahinter eine Zimmerwand mit einem Bildhaken; der Daumen sitzt "
         "links vom Haken", "Schatten: hart von links",
  "Gegenwart, ein Wohnzimmer", "teil", paar="M05")
m("M05", "Exakt dieselbe Aufnahme, aber der Daumen sitzt rechts vom "
         "Bildhaken — Ausschnitt und Kameraposition unverändert",
  "Schatten: hart von links", "Gegenwart, dasselbe Zimmer", "teil",
  paar="M04")
m("M06", "Ein Gesicht von der Seite in Nahaufnahme, ein Auge geschlossen, "
         "das offene blickt am hochgereckten Daumen vorbei",
  "Schatten: hart von links", "Gegenwart, dasselbe Zimmer", "teil")

# --- Januar / Juli -----------------------------------------------------------
m("M07", "Dieselbe Wohnstraße im Winter: Schnee auf den Dächern, kahle "
         "Bäume, eine markante Steinplatte im Gehweg vorn im Bild",
  "sichtbar: eine Straßenlaterne", "Gegenwart, dieselbe Straße im Januar",
  "ohne", flora="kahle Linden und Ahorne, Schneedecke", paar="M08")
m("M08", "Exakt derselbe Ausschnitt im Sommer: belaubte Bäume, dieselbe "
         "Steinplatte im Gehweg — Kameraposition unverändert",
  "sichtbar: dieselbe Straßenlaterne", "Gegenwart, dieselbe Straße im Juli",
  "ohne", flora="dieselben Bäume in vollem Laub", paar="M07")
m("M09", "Blick senkrecht nach unten auf zwei Schuhe auf einer Steinplatte "
         "des Gehwegs", "Schatten: hart von links",
  "Gegenwart, dieselbe Straße", "teil")

# --- Der Sprung am Himmel ----------------------------------------------------
m("M10", "Der Nachthimmel über das ganze Bild: ein Stern links, dreimal so "
         "breit gezeichnet wie die kleinen, rechts davon zwei mittelgroße",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne", paar="M11")
m("M11", "Derselbe Himmel, dieselben Sterne an denselben Stellen — nur der "
         "große steht jetzt rechts von den beiden mittelgroßen",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne", paar="M10")

# --- Das eine Diagramm -------------------------------------------------------
m("M12", "Das Parallaxendreieck als Tuschzeichnung auf hellem Papiergrund: "
         "die Sonne als Kreis, die Erdbahn als flache Ellipse, die Erde an "
         "zwei gegenüberliegenden Punkten, von beiden je eine gestrichelte "
         "Sichtlinie zu einem nahen Stern; an der Spitze ein kleiner "
         "gefüllter Kreissektor als Winkelmaß; ferne Sterne als dunkle "
         "Punkte auf dem hellen Grund", "Schema", "zeitlos, reine Zeichnung",
  "ohne", schema=True, schutz="Die Antwort: das Dreieck",
  diagramm="D1, im Stichprobenlauf freigegeben (M06-v2): zwei Standpunkte, "
           "zwei Linien, ein Winkelmaß — ohne Beschriftung lesbar. "
           "Bedingung aus dem Lauf: die Erdkugeln sitzen an den Enden der "
           "Sichtlinien, der nahe Stern deutlich größer als das Feld.")

# --- Koenigsberg -------------------------------------------------------------
m("M13", "Ein klassizistisches Sternwartengebäude mit Kuppel bei Nacht, "
         "davor kahle Bäume und eine gepflasterte Zufahrt",
  "sichtbar: der Mond über der Kuppel", "Königsberg in Ostpreußen, 1838",
  "ohne", flora="norddeutsche Stadtbäume ohne Laub — Linden, Kastanien; "
  "keine Palmen, keine Nadelbäume", ebenen=True)
m("M14", "Nahaufnahme einer runden Objektivlinse, exakt durch die Mitte "
         "durchgesägt; die eine Hälfte ist seitlich verschoben, an ihr "
         "eine feine Messingschraube", "Schatten: hart von rechts",
  "Königsberg in Ostpreußen, 1838", "ohne")
m("M15", "Ein Mann in hochgeschlossenem Rock des frühen 19. Jahrhunderts "
         "sitzt auf einem niedrigen Hocker, den Oberkörper vorgebeugt, den "
         "Kopf gesenkt, das rechte Auge am Okular am unteren Ende eines "
         "einzigen langen Fernrohrs, das von ihm weg nach rechts oben "
         "steigt; die rechte Hand umfasst eine kleine geriffelte "
         "Messingtrommel seitlich am Rohr dicht unter dem Okular, die "
         "linke Hand liegt flach auf dem Knie",
  "sichtbar: eine abgeschirmte Öllampe neben dem Instrument",
  "Königsberg in Ostpreußen, 1838", "ganz", sitzend=True, person=True,
  flora="Innenraum einer Kuppel, Holzdielen, keine Vegetation",
  schutz="Die Schraube — die Titelszene der Antwort")
m("M16", "Blick durch ein Okular: zwei getrennte Abbilder desselben "
         "Sterns nebeneinander im runden Gesichtsfeld",
  "sichtbar: die Sternabbilder im Gesichtsfeld",
  "Königsberg in Ostpreußen, 1838", "ohne", paar="M17")
m("M17", "Dasselbe runde Gesichtsfeld — die beiden Abbilder liegen jetzt "
         "exakt übereinander, ein einziger Punkt",
  "sichtbar: das Sternabbild im Gesichtsfeld",
  "Königsberg in Ostpreußen, 1838", "ohne", paar="M16")
m("M18", "Nahaufnahme der Skala der Mikrometerschraube mit feiner Teilung "
         "und Zeiger, daneben die Öllampe",
  "sichtbar: die Öllampe", "Königsberg in Ostpreußen, 1838", "ohne")

# --- Tycho -------------------------------------------------------------------
m("M19", "Ein aufgeschlagenes gedrucktes Buch des 16. Jahrhunderts auf "
         "einem Lesepult, daneben eine Kerze; die eine Seite trägt eine "
         "kreisförmige Bahnfigur mit konzentrischen Kreisen, die andere "
         "einen gleichmäßigen grauen Satzspiegel aus feinen waagerechten "
         "Strichen — Zeilen aus der Distanz, in denen keine Type "
         "ausgeformt ist",
  "sichtbar: die Kerze", "Frauenburg im Ermland, 1543", "ohne",
  flora="Innenraum, keine Vegetation")
m("M20", "Ein bärtiger Mann in Wams und Halskrause steht an einem großen "
         "Mauerquadranten aus Messing, das Auge an der Visiereinrichtung; "
         "kein Fernrohr im Bild",
  "sichtbar: der Nachthimmel durch eine offene Dachluke",
  "Uraniborg auf der Insel Ven, um 1580", "ganz", person=True,
  flora="Innenraum einer Sternwarte, Backsteinnischen, keine Vegetation")
m("M22", "Die Visiereinrichtung des Quadranten in Nahaufnahme, daneben die "
         "fein geteilte Messingskala mit Zeiger",
  "Schatten: hart von oben rechts", "Uraniborg auf der Insel Ven, um 1580",
  "ohne")
m("M23", "Derselbe Mann sitzt an einem Schreibpult, umgeben von "
         "Messinstrumenten; vor ihm ein beschriebenes Blatt, auf dem die "
         "Feder ruht, " + SCHRIFT, "sichtbar: eine Kerze auf dem Pult",
  "Uraniborg auf der Insel Ven, um 1580", "ganz", sitzend=True,
  person=True, flora="Innenraum, keine Vegetation")
m("M24", "Ein einzelner Stern in großer Nähe, wie ihn ein bloßes Auge "
         "sieht: eine runde weiße Scheibe, darum ein breiterer Ring in "
         "einem helleren Ton — beide hart abgegrenzt und flächig gefüllt",
  "sichtbar: der Stern selbst", "zeitlos, Blick zum Nachthimmel", "ohne",
  paar="M25")
m("M25", "Dieselbe Nahaufnahme desselben Sterns — Scheibe und Ring sind "
         "verschwunden, an ihrer Stelle bleibt ein kleiner harter "
         "Lichtpunkt",
  "sichtbar: der Stern selbst", "zeitlos, Blick zum Nachthimmel", "ohne",
  paar="M24")
m("M26", "Derselbe Mann wendet sich vom Quadranten ab; im Hintergrund eine "
         "ruhende Erdkugel auf einem Sockel",
  "sichtbar: der Nachthimmel durch die Dachluke",
  "Uraniborg auf der Insel Ven, um 1580", "ganz", person=True,
  flora="Innenraum, keine Vegetation")
m("M27", "Ein Fernrohr auf einem Holzstativ, daneben mehrere Männer in "
         "Perücken und Rockschößen, die sich über eine Zeichnung beugen",
  "sichtbar: ein Fenster mit Tageslicht",
  "eine europäische Sternwarte, um 1700", "ganz",
  flora="Innenraum, Stuckdecke, keine Vegetation")

# --- Das Rennen --------------------------------------------------------------
m("M28", "Drei kleine Nachtvignetten nebeneinander in einem Bild: eine "
         "Kuppelsternwarte zwischen kahlen Bäumen, ein weißes flaches "
         "Observatorium vor einem Tafelberg, ein verschneites hölzernes "
         "Observatorium — drei Orte, eine Reihe",
  "sichtbar: über jeder Vignette derselbe Sternhimmel",
  "1830er Jahre: Königsberg, Kap der Guten Hoffnung, Dorpat", "ohne",
  flora="je Vignette die Vegetation ihres Ortes: kahle Linden — Fynbos-"
        "Buschwerk — verschneite Birken")
m("M29", "Ein Sternfeld, darin ein unscheinbarer Doppelstern, dessen "
         "schnelle Eigenbewegung als kurze feine Spur markiert ist",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne")
m("M30", "Eine schnurgerade Landstraße bis zum Horizont, vorn im Bild eine "
         "Zwei-Euro-Münze aufgestellt auf dem Asphalt, am fernen Ende der "
         "Straße ein kaum sichtbarer Punkt",
  "sichtbar: die tief stehende Sonne am Ende der Straße",
  "Gegenwart, eine Landstraße", "ohne",
  flora="Alleebäume beidseits — Pappeln oder Linden")

# --- Das Kap -----------------------------------------------------------------
m("M31", "Ein weißes Sternwartengebäude mit flachem Dach auf einem "
         "Hügelrücken, dahinter ein Tafelberg und das Meer",
  "sichtbar: die tief stehende Sonne über dem Meer",
  "Royal Observatory am Kap der Guten Hoffnung, 1833", "ohne",
  flora="Fynbos des Kaps — silbriges Buschwerk, Proteen, niedrige "
        "Hartlaubsträucher; ausdrücklich keine Palmen, keine Akazien",
  ebenen=True)
m("M32", "Ein Mann in dunklem Rock der 1830er sitzt an einem Pult, ein "
         "beschriebenes Blatt in der Hand, den Blick darauf gesenkt; "
         + SCHRIFT,
  "sichtbar: eine Öllampe auf dem Pult",
  "Kapstadt, 1833", "ganz", sitzend=True, person=True,
  flora="Innenraum, keine Vegetation")
m("M33", "Nahaufnahme: eine Hand legt ein beschriebenes Blatt in eine "
         "offene Schreibtischschublade; das Blatt füllt einen guten Teil "
         "des Bildes, " + SCHRIFT,
  "Schatten: hart von links", "Kapstadt, 1833", "teil", paar="M34")
m("M34", "Dieselbe Schublade, derselbe Ausschnitt — geschlossen, die Hand "
         "ruht flach auf dem Holz",
  "Schatten: hart von links", "Kapstadt, 1833", "teil", paar="M33")

# --- Dorpat ------------------------------------------------------------------
m("M35", "Ein niedriges verputztes Observatorium mit Holzverschalung in "
         "winterlicher Landschaft, Schneedecke, kahle Bäume",
  "sichtbar: der Mond hinter dünnen Wolken", "Dorpat im Baltikum, 1837",
  "ohne", flora="baltische Winterlandschaft — Birken und Kiefern, "
  "Schneedecke", ebenen=True)

# --- Satelliten und die Grenze -----------------------------------------------
m("M36", "Ein weites, dichtes Sternfeld über die ganze Bildfläche, ohne "
         "Vordergrund", "sichtbar: die Sterne", "zeitlos, Blick ins All",
  "ohne")
m("M37", "Ein Satellit mit aufgeklapptem Sonnensegel über der gekrümmten "
         "Erdkante, dahinter Sterne",
  "Schatten: hart von rechts, scharfe Licht-Schatten-Kante am Rumpf; die "
  "Sonne selbst bleibt außerhalb des Bildes",
  "Erdumlaufbahn, um 1990", "ohne", ebenen=True)
m("M38", "Ein kompakter Satellit mit zylindrischem Sonnenschild, weit von "
         "der Erde entfernt vor dem schwarzen All",
  "Schatten: hart von links, scharfe Kante am Sonnenschild; die Sonne "
  "selbst bleibt außerhalb des Bildes",
  "Lagrangepunkt hinter der Erde, 2015", "ohne", ebenen=True)
m("M39", "Der Vollmond über der Wohnstraße, im Vordergrund auf einer "
         "Fensterbank eine Zwei-Euro-Münze, scharf",
  "sichtbar: der Mond", "Gegenwart, dieselbe Straße", "ohne",
  flora=FLORA_STRASSE, ebenen=True)
m("M40", "Eine Spiralgalaxie von schräg oben, die die Bildfläche füllt — "
         "Arme, Staubbänder, dichter Kern",
  "sichtbar: die Galaxie selbst", "zeitlos, Blick ins All", "ohne")
m("M41", "Blick durch ein Okular: auf der einen Seite ein scharfer "
         "Lichtpunkt, auf der anderen ein verwaschener, ausgefranster "
         "Fleck", "sichtbar: die Sterne im Gesichtsfeld",
  "zeitlos, Blick ins All", "ohne")

# --- Die Leiter --------------------------------------------------------------
m("M42", "Die Leiter als flaches Sinnbild auf hellem Papiergrund, in "
         "Seitenansicht: die Holme laufen unten in einem Punkt zusammen "
         "und öffnen sich nach oben, jede Sprosse länger als die darunter; "
         "der unterste Punkt steht exakt auf der Spitze eines breiten "
         "flachen Dreiecks; um das obere Ende kleine dunkle Punkte als "
         "Sterne", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True, paar="M54", schutz="Die Leiter auf dem Dreieck",
  diagramm="D2, im Stichprobenlauf freigegeben (M52-v3): der Keil öffnet "
           "sich nach oben, der Fuß steht Spitze auf Spitze auf dem "
           "Dreieck aus M12 — Sprossenlänge und Rückbindung sind baulich "
           "erzwungen, ohne ein Zeichen Text.")
m("M54", "Dieselbe Leiter, derselbe Ausschnitt — zwei Sprossen sind "
         "durchgebrochen und hängen schief herab",
  "Schema", "zeitlos, reine Zeichnung", "ohne", schema=True, paar="M42",
  diagramm="D2b: Zustand B. Die Wiedererkennung derselben Leiter trägt "
           "den Bruch; ohne Text eindeutig.")
m("M64", "Dieselbe Leiter, intakt — aber die zweite Sprosse von unten ist "
         "sichtbar eine andere: dunkler gefärbt, anders profiliert, neu "
         "eingesetzt", "Schema", "zeitlos, reine Zeichnung", "ohne",
  schema=True,
  diagramm="D2c: der Austausch einer einzigen Sprosse ist als Farb- und "
           "Formabweichung lesbar, ohne Symbolik und ohne Text — die "
           "Kalibrator-Streitfrage als Bild.")

# --- Harvard -----------------------------------------------------------------
m("M43", "Ein langer heller Arbeitsraum; an mehreren Tischen sitzen Frauen "
         "in hochgeschlossenen Blusen über Glasplatten gebeugt; an der Tür "
         "reicht ein Mann im Anzug einen Plattenkasten herein",
  "sichtbar: hohe Sprossenfenster auf der linken Seite",
  "Harvard College Observatory, Massachusetts, 1908 bis 1912", "ganz",
  flora="Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation",
  ebenen=True)
m("M44", "Eine Frau mit im Nacken hochgestecktem Haarknoten, in dunkler "
         "hochgeschlossener Bluse, sitzt allein am Leuchttisch. Ihr Kopf "
         "ist nach vorn und unten geneigt, die Augen blicken senkrecht auf "
         "die Platte hinab — das Gesicht ist von schräg oben zu sehen, "
         "nicht dem Betrachter zugewandt. Die rechte Hand hält eine runde "
         "Lupe am Griff dicht über der Platte, die linke liegt am "
         "Plattenrand; Stapel weiterer Platten um sie herum",
  "sichtbar: der Leuchttisch von unten — das Licht liegt auf Kinn und "
  "Wangen, nicht auf der Stirn",
  "Harvard College Observatory, Massachusetts, um 1910", "ganz",
  sitzend=True, person=True,
  flora="Innenraum, Holzvertäfelung, keine Vegetation",
  schutz="Leavitt am Leuchttisch")
m("M45", "Nahaufnahme: eine Hand hält eine Lupe über eine Glasplatte auf "
         "dem Leuchttisch; unter dem Glas eine unregelmäßige Sternwolke "
         "mit dichtem Kern und ausgefransten Rändern",
  "Durchlicht: die Platte wird von unten durchleuchtet",
  "Harvard College Observatory, Massachusetts, um 1910", "teil")
m("M46", "Ein Sternfeld, in dem einer dreimal so breit gezeichnet ist wie "
         "alle anderen",
  "sichtbar: der Stern selbst", "zeitlos, Blick ins All", "ohne",
  paar="M47")
m("M47", "Dasselbe Sternfeld, derselbe Ausschnitt — der große Stern ist "
         "jetzt so klein gezeichnet wie die übrigen",
  "sichtbar: der Stern selbst", "zeitlos, Blick ins All", "ohne",
  paar="M46")
m("M48", "Nahaufnahme: auf dem Leuchttisch liegt ein handgezeichnetes "
         "Diagrammblatt — Punkte, die sich entlang zweier paralleler "
         "aufsteigender Geraden ordnen, keine Beschriftung; daneben die "
         "Hand mit dem Bleistift",
  "Durchlicht: der Leuchttisch von unten",
  "Harvard College Observatory, Massachusetts, um 1910", "teil",
  paar="M49", schutz="Die Karte — zwei Geraden auf Glas")
m("M49", "Derselbe Ausschnitt, dieselbe Hand mit dem Bleistift — auf dem "
         "Blatt ist die senkrechte Achse jetzt ein blanker Strich ohne "
         "einen einzigen Teilstrich",
  "Durchlicht: der Leuchttisch von unten",
  "Harvard College Observatory, Massachusetts, um 1910", "teil",
  paar="M48")
m("M50", "Ein Feld kleiner Sterne, in dem dreizehn doppelt so breit "
         "gezeichnet sind wie der Rest, weit über die Fläche verstreut",
  "sichtbar: die Sterne", "zeitlos, Blick ins All", "ohne")
m("M51", "Nahaufnahme eines Schriftstücks: unten rechts eine große "
         "geschwungene Unterschrift als eine einzige durchgehende "
         "Tintenschleife mit kräftigem Aufstrich und langem Auslauf, ohne "
         "abgesetzte Zeichen; darüber die angeschnittene erste Zeile des "
         "Blatts als eine Reihe kurzer gleichmäßiger Striche in kleinen "
         "Gruppen, alle von derselben Höhe",
  "Schatten: hart von links oben",
  "Harvard College Observatory, 1912", "ohne")
m("M52", "Ein leerer Schreibtisch am Fenster, darauf ein ungeöffneter "
         "Briefumschlag; der Stuhl leicht zurückgeschoben",
  "sichtbar: das Fenster mit fahlem Tageslicht",
  "Harvard, Massachusetts, 1925", "ohne",
  flora="Innenraum; durch das Fenster kahle Laubbäume Neuenglands",
  ebenen=True)

# --- Die Brueche -------------------------------------------------------------
m("M55", "Ein Mann in Tweedjacke sitzt am Okular eines sehr großen "
         "Spiegelteleskops in einer Kuppel, Stahlfachwerk über ihm",
  "sichtbar: der Nachthimmel durch den offenen Kuppelspalt",
  "Mount-Wilson-Observatorium, Kalifornien, 1929", "ganz", sitzend=True,
  person=True, flora="Innenraum einer Kuppel, keine Vegetation",
  ebenen=True)
m("M56", "Ein Feld kleiner Spiralgalaxien, verstreut über die ganze "
         "Bildfläche, verschieden groß",
  "sichtbar: die Galaxien selbst", "zeitlos, Blick ins All", "ohne")
m("M58", "Zwei pulsierende Sterne nebeneinander in einem Sternfeld, der "
         "eine groß und gelblich, der andere kleiner und bläulich",
  "sichtbar: die Sterne selbst", "zeitlos, Blick ins All", "ohne")
m("M59", "Ein Saal mit Reihenbestuhlung, vorn ein Mann am Rednerpult vor "
         "einer hellen Projektionsfläche, die Zuhörer beugen sich vor",
  "sichtbar: der Projektionsstrahl von hinten",
  "Rom, Tagung der Internationalen Astronomischen Union, 1952", "ganz",
  person=True, flora="Innenraum, Marmorpilaster, keine Vegetation",
  ebenen=True)
m("M60", "Nahaufnahme einer Fotoplatte: ein scharfer heller Punkt, direkt "
         "daneben ein weicher leuchtender Fleck etwa gleicher Helligkeit",
  "Durchlicht: die Platte wird von hinten durchleuchtet",
  "Kalifornien, 1958", "ohne")
m("M61", "Ein kleiner dichter Sternhaufen aus wenigen großen weißen "
         "Sternen, von einem dünnen blassen Nebelschleier umgeben, über "
         "Baumsilhouetten am Nachthimmel",
  "sichtbar: die Sterne des Haufens", "Gegenwart, Blick vom Boden",
  "ohne", flora="mitteleuropäische Laubbäume als Silhouette", ebenen=True)
m("M62", "Mehrere große Parabolantennen auf freiem Feld, alle in dieselbe "
         "Richtung geneigt, lange Schatten über den Boden",
  "Schatten: hart von rechts",
  "Gegenwart, ein Antennenfeld im Hochland des amerikanischen Südwestens",
  "ohne", flora="trockenes Steppengras, niedrige Beifußbüsche, ferne "
  "kahle Bergrücken; keine Bäume, keine Kakteen", ebenen=True)

# --- Der offene Streit -------------------------------------------------------
m("M63", "Ein feinkörniges Fleckenmuster über die ganze Bildfläche, davor "
         "klein ein Satellit im Profil",
  "sichtbar: das Muster leuchtet selbst", "Lagrangepunkt, 2013", "ohne",
  ebenen=True)
m("M65", "Zwei Spiralgalaxien nebeneinander vor dunklem Grund, etwa "
         "gleich groß", "sichtbar: die Galaxien selbst",
  "zeitlos, Blick ins All", "ohne")
m("M66", "Nahaufnahme: zwei Hände am Fuß einer soliden Holzleiter, die "
         "eine hält einen einzelnen Nagel, die andere greift danach",
  "Schatten: hart von links", "zeitlos, sinnbildlich", "teil")
m("M67", "Ein Sternfeld, in dem mehrere deutlich rötliche, aufgeblähte "
         "Sterne zwischen weißen Punkten stehen",
  "sichtbar: die Sterne selbst", "zeitlos, Blick ins All", "ohne")
m("M69", "Ein Galaxienfeld; am Rand einer der Galaxien sitzt ein einzelner "
         "weißer Punkt, größer und weißer gezeichnet als ihr Zentrum",
  "sichtbar: der aufleuchtende Stern selbst", "zeitlos, Blick ins All",
  "ohne")

# --- Der Schluss -------------------------------------------------------------
m("M68", "Nahaufnahme: eine Hand notiert mit Bleistift auf einem Blatt "
         "neben einer Messreihe eine zweite, kürzere Spalte; beide Spalten "
         "bestehen aus kurzen gleichmäßigen Bleistiftstrichen "
         "untereinander, in sauberen Zeilen ausgerichtet, jede Eintragung "
         "eine kleine Gruppe von Strichen ohne ausgeformte Ziffer",
  "Durchlicht: der Leuchttisch von unten",
  "Harvard College Observatory, um 1910", "teil")

# ------------------------------------------------------------ Einstellungen --
FAHRTEN = {"Zoom rein", "Zoom raus", "Schwenk links", "Schwenk rechts",
           "statisch"}
E: list[tuple[str, str, str]] = [
 # Absatz 1
 ("You're outside, and it's dark. Look up. Pick a star. Any one you like.", "M01", "Zoom rein"),
 ("Now answer me: how far away is your star?", "M02", "Zoom raus"),
 # Absatz 2
 ("Nothing comes. You're not alone in that.", "M02", "statisch"),
 ("More than three thousand people got the same question.", "M03", "Zoom raus"),
 ("One in four put the stars closer to us than the Sun.", "M03", "Schwenk rechts"),
 ("Five out of six students wouldn't put a number on the nearest one at all.", "M03", "Zoom rein"),
 ("Of those who tried, one in five landed in the right range. About three people in a hundred.", "M03", "Schwenk links"),
 # Absatz 3
 ("So there you stand in the street with no answer.", "M02", "Zoom rein"),
 ("What you need is a triangle. Here is how you build yours.", "M12", "Zoom rein"),
 # Absatz 4
 ("Put your thumb up, arm straight out, and shut your left eye.", "M04", "statisch"),
 ("Now swap eyes. Your thumb jumped. The wall stayed where it was.", "M05", "statisch"),
 ("Your two eyes sit apart. Each one looks past your thumb from its own spot. Two spots, one jump.", "M06", "Zoom rein"),
 # Absatz 5
 ("Now you need two spots much further apart. Stand in this street in January.", "M07", "Zoom raus"),
 ("Come back in July and stand on the same flagstone.", "M08", "statisch"),
 ("You never lifted a foot. And you have moved three hundred million kilometres.", "M09", "Zoom rein"),
 ("Your planet carried you.", "M09", "statisch"),
 ("Photograph a near star from both ends of your ride, and it jumps.", "M10", "statisch"),
 ("Same as your thumb did.", "M11", "statisch"),
 # Absatz 6
 ("A man in Königsberg spent two years catching that jump.", "M13", "Zoom rein"),
 ("The same trick you just played against your wall, done properly.", "M15", "Zoom rein"),
 ("His telescope had its main lens sawn clean in half. One half slid on a fine screw.", "M14", "Zoom rein"),
 ("Night after night he turned the screw until two images of one faint star", "M16", "statisch"),
 ("lay exactly on top of each other.", "M17", "statisch"),
 ("Then he read the screw off by lamplight. That reading was the jump.", "M18", "Zoom rein"),
 ("Half of it, drawn as an angle, is what you were after: the parallax.", "M12", "Zoom rein"),
 ("Small jump, far star. That is the whole rule, and now you have it too.", "M12", "Zoom raus"),
 # Absatz 7
 ("One catch. Between idea and lamplit reading lie two hundred and ninety-five years.", "M18", "statisch"),
 # Absatz 8
 ("In 1543 a book set the Earth moving. The objection came at once.", "M19", "Zoom rein"),
 ("If you ride a moving platform, the stars should sway.", "M11", "Zoom rein"),
 ("Nobody saw any sway.", "M10", "statisch"),
 ("The sharpest eyes of the century belonged to a Danish noble.", "M20", "Zoom rein"),
 ("Stand beside him at his quadrant — brass, taller than you.", "M22", "Zoom rein"),
 ("No telescope. He charted the whole sky with his bare eye, finer than anyone alive.", "M20", "Zoom raus"),
 ("He hunted your sway for years — your thumb-jump, up there — and never found it.", "M10", "Zoom raus"),
 ("So he did the maths on that nothing. To hide from his instruments,", "M23", "Zoom rein"),
 ("the stars would have to sit seven hundred times farther out than Saturn.", "M23", "statisch"),
 ("To his eye — to yours too — every bright star shows a small round disk.", "M24", "Zoom rein"),
 ("Push a disk that wide out that far: a star of monstrous size, dwarfing the Sun.", "M24", "Zoom rein"),
 ("Too absurd, he ruled. The Earth stands still. His logic was sound. His premise was not.", "M26", "Zoom raus"),
 ("The disks are not real. Air and your own eye wrap every point of light in blur.", "M25", "Zoom rein"),
 ("The blur is what he measured.", "M25", "statisch"),
 ("The largest true star disk in your night sky is about a thousand times smaller than the disk he drew.", "M24", "statisch"),
 ("It took until around 1700 to call them an illusion.", "M27", "Zoom rein"),
 ("An \"optick fallacy,\" as it was put back then.", "M27", "statisch"),
 ("He wasn't sloppy. He measured what your eye can see. It just isn't the star.", "M06", "Zoom rein"),
 # Absatz 9
 ("The hunt ran on. By the 1830s it was a race.", "M28", "Zoom raus"),
 ("Three men, three cities, three stars — and you have met the first.", "M28", "Schwenk rechts"),
 # Absatz 10
 ("The man in Königsberg had aimed your trick at a dim star called 61 Cygni.", "M29", "Zoom rein"),
 ("It crawls across the sky unusually fast.", "M29", "statisch"),
 ("An Italian had spotted that hurry in 1792. A fast star is usually a near one.", "M29", "Schwenk rechts"),
 ("Through 1837 and 1838 he measured. Then he published: a jump of about a third of an arcsecond.", "M15", "Zoom raus"),
 ("An arcsecond: take one degree. Cut it into three thousand six hundred slices. Keep one.", "M18", "Zoom rein"),
 ("His angle is a two-euro coin seen from seventeen kilometres.", "M30", "Zoom raus"),
 ("From it he got ten point four light-years. A light-year is the stretch light crosses in one year.", "M10", "Zoom raus"),
 ("Nine and a half trillion kilometres.", "M10", "statisch"),
 ("Today's value for that star: eleven point four. He came within a tenth of the truth.", "M15", "statisch"),
 ("With a saw, a screw, and your thumb trick.", "M14", "statisch"),
 # Absatz 11
 ("But he wasn't first to measure. Go five years back, to the Cape of Good Hope.", "M31", "Zoom rein"),
 ("A man there catches the jump of a bright southern star, Alpha Centauri.", "M32", "Zoom rein"),
 ("He does his sums — and puts the sheet in a drawer.", "M33", "Zoom rein"),
 ("Earlier claims had been shot down. The story handed down says he didn't trust his own numbers.", "M32", "Zoom rein"),
 ("He shut the drawer on your answer. He published in 1839 — second, for want of nerve.", "M34", "Zoom rein"),
 # Absatz 12
 ("And in Dorpat, a third man had measured Vega. He landed close: 0.125 arcseconds, against the modern 0.129.", "M35", "Zoom rein"),
 ("Then Königsberg doubted those numbers. The man in Dorpat revised his good value to nearly double. Away from the truth.", "M35", "statisch"),
 ("So who was first? Pick your rule. First to measure: the Cape.", "M28", "Zoom rein"),
 ("First to make the full case in print: Königsberg.", "M28", "Schwenk links"),
 ("First to print any number at all: arguably Dorpat.", "M28", "Schwenk rechts"),
 ("The books give all three answers — side by side.", "M28", "Zoom raus"),
 # Absatz 13
 ("You'd think the flood starts there. It doesn't.", "M28", "statisch"),
 ("By 1900 — sixty years on — the world's whole haul: about sixty parallaxes.", "M36", "Zoom raus"),
 ("Sixty known distances, in your galaxy of billions.", "M36", "statisch"),
 ("The flood came when the measuring left the ground.", "M37", "Zoom rein"),
 ("A satellite called Hipparcos pinned down 118,000 stars in the 1990s.", "M37", "Schwenk rechts"),
 ("Only about one in six had an error under ten percent.", "M37", "statisch"),
 ("Then came Gaia, a European craft. From 2013 to 2025 it scanned the sky and measured more than a billion stars.", "M38", "Zoom rein"),
 ("At its sharpest — on paper — it reads your two-euro coin from 759,000 kilometres. Twice as far as the Moon.", "M39", "Zoom raus"),
 ("And still your triangle runs out inside your own galaxy.", "M40", "Zoom raus"),
 ("The Milky Way spans some 87,000 light-years, give or take a few thousand.", "M40", "Schwenk rechts"),
 ("For most stars, Gaia's sharp reach covers a slice of that.", "M40", "Zoom rein"),
 ("Build a bigger telescope. The base of your triangle has not grown a metre.", "M38", "Zoom raus"),
 ("Past a point, the jump is smaller than the blur.", "M41", "Zoom rein"),
 # Absatz 14
 ("Everything farther — every other galaxy, the deep sky — stands on something else. A ladder.", "M42", "Zoom raus"),
 ("Its second rung was built by a woman paid thirty cents an hour.", "M42", "Zoom rein"),
 # Absatz 15
 ("Step into a long bright workroom. Harvard, 1908 to 1912.", "M43", "Zoom rein"),
 ("At the tables sit women, bent over the sky on glass.", "M43", "Schwenk rechts"),
 ("The plates come from the men who run the telescopes. The women measure them.", "M43", "Schwenk links"),
 ("Stop at one table. Under her magnifier lies the Small Magellanic Cloud, a companion galaxy of ours.", "M45", "Zoom rein"),
 ("Plate after plate, she finds stars that pulse. They brighten, fade, and brighten again.", "M46", "statisch"),
 ("A steady beat of days or weeks.", "M47", "statisch"),
 ("We now call them Cepheids.", "M46", "statisch"),
 ("She works through twenty-five of them. And the pattern rises out of the glass in front of you.", "M44", "Zoom rein"),
 ("The slower the beat, the brighter the star.", "M44", "statisch"),
 ("On her chart, the points fall along two clean straight lines.", "M48", "Zoom rein"),
 ("She writes down, herself, what it means.", "M48", "statisch"),
 ("These stars all sit at roughly the same distance from us — they share the Cloud.", "M45", "statisch"),
 ("So the beat apparently tracks how much light a star truly puts out.", "M44", "Zoom rein"),
 # Absatz 16
 ("Hold on to what she wrote. It unlocks the deep universe for you.", "M48", "Zoom rein"),
 ("Read a Cepheid's rhythm, and you know its true brightness.", "M46", "statisch"),
 ("See how faint it looks, and the dimming hands you the distance. Hers you could read across millions of light-years.", "M47", "statisch"),
 # Absatz 17
 ("One catch — and she named it too. Her chart had no scale.", "M49", "Zoom rein"),
 ("Nobody knew the distance to the Cloud itself, so her law gave only ratios.", "M45", "Zoom raus"),
 ("This star is four times farther than that one. Four times what?", "M10", "statisch"),
 ("She wrote that she hoped parallaxes would be measured for a few stars of this kind.", "M44", "Zoom raus"),
 ("A year on, an astronomer found a rough scale. No clean triangle — the slow drift of thirteen nearby Cepheids, pooled.", "M50", "Zoom raus"),
 # Absatz 18
 ("Her paper went out under her director's signature. Her name survives in the first line: \"prepared by Miss Leavitt\".", "M51", "Zoom rein"),
 ("In 1925, a Swedish mathematician wrote to her about putting her name up for the Nobel Prize.", "M52", "Zoom rein"),
 ("He did not know she had been dead for four years.", "M52", "statisch"),
 # Absatz 19
 ("Mark the shape of what you now own. Your triangle is the bottom rung.", "M42", "Zoom rein"),
 ("The Cepheids stand on the triangle.", "M42", "statisch"),
 ("The rungs above — exploding stars, whole galaxies — stand on the Cepheids.", "M42", "Zoom rein"),
 ("Every rung inherits the reach of the one below — and its errors.", "M42", "Zoom raus"),
 # Absatz 20
 ("And the errors came. Your ladder has snapped twice.", "M54", "statisch"),
 # Absatz 21
 ("First break.", "M54", "statisch"),
 ("In 1929, a man at a great telescope in California used Cepheid distances to show the galaxies flee from us.", "M55", "Zoom rein"),
 ("The farther, the faster. The universe expands. Run that film backwards, and you get an age.", "M56", "Zoom raus"),
 ("His rate gave: not quite two billion years. Awkward, even then.", "M55", "statisch"),
 ("The geologists put the Earth itself at around two billion.", "M09", "statisch"),
 ("By the mid-fifties it turned absurd. The Earth's true age came in at four and a half billion.", "M02", "Zoom raus"),
 ("Run those numbers, and you are standing on a planet older than the universe around it.", "M02", "Zoom rein"),
 ("Part of the fault lay on Leavitt's rung. There are two families of pulsing stars, with two different rulers.", "M58", "Zoom rein"),
 ("Mixing them had shrunk the cosmos.", "M58", "statisch"),
 ("In 1952, in a hall in Rome, a man stood up and pulled the families apart.", "M59", "Zoom rein"),
 ("At a stroke, the universe doubled. Still too small.", "M59", "Zoom raus"),
 ("In 1958, another astronomer found: the California man had also mistaken glowing gas clouds for bright stars.", "M60", "Zoom rein"),
 ("The rate fell again, and the universe came out comfortably older than the Earth.", "M56", "Zoom raus"),
 ("Total correction, first to last: about a factor of seven.", "M60", "statisch"),
 # Absatz 22
 ("Second break, closer to home. The Pleiades — the little cluster you can spot with your bare eyes.", "M61", "Zoom rein"),
 ("Hipparcos, the trusted satellite, put it at about 390 light-years.", "M37", "statisch"),
 ("Nearly every other method said 435 to 445. For seventeen years, the field's best instrument disagreed with everyone else.", "M61", "statisch"),
 ("About one of the nearest clusters in your sky.", "M61", "Zoom raus"),
 ("In 2014, radio telescopes settled it: 444 light-years, give or take four. The satellite was wrong.", "M62", "Schwenk rechts"),
 # Absatz 23
 ("And today your ladder is in its third fight — this one still open.", "M42", "statisch"),
 ("Two teams, two numbers for how fast the universe grows.", "M65", "Zoom raus"),
 ("One number comes from the oldest light there is.", "M63", "Zoom rein"),
 ("A satellite called Planck reads 67.4, with an error of half a point.", "M63", "statisch"),
 ("The other comes off your ladder. Parallax, to Cepheids, to exploding stars that all flare to nearly the same true brightness.", "M69", "Zoom rein"),
 ("The ladder team, called SH0ES, reads 73.0, plus or minus one.", "M69", "statisch"),
 ("A five-sigma difference, in their own words: far too large to be chance.", "M63", "Zoom raus"),
 ("You'll hear that sold as the early universe against today's. Watch what that framing skips.", "M56", "statisch"),
 ("A second team climbed the same ladder with a different second rung.", "M64", "Zoom rein"),
 ("Red giant stars instead of Cepheids, the new James Webb telescope in the mix.", "M67", "Zoom rein"),
 ("They read 67.8 to 70.4, depending on the sample and the method.", "M64", "statisch"),
 ("Their own verdict: no new physics needed.", "M64", "statisch"),
 ("Strangest of all: both teams agree on the distances to the very same galaxies. To about one percent.", "M65", "Zoom rein"),
 ("The stars are not the quarrel. The quarrel is over which exploding stars to hang the scale on.", "M65", "statisch"),
 ("The ladder holds. The fight is about the nail.", "M66", "Zoom rein"),
 ("Nobody yet knows which side is right.", "M66", "statisch"),
 # Absatz 24
 ("Go back out to your street and find your star. How far away is it?", "M02", "Zoom raus"),
 ("For the near ones: your triangle. The thumb trick, stretched across your planet's orbit.", "M12", "Zoom raus"),
 ("Sharpened until a coin past the Moon is an easy target.", "M39", "statisch"),
 ("For the far ones: the ladder. A rhythm read off glass plates at thirty cents an hour.", "M48", "Zoom raus"),
 ("Nailed to your triangle. Broken twice, patched twice, fought over right now.", "M54", "statisch"),
 ("One in four of the people asked still hangs the stars closer than the Sun.", "M03", "Zoom raus"),
 ("The nearest one sits so deep that its light spends four years on the road to your eye.", "M01", "Zoom rein"),
 ("But that number is no guess. It never was. Someone caught its jump. Someone read its beat.", "M68", "Zoom rein"),
 ("And beside every distance, someone wrote a second number. How far off it might be.", "M68", "statisch"),
 ("That second number is the honest answer.", "M68", "statisch"),
 ("You don't just know how far your star is.", "M02", "Zoom raus"),
 ("You know how well you know it — and exactly where you don't.", "M02", "Zoom rein"),
]

BILD_2K = 2.0
CLIP_4S = 12.0
EURO_ULTRA = 0.033
EURO_NACHKAUF = 0.049
KOSTEN_STAND = "2026-08-16"


def absatz_je_einstellung(rein: str, zeilen: list[dict]) -> list[int]:
    grenzen, n = [], 0
    for abs_ in [a for a in rein.split("\n\n") if a.strip()]:
        n += len(abs_.split())
        grenzen.append(n)
    out, w = [], 0
    for z in zeilen:
        out.append(next(i for i, g in enumerate(grenzen, 1) if w < g))
        w += z["woerter"]
    return out


def schreibe_md(zeilen: list[dict], rein: str, kum: float) -> None:
    ab = absatz_je_einstellung(rein, zeilen)
    schema = [k for k, v in M.items() if v.get("schema")]
    welt = [k for k, v in M.items() if not v.get("schema")]
    eb = [k for k, v in M.items() if v.get("ebenen")]
    schutz = [k for k, v in M.items() if v.get("schutz")]
    pers = [k for k, v in M.items() if v.get("person")]
    sitz = [k for k, v in M.items() if v.get("sitzend")]
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
        return f"{x:.{n}f}".replace(".", ",")

    def mmss(x: float) -> str:
        return f"{int(x//60)}:{x%60:04.1f}".replace(".", ",")

    def eur(c: float) -> str:
        return z2(c * EURO_ULTRA) + " | " + z2(c * EURO_NACHKAUF)

    def kurz(t: str, n: int = 84) -> str:
        t = " ".join(t.split())
        return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"

    L: list[str] = []
    w = L.append
    w("# Szenenliste — Video 2, „How Do We Know How Far Away the Stars Are?"
      "\"\n")
    w("> **Zweite Fassung, 16.08.2026 — neu gebaut für die Erzählfassung "
      "des Skripts.**\n"
      "> Die erste Fassung (Erklärform, 58 % Schema-Laufzeit) liegt in der\n"
      "> Git-Historie. Erzeugt aus `szenenplan.py`, nicht getippt: der\n"
      "> Wortlaut jeder Einstellung wird gegen `skript.md` geprüft, jedes\n"
      "> Motiv hat Pflichtfelder, und der Generator bricht ab, wenn der\n"
      "> Schema-Anteil 10 % der Laufzeit übersteigt.\n"
      "> **0 Credits verbraucht**; Preise per `get_cost`-Preflight am "
      f"{KOSTEN_STAND}.\n")

    w("## Wie zu lesen\n")
    w("- **Motiv** = ein zu generierendes Bild; mehrere Einstellungen "
      "teilen sich eines über Kamerafahrten.\n"
      "- **Licht**: `sichtbar:` (Quelle im Bild), `Schatten:` (gerichtet, "
      "Quelle außen), `Durchlicht:`.\n"
      "- **Framing**: `ganz` · `ohne` · `teil`; sitzende Figuren nutzen "
      "`FRAMING_SITZEND` aus `bildplan.py`.\n"
      "- **Zustandspaar** = zwei Bilder derselben Komposition; nur auf "
      "ihnen (oder demselben Motiv) darf ein Schnitt unter 2,4 s liegen.\n"
      "- **Schema** = Zeichnung auf hellem Papiergrund nach der Grundregel "
      "vom 16.08. — hier nur noch **vier Motive**: das Dreieck und die "
      "Leiter in drei Zuständen, beide Formen im Stichprobenlauf "
      "freigegeben.\n")

    w("## Stilbindung\n")
    w("V2-Machart, erwachsene Figuren, Z3-Licht; kein Türkis, natürliche "
      "Farben; Schemata auf hellem neutralem Grund (Sterne dort als dunkle "
      "Punkte); kein Text im Bild. Handschrift in den Dokument-Nahaufnahmen "
      "(M19, M23, M32, M33, M51, M68) ist als **Tintenspur und "
      "Zeilenrhythmus beschrieben**, nicht als Verbot — bei Video 1 wurde "
      "aus „keine lesbare Schrift“ zweimal lesbare Handschrift, die "
      "Promptwörter abschrieb. Versalien-Prüfung über `pruefe_szene()`. "
      "Historische "
      "Personen als Epochenfiguren ohne Portraitähnlichkeit; kein "
      "Personenname im Bildtext (geprüft).\n")

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
    for k, v in M.items():
        marken = []
        if v.get("schema"):
            marken.append("Schema")
        if v.get("person"):
            marken.append("Epochenfigur")
        if v.get("sitzend"):
            marken.append("sitzend")
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
    w(f"| unter 3 s | {sum(1 for x in d if x < 3)} — jede auf demselben "
      "Motiv wie die Einstellung davor oder auf dessen Paarpartner |")
    w(f"| über 5 s | {sum(1 for x in d if x > 5)}, davon über 6 s: "
      f"{sum(1 for x in d if x > LANG_AB)} |")
    w(f"| **Motive (zu generierende Bilder)** | **{len(M)}** |")
    w(f"| Einstellungen je Motiv | {z2(len(zeilen)/len(M))} im Mittel |")
    w(f"| Mehrfach genutzte Motive | {sum(1 for k in M if sum(1 for z in zeilen if z['motiv']==k)>1)}"
      f" → **{len(zeilen)-len(M)} Bilder gespart** |")
    w(f"| **Schema-Anteil** | {len(schema)} Motive · {s_ein} Einstellungen "
      f"· **{z2(s_zeit/kum*100,1)} % der Laufzeit** (Vorgabe ≤ 10 %; "
      "Erklärform: 58 %, Video 1: 26 %) |")
    w(f"| Weltbilder | {len(welt)} — Framing ganz {wfr['ganz']} · "
      f"ohne {wfr['ohne']} · teil {wfr['teil']} |")
    w(f"| Zustandspaare | {len(paare)} |")
    w(f"| Motive mit getrennten Ebenen | {len(eb)} |")
    w(f"| Epochenfiguren | {len(pers)} · davon sitzend {len(sitz)} |")
    w(f"| Einstellungen mit Figur oder Körperteil | {fig} "
      f"({fig/len(zeilen)*100:.0f} %) |")
    w("")

    w("## Kosten\n")
    w(f"Preise per `get_cost` am {KOSTEN_STAND}: Standbild "
      f"`nano_banana_2` 16:9 2k = {z2(BILD_2K,1)} Credits, Clip Seedance "
      f"1.5 Pro 1080p 4 s = {CLIP_4S:.0f} Credits.\n")
    w("| Variante | Credits | € Ultra | € Nachkauf |")
    w("|---|---:|---:|---:|")
    w(f"| **A — alle Motive als Standbild, ffmpeg bewegt** | **{A:.0f}** | {eur(A)} |")
    w(f"| **B — A plus getrennte Ebenen** | **{B:.0f}** | {eur(B)} |")
    w(f"| **C — B plus {len(schutz)} echte Clips für die geschützten "
      f"Momente** | **{C:.0f}** | {eur(C)} |")
    w(f"| zum Vergleich: alle {len(zeilen)} Einstellungen als Clip | "
      f"{ALLES:.0f} | {eur(ALLES)} |")
    w("")
    w("Ultra: 3.000 Credits/Monat für 99 €/Monat bei Jahreszahlung = "
      "0,033 €/Credit; Nachkauf 0,049 €/Credit. **Variante C bleibt unter "
      "der Abbruchschwelle von 500 Credits.**\n")

    w("## Was diese Fassung nicht leistet\n")
    w("- **Die Dokument-Nahaufnahmen sind das neue Risiko.** Sechs Motive "
      "zeigen beschriebenes Papier. Die Schrift ist als Tintenspur "
      "beschrieben statt verboten — die Lehre aus Video 1, wo ein Verbot "
      "ignoriert wurde und die Handschrift Promptwörter abschrieb. Ob die "
      "Beschreibung trägt, ist der Kern des nächsten Stichprobenlaufs.\n"
      "- **M28 (Triptychon) ist kompositorisch unerprobt** — drei Vignetten "
      "in einem Bild gab es in Video 1 nicht.\n"
      "- **M44 verlangt Licht von unten am Gesicht.** Der erste "
      "Stichprobenlauf hat genau das ignoriert; die Formulierung nennt "
      "jetzt Kinn und Wangen, aber verifiziert ist sie nicht.\n"
      "- Die Dauern rechnen mit 219 WPM; beim Schnitt ersetzen die echten "
      "ElevenLabs-Zeichenzeiten sie.\n")

    w("## Anschluss\n")
    w("1. Stichprobenlauf über die neuen Risikofälle: M28, M33, M44, M51 "
      "— die Schemata sind schon freigegeben.\n"
      "2. Bei Freigabe: alle Motive in Stapeln, dann die "
      f"{len(eb)} zweiten Ebenen, zuletzt die {len(schutz)} Clips.\n"
      "3. `szenenplan.json` liefert `montage.py` Wortlaut, Motiv und "
      "Fahrt je Einstellung.\n")

    (HIER / "szenen.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main() -> None:
    t = (HIER / "skript.md").read_text(encoding="utf-8")
    mm = re.search(r"^## Sprechtext\s*\n(.*?)^---\s*$", t, re.S | re.M)
    rein = re.sub(r"\s*\[(?:[WLA]\d*|A)\]", "", mm.group(1).strip())
    ziel = " ".join(rein.split())

    # 1. Textkachelung
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

    # 2. Pflichtfelder, Licht, Namen, Versalien
    for mid, d in M.items():
        for feld in ("szene", "licht", "ort", "framing", "flora"):
            if not d.get(feld):
                raise SystemExit(f"{mid}: Feld {feld} fehlt")
        if d["framing"] not in ("ganz", "ohne", "teil"):
            raise SystemExit(f"{mid}: Framing {d['framing']!r} unbekannt")
        for n in PERSONEN:
            if n in d["szene"]:
                raise SystemExit(f"{mid}: Bildtext nennt {n}")
        pruefe_szene(mid, d["szene"])
        if d.get("schema") and not d["licht"].startswith("Schema"):
            raise SystemExit(f"{mid}: Schema, aber Licht {d['licht']!r}")
        if not d.get("schema"):
            if not d["licht"].startswith(("sichtbar:", "Schatten:",
                                          "Durchlicht:")):
                raise SystemExit(f"{mid}: Licht {d['licht']!r} unzulaessig")
            if (d["licht"].startswith("sichtbar:")
                    and "außerhalb" in d["licht"]):
                raise SystemExit(f"{mid}: Quelle sichtbar deklariert, aber "
                                 "außerhalb des Bildes")
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
        wz = len(txt.split())
        dauer = wz / WPM * 60
        zeilen.append(dict(nr=nr, text=txt, motiv=mid, fahrt=fahrt,
                           woerter=wz, start=kum, dauer=dauer))
        kum += dauer

    # 4. Schnittrhythmus
    kurz_fehl = []
    for i, z in enumerate(zeilen):
        if z["dauer"] >= KURZ_AB:
            continue
        vor = zeilen[i - 1]["motiv"] if i else None
        if vor == z["motiv"] or M[z["motiv"]].get("paar") == vor:
            continue
        kurz_fehl.append(f'{z["nr"]} {z["dauer"]:.1f}s {z["motiv"]} '
                         f'(davor {vor}) {z["text"][:52]!r}')
    lang = [f'{z["nr"]} {z["dauer"]:.1f}s {z["motiv"]} {z["text"][:52]!r}'
            for z in zeilen if z["dauer"] > LANG_AB]
    if kurz_fehl or lang:
        for x in kurz_fehl:
            print("ZU KURZ, ohne Vorbild:", x)
        for x in lang:
            print("ZU LANG:", x)
        raise SystemExit(f"Schnittrhythmus: {len(kurz_fehl)} zu kurz, "
                         f"{len(lang)} zu lang")

    # 5. Schema-Anteil — die Bildvorgabe der Erzaehlfassung, hart.
    s_zeit = sum(z["dauer"] for z in zeilen if M[z["motiv"]].get("schema"))
    if s_zeit / kum > SCHEMA_MAX:
        for z in zeilen:
            if M[z["motiv"]].get("schema"):
                print(f'SCHEMA {z["nr"]:3d} {z["dauer"]:4.1f}s {z["motiv"]} '
                      f'{z["text"][:60]!r}')
        raise SystemExit(f"Schema-Anteil {s_zeit/kum*100:.1f} % > "
                         f"{SCHEMA_MAX*100:.0f} %")

    (HIER / "szenenplan.json").write_text(
        json.dumps({"einstellungen": zeilen, "motive": M}, indent=1,
                   ensure_ascii=False), encoding="utf-8")

    d = [z["dauer"] for z in zeilen]
    schema = [k for k, v in M.items() if v.get("schema")]
    print(f"Einstellungen {len(E)} · Motive {len(M)} · Laufzeit "
          f"{int(kum//60)}:{kum%60:04.1f}")
    print(f"Dauer Mittel {sum(d)/len(d):.2f} s · Spanne {min(d):.1f}–"
          f"{max(d):.1f} s · unter 3 s: {sum(1 for x in d if x < 3)} · "
          f"über 5 s: {sum(1 for x in d if x > 5)}")
    print(f"Schema: {len(schema)} Motive · {s_zeit/kum*100:.1f} % der "
          f"Laufzeit (Schranke {SCHEMA_MAX*100:.0f} %)")
    print(f"Mehrfach genutzte Motive → {len(E)-len(M)} Bilder gespart")

    schreibe_md(zeilen, rein, kum)
    print("szenen.md geschrieben")


if __name__ == "__main__":
    main()
