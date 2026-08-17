# Verbindliche Entscheidungen — Video 1

> Entschieden am 15.08.2026. **Diese Datei ist verbindlich.** Wer für Video 1
> vertont, generiert oder montiert, hält sich an die Werte hier; abweichende
> Angaben in älteren Dokumenten sind überholt.

## Stimme und Vertonung — ENTSCHIEDEN

| Feld | Wert |
|---|---|
| Anbieter | ElevenLabs |
| Stimme | **Eric** |
| `voice_id` | `cjVigY5qzO86Huf0OWal` |
| Modell | `eleven_multilingual_v2` |
| **`seed`** | **`4242`** — Pflicht, siehe unten |
| `speed` | **`1.1955`** |
| `stability` | `0.5` |
| `similarity_boost` | `0.75` |
| `style` | **`0.0`** — Style wirkt dokumentiert auch aufs Tempo |
| `use_speaker_boost` | `true` |
| Ausgabeformat | `mp3_44100_128` |
| Gemessenes Tempo bei diesen Werten | **214,3 WPM** (Zielwert war 219) |
| Textfassung | **korrigiert** — Aussprachekorrekturen aus `aussprache.md` direkt im Sprechtext |

### Der Seed ist Pflicht, nicht Kür

Ohne festen `seed` ist die Ausgabe **nicht reproduzierbar**. Gemessen an vier
identischen Anfragen (gleiche Stimme, gleicher Text, gleiche Einstellungen):

```
186,9 · 173,1 · 163,9 · 167,8 WPM      Spanne 23,0 WPM · Standardabweichung 10,05
```

Mit `seed = 4242` liefert dieselbe Anfrage exakt dasselbe Timing — dreimal
59,304 s auf die Millisekunde. Beleg: [`stimmproben/hoerbericht.md`](stimmproben/hoerbericht.md),
Befund 3.

**Folge für die Montage:** Ohne festen Seed weicht die Laufzeit eines
Neurenderings um bis zu 23 WPM ab, und jede Einstellungslänge aus `szenen.md`
wäre hinfällig. Der Seed gehört in jede TTS-Anfrage für dieses Video.

### Warum 214,3 und nicht 219 WPM

219 WPM ist mit Eric nicht exakt einstellbar. ElevenLabs kennt keinen
WPM-Parameter, nur den relativen Faktor `speed` (0,7–1,2), und dessen Kennlinie
ist **gestuft**: Eric liefert bei `speed` 1,186 → 213,2 WPM, bei 1,1955 →
214,3 WPM und springt bei 1,2000 auf 226,8 WPM. Zwischen 214,3 und 226,8 liegt
keine erreichbare Stufe. 214,3 ist der dem Ziel nächste erreichbare Wert.

**Laufzeitfolge fürs ganze Skript:** 1.875 Wörter ÷ 214,3 WPM = **8:45**
(gegenüber 8:34 bei rechnerischen 219 WPM). Die Einstellungslängen in
`szenen.md` sind auf 219 WPM gerechnet und laufen damit **11 Sekunden zu kurz**;
das ist bei der Montage auszugleichen.

### Aussprachekorrektur: im Text, nicht über das Lexikon

Die Korrekturen aus `aussprache.md` werden **direkt in den Sprechtext**
geschrieben. Das Aussprachelexikon (PLS) wird **nicht** benutzt, weil dem
API-Schlüssel das Recht `pronunciation_dictionaries_write` fehlt.

Belegte Wirkung der Textkorrektur (aus `hoerbericht.md`, zwei Spracherkenner):

| Stelle | ohne Korrektur | mit Korrektur |
|---|---|---|
| Dümmer | fällt bei 4/4 Stimmen aus, klingt wie *dumber* | greift bei 4/4 |
| Campemoor | Mittelsilbe fehlt bei 1/4 | dreisilbig bei 4/4 |
| Widan el-Faras | Betonung falsch bei 4/4 | Betonung wandert, Ergebnis streut |
| Pr 31 | sitzt bereits bei 4/4 | unverändert — Korrektur unnötig |

**Offen:** Elf der fünfzehn Eigennamen des Skripts waren im Testtext nicht
enthalten und sind ungeprüft, ebenso alle BC-Jahreszahlen.

## Bildstil — NICHT ENTSCHIEDEN, siehe Konfliktmeldung

Der Stil ist **nicht** eintragbar, solange der Widerspruch zwischen `szenen.md`
und dem Stilarchiv nicht aufgelöst ist. Drei Dokumente nennen sich „V2" und
beschreiben drei unvereinbare Macharten. Details und offene Fragen stehen in
[`stilkonflikt.md`](stilkonflikt.md). **Bis dahin wird kein Bild generiert.**
