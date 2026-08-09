# Serien-Motivvarianten — Handytest

> **Stand 2026-08-04, zweiter Lauf.** Serienmotiv nach `formel/thumbnail-motive.md`,
> Richtung 2:
> **sitzende Jesus-Figur, allein in dunkler Nachtlandschaft, kein Blickkontakt.**
> Erzeugt mit Higgsfield (nano-banana), 1376×768 → auf 1920×1080 gebracht
> (Höhe skaliert, Breite mittig auf 16:9 beschnitten, Verlust ~0,8 %).

## Dateien

| Datei | Inhalt |
|---|---|
| `motiv-V1.png` | Felsen über weitem Tal, **großer Mond tief am Horizont** als Lichtquelle (Formel §5 zählt den Mond zu den zulässigen warmen Lichtquellen) |
| `motiv-V2.png` | Seeufer, **große Öllampe**, Nebel über dem Wasser |
| `motiv-V3.png` | Alter Baum auf Anhöhe, **großes Lagerfeuer mit sichtbarer Glut**, ferne Hügel |
| `motiv-V4.png` | Wegrand, **große Laterne**, weite Ebene |
| `loops/loop-V?.mp4` | nahtloser 60-s-Animations-Loop je Variante |
| `loops/qa-V?.json` | Naht- und Bitratenmessung je Loop |
| `motiv-V?_160x90.png` | Feed-Größe für die Handy-Entscheidung |
| `motiv-V3_text.png` (+160×90) | Textvariante mit der Zeile von Video 01 |
| `text_messung.json` | Messwerte der Textvariante |
| `kanal-avatar.png` (+`_kreistest.png`) | Kanal-Profilbild, 1024×1024: vereinfachte Silhouette der Serienfigur an verglimmender Glut — quadratisch, Figur mittig mit Randreserve für den Kreisbeschnitt; Kreistest in 800/176/88/48 px |
| `kanal-avatar-b.png` (+`_kreistest.png`) | Profilbild-Variante B: enger Kopf-Schulter-Anschnitt der Serienfigur, dunkelrote Kapuze, Feuerlicht von rechts unten — bei 88/48 px deutlich besser lesbar als Variante A; helle Masse ragt zu 20 % über den Kreis (nur Kapuze/Schulter, Gesicht bleibt zentral) |
| `kanal-avatar-b2.png` (+`_kreistest.png`) | Zweiter Wurf desselben Prompts: näherer Anschnitt, Dreiviertelprofil (Augen zu, kein Blickkontakt), wärmer. Bei 88/48 px die lesbarste der drei Fassungen; 23,5 % der hellen Masse außerhalb des Kreises (Kapuze/Schulter, Gesicht zentral). Dreiervergleich: `kanal-avatar_vergleich_klein.png` |
| `kanal-banner.png` (+`_zonen.png`, `_mobilansicht.png`, `-quelle.png`) | **Finales Kanalbanner, 2560×1440, 3,1 MB** (Limit 6 MB). Neufassung mit zentrierter Figur auf dem Horizont, symmetrische Hügel; vertikal umkomponiert (Versatz −222 px, Bodenfüllung unten), damit Figur+Feuer im Beschnitt liegen: 82 % der warmen Masse im Desktop-Streifen UND im Mobil-Safe (Figur war mit 34 % Bildhöhe größer als bestellt — der Block ist 70 px höher als der 423-px-Streifen, Haarspitze/Feuerbasis ragen minimal hinaus). Mobilansicht als eigene Vorschau |
| `motiv-video-02.png` (+`_160x90.png`, `_messung.json`) | **Standbild Video 02**, 1920×1080: Grundmotiv mit aufgeschlagenem Buch neben der Figur, größeres Feuer, dichteres Sternenfeld (Vorgabe aus `videos-01-08.md`, Thumbnail-Block Video 02). Aus einem 2k-Wurf mit eingebrannten Balken beschnitten — siehe „Standbild Video 02" |
| `kanal-banner-entwurf.png` (+`_zonen.png`) | Banner-Panorama, **als Banner so nicht verwendbar**: Figur+Feuer liegen zu 99 % unter dem Desktop-Streifen und zu 100 % außerhalb des Mobil-Safe-Bereichs (nur leerer Himmel sichtbar); Zonen-Overlay zeigt die Beschnitte. Neufassung braucht Figur+Feuer im Mittelband |

Alle vier erfüllen die nicht verhandelbaren Vorgaben: gemalter Stil, Nacht,
dunkles Blau dominant, genau **eine** warme Lichtquelle, Figur sitzend im
Profil/halb abgewandt, kein Blickkontakt, kein Innenraum, kein Text (außer der
ausgewiesenen Textvariante).

## Textvariante — gemessene Werte

Auf **V3** gelegt, nicht auf V1: Bei V1 steht der Mond in der Textzone, und die
Checkliste verbietet weißen Text über dem Mond. V3 hat das dunkelste
durchgehende Himmelsband (p95-Luminanz 0,030) und ist zugleich die
Serien-Kernvariante (Feuer als Lichtquelle wie in 8/10 Treffern).

| Größe | gemessen | Vorgabe |
|---|---|---|
| Versalhöhe | **125 px = 11,57 %** der Bildhöhe | ≥ 125 px / ≥ 11,5 % |
| Kontrast zum direkten Hintergrund (Mittel) | **17,4 : 1** | ≥ 10 : 1 |
| Kontrast (p95, ungünstige Pixel) | **15,5 : 1** | ≥ 10 : 1 |
| Wörter | 3 (`SO TIRED TONIGHT`) | ≤ 4 |
| Schrift | FreeSerif Bold, weiß, Versalien, oberes Drittel, zentriert | B-Serie 13/13 |

Gegen den **Rohhintergrund** (vor dem weichen dunklen Schein hinter der
Schrift): Mittel 15,8:1, p95 13,7:1 — 90 einzelne Sternpixel unter den Glyphen
würden nackt durchfallen; der Schein im fertigen Bild löst das (ungünstigster
Pixel dort 2,0:1 → nur noch abgedunkelte Sterne unter deckend weißer Schrift).

## Textbreiten aller acht Zeilen — erledigt (Stand 2026-08-07)

Bei 1920 px Bildbreite und 40 px Rand je Seite stehen **1840 px** zur
Verfügung. Die Versalhöhe von 125 px ist nicht verhandelbar (Checkliste,
≥ 11,5 % der Bildhöhe), und die Checkliste schreibt bei Überlänge
ausdrücklich vor: **Wörter kürzen, nicht die Schrift verkleinern.** Alle Werte
in FreeSerif Bold @ 184 px, der schmalsten der drei installierten Serifen.

| | Zeile | Zeichen | Breite | Rand je Seite | |
|---|---|---|---|---|---|
| V01 | `SO TIRED TONIGHT` | 16 | 1787 px | 66 px | knapp |
| V02 | `QUIET YOUR MIND` | 15 | 1726 px | 97 px | |
| V03 | `GOSPEL OF JOHN` | 14 | 1609 px | 155 px | |
| V04 | `THINK NO MORE` | 13 | 1548 px | 186 px | gekürzt |
| V05 | `YOU'RE TIRED` | 12 | 1328 px | 296 px | |
| V06 | `ISAIAH TONIGHT` | 14 | 1565 px | 177 px | |
| V07 | `NO MORE STRESS` | 14 | 1624 px | 148 px | gekürzt |
| V08 | `IN THE BEGINNING` | 16 | 1750 px | 85 px | knapp |

**Alle acht liegen unter 1840 px — kein weiterer Textfall ist offen.**

Quellen: V01–V04 aus den Messdateien der gebauten Thumbnails
(`produktion/video-0?/thumbnail*_messung.json`), nicht neu gemessen.
V05–V08 mit der Methode aus `thumbnail.py` gerechnet (gleiche Fontkette,
gleiche 125 px Versalhöhe) — bisher ohne Bild, weil diese Videos erst nach
Gate 2 starten.

Zwei Zeilen mussten weichen, beide dokumentiert in `videos-01-08.md`:
`NO MORE THINKING` (1896 px, 56 px zu breit) → `THINK NO MORE`, und
`REST WITHOUT STRESS` (2163 px, 323 px zu breit) → `NO MORE STRESS`.

Die praktische Faustregel bleibt: **13–14 Zeichen sitzen bequem**, 16 gehen
nur mit schmalen Glyphen. `SO TIRED TONIGHT` und `NO MORE THINKING` haben
beide 16 Zeichen und unterscheiden sich um 109 px — `M`, `N`, `K` und `W`
sind breit, `S`, `T`, `I` schmal. Zeichen zählen reicht also nicht, es muss
gemessen werden. Zum Vergleich: dieselbe V01-Zeile bräuchte in DejaVu Serif
Bold 1967 px und passte dort nicht.

> Die frühere Warnung an dieser Stelle („fünf der acht Zeilen liegen über der
> bequemen Breite, vor dem Rendern entscheiden") ist mit den beiden Kürzungen
> aufgelöst und wurde durch die Tabelle oben ersetzt.

## Wie es weitergeht

Die Entscheidung fällt am Handy auf den 160×90-Versionen. Danach wird die
gewählte Variante das **Serienbild**: gleiche Figur, gleiche Palette, je Video
nur die dokumentierte Detailvariation (`produktion/videos-01-08.md`,
Thumbnail-Blöcke). Generierungs-Prompts für Nachschübe stehen in
`formel/thumbnail-motive.md` §5.

## Standbild Video 02 (2026-08-06)

Serienmotiv mit der Detailvariation aus `videos-01-08.md`: **aufgeschlagenes
Buch** neben der Figur (belegt in A's 245K), größeres Feuer, dichteres
Sternenfeld. Figur unverändert — Serienkonsistenz nach Formel §3.

**Befund: nano-banana brennt Letterbox-Balken ins Bild.** Alle vier erzeugten
Kandidaten hatten schwarze Balken oben *und* unten — gemalte Kinobalken im
Bild, nicht am Bildrand. Der ausdrückliche Prompt-Zusatz „no letterbox, no
black cinematic bars, sky continues to the very top edge" im zweiten Lauf hat
daran **nichts** geändert. Für Nachschübe einplanen: nach der Generierung
immer `motiv_zuschnitt.py` laufen lassen und das Ergebnis auf Restbalken
prüfen. Angefordert war `nano_banana_2`, ausgeführt und abgerechnet hat die
Plattform beide Male `nano_banana_flash`.

Gewählt wurde Kandidat D (2752×1536, 2k). Zuschnitt mit
`produktion/pipeline/motiv_zuschnitt.py`, **0 Credits**:

| Schritt | Wert |
|---|---|
| Balken oben / unten | 184 px (12,0 %) / 182 px (11,8 %) |
| Nutzband nach Balkenschnitt | 2752×1170 = 2,352 : 1 |
| Breitenschnitt mittig auf 16:9 | 2752 → 2080 px, je Seite 336 px = **12,2 %** |
| Skalierung auf 1920×1080 | Faktor **0,923** — Verkleinerung, keine Hochrechnung |
| Restbalken am Ergebnis | 0 px oben, 0 px unten |

Zonenwerte im Vergleich zum Video-01-Motiv (`motiv-V3.png`):

| | V3 (Video 01) | Video 02 |
|---|---|---|
| oberes Sechstel p95 (Textzone) | 50,3 | **23,7** |
| oberes Drittel, Anteil heller Pixel | 3,44 % | **1,32 %** |
| Gesamtmittel (dunkles Bild, Formel §5) | 48,2 | **30,2** |
| unteres Achtel p95, Mitte (Untertitel) | 104,1 | 110,9 |
| unteres Achtel p95, rechtes Drittel | 104,9 | **213,2** |

Die Textzone ist deutlich dunkler als bei Video 01 — das Thumbnail gewinnt
dadurch Kontrast. Heller ist nur das **rechte** untere Drittel: das Feuer
reicht nach dem Balkenschnitt bis an die Unterkante. In der mittigen
Untertitelzone (110,9 gegenüber 104,1) ist der Unterschied belanglos, im
Mittel ist das neue Motiv dort sogar dunkler (46,5 gegenüber 54,3).

**Bekannte Schwäche, bewusst angenommen:** Die Hand auf dem Knie ist weich
gemalt und geht in die Gewandfalte über. Bei Feed-Größe 160×90 nicht sichtbar
— dieselbe Abwägung wie bei den drei dokumentierten Mängeln im 166K-Thumbnail
von Kanal B (`formel/thumbnail-checkliste.md`).

## Animations-Loops (`loops/`)

Erzeugt mit `produktion/pipeline/loop_animation.py` — **keine KI-Videoclips**,
sondern mathematische Ebenen über dem Standbild: alle Bewegungen sind Sinus-
bzw. deterministische Rauschfunktionen, deren Frequenzen ganzzahlige Vielfache
von 1/60 s sind. Frame 0 und Frame 1440 sind dadurch **bitidentisch berechenbar**
(gemessen: max. Pixeldifferenz 0 bei allen vier).

Ebenen je Variante: Lichtpuls (drei überlagerte Sinuswellen) überall ·
V1 zusätzlich Sternfunkeln · V2 Nebel-Drift + Wasserglitzern + Sterne ·
V3 Glutflackern + 12 Funken (Helligkeit an beiden Lebensenden null) +
Rauchfahne + Baum-Wiegen + Sterne · V4 Gras-Wiegen + Sterne.
Alles bewusst sehr dezent — Einschlaf-Video, kein Blickfang.

### Messwerte (qa-V?.json)

| | Wrap-Schritt roh | normale Schritte roh (Median/Max) | Naht dekodiert (3×-Rendering) | interne Keyframes (Median/Max) | kbit/s | 3,5 h Bildspur |
|---|---|---|---|---|---|---|
| V1 | 0,0016 | 0,0011 / 0,0576 | 1,284 | 0,998 / 1,295 | 183 | 0,29 GB |
| V2 | 0,0036 | 0,0023 / 0,0125 | 1,470 | 1,134 / 1,435 | 200 | 0,31 GB |
| V3 | 0,0094 | 0,0085 / 0,0195 | 1,532 | 1,313 / 1,505 | 234 | 0,37 GB |
| V4 | 0,0027 | 0,0018 / 0,0209 | 1,406 | 1,104 / 1,412 | 198 | 0,31 GB |

Lesart der Nahtprüfung: Der **rohe** Wrap-Schritt (Bewegung selbst) liegt bei
allen vier innerhalb der normalen Frame-zu-Frame-Bewegung — die Animation
schließt mathematisch exakt. Der **dekodierte** Sprung an der Bitstrom-Naht
(~1,3–1,5 mittlere |Δ|/Pixel von 255) ist kein Animationsfehler, sondern der
Keyframe-Refresh des Encoders — er tritt **in gleicher Höhe alle 10 s mitten im
Stream auf** (interne Keyframes, gemessen). Die Naht ist davon nicht
unterscheidbar; kleiner kann sie physikalisch nicht werden, und YouTube
enkodiert das Material ohnehin neu.

### Bitrate

180–234 kbit/s gegenüber ~200 kbit/s der bisherigen reinen Zoom-Bildspur —
**kein nennenswerter Anstieg** (die Ebenen sind klein und dunkel). 3,5 h
Bildspur ≈ 0,3–0,4 GB, mit Ton ~0,6–0,7 GB gesamt.

### Integration in die Pipeline

Der Atem-Zoom aus `schritt5_video.py` (300-s-Zyklus) bleibt: 300 ist ein
ganzzahliges Vielfaches von 60, der gemeinsame Zyklus schließt also exakt
(5 Loop-Durchläufe je Zoom-Atemzug). Nach der Motiv-Entscheidung wird der
gewählte Loop statt des Standbilds als Quelle des 300-s-Zyklus gerendert;
Montage per Bitstrom-Kopie bleibt unverändert.

## Echte KI-Clips (`loops/ki/`, 2026-08-04)

Bild-zu-Video über Higgsfield, Modell **Seedance 1.5 Pro** (einziges Modell,
dessen 4 Clips ins Guthaben passten — FLUX 3 hätte 180 Credits **je** Clip
gekostet). Loop-Trick: `motiv-V3.png` als `start_image` **und** `end_image`,
dadurch enden alle Clips wieder auf dem Ausgangsbild und sind beliebig
aneinanderreihbar. 4 Clips à 12 s = 48-s-Zyklus.

| Messung (alle 4 Clips) | Wert |
|---|---|
| Auflösung / fps / Dauer | 1920×1080 · 24 fps · 12,04 s |
| Kameradrift (Phasenkorrelation Randzonen) | ≤ 0,05 px — praktisch null |
| erster vs. letzter Frame | mittl. \|Δ\| 2,78–2,91 (nicht pixelidentisch — der Generator trifft das Zielbild nur näherungsweise) |
| Übergangsschritt Clip→Clip (alle 16 Paare) | 2,83–3,14 |
| normaler Frameschritt im Clip | 1,40–1,53 |
| Artefakte | keine verformten Objekte, kein Stilbruch, Figur ruhig; **Rauch deutlich kräftiger als „thin wisps"** — Geschmacksfrage, im 3-min-Test beurteilen |

Ein Schnitt zwischen Clips ist also ≈2× ein normaler Frameschritt — beide
Grenzframes nähern dasselbe ruhige Ausgangsbild an. `kette-3min.mp4` zeigt
16 Übergänge in Produktionsqualität.

**Bitraten-Vorfall, gemeldet:** Die Clips kommen mit ~10,3 Mbit/s. Per
Bitstrom-Kopie geloopt wären das **16,6 GB** für 3,58 h (Lauf nach 15 GB
abgebrochen). Lösung in `schritt5_video.py`: der 48-s-Zyklus wird **einmal**
neu kodiert (CRF 28 → 1,31 Mbit/s), danach loopt die Montage wieder per
Kopie. Gesamtvideo damit ≈ 2,1 GB Bildspur + 0,31 GB Ton ≈ **2,4 GB**
(vorher 0,67 GB mit Standbild-Zoom; CRF 26 wäre mit ≈ 3,3 GB gesamt die
höherwertige Option — `video_crf` in `config.md`).

**Atem-Zoom: entfällt bei `videoquelle = ki_clips`.** Er stört visuell nicht,
aber er ist doppelt verzichtbar: Die PFLICHT aus Formel §5 („Standmotiv mit
sanfter Bewegung") erfüllen die Clips selbst, und ein Zoom obendrauf würde
die kopierfähige Montage in einen vollständigen Re-Encode von 3,5 h
verwandeln (zusätzlich LCM-Zyklus 1200 s). Umschaltbar bleibt beides über
`videoquelle` in `config.md`.

**Gültigkeit:** Diese 4 Clips gehören zum aktuellen `motiv-V3.png`. Fällt die
Handytest-Entscheidung auf eine andere Variante, braucht sie eigene Clips
(erneut 144 Credits bei Seedance 1.5).

## KI-Clips Video 02 (`loops/ki-v02/`, 2026-08-06)

Gleiches Verfahren wie oben, Quelle ist `motiv-video-02.png` als `start_image`
**und** `end_image`.

**Der Preis hat sich halbiert:** Seedance 1.5 Pro kostet jetzt **18 Credits je
Clip** statt 36 — die vier Clips haben **72 Credits** gekostet, nicht die für
V01 vermerkten 144 (belegt im Transaktionsprotokoll, 4 × −18 am 2026-08-06).
Für die Planung der Videos 03–08 gilt der neue Wert.

Drei Prompt-Änderungen gegenüber V01, alle aus dem V01-Befund:

- **Buch ausdrücklich still** („the open book lies completely still — its pages
  do not turn, do not flutter"). Blätternde Seiten wären in einem
  Einschlafvideo ein Blickfang und hätten den Loop gebrochen.
- **Rauch schwächer** („very faint thin wisps, barely visible") — bei V01 war
  er „deutlich kräftiger als bestellt" und als Geschmacksfrage vermerkt.
- Kein Baum mehr im Prompt: dieses Motiv hat keinen.

| Messung | Video 01 | **Video 02** |
|---|---|---|
| Auflösung / fps / Dauer | 1920×1080 · 24 fps · 12,04 s | identisch |
| Kameradrift (Median Randzonen) | ≤ 0,05 px | ≤ 0,065 px |
| erster vs. letzter Frame (mittl. \|Δ\|) | 2,78–2,91 | **2,43–2,49** |
| Übergangsschritt Clip→Clip (16 Paare) | 2,83–3,14 | **2,43–2,70** (Median 2,51) |
| normaler Frameschritt im Clip | 1,40–1,53 | 1,42–1,71 |
| Naht / normaler Schritt | ≈ 2,0 | **1,75** |
| Bitrate der Kette (CRF 28) | 1,31 Mbit/s | 1,27 Mbit/s |

Die Nähte sind also **relativ kleiner** als bei Video 01: der Sprung an einem
Schnitt ist nur noch das 1,75-fache eines normalen Frameschritts. Schlimmstes
Paar `clip-2 → clip-1` mit 2,695.

Nahtsichtung an `kette-3min.mp4` (16 Übergänge, Produktionsqualität, 192,7 s):
Figur, Buch, Fels und Hügellinie stehen über den Schnitt hinweg exakt still;
sichtbar wechselt allein die Flammenform — die ändert sich innerhalb eines
Clips ohnehin von Frame zu Frame. Gemessen an den beiden geprüften Nähten
3,27 (Clip 1→2) und 3,46 (Clip 4→1, der Loop-Rücksprung).

Hochgerechnet auf die 3,52 h Laufzeit: **≈ 2,0 GB Bildspur**, mit Ton ≈ 2,3 GB.

**Zuordnung:** Diese Clips gehören zu `motiv-video-02.png` und zu keinem
anderen Motiv. Die Pipeline liest den Ordner deshalb je Video aus
`ki_clip_ordner_V2` in `config.md`; der allgemeine `ki_clip_ordner` bleibt
für V01 stehen.
