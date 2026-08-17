# Messungen für das Regelwerk Kanal 2 — Datengrundlage

> Erhebung vom **2026-08-10**. Teil A (Gruppen) und Teil B (Messen) des
> Auftrags. **0 Credits ausgegeben** — ausschließlich kostenlose Werkzeuge:
> `youtube_channel_about`, `youtube_channel_videos`, `youtube_video_details`,
> `get_video_transcript`, `search_niche_finder_channels`,
> `get_batch_channel_metrics_v2`, dazu eigene Messskripte auf
> heruntergeladenen Thumbnails.
>
> **Dieses Dokument enthält keine Regeln.** Es zählt aus und tabelliert.
> Die Ableitung von Regeln ist ausdrücklich nicht Teil dieses Auftrags;
> Stilanalyse und Videosichtung (Teil C) ebenfalls nicht — deshalb wurde
> `watch_youtube_video_and_ask` nirgends aufgerufen.
>
> Kennzeichnung wie in `recherche/nischen-kanal-2.md`:
> **[gemessen]** = direkt aus einem Tool-Ergebnis oder einer eigenen Messung ·
> **[geschätzt]** = NexLev-Modellwert · **n. e.** = nicht ermittelbar.
> Wo eine Zahl fehlt, steht „n. e." — nichts ist geschätzt worden.

## Was hier belastbar ist und was nicht

| Größe | Herkunft | Belastbarkeit |
|---|---|---|
| Gründungsdatum, Abos, Videoanzahl, Gesamtviews | `youtube_channel_about` | **[gemessen]**, direkt von YouTube |
| Videotitel, Views, Länge | `youtube_channel_videos` + `youtube_video_details` | **[gemessen]**; Listenviews sind gerundet, in den Einzelmessungen stehen die exakten Werte aus `video_details` |
| Wortzahl, WPM, Marker, CTAs, Einstiegstyp | eigene Messung am ASR-Transkript | **[gemessen]**, aber ASR-Transkripte enthalten Hörfehler und keine Satzzeichen |
| Versalhöhe, Kontrast, Wortzahl im Thumbnail | eigene Messung am heruntergeladenen Bild | **[gemessen]** |
| Monatsumsatz, RPM | NexLev-Modell | **[geschätzt]** — Modellwerte, keine Auszahlungen |
| Monetarisierung | `get_batch_channel_metrics_v2` | **[gemessen]** im Sinne von „Tool meldet Status" |

**Zwei RPM-Werte je Kanal.** Suche (`rpm.total`) und Batch-Metrics liefern
unterschiedliche Zahlen für denselben Kanal (Ink Explainer: 3,96 gegen 2,85).
In den Tabellen steht der Batch-Wert, weil er am selben Tag für alle Kanäle
einheitlich gezogen wurde; beide liegen in den Rohdaten.

## Methodik der einzelnen Messungen

**Long-Form** = Videolänge über 180 s. Shorts sind überall ausgeschlossen.

**Treffer und schwaches Video je Kanal.** Treffer = das meistgesehene
Long-Form-Video. Schwach = das am wenigsten gesehene Long-Form-Video, das
älter als 30 Tage ist (Veröffentlichung vor 2026-07-11) — die Altersgrenze
verhindert, dass ein frisch hochgeladenes Video als „schwach" gilt, nur weil
es noch keine Zeit hatte.

**Epistemische Marker** je 1.000 Wörter: Wortlisten-Heuristik, wie in
`recherche/nischen-kanal-2.md` („Umgang mit unsicheren Fakten") eingeführt.
Gezählt werden echte Unsicherheits-Kennzeichnungen in vier Klassen: explizites
Nichtwissen („we don't know", „remains a mystery"), Theorie-Zuschreibung („the
most common theory", „historians believe"), Evidenz-Hedges („evidence
suggests", „appears to") und Abschwächungs-Adverbien („probably", „possibly",
„may have"). Überlappende Treffer werden nur einmal gezählt. Die Liste steht
offen in `regeln/daten/skript_metriken.py`. **Kalibrierprobe:** Am selben
Video wie in der bestehenden Auswertung (Ink Explainer, „Rained All Week")
ergibt die Messung **3,7 Marker je 1.000 Wörter** — derselbe Wert wie dort.

**CTAs**: Treffer aus einer Musterliste (subscribe, like, comment, Patreon,
Mitgliedschaft, Link in der Beschreibung, Glocke). Treffer im Abstand unter
15 s zählen als ein Ereignis, damit ein zusammenhängender Aufruf nicht
mehrfach gezählt wird. Position in Sekunden und in Prozent der Laufzeit.

**Einstiegstyp der ersten 60 s** wird am ersten Satz klassifiziert, Vorrang in
dieser Reihenfolge: *du-versetzung* (beginnt mit „You…", „Imagine", „Picture
this", „If you…"), *szene-datum-ort* (beginnt mit Datum, Jahreszahl, Ort oder
„X million years ago"), *ankuendigung* („Today we're going over…", „Here are…",
„Tier one…"), sonst *aussage-these*. Dazu die Sekunde, in der die zweite
Person zum ersten Mal fällt, und ob in den ersten 60 s eine Zahl vorkommt.
Der volle Wortlaut der ersten 60 s steht je Video in
`regeln/daten/skript.json`.

**Titelauszählung** über alle erfassten Long-Form-Titel eines Kanals.
*Frageform* = endet mit „?" **oder** beginnt mit Fragewort/Hilfsverb;
*Zahl* = enthält eine Ziffer; *Superlativ* = Positivliste (most, best, worst,
deadliest, darkest, …); *Extremwort* = first, last, only, ever, never, all,
entire, every, actually, really, secret, hidden, forbidden, banned. „Treffer"
und „Flops" sind das obere und untere Drittel nach Views **innerhalb**
desselben Kanals — so vergleicht die Auszählung Titel gegen Titel derselben
Marke, nicht gegen fremde Reichweite.

**Quellenangaben ja/nein** an den Videobeschreibungen der beiden vermessenen
Videos: ein Quellenblock („Sources:", „References:") oder mindestens zwei
akademische Links (DOI, Journal, Universität). **Musiklizenz-Quellen zählen
nicht** — ein „Source: chriszabriskie.com" unter einer Creative-Commons-Musik
ist keine inhaltliche Quellenangabe. Diese Ausnahme wurde nachträglich
eingebaut, nachdem sie bei Prehistoric Archive einen Fehltreffer erzeugt hatte.

**Thumbnails**: Methodik nach dem Muster von `formel/thumbnail-checkliste.md`
im BibelTube-Repo — **die Schwellenwerte von dort wurden bewusst nicht
übernommen**, gemessen wird ergebnisoffen. Bild in Originalauflösung geladen
(`maxresdefault`, sonst `sddefault`/`hqdefault`), Gitternetz in 5-%-Schritten
darübergelegt, Textbereich am Gitter bestimmt. Im Textbereich trennt eine
Otsu-Schwelle Schrift und direkten Hintergrund; **Versalhöhe** = Höhe der
größten zusammenhängenden Textzeile in Prozent der Bildhöhe (bei mehrzeiligem
Text die dominante Zeile, nicht der ganze Block); **Kontrast** = WCAG-Verhältnis
der beiden Luminanz-Cluster, gerechnet mit derselben Relativluminanz-Formel wie
`produktion/pipeline/thumbnail.py`. Der Feed-Test verkleinert jedes Bild auf
160 × 90 px, die Größe im Handy-Feed.

## Teil A — die drei Gruppen

### Wie gesucht wurde

Drei Läufe von `search_niche_finder_channels` am 2026-08-10, dazu ein
Wildcard-Lauf über die junge Kohorte und gezielte Namens-Queries für Kanäle,
die in keinem Listenlauf auftauchten:

| Lauf | Filter | Treffer |
|---|---|---|
| G1-Lauf | Query „history explainer ancient humans everyday life", `channelCreatedAfter` 2026-04-01, `minMonthlyRevenue` 2000 | 50, `hasMore` |
| G2-Lauf | dieselbe Query, `channelCreatedBefore` 2025-08-10, `minMonthlyRevenue` 1000 | 50, `hasMore` |
| **G3-Lauf** | dieselbe Query, `channelCreatedAfter` 2025-08-10, **ohne Umsatzuntergrenze**, `maxMonthlyRevenue` 200 | **50, `hasMore`** |
| Wildcard | `*`, `channelCreatedAfter` 2026-04-01, `minMonthlyRevenue` 2000 | 169 über zwei Seiten |

Die Gruppenzugehörigkeit wurde anschließend gegen `youtube_channel_about`
geprüft — das Gründungsdatum von YouTube hat Vorrang vor dem Katalogdatum.

### G1 — junge Gewinner

Kriterium: gegründet nach 2026-04-10, mindestens 2.000 $/Monat.

Die fünf vorgegebenen Kanäle wurden um drei aus dem G1-Lauf ergänzt: **Mogo**,
**Banana Explains**, **Prehistoria Hub**. Auswahlgrund war thematische Nähe bei
gleichzeitig unterschiedlichem Produktionsstil — Mogo und Banana Explains
fahren dieselbe Strichfiguren-Handschrift wie Ink Explainer, Prehistoria Hub
dagegen KI-Fotorealismus. Damit enthält die Gruppe beide Bauformen.

**Zwei Kanäle verfehlen die Umsatzschwelle** und bleiben nur drin, weil der
Auftrag sie ausdrücklich nennt:

| Kanal | Katalogumsatz | Abweichung |
|---|---|---|
| Noxenn | 1.123 $/Mon | **unter 2.000 $** |
| Prehistoric Archive | 1.074 $/Mon | **unter 2.000 $** |

Beide sind monetarisiert und wachsen, aber nach dem Auftragskriterium wären sie
keine „Gewinner". Streng gerechnet erfüllen **6 von 8** G1-Kanälen die
Schwelle. Die Werte stehen so in den Tabellen; nichts wurde geglättet.

### G2 — etablierte Gewinner

Kriterium: älter als 12 Monate, mindestens 1.000 $/Monat. Die vier
vorgegebenen Kanäle plus **History Mapped Out** und **Professor Historian**
aus dem G2-Lauf. Alle sechs erfüllen beide Kriterien.

Historically und quack doc erscheinen in keinem der Listenläufe (der
Wildcard-Lauf filtert auf Gründung nach 2026-04-01); ihre Katalogwerte wurden
per Namens-Query nachgezogen, ebenfalls Stand 2026-08-10.

### G3 — Verlierer

Kriterium: jünger als 12 Monate, unter 200 $/Monat, mindestens 8 Videos.
Gesucht wie beauftragt **ohne Umsatzuntergrenze, mit `maxMonthlyRevenue` 200**.

**Die Gruppe ließ sich problemlos besetzen** — der Lauf lieferte 50 Treffer
mit `hasMore`, also mehr Kandidaten als gebraucht. Das ist selbst ein Befund:
Die Nische produziert deutlich mehr junge Kanäle unter 200 $/Monat als
darüber. Aus den 50 wurden sechs gewählt, die laut Suche **monetarisiert sind
und trotzdem unter 200 $ liegen** — das trennt Publikumsversagen von bloßer
fehlender Programmfreigabe. Ein siebter (Sten Explains) kam als Reserve dazu,
weil er aus derselben Gründungskohorte wie die G1-Gewinner stammt und damit
den direktesten Vergleich erlaubt.

**Nachtrag aus der Prüfung:** `get_batch_channel_metrics_v2` widerspricht der
Suche bei zweien der sieben — HUMAN-ISH und Sten Explains gelten dort als
**nicht** monetarisiert. Fünf der sieben G3-Kanäle sind damit nach beiden
Quellen freigeschaltet und verdienen trotzdem zwischen 5 und 111 $/Monat.
Der Befund „Umsatz fehlt trotz Freigabe" trägt also für fünf Kanäle, nicht
für sieben.

Bewusst **nicht** aufgenommen wurden die vielen nicht monetarisierten Kanäle
mit hohen Abozahlen aus dem G3-Lauf (etwa Primal Earth Channel, 126.000 Abos,
0 $/Mon; Ancient Bloodline, 99.800 Abos, 0 $/Mon). Bei ihnen ist unklar, ob
das Publikum fehlt oder nur die Monetarisierung — sie hätten die Gruppe
verwässert.

## Übersicht nach Gruppen

| Gruppe | Kanäle (n) | Alter Mon. Med. | $/Mon Med. | Views/Video Med. | Up/Wo Med. | Länge Med. | mit Quellen | Videos (n) | WPM Med. | Wörter Med. | Du-Einstieg | epist./1.000 W Med. | Thumbs ohne Text | Versalh. % Med. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | 8 | 2.9 | 2878.2 | 4.950 | 3.6 | 23:45 | 4/8 | 16 | 158 | 2925.5 | 12/16 | 1.1 | 2/16 | 16.5 |
| G2 | 6 | 41.2 | 5410.9 | 54.000 | 0.4 | 19:38 | 0/6 | 12 | 163 | 2158.5 | 0/12 | 1.6 | 5/12 | 17.9 |
| G3 | 7 | 3.3 | 67.8 | 1.250 | 1.2 | 9:51 | 3/7 | 12 | 165 | 1530.5 | 6/12 | 1.2 | 4/14 | 18.6 |

## Struktur je Kanal

| Gr. | Kanal | gegr. | Alter Mon. | Long-Form | Abos | $/Mon | Up/Wo L/K | Länge Median | Spanne | RPM | Mon. | Quellen | Kapitel | Views Median | Views Max | Spreizung |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Axen | 2026-04-28 | 3.4 | 13 | 53.600 | 3089.73 | 0.88 / 0.25 | 8:33 | 5:15–12:41 | 4.22 | ja | ja | 0 | 25.000 | 3.100.000 | 124x |
| G1 | Banana Explains | 2026-06-08 | 2.1 | 36 | 4.230 | 3902.56 | 4.0 / 4 | 23:35 | 17:02–28:19 | 6.62 | ja | nein | 0 | 4.000 | 448.000 | 112x |
| G1 | Before Civilization | 2026-04-28 | 3.4 | 69 | 14.200 | 2638.97 | 4.64 / 5.25 | 25:00 | 5:46–36:32 | 5.69 | ja | ja | 5 | 5.900 | 492.000 | 83x |
| G1 | Ink Explainer | 2026-04-09 | 4.0 | 13 | 47.600 | 9560.49 | 0.74 / 0.5 | 8:24 | 4:09–12:48 | 2.85 | ja | ja | 0 | 196.000 | 1.100.000 | 6x |
| G1 | Mogo | 2026-06-08 | 2.1 | 33 | 2.640 | 3840.91 | 3.67 / 4.5 | 23:56 | 20:05–28:16 | 6.4 | ja | nein | 0 | 3.300 | 389.000 | 118x |
| G1 | Noxenn | 2026-05-12 | 3.0 | 46 | 3.610 | 1123.39 | 3.58 / 4.5 | 17:28 | 10:29–25:22 | 4.17 | ja | ja | 0 | 2.850 | 130.000 | 46x |
| G1 | Prehistoria Hub | 2026-05-21 | 2.7 | 18 | 5.000 | 2666.57 | 1.56 / 2 | 32:03 | 22:28–40:14 | 5.89 | ja | nein | 0 | 10.500 | 502.000 | 48x |
| G1 | Prehistoric Archive | 2026-06-03 | 2.2 | 65 | 1.830 | 1074.43 | 6.69 / 6.75 | 24:54 | 10:44–67:19 | 9.72 | ja | nein | 0 | 1.100 | 103.000 | 94x |
| G2 | First Humans | 2025-05-24 | 14.6 | 50 | 33.200 | 4910.02 | 0.79 / 1.5 | 8:40 | 8:01–16:05 | 4.3 | ja | nein | 0 | 47.000 | 2.300.000 | 49x |
| G2 | Folks of Yore | 2024-09-22 | 22.6 | 21 | 21.000 | 1249.28 | 0.21 / 0.25 | 20:56 | 10:04–30:14 | 5.77 | ja | nein | 7 | 6.300 | 657.000 | 104x |
| G2 | Historically | 2023-03-08 | 41.1 | 21 | 1.330.000 | 12956.13 | 0.12 / 0.5 | 18:21 | 3:01–74:36 | 5.99 | ja | nein | 8 | 1.800.000 | 6.100.000 | 3x |
| G2 | History Mapped Out | 2023-02-27 | 41.4 | 134 | 176.000 | 2158.28 | 0.74 / 1.75 | 22:04 | 7:08–38:21 | 4.81 | ja | nein | 0 | 95.000 | 1.800.000 | 19x |
| G2 | Professor Historian | 2007-04-04 | 232.2 | 24 | 28.100 | 5911.68 | 0.02 / 1.5 | 15:15 | 12:13–68:03 | 7.51 | ja | nein | 11 | 17.500 | 4.600.000 | 263x |
| G2 | quack doc | 2023-01-22 | 42.6 | 126 | 148.000 | 11790.16 | 0.68 / 1.25 | 49:47 | 7:26–427:57 | 11.6 | ja | nein | 25 | 61.000 | 1.900.000 | 31x |
| G3 | Endless Origins | 2025-09-23 | 10.5 | 38 | 1.790 | 91.44 | 0.83 / 1.75 | 9:51 | 4:44–30:21 | 4.53 | ja | nein | 0 | 1.250 | 360.000 | 288x |
| G3 | ExplainMatics | 2026-05-04 | 3.2 | 10 | 5.200 | 67.82 | 0.71 / 0.75 | 8:17 | 3:37–10:19 | 7.15 | ja | ja | 0 | 771 | 652.000 | 845x |
| G3 | HUMAN-ISH | 2026-05-03 | 3.3 | 34 | 3.880 | 98.71 | 2.4 / 1.5 | 14:35 | 8:11–19:30 | 4.88 | nein* | nein | 0 | 997 | 408.000 | 409x |
| G3 | Histor | 2026-03-09 | 5.1 | 26 | 1.860 | 5.02 | 1.18 / 0.75 | 17:58 | 16:58–25:50 | 2.73 | ja | nein | 0 | 2.400 | 57.000 | 24x |
| G3 | Million-Year Prehistory | 2025-12-17 | 7.8 | 11 | 1.900 | 110.88 | 0.33 / 0 | 13:14 | 8:25–58:56 | 2.42 | ja | nein | 0 | 2.500 | 394.000 | 158x |
| G3 | Sten Explains | 2026-05-22 | 2.6 | 18 | 830 | 0 | 1.57 / 1.25 | 9:04 | 8:17–10:30 | 3.34 | nein | ja | 10 | 2.400 | 36.000 | 15x |
| G3 | ThenFolk | 2026-05-04 | 3.2 | 54 | 2.020 | 19.95 | 3.86 / 4.5 | 8:26 | 8:02–10:32 | 3.34 | ja | ja | 0 | 499 | 144.000 | 288x |

## Skript je Video

| Gr. | Kanal | Rolle | Video | Views | Wörter | WPM | Einstieg | 1. Anrede | Aufbau | CTA (Position) | epist./1.000 W | 2. Pers./1.000 W |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Axen | treffer | What Did Ancient Humans Do all Day Bef | 3.167.434 | 1.588 | 186 | du-versetzung | 0.0 s | fliess | 0 | 0.6 | 26.4 |
| G1 | Axen | schwach | Napoleon Did Some Truly Bizarre Things | 9.933 | 1.082 | 190 | aussage-these | 18.2 s | fliess | 0 | 1.8 | 8.3 |
| G1 | Banana Explains | treffer | Where Do You Go Under Anesthesia?  | 448.000 | 3.468 | 153 | du-versetzung | 0.0 s | fliess | 0 | 1.2 | 14.7 |
| G1 | Banana Explains | schwach | Why Did Ancient Humans Start Making Mu | 1.000 | 3.268 | 147 | du-versetzung | 0.0 s | fliess | 0 | 0.9 | 20.2 |
| G1 | Before Civilization | treffer | The Darkest Things Ancient Humans Did  | 492.395 | 1.226 | 157 | du-versetzung | 0.0 s | ohne signal | 0 | 6.5 | 19.6 |
| G1 | Before Civilization | schwach | The Darkest Things Ancient Humans Did  | 1.316 | 2.362 | 167 | du-versetzung | 0.0 s | liste | 1 (50 %) | 1.7 | 23.7 |
| G1 | Ink Explainer | treffer | What Did Ancient Humans Do When It Rai | 1.196.165 | 2.439 | 210 | du-versetzung | 0.0 s | fliess | 0 | 3.7 | 25.0 |
| G1 | Ink Explainer | schwach | what is The IKEA Effect. | 7.237 | 766 | 185 | du-versetzung | 0.0 s | fliess | 1 (28 %) | 0.0 | 67.9 |
| G1 | Mogo | treffer | Why Don’t We Eat Other Animal Eggs? | 389.797 | 3.193 | 159 | du-versetzung | 0.0 s | ohne signal | 1 (77 %) | 0.0 | 2.8 |
| G1 | Mogo | schwach | Where Are You When You Dream? | 569 | 3.220 | 155 | du-versetzung | 0.0 s | fliess | 0 | 0.6 | 42.5 |
| G1 | Noxenn | treffer | Why Did Ancient Humans Have Kids at 12 | 130.000 | 2.658 | 159 | du-versetzung | 0.0 s | fliess | 0 | 4.9 | 17.3 |
| G1 | Noxenn | schwach | What Did Ancient Humans Dream About? | 264 | 1.776 | 155 | du-versetzung | 0.0 s | fliess | 0 | 0.6 | 30.4 |
| G1 | Prehistoria Hub | treffer | The Last 24 Hours of the Dinosaurs — M | 502.608 | 4.597 | 133 | szene-datum-ort | 110.5 s | ohne signal | 0 | 0.2 | 2.0 |
| G1 | Prehistoria Hub | schwach | Earth's Nightmare Era: The Swamp World | 4.473 | 3.813 | 154 | du-versetzung | 15.0 s | ohne signal | 1 (98 %) | 1.6 | 5.2 |
| G1 | Prehistoric Archive | treffer | What Was Living in a Cave During the I | 103.000 | 4.967 | 140 | aussage-these | 56.8 s | ohne signal | 2 (3 %, 29 %) | 4.2 | 1.0 |
| G1 | Prehistoric Archive | schwach | The Prehistoric Predator That Hunted H | 114 | 3.267 | 162 | szene-datum-ort | 26.3 s | fliess | 0 | 0.0 | 4.6 |
| G2 | First Humans | treffer | Scientists Finally Solved The Roanoke  | 2.300.000 | 1.591 | 181 | szene-datum-ort | 194.2 s | ohne signal | 1 (98 %) | 1.9 | 5.7 |
| G2 | First Humans | schwach | Ancient Human Species We Once Shared t | 1.300 | 1.528 | 149 | szene-datum-ort | n. e. | ohne signal | 0 | 14.4 | 0.0 |
| G2 | Folks of Yore | treffer | Your "Busy" Life Would Disgust an Anci | 657.000 | 1.909 | 142 | aussage-these | 5.9 s | fliess | 0 | 0.0 | 44.0 |
| G2 | Folks of Yore | schwach | What It Was Actually Like to Be a Rena | 1.200 | 2.700 | 142 | aussage-these | 154.6 s | fliess | 1 (99 %) | 1.5 | 7.8 |
| G2 | Historically | treffer | The ENTIRE History of ROME | 6.194.859 | 6.630 | 172 | aussage-these | 58.6 s | gemischt | 1 (100 %) | 1.8 | 10.3 |
| G2 | Historically | schwach | The Dumbest Heist in History | 792.509 | 2.109 | 180 | szene-datum-ort | 45.0 s | fliess | 0 | 0.9 | 13.3 |
| G2 | History Mapped Out | treffer | The Reconquista: The Victory of Christ | 1.812.656 | 3.092 | 142 | aussage-these | n. e. | ohne signal | 0 | 0.0 | 0.0 |
| G2 | History Mapped Out | schwach | Money Through Time: From Antiquity to  | 5.431 | 2.068 | 159 | aussage-these | 747.3 s | fliess | 0 | 0.0 | 0.5 |
| G2 | Professor Historian | treffer | Ancient Technologies We Still Can't Ex | 4.600.000 | 2.509 | 151 | ankuendigung | 327.7 s | liste | 0 | 4.4 | 4.0 |
| G2 | Professor Historian | schwach | Every Poison Used in Ancient Civilizat | 3.500 | 2.208 | 167 | aussage-these | 2.5 s | fliess | 0 | 0.9 | 30.8 |
| G2 | quack doc | treffer | The Most Disturbing Afterlife Theories | 1.900.000 | 10.172 | 181 | ankuendigung | 0.2 s | gemischt | 2 (30 %, 100 %) | 2.1 | 41.0 |
| G2 | quack doc | schwach | Things That Would Get You Killed In Th | 4.500 | 1.551 | 188 | aussage-these | 11.3 s | ohne signal | 1 (99 %) | 1.9 | 63.2 |
| G3 | Endless Origins | treffer | Life 20,000 Years Ago | How Humans Sle | 360.000 | 812 | 127 | du-versetzung | 12.6 s | fliess | 0 | 6.2 | 3.7 |
| G3 | Endless Origins | schwach | Life 700 Years Ago: The Bubonic Plague | 142 | 1.096 | 116 | du-versetzung | n. e. | ohne signal | 0 | 0.9 | 0.0 |
| G3 | ExplainMatics | treffer | How Did Ancient Humans Survive Sicknes | 652.932 | 1.387 | 171 | du-versetzung | 0.0 s | fliess | 0 | 1.4 | 13.0 |
| G3 | ExplainMatics | schwach | Every Social Media Addiction Trick (In | 191 | 1.703 | 174 | aussage-these | 2.5 s | ohne signal | 4 (19 %, 27 %, 88 %, 98 %) | 1.2 | 71.6 |
| G3 | HUMAN-ISH | treffer | What Did Ancient Humans Do When Someon | 408.000 | 1.564 | 148 | du-versetzung | 0.0 s | fliess | 0 | 1.3 | 6.4 |
| G3 | HUMAN-ISH | schwach | Why Do We Hiccup Like a 375 Million Ye | 98 | 1.337 | 159 | du-versetzung | 0.0 s | ohne signal | 0 | 3.7 | 38.1 |
| G3 | Histor | treffer | These Photos Expose the RAW Reality of | 57.702 | 2.019 | 112 | aussage-these | 658.8 s | ohne signal | 1 (100 %) | 0.0 | 2.0 |
| G3 | Histor | schwach | These Photos Expose the RAW Reality of | 368 | 3.127 | 121 | aussage-these | 296.6 s | ohne signal | 1 (100 %) | 0.0 | 3.5 |
| G3 | Million-Year Prehistory | treffer | Life Millions of Years Ago: Homo Habil | 394.000 | — | — | — | — | — | — | — |
| G3 | Million-Year Prehistory | schwach | Life Millions of Years Ago | Homo Habi | 716 | — | — | — | — | — | — | — |
| G3 | Sten Explains | treffer | Did Animals Accidentally Make Us Human | 36.000 | 1.511 | 182 | aussage-these | 0.0 s | fliess | 0 | 2.6 | 13.2 |
| G3 | Sten Explains | schwach | Did Ancient Humans Fall in Love Like W | 457 | 1.482 | 176 | aussage-these | 0.0 s | fliess | 0 | 1.3 | 31.0 |
| G3 | ThenFolk | treffer | Why Did Animals Fear Ancient Humans Wh | 144.000 | 1.569 | 171 | du-versetzung | 0.0 s | fliess | 0 | 0.0 | 28.7 |
| G3 | ThenFolk | schwach | How Ancient Humans Dealt with Nightmar | 75 | 1.550 | 189 | aussage-these | 0.0 s | fliess | 0 | 0.0 | 42.6 |

## Titel — Gruppenaggregat

| Gruppe | Titel (n) | Frageform | mit „?" | Zahl | Superlativ | Extremwort | Wörter Med. | Zeichen Med. |
|---|---|---|---|---|---|---|---|---|
| G1 | 293 | 76 % | 64 % | 10 % | 8 % | 20 % | 8 | 49 |
| G2 | 376 | 7 % | 1 % | 12 % | 15 % | 16 % | 7.0 | 48.0 |
| G3 | 191 | 56 % | 49 % | 22 % | 7 % | 15 % | 9 | 55 |

## Titel je Kanal

| Gr. | Kanal | Menge | n | Frageform | mit „?" | Zahl | Superlativ | Extremwort | Wörter Med. | Zeichen Med. |
|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Axen | alle | 13 | 77 % | 77 % | 0 % | 15 % | 23 % | 7 | 46 |
| G1 | Axen | treffer | 4 | 100 % | 100 % | 0 % | 25 % | 25 % | 8.0 | 50.5 |
| G1 | Axen | flops | 4 | 50 % | 50 % | 0 % | 25 % | 50 % | 6.0 | 36.0 |
| G1 | Banana Explains | alle | 36 | 100 % | 100 % | 3 % | 3 % | 11 % | 7.0 | 41.5 |
| G1 | Banana Explains | treffer | 12 | 100 % | 100 % | 0 % | 0 % | 0 % | 6.0 | 40.5 |
| G1 | Banana Explains | flops | 12 | 100 % | 100 % | 0 % | 8 % | 17 % | 7.0 | 42.0 |
| G1 | Before Civilization | alle | 69 | 70 % | 48 % | 10 % | 12 % | 20 % | 9 | 54 |
| G1 | Before Civilization | treffer | 23 | 65 % | 48 % | 17 % | 17 % | 30 % | 10 | 56 |
| G1 | Before Civilization | flops | 23 | 70 % | 48 % | 4 % | 9 % | 13 % | 9 | 50 |
| G1 | Ink Explainer | alle | 13 | 85 % | 54 % | 0 % | 8 % | 15 % | 7 | 46 |
| G1 | Ink Explainer | treffer | 4 | 100 % | 75 % | 0 % | 0 % | 50 % | 8.5 | 49.0 |
| G1 | Ink Explainer | flops | 4 | 100 % | 25 % | 0 % | 25 % | 0 % | 7.5 | 42.0 |
| G1 | Mogo | alle | 33 | 100 % | 100 % | 9 % | 3 % | 6 % | 7 | 37 |
| G1 | Mogo | treffer | 11 | 100 % | 100 % | 9 % | 0 % | 9 % | 7 | 36 |
| G1 | Mogo | flops | 11 | 100 % | 100 % | 18 % | 0 % | 0 % | 7 | 37 |
| G1 | Noxenn | alle | 46 | 100 % | 98 % | 11 % | 0 % | 26 % | 7.0 | 40.0 |
| G1 | Noxenn | treffer | 15 | 100 % | 93 % | 13 % | 0 % | 40 % | 7 | 40 |
| G1 | Noxenn | flops | 15 | 100 % | 100 % | 7 % | 0 % | 27 % | 8 | 39 |
| G1 | Prehistoria Hub | alle | 18 | 17 % | 0 % | 28 % | 22 % | 39 % | 10.5 | 61.0 |
| G1 | Prehistoria Hub | treffer | 6 | 17 % | 0 % | 50 % | 0 % | 83 % | 11.5 | 59.5 |
| G1 | Prehistoria Hub | flops | 6 | 17 % | 0 % | 17 % | 33 % | 33 % | 9.5 | 56.0 |
| G1 | Prehistoric Archive | alle | 65 | 57 % | 37 % | 14 % | 11 % | 22 % | 11 | 67 |
| G1 | Prehistoric Archive | treffer | 21 | 57 % | 29 % | 24 % | 19 % | 14 % | 12 | 70 |
| G1 | Prehistoric Archive | flops | 21 | 48 % | 38 % | 5 % | 10 % | 33 % | 11 | 62 |
| G2 | First Humans | alle | 50 | 2 % | 0 % | 24 % | 2 % | 26 % | 9.5 | 60.0 |
| G2 | First Humans | treffer | 16 | 6 % | 0 % | 25 % | 0 % | 31 % | 10.0 | 61.0 |
| G2 | First Humans | flops | 16 | 0 % | 0 % | 19 % | 0 % | 19 % | 9.0 | 56.5 |
| G2 | Folks of Yore | alle | 21 | 38 % | 0 % | 10 % | 5 % | 33 % | 9 | 54 |
| G2 | Folks of Yore | treffer | 7 | 43 % | 0 % | 14 % | 0 % | 0 % | 8 | 55 |
| G2 | Folks of Yore | flops | 7 | 29 % | 0 % | 0 % | 14 % | 43 % | 10 | 54 |
| G2 | Historically | alle | 21 | 10 % | 5 % | 14 % | 24 % | 29 % | 5 | 29 |
| G2 | Historically | treffer | 7 | 14 % | 14 % | 29 % | 29 % | 29 % | 4 | 26 |
| G2 | Historically | flops | 7 | 14 % | 0 % | 14 % | 29 % | 29 % | 5 | 28 |
| G2 | History Mapped Out | alle | 134 | 6 % | 0 % | 7 % | 5 % | 4 % | 9.0 | 51.5 |
| G2 | History Mapped Out | treffer | 44 | 2 % | 0 % | 5 % | 5 % | 5 % | 8.5 | 50.0 |
| G2 | History Mapped Out | flops | 44 | 5 % | 0 % | 16 % | 7 % | 5 % | 9.0 | 52.5 |
| G2 | Professor Historian | alle | 24 | 0 % | 0 % | 12 % | 50 % | 25 % | 6.5 | 42.0 |
| G2 | Professor Historian | treffer | 8 | 0 % | 0 % | 25 % | 62 % | 12 % | 6.0 | 41.5 |
| G2 | Professor Historian | flops | 8 | 0 % | 0 % | 12 % | 25 % | 38 % | 7.0 | 47.5 |
| G2 | quack doc | alle | 126 | 6 % | 1 % | 13 % | 25 % | 18 % | 6.0 | 43.0 |
| G2 | quack doc | treffer | 42 | 2 % | 0 % | 17 % | 31 % | 12 % | 6.0 | 44.0 |
| G2 | quack doc | flops | 42 | 10 % | 2 % | 14 % | 31 % | 29 % | 7.0 | 40.5 |
| G3 | Endless Origins | alle | 38 | 5 % | 0 % | 92 % | 0 % | 18 % | 12.0 | 61.5 |
| G3 | Endless Origins | treffer | 12 | 0 % | 0 % | 100 % | 0 % | 17 % | 12.0 | 61.5 |
| G3 | Endless Origins | flops | 12 | 17 % | 0 % | 75 % | 0 % | 25 % | 11.0 | 56.0 |
| G3 | ExplainMatics | alle | 10 | 50 % | 30 % | 40 % | 20 % | 40 % | 8.0 | 46.5 |
| G3 | ExplainMatics | treffer | 3 | 100 % | 33 % | 33 % | 0 % | 67 % | 8 | 51 |
| G3 | ExplainMatics | flops | 3 | 33 % | 33 % | 67 % | 0 % | 33 % | 8 | 44 |
| G3 | HUMAN-ISH | alle | 34 | 79 % | 71 % | 3 % | 3 % | 9 % | 8.0 | 49.5 |
| G3 | HUMAN-ISH | treffer | 11 | 82 % | 82 % | 0 % | 9 % | 9 % | 8 | 47 |
| G3 | HUMAN-ISH | flops | 11 | 82 % | 82 % | 9 % | 0 % | 18 % | 8 | 49 |
| G3 | Histor | alle | 26 | 8 % | 0 % | 0 % | 0 % | 0 % | 14.0 | 81.0 |
| G3 | Histor | treffer | 8 | 12 % | 0 % | 0 % | 0 % | 0 % | 14.0 | 81.0 |
| G3 | Histor | flops | 8 | 0 % | 0 % | 0 % | 0 % | 0 % | 14.0 | 81.0 |
| G3 | Million-Year Prehistory | alle | 11 | 0 % | 0 % | 18 % | 9 % | 0 % | 14 | 74 |
| G3 | Million-Year Prehistory | treffer | 3 | 0 % | 0 % | 0 % | 0 % | 0 % | 13 | 74 |
| G3 | Million-Year Prehistory | flops | 3 | 0 % | 0 % | 67 % | 33 % | 0 % | 15 | 85 |
| G3 | Sten Explains | alle | 18 | 100 % | 83 % | 0 % | 6 % | 11 % | 8.0 | 44.5 |
| G3 | Sten Explains | treffer | 6 | 100 % | 50 % | 0 % | 17 % | 17 % | 7.5 | 45.5 |
| G3 | Sten Explains | flops | 6 | 100 % | 100 % | 0 % | 0 % | 0 % | 7.5 | 48.5 |
| G3 | ThenFolk | alle | 54 | 98 % | 96 % | 0 % | 15 % | 22 % | 8.0 | 53.5 |
| G3 | ThenFolk | treffer | 18 | 94 % | 89 % | 0 % | 11 % | 33 % | 9.0 | 54.5 |
| G3 | ThenFolk | flops | 18 | 100 % | 100 % | 0 % | 22 % | 17 % | 8.0 | 44.5 |

## Thumbnails

| Gr. | Kanal | Rolle | Text im Bild | Wörter | Zeilen | Versalhöhe | Kontrast | Position | Figur | Bildstil | Feed lesbar |
|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Axen | schwach | WEIRDEST EMPEROR? | 2 | 1 | 13.5 % | 7.4 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Axen | treffer | FREE ALL DAY | 3 | 1 | 18.8 % | 3.1 | oben, zentriert | ja | Cartoon/Ink | ja |
| G1 | Banana Explains | schwach | BONE FLUTE? | 2 | 1 | 16.2 % | 12.3 | oben, zentriert | ja | Cartoon/Ink | ja |
| G1 | Banana Explains | treffer | WHERE DID YOU GO? | 4 | 1 | 9.4 % | 18.9 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Before Civilization | schwach | LEAVE HIM? | 2 | 1 | 22.1 % | 8.7 | oben links | ja | Cartoon/Ink | ja |
| G1 | Before Civilization | treffer | INSIDE THEM + '-40°' | 3 | 1 | 11.0 % | 9.1 | oben zentriert; '-40°' obe | ja | Cartoon/Ink | ja |
| G1 | Ink Explainer | schwach | THE IKEA EFFECT ? | 3 | 1 | 11.5 % | 21.0 | oben, zentriert | ja | Cartoon/Ink | ja |
| G1 | Ink Explainer | treffer | RAINED ALL WEEK | 3 | 1 | 18.1 % | 8.0 | oben, zentriert, volle Bre | ja | Cartoon/Ink | ja |
| G1 | Mogo | schwach | WHERE DO YOU GO? | 4 | 1 | 14.0 % | 11.1 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Mogo | treffer | WHY ONLY SOME? | 3 | 1 | 16.8 % | 11.9 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Noxenn | schwach | DREAMED WHAT? | 2 | 1 | 20.1 % | 9.3 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Noxenn | treffer | KIDS AT 12?! | 3 | 1 | 22.6 % | 10.8 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G1 | Prehistoria Hub | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | KI-Fotorealismus | ja |
| G1 | Prehistoria Hub | treffer | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | KI-Fotorealismus | ja |
| G1 | Prehistoric Archive | schwach | TERROR BIRDS / THE MOST TERRIFYING | 6 | 3 | 18.1 % | 15.1 | links, dreizeilig | ja | KI-Fotorealismus | ja |
| G1 | Prehistoric Archive | treffer | LIVING IN A CAVE / How Humans Surv | 11 | 2 | 13.9 % | 7.3 | oben, zentriert, zweizeili | ja | KI-Fotorealismus | ja |
| G2 | First Humans | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Fotografie/Museum | ja |
| G2 | First Humans | treffer | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Fotografie | ja |
| G2 | Folks of Yore | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | klassisches Gemaelde | ja |
| G2 | Folks of Yore | treffer | ROMAN LEISURE | 2 | 1 | 17.9 % | 5.8 | Bildmitte | ja | klassisches Gemaelde | ja |
| G2 | Historically | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Cartoon | ja |
| G2 | Historically | treffer | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Cartoon | ja |
| G2 | History Mapped Out | schwach | THE HISTORY OF / MONEY | 4 | 2 | 23.5 % | 6.5 | rechte Bildhaelfte, zweize | nein | Karte + Rendering | ja |
| G2 | History Mapped Out | treffer | RECONQUISTA / THE UNIFICATION + Ka | 5 | 2 | 12.1 % | 8.8 | oben links, zweizeilig; La | ja | Karte + Gemaeldeauss | ja |
| G2 | Professor Historian | schwach | DEADLIEST POISONS + 10 Objektlabel | 12 | 1 | 16.8 % | 5.7 | oben; Labels ueber das gan | nein | Cartoon/Ink auf Weis | nein |
| G2 | Professor Historian | treffer | WE STILL CAN'T REBUILD THESE | 5 | 1 | 10.0 % | 15.0 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G2 | quack doc | schwach | WHY YOU ARE / DEAD | 4 | 2 | 18.1 % | 17.7 | oben links schraeg + Mitte | ja | Cartoon/Ink auf Foto | ja |
| G2 | quack doc | treffer | Afterlife Theories | 2 | 2 | 20.6 % | 17.3 | unten rechts | ja | Cartoon/Ink | ja |
| G3 | Endless Origins | schwach | The Bubonic Plague | 3 | 1 | 20.0 % | 4.5 | Bildmitte | ja | KI-Fotorealismus | ja |
| G3 | Endless Origins | treffer | -30 °C | 2 | 1 | 20.0 % | 3.9 | oben rechts | ja | KI-Fotorealismus | ja |
| G3 | ExplainMatics | schwach | DESIGNED TO ADDICT + 10 Kachel-Bes | 23 | 1 | 7.5 % | 5.2 | oben; Labels in 10 Kacheln | nein | Infografik/Flat | nein |
| G3 | ExplainMatics | treffer | Before Medicine | 2 | 1 | 14.4 % | 5.9 | oben, zentriert | ja | Cartoon/Ink | ja |
| G3 | HUMAN-ISH | schwach | FISH DNA | 2 | 1 | 18.8 % | 6.8 | oben, zentriert | ja | Cartoon/Ink | ja |
| G3 | HUMAN-ISH | treffer | PREGNANT? | 1 | 1 | 17.2 % | 18.2 | oben, zentriert | ja | Cartoon/Ink | ja |
| G3 | Histor | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Archivfoto-Montage | ja |
| G3 | Histor | treffer | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | Archivfoto-Montage | ja |
| G3 | Million-Year Prehistory | schwach | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | KI-Fotorealismus | ja |
| G3 | Million-Year Prehistory | treffer | (kein Text) | 0 | 0 | n. e. | n. e. | — | ja | KI-Fotorealismus | ja |
| G3 | Sten Explains | schwach | WHO LOVED FIRST? | 3 | 1 | 17.4 % | 10.9 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G3 | Sten Explains | treffer | THEY FORCED US | 3 | 1 | 18.6 % | 6.7 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G3 | ThenFolk | schwach | THEY WATCH? | 2 | 1 | 18.5 % | 14.1 | oben, volle Breite | ja | Cartoon/Ink | ja |
| G3 | ThenFolk | treffer | RUN TO DEATH? | 3 | 1 | 20.0 % | 15.2 | oben, volle Breite | ja | Cartoon/Ink | ja |

## Die auffälligsten Kontraste

> **Beobachtungen, keine Regeln.** Was davon Ursache ist und was Begleiterscheinung,
> entscheidet die Ableitung — nicht dieses Dokument. Fallzahlen stehen in jeder
> Zeile; wo n klein ist, ist die Richtung belastbarer als die Größe.

### 1. G1 und G2 sind zwei verschiedene Formate, keine zwei Erfolgsstufen

Der schärfste Kontrast der ganzen Erhebung liegt nicht zwischen Gewinnern und
Verlierern, sondern zwischen den beiden **Gewinner**gruppen:

| Merkmal | G1 (jung) | G2 (etabliert) |
|---|---|---|
| Frageform im Titel | **76 %** (n = 293) | **7 %** (n = 376) |
| Titel endet mit „?" | 64 % | 1 % |
| Einstieg als Du-Versetzung | **12 von 16** | **0 von 12** |
| Zweite Person in Sekunde 0 | 11 von 16 | 0 von 12 |
| Kapitelmarken in der Beschreibung | 1 von 8 Kanälen | 4 von 6 Kanälen |
| Thumbnails ganz ohne Text | 2 von 16 | 5 von 12 |
| Uploads/Woche (Median) | 3,6 | 0,4 |
| Views je Video (Median) | 4.950 | 54.000 |

G2 erzählt dokumentarisch: Datum, Ort, Person, in Kapitel gegliedert, ohne
Anrede, oft mit textlosem Thumbnail. G1 stellt eine Frage und versetzt den
Zuschauer hinein — „You are 12 years old", „Imagine you haven't eaten in
2 days", „Picture this. You're lying on an operating table."

Beide Modelle verdienen fünfstellig. Das ist die wichtigste Einordnung für
alles Weitere: **in dieser Nische gibt es nicht einen richtigen Weg.**

### 2. Die Verlierer kopieren die Oberfläche der Gewinner

Genau die Merkmale, die G1 von G2 unterscheiden, zeigen die Verlierer **auch**:

| Merkmal | G1 | G3 |
|---|---|---|
| Frageform im Titel | 76 % (n = 293) | **56 %** (n = 191) |
| Titel endet mit „?" | 64 % | **49 %** |
| Einstieg als Du-Versetzung | 12 von 16 | **6 von 12** |
| Zweite Person in Sekunde 0 | 11 von 16 | **7 von 12** |
| Versalhöhe im Thumbnail (Median) | 16,5 % | **18,6 %** |
| Kontrast im Thumbnail (Spanne) | 3,1–21,0 : 1 | 3,9–18,2 : 1 |
| Thumbnails im Strichfiguren-Stil | 12 von 16 | 7 von 14 |
| Quellenangaben in der Beschreibung | 4 von 8 Kanälen | **3 von 7 Kanälen** |
| Videos ohne jeden CTA | 11 von 16 | 9 von 12 |

Der Feed-Test macht es sichtbar: Die Thumbnails von ThenFolk, HUMAN-ISH und
Sten Explains (alle G3) sind von denen von Mogo, Noxenn und Banana Explains
(alle G1) bei 160 × 90 px **nicht zu unterscheiden** — gelbe Versalien mit
schwarzer Kontur, oben über die volle Breite, Strichfigur darunter, Frageform.

**Kein einziges der hier gemessenen Oberflächenmerkmale trennt G1 von G3
sauber.** Zwei feine Unterschiede bleiben, beide zu klein für eine Regel:
G3-Titel sind etwas länger (9 gegen 8 Wörter im Median, 55 gegen 49 Zeichen)
und tragen doppelt so oft eine Zahl (22 % gegen 10 %).

### 3. Was tatsächlich trennt: der Median, nicht der Treffer

| Gruppe | Views/Video (Median) | höchstes Video | Spreizung Max/Median |
|---|---|---|---|
| G1 | 4.950 | 3,1 Mio. | 6–124× |
| G2 | 54.000 | 6,1 Mio. | 3–263× |
| G3 | **1.250** | 652.000 | **15–845×** |

Fünf der sieben G3-Kanäle haben einen sechsstelligen Treffer — ExplainMatics
652.000, HUMAN-ISH 408.000, Million-Year Prehistory 394.000, Endless Origins
360.000, ThenFolk 144.000. Ihre Mediane liegen bei 771, 997, 2.500, 1.250
und 499 Views.

**Ein Treffer beweist in dieser Nische nichts.** ExplainMatics hat mit 652.000 Views auf einem einzigen Video
mehr erreicht als jeder G1-Kanal außer Axen und Ink Explainer — und verdient
68 $/Monat [geschätzt].

### 4. Zwei Kontrollpaare, die zeigen, dass Titel und Thumbnail nicht reichen

Zwei G3-Kanäle liefern ungewöhnlich saubere Paare — dasselbe Format, dieselbe
Reihe, praktisch derselbe Titel:

| Kanal | Treffer | schwaches Video | Faktor |
|---|---|---|---|
| **Histor** | „These Photos Expose the RAW Reality of Our Ancestors. How Did They Even SURVIVE?!" — **57.702** | **wortgleicher Titel** — **368** | **157×** |
| **Million-Year Prehistory** | „…Homo Habilis Saves a Tiger Cub" (13:30) — **394.000** | „…Homo Habilis vs Giant Beasts — Full Survival Story" (58:55) — **716** | **550×** |

Bei Histor ist der Titel **identisch** und das Ergebnis unterscheidet sich um
Faktor 157. Bei Million-Year Prehistory unterscheidet sich vor allem die
Länge: 13 Minuten gegen eine 59-Minuten-Compilation.

Beide Paare sagen dasselbe: Was hier den Unterschied macht, steht nicht im
Titel und nicht im Thumbnail.

### 5. Quellenarbeit ist ein Merkmal des Jahrgangs, nicht des Erfolgs

4 von 8 G1-Kanälen führen echte Quellen — Ink Explainer mit 10 DOI-Links,
dazu Axen, Before Civilization, Noxenn. **0 von 6** G2-Kanälen tun das.

Und in G3 tun es **3 von 7**: ThenFolk zitiert Bramble & Lieberman (2004) aus
*Nature*, Wrangham und Harari — bei 499 Views im Median. Dazu ExplainMatics
und Sten Explains.

Das korrigiert einen Befund aus `recherche/nischen-kanal-2.md`: Quellenarbeit
ist dort als Alleinstellungsmerkmal von Ink Explainer beschrieben. Über die
größere Stichprobe ist sie ein Merkmal des **jungen Jahrgangs 2026** —
Gewinner wie Verlierer — und kein Erfolgsunterschied.

### 6. Epistemische Marker: der alte Befund hält nicht mehr

| Gruppe | Marker je 1.000 Wörter (Median) | n Videos |
|---|---|---|
| G1 | 1,1 | 16 |
| G2 | 1,6 | 12 |
| G3 | 1,2 | 12 |

Die Kalibrierprobe an Ink Explainers Treffer reproduziert die **3,7** aus der
bestehenden Auswertung exakt — die Wortliste misst dasselbe wie dort.

Innerhalb der Kanäle ist die Richtung aber uneinheitlich: Bei **11 von 20**
Paaren markiert das Treffer-Video häufiger Unsicherheit, bei **6** das
schwächere, **3** liegen gleich (alle drei bei 0,0 gegen 0,0). **Der Befund
aus `recherche/nischen-kanal-2.md` („innerhalb jedes Kanals ist das
Treffer-Video das vorsichtigere", dort n = 3 Paare) hält bei n = 20 nicht mehr
durchgehend.** Die dort formulierte sichere Lesart bleibt gültig: Die These
„glattes Behaupten gewinnt" wird von diesen Daten nicht gestützt — aber die
Gegenrichtung ist jetzt auch nicht mehr belegt.

### 7. Was nachweislich nicht trennt

Damit hier keine Zeit investiert wird:

| Geprüft | Ergebnis |
|---|---|
| **Versalhöhe im Thumbnail** | G1 16,5 % / G2 17,9 % / G3 **18,6 %** (Mediane) — die Verlierer setzen die **größte** Schrift |
| **Kontrast im Thumbnail** | überall 3,1–21,0 : 1, breit gestreut, kein Muster. Der niedrigste Wert der Erhebung (3,1 : 1) gehört Axens 3,1-Mio.-Treffer |
| **Sprechtempo** | G1 158 / G2 163 / G3 165 WPM (Mediane); Spanne 112–210 quer durch alle Gruppen |
| **Monetarisierung** | G1 8/8, G2 6/6, G3 **5/7** freigeschaltet — bei den fünf freigeschalteten G3-Kanälen fehlt der Umsatz **trotz** Freigabe. Bei HUMAN-ISH und Sten Explains widersprechen sich die beiden NexLev-Quellen (Suche „ja", Batch-Metrics „nein"); in den Tabellen steht der Batch-Wert, markiert mit `nein*` |
| **Untertitel** | kein einziger der 21 Kanäle liefert eigene Untertitel (`hasCaption` überall `false`); alle Transkripte stammen aus der YouTube-Spracherkennung |
| **CTAs** | 27 von 40 vermessenen Videos haben **gar keinen** CTA. Wo einer vorkommt, sitzt er in G2 fast immer am Schluss (98–100 % der Laufzeit), in G1 und G3 verstreut |
| **Quellenangaben** | siehe Punkt 5 — G1 4/8, G3 3/7 |

### 8. Zwei Beobachtungen zur Videolänge

Die G1-Kanäle zerfallen in zwei Längenklassen: **kurz** (Ink Explainer 8:24,
Axen 8:33 im Median) und **lang** (Banana Explains 23:35, Mogo 23:56,
Prehistoria Hub 32:03). Beide verdienen. Die kurzen sind zugleich die mit der
niedrigsten Kadenz — und **Ink Explainer, der Kanal mit dem höchsten Umsatz
der ganzen Erhebung (9.560 $/Monat [geschätzt]), fährt die niedrigste Kadenz
aller G1-Kanäle (0,74/Woche) bei den kürzesten Videos.** Er hat außerdem als
einziger Kanal überhaupt eine Spreizung von nur 6× — sein mittleres Video
erreicht 196.000 Views, fast das Vierzigfache des G1-Medians (4.950).

Die G3-Kanäle liegen im Median bei 9:51, mit dem auffälligsten Ausreißer der
Erhebung: Million-Year Prehistorys schwaches Video ist eine
**59-Minuten-Compilation** mit 716 Views.

### 9. Ein Kanal, der nicht ins Raster passt

**Histor** (G3) erfüllt die formalen Kriterien — jung, unter 200 $/Monat,
26 Long-Form-Videos —, ist aber kein Erklärkanal: Die Videos montieren
historische Archivfotos, die Thumbnails tragen keinen Text, das Format ist
Bilderstrecke statt Erklärung. Der Kanal bleibt in den Tabellen, weil er
sauber gemessen ist; für einen Vergleich mit Erklärformaten taugt er nur
eingeschränkt.

## Datenlücken und Vorbehalte

- **Alle $- und RPM-Angaben sind NexLev-Modellwerte [geschätzt]**, keine
  Auszahlungen. Suche und Batch-Metrics widersprechen sich teils deutlich
  (Ink Explainer 3,96 gegen 2,85 $ RPM). Beide Werte liegen in den Rohdaten.
- **Zwei Videos je Kanal sind eine kleine Stichprobe.** Die Skriptmessung
  vergleicht je Kanal ein Treffer- gegen ein schwaches Video. Thema, Alter und
  Länge sind dabei nicht kontrolliert — die Richtung eines Unterschieds ist
  belastbarer als seine Größe.
- **ASR-Transkripte enthalten Hörfehler** und keine Satzzeichen. Wortzahl und
  WPM sind dadurch leicht unscharf; die Marker-Heuristik zählt an Wortformen,
  nicht an Bedeutung. Ein „probably" in wörtlicher Rede zählt mit.
- **WPM misst gegen die Videolaufzeit**, nicht gegen die reine Sprechzeit.
  Kanäle mit langen Musik- oder Grafikpausen erscheinen dadurch langsamer, als
  sie sprechen.
- **Die Titelauszählung misst Wortformen, nicht Wirkung.** Dass ein Kanal
  Frageformen benutzt, sagt nichts darüber, ob die Frageform die Views
  verursacht hat.
- **Die Wortfrequenz Treffer gegen Flops ist auf Gruppenebene von einzelnen
  Kanälen dominiert.** Der stärkste G2-Wert („iceberg", +37,5 pp) stammt
  praktisch vollständig aus der Iceberg-Serie von quack doc — das ist ein
  Kanalformat, kein Gruppenmuster. Die Zeilen sind als Beobachtung an
  einzelnen Katalogen zu lesen.
- **Die Videoanzahl aus `youtube_channel_about` enthält Shorts.** Bei drei
  Kanälen klafft sie deshalb gegen die erfasste Long-Form-Liste: Historically
  (69 gegen 21 — der Videos-Tab meldet selbst „21"), History Mapped Out
  (149 gegen 134), Before Civilization (74 gegen 69). Die Kadenz „Uploads pro
  Woche über die Lebenszeit" ist deshalb aus den **erfassten Long-Form-Videos**
  gerechnet, nicht aus der `about`-Zahl.
- **Die beiden NexLev-Quellen widersprechen sich bei der Monetarisierung.**
  Für HUMAN-ISH und Sten Explains meldet `search_niche_finder_channels`
  `isMonetizationEnabled: true`, `get_batch_channel_metrics_v2` am selben Tag
  `isMonetized: false`. In den Tabellen steht der Batch-Wert, mit `nein*`
  markiert. Welcher stimmt, ist von außen nicht entscheidbar.
- **Views sind eine Momentaufnahme vom 2026-08-10.** Junge Videos hatten
  weniger Zeit; deshalb ist als „schwaches" Video nur zugelassen, was älter
  als 30 Tage ist.
- **Veröffentlichungsdaten in den Videolisten sind relativ** („3 months ago")
  und wurden umgerechnet; exakte Daten stehen nur für die beiden vermessenen
  Videos je Kanal aus `youtube_video_details` zur Verfügung.
- **Uploads/Woche in zwei Varianten**: über die gesamte Lebenszeit selbst
  gerechnet (Videoanzahl geteilt durch Kanalalter) und der NexLev-Katalogwert,
  der die jüngste Aktivität misst. Bei Professor Historian (gegr. 2007) klaffen
  sie weit auseinander (0,02 gegen 1,5) — der Kanal lief jahrelang leer und
  wurde später reaktiviert. Die Lebenszeit-Rate ist bei alten Kanälen
  irreführend.
- **Thumbnail-Textbereiche wurden von Hand am Gitternetz bestimmt.** Die
  Versalhöhe misst danach die Maschine; die Auswahl des Bereichs ist
  Handarbeit und bei mehrzeiligen oder verstreuten Textblöcken eine
  Ermessensentscheidung. Bei quack doc („WHY YOU ARE / **DEAD**") ließ sich die
  große rote Zeile nicht maschinell vom dunklen Grund trennen — sie ist
  deshalb **nicht** als Messwert geführt.
- **Kein Kanal wurde angesehen.** Schnitt, Tempo, Stimme, Musik und Bildstil
  sind hier nur so weit erfasst, wie Thumbnails und Transkripte sie verraten.
  Das ist Teil C.
- **Keine Klickraten.** Ohne Impressions und CTR aus fremden Analytics bleibt
  offen, ob Thumbnails oder Titel überhaupt der Engpass sind.

## Rohdaten

Alles in `regeln/daten/`, ein File je Erhebungsart:

| Datei | Inhalt |
|---|---|
| `kanal_gruppen.json` | Gruppenzuordnung, Auswahlkriterien, Katalogwerte je Kanal, Batch-Metrics, Abweichungen |
| `struktur.json` | Strukturmessung je Kanal inkl. Beschreibungsanalyse und Kapitelmarken |
| `skript.json` | Skriptmessung je Video, mit dem vollen Wortlaut der ersten 60 s |
| `titel.json` | Titelauszählung je Kanal, Treffer-/Flop-Drittel, Gruppenaggregate, Wortfrequenz |
| `thumbnails.json` | Thumbnail-Messwerte je Video |
| `videoliste.csv` | alle erfassten Long-Form-Videos mit Titel, Views, Länge |

**Nicht mitgeliefert:** die vollständigen Transkripte der 40 vermessenen
Videos (zusammen rund 2 MB). `skript.json` enthält je Video den Wortlaut der
ersten 60 Sekunden und alle daraus abgeleiteten Messwerte; die Volltexte sind
über `get_video_transcript` mit der `videoId` jederzeit kostenlos
nachzuziehen.

Die Messskripte liegen daneben und sind wiederholbar — wie
`recherche/daten/pruefe_fragen.py`:

| Skript | Misst |
|---|---|
| `struktur_metriken.py` | Kanalalter, Kadenz, Längen, Beschreibung, Quellenangaben |
| `skript_metriken.py` | Wortzahl, WPM, Einstiegstyp, CTAs, epistemische Marker, zweite Person |
| `titel_metriken.py` | Titelmuster, Treffer-/Flop-Drittel, Wortfrequenz |
| `thumb_werkzeuge.py` | Gitternetz, Versalhöhe, WCAG-Kontrast, Feed-Verkleinerung |

Aufruf der Thumbnail-Messung, wie sie für diese Tabelle benutzt wurde:

```
python3 thumb_werkzeuge.py raster   bild.jpg raster.png
python3 thumb_werkzeuge.py caphoehe bild.jpg 0.05 0.01 0.97 0.25
```

Die vier Zahlen sind der Textbereich als Anteil der Bildkanten
(links, oben, rechts, unten), am Gitternetz abgelesen.

## Nächste Schritte (nicht Teil dieses Auftrags)

1. **Regelableitung** aus diesen Zahlen — gemeinsam, wie beauftragt.
2. **Teil C**: Stilanalyse und Videosichtung. Kostet Credits, kommt als
   eigener Auftrag.
3. Offen geblieben und nachholbar ohne Kosten: Retention-Proxys, Kommentare,
   `youtube_channel_outliers` je Kanal für bewiesene Videoideen.
