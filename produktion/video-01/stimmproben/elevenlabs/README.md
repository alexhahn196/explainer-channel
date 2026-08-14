# Stimmproben Video 1 — ElevenLabs

> **Stand: Vorbereitung abgeschlossen, noch keine Probe erzeugt.**
> Es fehlt der API-Schlüssel. Sobald `ELEVENLABS_API_KEY` gesetzt ist,
> erzeugt ein Aufruf sämtliche Proben und trägt die Messwerte ein:
>
> ```
> export ELEVENLABS_API_KEY=...
> python3 produktion/video-01/stimmproben/elevenlabs/proben_erzeugen.py
> ```

Dies ist der **erste und einzige Stimmentest für diesen Kanal**. Es gibt keinen
Vergleichslauf mit einem anderen Anbieter. Das Fish Audio im
[BibelTube](https://github.com/alexhahn196/BibelTube)-Repo gehört zum
Bibel-Schlafkanal und läuft dort bei **141 WPM** — ein bewusst einschläferndes
Tempo für ein 3,5-Stunden-Video. Für einen 8–15-Minuten-Erklärkanal bei ~219 WPM
ist das keine Vergleichsgröße, sondern ein anderer Anwendungsfall. Entsprechend
steht hier keine Anbieter-Gegenüberstellung, sondern eine Messung.

## Der Testtext

217 Wörter, 1.159 Zeichen — montiert aus **vier Stellen** des Sprechtexts in
[`../../skript.md`](../../skript.md), verbunden durch drei kurze Übergänge.
Erzeugt von [`testtext_bauen.py`](testtext_bauen.py), Zeile für Zeile belegt in
[`testtext_herkunft.md`](testtext_herkunft.md).

| Baustein | Wörter | Was er prüft |
|---|---|---|
| Eröffnung bis „They were fighting water." (Absatz 1) | 107 | Tempo im Fließtext, Direktansprache, und ob die Ein-Satz-Antwort als Antwort klingt |
| Dümmer / Pr 31 / Campemoor (Absatz 6) | 27 | deutsche Ortsnamen, Label ohne etablierte Sprechweise |
| Widan el-Faras (Absatz 10) | 35 | der schwerste Eigenname der Liste — arabisch, Betonung auf der zweiten Silbe |
| „The wheel is not the parent of the road." (Absatz 8) | 16 | bekommt eine Pointe Betonung? |
| *drei Übergänge* | 32 | *nicht Teil des Skripts* |

**185 der 217 Wörter stehen wörtlich so in `skript.md`.** Die 32 Wörter
Übergang sind für diesen Test geschrieben und kommen im Skript nicht vor — sie
sind in `testtext_herkunft.md` einzeln ausgewiesen, damit die Proben nicht
versehentlich für eine Vertonung des Skripts gehalten werden.

Zur Auswahl des zweiten Bausteins: Vorgegeben war „der Satz mit Pr 31 und
Campemoor". Der davorstehende Dümmer-Satz ist mitgenommen, weil „One of them"
sonst ohne Bezugswort dasteht — und weil Dümmer der in `aussprache.md`
als **kritisch** markierte Fall ist (englisch gelesen klingt er wie *dumber*).

Nicht im Testtext, aber vom Lexikon abgedeckt: Nebuchadnezzar, Ishtar, Susa,
Sardis, Chaco, Pueblo, Wari, Tiwanaku, Westhay, Shapwick, Pr 7 und sämtliche
BC-Jahreszahlen.

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
will, muss auf ein anderes Modell wechseln. Beide Varianten sind gebaut und
werden beide erzeugt, damit der Unterschied hörbar wird:

- [`lexikon_alias.pls`](lexikon_alias.pls) — **23 Regeln**: 13 Eigennamen plus
  die 10 Lesarten aus dem zweiten Tabellenblock von `aussprache.md`
  (Pr 31 → „P-R thirty-one“, 3807 BC → „thirty-eight-oh-seven B C“, 50.5 →
  „fifty point five“, BC → „B C“ …).
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

**Begründung der Wahl:** `style = 0` ist der wichtigste Punkt. Style wirkt
dokumentiert auf das Tempo, und ein Tempotest, bei dem zwei Regler gleichzeitig
auf das Tempo wirken, misst nichts Belastbares. `stability` bleibt auf der
Vorgabe 0.5, weil jede Abweichung eine Klangentscheidung wäre — und die ist
nicht meine.

**Für diesen Testlauf bewusst nicht benutzt:** `<break>`-Tags und
Großschreibung. Der vierte Baustein prüft, ob die Pointe **von sich aus**
Betonung bekommt. Wenn dort nachgeholfen wird, misst der Test die Nachhilfe und
nicht die Stimme. Für die spätere Produktion sind beide Mittel verfügbar —
`aussprache.md` verlangt an zwei Stellen ausdrücklich eine Pause (zwischen
*Susa* und *Sardis*, und vor „came" in „dressed for came"), und die ist über
`<break>` steuerbar, aber nur auf v2-Modellen.

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
   wäre eine Qualitätsentscheidung, und die ist deine. Der Testtext ist kurz
   genug, dass alle vier zusammen rund 4.700 Zeichen kosten — billiger als eine
   falsche Vorauswahl.
2. **Lauf E nutzt ein anderes Modell** (`eleven_turbo_v2` statt
   `eleven_multilingual_v2`), weil Phonem-Regeln auf dem Hauptmodell wirkungslos
   sind. Die Probe ist damit nicht direkt gegen A–D hörbar — sie beantwortet nur
   die Frage, ob IPA überhaupt greift.

## Messung und Kosten

`messungen.json` entsteht beim Lauf und enthält je Probe: Stimme, Lauf,
`speed`-Faktor, Dauer (Sprache und Datei), beide WPM-Werte, Zeichenzahl und ob
der Faktor gekappt wurde. Dazu der Tarif und der Zeichenstand **vor und nach**
dem Lauf, aus `/v1/user/subscription` — die abgerechnete Zahl kommt also vom
Konto, nicht aus meiner Schätzung.

| | |
|---|---|
| Abrechnungseinheit | Zeichen |
| Erwarteter Verbrauch | **~20.900 Zeichen** (18 Proben) |
| Tarif | *wird beim Lauf ausgelesen* |
| Tatsächlich abgerechnet | *wird beim Lauf ausgelesen* |

## Dateien

| Datei | Zweck |
|---|---|
| `testtext_bauen.py` | montiert den Testtext aus vier Skriptstellen |
| `testtext.txt` | der Testtext, 217 Wörter |
| `testtext_korrigiert.txt` | derselbe Text mit 4 Ersatzschreibungen |
| `testtext_herkunft.md` | Herkunftsnachweis je Baustein |
| `lexikon_bauen.py` | baut beide PLS-Dateien aus `aussprache.md` |
| `lexikon_alias.pls` / `lexikon_phoneme.pls` | die Aussprachelexika |
| `proben_erzeugen.py` | erzeugt alle Proben, misst Tempo, schreibt `messungen.json` |
| `messungen.json` | Messwerte, Zeichenverbrauch, Tarifstand — *entsteht beim Lauf* |

## Quellen

- [Text to Speech — Modelle und Einstellungen](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [Using pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries)
- [Create a pronunciation dictionary from a file](https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-file)
- [Prompting controls — Pausen, Betonung, Tempo](https://elevenlabs.io/docs/best-practices/prompting/controls)
- [POST /v1/text-to-speech/{voice_id}](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
