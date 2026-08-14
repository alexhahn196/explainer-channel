# Stimmproben Video 1 — ElevenLabs

> **Stand: Vorbereitung abgeschlossen, noch keine Probe erzeugt.**
> Es fehlt der API-Schlüssel. Sobald `ELEVENLABS_API_KEY` gesetzt ist,
> erzeugt ein Aufruf sämtliche Proben und trägt die Messwerte ein:
>
> ```
> export ELEVENLABS_API_KEY=...
> python3 produktion/video-01/stimmproben/elevenlabs/proben_erzeugen.py
> ```

## Was hier getestet wird

Testtext ist **Absatz 6** des Sprechtexts aus [`../../skript.md`](../../skript.md)
— 205 Wörter, 1.076 Zeichen. Der Absatz wurde gewählt, weil er die dichteste
Häufung von Stolperstellen aus [`../../aussprache.md`](../../aussprache.md)
enthält: **Dümmer** (der als kritisch markierte Fall — englisch gelesen klingt
er wie *dumber*), **Campemoor** und das Label **Pr 31**.

**Was dieser Ausschnitt nicht abdeckt:** die übrigen zehn Eigennamen der
Ausspracheliste (Widan el-Faras, Nebuchadnezzar, Ishtar, Susa, Sardis, Chaco,
Pueblo, Wari, Tiwanaku, Westhay, Shapwick), das zweite Label Pr 7 und sämtliche
BC-Jahreszahlen — die stehen in anderen Absätzen. Das Aussprachelexikon deckt
sie trotzdem vollständig ab (23 Regeln), geprüft werden können sie an diesem
Ausschnitt aber nicht.

## Die zwei Fragen zu ElevenLabs

### 1. Gibt es eine Wörterbuch-Funktion? — Ja

ElevenLabs hat **Pronunciation Dictionaries** im PLS-Format (Pronunciation
Lexicon Specification, ein W3C-XML-Format). Sie werden einmal hochgeladen und
danach je Anfrage über `pronunciation_dictionary_locators` angehängt (maximal
drei gleichzeitig).

Es gibt **zwei Regelarten**, und der Unterschied ist folgenreich:

| Regelart | Was drinsteht | Welche Modelle werten sie aus |
|---|---|---|
| `<phoneme>` | Lautschrift, `alphabet="ipa"` oder `"cmu"` | **nur Flash v2 / Turbo v2** (und v3 für nicht-englische Lautschrift). Andere Modelle **überspringen sie stillschweigend**. |
| `<alias>` | Ersatzschreibung, also normaler Text | **alle** Modelle |

Das heißt: Auf `eleven_multilingual_v2` — dem Modell, das die Dokumentation als
das für Langform stabilste führt — wirken **nur Alias-Regeln**. Wer IPA nutzen
will, muss auf ein anderes Modell wechseln. Beide Varianten sind hier gebaut und
werden beide erzeugt, damit der Unterschied hörbar wird:

- [`lexikon_alias.pls`](lexikon_alias.pls) — **23 Regeln**: 13 Eigennamen plus
  die 10 Lesarten aus dem zweiten Tabellenblock von `aussprache.md`
  (Pr 31 → „P-R thirty-one", 3807 BC → „thirty-eight-oh-seven B C", 50.5 →
  „fifty point five", BC → „B C" …).
- [`lexikon_phoneme.pls`](lexikon_phoneme.pls) — **13 Regeln** in IPA, direkt
  aus der IPA-Spalte von `aussprache.md`.

Beide werden von [`lexikon_bauen.py`](lexikon_bauen.py) aus der Tabelle in
`aussprache.md` erzeugt, sind also nachvollziehbar und bei Änderungen an der
Ausspracheliste neu baubar.

**Ein Fall ist nicht sauber abbildbar:** „Dümmer". `aussprache.md` empfiehlt
*DUEM-uh* mit gerundetem ü und nennt `/ˈdiːmər/` („DEE-mer") ausdrücklich als
Notlösung, falls das TTS das ü nicht trifft. Eine Alias-Regel muss englische
Orthographie sein — ein ü ist darin nicht schreibbar. Das Alias-Lexikon nutzt
deshalb die dokumentierte Notlösung `Deemer`. Nur das Phonem-Lexikon kann
`/ˈdʏmɐ/` überhaupt transportieren, und das nur auf einem der beiden
Phonem-Modelle. Ob das Modell das ü dann trägt, ist eine Hörfrage.

### 2. Welche Einstellungen beeinflussen Betonung und Tempo

| Einstellung | Bereich | Wirkung | Hier gewählt |
|---|---|---|---|
| `speed` | 0.7–1.2, Vorgabe 1.0 | **Der einzige Tempo-Regler.** Relativer Faktor auf das natürliche Tempo der Stimme, kein WPM-Wert. | **wird je Stimme berechnet**, siehe unten |
| `stability` | 0–1, Vorgabe 0.5 | niedrig = mehr Variation in Betonung und Emotion, hoch = gleichförmiger | **0.5** |
| `style` | 0–1, Vorgabe 0 | Überzeichnung des Sprechstils; verändert Betonung **und Tempo** mit | **0.0** — damit `speed` der einzige Tempo-Einfluss bleibt |
| `similarity_boost` | 0–1, Vorgabe 0.75 | Nähe zur Originalstimme | **0.75** |
| `use_speaker_boost` | an/aus, Vorgabe an | Verstärkung der Stimmähnlichkeit | **an** |
| `model_id` | — | bestimmt Ausdrucksbreite, Zeichenlimit und Lexikon-Unterstützung | **`eleven_multilingual_v2`** |

Dazu kommen **Einflüsse im Text selbst**, die kein Parameter sind:

- `<break time="1.0s" />` — Pause, maximal 3 s, **nur v2-Modelle**, laut
  Dokumentation bei häufigem Einsatz instabil.
- Auslassungspunkte (`…`) erzeugen Zögern, Gedankenstriche kurze Pausen.
- **Großschreibung** verstärkt die Betonung eines Worts („a VERY long day").
- Nur `eleven_v3`: Audio-Tags wie `[whispers]`, `[excited]`.

Das ist unmittelbar relevant für zwei Vorgaben aus `aussprache.md`: die Pause
zwischen *Susa* und *Sardis* und die Betonung auf „for" mit anschließender Pause
in „dressed for came". Beides ist über `<break>` und Großschreibung steuerbar —
aber nur auf v2-Modellen.

**Begründung der Wahl:** `style = 0` ist der wichtigste Punkt. Style wirkt
dokumentiert auf das Tempo, und ein Tempotest, bei dem zwei Regler gleichzeitig
auf das Tempo wirken, misst nichts Belastbares. `stability` bleibt auf der
Vorgabe 0.5, weil jede Abweichung eine Klangentscheidung wäre — und die ist
nicht meine.

### Warum kalibriert werden muss

ElevenLabs kennt **keinen WPM-Parameter**. `speed` ist ein relativer Faktor auf
das natürliche Tempo der jeweiligen Stimme, und das ist von Stimme zu Stimme
verschieden. „219 WPM" lässt sich also nicht einstellen, sondern nur treffen:

1. **Lauf K** — jede Stimme bei `speed = 1.0`, Tempo messen.
2. `speed = 219 / gemessenes Tempo`, gekappt auf 0.7–1.2.
3. **Lauf A/B** — mit diesem Faktor erzeugen und **erneut messen**.

Berichtet wird die gemessene Zahl, nicht die angepeilte. Wo der Faktor an die
Grenze 0.7/1.2 stößt, ist das Zieltempo mit dieser Stimme nicht erreichbar; die
Messtabelle markiert solche Fälle.

Gemessen wird doppelt, weil sich beide Werte systematisch unterscheiden:
`wpm_sprache` aus dem Zeichen-Alignment der API (Ende des letzten gesprochenen
Zeichens, ohne Auslaufstille) und `wpm_datei` aus der MP3-Länge (mit).

## Die Proben

Stimmen: zwei männliche, zwei weibliche. Ausgewählt nach den Labels der
ElevenLabs-Standardstimmen — Akzent `american` (Zielmarkt US laut Repo-README)
und Verwendungszweck `informative_educational` beziehungsweise erzählnah. **Das
ist eine Auswahl nach Katalogangaben, keine Klangbewertung.**

| Datei | Lauf | Stimme | Ziel-Tempo | Aussprachekorrektur |
|---|---|---|---|---|
| `k-<stimme>-speed100.mp3` | K | alle vier | — (Kalibrierung) | keine |
| `a-<stimme>-219wpm.mp3` | A | alle vier | ~219 WPM | keine |
| `b-<stimme>-195wpm.mp3` | B | alle vier | ~195 WPM | keine |
| `c-<stimme>-219wpm-korrigiert.mp3` | C | alle vier | ~219 WPM | Respelling im Text |
| `d-<stimme>-219wpm-lexikon-alias.mp3` | D | eine | ~219 WPM | Alias-Lexikon |
| `e-<stimme>-219wpm-lexikon-phoneme.mp3` | E | eine | ~219 WPM | Phonem-Lexikon (`eleven_turbo_v2`) |

**Zwei Abweichungen vom Auftrag, beide bewusst:**

1. **Lauf C läuft über alle vier Stimmen, nicht nur über „die beste".** „Beste"
   wäre eine Qualitätsentscheidung, und die ist ausdrücklich deine. Der Absatz
   ist kurz genug, dass alle vier zusammen rund 4.400 Zeichen kosten — billiger
   als eine falsche Vorauswahl.
2. **Lauf E nutzt ein anderes Modell** (`eleven_turbo_v2` statt
   `eleven_multilingual_v2`), weil Phonem-Regeln auf dem Hauptmodell wirkungslos
   sind. Die Probe ist damit nicht direkt gegen A–D hörbar — sie beantwortet nur
   die Frage, ob IPA überhaupt greift.

**Die Dateibenennung ist vorläufig.** Sie folgt dem Schema *Lauf – Stimme –
Tempo – Korrektur*; sobald die Benennung aus Test 1 vorliegt, wird sie darauf
umgestellt.

## Gegenüberstellung der Anbieter

| | Anbieter 1 | ElevenLabs |
|---|---|---|
| Anbieter / Modell | *nachzutragen* | `eleven_multilingual_v2` (Lauf E: `eleven_turbo_v2`) |
| Stimmen (m) | *nachzutragen* | Eric, Brian |
| Stimmen (w) | *nachzutragen* | Matilda, Bella |
| Tempo-Regler | *nachzutragen* | `speed` 0.7–1.2, relativ — kein WPM-Wert |
| Gemessenes Tempo, Lauf A | *nachzutragen* | *offen bis zum Lauf* |
| Gemessenes Tempo, Lauf B | *nachzutragen* | *offen bis zum Lauf* |
| Aussprachelexikon | *nachzutragen* | ja, PLS; Phonem nur auf Flash/Turbo v2 |
| Abrechnungseinheit | *nachzutragen* | Zeichen |
| Kosten dieses Tests | *nachzutragen* | *offen bis zum Lauf* |
| Tarif | *nachzutragen* | *wird aus `/v1/user/subscription` gelesen* |

Die Werte für Anbieter 1 liegen in diesem Repository nicht vor — es gibt weder
Proben noch eine README aus Test 1 in irgendeinem Zweig. Sie werden nachgereicht
und dann hier eingetragen.

## Dateien

| Datei | Zweck |
|---|---|
| `testtext.txt` | Absatz 6, unverändert aus `skript.md`, ohne Quellen-IDs |
| `testtext_korrigiert.txt` | derselbe Absatz mit 3 Ersatzschreibungen (Dümmer, Campemoor, Pr 31) |
| `lexikon_bauen.py` | baut beide PLS-Dateien aus `aussprache.md` |
| `lexikon_alias.pls` / `lexikon_phoneme.pls` | die Aussprachelexika |
| `proben_erzeugen.py` | erzeugt alle Proben, misst Tempo, schreibt `messungen.json` |
| `messungen.json` | Messwerte je Probe, Zeichenverbrauch, Tarifstand — *entsteht beim Lauf* |

## Quellen

- [Text to Speech — Modelle und Einstellungen](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [Using pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries)
- [Create a pronunciation dictionary from a file](https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-file)
- [Prompting controls — Pausen, Betonung, Tempo](https://elevenlabs.io/docs/best-practices/prompting/controls)
- [POST /v1/text-to-speech/{voice_id}](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
