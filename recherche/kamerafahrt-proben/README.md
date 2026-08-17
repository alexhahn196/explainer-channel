# Kamerafahrten: Zittern — Ursache, drei Probeclips, Entscheidung offen

**Stand 2026-08-17.** Drei 6-Sekunden-Clips aus **einem** vorhandenen Bild,
0 Credits, kein neues Material. Sie liegen hier, damit die Kamerafahrt für
alle künftigen Videos **einmal** entschieden wird.

> ⬜ **ENTSCHEIDUNG OFFEN.** Bis sie fällt, wird an `schritt5_video.py` und
> `produktion/config.md` nichts geändert. Wer hier vorbeikommt, bevor
> entschieden ist: **die Kamerafahrt in `schritt5_video.py` ist defekt** —
> Begründung unten. Nicht ungeprüft für dieses Format übernehmen.

| Clip | Datei | Was er zeigt |
|---|---|---|
| **(a)** | [`probe-a-bisher.mp4`](probe-a-bisher.mp4) | der bisherige Weg — Vergleichspunkt |
| **(b)** | [`probe-b-korrigiert.mp4`](probe-b-korrigiert.mp4) | die Korrektur |
| **(c)** | [`probe-c-statisch.mp4`](probe-c-statisch.mp4) | ganz ohne Bewegung |

Alle drei: 1920×1080, 24 fps, **exakt 6,000 s / 144 Frames**, dieselbe Quelle
([`stil-1-flatvector-szeneA.png`](../stile-erklaerkanal/stil-1-flatvector-szeneA.png)),
dieselbe Fahrt (Zoom 1,00 → 1,08 mit Schwenk, Kosinus-Rampe), dieselbe
Kodierung. **Der einzige Unterschied ist der Weg, auf dem die Fahrt
entsteht.** Je 1,7–1,9 MB, kein Aufteilen in Teile nötig — die Grenze bei
GitHub liegt bei 100 MB je Datei.

Das Motiv ist absichtlich flacher Vektorstil mit harten Konturen: dünne
Tischbeine, Fensterrahmen, Regalkanten. Genau die Bildwelt, in der das
Problem auffällt.

---

## Schritt 1 — die Ursache

Die Fahrt entsteht in
[`produktion/pipeline/schritt5_video.py:37`](../../produktion/pipeline/schritt5_video.py)
(`zyklus_bauen`), Kern ist Zeile 45:

```python
vf = (f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
      f":d=1:s={cfg['breite']}x{cfg['hoehe']}:fps={fps},format=yuv420p")
```

Maßgeblich ist, was `vf_zoompan.c` daraus je Frame macht:

```c
w = in->width  * (1.0 / zoom);      /* int — abgeschnitten */
h = in->height * (1.0 / zoom);      /* int — abgeschnitten */
x = av_clipd(dx, 0, in->width - w); /* int — abgeschnitten */
```

**Der Ausschnitt rastet auf ganze Quellpixel ein — Größe *und* Lage.** Die
Zoomstufe ist eine Fließkommazahl, der Ausschnitt, den sie beschreibt, ist es
nicht. Die Fahrt bewegt sich also nicht kontinuierlich, sondern steht still
und springt dann um einen ganzen Quellpixel weiter.

Von den vier bekannten Kandidaten treffen **drei zu, und sie verstärken
einander:**

| Kandidat | Befund |
|---|---|
| **Rundung der Zoomstufe je Frame** | ✅ **Hauptursache.** Ausschnittsbreite und ‑lage sind `int`. Nicht die Zoomrate ist schuld, sondern dass `zoompan` sie auf ganze Quellpixel rundet. |
| **Hochskalierung statt Herunterskalierung** | ✅ **Verstärker, und hausgemacht.** [`schritt4_bild.py:40`](../../produktion/pipeline/schritt4_bild.py) (`zuschneiden`) skaliert **jede** Quelle vorab per LANCZOS auf `breite`×`hoehe` = 1920×1080 und speichert erst dann. Unsere Quellen sind **2752×1536**. Die Reserve ist weg, bevor die Fahrt beginnt — `zoompan` schneidet danach aus 1920 px einen 1778‑px‑Ausschnitt und **zieht ihn wieder auf 1920 hoch**. Ein Quellpixel = ein Ausgabepixel, also rastet die Fahrt auf volle Bildpixel. |
| **zu kleiner Zoombereich über zu viele Frames** | ✅ **Im Originalfall katastrophal.** `zoom_faktor 1.04` über `zoom_zyklus_s 300` bei 24 fps = 7200 Frames auf 74 Rasterstufen → **99,0 % der Frames sind exakte Standbilder**, dazwischen ein Sprung von 1,04 px. Für dieses Format ist der 300‑s‑Zyklus ohnehin gegenstandslos (steht so in `config.md`), aber derselbe Code auf 6 s angewandt zittert weiter. |
| **fehlende/schwache Interpolation** | ⚠️ **Vorhanden, aber nicht die Ursache — und in `zoompan` nicht abstellbar.** `ffmpeg -h filter=zoompan` kennt genau sieben Optionen: `zoom/z, x, y, d, s, fps`. **Keine Flags-Option.** Der interne Skalierer ist auf `SWS_BICUBIC` festgenagelt. Bessere Interpolation ist nur *um* `zoompan` herum zu haben, nicht darin. |

### Warum das gerade bei flachen Grafiken auffällt

Ein Sprung um einen Pixel ist immer da. Sichtbar wird er an der Kante: eine
harte Kontur zwischen zwei einfarbigen Flächen springt als **ganze Kante**
sichtbar um eine Pixelspalte. In einem fotografischen Bild mit Textur und
Rauschen verschwindet derselbe Sprung im Detail. Unsere Bildwelt ist der
ungünstigste Fall.

### Nachgerechnet

`quantisierung.py` simuliert die drei `int`-Zeilen oben Frame für Frame.
„Zittern" = wie weit die gerastete Lage von der ideal glatten Bahn abweicht,
in **Ausgabepixeln** — die Fahrt selbst ist herausgerechnet, übrig bleibt der
Sägezahn der Rundung.

| Weg | Quellpixel in Ausgabepixeln | Frames ohne jede Änderung | Zittern Lage | Zittern Skala |
|---|---|---|---|---|
| **Original BibelTube** (1920 px, 1,04 / 300 s) | 1,000 | **99,0 %** | 1,04 px | 0,52 px |
| **derselbe Code auf 6 s** (1920 px) | 1,000 | 18,2 % | 1,34 px | 0,51 px |
| 2752 px nativ, `zoompan` direkt auf 1920 | 0,703 | 11,9 % | 0,95 px | 0,38 px |
| **3× überabgetastet** (5760 px) | 0,333 | 6,3 % | 0,46 px | 0,17 px |
| **4× überabgetastet** (7680 px) | 0,250 | 4,9 % | **0,35 px** | **0,13 px** |

**Faustregel, die daraus folgt:** Das Zittern verschwindet, wenn eine
Rasterstufe unter ~0,3 Ausgabepixel bleibt. Das heißt: **die Quelle muss
mindestens dreimal so breit sein wie die Ausgabe** — und sie darf vorher
nicht kleingerechnet werden.

---

## Schritt 2 — die drei Clips, gemessen

Nicht am Filtergraphen, sondern **am dekodierten Bild** der fertigen MP4s,
also an dem, was der Zuschauer sieht (`messen.py`). „Ruckeln" ist die
Streuung des Bildversatzes um seinen eigenen glatten Verlauf — wieder ist
die beabsichtigte Fahrt herausgerechnet.

| | (a) bisher | (b) korrigiert | (c) statisch |
|---|---|---|---|
| **Ruckeln** | **0,998 px** | **0,148 px** | **0,000 px** |
| eingefrorene Frames | 19 von 143 (13,3 %) | 3 von 143 (2,1 %) | — (statisch) |
| Bewegung \|Δ\| Median | 0,979 | 0,506 | 0,000 |
| Kantenschärfe Frame 0 | 0,827 | 0,807 | **0,964** |
| Kantenschärfe Frame 143 | 0,853 | **0,917** | **0,967** |
| Rechenzeit für 6 s (4 Kerne) | 16 s | 44 s | 8 s |
| Dateigröße | 1,95 MB | 1,72 MB | 1,80 MB |

Die gemessenen **0,998 px** in (a) sind genau der vorausgesagte eine
Quellpixel. Ursachenanalyse und Messung stimmen überein.

### Die Kantenspur

![Kantenspur](kantenspur.png)

Dieselbe Bildzeile aus allen 144 Frames, untereinandergelegt — **Zeit läuft
nach unten**, Kontrast gespreizt. Links die Treppe, in der Mitte eine glatte
Kurve mit weichem Übergang, rechts die Senkrechte. Das ist kein Diagramm,
sondern sind die Pixel selbst.

### Was (b) genau macht

```
Quelle 2752×1536
  → EINMAL scale=7680:4320:flags=lanczos          (4× Ausgabebreite)
  → zoompan …:s=3840x2160                         (rastet auf 0,25 Ausgabepixel)
  → scale=1920:1080:flags=lanczos                 (mittelt den Rest weg)
```

Drei Dinge auf einmal: Die Rasterstufe sinkt auf ein Viertel Ausgabepixel;
der Ausschnitt wird **herunter**- statt hochskaliert, behält also echtes
Detail; und die letzte Reduktion von 3840 auf 1920 verwandelt den
Restsprung in eine weiche Helligkeitsänderung an der Kante statt in einen
Versatz — genau das, was Bewegung unterhalb eines Pixels ausmacht.

**Zwei einfachere Fassungen wurden geprüft und sind schlechter:**

| Variante | Ruckeln | Schärfe Frame 0 | |
|---|---|---|---|
| 7680 → `zoompan` **s=3840** → lanczos 1920 | **0,148 px** | **0,807** | ✅ gewählt |
| 7680 → `zoompan` **s=1920** direkt | 0,250 px | 0,693 | verworfen |
| 5760 → `zoompan` **s=1920** direkt | 0,289 px | 0,699 | verworfen |

Grund: der interne Bicubic von `zoompan` ist als 4:1‑Verkleinerer schlecht.
Zweistufig — 2:1 bicubic, dann 2:1 lanczos — ist das Bild sowohl ruhiger
**als auch** um 15 % härter in der Kontur.

### Ehrliche Nachteile von (b)

- **Rechenzeit ×2,8** gegenüber (a). Hochgerechnet auf ein 10‑Minuten‑Video:
  **rund 75 Minuten** Bildspur auf diesen 4 Kernen. Einmal je Video,
  parallelisierbar über die Einstellungen.
- **Am Anfang der Fahrt 2,4 % weicher als (a)** (0,807 gegen 0,827), weil
  zweimal neu abgetastet wird. Ab der Bildmitte dreht sich das um; am Ende
  ist (b) **7,5 % härter**, weil (a) dort echtes Detail hochrechnet, das es
  nicht mehr hat.
- Zwischenframes bei 3840×2160 brauchen Speicher.

### Und (c)?

(c) ist **schärfer als beide** — 0,964 gegen 0,827/0,807 — weil überhaupt
nicht neu abgetastet wird: ein einziger LANCZOS-Schritt von 2752 auf 1920,
danach 144 identische Frames. Zittern ist nicht reduziert, sondern
**begrifflich ausgeschlossen**.

Der Einwand aus der Aufgabenstellung trägt: bei 3–4 s je Einstellung und
120–300 Einstellungen entsteht die Bewegung durch den **Schnitt**. Das
Vorbild bewegt die Kamera „fast nur auf Karten"
([`stil-ink-explainer.md`](../stil-ink-explainer.md), Zeile 84) — also nicht
durchgehend. (c) kostet außerdem **die Hälfte der Rechenzeit von (a)** und
ein Fünftel von (b).

Wogegen (c) steht: nichts in diesem Repo. Die Pflicht „Standmotiv mit
sanfter Bewegung" stammt aus `formel/` in BibelTube und gilt hier
ausdrücklich **nicht** (siehe `README.md`, `config.md`). Für diesen Kanal
ist statisch frei wählbar.

---

## Empfehlung

**(b) als Standardweg, (c) als ausdrücklich erlaubte Alternative je
Einstellung.**

Nicht „(b) überall": Eine Fahrt, die nichts erzählt, ist auch ruckelfrei
noch Zierrat, und (c) ist schärfer und billiger. Aber der Weg muss gebaut
und geprüft sein, damit eine Fahrt möglich ist, **wo sie etwas zeigt** — auf
Karten, Zeitleisten, Diagrammen, so wie beim Vorbild.

Wer (c) allein wählt, bekommt das schärfste Bild, die kürzeste Rechenzeit
und garantiert kein Zittern — um den Preis, dass eine Karte nicht mehr
abgefahren werden kann.

---

## Was nach der Wahl passiert

1. **`video-02.mp4` neu montieren** — derselbe Schnittplan, dieselben 159
   Einstellungen, dieselbe Tonspur.
   **⚠️ Das geht derzeit nicht, und zwar aus einem Grund, der nichts mit der
   Kamerafahrt zu tun hat:** In diesem Repository gibt es **kein
   `montage.py`, kein `video-02`, keine Tonspur, keinen Schnittplan und
   keine 159 Einstellungen.** Geprüft: Arbeitsbaum, vollständige
   Git-Historie aller acht Zweige, Dateisystem. Die Kamerafahrt liegt in
   `produktion/pipeline/schritt5_video.py` — deshalb war Schritt 1
   beantwortbar. Der Rest fehlt. Es deckt sich mit dem Repo-Stand:
   `README.md` führt die Pipeline als **„nicht gebaut"**, den Bildstil und
   die Stimme als **OFFEN**, und nennt als frühesten sinnvollen
   Produktionsstart den **26.10.2026**.
2. **Festschreiben** in `schritt5_video.py`, `produktion/config.md` und den
   Szenenlisten-Vorgaben, mit datiertem Vermerk.

Video 1 bleibt unangetastet.

---

## Nachvollziehen

```bash
python3 recherche/kamerafahrt-proben/quantisierung.py   # Rasterung nachrechnen
bash    recherche/kamerafahrt-proben/bauen.sh           # die drei Clips bauen
python3 recherche/kamerafahrt-proben/messen.py          # Zittern messen
python3 recherche/kamerafahrt-proben/kantenspur.py      # Kantenspur zeichnen
```

Gemessen mit ffmpeg 6.1.1, 4 Kerne. `bauen.sh` schreibt die Clips in ein
Arbeitsverzeichnis; `messen.py` und `kantenspur.py` erwarten sie im
aktuellen Ordner.

**Warum CRF 16 und nicht die 28 aus `config.md`:** Bei CRF 28 hätte man
Kamerafahrt und Codec gleichzeitig verglichen. Alle drei Clips sind deshalb
identisch bei CRF 16 kodiert — der Vergleich zeigt nur die Fahrt. Dass CRF
28 für dieses Format vermutlich zu hoch ist, ist ein **eigener, unabhängiger
Befund** und steht bereits als „erster Kandidat zum Nachmessen" in
`config.md`. Er ist hier nicht mitentschieden.
