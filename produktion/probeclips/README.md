# Probeclips

> **Hier liegt ein Clip, nicht drei.** Mehr war im Repository nicht zu finden —
> die Suche ist unten dokumentiert. Nichts wurde neu gerendert
> (**0 Higgsfield-Credits**).

## Die Datei

| | |
|---|---|
| Datei | `video-01-probe.mp4` |
| Größe | 9.720.798 B = 9,3 MB |
| MD5 | `efb61d1b7bc01a337f5f82fedef1ec47` |
| Laufzeit | **43,03 s** [gemessen, mvhd-Atom] |
| Spuren | Video `avc1` (H.264), Ton `mp4a` (AAC) [gemessen, stsd-Atom] |
| **Nicht zerlegt** | 9,3 MB liegen weit unter der GitHub-Grenze von 100 MB je Datei — die Teilung wie in `produktion/auslieferung/` ist hier unnötig |

## Was der Clip ist

Ein **Teilrender von Video 1** („Who Built the First Roads and Why?"), nicht ein
eigenständiger Probeclip. Erzeugt von `produktion/video-01/montage.py` im
Modus `--bis N`: dabei wird der Schnittplan auf die ersten N Einstellungen
gekürzt und das Ergebnis unter dem Namen `video-01-probe.mp4` statt
`video-01.mp4` abgelegt (Zeile 123 des Skripts).

Es sind also die **ersten 43 Sekunden des fertigen Videos** mit der echten
Tonspur, kein 6-Sekunden-Muster und kein Stiltest.

## Woher er kommt

Die Datei lag nicht am Kopf eines Branches, sondern nur in der Historie:

| Commit | Was |
|---|---|
| `09acc99` Tonspur fertig, Aussprache-QA bestanden … | **angelegt** |
| `78333d6` Video fertig montiert und gegen den Schnittplan geprueft | **gelöscht** |

Gelöscht wurde sie zusammen mit dem Endvideo, mit der Begründung im
Commit-Text: „Die Videodatei bleibt aus dem Repository heraus (142 MB)." Der
Probeclip mit seinen 9,3 MB fiel dabei mit weg, obwohl er die Grenze nie
gerissen hätte.

Enthalten ist der anlegende Commit in `claude/elevenlabs-voice-samples-p4t00y`
und `claude/unknown-frequencies-style-r38epq`. Hierher geholt wurde die Datei
per `git cat-file blob` aus Blob `cad55130` — **byteweise dieselbe**, die Größe
stimmt mit der über die GitHub-API gemeldeten exakt überein.

## Was NICHT gefunden wurde

Gesucht wurde nach drei Probeclips. Geprüft [alle gemessen, 2026-08-17]:

- **alle acht Branches auf dem Remote**, jeweils der komplette Dateibaum
- **die vollständige Historie über alle Refs** (`git log --all --name-only`)
- **das Dateisystem des Containers** — dort liegt **keine einzige** Videodatei
- Stashes und verlorene Objekte (`git stash list`, `git fsck --lost-found`)

Ergebnis: In diesem Repository existiert und existierte **genau eine** Datei mit
Video-Endung außerhalb der Auslieferungsteile — diese hier. Ein Verzeichnis
`probeclips` gab es nie.

Bewegte Bilder im Repo insgesamt:

| Ort | Was | Wo |
|---|---|---|
| `produktion/auslieferung/*.part` | die **zwei fertigen Videos**, je in 4 Teilen à ~37 MB | Branch `claude/elevenlabs-voice-samples-p4t00y` |
| `produktion/video-01/video-01-probe.mp4` | dieser Clip | nur in der Historie, jetzt hier |

Dazu 71 MP3-Dateien (Stimmproben und Tonspuren) — Ton, keine Clips.

## Wenn drei Clips gemeint waren

Dann stammen sie aus einer anderen Sitzung und wurden dort nie committet.
Die Container sind flüchtig; was nicht im Repository liegt, ist nach Ende der
Sitzung weg und von hier aus nicht wiederherstellbar.

Nachbauen ließe sich der Teilrender jederzeit ohne Bildkosten — `montage.py
--bis N` setzt nur vorhandene Motivbilder und die fertige Tonspur zusammen.
**Neue** Probeclips in einem anderen Stil wären dagegen echte Bildgenerierung
und damit kostenpflichtig; außerdem ist die Stilentscheidung laut `README.md`
noch offen.

## Abholen

```sh
git checkout claude/erklaerchannel-neue-fragen-axt842 -- produktion/probeclips/
md5sum produktion/probeclips/video-01-probe.mp4
# efb61d1b7bc01a337f5f82fedef1ec47
```
