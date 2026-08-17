# Kanal-Konfiguration — Erklärkanal

> **Diese Datei ist noch keine Konfiguration, sondern eine Checkliste.**
> Die Pipeline aus dem BibelTube-Repo liest einen solchen Block maschinell
> (`produktion/pipeline/gemeinsam.py`). Bevor hier irgendetwas gerendert wird,
> muss **jeder** mit `PRÜFEN` markierte Wert für diesen Kanal entschieden sein.
>
> Legende:
> **`ÜBERNOMMEN — UNGEPRÜFT`** = Wert stammt unverändert aus BibelTube und ist
> für einen 10-Minuten-Erklärkanal **nicht** validiert ·
> **`OFFEN`** = es gibt noch keinen Wert ·
> **`GILT NICHT`** = der BibelTube-Wert ist für diesen Kanal gegenstandslos.

---

## Warum hier nichts stillschweigend übernommen wird

Die BibelTube-Werte sind aus **10 christlichen Schlafkanälen** abgeleitet:
3,5 Stunden Laufzeit, Sprachanteil 95 %, ein einziges Standmotiv über die volle
Länge, Publikum liegt im Bett und schläft ein. Dieser Kanal ist das Gegenteil:
**8–15 Minuten, ~120–300 Einstellungen je Video, wacher Zuschauer, der etwas
verstehen will.** Kein einziger inhaltlicher Schwellenwert überträgt sich
automatisch. Die *Technik* überträgt sich — die Skripte, das Schrittmodell, das
Rendern. Die *Zahlen* nicht.

---

## Stimme

| Feld | Wert | Status |
|---|---|---|
| `stimme_name` / `stimme_id` | — | **OFFEN** — BibelTube nutzt „MILO SOOTHING VOICE", eine bewusst einschläfernde Stimme. Für einen Erklärkanal ungeeignet. Neuer Blindtest nötig. |
| `tts_modell` | `s2.1-pro-free` | **ÜBERNOMMEN — UNGEPRÜFT** (Fish Audio; Anbieterwahl ist Technik, das Modell aber nicht getestet) |
| `tts_endpoint` | `https://api.fish.audio/v1/tts` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `prosody_speed` | `0.88` | **GILT NICHT** — 0,88 ist Schlaftempo. Ein Erklärkanal braucht Normaltempo oder darüber. |
| `wpm_erwartet` | `145.9` | **GILT NICHT** — folgt aus `prosody_speed`. Ink Explainer liegt bei ~2.400 Wörtern auf 11:37, also grob **210 wpm**. |

**Akzentprüfung:** Das Verfahren aus BibelTube (`rhotik.py`, F3-Formant-Minimum
über postvokalischem /r/, Grenze 2100 Hz) ist **übertragbare Technik** und sollte
auf die neue Stimme angewandt werden. Die dortigen Referenzwerte
(`produktion/pipeline/qa/rhotik_referenz.json`) sind **Kanal-1-Messungen** und
absichtlich **nicht** mitkopiert worden.

## Text

| Feld | Wert | Status |
|---|---|---|
| `uebersetzung` | `webbe` | **GILT NICHT** — Bibelübersetzung |
| `bibel_api` | `https://bible-api.com` | **GILT NICHT** |
| `versalien_normalisieren` | `ja` | **ÜBERNOMMEN — UNGEPRÜFT** — die Ursache (TTS buchstabiert Versalien) ist stimmenabhängig, nicht inhaltsabhängig. Mit der neuen Stimme nachprüfen. |
| Faktenprüfung vor der TTS | — | **OFFEN** — für diesen Kanal **zusätzlich nötig**, siehe die Skizze in `recherche/nischen-kanal-2.md`. Rund 25 prüfpflichtige Aussagen je 1.500-Wort-Skript, ~1–1,75 h je Video. Für BibelTube gab es diesen Schritt nicht. |

## Skriptvorgaben

Kanalweit, aus der Arbeit an Video 1 und 2 abgeleitet. Anders als die
Tabellen oben stammen diese Werte nicht aus BibelTube, sondern aus
eigenen Messungen an den Vorbildkanälen.

| Feld | Wert | Status |
|---|---|---|
| Wortzahl | 1.850–2.050 | **GEMESSEN** — ergibt 8:30–9:30 bei 219 WPM |
| Wörter unter 7 Zeichen | ≥ 82 % | **GEMESSEN** an Ink Explainer |
| Antwort auf die Titelfrage | in den ersten 30 s | **GEMESSEN** |
| Belegpflicht | jede neue Behauptung mit Zahl oder Datum trägt eine Quellen-ID | **GESETZT** — daran hängt `faktencheck.py` |
| **Schema-Anteil der Laufzeit** | **≤ 12 %** | **GESETZT 16.08.2026, angehoben 17.08.2026** — Video 1 lag bei 26 % und war schon zu viel, der erste Sterne-Entwurf bei 58 %. Gemessen wie in `produktion/video-02/tonprobe-bilder.py`. Wo ein Vorgang erklärt werden müsste, wird stattdessen gezeigt, was ein Mensch dabei tat. **Der Wert ist gesetzt, nicht gemessen** — 10 war so willkürlich wie 12. Angehoben, weil Video 2 nach der Verankerung bei 10,1 % lag und 0,6 s Laufzeit keine neue Montage rechtfertigen. |
| **Anstieg durch die Verankerung** | bis zu **1 Punkt** | **GEMESSEN 17.08.2026** — der Schema-Anteil wird am Plan gerechnet (Video 2: 9,7 %) und steigt, wenn die Einstellungen am gesprochenen Wort verankert werden (10,1 %). Die Laufzeit verteilt sich dorthin, wo tatsächlich länger gesprochen wird, und das trifft die Schemastellen nicht gleichmäßig. Bei der Planung einen Punkt Luft lassen. |
| **Einstellungslänge** | 2,4–6,0 s | **PLANUNGSWERT, kein Prüfkriterium** — auf 219 WPM gerechnet. Die Stimme liefert 202, also werden alle Einstellungen rund ein Zehntel länger; in Video 2 stehen 14 von 159 über 6,0 s, die längste bei 8,95 s. Geprüft wird nur die Untergrenze, und die auch nur mit Vorbild: unter 2,4 s darf ein Schnitt nur liegen, wenn dasselbe Motiv oder sein Paarpartner daneben steht. |

### Aussprachekorrekturen kosten Tempo: rund 5 %

**GEMESSEN 17.08.2026, für alle künftigen Videos in der Laufzeitplanung.**

| Lauf | Text | WPM |
|---|---|---:|
| Stimmentest Video 1 | Testtext **ohne** Respellings | **214,3** |
| Video 2, Vertonung | Skript **mit** 24 Korrekturen | **205,3** |
| Video 2, ganze Spur | dazu 0,42 s Atempause je Fuge (23×) | **202,0** |

Ein Respelling wird bedächtiger gesprochen als das Wort, das es ersetzt:
„SEF-ee-ids" braucht mehr Zeit als „Cepheids". Bei 24 Korrekturen in
2.071 Wörtern kostet das **rund 5 % Tempo**, die Atempausen weitere 1,6 %.

**Rechenweg für die Planung:** erwartete Laufzeit = Wörter ÷ (214 × 0,95)
× 60, plus 0,42 s je Absatzfuge. Für Video 2 ergibt das 10:12 — die
gemessene Spur liegt bei 10:15. Wer mit 219 WPM plant, unterschätzt die
Laufzeit um fast eine Minute: geplant waren 9:20, geworden sind 10:16.

**Und umgekehrt:** wer die Wortzahl an einer Ziellaufzeit ausrichtet, muss
die Respellings vorher kennen. Die Ausspracheliste gehört damit vor die
Wortzahlprüfung, nicht danach.

### Anrede-Marker: der Zielwert gilt je Passage, nicht als Gesamtmittel

**Befund vom 16.08.2026, bindend für alle künftigen Videos.**

Der gemessene Zielwert (74,7 Anrede-Marker je 1.000 Wörter, aus der
Schreibart von Unknown Frequencies) gilt für **anredegetragene
Passagen** — Eröffnung, direkte Anleitung, Schluss. Er gilt **nicht** als
Mittelwert über ein ganzes Skript, das Vignetten enthält.

Der Grund ist strukturell, nicht nachlässig. Eine Vignette erzählt von
*jemandem*, nicht von *dir*: der Mann an der Mikrometerschraube, die Frau
am Leuchttisch. Genau diese Vignetten sind der Grund, warum die
Erzählform trägt und warum der Schema-Anteil auf 10 % fällt — ein
Vorgang, den ein Mensch ausführt, braucht kein Diagramm. Die Marker-Dichte
über das ganze Skript auf 74,7 zu zwingen hieße, die Vignetten in die
zweite Person umzuschreiben („du bist der Mann in Königsberg"). Das ist
eine andere Form, und eine schlechtere.

Gemessen an Video 2, Erzählfassung:

| Passage | Anrede je 1.000 |
|---|---:|
| erstes Fünftel (Eröffnung, Daumen, Erdbahn) | **68,6** |
| Königsberg-Vignette (der freigegebene Maßstab) | ~50 |
| gesamtes Skript | **34,2** |

**Prüfregel:** Das erste Fünftel muss ≥ 40 erreichen (harte Vorgabe, wie
bisher). Kein Absatz darf anredefrei sein. Der Gesamtwert wird gemessen
und berichtet, aber nicht gegen 74,7 geprüft.

## Chunking

| Feld | Wert | Status |
|---|---|---|
| `chunk_max_zeichen` | `1900` | **ÜBERNOMMEN — UNGEPRÜFT** — hergeleitet aus Psalm 136 (23 Semikolon-Verse), also aus der Struktur eines Bibeltexts. Ein Fließtext-Skript hat andere Satzgrenzen. |
| `chunk_nur_satzende` | `ja` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `chunk_pegel_angleichen` | `ja` | **ÜBERNOMMEN — UNGEPRÜFT** — die Ursache (TTS normalisiert jeden Chunk einzeln) ist technisch, gilt vermutlich weiter |
| `tts_parallel` | `12` | **ÜBERNOMMEN — UNGEPRÜFT** — reine Durchsatzgröße, unkritisch |

## Pegel

| Feld | Wert | Status |
|---|---|---|
| `pegel_stimme_dbfs` | `-19.0` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `pegel_bett_dbfs` | `-31.0` | **GILT NICHT** — setzt ein durchlaufendes Klangbett voraus |
| `abstand_soll_db` | `12.0` | **GILT NICHT** — die 12 dB stammen aus „Stimme in 6/6 Fällen klar über dem Bett" bei Schlafvideos. Ein Erklärkanal hat meist gar kein Bett, und wenn, dann leiser. |
| `peak_max_dbfs` | `-1.0` | **ÜBERNOMMEN — UNGEPRÜFT** — technischer Headroom, vermutlich unverändert gültig |
| `ducking` | `nein` | **OFFEN** — bei Musik unter Sprache in einem Erklärvideo neu zu entscheiden |

## Klangbett

| Feld | Wert | Status |
|---|---|---|
| `bett_datei` | `bett_pad_feuer.flac` | **GILT NICHT** — Kanal-1-Artefakt, nicht mitkopiert |
| `vorlauf_s` `1.5` / `einblende_s` `1.5` | | **ÜBERNOMMEN — UNGEPRÜFT** — abgeleitet aus „Sprache beginnt in Sekunde 0–3 (n=24)" bei Schlafkanälen. Für einen Erklärkanal ist der Hook-Zeitpunkt neu zu messen. |
| `nachlauf_s` `6.0` / `ausblende_s` `3.0` | | **GILT NICHT** — 6 s Nachlauf sind Schlafvideo-Logik |

## Bild und Video

| Feld | Wert | Status |
|---|---|---|
| `breite` / `hoehe` | `1920` / `1080` | **ÜBERNOMMEN — UNGEPRÜFT** — Standardformat, vermutlich gültig |
| `fps` | `24` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `videoquelle` | `ki_clips` | **GILT NICHT** — 4 Clips à 12 s als 48-s-Zyklus über 3,5 h. Dieser Kanal braucht **120–300 verschiedene Einstellungen** je Video. Anderes Modell. |
| `zoom` / `zoom_faktor` / `zoom_zyklus_s` | `ja` / `1.04` / `300` | **GILT NICHT** — der 300-Sekunden-Atemzyklus ist für ein 10-Minuten-Video sinnlos. Ersetzt durch `kamerafahrt` (Zeile darunter). |
| `kamerafahrt` | **`fahrt` über `kamerafahrt.py`, Voreinstellung je Einstellung `statisch`** | **ENTSCHIEDEN 2026-08-17** — siehe den Vermerk unten. Geplant wird die Fahrt je Einstellung in [`szenenliste-vorgaben.md`](szenenliste-vorgaben.md), gerendert ausschließlich über [`pipeline/kamerafahrt.py`](pipeline/kamerafahrt.py). |
| `ki_clip_ordner*` | — | **GILT NICHT** |
| `kapitelmarken_videos` | `V1,V2,V6,V8` | **GILT NICHT** — videobezogene Kanal-1-Liste |
| `video_crf` | `28` | **ÜBERNOMMEN — UNGEPRÜFT** — CRF 28 ist auf ein nahezu statisches Bild optimiert. Bei 2–5-Sekunden-Schnitten ist das vermutlich zu hoch (sichtbare Artefakte an Schnittkanten). **Erster Kandidat zum Nachmessen.** |
| `video_preset` | `medium` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `audio_bitrate` | `192k` | **ÜBERNOMMEN — UNGEPRÜFT** |
| **Bildstil** | — | **ENTSCHIEDEN 15.08.2026** — V2: finaler Machart-Block aus `recherche/stil-figuren/lauf2-erwachsen/README.md` plus Z3-Lichtquelle aus `recherche/stil-touch/`. |
| **Farbe** | — | **ENTSCHIEDEN 15.08.2026** — natürliche Farben, so wie die Sache wirklich aussieht. **Keine** Themenpaletten und **keine** Signalfarbe; beide getestet und verworfen, Grund in `recherche/stil-archiv.md`. Schemabilder haben eine eigene Fassung ohne Himmel und Vegetation. |

### Bildvorgaben: die Bedingungsregel

**ENTSCHIEDEN 16.08.2026.** Gilt für alle künftigen Videos.

> **Jeder Block im Anweisungsteil darf nur nennen, was in ALLEN Motiven
> vorkommt, für die er gilt. Was nur manchmal vorkommt, gehört in einen
> bedingten Block.**

Das ist die gemeinsame Wurzel von vier Fehlschlägen in zwei Videos. Der
Mechanismus ist immer derselbe: **ein Wort im Prompt, das etwas benennt,
was in diesem Bild nicht sein soll, zeichnet es hin** — auch wenn es nur
als Beispiel, als Stilangabe oder in einer Verneinung dasteht.

| Block | nannte | fehlte in | Schaden |
|---|---|---|---|
| Epochensatz | `Clothing, tools` | 43 figurenlosen Motiven | M01 kam mit zwei Personen in Kleidung um 1900 und einer Schubkarre zurück, obwohl „no people in this picture at all" dastand |
| Farbsatz | `foliage and grass are green`, `The sky is blue` | 49 Motiven ohne Vegetation | M24 verlangte die Nahaufnahme eines Sterns und kam als Tageslandschaft: 60 % blauer Himmel, 22 % grün |
| Strichstärkenregel | `figures, clothing, props` | denselben 43 | zweiter Auslöser für dieselben Figuren |
| Florazeile | `without leaves` | — | M13 verlangte kahle Bäume und bekam belaubte Kronen; die Verneinung nennt das Laub |

Drei Folgeregeln, die daraus folgen:

1. **Verneinen zählt als Nennen.** „no palms", „without leaves", „no wood
   grain" schreiben Palme, Laub und Holz in den Prompt. Wo eine Verneinung
   ersetzbar ist, wird sie durch die Beschreibung dessen ersetzt, was
   dasteht — „each drawn as a bare branching silhouette of trunk and open
   twigs" statt „without leaves".
2. **Beispielreihen sind Inventarlisten.** „every surface — rock, stone
   blocks, earth, water, sky and vegetation alike" war als Illustration
   einer Regel gemeint und wurde als Bestandsangabe des Bildes gelesen. Eine
   Regel, die ohne Beispiele auskommt, kommt ohne Beispiele aus.
3. **Der Block darf der Szene nicht widersprechen.** M06 zeigt ein Gesicht
   in Nahsicht, und derselbe Prompt verbot „no head, no face" — der
   Anweisungsteil verbot, was die Szene verlangte.

Umgesetzt in `produktion/video-01/bildplan.py` als bedingte Fassungen
(`machart()`, `farben()`, `figur()`, `EPOCHE_*`, `FRAMING_*`) und in
`produktion/video-02/bildplan2.py` als harte Prüfungen, die den Lauf
abbrechen, bevor Credits fließen: `pruefe_szene` (Versalien),
`pruefe_personenworte` (43 figurenlose Motive), `pruefe_pflanzenworte`
(49 Motive ohne Vegetation), `pruefe_vokabular` (Schrift, Grafik-Gattung,
Beschriftung, Aufschrift-Träger).

**Granularität.** Die Bedingung wird je Motiv gestellt — ein Motiv, das
mehrere Felder zeigt, kann sie in sich wechseln. M28 ist ein Triptychon aus
drei Orten: die mittlere Vignette hat Vegetation, die beiden anderen nicht,
und die Laubzusage landete prompt in der kahlen. **Bei jedem Mehrfeld-Motiv
— Triptychon, Vorher-Nachher, geteilter Rahmen — gilt die vorsichtigere
Fassung**, und was nur ein Feld betrifft, gehört in die Szene, nicht in den
Anweisungsteil. In `bildplan2.py` steht das als `GEMISCHTE_FLORA`.

### Die zweite Hälfte: ein fehlender Satz ist so teuer wie ein falscher

**ENTSCHIEDEN 16.08.2026.**

> **Was in ALLEN Motiven einer Gruppe gleich sein soll, muss ausdrücklich
> genannt werden — sonst wählt das Modell je Bild neu, und die Serie
> zerfällt.**

Die erste Hälfte der Regel verhindert, dass ein Block etwas nennt, was nicht
da ist. Sie sagt nichts darüber, was ungesagt bleibt. Der Sternbefund aus
Stapel 3 ist der Beleg: kein Block sagte je, wie ein Stern dieser Reihe
aussieht.

| Motiv | helle Fläche | davon farbig |
|---|---:|---:|
| M10 — Szene sagt „white star shapes" | 2,63 % | **0,0 %** |
| M29 — Szene sagt nichts | 0,24 % | **60,3 %** |
| M36 — Szene sagt nichts | 1,94 % | **81,2 %** |

Drei Sternfelder in einem Video, die aus drei Kanälen stammen könnten. Kein
falscher Satz war schuld, sondern ein fehlender.

**Die Prüffrage lautet deshalb doppelt:**

1. Nennt der Block etwas, das in einem Teil der Motive nicht vorkommt?
2. Gibt es eine Eigenschaft, die über alle Motive gleich sein soll, und
   sagt sie niemand?

Frage 2 fällt beim Lesen des Prompts nicht auf — dort steht ja nichts
Falsches. Sie fällt erst auf, wenn man die fertigen Bilder **misst**.

An den ersten 35 Bildern von Video 2 durchgemessen, jeweils die größte
Farbfläche der betreffenden Art:

| Eigenschaft | gemessene Spanne | Befund |
|---|---|---|
| Sternfarbe | 0,0 % / 60,3 % / 81,2 % farbige Sternpunkte | **festgelegt** — `STERNFELD`, 14 Motive |
| Grundton dunkler Bilder | (0,0,0) reines Schwarz · (24,24,24) neutral · (12,24,36) tiefblau · M02 mit (48,48,60) doppelt so hell | **festgelegt** — `DUNKELGRUND`, 25 Motive |
| Papierton | (228,228,228) neutral · (240,228,228) rosastichig · (240,240,216) gelblich | **festgelegt** — `PAPIERTON`, 13 Motive |
| Metallton | (160,130,60) dunkler Ocker · (230,170,70) leuchtendes Gold · (250,220,160) blasser Sand | **festgelegt** — `MESSINGTON`, 5 Motive |
| wiederkehrende Figur | derselbe Mann in M20/M23/M26 mit (230,170,150), (210,170,100), (200,170,120) | **festgelegt** — Steckbrief, 3 Motive |
| Hauttonspanne allgemein | R 200–240, G 160–180, B 100–160 über zehn verschiedene Personen | **kein Befund** — verschiedene Menschen dürfen verschieden aussehen; nur wiederkehrende müssen gleich bleiben |
| Wasserfarbe | nur ein Motiv (M31) zeigt Wasser | **kein Befund** — eine Gruppe von eins ist keine Gruppe |

**Der teuerste Einzelfall war die wiederkehrende Figur.** Die Szene sagt
„derselbe Mann", aber die drei Bilder entstehen unabhängig voneinander, und
das Modell hat das erste nie gesehen — genau die Lage der Zustandspaare, nur
über eine Person statt über einen Bildausschnitt. Wer mehr als einmal
vorkommt, braucht einen Steckbrief im Anweisungsteil. Nach der Kanalvorgabe
(Epochenfiguren, keine Portraitähnlichkeit) legt der Steckbrief eine Bauform
fest, kein Gesicht: Alter, Bau, Haut, Bart- und Haarform, Kleidungsstück und
Farbe.

**Nicht rückwirkend nachgezogen:** die Blöcke gelten ab jetzt. Bereits
erzeugte Bilder werden nicht blind neu gemacht, sondern am Ende gemessen;
neu erzeugt wird, was dann noch aus der Reihe fällt.

### ⚠️ Vermerk 2026-08-17 — Zittern der Kamerafahrten

**Symptom.** Bei langsamen Zooms und Schwenks sprang das Bild pixelweise.
Am stärksten bei **flachen Grafiken mit harten Konturen** — also bei genau
unserer Bildwelt, weil dort eine Kante als Ganzes um eine Pixelspalte
springt, statt im Detail unterzugehen.

**Ursache.** `zoompan` rundet den Bildausschnitt auf **ganze Quellpixel** —
Größe *und* Lage (`w`, `h`, `x` sind in `vf_zoompan.c` `int`). Die Fahrt
steht still und springt dann um einen ganzen Pixel. Verschärft dadurch, dass
`schritt4_bild.py` jede Quelle vorab von 2752 auf 1920 px herunterrechnete:
danach war ein Quellpixel gleich einem Ausgabepixel. Gemessen **0,998 px**
Ruckeln; beim 300‑s‑Zyklus waren **99,0 % aller Frames exakte Standbilder**.

**Lösung.** Überabtasten, dann herunterskalieren — Quelle einmal auf das
Vierfache der Ausgabebreite, `zoompan` auf das Doppelte, danach lanczos auf
1920. Ergebnis **0,150 px**, und das Bild ist dabei an jedem Zeitpunkt
schärfer als vorher, weil herunter- statt hochskaliert wird.

**Festgeschrieben in** [`pipeline/kamerafahrt.py`](pipeline/kamerafahrt.py)
(einziger erlaubter Weg, mit `--selbsttest`),
[`szenenliste-vorgaben.md`](szenenliste-vorgaben.md) (Voreinstellung
`statisch`, eine Fahrt wird begründet) und
[`recherche/kamerafahrt-proben/README.md`](../recherche/kamerafahrt-proben/README.md)
(Messwerte, Probeclips, verworfene Varianten).

**Nicht wieder einbauen:** `zoompan` direkt auf ein Bild in Ausgabegröße ·
die Quelle vor der Fahrt kleinrechnen · `zoompan` direkt auf die Endgröße
rechnen. Alle drei sind gemessen und schlechter.

## Laufzeit

| Feld | BibelTube | Status |
|---|---|---|
| `laufzeit_min_h` | `3.0` | **GILT NICHT** |
| `laufzeit_ziel_von_h` / `_bis_h` | `3.4` / `3.8` | **GILT NICHT** — Zielkorridor hier **8–15 Minuten**, abgeleitet aus den Vorbildkanälen (Ink Explainer 5:15–11:37, Axen 5:15–12:41) |

## Qualitätsschwellen

| Feld | BibelTube | Status |
|---|---|---|
| `sprachanteil_min_pct` | `95.0` | **GILT NICHT** — 95 % Sprachanteil ist eine Schlafkanal-Kennzahl. Ein Erklärvideo darf und soll Pausen für Grafiken haben. |
| `laengste_pause_max_s` | `20.0` | **GILT NICHT** — 20 s Pause in einem 10-Minuten-Video wären ein Totalausfall. Realistische Grenze eher 2–3 s. **OFFEN.** |
| `sprachstart_max_s` | `3.0` | **ÜBERNOMMEN — UNGEPRÜFT** — der Wert könnte zufällig passen (Erklärkanäle starten ebenfalls sofort), ist aber aus anderen Daten hergeleitet |
| `cta_max` | `2` | **ÜBERNOMMEN — UNGEPRÜFT** |
| Quellenangaben in der Beschreibung | — | **OFFEN, aber empfohlen** — Ink Explainer legt als einziger der drei gemessenen Vorbildkanäle Quellen mit DOI offen und ist zugleich der jüngste mit dem stärksten Ergebnis. Siehe `recherche/nischen-kanal-2.md`. |
| Epistemische Marker | — | **OFFEN, aber empfohlen** — an sechs Transkripten gemessen: das jeweils stärkere Video eines Kanals markiert Unsicherheit häufiger. n = 6, Korrelation, kein Beweis. |

---

## Was hier bewusst NICHT steht

- **Kein API-Schlüssel.** Wie in BibelTube: ausschließlich über Umgebungsvariable,
  nie im Repository.
- **Kein Upload-Zugang.** Upload von Hand, damit die KI-Kennzeichnung gesetzt wird.
- **Kein Thumbnail-Pfad.** Noch nicht entschieden — und für diesen Kanal ist der
  Thumbnail-Stil nicht einmal gemessen (siehe Vorbehalte in
  `recherche/stil-ink-explainer.md`).

## Bilanz der Übernahme

Gezählt über die Tabellenzeilen oben (eine Zeile kann zwei verwandte Felder
zusammenfassen, etwa `vorlauf_s` / `einblende_s`):

| Status | Zeilen |
|---|---|
| **ÜBERNOMMEN — UNGEPRÜFT** | 17 |
| **GILT NICHT** | 16 |
| **OFFEN** | 6 |
| **Summe** | **39** |

**41 % der BibelTube-Konfiguration ist für diesen Kanal gegenstandslos, weitere
44 % sind unbestätigt.** Genau ein Wert wäre ohne Prüfung gefahrlos übernehmbar
gewesen — das Videoformat 1920×1080. Das ist die Begründung für die
Repo-Trennung in einer Zahl.
