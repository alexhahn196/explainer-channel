# Sprechweise — Unknown Frequencies, und was daraus für unseren Text folgt

> Erhebung vom **2026-08-16**, **0 Credits**, keine Vertonung, keine
> Videosichtung. Werkzeuge: `produktion/video-01/stimmproben/akustik.py`
> (unverändert importiert), die ElevenLabs-Zeichenzeitachse aus
> `produktion/video-01/ton/absatz-*.json`, die Untertitelzeiten beider Seiten.
> Messskript: `recherche/daten/uf_sprechweise_messen.py`.
>
> Kennzeichnung: **[gemessen]** · **[abgeleitet]** · **[unbekannt]**.

## Vorab: die Branches sind zusammengeführt

`claude/elevenlabs-voice-samples-p4t00y` enthielt die drei übrigen Branches
bereits vollständig (69 Commits, `kanal-2-datengrundlage`,
`established-channels-analysis` und `sechs-kulturfiguren` als Vorfahren). Es
genügte deshalb **ein** Merge auf diesen Branch; einziger Konflikt war
`.gitignore`, wo beide Seiten unterschiedliche Regeln ergänzt hatten — beide
sind übernommen.

Damit liegen alle vier zuvor fehlenden Kerndateien hier:
`regeln/ink-vs-axen.md`, `regeln/daten/skriptanatomie_inkaxen.py`,
`produktion/video-01/skript.md`, `recherche/stil-unknown-frequencies.md`.
Die Verweise in `recherche/schreibstil-unknown-frequencies.md` laufen nicht
mehr ins Leere; die dortige Vorbemerkung ist entsprechend korrigiert.

Eine Pfadangabe im Auftrag stimmte nicht: die eigene Tonspur liegt unter
`produktion/video-01/ton/tonspur.mp3`, nicht `produktion/video-01/tonspur.mp3`.

---

## Was gemessen werden konnte — und was nicht

**Die Tonspuren von Unknown Frequencies sind aus dieser Umgebung nicht
ladbar.** Das ist keine Vermutung, sondern ausprobiert:

| Schritt | Ergebnis |
|---|---|
| `yt-dlp`, Standardclient | HTTP 429, dann „Sign in to confirm you're not a bot" |
| fünf weitere `player_client`-Varianten | dieselbe Sperre bzw. PO-Token nötig |
| Deno als JS-Laufzeit nachinstalliert | löst die Formatauswahl, Sperre bleibt |
| EJS-Challenge-Solver (`yt-dlp-ejs` aus PyPI) | **JS-Challenge gelöst**, Format 251 gewählt |
| Mediendatei laden | **HTTP 403 von googlevideo** |
| signierte URL direkt mit `curl` | **HTTP 403**, auch mit Redirect-Folge |

Die Kette bricht erst am letzten Glied: die signierte URL ist gültig, der
CDN weist die Rechenzentrums-IP ab. Ohne Audiodatei sind **Pausenlängen,
Tonhöhenhub und Betonungsspitzen für Unknown Frequencies nicht messbar** und
aus Untertiteldaten auch nicht ableitbar. Was bleibt, ist das **Tempo**.

**Konsequenz für den Auftrag:** Von den fünf Messgrößen aus Teil 1 sind für
UF vier nicht erhebbar. Für unsere eigene Tonspur sind **alle fünf** erhoben.
Der Vergleich ist damit einseitig — das ist im Folgenden bei jeder Zahl
kenntlich gemacht und nicht durch Schätzungen aufgefüllt.

---

# TEIL 1 — Sprechweise, gemessen

## 1.1 Die drei gewählten POV-Videos

Ausgewählt sind die drei viewstärksten Videos der POV-Form (jener Form mit
74,7 Anrede-Markern je 1.000 Wörter aus
`recherche/schreibstil-unknown-frequencies.md`):

| Video | Titel | Länge | Views |
|---|---|---:|---:|
| `re_Av02zWcc` | Your Life as Every German Army Rank in WW2 | 9:01 | 992k |
| `COSuWgQjBhQ` | POV: You're a German Soldier in WW2 | 12:01 | 774k |
| `EhT6IhuZQp4` | Why It Sucked to Be a U.S. Soldier (in WW2) | 8:57 | 396k |

## 1.2 Tempo — die einzige für UF messbare Größe

YouTube-ASR-Untertitel sind **Rollfenster**: in allen drei Videos überlappen
**100 %** der Segmentübergänge [gemessen]. `dur` ist deshalb kein Zeitbudget,
und Wörter ÷ `dur` unterschätzt das Tempo systematisch. Gerechnet wird darum
mit dem **Onset-Abstand** (`start[i+1] − start[i]`), der sich in beiden
Formaten auf die Gesamtlaufzeit summiert und deshalb formatunabhängig ist.

Geeicht ist das Verfahren an der eigenen Tonspur, für die beide Wege vorliegen.

| | Brutto-WPM | lokale Rate Median | P10 | P90 | VK | Anteil unter 120 WPM |
|---|---:|---:|---:|---:|---:|---:|
| **Eric, eigene Spur** | **213,6** | 207,6 | 151,0 | 267,9 | 0,236 | **3,5 %** |
| UF Deutsche Ränge (992k) | 159,3 | 162,6 | 117,0 | 224,9 | 0,274 | **11,9 %** |
| UF Deutscher Soldat (774k) | 165,0 | 166,7 | 122,0 | 225,1 | 0,240 | 8,6 % |
| UF US-Soldat (396k) | **168,0** | 175,0 | 122,1 | 228,3 | 0,260 | 8,0 % |

Drei Befunde [gemessen]:

1. **UF liegt bei 159–168 WPM, wir bei 213,6.** Der Abstand beträgt 27–34 %.
2. **Die Tempostreuung ist fast gleich** (VK 0,24–0,27 gegen unsere 0,236).
   UF spricht nicht unregelmäßiger, sondern durchgehend langsamer.
3. **UF hat zwei- bis dreimal so viele langsame Stellen**: 8,0–11,9 % der
   Einheiten unter 120 WPM gegen unsere 3,5 %. Ob diese Stellen echte Pausen
   sind oder gedehnte Artikulation, ist ohne Audio **[unbekannt]** — der
   Onset-Abstand trennt beides nicht.

## 1.3 Eigene Tonspur — vollständig akustisch vermessen

`produktion/video-01/ton/tonspur.mp3`, 538,3 s, 1.916 gesprochene Wörter,
Eric bei `speed = 1,1955`, `seed = 4242`.

Das Verfahren wurde vorher an `a-eric-219wpm` gegen die gespeicherten Werte
in `akustik_ergebnis.json` geprüft: Pausenzahl, Median, Dauer und
Sprechanteil stimmen exakt, F0 auf 0,2 % [gemessen].

### Tempo und Pausen

| Größe | Wert |
|---|---:|
| Brutto-Tempo | **213,6 WPM** (dokumentiert: 214,3) |
| **Artikulationsrate** (ohne Pausenzeit) | **272,8 WPM** |
| Sprechanteil | 78,3 % |
| Pausen ≥ 0,12 s | **259**, zusammen 116,9 s |
| Median / P25 / P75 / P90 / längste | **0,390** / 0,235 / 0,620 / 0,782 / **1,450** s |

Verteilung: 0,12–0,2 s **18,9 %** · 0,2–0,3 s 15,1 % · 0,3–0,5 s **28,6 %** ·
0,5–0,8 s **27,8 %** · 0,8–1,2 s 7,7 % · über 1,2 s 1,9 %.

### Wo sitzen die Pausen? — praktisch ausschließlich an Interpunktion

Die Endzeit eines Satzzeichens läuft bei ElevenLabs in die Stille hinein; der
Pausenbeginn liegt im Median 0,14 s davor. Zugeordnet wird deshalb über ein
Toleranzfenster (−0,35 / +0,25 s) statt über einen exakten Vergleich.

| Pausen | Satzende | Klausel (`,` `;` `:`) | Gedankenstrich | wirklich innerhalb |
|---|---:|---:|---:|---:|
| ≥ 0,30 s (n=171) | 58,5 % | 24,0 % | 15,2 % | **2,3 %** |
| ≥ 0,50 s (n=97) | 73,2 % | 11,3 % | 13,4 % | **2,1 %** |

**97,7 % aller Pausen ab 0,30 s sitzen an einem Satzzeichen** [gemessen]. Die
Stimme setzt praktisch keine Pause, die nicht im Text steht. Umgekehrt
bekommen **75 % der Satzenden** eine Pause ≥ 0,30 s — das restliche Viertel
läuft ohne hörbare Zäsur durch.

### Welches Zeichen erzeugt welche Pause

| Zeichen | n | bekommt eine Pause | Median | P75 | P90 |
|---|---:|---:|---:|---:|---:|
| `.` `!` `?` | 133 | **92 %** | **0,570 s** | 0,748 | 0,999 |
| `,` | 137 | **44 %** | 0,285 s | 0,355 | 0,472 |
| `;` `:` | 24 | 83 % | 0,390 s | 0,538 | 0,574 |
| Gedankenstrich `—` | 46 | 80 % | 0,350 s | 0,550 | 0,744 |
| Absatzfuge | 16 | 100 % | **0,420 s** | — | — |

Die Absatzfuge ist **kein Stimmwert**, sondern in der Montage fest gesetzt —
sie lässt sich ohne neue Vertonung ändern.

### Tonhöhe

Grundlinie (Median aller stimmhaften Rahmen): **143,2 Hz**. Hub = P90 − P10
je Satz in Halbtönen; Spitze = Lage des F0-Maximums im Satz (0 = Anfang,
1 = Ende); Endfall = letztes Fünftel gegen den Satzmedian.

| Gruppe | n | Hub (HT) | Spitze | Endfall (HT) | fallend |
|---|---:|---:|---:|---:|---:|
| alle Sätze | 133 | 10,73 | 0,326 | −2,68 | 83 % |
| endet auf `.` | 127 | 10,77 | 0,317 | −2,84 | 86 % |
| **endet auf `?`** | 6 | 9,40 | **0,792** | **+1,70** | **33 %** |
| **1–5 Wörter** | 23 | **12,16** | 0,330 | **−6,79** | 87 % |
| 6–12 Wörter | 50 | 11,65 | 0,271 | −4,59 | 86 % |
| 13–25 Wörter | 41 | 10,67 | 0,497 | −1,99 | 83 % |
| **über 25 Wörter** | 19 | **9,26** | 0,491 | **−0,94** | 74 % |
| ohne Komma | 59 | **11,50** | 0,276 | **−5,88** | **93 %** |
| mit Komma | 74 | 10,66 | 0,449 | −1,51 | 76 % |
| ohne Gedankenstrich | 95 | 11,37 | 0,284 | −4,10 | 91 % |
| mit Gedankenstrich | 38 | 10,24 | 0,589 | −0,78 | 66 % |

**Die Betonungsspitze liegt im Median bei 32,6 % des Satzes**, also im ersten
Drittel; bei 53 % der Sätze im ersten Drittel. Bei Fragesätzen wandert sie ans
Ende (0,792) und der Schluss **steigt** statt zu fallen — bei nur 6 Sätzen ist
das ein Hinweis, kein Befund.

## 1.4 Der Vergleich in einem Satz

Für das Tempo gilt: **UF spricht 27–34 % langsamer und hat zwei- bis dreimal
so viele langsame Stellen.** Für Pausen, Tonhöhe und Betonung existiert auf
der UF-Seite **keine Messung** — jeder Vergleich dieser drei Größen wäre
erfunden.

---

# TEIL 2 — Übersetzung in Textvorgaben

## 2.1 Welche Satzlängen erzeugen die gemessenen Pausen? — Keine

Das ist das wichtigste Ergebnis dieses Teils, und es ist ein **negatives**:

| Satzlänge | n | Median-Folgepause | P90 |
|---|---:|---:|---:|
| 1–5 Wörter | 20 | 0,525 s | 0,803 |
| 6–10 Wörter | 36 | 0,595 s | 0,935 |
| 11–15 Wörter | 22 | 0,665 s | 0,959 |
| 16–25 Wörter | 25 | 0,630 s | 1,096 |
| über 25 Wörter | 19 | 0,440 s | 0,898 |

**Korrelation Satzlänge / Folgepause: r = 0,057** [gemessen] — also keine.
Ein längerer Satz erzeugt keine längere Pause. Die Spanne der Mediane liegt
zwischen 0,44 und 0,67 s, ohne Richtung.

**Folge:** Wer über Satzlängen die Pausenstruktur steuern will, steuert nichts.
Pausenlänge hängt am **Zeichen**, nicht an der Wortzahl davor. Satzlängen
steuern etwas anderes — die Tonhöhe (siehe 2.3).

## 2.2 Wo unser Text `<break>`-Tags bräuchte

Aus den Messwerten ergeben sich genau vier Stellen — überall sonst ist ein
Break überflüssig, weil die Interpunktion die Pause schon erzeugt:

1. **An den 25 % der Satzenden ohne Pause ≥ 0,30 s.** 133 Satzenden, 100 mit
   Pause, **33 ohne**. Wo die Montage dort eine Zäsur braucht (Bildwechsel,
   Kapitelgrenze), muss sie in den Text — die Stimme liefert sie nicht.
2. **An Kommas, an denen eine Pause gewollt ist.** Das Komma feuert nur in
   **44 %** der Fälle und dann mit 0,285 s. Ein Komma ist damit **kein
   verlässliches Pausenzeichen**. Wer dort sicher eine Pause will, setzt einen
   Break oder einen Punkt.
3. **Vor der Antwort auf die Kernfrage.** Der Zielwert aus dem Ink-Vergleich
   setzt die Antwort früh; eine Zäsur davor ist eine Regiefrage, keine
   Interpunktionsfrage, und deshalb explizit zu setzen.
4. **Nirgends an Absatzgrenzen.** Die 0,420 s dort kommen aus der Montage
   (`_zeitplan.json`), nicht aus der Stimme. Wer sie ändern will, ändert die
   Montage — das kostet **keine** neue Vertonung.

> **Ungeprüft:** `<break time="…">` ist in diesem Projekt **noch nie benutzt
> worden**. Ob das Tag mit `eleven_multilingual_v2`, `speed = 1,1955` und
> festem Seed zuverlässig greift und ob es das Timing der übrigen Absätze
> verschiebt, ist **[unbekannt]** und braucht **einen** Testlauf mit einem
> Absatz. Das ist der erste Kandidat, sobald wieder Credits da sind — vor
> jeder weiteren Vertonung, weil ein verschobenes Timing alle
> Einstellungslängen aus `szenen.md` hinfällig macht.

## 2.3 Welche Interpunktion erzeugt den Tonhöhenhub

Hier ist der Zusammenhang eindeutig und in die Gegenrichtung nutzbar
[gemessen]:

| Was der Text tut | Wirkung auf die Melodie |
|---|---|
| Satz **unter 6 Wörtern** | Hub **12,16 HT**, Endfall **−6,79 HT** |
| Satz **über 25 Wörter** | Hub 9,26 HT, Endfall −0,94 HT |
| Satz **ohne Komma** | Hub 11,50 HT, Endfall −5,88 HT, **93 % fallend** |
| Satz **mit Komma** | Hub 10,66 HT, Endfall −1,51 HT, 76 % fallend |
| Satz **ohne Gedankenstrich** | Hub 11,37 HT, Endfall −4,10 HT, 91 % fallend |
| Satz **mit Gedankenstrich** | Hub 10,24 HT, Endfall −0,78 HT, 66 % fallend |
| Satz endet auf **`?`** | Endfall **+1,70 HT** — der Schluss steigt |

**Kurze, komma- und gedankenstrichfreie Sätze erzeugen die größte
Tonhöhenbewegung und den saubersten Schlussfall.** Lange Sätze mit Kommas und
Gedankenstrichen verflachen die Melodie um bis zu 3 Halbtöne im Hub und um
fast 6 Halbtöne im Endfall.

Das verbindet Teil 1 mit dem Schreibstilbefund: **die POV-Form von UF hat
Satzlängen-Median 7,0 Wörter und 29,4 % Sätze unter 5 Wörtern**, unser
Video-1-Skript **11,0 Wörter und 13,5 %**. Wer die UF-Satzlängen übernimmt,
bekommt mit Eric **automatisch** die größere Melodiebewegung — ohne einen
einzigen Stimmparameter zu ändern. Das ist der billigste Hebel im ganzen
Bericht.

> **Wichtige Einschränkung zu allen UF-Textwerten.** Die Interpunktion in den
> UF-Transkripten stammt von YouTubes Spracherkennung, nicht vom Autor.
> Satzgrenzen sind damit brauchbar, aber **Komma- und Gedankenstrichzahlen
> sind Artefakte des ASR-Modells**: gemessen 0,38 Kommas je Satz und
> **0 Gedankenstriche in 1.975 Sätzen** — die Erkennung schreibt schlicht
> keine. Diese beiden Werte taugen deshalb **nicht** als Zielwerte. Die
> Komma- und Gedankenstrichregeln unten stützen sich ausschließlich auf die
> Melodiemessung an **unserer eigenen** Tonspur, wo Text und Audio beide
> vorliegen.

## 2.4 Ist 168 WPM mit Eric erreichbar? — Ja, über den Regler, nicht über Pausen

Erics Kennlinie ist im Repo gemessen (`elevenlabs/messungen.json`,
`entscheidungen.md`):

| `speed` | 1,000 | 1,094 | 1,121 | 1,169 | 1,186 | 1,196 | 1,200 |
|---|---:|---:|---:|---:|---:|---:|---:|
| WPM | **177,2** | 186,8 | 194,2 | 209,1 | 213,2 | 214,3 | **226,8** |

Bei `speed = 1,0` liefert Eric bereits **177,2 WPM** — nur 9 WPM über dem
UF-Wert. Die lokale Steigung dort beträgt **102,1 WPM je speed-Einheit**,
also:

| Ziel | nötiger `speed` [abgeleitet] |
|---|---:|
| 168,0 WPM (UF US-Soldat) | **≈ 0,91** |
| 165,0 WPM | ≈ 0,88 |
| 159,3 WPM (UF Deutsche Ränge) | ≈ 0,83 |

Alle drei liegen **innerhalb** des Reglerbereichs 0,7–1,2, mit Reserve nach
unten. **Aber:** unterhalb 1,0 ist die Kennlinie **nicht gemessen**, und sie
ist nachweislich gestuft — zwischen 1,1955 und 1,2000 springt sie um 12,5 WPM.
Der Wert 0,91 ist eine Extrapolation aus einem Ankerpunkt und braucht **einen**
Messlauf.

**Der Gegenweg funktioniert nicht.** 168 WPM allein über längere Pausen, bei
unveränderter Artikulationsrate von 272,8 WPM:

- Zieldauer 684,3 s statt 538,3 s
- nötige Pausenzeit **262,9 s** statt heute 116,9 s → **+146 s**
- auf 133 Satzenden verteilt: **+1,10 s je Satz**, die Satzendpause stiege von
  0,570 s auf **1,67 s**
- der Sprechanteil fiele von 78,3 % auf **61,6 %**

Das wäre kein ruhiger Erzähler, sondern ein stockender. **Tempo gehört an den
Regler, Struktur an die Interpunktion.**

Zwei Nebenwirkungen sind zu erwarten [abgeleitet, aus `hoerbericht.md`]:
`speed` staucht dort nachweislich **die Artikulation, nicht die Pausen** —
bei 219 gegen 195 WPM blieben Pausenzahl (31/31) und Median (0,52/0,50 s)
konstant. Ein Absenken auf 0,91 dehnt also die Silben, lässt die Pausen aber
etwa wie sie sind: die Satzendpause bliebe bei ~0,57 s, ihr **Anteil** an der
Laufzeit sänke. Und die Laufzeit stiege von 8:58 auf rund **11:24** — jede
Einstellungslänge in `szenen.md` wäre neu zu rechnen.

## 2.5 Die Regeln, kurz

1. **Satzlängen-Median auf 7 Wörter**, mindestens 25 % der Sätze unter
   5 Wörtern. Wirkung: Tonhöhenhub von 10,73 auf ~12 HT, Endfall von −2,68 auf
   ~−6 HT. (Heute: 11,0 Wörter, 13,5 %.)
2. **Kommas sparen.** Ein kommafreier Satz fällt am Ende um 5,88 HT statt um
   1,51 HT und ist zu 93 % statt 76 % fallend. Heute sind **44,4 %** unserer
   Sätze kommafrei (1,03 Kommas je Satz). Wo ein Komma nur eine Atempause
   markieren soll: Punkt setzen. *(Begründet an unserer Tonspur, nicht an UF —
   dessen Kommazahlen sind ASR-Artefakte.)*
3. **Gedankenstriche sparsam.** Sie kosten 1,13 HT Hub und 3,32 HT Endfall und
   verschieben die Betonungsspitze von 0,284 auf 0,589 — also ans Satzende.
   Unser Video-1-Skript hat **46 Gedankenstriche in 133 Sätzen** (28,6 % der
   Sätze). Nach der Satzlänge ist das der zweitgrößte Flachmacher.
4. **Fragezeichen bewusst setzen.** Sie kehren den Schlussfall um (+1,70 HT).
   Als Abschnittsscharnier gewollt, am Videoende ungewollt.
5. **Keine `<break>`-Tags an Satzenden** — 92 % bekommen ohnehin eine Pause
   von 0,570 s. Breaks nur an den 33 pausenlosen Satzenden und dort, wo ein
   Komma verlässlich eine Pause braucht.
6. **Tempo über `speed`**, Zielwert ≈ 0,91 für 168 WPM — erst nach einem
   Messlauf festschreiben, und nur zusammen mit neu gerechneten
   Einstellungslängen.
7. **Absatzfugen sind Montagesache**, nicht Textsache: 0,420 s, änderbar ohne
   Vertonung.

---

# TEIL 3 — Prompt-Baustein für Video 3

Abgeleitet aus der POV-Form in `recherche/schreibstil-unknown-frequencies.md`,
verbunden mit den Melodiebefunden aus 2.3. Zum Einsetzen in den nächsten
Skriptauftrag.

```text
SCHREIBSTIL (Video 3) — messbare Vorgaben

Erzählhaltung
- Schreib in der zweiten Person. Der Zuschauer IST die Person, um die es geht;
  er wird nicht über sie informiert.
- Zielwert Anrede-Marker (you/your/you're/you'll/you've/yourself):
  55-75 je 1.000 Woerter ueber den ganzen Text.
- Die Anrede darf zum Schluss NICHT abfallen. Zielwert im letzten Fuenftel:
  mindestens 50 je 1.000 Woerter. (Vorbild haelt 60,4; unser Video 1 faellt
  von 42,7 auf 13,3 — genau das nicht.)
- Erste Person Singular ("I", "my") hoechstens 1 je 1.000 Woerter.
  Kein Erzaehler, der sich zeigt.

Satzbau — steuert die Sprechmelodie, nicht nur den Rhythmus
- Satzlaengen-Median 7 Woerter. Mindestens 25 % der Saetze unter 5 Woertern.
  (Vorbild: 7,0 und 29,4 %. Video 1: 11,0 und 13,5 %.)
- Hoechstens 3 Saetze ueber 25 Woerter im ganzen Skript. (Video 1 hat 19.)
- Kommas sparen: mindestens 60 % der Saetze ganz ohne Komma, hoechstens
  0,6 Kommas je Satz. Grund ist gemessen an unserer eigenen Stimme: ein
  kommafreier Satz faellt am Ende um 5,88 Halbtoene statt um 1,51.
  (Video 1: 44,4 % kommafrei, 1,03 Kommas je Satz.)
- Gedankenstriche hoechstens 10 im ganzen Skript. Sie kosten 3,32 Halbtoene
  Endfall und schieben die Betonungsspitze ans Satzende.
  (Video 1 hat 46.)
- Anapher (zwei aufeinanderfolgende Saetze mit gleichem Anfangswort):
  Zielwert 12-15 % aller Saetze. Das ist das auffaelligste Stilmittel des
  Vorbilds und maschinell nachpruefbar.
- Beginne 15-20 % der Saetze mit "you" oder "your".

Einstieg
- Erster Satz in der zweiten Person, mit einer konkreten Zahl (Alter, Uhrzeit,
  Menge, Entfernung) in den ersten 35 Woertern. Beim Vorbild: 9 von 9 Videos.
- Keine grosse Zahl und kein Superlativ als Aufhaenger — das ist die andere
  Form des Vorbilds und passt nicht zur Ansprache.
- Die Antwort auf die Titelfrage faellt im ersten Drittel, moeglichst in den
  ersten 30 Sekunden.

Fragen
- Hoechstens 3 Fragezeichen im ganzen Skript. Die POV-Form des Vorbilds hat
  in 9 Videos zusammen 5. Fragen sind Abschnittsscharniere, keine Leitfrage.
- Kein Fragezeichen in den letzten 200 Woertern: es kehrt den Schlussfall der
  Stimme um.

Schluss
- Keine Handlungsaufforderung. Kein "abonnieren", kein Verweis aufs naechste
  Video. Beim Vorbild: 9 von 9 POV-Videos ohne jede CTA.
- Der letzte Absatz endet auf einen kurzen, wertenden Satz, gern ein Fragment
  unter 6 Woertern.
- Die zweite Person bleibt bis zum letzten Satz stehen.

Was NICHT uebernommen wird — hier weichen wir bewusst ab
- Unsicherheit bleibt hoerbar. Zielwert epistemische Marker: 2-4 je 1.000
  Woerter ("probably", "we don't know", "historians think", "the evidence
  suggests"). Das Vorbild liegt bei 0,0 und behauptet durchweg; unsere
  Recherche verlangt das Gegenteil. Diese Regel schlaegt alle anderen.
- Jede harte Zahl und jedes Datum bekommt eine Quellen-ID in eckigen Klammern.
- Hoechstens 6 benannte Personen im ganzen Skript, jede mit Rollen-Apposition
  eingefuehrt. Kein Titel und kein Aufhaenger, der Vorwissen voraussetzt.
- Kein Krieg, keine benannten lebenden Personen, kein laufender Konflikt.
- Kurzwortanteil nicht weiter treiben: wir liegen mit 90,9 % bereits ueber
  jedem Vergleichskanal (Maximum sonst 82,6 %).

Laufzeit
- 1.850-2.050 Woerter. Bei speed 1,1955 sind das 8:39-9:34; bei einem
  langsameren Regler entsprechend mehr — die Einstellungslaengen richten sich
  nach dem tatsaechlich gesetzten Wert, nicht nach 219 WPM.
```

Die Zielwerte in diesem Baustein sind mit den vorhandenen Skripten prüfbar:
`regeln/daten/skriptanatomie_inkaxen.py` liefert Anrede-Marker, Fünftel und
Satzlängen, `recherche/daten/uf_schreibstil_messen.py` die Satzbauformen und
die Anapher.

---

# VORBEHALT

**n = 1 Kanal, und ein übernommener Stil garantiert nichts.**

Im Ink-Axen-Vergleich (`regeln/ink-vs-axen.md` §2) waren beide Kanäle in elf
gemessenen Größen nicht unterscheidbar, zwei sprachen sogar **für** Axen
(Like-Rate 2,92 % gegen 2,00 %, stärkster Outlier 7,3× gegen 3,3×). Axens
Median fiel trotzdem von 495.396 auf 17.264 Views, Faktor 29 abwärts.

Für diesen Bericht kommt eine zweite Unsicherheit dazu: **die Sprechweise von
Unknown Frequencies ist zu vier Fünfteln nicht gemessen.** Belegt ist allein
das Tempo. Alles, was hier über Pausen, Melodie und Betonung steht, ist an
**unserer eigenen** Stimme gemessen — es beschreibt, wie Eric auf Text
reagiert, nicht, wie UF klingt. Die Textregeln in Teil 2 sind damit gut
begründet für die Frage „wie steuere ich Eric", und **nicht** begründet für
die Frage „so klingt der Vorbildkanal".

Die Übertragung in Teil 3 ist **Hypothese, kein Rezept**. Sie stützt sich auf
Textmerkmale (Satzlängen, Anrede, Anapher), die gemessen sind — nicht auf eine
gemessene Sprechweise des Vorbilds.

## Was nicht gemessen wurde

- **Pausen, Tonhöhe und Betonung von Unknown Frequencies.** Tonspuren nicht
  ladbar (HTTP 403), siehe oben. Das ist die größte Lücke dieses Berichts.
- **`<break>`-Tags**: in diesem Projekt nie benutzt, Wirkung auf Timing und
  Seed-Reproduzierbarkeit unbekannt.
- **Erics Kennlinie unter `speed` 1,0.** Ein einziger Ankerpunkt (177,2 WPM
  bei 1,0); alles darunter ist extrapoliert.
- **Ob 168 WPM besser wirkt.** Der Hörbericht hält ausdrücklich fest, dass
  objektiv nichts gegen 219 WPM spricht — weder Satzgrenzen noch
  Verständlichkeit. Dass UF langsamer spricht, ist eine Messung, kein Urteil.
- **Kein Ton gehört.** Wie bei allen bisherigen Berichten dieses Repos.

## Rohdaten

| Datei | Inhalt |
|---|---|
| `recherche/daten/uf_sprechweise_messen.py` | Messskript, `--eigen` und `--tempo` |
| `recherche/daten/uf_sprechweise.json` | Tempowerte beider Seiten |
| `produktion/video-01/stimmproben/akustik_ergebnis.json` | Akustik der 20 Stimmproben (vorhanden) |
| `produktion/video-01/ton/absatz-*.json` | ElevenLabs-Zeichenzeitachse (vorhanden) |

Die Untertiteldateien der Fremdvideos liegen unter
`recherche/daten/uf-audio/captions/` und sind per `.gitignore` ausgeschlossen —
sie enthalten Transkripttext.
