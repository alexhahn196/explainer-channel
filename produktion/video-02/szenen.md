# Szenenliste — Video 2, „How Do We Know How Far Away the Stars Are?"

> **Erzeugt aus `szenenplan.py`, nicht getippt.** Jedes Motiv ist ein
> Datensatz mit Pflichtfeldern; fehlt eines, bricht der Generator ab,
> bevor eine Zeile Markdown entsteht. Der Wortlaut jeder Einstellung
> wird gegen `skript.md` geprüft — die Aneinanderreihung aller
> Einstellungen muss den Sprechtext exakt ergeben.
> **0 Credits verbraucht**, keine Bildgenerierung; Preise nur per
> `get_cost`-Preflight am 2026-08-16.

## Wie zu lesen

- **Motiv** = ein zu generierendes Bild. Mehrere Einstellungen mit
  demselben Motiv teilen sich **ein** Bild und unterscheiden sich nur
  durch die Kamerafahrt.
- **Fahrt** = was `ffmpeg` über dem Standbild fährt: `Zoom rein`,
  `Zoom raus`, `Schwenk links`, `Schwenk rechts`, `statisch`.
- **Licht** ist Pflichtfeld und kennt genau drei Formen: `sichtbar:`
  (die Quelle steht **im Bild**), `Schatten:` (Quelle außerhalb, aber
  eindeutig gerichteter harter Schatten), `Durchlicht:`. Bei Video 1
  konnten 27 von 62 Raumbildern die Quelle physisch nicht zeigen, weil
  der Plan sie nie verlangt hatte. Der Generator lehnt jetzt jede
  Zeile ab, die eine Quelle als sichtbar deklariert und sie im selben
  Satz aus dem Bild schiebt.
- **Ort** nennt Epoche und Ort, auch bei figurenlosen Motiven.
- **Flora** ist bedingt formuliert: eine Grenze dessen, was hier
  wachsen darf, keine Aufforderung, Pflanzen hinzuzufügen.
- **Framing** dreifach: `ganz` (Ganzfigur), `ohne` (keine Figur),
  `teil` (Körperteil-Nahaufnahme).
- **Zustandspaar** = zwei Bilder derselben Komposition in zwei
  Zuständen. Spart kein Bild, aber die Wiedererkennung ist der Grund,
  warum eine Einstellung kürzer als drei Sekunden stehen darf.
- **Ebenen** = Vorder- und Hintergrund werden getrennt generiert,
  damit `ffmpeg` sie unterschiedlich schnell bewegen kann.

## Stilbindung

Gilt für jeden Prompt, ohne Ausnahme:

- **V2-Machart** aus `stil-figuren/lauf2-erwachsen/README.md`,
  erwachsene Figuren, **Z3-Lichtführung**.
- **Kein Türkis, keine Themenpalette.** Beides ist am 15.08.2026
  ersatzlos entfallen; die Farbwelt ist natürlich.
- **Getrennte Farbsätze.** Weltbilder tragen den Naturfarbsatz,
  Schemata den Schemafarbsatz — kein Himmel, keine Vegetation, ein
  ruhiger einfarbiger Grund. Bei Video 1 war das eine Regel für alle,
  und ein Diagramm bekam prompt blauen Himmel und Gras.
- **Kein Text im Bild.** `no text, no letters, no watermark, no logo`.
  Wo eine Zahl tragen muss, trägt sie die Stimme.

## Entscheidung: die historischen Personen

Sieben Motive zeigen eine historisch belegte Person (M17, M19, M24, M34, M55, M69, M75).
**Alle sieben sind Epochenfiguren ohne Portraitähnlichkeit.** Sie sind
über Kleidung, Haltung, Gerät und Ort beschrieben, nie über ein
Gesicht. Kein Bildtext nennt einen Namen — der Generator prüft das und
bricht ab, wenn doch einer darin steht, denn ein Name im Prompt ist
die Anweisung, ein Gesicht zu treffen.

Zwei Merkmale sind dabei bewusst weggelassen worden: Tycho Brahes
Metallnase und Hubbles Pfeife. Beide sind das eine Attribut, an dem
eine Figur aufhört, „ein Astronom dieser Zeit" zu sein, und anfängt,
eine bestimmte Person zu sein. Die Epoche tragen Halskrause und
Mauerquadrant beziehungsweise Tweed und Spiegelteleskop ohnehin.

## Szenentabelle

| # | ab | s | Motiv | Fahrt | Wortlaut |
|---:|---:|---:|---|---|---|
| | | | | | **— Absatz 1 —** |
| 1 | 0:00,0 | 3,0 | M01 | Zoom rein | Look up tonight and pick a star. Any star you like. |
| 2 | 0:03,0 | 2,5 | M01 | statisch | Now ask yourself: how far away is that thing? |
| 3 | 0:05,5 | 2,5 | M02 | Zoom raus | If you draw a blank, you're in good company. |
| 4 | 0:07,9 | 2,5 | M03 | Zoom raus | In a survey of more than three thousand people, |
| 5 | 0:10,4 | 3,6 | M03 | Zoom rein | one in four said the stars are closer to us than the Sun. |
| 6 | 0:14,0 | 4,7 | M04 | Schwenk rechts | Asked to put a number on the nearest star, five out of six students wouldn't even guess. |
| 7 | 0:18,6 | 3,6 | M05 | Zoom rein | Of those who did, only one in five landed in the right range |
| 8 | 0:22,2 | 1,9 | M05 | statisch | — about three people in a hundred. |
| 9 | 0:24,1 | 3,6 | M06 | Zoom rein | So how do astronomers know? Here's the answer, right away: with a triangle. |
| 10 | 0:27,7 | 2,5 | M07 | statisch | No probe flies out there. No radar comes back. |
| 11 | 0:30,1 | 4,1 | M06 | Schwenk rechts | You measure an angle, twice, half a year apart — and geometry does the rest. |
| 12 | 0:34,2 | 4,7 | M09 | Zoom rein | And you already own the trick. Hold up your thumb at arm's length. Shut your left eye. |
| | | | | | **— Absatz 2 —** |
| 13 | 0:38,9 | 2,5 | M10 | statisch | Now swap eyes. Your thumb jumps against the wall |
| 14 | 0:41,4 | 3,0 | M11 | Zoom rein | — because each of your eyes looks from its own spot. |
| 15 | 0:44,4 | 2,5 | M11 | statisch | Two viewpoints, one shift: that's how you see depth. |
| 16 | 0:46,8 | 5,2 | M12 | Zoom raus | To do the same with a star, you need two viewpoints as far apart as you can get them. |
| 17 | 0:52,1 | 4,9 | M12 | Schwenk rechts | The farthest pair you will ever own is this: the Earth in January, and the Earth in July. |
| 18 | 0:57,0 | 3,0 | M12 | Zoom rein | Two points of your planet's orbit, three hundred million kilometres apart. |
| 19 | 1:00,0 | 3,8 | M13 | statisch | Photograph a near star from both. Against the sea of far stars behind it, |
| 20 | 1:03,8 | 2,2 | M14 | statisch | it jumps — just like your thumb did. |
| 21 | 1:06,0 | 3,0 | M06 | Zoom rein | Half of that jump, as an angle, is called the parallax. |
| 22 | 1:09,0 | 4,1 | M15 | Schwenk rechts | One clean rule ties it to distance: the smaller the jump, the farther the star. |
| | | | | | **— Absatz 3 —** |
| 23 | 1:13,2 | 5,5 | M16 | Zoom raus | Simple? You'd think so. The catch: from the idea to the first published jump took two hundred and ninety-five years. |
| | | | | | **— Absatz 4 —** |
| 24 | 1:18,6 | 3,6 | M17 | Zoom rein | Copernicus set the Earth moving in 1543, and the objection came at once: |
| 25 | 1:22,2 | 2,7 | M18 | Schwenk rechts | if we ride a moving platform, the stars should sway |
| 26 | 1:24,9 | 1,6 | M18b | statisch | — and nobody saw any sway. |
| 27 | 1:26,6 | 2,7 | M19 | Zoom rein | The sharpest eyes of that century belonged to Tycho Brahe, |
| 28 | 1:29,3 | 4,1 | M19 | Schwenk links | a Danish noble who charted the sky, with no telescope, more finely than anyone alive. |
| 29 | 1:33,4 | 3,0 | M20 | Zoom rein | He looked. Nothing. Then he did the maths on that nothing: |
| 30 | 1:36,4 | 4,9 | M21 | Zoom raus | to hide from his instruments, the stars would have to sit seven hundred times farther out than Saturn. |
| 31 | 1:41,4 | 3,3 | M22 | Zoom rein | Worse: to his eye, every bright star showed a tiny round disk. |
| 32 | 1:44,7 | 4,9 | M23 | Zoom raus | A disk that wide, pushed that far out, means a star of monstrous size — dwarfing the Sun. |
| 33 | 1:49,6 | 3,0 | M24 | statisch | Too absurd to accept, he judged, and kept the Earth still. |
| 34 | 1:52,6 | 2,2 | M24 | Zoom rein | His logic was sound. His premise was not. |
| 35 | 1:54,8 | 4,1 | M25 | statisch | The disks are not real. Air and eye wrap every point of light in blur, |
| 36 | 1:58,9 | 1,9 | M22 | Zoom rein | and what Tycho measured was the blur. |
| 37 | 2:00,8 | 5,2 | M26 | Zoom raus | The largest true star disk in our night sky is about a thousand times smaller than what he saw. |
| 38 | 2:06,0 | 3,3 | M27 | Zoom rein | It took until around 1700 to accept the disks as an illusion |
| 39 | 2:09,3 | 2,7 | M27 | Schwenk rechts | — an "optick fallacy," as it was put back then. |
| 40 | 2:12,1 | 4,7 | M22 | Zoom rein | Tycho wasn't sloppy. He measured what a human eye can see — it just wasn't the star. |
| | | | | | **— Absatz 5 —** |
| 41 | 2:16,7 | 3,6 | M28 | Zoom raus | The hunt ran on — into the 1830s, when it became a race. |
| 42 | 2:20,3 | 1,6 | M28 | Schwenk rechts | Three men, three cities, three stars. |
| | | | | | **— Absatz 6 —** |
| 43 | 2:21,9 | 2,7 | M29 | Zoom rein | In Königsberg, Friedrich Bessel had a new tool: a telescope |
| 44 | 2:24,7 | 4,1 | M30 | Zoom rein | whose main lens was cut clean in half, one half sliding on a fine screw. |
| 45 | 2:28,8 | 2,7 | M31 | statisch | Slide it until two star images meet, read the screw, |
| 46 | 2:31,5 | 2,5 | M32 | statisch | and you've read an angle no eye could split. |
| 47 | 2:34,0 | 5,2 | M33 | Schwenk rechts | He aimed at a dim star called 61 Cygni — picked because it crawls across the sky unusually fast. |
| 48 | 2:39,2 | 5,2 | M33 | Zoom rein | An Italian, Giuseppe Piazzi, had spotted that hurry in 1792 — a fast star is usually a near one. |
| 49 | 2:44,4 | 2,5 | M34 | Zoom rein | Through 1837 and 1838 Bessel measured; then he published: |
| 50 | 2:46,8 | 2,5 | M34 | statisch | a jump of about a third of an arcsecond. |
| 51 | 2:49,3 | 4,4 | M35 | Zoom rein | An arcsecond — take one degree, cut it into three thousand six hundred slices, keep one. |
| 52 | 2:53,7 | 2,7 | M36 | Zoom raus | Bessel's angle is a two-euro coin seen from seventeen kilometres. |
| 53 | 2:56,4 | 3,0 | M37 | Zoom raus | From it he got a distance of ten point four light-years |
| 54 | 2:59,5 | 4,7 | M37 | Schwenk rechts | — a light-year being the stretch light crosses in one year, nine and a half trillion kilometres. |
| 55 | 3:04,1 | 4,1 | M38 | statisch | Today's value for that star: eleven point four. With a sawn lens and a screw, |
| 56 | 3:08,2 | 2,2 | M38 | Zoom rein | he came within a tenth of the truth. |
| | | | | | **— Absatz 7 —** |
| 57 | 3:10,4 | 4,1 | M39 | Zoom raus | But he wasn't first to measure. Five years before, at the Cape of Good Hope, |
| 58 | 3:14,5 | 3,6 | M39 | Schwenk links | Thomas Henderson had caught the jump of a bright southern star, Alpha Centauri |
| 59 | 3:18,1 | 4,7 | M40 | Zoom rein | — and put the result in a drawer. Earlier claims of a parallax had been shot down; |
| 60 | 3:22,7 | 3,0 | M40 | statisch | the story handed down says he didn't trust his own numbers. |
| 61 | 3:25,8 | 2,7 | M40 | Zoom raus | He published in 1839 — second, for want of nerve. |
| 62 | 3:28,5 | 3,8 | M41 | Zoom rein | And in Dorpat, Wilhelm Struve had measured Vega and landed close to today's value |
| 63 | 3:32,3 | 3,3 | M42 | Zoom rein | — 0.125 arcseconds, against the modern 0.129. Then Bessel doubted Struve's data, |
| 64 | 3:35,6 | 3,6 | M43 | statisch | and Struve revised his good number to nearly double. Away from the truth. |
| 65 | 3:39,2 | 1,4 | M43 | Zoom raus | Colleagues stopped trusting his numbers. |
| 66 | 3:40,5 | 3,0 | M44 | statisch | So who was first? Pick your rule. First to measure: Henderson. |
| 67 | 3:43,6 | 2,5 | M44 | Schwenk rechts | First to make the full case in print: Bessel. |
| 68 | 3:46,0 | 5,2 | M44 | Zoom raus | First to print any number at all: arguably Struve. The books give all three answers — side by side. |
| | | | | | **— Absatz 8 —** |
| 69 | 3:51,2 | 3,6 | M45 | Zoom raus | You'd think it gets easy after that. It doesn't. The angles are brutal. |
| 70 | 3:54,8 | 4,1 | M45 | Zoom rein | By 1900 — sixty years on — astronomers had collected about sixty parallaxes in total. |
| 71 | 3:58,9 | 2,2 | M45 | Schwenk rechts | Sixty known distances, in a galaxy of billions. |
| 72 | 4:01,1 | 2,5 | M46 | Zoom raus | The real jump came when measuring left the ground. |
| 73 | 4:03,6 | 3,0 | M46 | Schwenk rechts | A satellite called Hipparcos pinned down 118,000 stars in the 1990s |
| 74 | 4:06,6 | 4,1 | M47 | Zoom rein | — though only about one in six of them with an error under ten percent. |
| 75 | 4:10,7 | 5,8 | M48 | Schwenk links | Then came Gaia, a European craft that scanned the sky from 2013 to 2025 and measured more than a billion stars. |
| 76 | 4:16,4 | 3,8 | M49 | Zoom raus | At its sharpest — on paper — its angle is that same two-euro coin, |
| 77 | 4:20,3 | 3,0 | M49 | Zoom rein | now seen from 759,000 kilometres, twice as far as the Moon. |
| 78 | 4:23,3 | 2,5 | M50 | Zoom raus | Still: the triangle runs out inside our own galaxy. |
| 79 | 4:25,8 | 3,6 | M50 | Schwenk rechts | The Milky Way spans some 87,000 light-years, give or take a few thousand |
| 80 | 4:29,3 | 3,6 | M50 | Zoom rein | — and for most stars, Gaia's sharp reach covers a slice of that. |
| 81 | 4:32,9 | 4,4 | M51 | Zoom rein | Past it, the jump drowns in noise. No bigger telescope changes the base of the triangle |
| 82 | 4:37,3 | 3,3 | M51 | statisch | — and past a point, the jump is smaller than the blur. |
| | | | | | **— Absatz 9 —** |
| 83 | 4:40,5 | 4,4 | M52 | Zoom raus | Everything farther — every other galaxy, the deep sky — stands on something else. A ladder. |
| 84 | 4:44,9 | 3,8 | M53 | Zoom rein | And its second rung was built by a woman paid thirty cents an hour. |
| | | | | | **— Absatz 10 —** |
| 85 | 4:48,8 | 3,3 | M54 | Zoom raus | Harvard, 1908 to 1912. Henrietta Leavitt worked in a room of women |
| 86 | 4:52,1 | 2,2 | M54 | Schwenk rechts | hired to read glass photographs of the sky |
| 87 | 4:54,2 | 4,9 | M54 | Zoom rein | — plates taken by the men who ran the telescopes, and brought in for the women to measure. |
| 88 | 4:59,2 | 3,6 | M56 | Zoom raus | Her plates showed the Small Magellanic Cloud, a small companion galaxy of ours. |
| 89 | 5:02,7 | 3,6 | M57 | statisch | On them she found stars that pulse: they brighten, fade, and brighten again, |
| 90 | 5:06,3 | 2,2 | M58 | statisch | on a steady beat of days or weeks. |
| 91 | 5:08,5 | 1,4 | M57 | Zoom rein | We now call them Cepheids. |
| 92 | 5:09,9 | 4,4 | M55 | Zoom rein | Across twenty-five of them, she found the pattern: the slower the beat, the brighter the star. |
| 93 | 5:14,2 | 3,0 | M59 | Zoom raus | On her chart, the points fell along two clean straight lines. |
| 94 | 5:17,3 | 5,2 | M55 | statisch | And she wrote down, herself, what it meant: these stars all sit at roughly the same distance from us |
| 95 | 5:22,5 | 5,2 | M56 | Zoom rein | — they share the Cloud — so the beat apparently tracks how much light a star truly puts out. |
| 96 | 5:27,7 | 2,7 | M59 | Zoom rein | Hold on to that — it unlocks the deep universe. |
| 97 | 5:30,4 | 2,7 | M60 | statisch | Read a Cepheid's rhythm, and you know its true brightness. |
| 98 | 5:33,2 | 3,8 | M61 | Schwenk rechts | Compare that with how faint it looks, and the dimming hands you the distance. |
| 99 | 5:37,0 | 3,6 | M60 | Zoom rein | Astronomers call that a standard candle: a lamp whose true output you know. |
| 100 | 5:40,5 | 4,4 | M61 | Zoom raus | Hers could be read across millions of light-years. One catch — and she named it too. |
| | | | | | **— Absatz 11 —** |
| 101 | 5:44,9 | 3,8 | M62 | Zoom rein | Her chart had no scale. No one knew the distance to the Cloud itself, |
| 102 | 5:48,8 | 4,1 | M62 | statisch | so her law gave only ratios: this star is four times farther than that one. |
| 103 | 5:52,9 | 0,8 | M62 | Zoom raus | Four times what? |
| 104 | 5:53,7 | 4,4 | M55 | Zoom rein | She wrote that she hoped parallaxes would be measured for a few stars of this kind. |
| 105 | 5:58,1 | 4,1 | M63 | Zoom raus | A year on, Ejnar Hertzsprung found a rough scale — not by one clean triangle, |
| 106 | 6:02,2 | 2,7 | M63 | Zoom rein | but by pooling the slow drift of thirteen nearby Cepheids. |
| | | | | | **— Absatz 12 —** |
| 107 | 6:04,9 | 4,9 | M64 | Schwenk links | Her paper ran under her director's signature; its first line records that it was "prepared by Miss Leavitt". |
| 108 | 6:09,9 | 4,7 | M65 | Zoom rein | In 1925, a Swedish mathematician wrote to her about putting her name up for the Nobel Prize |
| 109 | 6:14,5 | 2,7 | M65 | statisch | — not knowing she had been dead for four years. |
| | | | | | **— Absatz 13 —** |
| 110 | 6:17,3 | 4,7 | M66 | Zoom raus | Mark that shape — everything since is built the same way: rung two stands on rung one. |
| 111 | 6:21,9 | 1,4 | M66 | Zoom rein | Cepheids are calibrated by parallax. |
| 112 | 6:23,3 | 3,6 | M66 | Schwenk rechts | The rungs above — exploding stars, whole galaxies — are calibrated by Cepheids. |
| 113 | 6:26,8 | 4,1 | M67 | Zoom rein | Every rung inherits the reach of the one below. And every rung inherits its errors. |
| | | | | | **— Absatz 14 —** |
| 114 | 6:31,0 | 3,0 | M68 | Zoom rein | And the errors came. The ladder has snapped twice, in public. |
| | | | | | **— Absatz 15 —** |
| 115 | 6:34,0 | 2,5 | M69 | Zoom rein | First break. In 1929, Edwin Hubble used Cepheid distances |
| 116 | 6:36,4 | 3,6 | M70 | Zoom raus | to show that the galaxies flee from us — the farther, the faster. |
| 117 | 6:40,0 | 3,3 | M71 | Zoom rein | The universe expands; run that film backwards, and you get an age. |
| 118 | 6:43,3 | 3,0 | M72 | statisch | His rate gave: not quite two billion years. Awkward, even then |
| 119 | 6:46,3 | 2,7 | M72 | Zoom rein | — geologists put the Earth itself at around two billion. |
| 120 | 6:49,0 | 4,9 | M73 | statisch | By the mid-fifties it turned absurd: the Earth's true age came in at four and a half billion |
| 121 | 6:54,0 | 1,9 | M73 | Zoom rein | — older than the universe around it. |
| 122 | 6:55,9 | 4,1 | M74 | Zoom raus | Part of the fault lay on Leavitt's rung. There are two families of pulsing stars, |
| 123 | 6:60,0 | 3,0 | M74 | Schwenk rechts | with two different rulers, and mixing them had shrunk the cosmos. |
| 124 | 7:03,0 | 3,3 | M75 | Zoom rein | Walter Baade pulled them apart and announced it in Rome, in 1952 |
| 125 | 7:06,3 | 2,7 | M76 | Zoom raus | — at a stroke, the universe doubled. Still too small. |
| 126 | 7:09,0 | 4,4 | M77 | Zoom rein | In 1958, Allan Sandage found that Hubble had also mistaken glowing gas clouds for bright stars. |
| 127 | 7:13,4 | 3,8 | M73 | Zoom raus | The rate fell again, and the universe came out comfortably older than the Earth. |
| 128 | 7:17,3 | 2,7 | M78 | Schwenk rechts | Total correction, first to last: about a factor of seven. |
| | | | | | **— Absatz 16 —** |
| 129 | 7:20,0 | 4,7 | M79 | Zoom rein | Second break, closer to home. The Pleiades — the little cluster you can spot with bare eyes. |
| 130 | 7:24,7 | 2,7 | M80 | statisch | Hipparcos, the trusted satellite, put it at about 390 light-years. |
| 131 | 7:27,4 | 2,2 | M80 | Zoom rein | Nearly every other method said 435 to 445. |
| 132 | 7:29,6 | 3,0 | M80 | Zoom raus | For seventeen years, the field's best instrument disagreed with everyone else |
| 133 | 7:32,6 | 4,4 | M82 | Schwenk rechts | — about one of the nearest clusters in the sky. In 2014, radio telescopes settled it: |
| 134 | 7:37,0 | 3,0 | M81 | Zoom rein | 444 light-years, give or take four — the satellite was wrong. |
| | | | | | **— Absatz 17 —** |
| 135 | 7:40,0 | 2,5 | M84 | Zoom raus | And today, the ladder is in its third fight |
| 136 | 7:42,5 | 3,6 | M85 | statisch | — this one still open. Two numbers for how fast the universe grows. |
| 137 | 7:46,0 | 4,9 | M83 | Zoom rein | From the oldest light there is, the Planck satellite reads 67.4, with an error of half a point. |
| 138 | 7:51,0 | 5,5 | M84 | Schwenk rechts | From the ladder — parallax, to Cepheids, to exploding stars that all flare to nearly the same true brightness — |
| 139 | 7:56,4 | 2,7 | M85 | Zoom rein | a team called SH0ES reads 73.0, plus or minus one. |
| 140 | 7:59,2 | 3,6 | M85 | Zoom raus | A five-sigma difference, in their own words: far too large to be chance. |
| 141 | 8:02,7 | 2,7 | M83 | Zoom raus | You'll hear that sold as the early universe against today's. |
| 142 | 8:05,5 | 3,6 | M86 | statisch | But here's what that framing skips. A second team climbed the same ladder |
| 143 | 8:09,0 | 3,3 | M86 | Zoom rein | with a different second rung — red giant stars instead of Cepheids, |
| 144 | 8:12,3 | 2,7 | M86 | Schwenk rechts | with the new James Webb telescope in the mix — |
| 145 | 8:15,1 | 3,3 | M87 | Zoom raus | and read 67.8 to 70.4, depending on the sample and the method. |
| 146 | 8:18,4 | 1,9 | M87 | statisch | Their own verdict: no new physics needed. |
| 147 | 8:20,3 | 2,5 | M87 | Zoom rein | Same universe. Same ladder. Different rung — different answer. |
| 148 | 8:22,7 | 5,2 | M88 | Zoom rein | And the strangest part: both teams agree on the distances to the very same galaxies, to about one percent. |
| 149 | 8:27,9 | 1,6 | M88 | statisch | The stars are not the quarrel. |
| 150 | 8:29,6 | 3,3 | M89 | Zoom raus | The quarrel is over which exploding stars to hang the scale on. |
| 151 | 8:32,9 | 4,4 | M89 | Zoom rein | The ladder holds; the argument is about the nail. Nobody yet knows which side is right. |
| | | | | | **— Absatz 18 —** |
| 152 | 8:37,3 | 3,3 | M90 | Zoom raus | So — how do we know how far away the stars are? |
| 153 | 8:40,5 | 3,8 | M90 | Zoom rein | For the near ones: a triangle. Your thumb trick, stretched across the Earth's orbit, |
| 154 | 8:44,4 | 3,0 | M49 | Zoom rein | sharpened until a coin past the Moon is an easy target. |
| 155 | 8:47,4 | 2,7 | M91 | Zoom raus | For the far ones: a ladder of light. A rhythm |
| 156 | 8:50,1 | 2,5 | M53 | Zoom rein | read off glass plates for thirty cents an hour, |
| 157 | 8:52,6 | 3,6 | M91 | Zoom rein | nailed to the triangle, broken twice, patched twice, and argued over right now. |
| 158 | 8:56,2 | 4,1 | M03 | Zoom rein | One in four of the people asked thinks the stars hang closer than the Sun. |
| 159 | 9:00,3 | 4,7 | M37 | Zoom rein | The nearest one sits so deep that its light spends four years on the road to you. |
| 160 | 9:04,9 | 3,6 | M90 | Zoom raus | But that number is no guess, and never was. Someone caught its jump. |
| 161 | 9:08,5 | 3,6 | M92 | statisch | Someone read its beat. And beside every distance, they wrote a second number: |
| 162 | 9:12,1 | 3,6 | M93 | Zoom rein | how far off it might be. That second number is the honest answer. |
| 163 | 9:15,6 | 2,5 | M02 | Zoom raus | We don't just know how far the stars are. |
| 164 | 9:18,1 | 3,6 | M02 | Zoom rein | We know how well we know it — and exactly where we don't. |

## Motivkatalog

Der `szene`-Text ist der `SCENE:`-Teil des Prompts, nicht der ganze
Prompt — das Stilgerüst kommt davor, die Ausschlussklausel danach.

**M01** · 2 Einstellungen · getrennte Ebenen
- Bild: Aufsicht von unten in einen Nachthimmel voller Sterne, einer davon etwas heller als die übrigen; unten im Bild die dunkle Silhouette einer Dachkante
- Licht: sichtbar: die Sterne selbst, sonst nichts
- Ort: Gegenwart, eine Wohnstraße bei Nacht
- Framing: ohne

**M02** · 3 Einstellungen · getrennte Ebenen · **geschützter Moment**
- Bild: Dieselbe Person von hinten, klein, den Kopf in den Nacken gelegt, vor dem Sternhimmel; um sie herum nichts als leerer Raum
- Licht: sichtbar: die Sterne
- Ort: Gegenwart, dieselbe Straße
- Framing: ganz

**M03** · 3 Einstellungen · Schema
- Bild: Vier gleich große Figurenumrisse nebeneinander; über JEDER stehen eine Sonne und ein Stern übereinander. Bei dreien hängt die Sonne tiefer, bei der vierten hängt der Stern tiefer
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-A: Ohne Beschriftung lesbar, weil der Abstand selbst die Aussage ist. Wichtig: beide Himmelskörper müssen über JEDER Figur stehen — bekäme die vierte nur den Stern und die anderen nur die Sonne, gäbe es nichts zu vergleichen und die eine Abweichung wäre unsichtbar.

**M04** · 1 Einstellung · Schema
- Bild: Sechs Figurenumrisse in einer Reihe, über jedem eine leere Gedankenblase; fünf Blasen sind völlig leer, in der sechsten stehen ein Stern und eine kurze Maßlinie darunter
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-B: Fünf leere Blasen, eine gefüllte. Leer = keine Antwort, Stern mit Maßlinie = eine Entfernung genannt. Ohne Text verständlich, und die Fünf-zu-Eins ist abzählbar.

**M05** · 2 Einstellungen · Schema
- Bild: Ein Raster aus hundert gleichen Punkten, drei davon deutlich dunkler und größer
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-C: Drei von hundert, rein durch Abzählbarkeit.

**M06** · 3 Einstellungen · Schema · **geschützter Moment**
- Bild: Das Parallaxendreieck: die Erdbahn als flache Ellipse, die Erde an zwei gegenüberliegenden Punkten, von beiden je eine lange gestrichelte Sichtlinie zu einem nahen Stern; der Winkel zwischen den Linien als schmaler Keil; dahinter ein Feld ferner Sterne
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D1 — DAS Grundbild. Ohne Beschriftung lesbar, weil zwei Standpunkte, zwei Linien und ein Keil die ganze Aussage sind. Keine Winkelmaße, keine Achsen, keine Buchstaben nötig. BEDINGUNG: der nahe Stern muss deutlich größer und heller sein als das Feld dahinter. Geht er darin unter, scheint der Keil an einem Hintergrundstern zu sitzen, und das Bild zeigt die falsche Messung.

**M07** · 1 Einstellung · Schema
- Bild: Eine Raumsonde und eine Radarschüssel nebeneinander, beide von einem breiten diagonalen Balken durchgestrichen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-D: Durchstrichener Gegenstand — die geläufigste Verneinungsgeste, ohne Text eindeutig.

**M09** · 1 Einstellung · Zustandspaar mit M10
- Bild: Derselbe Daumen vor derselben Wand, der Daumen sitzt links von einem Bildhaken an der Wand
- Licht: Schatten: hart von links
- Ort: Gegenwart, dasselbe Zimmer
- Framing: teil

**M10** · 1 Einstellung · Zustandspaar mit M09
- Bild: Exakt dieselbe Aufnahme, aber der Daumen sitzt jetzt rechts vom Bildhaken — Bildausschnitt und Kameraposition identisch
- Licht: Schatten: hart von links
- Ort: Gegenwart, dasselbe Zimmer
- Framing: teil

**M11** · 2 Einstellungen · Schema
- Bild: Zwei Augen im Profil, von jedem geht eine Linie zu einem nahen Gegenstand und weiter auf eine Rückwand; die beiden Treffpunkte auf der Wand liegen auseinander
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D2: Zwei Augen, zwei Linien, zwei Treffpunkte. Der Versatz ist die Aussage und braucht keine Beschriftung.

**M12** · 3 Einstellungen · Schema
- Bild: Die Sonne in der Mitte, die Erdbahn als Ellipse darum, die Erde einmal links und einmal rechts auf der Bahn; zwischen den beiden Erden eine gerade Verbindungslinie quer durch die Bahn
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-E: Zwei Erden auf einer Bahn, eine Strecke dazwischen. Die Länge trägt die Stimme, nicht das Bild.

**M13** · 1 Einstellung · Zustandspaar mit M14
- Bild: Ein rechteckiger Bildausschnitt des Sternhimmels, ein Stern darin links von zwei Hintergrundsternen
- Licht: sichtbar: die Sterne
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M14** · 1 Einstellung · Zustandspaar mit M13
- Bild: Derselbe Ausschnitt, derselbe Himmel — nur der eine Stern sitzt jetzt rechts von den beiden Hintergrundsternen
- Licht: sichtbar: die Sterne
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M15** · 1 Einstellung · Schema
- Bild: Zwei Sterne über einer gemeinsamen Grundlinie: der nahe mit einem weiten Doppelpfeil-Versatz, der ferne mit einem winzigen; die Sichtlinien laufen jeweils zu denselben zwei Standpunkten
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D4 ERSETZT: Statt der Hyperbel d = 1/p zwei nebeneinander gestellte Fälle. Eine Kurve ohne Achsenbeschriftung wäre bedeutungslos — zwei Sterne mit großem und kleinem Versatz sind ohne ein einziges Zeichen verständlich.

**M16** · 1 Einstellung · Schema
- Bild: Ein waagerechter Zeitstrahl, ganz links ein Markierungsstrich, ganz rechts ein zweiter, dazwischen eine sehr lange leere Strecke
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-F: Die Leere zwischen zwei Marken IST die Aussage. Ohne Jahreszahlen lesbar; die Zahl trägt die Stimme.

**M17** · 1 Einstellung · Epochenfigur · getrennte Ebenen
- Bild: Ein Mann in Talar und Barett des 16. Jahrhunderts beugt sich über einen Tisch, auf dem eine Armillarsphäre steht; er schiebt eine kleine Kugel von der Mitte an den Rand
- Licht: sichtbar: eine Kerze auf dem Tisch
- Ort: Frauenburg im Ermland, 1543
- Flora: Innenraum, keine Vegetation; spätgotische Fensternische, Holzbalkendecke
- Framing: ganz

**M18** · 1 Einstellung · Schema · Zustandspaar mit M18b
- Bild: Derselbe Sternhimmel zweimal übereinander im selben Bild, die obere Hälfte gegen die untere deutlich seitlich versetzt, dazwischen ein schmaler Zwischenraum
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-G: Zwei Himmel, gegeneinander verschoben — die erwartete Schwankung. Ohne Text verständlich, weil der Versatz selbst der Inhalt ist.

**M18b** · 1 Einstellung · Schema · Zustandspaar mit M18
- Bild: Exakt dasselbe Bild, derselbe Ausschnitt, dieselben zwei Himmel — nur liegt jeder Stern der oberen Hälfte jetzt genau über seinem Gegenstück in der unteren, ohne jeden Versatz
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-Gb: Zustand B. Das AUSBLEIBEN der Schwankung ist der Inhalt des Satzes und lässt sich nur als zweiter Zustand zeigen — auf dem Bild der erwarteten Schwankung stehenzubleiben, während die Stimme sagt, dass niemand eine sah, hätte das Gegenteil behauptet.

**M19** · 2 Einstellungen · Epochenfigur · getrennte Ebenen
- Bild: Ein bärtiger Mann in Wams und Halskrause steht an einem großen Mauerquadranten aus Messing, dem Auge an der Visiereinrichtung; kein Fernrohr im Bild
- Licht: sichtbar: der Nachthimmel durch eine offene Dachluke
- Ort: Uraniborg auf der Insel Ven, um 1580
- Flora: Innenraum einer Sternwarte, Backsteinnischen, keine Vegetation
- Framing: ganz

**M20** · 1 Einstellung
- Bild: Dieselbe Visiereinrichtung in Nahaufnahme, die Skala daneben, der Zeiger steht exakt auf einem Teilstrich und rührt sich nicht
- Licht: Schatten: hart von oben rechts
- Ort: Uraniborg auf der Insel Ven, um 1580
- Framing: teil

**M21** · 1 Einstellung · Schema
- Bild: Ein Ringplanet auf halber Bildhöhe, davon nach rechts eine gestrichelte Strecke; ganz rechts, weit dahinter, ein einzelner Stern — die Strecke dazwischen vielfach länger
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-H: Zwei Abstände im Größenverhältnis. Der Faktor trägt die Stimme; das Bild zeigt nur, dass der zweite ungleich größer ist.

**M22** · 3 Einstellungen · Zustandspaar mit M25
- Bild: Extreme Nahaufnahme eines einzelnen Sterns, wie ihn ein bloßes Auge sieht: eine kleine runde Scheibe mit weichem Rand
- Licht: sichtbar: der Stern selbst
- Ort: zeitlos, Blick zum Nachthimmel
- Framing: ohne

**M23** · 1 Einstellung · Schema
- Bild: Größenvergleich nebeneinander: links eine kleine Sonne, rechts eine Kugel, die ein Vielfaches davon misst und über den Bildrand hinaus angedeutet ist
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-I: Zwei Kreise im Größenverhältnis, der größere angeschnitten. Ohne Beschriftung lesbar.

**M24** · 2 Einstellungen · Epochenfigur
- Bild: Derselbe Mann an seinem Quadranten wendet sich ab; im Hintergrund eine ruhende Erdkugel auf einem Sockel
- Licht: sichtbar: eine Öllampe an der Wand
- Ort: Uraniborg auf der Insel Ven, um 1580
- Flora: Innenraum, keine Vegetation
- Framing: ganz

**M25** · 1 Einstellung · Zustandspaar mit M22
- Bild: Dieselbe Nahaufnahme desselben Sterns, aber die Scheibe ist verschwunden: ein winziger harter Punkt, umgeben von einem feinen Ring aus Beugungslicht
- Licht: sichtbar: der Stern selbst
- Ort: zeitlos, Blick zum Nachthimmel
- Framing: ohne

**M26** · 1 Einstellung · Schema
- Bild: Zwei Kreisflächen nebeneinander, die linke groß, die rechte ein kaum sichtbarer Punkt
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D6: Der Größenunterschied allein. Der Faktor tausend ist im Bild nicht abzählbar — die Stimme nennt ihn, das Bild zeigt nur, dass es sehr viel weniger ist.

**M27** · 2 Einstellungen
- Bild: Ein Fernrohr auf einem Holzstativ, daneben mehrere Männer in Perücken und Rockschößen, die sich über eine Zeichnung beugen
- Licht: sichtbar: ein Fenster mit Tageslicht
- Ort: eine europäische Sternwarte, um 1700
- Flora: Innenraum, Stuckdecke, keine Vegetation
- Framing: ganz

**M28** · 2 Einstellungen · Schema
- Bild: Eine flache Landkarte Europas mit drei markierten Punkten weit auseinander, von jedem geht eine dünne Linie nach oben zu je einem eigenen Stern
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-J: Drei Orte, drei Sterne, drei Linien. Ohne Ortsnamen verständlich, weil die Dreizahl die Aussage ist.

**M29** · 1 Einstellung · getrennte Ebenen
- Bild: Ein klassizistisches Sternwartengebäude mit Kuppel bei Nacht, davor kahle Bäume und eine gepflasterte Straße
- Licht: sichtbar: der Mond über der Kuppel
- Ort: Königsberg in Ostpreußen, 1838
- Flora: norddeutsche Stadtbäume ohne Laub — Linden und Kastanien; Backstein und Putz, keine Palmen, keine Nadelbäume
- Framing: ohne

**M30** · 1 Einstellung
- Bild: Nahaufnahme einer runden Objektivlinse, die exakt durch die Mitte durchgesägt ist; die eine Hälfte sitzt fest, die andere ist auf einer feinen Gewindeschraube seitlich verschoben
- Licht: Schatten: hart von rechts
- Ort: Königsberg in Ostpreußen, 1838
- Framing: teil

**M31** · 1 Einstellung · Zustandspaar mit M32
- Bild: Blick durch ein Okular: zwei getrennte Sternabbilder nebeneinander im runden Gesichtsfeld
- Licht: sichtbar: die Sterne im Gesichtsfeld
- Ort: Königsberg in Ostpreußen, 1838
- Framing: ohne

**M32** · 1 Einstellung · Zustandspaar mit M31
- Bild: Dasselbe runde Gesichtsfeld, dieselbe Lage — die beiden Sternabbilder liegen jetzt genau übereinander und bilden einen Punkt
- Licht: sichtbar: die Sterne im Gesichtsfeld
- Ort: Königsberg in Ostpreußen, 1838
- Framing: ohne

**M33** · 2 Einstellungen
- Bild: Ein Sternfeld, in dem ein unscheinbarer Doppelstern durch eine kurze Spur markiert ist, die seinen Weg gegenüber den Nachbarn zeigt
- Licht: sichtbar: die Sterne
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M34** · 2 Einstellungen · Epochenfigur · getrennte Ebenen
- Bild: Ein Mann in hochgeschlossenem Rock des frühen 19. Jahrhunderts sitzt am Okular eines großen Refraktors und dreht mit der rechten Hand eine Mikrometerschraube
- Licht: sichtbar: eine abgeschirmte Öllampe neben dem Instrument
- Ort: Königsberg in Ostpreußen, 1838
- Flora: Innenraum einer Kuppel, Holzdielen, keine Vegetation
- Framing: ganz

**M35** · 1 Einstellung · Schema
- Bild: Ein Kreissektor, aus dem ein einzelner haarfeiner Ausschnitt herausgehoben und daneben stark vergrößert gezeigt wird
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D3a: Ein Tortenstück und seine Lupe. Dass es 3.600 Teile sind, sagt die Stimme — das Bild zeigt nur, wie dünn eines davon ist.

**M36** · 1 Einstellung · Schema
- Bild: Eine Münze im Vordergrund und dieselbe Münze am fernen Ende einer schnurgeraden Landstraße, dort nur noch ein Pünktchen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D3b: Dasselbe Ding nah und fern. Die Entfernung trägt die Stimme; das Bild zeigt die Schrumpfung.

**M37** · 3 Einstellungen · Schema
- Bild: Ein Lichtstrahl als lange durchgehende Linie zwischen zwei Sternen, an der Linie eine einzelne Kerbe kurz hinter dem Startpunkt
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-K: Eine Strecke mit einer einzigen Kerbe nahe dem Anfang — ein Jahr gegen die ganze Reise. Ohne Text lesbar.

**M38** · 2 Einstellungen · Schema
- Bild: Zwei senkrechte Balken nebeneinander auf gemeinsamer Grundlinie, der rechte etwa ein Zehntel höher als der linke
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-L: Zwei Balken, geringer Höhenunterschied. Genau das ist die Aussage — Bessel lag knapp daneben.

**M39** · 2 Einstellungen · getrennte Ebenen
- Bild: Ein weißes Sternwartengebäude mit flachem Dach auf einem Hügelrücken, dahinter ein Tafelberg und offenes Meer
- Licht: sichtbar: die tief stehende Sonne über dem Meer
- Ort: Royal Observatory am Kap der Guten Hoffnung, 1833
- Flora: Fynbos des Kaps — silbriges Buschwerk, Proteen, niedrige Hartlaubsträucher; ausdrücklich keine Palmen, keine Akazien, keine Wüstenpflanzen
- Framing: ohne

**M40** · 3 Einstellungen
- Bild: Nahaufnahme: eine Hand legt ein beschriebenes Blatt in eine Schreibtischschublade und schiebt sie zu; kein Gesicht im Bild
- Licht: Schatten: hart von links
- Ort: Kapstadt, 1833
- Framing: teil

**M41** · 1 Einstellung · getrennte Ebenen
- Bild: Ein niedriges verputztes Observatorium mit Holzverschalung in einer winterlichen Landschaft, davor eine Schlittenspur im Schnee
- Licht: sichtbar: der Mond hinter dünnen Wolken
- Ort: Dorpat im Baltikum, 1837
- Flora: baltische Winterlandschaft — Birken und Kiefern ohne Laub, Schneedecke; keine Laubbäume in Blatt
- Framing: ohne

**M42** · 1 Einstellung · Schema · Zustandspaar mit M43
- Bild: Zwei sehr kurze waagerechte Striche übereinander, fast gleich lang, der Unterschied kaum auszumachen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-M: Zwei fast gleiche Längen. Dass sie fast gleich sind, IST die Aussage — kein Zahlenwert nötig.

**M43** · 2 Einstellungen · Schema · Zustandspaar mit M42
- Bild: Dasselbe Bild, dieselbe Anordnung — nur der obere Strich ist jetzt auf die doppelte Länge gewachsen und ragt weit über den unteren hinaus
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-N: Zustand B zu M42. Der Sprung ist ohne Beschriftung unmittelbar sichtbar.

**M44** · 3 Einstellungen · Schema
- Bild: Drei gleich große Rahmen nebeneinander, in jedem eine Figurensilhouette; über allen dreien schwebt derselbe Siegerkranz, keiner ist hervorgehoben
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-O: Drei gleichrangige Rahmen, ein Kranz über allen. Zeigt 'kein eindeutiger Erster' ohne ein einziges Wort.

**M45** · 3 Einstellungen
- Bild: Ein weites Sternfeld mit vielen hundert Punkten; nur etwa sechzig davon tragen einen kleinen Ring
- Licht: sichtbar: die Sterne
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M46** · 2 Einstellungen · getrennte Ebenen
- Bild: Ein Satellit mit aufgeklapptem Sonnensegel über der gekrümmten Erdkante, im Hintergrund Sterne
- Licht: Schatten: hart von rechts, scharfe Licht-Schatten-Kante am Rumpf und am Sonnensegel; die Sonne selbst bleibt außerhalb des Bildes
- Ort: Erdumlaufbahn, um 1990
- Framing: ohne

**M47** · 1 Einstellung · Schema
- Bild: Sechs gleiche Punkte in einer Reihe, einer davon von einem engen Ring umschlossen, die anderen fünf von weiten, unscharfen Ringen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-P: Enger Ring = sicher, weiter Ring = unsicher. Die Ringgröße als Fehlerbalken, ohne Achse und ohne Zahl.

**M48** · 1 Einstellung · getrennte Ebenen
- Bild: Ein kompakterer Satellit mit zylindrischem Sonnenschild vor dem schwarzen All, weit von der Erde entfernt
- Licht: Schatten: hart von links, scharfe Kante am Sonnenschild; die Sonne selbst bleibt außerhalb des Bildes
- Ort: Lagrangepunkt hinter der Erde, 2015
- Framing: ohne

**M49** · 3 Einstellungen · Schema
- Bild: Eine Münze im Vordergrund, dahinter der Mond, und weit dahinter noch einmal dieselbe Münze als kaum sichtbarer Punkt
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D3c: Die Münze zum dritten Mal, jetzt mit dem Mond als Zwischenmarke. Der Mond ist das einzige Maß, das jeder kennt.

**M50** · 3 Einstellungen · Schema
- Bild: Aufsicht auf eine Spiralgalaxie, die die ganze Bildbreite einnimmt; in einem äußeren Arm ein einzelner heller Punkt, um ihn herum eine schwach ausgeleuchtete Scheibe, die nur einen kleinen Teil der Galaxie bedeckt
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-Q: Eine kleine ausgeleuchtete Scheibe in einer großen Galaxie. Das Größenverhältnis ist die ganze Aussage und braucht keine Zahl.

**M51** · 2 Einstellungen · Schema
- Bild: Ein scharfer, klar begrenzter Punkt auf der einen Bildseite und ein verwaschener, ausgefranster Fleck auf der anderen; der Versatz zwischen zwei Lagen des Flecks verschwindet in seiner eigenen Unschärfe
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-R: Scharf gegen unscharf, und der Versatz kleiner als die Unschärfe. Der Kernsatz des Absatzes, rein bildlich.

**M52** · 1 Einstellung · Schema · **geschützter Moment**
- Bild: Eine Leiter, die schräg in einen Sternhimmel hinaufführt; die unterste Sprosse steht auf einem kleinen Dreieck, die Sprossen darüber werden nach oben hin länger
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D10 — die zweite Schlüsselgrafik. Ohne Beschriftung lesbar: eine Leiter steht auf dem Dreieck von M06. Die Rückbindung an das Grundbild ist die ganze Aussage.

**M53** · 2 Einstellungen
- Bild: Nahaufnahme zweier Hände über einer großen Glasplatte auf einem Leuchttisch; die eine Hand hält eine Lupe, die andere notiert mit einem Bleistift; kein Gesicht im Bild
- Licht: sichtbar: der Leuchttisch von unten
- Ort: Harvard College Observatory, Massachusetts, um 1910
- Framing: teil

**M54** · 3 Einstellungen · getrennte Ebenen
- Bild: Ein langer heller Arbeitsraum, an mehreren Tischen sitzen Frauen in hochgeschlossenen Blusen und langen Röcken über Glasplatten gebeugt; an der Tür ein Mann im Anzug, der einen Plattenkasten hereinreicht
- Licht: sichtbar: hohe Sprossenfenster auf der linken Seite
- Ort: Harvard College Observatory, Massachusetts, 1908 bis 1912
- Flora: Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation
- Framing: ganz

**M55** · 3 Einstellungen · Epochenfigur · getrennte Ebenen
- Bild: Eine Frau in dunkler Bluse sitzt allein am Leuchttisch, den Blick auf die Platte gesenkt, eine Lupe in der Hand; um sie herum Stapel weiterer Platten
- Licht: sichtbar: der Leuchttisch von unten
- Ort: Harvard College Observatory, Massachusetts, um 1910
- Flora: Innenraum, Holzvertäfelung und Sprossenfenster, keine Vegetation
- Framing: ganz

**M56** · 2 Einstellungen · getrennte Ebenen
- Bild: Eine unregelmäßige Sternwolke, deutlich abgesetzt vom umgebenden Himmel, mit einem dichten Kern und ausgefransten Rändern
- Licht: sichtbar: die Wolke selbst
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M57** · 2 Einstellungen · Zustandspaar mit M58
- Bild: Ein einzelner Stern in einem Sternfeld, groß und hell
- Licht: sichtbar: der Stern selbst
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M58** · 1 Einstellung · Zustandspaar mit M57
- Bild: Dasselbe Sternfeld, derselbe Ausschnitt — der eine Stern ist auf einen kleinen matten Punkt zusammengefallen
- Licht: sichtbar: der Stern selbst
- Ort: zeitlos, Blick ins All
- Framing: ohne

**M59** · 2 Einstellungen · Schema · Zustandspaar mit M62
- Bild: Ein Feld aus Punkten, die sich sichtbar entlang zweier paralleler gerader Linien anordnen; die Linien steigen beide von links unten nach rechts oben
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D8 — Leavitts eigene Abbildung. Ohne Achsenbeschriftung verständlich, weil die Botschaft die AUSRICHTUNG ist: Punkte fallen auf Geraden, also gibt es eine Regel. Was auf den Achsen steht, sagt die Stimme.

**M60** · 2 Einstellungen · Schema
- Bild: Zwei gleiche Lampen, die linke nah und grell, die rechte weit weg und schwach; von beiden geht dieselbe Anzahl Strahlen aus
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-S: Gleiche Lampe, unterschiedlich hell, weil unterschiedlich weit. Die Strahlenzahl macht die Gleichheit sichtbar — ohne Text.

**M61** · 2 Einstellungen · Schema
- Bild: Eine Reihe derselben Lampe, von links nach rechts immer kleiner und matter, darunter eine Maßleiste, deren Abstände nach rechts zunehmen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-T: Abnehmende Helligkeit gegen zunehmende Strecke. Die Übersetzung Helligkeit → Entfernung, rein grafisch.

**M62** · 3 Einstellungen · Schema · Zustandspaar mit M59 · **geschützter Moment**
- Bild: Dasselbe Punktfeld mit denselben zwei Geraden wie zuvor — aber die senkrechte Achse ist ein blanker Strich ohne einen einzigen Teilstrich
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D9 — der fehlende Nullpunkt. **Genau hier ist die Textlosigkeit ein Vorteil**: eine Achse ohne Teilung ist ohne Beschriftung verständlicher als mit. Zustand B zu M59, identischer Ausschnitt.

**M63** · 2 Einstellungen · Schema
- Bild: Dreizehn Sterne über eine Fläche verstreut, von jedem geht ein kurzer Pfeil aus; die Pfeile zeigen in verschiedene Richtungen, aber ein dicker Sammelpfeil in der Mitte fasst sie zu einer gemeinsamen Richtung zusammen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-U: Dreizehn Einzelpfeile, ein Mittelwertpfeil. Zeigt das Poolen ohne ein einziges Wort — und dass es ein Mittel ist, keine Einzelmessung.

**M64** · 1 Einstellung
- Bild: Nahaufnahme eines Schriftstücks, auf dem unten rechts eine große geschwungene Unterschrift steht und oben links eine viel kleinere; die Schrift ist als reines Liniengekritzel angedeutet, keine lesbaren Buchstaben
- Licht: Schatten: hart von links oben
- Ort: Harvard College Observatory, 1912
- Framing: teil

**M65** · 2 Einstellungen · getrennte Ebenen
- Bild: Ein leerer Schreibtisch am Fenster, darauf ein ungeöffneter Briefumschlag; der Stuhl davor ist leer und leicht zurückgeschoben
- Licht: sichtbar: das Fenster mit fahlem Tageslicht
- Ort: Harvard, Massachusetts, 1925
- Flora: Innenraum; was durch das Fenster zu sehen ist, sind kahle Laubbäume Neuenglands — keine Palmen, keine immergrünen Hecken
- Framing: ohne

**M66** · 3 Einstellungen · Schema
- Bild: Dieselbe Leiter wie zuvor, jetzt von der Seite: jede Sprosse ruht sichtbar auf zwei Streben, die von der Sprosse darunter aufsteigen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D10b: Die Leiter im Konstruktionsschnitt. Dass jede Sprosse auf der vorigen ruht, ist rein baulich sichtbar.

**M67** · 1 Einstellung · Schema
- Bild: Dieselbe Leiter, an der untersten Sprosse ein kleiner Riss; derselbe Riss wiederholt sich an jeder Sprosse darüber, nach oben hin immer breiter
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D11: Ein Riss, der sich nach oben verbreitert. Fehlerfortpflanzung ohne Formel und ohne Text.

**M68** · 1 Einstellung · Schema · **geschützter Moment**
- Bild: Dieselbe Leiter, zwei Sprossen sind durchgebrochen und hängen schief herab
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-V: Gebrochene Sprossen. Die Wiedererkennung derselben Leiter trägt den Beat; ohne Text eindeutig.

**M69** · 1 Einstellung · Epochenfigur · getrennte Ebenen
- Bild: Ein Mann in Tweedjacke sitzt am Okular eines sehr großen Spiegelteleskops in einer Kuppel
- Licht: sichtbar: der Nachthimmel durch den offenen Kuppelspalt
- Ort: Mount-Wilson-Observatorium, Kalifornien, 1929
- Flora: Innenraum einer Kuppel, Stahlfachwerk, keine Vegetation
- Framing: ganz

**M70** · 1 Einstellung · Schema
- Bild: Ein Feld kleiner Spiralgalaxien, von einem gemeinsamen Mittelpunkt nach außen strebend; die äußeren tragen längere Bewegungsspuren als die inneren
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-W: Längere Spur = schneller. Die Zunahme nach außen ist ohne Beschriftung ablesbar.

**M71** · 1 Einstellung · Schema
- Bild: Dasselbe Galaxienfeld, aber alle Bewegungsspuren zeigen nach innen, und die Galaxien sind auf einen dichten Punkt zusammengelaufen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-X: Der Film rückwärts. Zusammenlaufen statt auseinander — ohne Text als Umkehrung lesbar.

**M72** · 2 Einstellungen · Schema · Zustandspaar mit M73
- Bild: Zwei senkrechte Balken nebeneinander, fast exakt gleich hoch; der linke trägt oben ein kleines Sternsymbol, der rechte eine kleine Erdkugel
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D13 KORRIGIERT: 1929 waren beide Balken fast gleich hoch — das ist der historisch richtige Stand, nicht der oft gezeigte Faktor-2-Widerspruch. Die Symbole ersetzen die Beschriftung.

**M73** · 3 Einstellungen · Schema · Zustandspaar mit M72
- Bild: Dieselben zwei Balken, dieselbe Anordnung — der rechte mit der Erdkugel ist jetzt deutlich höher als der linke mit dem Stern
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D13b: Zustand B. Die Erde überragt das Universum — der Widerspruch wird rein durch Balkenhöhe erzählt.

**M74** · 2 Einstellungen · Schema
- Bild: Ein Punktfeld, durch das zunächst eine einzige Gerade läuft; im selben Bild spaltet sie sich nach rechts in zwei getrennte Geraden auf, jede mit ihrer eigenen Punktgruppe
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D12: Aus einer Geraden werden zwei. Direkter Rückgriff auf M59 — dieselbe Bildsprache, jetzt verdoppelt.

**M75** · 1 Einstellung · Epochenfigur · getrennte Ebenen
- Bild: Ein Saal mit Reihenbestuhlung, vorn ein Mann am Rednerpult vor einer hellen Projektionsfläche, die Zuhörer beugen sich vor
- Licht: sichtbar: der Projektionsstrahl von hinten
- Ort: Rom, Tagung der Internationalen Astronomischen Union, 1952
- Flora: Innenraum, Marmorpilaster und hohe Fenster, keine Vegetation
- Framing: ganz

**M76** · 1 Einstellung · Schema
- Bild: Eine Kugel mit Sternen darin, daneben dieselbe Kugel im doppelten Durchmesser
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-Y: Zwei Kugeln, klares Größenverhältnis. Verdopplung ohne Text.

**M77** · 1 Einstellung
- Bild: Nahaufnahme einer Fotoplatte: an einer Stelle ein einzelner scharfer Punkt, direkt daneben ein Fleck, der bei näherem Hinsehen aus vielen dicht gedrängten Punkten und diffusem Leuchten besteht
- Licht: Durchlicht: die Platte wird von hinten durchleuchtet, die Quelle liegt hinter ihr und ist nicht im Bild
- Ort: Kalifornien, 1958
- Framing: teil

**M78** · 1 Einstellung · Schema
- Bild: Links eine kleine Kugel, rechts dieselbe Kugel weit größer; quer über den Durchmesser der großen liegen sieben Abdrücke der kleinen in einer Reihe, die ihn genau ausfüllen
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-Z: Der Faktor sieben als abzählbare Kette quer durch die große Kugel. Eine Reihe von sieben WACHSENDEN Kugeln wäre die naheliegende Lösung und wäre falsch gelesen worden — sie zeigt sieben Schritte, nicht das Verhältnis sieben zu eins. Hier ist abzählbar, was die Stimme sagt.

**M79** · 1 Einstellung · getrennte Ebenen
- Bild: Ein kleiner dichter Sternhaufen aus wenigen hellen Sternen, von zartem Nebel umgeben, am Nachthimmel über einer Baumsilhouette
- Licht: sichtbar: die Sterne des Haufens
- Ort: Gegenwart, Blick vom Boden
- Flora: mitteleuropäische Laubbäume als Silhouette
- Framing: ohne

**M80** · 3 Einstellungen · Schema · Zustandspaar mit M81
- Bild: Ein Maßstab, an dem zwei Zeiger sitzen: der linke deutlich weiter unten als der rechte; zwischen beiden eine auffällige Lücke
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AA: Zwei Zeiger, eine Lücke. Der Abstand ist die Aussage.

**M81** · 1 Einstellung · Schema · Zustandspaar mit M80
- Bild: Derselbe Maßstab, dieselben zwei Zeiger — der linke ist jetzt zum rechten hinaufgewandert, beide stehen dicht beieinander
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AB: Zustand B. Die Lücke ist geschlossen, der Satellit hat nachgegeben.

**M82** · 1 Einstellung · getrennte Ebenen
- Bild: Mehrere große Parabolantennen auf freiem Feld, alle in dieselbe Richtung geneigt
- Licht: Schatten: hart von rechts, lange Schatten über den Boden
- Ort: Gegenwart, ein Antennenfeld im Hochland des amerikanischen Südwestens
- Flora: trockenes Steppengras, niedrige Beifußbüsche, ferne kahle Bergrücken; keine Bäume, keine Kakteen
- Framing: ohne

**M83** · 2 Einstellungen · getrennte Ebenen
- Bild: Ein feinkörniges Fleckenmuster über die ganze Bildfläche, dahinter ein kleiner Satellit im Profil
- Licht: sichtbar: das Muster leuchtet selbst
- Ort: Lagrangepunkt, 2013
- Framing: ohne

**M84** · 2 Einstellungen · Schema
- Bild: Dieselbe Leiter wie zuvor, jetzt mit drei deutlich abgesetzten Sprossen: unten ein Dreieck, in der Mitte eine pulsende Lampe, oben ein aufplatzender Stern
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D10c: Die Leiter mit ihren drei Stufen als Symbolen. Jedes Symbol wurde vorher eingeführt — deshalb ohne Text lesbar.

**M85** · 3 Einstellungen · Schema
- Bild: Zwei waagerechte Fehlerbalken übereinander auf gemeinsamer Achse, deren Enden sich nicht berühren; zwischen ihnen eine klare Lücke. Am linken Ende des oberen sitzt eine feinfleckige Scheibe, am linken Ende des unteren eine kleine Leiter
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AC: Zwei Balken, die sich nicht überlappen. Die Lücke IST die Signifikanz — ohne Sigma-Zeichen und ohne Zahl. Die beiden Symbole sagen ohne ein Wort, wessen Balken welcher ist, und bereiten die Symbolschrift von M87 vor.

**M86** · 3 Einstellungen · Schema
- Bild: Dieselbe Leiter, aber die mittlere Sprosse ist gegen eine andere ausgetauscht: statt der pulsenden Lampe sitzt dort ein großer roter Stern
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AD: Dieselbe Leiter, eine andere Sprosse. Der Austausch ist der Kern des Streits und rein bildlich zu zeigen.

**M87** · 3 Einstellungen · Schema · **geschützter Moment**
- Bild: Sieben waagerechte Fehlerbalken untereinander auf einer gemeinsamen senkrechten Achse. Am linken Ende jedes Balkens sitzt ein kleines Symbol: beim obersten eine feinfleckige Scheibe, bei drei weiteren ein großer roter Stern, bei den unteren drei eine pulsende Lampe. Die Balken mit Scheibe und rotem Stern überlappen sich; die drei mit der Lampe liegen weiter rechts und berühren die obere Gruppe nicht
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D14 — der wichtigste Befund des Videos als Bild, und der schwierigste Fall der ganzen Liste. Sieben unbeschriftete Balken allein zeigen ZWEI HAUFEN — und damit genau das Früh-gegen-Spät-Bild, das das Skript ausdrücklich verwirft. Ohne Beschriftung richtig lesbar wird es erst durch die Symbole am Balkenende: die Fleckenscheibe (aus M83), der rote Riesenstern (aus M86) und die pulsende Lampe (aus M84) sind alle vorher eingeführt. Dann liest das Auge, was die Aussage ist: die Trennlinie läuft NICHT zwischen Scheibe und Leiter, sondern zwischen den beiden Leitersprossen — der rote Stern steht bei der Scheibe, nicht bei der Lampe. Ohne diese Symbole ist das Diagramm nicht bloß unverständlich, sondern irreführend.

**M88** · 2 Einstellungen · Schema
- Bild: Zwei Galaxien nebeneinander, von beiden geht je eine Messlinie zu einem gemeinsamen Nullpunkt; die beiden Linien sind praktisch gleich lang
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AE: Zwei gleich lange Messlinien. Zeigt die Übereinstimmung, die dem Streit widerspricht.

**M89** · 2 Einstellungen
- Bild: Eine solide Leiter, die fest steht — und an ihrem Fuß zwei Hände, die um einen einzelnen Nagel ringen; keine Gesichter im Bild
- Licht: Schatten: hart von links
- Ort: zeitlos, sinnbildlich
- Framing: teil
- Ohne Beschriftung: Kein Schema: Raumbild mit Körperteil-Framing. Die Leiter aus den Schemata taucht hier als Gegenstand auf — bewusster Bruch, damit der Schlusspunkt des Absatzes greifbar wird.

**M90** · 3 Einstellungen · Schema
- Bild: Das Parallaxendreieck aus dem Anfang, unverändert: Erdbahn, zwei Standpunkte, zwei Sichtlinien, ein Keil
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D1-Reprise. Identisch zu M06 — die Wiedererkennung ist der Zweck.

**M91** · 2 Einstellungen · Schema
- Bild: Die Leiter und das Dreieck zusammen in einem Bild: das Dreieck unten, die Leiter darauf, oben verliert sie sich in einem Sternfeld
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D10d: Beide Schlüsselgrafiken vereint. Nur verständlich, WEIL beide vorher einzeln eingeführt wurden.

**M92** · 1 Einstellung
- Bild: Nahaufnahme: dieselben zwei Hände wie am Leuchttisch, die eine notiert mit dem Bleistift eine kurze Linie, direkt daneben eine zweite, kürzere Linie
- Licht: sichtbar: der Leuchttisch von unten
- Ort: Harvard College Observatory, um 1910
- Framing: teil

**M93** · 1 Einstellung · Schema
- Bild: Ein einzelner Punkt mit einem waagerechten Fehlerbalken darunter, sonst nichts im Bild
- Licht: Schema
- Ort: zeitlos, reine Zeichnung
- Framing: ohne
- Ohne Beschriftung: D-AF: Ein Wert, ein Fehlerbalken. Das Schlussbild des Gedankens — die zweite Zahl neben der ersten, ohne ein Wort.

## Die Diagramme ohne Beschriftung

Alle 52 Schemata sind einzeln daraufhin geprüft worden, ob
sie ohne ein einziges Zeichen lesbar sind; das Urteil steht bei jedem
im Motivkatalog. Sieben haben die Prüfung **nicht** bestanden und sind
geändert worden, bevor dieser Plan stand:

| Motiv | Was nicht funktionierte | Was jetzt dasteht |
|---|---|---|
| **M87** | Sieben unbeschriftete Fehlerbalken zeigen zwei Haufen — also genau das Früh-gegen-Spät-Bild, das das Skript widerlegt. Das Diagramm war nicht bloß unverständlich, es hätte das Gegenteil behauptet. | Jeder Balken trägt am Ende ein Symbol, das vorher eingeführt wurde: Fleckenscheibe, roter Riesenstern, pulsende Lampe. Damit liest das Auge die Trennlinie dort, wo sie verläuft — zwischen den beiden Leitersprossen. |
| **M85** | Zwei Balken ohne Kennung; welcher wessen ist, hing allein am Schnitt. | Dieselben zwei Symbole, Scheibe und Leiter. |
| **M78** | Sieben wachsende Kugeln zeigen sieben **Schritte**, nicht den **Faktor** sieben. | Eine kleine und eine große Kugel; über den Durchmesser der großen liegen sieben Abdrücke der kleinen. |
| **M15** | Die Hyperbel *d = 1/p* ist ohne Achsenbeschriftung bedeutungslos. | Zwei Sterne nebeneinander, einer mit weitem, einer mit winzigem Versatz. |
| **M03** | Drei Figuren hatten nur eine Sonne, die vierte nur einen Stern — es gab nichts zu vergleichen. | Über **jeder** Figur stehen beide; bei dreien hängt die Sonne tiefer, bei der vierten der Stern. |
| **M04** | Der eine, der geraten hat, trug einen *fragenden* Kopf — das ist keine Antwort. | Sechs Gedankenblasen, fünf leer, in der sechsten ein Stern mit einer Maßlinie. |
| **M18** | Auf dem Bild der erwarteten Schwankung stehen zu bleiben, während die Stimme sagt, dass niemand eine sah, behauptet das Gegenteil. | Zustandspaar M18/M18b: erst der Versatz, dann seine Abwesenheit. |

**Der schwierigste Fall ist nicht das Parallaxendiagramm.** M06 trägt
sich ohne Beschriftung, weil zwei Standpunkte, zwei Sichtlinien und
ein Keil die ganze Aussage sind — es braucht keine Winkelmaße. Die
eine Bedingung: der nahe Stern muss sichtbar größer und heller sein
als das Feld dahinter, sonst sitzt der Keil scheinbar am falschen
Punkt. Schwierig sind die **Fehlerbalken**, weil dort erstmals nicht
eine Form, sondern eine Zuordnung getragen werden muss.

**Einmal ist die Textlosigkeit ein Vorteil:** M62, der fehlende
Nullpunkt. Eine Achse ohne einen einzigen Teilstrich sagt genau das,
was Leavitts Gesetz fehlte — mit Beschriftung wäre es schwerer zu
sehen, nicht leichter.

## Zustandspaare

| Paar | Zustand A | Zustand B |
|---|---|---|
| M09 / M10 | Derselbe Daumen vor derselben Wand, der Daumen sitzt links von einem Bildhaken an … | Exakt dieselbe Aufnahme, aber der Daumen sitzt jetzt rechts vom Bildhaken — … |
| M13 / M14 | Ein rechteckiger Bildausschnitt des Sternhimmels, ein Stern darin links von zwei … | Derselbe Ausschnitt, derselbe Himmel — nur der eine Stern sitzt jetzt rechts von … |
| M18 / M18b | Derselbe Sternhimmel zweimal übereinander im selben Bild, die obere Hälfte gegen … | Exakt dasselbe Bild, derselbe Ausschnitt, dieselben zwei Himmel — nur liegt jeder … |
| M22 / M25 | Extreme Nahaufnahme eines einzelnen Sterns, wie ihn ein bloßes Auge sieht: eine … | Dieselbe Nahaufnahme desselben Sterns, aber die Scheibe ist verschwunden: ein … |
| M31 / M32 | Blick durch ein Okular: zwei getrennte Sternabbilder nebeneinander im runden … | Dasselbe runde Gesichtsfeld, dieselbe Lage — die beiden Sternabbilder liegen jetzt … |
| M42 / M43 | Zwei sehr kurze waagerechte Striche übereinander, fast gleich lang, der Unterschied … | Dasselbe Bild, dieselbe Anordnung — nur der obere Strich ist jetzt auf die doppelte … |
| M57 / M58 | Ein einzelner Stern in einem Sternfeld, groß und hell | Dasselbe Sternfeld, derselbe Ausschnitt — der eine Stern ist auf einen kleinen … |
| M59 / M62 | Ein Feld aus Punkten, die sich sichtbar entlang zweier paralleler gerader Linien … | Dasselbe Punktfeld mit denselben zwei Geraden wie zuvor — aber die senkrechte Achse … |
| M72 / M73 | Zwei senkrechte Balken nebeneinander, fast exakt gleich hoch; der linke trägt oben … | Dieselben zwei Balken, dieselbe Anordnung — der rechte mit der Erdkugel ist jetzt … |
| M80 / M81 | Ein Maßstab, an dem zwei Zeiger sitzen: der linke deutlich weiter unten als der … | Derselbe Maßstab, dieselben zwei Zeiger — der linke ist jetzt zum rechten … |

## Getrennte Ebenen

**19 von 93 Motiven**: M01, M02, M17, M19, M29, M34, M39, M41, M46, M48, M54, M55, M56, M65, M69, M75, M79, M82, M83.

## Die geschützten Momente

| Moment | Einstellungen | Motiv | Dauer |
|---|---|---|---:|
| Die Klammer — erstes und letztes Bild | 3, 163, 164 | M02 | 8,5 s |
| Die Antwort: das Dreieck | 9, 11, 21 | M06 | 10,7 s |
| Die Leiter, zum ersten Mal | 83 | M52 | 4,4 s |
| Der fehlende Nullpunkt | 101, 102, 103 | M62 | 8,8 s |
| Die gebrochenen Sprossen | 114 | M68 | 3,0 s |
| Die sieben Fehlerbalken | 145, 146, 147 | M87 | 7,7 s |

## Zahlen

| Größe | Wert |
|---|---|
| Einstellungen | **164** |
| Gesamtlaufzeit | 9:21,6 |
| Mittlere Dauer | **3,42 s** (Ziel 3–5 s) |
| Spanne | 0,8 – 5,8 s |
| unter 3 s | 54 — jede davon auf demselben Motiv wie die Einstellung davor oder auf dessen Paarpartner |
| über 5 s | 11, davon über 6 s: 0 |
| **Motive (zu generierende Bilder)** | **93** |
| Einstellungen je Motiv | 1,76 im Mittel |
| Mehrfach genutzte Motive | 50 → **71 Bilder gespart** |
| Schemata | 52 Motive (56 %) · 97 Einstellungen (59 %) · **58 % der Laufzeit** |
| Weltbilder | 41 — Framing ganz 10 · ohne 21 · teil 10 |
| Zustandspaare | 10 |
| Motive mit getrennten Ebenen | 19 |
| Epochenfiguren | 7 |
| Einstellungen mit Figur oder Körperteil | 34 (21 %) |

## Kosten

Preise per `get_cost` gemessen am 2026-08-16, unverändert gegenüber Video 1:

| Posten | Credits |
|---|---:|
| Standbild `nano_banana_2`, 16:9, **2k** | **2,0** |
| Standbild 1k | 1,5 |
| Clip Seedance 1.5 Pro, 1080p, 4 s | 12 |

| Variante | Credits | € Ultra | € Nachkauf |
|---|---:|---:|---:|
| **A — alle Motive als Standbild, ffmpeg bewegt** | **186** | 6,14 | 9,11 |
| **B — A plus getrennte Ebenen** | **224** | 7,39 | 10,98 |
| **C — B plus 6 echte Clips für die geschützten Momente** | **296** | 9,77 | 14,50 |
| zum Vergleich: alle 164 Einstellungen als Clip | 1968 | 64,94 | 96,43 |

**Euro-Grundlage.** Das Konto läuft auf **Ultra**: 3.000 Credits im
Monat, 99 € im Monat bei Jahreszahlung — also **0,033 € je Credit**.
Ein Nachkauf kostet 0,049 € je Credit (1.000 Credits für 49 €).

> **Achtung, Abweichung zu Video 1.** `produktion/video-01/szenen.md`
> rechnet mit 0,00275 € je Credit und liest die 99 € als Jahrespreis.
> Das ist um den Faktor zwölf zu niedrig. Video 1 bleibt auf Wunsch
> unverändert; die Zahl hier ist die richtige.

**Variante C liegt bei 296 Credits** — unter der vereinbarten
Abbruchschwelle von 500 und bei 10 % des Monatskontingents.

## Was diese Fassung nicht leistet

- **Der Schema-Anteil ist hoch und bleibt es.** 58 % der Laufzeit
  sind Zeichnung, gegenüber 26 % bei Video 1. Das folgt aus dem Thema —
  ein Winkel, eine Leiter und ein Fehlerbalken lassen sich nicht
  fotografieren. Abgefedert ist es nur über den Wechsel: 52 Übergänge
  zwischen Zeichnung und Welt, längste reine Schema-Strecke 28,5 s.
  Ob das reicht, ist eine Frage an das fertige Video, nicht an den Plan.
- **Die Figurenquote ist niedrig.** 21 % der Einstellungen zeigen eine
  Figur oder ein Körperteil, gegen 32 % bei Video 1. Derselbe Grund.
- **Die Diagramm-Prüfung ist ein Urteil, keine Messung.** Ob ein Bild
  ohne Beschriftung verständlich ist, lässt sich vor der Generierung
  nicht messen; die Notizen im Motivkatalog sind begründete
  Einschätzungen. Bei Video 1 waren es die Bilder, die dem Auge
  durchgingen und erst der Messung auffielen — hier ist es umgekehrt,
  und es bleibt offen.
- **Kein Bildtext heißt auch: keine Achsen.** Bei M59, M62 und M87
  hängt das Verständnis daran, dass die Stimme im selben Moment sagt,
  was auf den Achsen stünde. Verschiebt sich der Schnitt gegen den
  Ton, bricht genau das.

## Anschluss

1. Stichprobenlauf über 8–10 Motive, darunter **M06, M15, M87** — die
   drei, an denen die Textlosigkeit am ehesten scheitert.
2. Bei Freigabe: die restlichen Motive in Stapeln, danach die
   19 zweiten Ebenen, zuletzt die 6 Clips.
3. `szenenplan.json` liefert `montage.py` Wortlaut, Motiv und Fahrt je
   Einstellung; die Dauern hier sind aus 219 WPM gerechnet und werden
   beim Schnitt durch die echten ElevenLabs-Zeichenzeiten ersetzt.

