# Auslieferung NEU — Video 2, neu montiert mit korrigierter Kamerafahrt

> **Stand 2026-08-17.** Dieselben 159 Einstellungen, derselbe Schnittplan,
> dieselbe Tonspur. **Geändert ist ausschließlich, wie die Kamerafahrten
> gerechnet werden.**
>
> Zusammensetzen: `sh zusammensetzen.sh` — prüft dabei die Prüfsumme.
> Die alte Fassung bleibt unangetastet in [`../auslieferung/`](../auslieferung/).
>
> **Nichts wurde zu YouTube hochgeladen.**

## Die Dateien

| Video | Teile | Summe | MD5 |
|---|---|---|---|
| `video-02.mp4` | `video-02.mp4.00.part` … `.03.part` | 102.180.394 B = 97,4 MB | `c2bcdc13ff1f960a3ebe07a63f783ef7` |

Erzeugt mit `split -n 4 -d --additional-suffix=.part`, wie in
`../auslieferung/`.

## Laufzeit und Verankerung — unverändert, exakt

Das war die Bedingung, und sie ist nicht ungefähr, sondern **auf den Frame
genau** erfüllt. Gemessen an beiden Dateien:

| | alt (`../auslieferung/`) | neu (hier) |
|---|---|---|
| Frames | **18 487** | **18 487** |
| Laufzeit | **616,233333 s** = 10:16,2 | **616,233333 s** = 10:16,2 |
| Format | 1920×1080, 30 fps, H.264 | 1920×1080, 30 fps, H.264 |
| Dateigröße | 151.231.124 B = 144,2 MB | 102.180.394 B = 97,4 MB |

Gleiche Framezahl heißt: **jeder Schnitt fällt auf denselben Frame wie
vorher.** Die Verankerung am gesprochenen Wort ist damit bitgenau
übernommen, nicht nachgerechnet. Zusätzlich geprüft mit
[`../video-02/pruefe_verankerung.py`](../video-02/pruefe_verankerung.py):
159 von 159 Einstellungen haben exakt die geforderte Framezahl.

**Die Datei ist 32 % kleiner.** Kein Qualitätsverlust — dieselbe Kodierung
(CRF 18, `veryfast`), aber 97 statt 54 Einstellungen stehen still, und ein
unbewegtes Bild kostet fast keine Bitrate.

## Was sich geändert hat

### 1. Der Fahrtweg

Gerechnet wird jetzt über
[`produktion/pipeline/kamerafahrt.py`](../pipeline/kamerafahrt.py) statt
über eine eigene Filterkette in `montage.py`.

Die alte Kette brachte das Bild vor `zoompan` auf 3840 px — der richtige
Gedanke, aber zu knapp: `zoompan` rastet den Ausschnitt auf ganze
**Quell**pixel, und bei 3840 px Eingang ist ein Quellpixel immer noch ein
**halber** Ausgabepixel. Der Standardweg tastet vierfach über (7680),
rechnet `zoompan` auf 3840 und reduziert erst danach mit lanczos auf 1920.

Gemessen an den drei längsten Einstellungen, die eine echte Fahrt behalten
haben — Ruckeln ist die Streuung des Bildversatzes um seinen eigenen
glatten Verlauf, die Fahrt selbst ist herausgerechnet:

| Einstellung | Fahrt | Dauer | alt | neu | |
|---|---|---|---|---|---|
| 63 | Zoom rein | 8,95 s | 0,503 px | **0,030 px** | 16,7× ruhiger |
| 104 | Zoom raus | 7,82 s | 0,533 px | **0,033 px** | 16,3× ruhiger |
| 76 | Zoom raus | 7,59 s | 0,492 px | **0,026 px** | 18,7× ruhiger |

Die gemessenen ~0,5 px der alten Fassung sind genau der vorausgesagte halbe
Quellpixel. Die Ursachenanalyse trifft also auch auf diesen Code zu, nicht
nur auf den aus BibelTube übernommenen.

### 2. Statisch bei Figuren

Zeigt ein Motiv einen Menschen — ganz, als Kopf oder als Hand bei der
Arbeit —, läuft die Einstellung ohne Bewegung. **23 der 66 Motive** fallen
darunter, dadurch werden **43 Einstellungen** von Fahrt auf statisch
umgestellt:

| | vorher | nachher |
|---|---|---|
| statisch | 54 | **97** |
| Zoom rein | 61 | 35 |
| Zoom raus | 33 | 20 |
| Schwenk rechts | 8 | 6 |
| Schwenk links | 3 | 1 |

Es bleiben **62 Einstellungen mit echter Fahrt = 43,8 % der Laufzeit.**

Welches Motiv eine Figur zeigt, steht in keiner von Hand gepflegten Liste,
sondern wird aus dem `FRAMING`-Absatz von
[`../video-02/bildplan2-prompts.json`](../video-02/bildplan2-prompts.json)
gelesen — derselben Quelle, aus der die Bilder erzeugt wurden. Die vier
Formulierungen, die zählen: `a single person`, `several people`,
`one head only`, `one part of a body only`.

Dass auch die Hand-und-Fuß-Nahaufnahmen dazugehören, ist eine Entscheidung
und keine Zwangsläufigkeit: `M04` etwa ist ein Daumen mit Unterarm,
formatfüllend, mit harten Konturen — für die Frage, wo eine Fahrt stört,
zählt das wie eine Figur. Ohne diese zehn Motive wären es 38 statt 58
betroffene Einstellungen.

### 3. Zwei kleinere Korrekturen, beide beabsichtigt

- **Die Rampe läuft als Kosinus statt linear.** Die Fahrt ist damit am
  Schnitt am langsamsten und setzt weich an, statt hart loszulaufen. Bei
  3–4 s Einstellungslänge ist das der Punkt, an dem eine Fahrt sonst
  „anspringt".
- **Der 16:9-Zuschnitt geschieht vor der Fahrt.** Die alte Kette skalierte
  2752×1536 (Seitenverhältnis 1,792) auf 3840×2143 und ließ `zoompan`
  daraus 16:9 machen — das **quetschte das Bild um 0,8 % in der Breite**.
  Jetzt wird beschnitten statt gequetscht. Der Unterschied ist klein, aber
  er war eine Verzerrung und ist jetzt keine mehr.

## Was NICHT geändert wurde

- `schnittplan.json` — unangetastet. Die Figurenregel schreibt ihr Ergebnis
  in ein Feld `fahrt_neu` zur Laufzeit, nicht in den Plan.
- Die Tonspur, die 66 Bilder, die Ausspracheliste.
- Die Kodierung: H.264, CRF 18, `veryfast`, AAC 192 kb/s.
- `ABSPANN_S = 1.4` — **weiterhin der ungemessene Platzhalter aus Video 1.**
  Er war es vorher auch; die Neumontage ändert daran nichts und behebt es
  nicht. Für Video 2 gehört er an der eigenen Tonspur nachgemessen.

## Nachvollziehen

```sh
python3 produktion/video-02/montage.py              # neu montieren, ~10 min
python3 produktion/video-02/pruefe_verankerung.py   # Laufzeit und Anker
python3 produktion/pipeline/kamerafahrt.py <bild> --selbsttest
```
