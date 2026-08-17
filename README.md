# explainer-channel

Englischsprachiger **Erklärkanal**, faceless. Zweiter Kanal neben BibelTube —
in einem eigenen Repository, aus einem Grund, der weiter unten steht und der
wichtigste Satz dieser Datei ist.

## Was der Kanal ist

| | |
|---|---|
| Sprache / Markt | Englisch, Zielmarkt US |
| Format | faceless, KI-Standbilder mit sanfter Bewegung, TTS-Stimme |
| Videolänge | **8–15 Minuten** |
| Kadenz | **0,5 Uploads/Woche** — ein Video alle 14 Tage |
| Vorbild | **Ink Explainer** ([UCpgrEMx8diLrw7YNQ6r3uUw](https://youtube.com/channel/UCpgrEMx8diLrw7YNQ6r3uUw)) |
| Bauform | „Alltagsfrage an die Vergangenheit" plus Anlassbindung: ein Ereignis bringt die Suchanfragen, das Video behandelt den zeitlosen Stoff dahinter |
| Ausgeschlossen | Krieg, benannte lebende Personen, fremdes IP als Kern, True Crime, laufende politische Konflikte |

## ⚠️ Die BibelTube-Regeln gelten hier NICHT

Im Repository [alexhahn196/BibelTube](https://github.com/alexhahn196/BibelTube)
liegen `regeln/erfolgsregeln.md` und `formel/video-formel.md`. Beide sind aus
**zehn christlichen Schlafkanälen** abgeleitet und beschreiben deren
Erfolgsmuster:

- **3,5 Stunden** Laufzeit
- **Versalhöhe 11,5 %** im Thumbnail
- **Sprachanteil 95 %**
- durchgehendes **Serienmotiv**
- **Titelanker** als wiederkehrende Wortformel

Für einen **10-Minuten-Erklärkanal ist jede einzelne dieser Zahlen falsch.** Ein
Erklärvideo mit 95 % Sprachanteil hätte keine Luft für Grafiken; ein
Serienmotiv über 8 Minuten mit 120–300 Einstellungen ergibt keinen Sinn; 3,5
Stunden sind das Zwanzigfache der Ziellänge.

**Deshalb die getrennten Repositories: damit keine Sitzung versehentlich die
falsche Formel liest.** Wer in diesem Repo arbeitet, öffnet `regeln/` und
`formel/` aus BibelTube nicht — sie sind hier absichtlich nicht vorhanden.

Wie viel davon betroffen ist, steht als Zahl in
[`produktion/config.md`](produktion/config.md): von 39 durchgegangenen
Konfigurationszeilen sind **16 für diesen Kanal gegenstandslos**, 17 unbestätigt
übernommen und 6 noch offen — genau eine Einstellung wäre ohne Prüfung gefahrlos
übernehmbar gewesen.

## Stand

| Bereich | Stand |
|---|---|
| **Nische** | ✅ geprüft — History-Explainer, Belegkanäle und Einstiegsfenster dokumentiert in [`recherche/nischen-kanal-2.md`](recherche/nischen-kanal-2.md) |
| **Themen** | ✅ **47 Fragen** — 42 terminiert bis 08/2027, dazu **5 neue mit je 8/8 Punkten** und Anlässen bis 10/2028. Anlass-Kalender mit 29 belegten Ereignissen, Titelprüfung gegen 136 Konkurrenztitel, Belegbarkeit über Crossref und Wikipedia: [`recherche/themen-erklaerkanal.md`](recherche/themen-erklaerkanal.md). Die fünf neuen sind zusätzlich auf **Erzählbarkeit** geprüft — die Achse, die in der Bewertung der 42 fehlt. Die 42 sind gegen die Vergleichskanäle nachgeprüft, Stand 08/2026: [`recherche/vergleichskanaele-90-tage.md`](recherche/vergleichskanaele-90-tage.md) — 2 Fragen (F38, F18) stehen inzwischen fast wörtlich bei einem anderen Kanal, beide dort durchgefallen; kein Titelmerkmal der 28 Treffer hält der Prüfung stand |
| **Bildstil** | ⬜ **OFFEN** — Stil des Vorbilds gemessen ([`recherche/stil-ink-explainer.md`](recherche/stil-ink-explainer.md)), drei eigene Varianten getestet und bewertet ([`recherche/stil-ink-varianten/README.md`](recherche/stil-ink-varianten/README.md)). Empfehlung dort: V1 (Dreifarbenpalette) als Basis plus das wiederkehrende Element aus V3. **Nicht entschieden.** |
| **Pipeline** | ⬜ **nicht gebaut** — Skripte aus BibelTube liegen unter `produktion/pipeline/`, sind aber auf ein 3,5-Stunden-Schlafvideo eingestellt und für dieses Format weder angepasst noch gelaufen |
| **Stimme** | ⬜ OFFEN — die BibelTube-Stimme ist bewusst einschläfernd, hier unbrauchbar. Neuer Blindtest nötig. |
| **Faktenprüfung** | ⬜ konzipiert, nicht gebaut — Skizze in `recherche/nischen-kanal-2.md`, ~25 prüfpflichtige Aussagen und 1–1,75 h je Video |

## Nächste Schritte

1. **Stilentscheidung.** V1 + Element aus V3 gegenrechnen (ein Lauf, 2 Bilder,
   ~4 Credits). Die Laternenfigur muss dabei über ein Referenzbild fixiert
   werden, nicht über Text — sie wechselte in den Tests zwischen den Szenen die
   Proportionen.
2. **Ink-Explainer-Teardown.** Die 13 Videos des Vorbilds nach dem Muster von
   `teardown/` aus BibelTube auseinandernehmen. Transkripte sind über NexLev
   ziehbar, 0 Credits.
3. **Pipeline auf das Format umbauen.** Erster Kandidat zum Nachmessen:
   `video_crf = 28` — auf ein nahezu statisches Bild optimiert, bei
   2–5-Sekunden-Schnitten vermutlich zu hoch.
4. **Früheste sinnvolle Produktion: 26.10.2026.** Das ist der Produktionsstart
   für „Who Built the First Roads and Why?" zum **100. Jahrestag der Route 66 am
   11.11.2026** — der erste unverschiebbare Anlass, für den der Vorlauf noch
   reicht. Die davorliegenden Slots (ab 17.08.2026) setzen voraus, dass Stil und
   Pipeline bis dahin stehen; siehe die Terminwarnung in
   `recherche/themen-erklaerkanal.md`.

## Herkunft der Technik

Alles unter `produktion/` stammt aus
[alexhahn196/BibelTube](https://github.com/alexhahn196/BibelTube) und ist
**Technik, nicht Inhalt**:

| Übernommen | Was es ist |
|---|---|
| `produktion/pipeline/*.py` (17 Skripte) | Siebenschritt-Pipeline: Text → TTS → Klangbett → Bild → Video → SRT → Upload-Paket, dazu QA-Werkzeuge (`rhotik.py`, `qa_namen.py`, `satzlaengen.py`, `thumbnail.py`) |
| `produktion/pipeline/README.md` | Beschreibung des Schrittmodells |
| `produktion/motive/README.md` | Bildworkflow |
| `produktion/config.md` | **neu geschrieben** — jeder übernommene Schwellenwert einzeln markiert |

**Bewusst nicht übernommen:** `regeln/`, `formel/`, `teardown/`,
`produktion/videos-01-08.md`, `produktion/video-0*/`, `bibeltube-wissen.md`,
`stimmtest/` — sämtlich Kanal-1-Inhalt.

Ebenfalls dort geblieben: `produktion/pipeline/qa/` — das sind gemessene
Referenzwerte der Kanal-1-Stimme (F3-Formanten), also Inhalt. Das *Verfahren*
(`rhotik.py`) ist mitgekommen, die *Messwerte* nicht.
