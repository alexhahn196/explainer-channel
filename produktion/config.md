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
| `zoom` / `zoom_faktor` / `zoom_zyklus_s` | `ja` / `1.04` / `300` | **GILT NICHT** — der 300-Sekunden-Atemzyklus ist für ein 10-Minuten-Video sinnlos. ⚠️ **2026-08-17: Der Zoom-Weg in `schritt5_video.py` ist zusätzlich defekt** — `zoompan` rastet den Ausschnitt auf ganze Quellpixel, das Bild zittert um 1 px, bei flachen Grafiken mit harten Konturen sichtbar. Gemessen und belegt in [`recherche/kamerafahrt-proben/README.md`](../recherche/kamerafahrt-proben/README.md). **Nicht ungeprüft übernehmen; Entscheidung über den Ersatzweg steht aus.** |
| `ki_clip_ordner*` | — | **GILT NICHT** |
| `kapitelmarken_videos` | `V1,V2,V6,V8` | **GILT NICHT** — videobezogene Kanal-1-Liste |
| `video_crf` | `28` | **ÜBERNOMMEN — UNGEPRÜFT** — CRF 28 ist auf ein nahezu statisches Bild optimiert. Bei 2–5-Sekunden-Schnitten ist das vermutlich zu hoch (sichtbare Artefakte an Schnittkanten). **Erster Kandidat zum Nachmessen.** |
| `video_preset` | `medium` | **ÜBERNOMMEN — UNGEPRÜFT** |
| `audio_bitrate` | `192k` | **ÜBERNOMMEN — UNGEPRÜFT** |
| **Bildstil** | — | **OFFEN** — drei Varianten getestet, siehe `recherche/stil-ink-varianten/README.md`. Empfehlung dort: V1 als Basis plus das Element aus V3. Nicht entschieden. |

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
