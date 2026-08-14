# Szenenliste — Video 1, „Who Built the First Roads and Why?"

> **Zweite Fassung, auf Konkurrenz-Schnittfrequenz neu geschnitten.**
> Die erste Fassung mit 56 Einstellungen liegt als `szenen-v1.md` daneben.
> Grundlage des Neuschnitts: [`recherche/stil-unknown-frequencies.md`](../../recherche/stil-unknown-frequencies.md)
> — dort gemessen **3 s** (Odyssey) bzw. **4 s** (Iwo Jima) je Einstellung,
> Limited Animation, Schwenks und Zooms über statische Kompositionen,
> Figurenbewegung als Cut-out.
> **0 Credits verbraucht**, keine Bildgenerierung; Preise nur per
> `get_cost`-Preflight.

## Wie zu lesen

- **Motiv** = ein zu generierendes Bild. Mehrere Einstellungen mit demselben
  Motiv teilen sich **ein** Bild und unterscheiden sich nur durch die
  Kamerafahrt — das ist genau die Machart des Vorbilds und spart Bilder.
- **Fahrt** = was `ffmpeg` über dem Standbild fährt. Vier Werte:
  `Zoom rein`, `Zoom raus`, `Schwenk links`, `Schwenk rechts`, `statisch`.
- **Fig** = Figur im Bild · **Elem** = Referenz-Element `<<<ab1406ea-…>>>`
  muss in den Prompt eingebettet werden (immer dann, wenn der **Kopf mit dem
  Balken** sichtbar ist; bei Hand-, Bein- oder Fußbildern nicht).
- **Ebenen** = Vordergrund und Hintergrund werden **getrennt** generiert,
  damit `ffmpeg` sie unterschiedlich schnell bewegen kann (Parallax).
- **Zustandspaar** = zwei Bilder derselben Komposition in zwei Zuständen.
  Sichert die Wiedererkennung; spart kein Bild, aber den halben Prompt.

## Stilbindung (gilt für jede Bildbeschreibung)

Jeder Prompt beginnt mit dem V2-Gerüst aus
[`recherche/stil-uf-element/README.md`](../../recherche/stil-uf-element/README.md)
und endet mit der Proportionsklausel. Die Bildbeschreibungen in der Tabelle
sind der `SCENE:`-Teil, nicht der ganze Prompt.

```
Flat 2D vector cartoon in the style of a limited-animation explainer video.
Clean uniform anti-aliased black outlines of constant medium weight; no sketchy
lines, no hand-drawn jitter, no crosshatching. The background is noticeably more
detailed than the figures: layered flat shapes with a faint paper grain and light
stipple texture. Restricted three-colour palette - ink indigo #1F3A5F, warm amber
#E0A93B, off-white paper #F2EDE3 - plus the black outlines. No olive, no military
green, no slate grey, no brown. Flat colour fills, no gradients on the figures,
hard-edged shapes. Sparse composition, at most N distinct objects, generous empty
background. SCENE: <Bildbeschreibung, Figur als <<<ab1406ea-8d08-421e-a8b8-5d3ef88042cf>>>>
The character keeps its oversized round head at roughly one third of its total
body height, its off-white head colour and the solid indigo bar across the eye
region exactly as in the reference; the head must not drift to normal human
proportions. no text, no letters, no watermark, no logo.
```

**Objektobergrenze je Szenentyp, nicht global.** Der Elementtest hat gemessen,
dass Sachszenen 1,5- bis 1,7-mal dichter geraten als Personenszenen und dass
eine globale Bremse beide Seiten gleichmäßig senkt, den Unterschied aber nicht
behebt. Vorgabe daher: **N = 5** für Szenen mit Figur, **N = 3** für Schemata,
Karten und Detailaufnahmen.

**Kein Bildtext.** Das Vorbild fährt viel Text im Bild; unsere Prompts schließen
Text aus (`no text, no letters`). Wo eine Zahl tragen muss, trägt sie die
Sprecherstimme, nicht die Grafik.

## Szenentabelle

| Nr | Text (Anfang … Ende) | Start | Dauer | Motiv | Bild (SCENE-Teil) | Fahrt | Epoche/Ort | Fig | Elem | Ebenen | Anmerkung |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Look down the … road under you. | 0:00 | 4.1 s | **M01** | Aufsicht: die Figur tritt aus einer Haustür auf eine leere Asphaltstraße, die das untere Bilddrittel füllt | Zoom raus | heute | ja | ja | ja | — |
| 2 | You use roads … they come from | 0:04 | 3.6 s | **M01** | ↑ dasselbe Bild wie Einstellung 1 | Schwenk rechts | heute | ja | ja | ja | — |
| 3 | you save that … old to you. | 0:07 | 3.6 s | **M02** | Formatfüllende Asphaltfläche mit Fugen und Rissen, kein Horizont | Zoom rein | heute | – | – | – | — |
| 4 | They feel like … roads, and why? | 0:11 | 4.7 s | **M03** | Drei flache Fahrzeugsilhouetten — Auto, Lastwagen, Container — ziehen als Streifen über die Straße | Schwenk links | heute | – | – | ja | — |
| 5 | You'll probably reach … traders, moving goods. | 0:15 | 3.6 s | **M04** | Drei gleich große Felder nebeneinander: römischer Helm, Händlerwaage, einzelnes Speichenrad | Zoom rein | Symbolik | – | – | – | — |
| 6 | Or no one, … three feel right. | 0:19 | 3.3 s | **M04** | ↑ dasselbe Bild wie Einstellung 5 | Schwenk rechts | Symbolik | – | – | – | — |
| 7 | All three, as … tell, are wrong. | 0:22 | 2.7 s | **M05** | Dieselben drei Felder, jedes von einem breiten Indigobalken durchgestrichen | statisch | Symbolik | – | – | – | Zustand B zu M04 |
| 8 | The earliest road … were fighting water. | 0:25 | 3.8 s | **M06** | Weite flache Wiesenlandschaft, dunkles Wasser breitet sich von rechts über den Boden aus, die Figur steht klein am linken Rand | Zoom rein | urzeitlich | ja | ja | ja | GESCHÜTZT — Antwort |
| 9 | Their land was … it a floor. | 0:29 | 3.8 s | **M07** | Nahaufnahme: die Figur kniet und legt eine helle Holzbohle auf den weichen Grund, das Wasser stoppt an der Kante | statisch | urzeitlich | ja | ja | ja | — |
| 10 | To see what … in a bog. | 0:33 | 3.3 s | **M08** | Weite Moorfläche mit Torfmoospolstern und offenen schwarzen Wasseraugen, die Figur steht klein in der Bildmitte | Zoom rein | Moor | ja | ja | ja | — |
| 11 | A bog is … grows over it | 0:36 | 4.7 s | **M08** | ↑ dasselbe Bild wie Einstellung 10 | Schwenk rechts | Moor | ja | ja | ja | — |
| 12 | and the ground … a wet sponge | 0:41 | 2.2 s | **M09** | Nahaufnahme Moorboden: ein Stiefel sinkt bis zum Schaft in schwarzes Wasser zwischen Moospolstern | Zoom rein | Moor | ja | – | – | — |
| 13 | it will take … can't cross it. | 0:43 | 4.9 s | **M09** | ↑ dasselbe Bild wie Einstellung 12 | statisch | Moor | ja | – | – | — |
| 14 | Almost six thousand … south of England | 0:48 | 3.6 s | **M10** | Weite Marschlandschaft im Morgennebel: Schilfbänder, offene Wasserflächen, am Horizont eine bewaldete Insel | Schwenk rechts | Somerset ~3800 v. Chr. | – | – | ja | — |
| 15 | people faced the … and they built. | 0:51 | 3.0 s | **M11** | Dieselbe Marschlandschaft, jetzt mit der Figur am Ufer und einer ersten Bohle im Schilf | Zoom rein | Somerset | ja | ja | ja | Zustand B zu M10 |
| 16 | We call what … pin its date | 0:54 | 3.6 s | **M12** | Formatfüllende Eichen-Querschnittscheibe, konzentrische Jahresringe als flache Ringe | Zoom rein | Detail | – | – | – | — |
| 17 | each year a … a bad one | 0:58 | 4.7 s | **M13** | Dieselbe Ringfolge als abgewickeltes Streifenband, breite und schmale Ringe im Wechsel | Schwenk rechts | Schema | – | – | – | — |
| 18 | and you can … series. The result: | 1:03 | 3.3 s | **M13** | ↑ dasselbe Bild wie Einstellung 17 | Schwenk rechts | Schema | – | – | – | — |
| 19 | 3807 BC or … two calendar years | 1:06 | 4.7 s | **M14** | Kahler Winterwald im Schnee, die Figur schlägt mit einem Steinbeil in eine mächtige Eiche | Zoom rein | Somerset 3807/3806 v. Chr. | ja | ja | ja | — |
| 20 | and even the … tell you which. | 1:10 | 2.2 s | **M14** | ↑ dasselbe Bild wie Einstellung 19 | statisch | Somerset 3807/3806 v. Chr. | ja | ja | ja | — |
| 21 | And what stood … was a structure. | 1:13 | 3.0 s | **M15** | Luftaufnahme: eine schnurgerade helle Bohlenlinie zieht durch dunkles Schilfmoor | Zoom raus | Somerset | – | – | – | — |
| 22 | About 1,800 metres … a reed marsh | 1:16 | 2.7 s | **M16** | Flache Karte: Insel links, Höhenrücken rechts, dazwischen die Linie durch die Marsch | Schwenk rechts | Somerset / Karte | – | – | – | — |
| 23 | from an island … ridge at Shapwick. | 1:18 | 2.7 s | **M16** | ↑ dasselbe Bild wie Einstellung 22 | Zoom rein | Somerset / Karte | – | – | – | — |
| 24 | Oak planks up … five centimetres thick | 1:21 | 4.1 s | **M17** | Stillleben vor leerem Grund: eine lange, breite, auffällig dünne Eichenbohle, daneben der Stamm mit steckenden Spaltkeilen | Zoom rein | Detail | – | – | ja | — |
| 25 | split, not sawn, … a metre through. | 1:25 | 4.1 s | **M17** | ↑ dasselbe Bild wie Einstellung 24 | Schwenk links | Detail | – | – | ja | — |
| 26 | The tool kit: … mallets. That's all. | 1:29 | 3.0 s | **M18** | Drei Werkzeuge nebeneinander auf leerem Grund: Steinbeil, Holzkeil, Schlegel | statisch | Detail | – | – | – | — |
| 27 | They drove crossed … packed dead plants | 1:32 | 4.7 s | **M19** | Halbnah: die Hände der Figur treiben gekreuzte Pflöcke in den Torf und legen eine Bohle in die Kerbe | Zoom rein | Somerset | ja | – | ja | — |
| 28 | laid long rails … the parts together. | 1:37 | 4.7 s | **M19** | ↑ dasselbe Bild wie Einstellung 27 | Schwenk rechts | Somerset | ja | – | ja | — |
| 29 | No nails. A … A push fit. | 1:42 | 1.4 s | **M20** | Extreme Nahaufnahme der Steckverbindung: Kerbe und Pflock greifen ineinander, kein Nagel | Zoom rein | Detail | – | – | – | — |
| 30 | And the pegs … a managed stand | 1:43 | 4.4 s | **M21** | Niederwald in Reihen: schnurgerade astfreie Haselstangen, an den Stöcken alte Schnittstellen | Schwenk rechts | Somerset / Wald | – | – | ja | — |
| 31 | trees cut low … this was built. | 1:47 | 4.4 s | **M21** | ↑ dasselbe Bild wie Einstellung 30 | Zoom raus | Somerset / Wald | – | – | ja | — |
| 32 | Now hold on … the strangest part. | 1:52 | 1.9 s | **M22** | Bodennähe im Gegenlicht: die fertige Bahn ist genau eine Planke breit und verliert sich im Schilf | Zoom rein | Somerset | – | – | – | — |
| 33 | All that effort … end to end. | 1:54 | 3.8 s | **M22** | ↑ dasselbe Bild wie Einstellung 32 | statisch | Somerset | – | – | – | — |
| 34 | Not a cart … about ten years. | 1:58 | 4.4 s | **M23** | Dieselbe Bahn, Wasser steht bereits über den Planken | statisch | Somerset | – | – | ja | Zustand B zu M22 |
| 35 | Then the water … and took it. | 2:02 | 2.2 s | **M23** | ↑ dasselbe Bild wie Einstellung 34 | Zoom rein | Somerset | – | – | ja | — |
| 36 | And under it … around 3838 BC | 2:04 | 4.1 s | **M24** | Blick unter die Wasseroberfläche: unter der versunkenen Bahn schimmert eine zweite, ältere Bohlenlinie | Zoom rein | Somerset | – | – | ja | — |
| 37 | same route, thirty … done this before. | 2:08 | 2.7 s | **M24** | ↑ dasselbe Bild wie Einstellung 36 | Schwenk links | Somerset | – | – | ja | — |
| 38 | One site might … be a fluke. | 2:11 | 1.6 s | **M25** | Flache Karte Nordwesteuropa: ein Lichtpunkt in Südengland, die Fläche zieht nach Nordosten zur norddeutschen Tiefebene | Schwenk rechts | Karte Europa | – | – | – | — |
| 39 | So go north-east, … in northern Germany. | 2:13 | 4.1 s | **M25** | ↑ dasselbe Bild wie Einstellung 38 | Schwenk rechts | Karte Europa | – | – | – | — |
| 40 | More than 550 … into modern times. | 2:17 | 5.8 s | **M26** | Dieselbe Karte, über der Tiefebene zünden hunderte kleine Lichtpunkte | Zoom rein | Karte Europa | – | – | – | Zustand B zu M25 |
| 41 | And beside one … business being there. | 2:23 | 4.4 s | **M27** | Grabungsschnitt im Torf: die Figur kniet mit Kelle vor einem halb freigelegten Fund unter einer Plane | Zoom rein | Niedersachsen, heute | ja | ja | ja | GESCHÜTZT — Anriss der Schleife; Zustand A |
| 42 | Hold on to … back for it. | 2:27 | 2.5 s | **M27** | ↑ dasselbe Bild wie Einstellung 41 | statisch | Niedersachsen, heute | ja | ja | ja | — |
| 43 | Some of the … the D mmer. | 2:29 | 3.6 s | **M28** | Stille Luftaufnahme: flacher See in dunklem, nassem Moorland | Schwenk rechts | Dümmer | – | – | – | — |
| 44 | One of them, … called the Campemoor. | 2:33 | 3.8 s | **M29** | Freigelegter Wegabschnitt im Torfprofil, daneben die Figur klein als Maßstab | Zoom rein | Campemoor | ja | ja | ja | — |
| 45 | It's around six … thousand years old | 2:37 | 2.5 s | **M29** | ↑ dasselbe Bild wie Einstellung 44 | statisch | Campemoor | ja | ja | ja | — |
| 46 | the studies differ … that number loosely. | 2:39 | 3.3 s | **M29** | ↑ dasselbe Bild wie Einstellung 44 | Zoom raus | Campemoor | ja | ja | ja | — |
| 47 | It ran up … it had layers: | 2:43 | 3.8 s | **M30** | Querschnitt-Schaubild: unten dünne Birkenstämme, darüber drei Reihen Kiefernstämme, oben dicke Rundholzdecke, seitlich schräge Pflöcke | Zoom raus | Campemoor / Schema | – | – | – | — |
| 48 | thin birch trunks … as a base | 2:46 | 3.8 s | **M30** | ↑ dasselbe Bild wie Einstellung 47 | Schwenk rechts | Campemoor / Schema | – | – | – | — |
| 49 | a surface of … with birch pegs. | 2:50 | 4.7 s | **M30** | ↑ dasselbe Bild wie Einstellung 47 | Zoom rein | Campemoor / Schema | – | – | – | — |
| 50 | Base, bed, surface. … with stone axes. | 2:55 | 3.0 s | **M31** | Extreme Nahaufnahme: das Ende eines Rundholzes mit facettierten Beilhieben im alten Holz | Zoom rein | Detail | – | – | – | — |
| 51 | The chop marks … of the logs. | 2:58 | 3.0 s | **M31** | ↑ dasselbe Bild wie Einstellung 50 | statisch | Detail | – | – | – | — |
| 52 | And thirty metres … hundred years later. | 3:01 | 4.7 s | **M32** | Luftaufnahme: zwei parallele helle Linien ziehen im Abstand von dreißig Metern durch dasselbe Moor | Schwenk rechts | Campemoor | – | – | – | — |
| 53 | Same bog, same … problem, same answer. | 3:06 | 1.6 s | **M32** | ↑ dasselbe Bild wie Einstellung 52 | Zoom raus | Campemoor | – | – | – | — |
| 54 | Why there, why … it with care | 3:07 | 3.8 s | **M33** | Schreibtisch von oben: eine aufgeschlagene Studie, eine Hand zeichnet eine steigende Kurve und setzt ein Fragezeichen an den Rand | Zoom rein | heute / Studie | ja | – | – | — |
| 55 | it's one paper, … goes like this: | 3:11 | 4.1 s | **M33** | ↑ dasselbe Bild wie Einstellung 54 | statisch | heute / Studie | ja | – | – | — |
| 56 | the rain grew, … follow that curve. | 3:15 | 4.1 s | **M34** | Uferlinie im Zeitverlauf: Wasser schiebt sich stufenweise über flaches Land, jede Stufe als eigene helle Kante | Schwenk rechts | Dümmer / Schema | – | – | ja | — |
| 57 | Pr 31, they … of increasing waterlogging. | 3:19 | 3.3 s | **M34** | ↑ dasselbe Bild wie Einstellung 56 | Zoom rein | Dümmer / Schema | – | – | ja | — |
| 58 | They point to … in new patterns | 3:23 | 3.6 s | **M35** | Geteiltes Bild: links steigendes Wasser, rechts wandernde Siedlungspunkte auf einer stilisierten Karte | statisch | Schema | – | – | – | — |
| 59 | so even here, … come in waves: | 3:26 | 5.2 s | **M36** | Diagramm: entlang einer waagerechten Zeitachse stapeln sich Bohlenstege zu drei Wellen, die Lücken dazwischen bleiben leer | Schwenk rechts | Schema | – | – | – | — |
| 60 | building booms that … an odd one: | 3:31 | 4.4 s | **M36** | ↑ dasselbe Bild wie Einstellung 59 | Zoom rein | Schema | – | – | – | — |
| 61 | pollen from the … path was built | 3:36 | 4.1 s | **M37** | Kiefernbestand am Moorrand, sichtbar gelichtet: Stümpfe im Vordergrund, wenige Kronen dahinter | Zoom rein | Campemoor | – | – | ja | — |
| 62 | the likely cause … was being built. | 3:40 | 4.9 s | **M37** | ↑ dasselbe Bild wie Einstellung 61 | Schwenk links | Campemoor | – | – | ja | — |
| 63 | Now, the thing … of these paths | 3:45 | 3.8 s | **M38** | Dieselbe Grabung wie M27, die Plane ist zurückgeschlagen: zwei zerbrochene hölzerne Wagenachsen liegen im nassen Torf | Zoom rein | Niedersachsen, heute | ja | ja | ja | GESCHÜTZT — Auflösung der Schleife; Zustand B zu M27 |
| 64 | Pr 7, laid … broken wagon axles. | 3:49 | 4.1 s | **M38** | ↑ dasselbe Bild wie Einstellung 63 | Zoom rein | Niedersachsen, heute | ja | ja | ja | — |
| 65 | They count among … of northern Germany. | 3:53 | 4.1 s | **M39** | Die beiden Achsen freigestellt auf leerem Grund, wie ein Museumsfund | statisch | Detail | – | – | – | — |
| 66 | So run the … in that region: | 3:57 | 3.3 s | **M40** | Zeitstrahl als Bohlenbahn: die Bahn läuft von links nach rechts, weit links ihr Anfang, erst kurz vor dem rechten Rand liegt ein kleines Rad | Schwenk rechts | Schema | – | – | ja | — |
| 67 | about six and … a half thousand. | 4:00 | 4.7 s | **M40** | ↑ dasselbe Bild wie Einstellung 66 | Schwenk rechts | Schema | – | – | ja | — |
| 68 | The road wins … two thousand years. | 4:05 | 2.2 s | **M40** | ↑ dasselbe Bild wie Einstellung 66 | Zoom rein | Schema | – | – | ja | — |
| 69 | People there built … rolled on one. | 4:07 | 3.6 s | **M41** | Die Figur schreitet denselben Zeitstrahl ab, das Rad liegt noch weit vor ihr | Schwenk rechts | Schema | ja | ja | ja | — |
| 70 | One axle lay … in the bog. | 4:10 | 3.6 s | **M41** | ↑ dasselbe Bild wie Einstellung 69 | Zoom rein | Schema | ja | ja | ja | — |
| 71 | The wheel is … guest on it. | 4:14 | 4.4 s | **M42** | Ein einzelnes Speichenrad rollt auf eine alte Bohlenstraße, wird langsamer und steht still | Zoom rein | zeitlos | – | – | ja | GESCHÜTZT — Rad als Gast |
| 72 | So if the … were roads for? | 4:18 | 4.4 s | **M43** | Flache Weltkarte: die zwei nordeuropäischen Punkte verlöschen, Lichter zünden in Ägypten, Irak, Iran, New Mexico und den Anden | Zoom raus | Karte Welt | – | – | – | — |
| 73 | Chase that question … at every stop | 4:23 | 4.1 s | **M43** | ↑ dasselbe Bild wie Einstellung 72 | Schwenk rechts | Karte Welt | – | – | – | — |
| 74 | and the answers … than you'd think. | 4:27 | 2.2 s | **M44** | Fünf leere Rahmen nebeneinander, in jedem ein Fragezeichen | statisch | Schema | – | – | – | — |
| 75 | Start in Egypt, … 4,500 years ago. | 4:29 | 2.2 s | **M45** | Wüsten-Luftbild: eine helle Steinstraße zieht vom dunklen Basaltbruch durch Geröllhänge zu einer fernen Uferlinie | Zoom rein | Ägypten ~2500 v. Chr. | – | – | – | — |
| 76 | In the desert … some eleven kilometres | 4:31 | 4.4 s | **M45** | ↑ dasselbe Bild wie Einstellung 75 | Schwenk rechts | Ägypten ~2500 v. Chr. | – | – | – | — |
| 77 | the reports differ … from a quarry | 4:36 | 3.0 s | **M46** | Der Steinbruch im Anschnitt: dunkle Basaltbänke mit Werkspuren, davor beginnt die Straße | Schwenk links | Ägypten | – | – | – | — |
| 78 | a pit where … of a lake. | 4:39 | 4.4 s | **M46** | ↑ dasselbe Bild wie Einstellung 77 | Zoom raus | Ägypten | – | – | – | — |
| 79 | The quarry is … whatever lay close: | 4:43 | 3.8 s | **M47** | Bodennah: Pflaster aus Basaltbrocken, Kalk- und Sandstein, dazwischen Platten aus versteinertem Holz mit sichtbarer Maserung | Zoom rein | Detail | – | – | – | — |
| 80 | basalt, a hard … of petrified wood | 4:47 | 3.6 s | **M47** | ↑ dasselbe Bild wie Einstellung 79 | Zoom rein | Detail | – | – | – | — |
| 81 | dead trees turned … No market anywhere. | 4:50 | 3.8 s | **M48** | Eine Hand fährt über eine Platte versteinertes Holz, die Maserung liegt frei | statisch | Detail | ja | – | – | — |
| 82 | Crews hauled basalt … for the pyramids | 4:54 | 5.5 s | **M49** | Die Figur zieht mit anderen in einer Reihe einen Basaltblock auf einem Holzschlitten die Straße hinab | Schwenk rechts | Ägypten, Altes Reich | ja | ja | ja | — |
| 83 | one of those … Pyramid at Giza. | 5:00 | 3.6 s | **M49** | ↑ dasselbe Bild wie Einstellung 82 | Zoom rein | Ägypten, Altes Reich | ja | ja | ja | — |
| 84 | Even here, the … of the trip. | 5:03 | 3.3 s | **M50** | Beladener Lastkahn mit dunklen Blöcken auf weitem Wasser, am Horizont eine Pyramidenbaustelle mit Rampen | Schwenk rechts | Ägypten | – | – | ja | — |
| 85 | The blocks moved … lake stood high. | 5:07 | 3.6 s | **M50** | ↑ dasselbe Bild wie Einstellung 84 | Zoom raus | Ägypten | – | – | ja | — |
| 86 | This road was … royal building site. | 5:10 | 3.0 s | **M51** | Der fertige dunkle Tempelboden aus Basaltplatten, streng gerastert | Zoom rein | Ägypten | – | – | – | — |
| 87 | Walls of glazed … bulls and dragons | 5:13 | 3.0 s | **M52** | Reliefwand in Aufsicht: Löwen, Stiere und Drachen als flache Figuren in Reihen | Schwenk rechts | Babylon, 569 v. Chr. | – | – | ja | — |
| 88 | about 120 figures … street in Babylon. | 5:16 | 3.6 s | **M52** | ↑ dasselbe Bild wie Einstellung 87 | Schwenk rechts | Babylon, 569 v. Chr. | – | – | ja | — |
| 89 | This is in … Nebuchadnezzar the Second. | 5:20 | 3.8 s | **M53** | Stadtsilhouette Babylons, das Tor als hellste Fläche | Zoom raus | Babylon | – | – | – | — |
| 90 | The street itself … bed of bitumen | 5:24 | 3.3 s | **M54** | Straßenquerschnitt: Steinplatten liegen in einer dunklen Bitumenschicht, die Breite als Maßband angedeutet | Zoom rein | Schema | – | – | – | — |
| 91 | natural tar up … yourself walking it: | 5:27 | 3.8 s | **M54** | ↑ dasselbe Bild wie Einstellung 90 | Schwenk rechts | Schema | – | – | – | — |
| 92 | from the river … the Ishtar Gate | 5:31 | 3.8 s | **M55** | Die Figur geht die breite Straße entlang, Reliefwände beidseits, vor ihr wächst das Tor auf | Zoom rein | Babylon | ja | ja | ja | — |
| 93 | the city's great … of the city. | 5:35 | 4.9 s | **M55** | ↑ dasselbe Bild wie Einstellung 92 | Zoom rein | Babylon | ja | ja | ja | — |
| 94 | But the day … once a year: | 5:40 | 3.0 s | **M56** | Prozession im Frühjahrslicht: Götterstatuen auf Tragen ziehen durch das Tor, dichte Menge, die Figur trägt mit | Schwenk rechts | Babylon, Neujahr | ja | ja | ja | — |
| 95 | at the spring … a grand procession. | 5:43 | 6.0 s | **M56** | ↑ dasselbe Bild wie Einstellung 94 | Zoom rein | Babylon, Neujahr | ja | ja | ja | — |
| 96 | All of it … heart, a stage. | 5:49 | 3.8 s | **M57** | Dieselbe Straße leer bei Nacht, nur Fackellicht auf den Reliefwänden | Zoom raus | Babylon | – | – | – | Zustand B zu M55 |
| 97 | Persia roughly, modern … gets one breath: | 5:52 | 1.9 s | **M58** | Ein Reiter wechselt im Lauf das Pferd an einer Poststation, dahinter läuft die Straße bis zum Horizont | Schwenk rechts | Persien ~500 v. Chr. | ja | ja | ja | — |
| 98 | a road of … walked in ninety. | 5:54 | 6.6 s | **M58** | ↑ dasselbe Bild wie Einstellung 97 | Schwenk rechts | Persien ~500 v. Chr. | ja | ja | ja | — |
| 99 | A post road, … ran an empire. | 6:01 | 3.6 s | **M59** | Kartenband Susa–Sardis: eine Linie mit Kettengliedern als Stationen | Schwenk rechts | Karte | – | – | – | — |
| 100 | And then there's … nobody can explain. | 6:04 | 2.2 s | **M60** | Canyon-Luftbild: rote Felswände, im Wüstenboden eine haarfeine gerade Linie | Zoom rein | Chaco ~1000 n. Chr. | – | – | – | — |
| 101 | Chaco Canyon, New … the United States | 6:07 | 3.6 s | **M60** | ↑ dasselbe Bild wie Einstellung 100 | Schwenk rechts | Chaco ~1000 n. Chr. | – | – | – | — |
| 102 | roughly a thousand … is argued over. | 6:10 | 3.0 s | **M61** | Drei durchgestrichene Felder: Rad, Pferd, Ochse | statisch | Schema | – | – | – | — |
| 103 | The people there … horse, no ox. | 6:13 | 2.7 s | **M61** | ↑ dasselbe Bild wie Einstellung 102 | Zoom rein | Schema | – | – | – | — |
| 104 | Yet they scraped … wide, dead straight | 6:16 | 4.4 s | **M62** | Bodennah im ausgeschabten Straßenbett: neun Meter Breite, Ränder aus Steinen, schnurgerade bis zum Horizont, die Figur klein am Rand | Zoom raus | Chaco | ja | ja | ja | — |
| 105 | one of them … in the way | 6:20 | 3.8 s | **M62** | ↑ dasselbe Bild wie Einstellung 104 | Schwenk rechts | Chaco | ja | ja | ja | — |
| 106 | they cut stone … went straight over. | 6:24 | 3.3 s | **M63** | In die Felswand geschlagene Steintreppe, die Straße läuft oben ungebrochen weiter | Zoom rein | Chaco | – | – | – | — |
| 107 | Nothing ever rolled … The honest answer: | 6:27 | 3.8 s | **M64** | Vier Symbolfelder über dem Straßenbett: Tragkorb, Speer, Rasselstab, Versammlungskreis | Schwenk rechts | Chaco / Schema | – | – | – | — |
| 108 | nobody knows. Scholars … war, worship, politics. | 6:31 | 3.0 s | **M64** | ↑ dasselbe Bild wie Einstellung 107 | statisch | Chaco / Schema | – | – | – | — |
| 109 | A recent laser … Pueblo peoples today | 6:34 | 6.0 s | **M65** | Lidar-Overlay: eine Punktwolke des Geländes, eine Straßenlinie richtet sich auf einen tief stehenden Sonnenpunkt über einem Berg | Zoom rein | Chaco / Schema | – | – | ja | — |
| 110 | a hint toward … reading among several. | 6:40 | 2.7 s | **M65** | ↑ dasselbe Bild wie Einstellung 109 | statisch | Chaco / Schema | – | – | ja | — |
| 111 | We can map … they were for. | 6:43 | 4.4 s | **M66** | Senkrechter Steigflug: die Straße wird zur dünnen Linie und endet im Leeren | Zoom raus | Chaco | – | – | – | GESCHÜTZT — Chaco-Nichtwissen |
| 112 | Last stop: the … of South America. | 6:47 | 3.0 s | **M67** | Anden-Panorama: ein Straßenfaden zieht über Grate und durch Täler, kein Ende sichtbar | Schwenk rechts | Anden ~1450 n. Chr. | – | – | ja | — |
| 113 | The Inca empire … nobody can state | 6:50 | 3.6 s | **M67** | ↑ dasselbe Bild wie Einstellung 112 | Zoom raus | Anden ~1450 n. Chr. | – | – | ja | — |
| 114 | estimates go from … to 60,000 kilometres. | 6:54 | 2.5 s | **M68** | Drei Zahlenbänder unterschiedlicher Länge übereinander, alle drei gleich hell | Zoom rein | Schema | – | – | – | — |
| 115 | Parts are older … and the Tiwanaku. | 6:56 | 4.1 s | **M69** | Dieselbe Anden-Trasse, ein älterer Abschnitt in abweichendem Farbton eingefärbt | Schwenk rechts | Anden | – | – | – | Zustand B zu M67 |
| 116 | It was paved … earth and sand. | 7:01 | 4.4 s | **M70** | Vorbeiflug, die Oberfläche wechselt in drei Abschnitten: Pflaster, gestampfte Erde, Sand | Schwenk rechts | Anden | – | – | – | — |
| 117 | Its builders had … pull a cart | 7:05 | 3.3 s | **M71** | Leere Trasse am Steilhang, kein Rad und kein Zugtier im Bild | Zoom rein | Anden | – | – | – | — |
| 118 | so where the … road can do: | 7:08 | 3.8 s | **M71** | ↑ dasselbe Bild wie Einstellung 117 | Schwenk rechts | Anden | – | – | – | — |
| 119 | it became a … a wheel cold. | 7:12 | 2.5 s | **M72** | Steintreppe zieht einen Steilhang hinauf, die Figur läuft sie leichtfüßig empor | Zoom rein | Anden | ja | ja | ja | — |
| 120 | For you, on … moved on foot | 7:15 | 5.2 s | **M72** | ↑ dasselbe Bild wie Einstellung 119 | Schwenk rechts | Anden | ja | ja | ja | — |
| 121 | and today, only … visible at all. | 7:20 | 3.6 s | **M73** | Karte Südamerika: das Netz leuchtet vollständig, nur ein Viertel der Linien bleibt hell | Zoom raus | Karte | – | – | – | — |
| 122 | Which brings us, … and to Rome. | 7:23 | 3.3 s | **M74** | Eine lange Reihe unscharfer Gestalten, ganz am Ende tritt ein einzelner Legionär ins Bild | Schwenk rechts | Rom, 312 v. Chr. | ja | ja | ja | — |
| 123 | You were promised … first great road | 7:27 | 4.1 s | **M74** | ↑ dasselbe Bild wie Einstellung 122 | Zoom rein | Rom, 312 v. Chr. | ja | ja | ja | — |
| 124 | the Appian Way, … move troops south. | 7:31 | 6.0 s | **M75** | Marschkolonne auf gerader Steinstraße nach Süden, Staub, Speerspitzen im Gegenlicht | Schwenk rechts | Rom, Via Appia | ja | ja | ja | — |
| 125 | Not a trade … of stone layers? | 7:37 | 4.4 s | **M76** | Zwei gleich große Querschnitte nebeneinander: links der Vier-Schichten-Steinstapel, rechts ein Erdweg mit dünner Kiesdecke | Zoom rein | Rom / Schema | – | – | – | — |
| 126 | Even in Rome … not the rule: | 7:41 | 3.0 s | **M76** | ↑ dasselbe Bild wie Einstellung 125 | Schwenk rechts | Rom / Schema | – | – | – | — |
| 127 | Roman law sorted … earth and gravel. | 7:44 | 4.4 s | **M76** | ↑ dasselbe Bild wie Einstellung 125 | Zoom raus | Rom / Schema | – | – | – | — |
| 128 | Trade is the … not showing up. | 7:49 | 3.8 s | **M77** | Eine sichtbar jahrhundertealte, blank getretene Bohlenstraße, leer | Zoom rein | zeitlos | – | – | – | — |
| 129 | That doesn't mean … walked these paths. | 7:52 | 2.2 s | **M77** | ↑ dasselbe Bild wie Einstellung 128 | statisch | zeitlos | – | – | – | — |
| 130 | It means trade … was already old. | 7:55 | 4.7 s | **M78** | Dieselbe Straße, jetzt ziehen Händler mit Bündeln darüber | Schwenk rechts | zeitlos | ja | ja | ja | Zustand B zu M77 |
| 131 | So here's the … only about speed. | 7:59 | 3.6 s | **M79** | Regennacht: eine einfache alte Straße hält unter einem Wasserfilm, Lichter spiegeln sich | Zoom rein | zeitlos | – | – | ja | — |
| 132 | A road is … be there tomorrow | 8:03 | 4.7 s | **M79** | ↑ dasselbe Bild wie Einstellung 131 | Schwenk rechts | zeitlos | – | – | ja | — |
| 133 | in the wet … in the dark. | 8:07 | 1.9 s | **M80** | Dieselbe Straße im Dunkeln, nur die Wegkante bleibt sichtbar | statisch | zeitlos | – | – | – | Zustand B zu M79 |
| 134 | People in a … thousand years back | 8:09 | 4.4 s | **M81** | Rückblende Somerset: die Figur legt im Regen die letzte Bohle, Wasser steht schon an den Pflöcken | Zoom rein | Somerset | ja | ja | ja | — |
| 135 | and kept it … German bog country | 8:14 | 4.1 s | **M81** | ↑ dasselbe Bild wie Einstellung 134 | statisch | Somerset | ja | ja | ja | — |
| 136 | the oldest road … thousand years apart | 8:18 | 4.1 s | **M82** | Nebeltotale: die zerbrochene Achse neben der uralten Bohlenlinie | Zoom raus | Niedersachsen | – | – | ja | — |
| 137 | road first. So … what humans do. | 8:22 | 4.7 s | **M82** | ↑ dasselbe Bild wie Einstellung 136 | Zoom rein | Niedersachsen | – | – | ja | — |
| 138 | They did it … it before Rome. | 8:27 | 3.0 s | **M83** | Moderne Schuhe am aufgeweichten Wegrand, Wasser sammelt sich in den Abdrücken | Zoom rein | heute | ja | – | – | — |
| 139 | They look at … build a yes. | 8:30 | 3.3 s | **M84** | Die Figur richtet sich über der frisch gelegten Bohle auf und sieht in die Kamera | Zoom rein | heute / urzeitlich | ja | ja | ja | GESCHÜTZT — Schlussbild |

## Zahlen

| Größe | Wert |
|---|---|
| Einstellungen | **139** (Ziel 130–170) |
| Gesamtlaufzeit | 8:33 |
| Mittlere Dauer | **3.69 s** (Ziel 3–5 s; Vorbild 3–4 s) |
| Spanne | 1.4 – 6.6 s |
| unter 3 s | 24 — überwiegend rhetorische Kurzbeats („No nails. A push fit.", „Same bog, same problem, same answer.") |
| über 5 s | 8 — je ein zusammenhängender Satz, der sich nicht sinnvoll teilen lässt |
| über 8 s | 0 |
| **Motive (zu generierende Bilder)** | **84** |
| Einstellungen je Motiv | 1,65 im Mittel |
| Motive mit mehreren Einstellungen | 51 → **55 Bilder gespart** |
| Zustandspaare | 12 (davon Anriss/Auflösung als geschütztes Paar) |
| Motive mit getrennten Ebenen | **38** → betrifft 69 Einstellungen |
| Einstellungen mit Figur | 45 (32 %) |
| Einstellungen mit eingebettetem Element | 37 (27 %) |

**Zur Figurenquote:** 32 % liegt unter der ersten Fassung (41 %), weil der
feinere Schnitt viele Detail-, Schema- und Kartenbilder erzeugt hat. Das
entspricht dem Vorbild — dort trägt nicht die Anwesenheit der Figur die
Wiedererkennung, sondern **ein einziges hartes Gesichtszeichen, wenn sie da
ist.** Der Balkenkopf ist in 37 Einstellungen sichtbar, verteilt über alle
siebzehn Absätze; die längste figurlose Strecke bleibt unter 40 Sekunden.

## Die sechs geschützten Momente

Jeder hat ein eigenes Motiv und darf länger stehen als der Zielwert.

| Moment | Einstellung(en) | Motiv | Dauer |
|---|---|---|---|
| Antwort | 8 | M06 | 3.8 s |
| Anriss der Schleife; Zustand A | 41–42 | M27 | 6.8 s |
| Auflösung der Schleife; Zustand B zu M27 | 63–64 | M38 | 7.9 s |
| Rad als Gast | 71 | M42 | 4.4 s |
| Chaco-Nichtwissen | 111 | M66 | 4.4 s |
| Schlussbild | 139 | M84 | 3.3 s |

**Das Paar M27 / M38** ist der Kern der offenen Schleife: dieselbe Grabung,
einmal mit geschlossener Plane (Anriss, Einstellung 41–42), einmal
zurückgeschlagen mit den zwei Achsen (Auflösung, 63–64). Zwei Bilder, eine
Komposition — der Wiedererkennungseffekt hängt daran, dass Bildausschnitt und
Kameraposition identisch bleiben.

## Getrennte Ebenen (Parallax)

**38 von 84 Motiven** werden in zwei Ebenen generiert: Vordergrund
freigestellt, Hintergrund vollflächig. `ffmpeg` fährt beide mit
unterschiedlicher Geschwindigkeit — das erzeugt Tiefe ohne Videoclip und ist
die billigste Annäherung an die Cut-out-Bewegung des Vorbilds.

Drei Gruppen:

1. **Figur vor Landschaft** (M01, M06, M07, M08, M11, M14, M27, M29, M38, M41,
   M49, M55, M56, M58, M62, M72, M74, M75, M78, M81, M84) — die Figur bewegt
   sich langsamer als der Hintergrund.
2. **Objekt vor Grund** (M03 Fahrzeuge, M17 Bohle, M40 Rad auf dem Zeitstrahl,
   M42 rollendes Rad, M50 Lastkahn) — das Objekt zieht, der Grund steht.
3. **Wetter- und Wasserebene** (M10 Nebel, M21 Wald, M23 steigendes Wasser,
   M24 Unterwasser, M34 Uferlinien, M37 Kiefern, M52 Reliefwand, M65
   Lidar-Punkte, M67 Anden, M79 Regen, M82 Nebel) — eine transparente Lage
   über der Landschaft.

## Kosten

Preise **per `get_cost` gemessen am 2026-08-14**:

| Posten | Credits |
|---|---:|
| Standbild `nano_banana_2`, 16:9, **2k** | **2,0** |
| Standbild 1k | 1,5 |
| Clip Seedance 1.5 Pro, 1080p, 4 s | 12 |
| Clip 8 s | 24 |
| Clip 12 s | 36 |

**Rechnung:**

| Schritt | Bilder/Clips | Credits |
|---|---:|---:|
| 84 Motive als Standbild 2k | 84 | 168 |
| *abzüglich* Mehrfachnutzung | −55 Bilder gegenüber „ein Bild je Einstellung" | −110 |
| Zweite Ebene für 38 Parallax-Motive | +38 | +76 |
| Die 6 geschützten Momente zusätzlich als Clip | +6 | +120 |

| Variante | Credits | € (Ultra-Kontingent) | € (Nachkauf) |
|---|---:|---:|---:|
| **A — alle Motive als Standbild, ffmpeg bewegt** | **168** | 0.46 | 8.23 |
| **B — A plus getrennte Ebenen** | **244** | 0.67 | 11.96 |
| **C — B plus 6 echte Clips für die geschützten Momente** | **364** | 1.00 | 17.84 |
| zum Vergleich: erste Fassung, alle 56 Einstellungen als Clip | 1.788 | 4,92 | 87,61 |

**Euro-Grundlage:** Das Konto läuft auf **Ultra** — 3.000 Credits im Monat für
99 € im Jahr, also **0,00275 € je Credit**. Ein Nachkauf kostet dagegen
0,049 € je Credit (1.000 Credits für 49 €). Beide Spalten stehen da, weil die
erste Zahl nur gilt, solange das Monatskontingent reicht: **Variante C
verbraucht 364 von 3.000 Monats-Credits — rund 12 %.** Ein ganzes
Video kostet damit im Kontingent unter einem Euro.

**Empfehlung: Variante C.** Der Aufschlag von B auf C sind 120 Credits
(0,32 €) für die sechs Momente, an denen das Video hängt — dort
lohnt echte Bewegung. Die anderen 78 Motive tragen ein Standbild mit
ffmpeg-Fahrt; das ist die Machart des Vorbilds, nicht ein Sparzwang.

## Was diese Fassung nicht leistet

- **Der Bildtext des Vorbilds fehlt.** Unknown Frequencies fährt in jedem
  Thumbnail 1–7 Wörter mit 10,4 % Versalhöhe und im Video „viel Text, groß,
  häufig". Unsere Prompts schließen Text aus. Ob der Balkenkopf **neben** einer
  Schlagzeile trägt, ist laut Elementtest ausdrücklich ungeprüft.
- **Die Cut-out-Figurenbewegung ist nur angenähert.** Das Vorbild rotiert
  Gliedmaßen um Gelenkpunkte. Zwei ffmpeg-Ebenen erzeugen Tiefe, aber keine
  Gliedmaßenbewegung. Wer das will, braucht entweder Clips oder eine
  Rigging-Stufe, die es in der Pipeline nicht gibt.
- **Die Serienstabilität des Balkenkopfs ist an vier Szenen geprüft, nicht an
  84.** Der Elementtest nennt das selbst: „Vier Szenen sind vier
  Datenpunkte." Vor dem Produktionslauf gehört ein Stichprobenlauf über 10–15
  Motive mit wechselnden Haltungen — Rückenansicht, starke Seitenansicht und
  Nahaufnahme sind **unbekanntes Gelände**.
- **Federschmuck kommt in Video 1 nicht vor.** Das Kopfbedeckungs-Set dieses
  Videos ist Kapuze, Kopftuch, Stirnband, Reiterkappe, Bronzehelm.

## Anschluss

1. Stichprobenlauf: 10–15 Motive mit wechselnden Haltungen, Balkengeometrie
   messen wie in `stil-uf-element/_bewertung.py`.
2. Bei Freigabe: 84 Motive in Stapeln generieren, danach die 38
   zweiten Ebenen, zuletzt die 6 Clips.
3. `render.py` braucht eine Fahrtenliste je Einstellung — die Spalte **Fahrt**
   ist bereits im Format der Pipeline gehalten.