# Upload-Paket — Video 1

> **Hochladen von Hand.** `produktion/config.md` hält fest: kein Upload-Zugang
> im Repository, damit beim Hochladen die **KI-Kennzeichnung** gesetzt wird.
> Diese Datei liefert die Textbausteine, nicht den Upload.

## Titel

**Who Built the First Roads and Why?**

Der Titel steht so im Skript und in der Szenenliste und ist die Frage, die das
Video im ersten Absatz stellt und im letzten beantwortet. Er bleibt unverändert.

### Sollte ein anderer Titel getestet werden

Der Kanal hat keine gemessene Titel-Regel — `config.md` führt Thumbnail- und
Titelstil ausdrücklich als **nicht gemessen**. Alternativen wären also geraten,
nicht hergeleitet. Ich schlage deshalb keine vor.

## Beschreibung

```
Roads are older than the wheel. In one German bog, by about two thousand years.

Ask who built the first roads and most people reach for the Romans, or traders,
or wait for someone to invent the wheel. All three are wrong. The earliest road
builders we can name weren't fighting distance — they were fighting water.

This video follows them: a plank walkway laid across a Somerset marsh in
3807 BC, a layered bog road in Lower Saxony built with stone axes, a paved
haul road in the Egyptian desert, a processional street in Babylon, a post road
across Persia, dead-straight roads in a canyon where nothing ever rolled, and
an Andean network that turns into a staircase where the land climbs.

Rome comes last. Its first great road was military, not commercial.

00:00  Roads are older than you think
00:33  Standing in a bog
00:54  The Sweet Track, 3807 BC
01:13  Oak planks, stone axes, no nails
01:54  A plank line — and an older one beneath it
02:15  550 wooden paths in Lower Saxony
03:11  Why there, why then
03:50  The thing that had no business being there
04:26  So what were roads for?
04:38  Egypt: a road that served a building site
05:25  Babylon: a street built as a stage
06:07  Persia: a road that moved messages
06:23  Chaco Canyon: the road nobody can explain
07:08  The Andes: where a road becomes a staircase
07:45  Rome, in last place
08:12  The answer that keeps not showing up
08:24  What a road actually promises

SOURCES
Sweet Track / Post Track — en.wikipedia.org/wiki/Sweet_Track
Pfahlwege im Campemoor — de.wikipedia.org/wiki/Pfahlwege_im_Campemoor
Widan el-Faras / Egyptian stone quarries — en.wikipedia.org/wiki/Widan_el_Faras_Basalt
Ishtar Gate — en.wikipedia.org/wiki/Ishtar_Gate
Royal Road — en.wikipedia.org/wiki/Royal_Road
Chaco Culture NHP — en.wikipedia.org/wiki/Chaco_Culture_National_Historical_Park
Inca road system — en.wikipedia.org/wiki/Inca_road_system
Appian Way — en.wikipedia.org/wiki/Appian_Way

Bloxam & Storemyr 2002, JEA 88(1): 23–36 — doi.org/10.1177/030751330208800103
Friedman, Sofaer & Weiner 2017, Advances in Archaeological Practice 5(4): 365–381 — doi.org/10.1017/aap.2017.25
Weiner, Friedman & Stein 2025, Antiquity 99(404): 500–516 — doi.org/10.15184/aqy.2025.4
Klein et al. 2026, Journal of Neolithic Archaeology 28: 1–36 — doi.org/10.12766/jna.2026.1

Dating and extent are contested in several places — the narration says so where
it matters, and the sources above are where to check.
```

**Zu den Zeitmarken:** sie stammen aus `ton/_zeitplan.json`, sind also an der
fertigen Spur gemessen und nicht geschätzt. Ändert sich die Tonspur, müssen sie
neu erzeugt werden (`python3 kapitel.py`).

**Quellenangaben** sind nach `config.md` „OFFEN, aber empfohlen" — Ink Explainer
legt als einziger der gemessenen Vorbildkanäle Quellen mit DOI offen und ist
zugleich der jüngste mit dem stärksten Ergebnis.

## Tags

```
first roads, sweet track, history of roads, neolithic, archaeology,
ancient engineering, chaco canyon, inca road system, appian way, ishtar gate,
royal road, bog trackway, prehistoric europe, ancient history, documentary
```

Fünfzehn Stück, alle aus dem Skriptinhalt abgeleitet. Der Kanal hat keine
gemessene Tag-Strategie; das hier ist Beschreibung des Inhalts, keine
Optimierung.

## Untertitel

`untertitel.srt` — 173 Blöcke, aus den ElevenLabs-Zeitmarken erzeugt, also vom
Erzeuger der Stimme selbst und nicht aus einer Spracherkennung. Keine
Überlappungen, keine Lücke über 3 s, höchstens 42 Zeichen je Zeile und zwei
Zeilen je Block.

Die Aussprache-Umschreibungen sind für die Anzeige zurückgesetzt: gesprochen
wird „Deemer", im Untertitel steht **Dümmer**.

## Thumbnail

**Nicht geliefert — und das ist Absicht.**

`config.md` hält fest: „Kein Thumbnail-Pfad. Noch nicht entschieden — und für
diesen Kanal ist der Thumbnail-Stil nicht einmal gemessen." Ein Thumbnail zu
bauen hieße, den wichtigsten Klickfaktor zu raten, während für alles andere in
diesem Video eine gemessene Grundlage vorliegt.

Was stattdessen bereitliegt: `thumbnail-kandidaten/` enthält vier Bilder aus dem
fertigen Satz in 1280×720, die als Ausgangsmaterial taugen. Welches davon
tauglich ist und welcher Text darauf gehört, ist eine Entscheidung, keine
Ableitung.

## KI-Kennzeichnung

Beim Hochladen zu setzen: **„Altered or synthetic content"**. Stimme und Bilder
sind vollständig erzeugt.
