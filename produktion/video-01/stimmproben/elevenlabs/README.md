# Stimmproben Video 1 — ElevenLabs

> **Stand: 20 Proben erzeugt und vermessen.** Was fehlt: die beiden
> Lexikon-Proben (Lauf D/E) — der Schlüssel hat die dafür nötige Berechtigung
> nicht. Siehe [„Was nicht lief"](#was-nicht-lief).
>
> Reproduzieren:
> ```
> export ELEVENLABS_API_KEY=...
> python3 produktion/video-01/stimmproben/elevenlabs/proben_erzeugen.py
> ```
> Alle Anfragen laufen mit festem `seed=4242` — ohne den ist nichts davon
> reproduzierbar, siehe Befund 3.

Dies ist der **erste und einzige Stimmentest für diesen Kanal**. Es gibt keinen
Vergleichslauf mit einem anderen Anbieter. Das Fish Audio im
[BibelTube](https://github.com/alexhahn196/BibelTube)-Repo gehört zum
Bibel-Schlafkanal und läuft dort bei **141 WPM** — ein bewusst einschläferndes
Tempo für ein 3,5-Stunden-Video. Für einen 8–15-Minuten-Erklärkanal bei ~219 WPM
ist das keine Vergleichsgröße, sondern ein anderer Anwendungsfall.

**Keine Klangbewertung in dieser Datei.** Hier stehen ausschließlich gemessene
Zahlen und technische Befunde. Ob „Dümmer" richtig klingt, ob die Pointe sitzt
und welche Stimme taugt — das entscheidet das Hören. Die Abnahmeliste dafür
steht in [`../../aussprache.md`](../../aussprache.md).

## Ergebnis

Gemessen am fertigen Audio, nicht angepeilt. `WPM` = Wörter ÷ Sprechdauer,
Sprechdauer aus dem Zeichen-Alignment der API (ohne Auslaufstille).

### Lauf A — Ziel ~219 WPM · Lauf B — etwas langsamer, Ziel ~195 WPM

| Stimme | m/w | Lauf A | Abw. | `speed` | Lauf B | Abw. | `speed` |
|---|---|---|---|---|---|---|---|
| Eric | m | **214,3** | −4,7 | 1,1955 | **194,2** | −0,8 | 1,1210 |
| Brian | m | **212,9** | −6,1 | 1,1970 | **196,2** | +1,2 | 1,1320 |
| Matilda | w | **219,5** | +0,5 | 1,2000 | **189,2** | −5,8 | 1,1390 |
| Bella | w | **215,2** | −3,8 | 1,1690 | **199,5** | +4,5 | 1,1160 |

Vier der acht Werte liegen 3,8–6,1 WPM neben dem Ziel. Das ist **kein
Kalibrierfehler, sondern eine Eigenschaft des Parameters** — siehe Befund 4.

### Lauf K — Kennlinie je Stimme

| Stimme | `speed`=1,0 | `speed`=1,2 | Faktor |
|---|---|---|---|
| Eric | 177,2 | 226,8 | 1,280 |
| Brian | 174,1 | 224,6 | 1,290 |
| Matilda | 167,1 | 219,5 | 1,314 |
| Bella | 177,6 | 230,7 | 1,299 |

### Lauf C — mit Aussprachekorrektur im Text

Vier Ersetzungen: `Dümmer→Deemer`, `Pr 31→P-R thirty-one`,
`Campemoor→Kahm-puh-mohr`, `Widan el-Faras→wih-Dahn el Fah-rass`.

| Stimme | WPM | `speed` |
|---|---|---|
| Eric | 221,5 | 1,1920 |
| Brian | 210,7 | 1,1970 |
| Matilda | 219,6 | 1,2000 |
| Bella | 222,5 | 1,1690 |

Lauf C lief mit dem `speed`-Wert, den Lauf A zum Zeitpunkt der Erzeugung hatte;
bei Eric wurde Lauf A danach noch auf 1,1955 nachgezogen. Die Differenz
entspricht rund 1,3 WPM und ist für den Aussprachevergleich ohne Belang.

## Technische Befunde

**1. Es gibt keinen WPM-Parameter.** Nur `speed`, einen relativen Faktor von
0,7 bis 1,2 auf das natürliche Tempo der jeweiligen Stimme. Ein Zieltempo lässt
sich nicht einstellen, nur durch Messen und Nachstellen annähern.

**2. 219 WPM liegt am oberen Rand des Machbaren.** Die vier Stimmen sprechen von
sich aus 167–178 WPM. Für ~219 WPM braucht es `speed` zwischen 1,17 und 1,20 —
also fast oder genau den Anschlag. **Nach oben ist praktisch kein Spielraum:**
Matilda erreicht 219,5 WPM erst bei exakt `speed=1.2` und kann nicht schneller.
Wenn das Skript später schneller laufen soll als 219 WPM, geht das mit diesen
Stimmen nicht über den Parameter.

**3. Ohne `seed` ist die Ausgabe nicht reproduzierbar.** Vier identische
Anfragen (gleiche Stimme, gleicher Text, `speed=1.0`) ergaben:

```
186,9 · 173,1 · 163,9 · 167,8 WPM     Spanne 23,0 · Standardabweichung 10,05
```

Mit festem `seed` liefert dieselbe Anfrage exakt dasselbe Tempo — dreimal
59,304 s auf die Millisekunde. Die MP3-Bytes unterscheiden sich trotzdem,
das Timing nicht. **Folge: Jede Tempomessung ohne Seed misst Rauschen.** Die
ersten beiden Läufe dieses Tests waren aus genau diesem Grund unbrauchbar und
wurden verworfen.

**4. Die Kennlinie ist gestuft, nicht glatt.** `speed` wirkt weder linear noch
stetig:

| Beobachtung | Messung |
|---|---|
| nicht linear | `speed`=1,2 liefert das 1,28- bis 1,31-fache Tempo, nicht das 1,2-fache |
| Plateaus | Brian: `speed`=1,1970 und 1,1986 → **beide exakt 212,9 WPM** |
| | Bella: `speed`=1,1160 und 1,1114 → **beide exakt 199,5 WPM** |
| Sprünge | Matilda: `speed`=1,1999 → 205,2 WPM · `speed`=1,2000 → **219,5 WPM** |

Der letzte Fall ist der deutlichste: **0,0001 Parameterunterschied, 14,3 WPM
Sprung.** Die erreichbaren Tempi sind damit eine diskrete Menge. Ein Zielwert,
der zwischen zwei Stufen liegt, ist mit dieser Stimme nicht erreichbar — und
keine Iteration ändert das. Deshalb bleiben vier der acht Proben 3,8–6,1 WPM
neben dem Ziel.

Praktische Folge für die Pipeline: `speed` sollte auf zwei Nachkommastellen
gesetzt und der Anschlag exakt getroffen werden. Ein per Interpolation knapp
verfehltes 1,2 landet auf der darunterliegenden Stufe.

**5. Aussprachelexika kennen zwei Regelarten mit unterschiedlicher
Modellabdeckung.**

| Regelart | Inhalt | Modelle |
|---|---|---|
| `<phoneme>` | IPA oder CMU | **nur Flash v2 / Turbo v2** (und v3 für nicht-englische Lautschrift); andere überspringen sie stillschweigend |
| `<alias>` | Ersatzschreibung | **alle** |

Auf `eleven_multilingual_v2` — laut Doku das für Langform stabilste Modell —
wirken also **nur Alias-Regeln**. Wer IPA will, muss das Modell wechseln.

**6. „Dümmer" ist als Alias-Regel nicht sauber abbildbar.** `aussprache.md`
empfiehlt *DUEM-uh* mit gerundetem ü und nennt `/ˈdiːmər/` als Notlösung. Eine
Alias-Regel muss englische Orthographie sein — ein ü ist darin nicht
schreibbar. Das Lexikon nutzt deshalb `Deemer`. Nur die Phonem-Regel könnte
`/ˈdʏmɐ/` transportieren, und die nur auf Flash/Turbo v2.

**7. Die Zeichen-Alignment-Antwort ist für die SRT-Erzeugung brauchbar.** Der
Endpunkt `/with-timestamps` liefert Start- und Endzeit **je Zeichen**. Das ist
genauer als alles, was `produktion/pipeline/schritt6_srt.py` heute macht, und
wäre beim Umbau der Pipeline zu prüfen.

**8. Nebenbefunde.** Die Antwort-Header nennen ein Limit von **5 gleichzeitigen
Anfragen** (`maximum-concurrent-requests`) — `tts_parallel = 12` aus
`produktion/config.md` ist für ElevenLabs also zu hoch. Sprechdauer und
Dateidauer sind bei allen 20 Proben identisch, das Modell hängt keine
Auslaufstille an.

## Gewählte Einstellungen

| Einstellung | Wert | Warum |
|---|---|---|
| `model_id` | `eleven_multilingual_v2` | laut Doku am stabilsten für Langform |
| `speed` | je Stimme, siehe Tabellen | einziger Tempo-Regler |
| `stability` | 0,5 (Vorgabe) | jede Abweichung wäre eine Klangentscheidung — die ist nicht meine |
| `style` | **0,0** | Style wirkt dokumentiert **auch aufs Tempo**; bei zwei Tempo-Reglern misst der Test nichts Belastbares |
| `similarity_boost` | 0,75 (Vorgabe) | — |
| `use_speaker_boost` | an (Vorgabe) | — |
| `seed` | **4242** | ohne ihn keine Reproduzierbarkeit, siehe Befund 3 |
| `output_format` | `mp3_44100_128` | — |

**Bewusst nicht benutzt:** `<break>`-Tags und Großschreibung. Beide steuern
Pausen und Betonung. Der vierte Baustein des Testtexts prüft, ob die Pointe
**von sich aus** Betonung bekommt — mit Nachhilfe misst er die Nachhilfe. Für
die Produktion stehen beide bereit; `aussprache.md` verlangt an zwei Stellen
ausdrücklich eine Pause (zwischen *Susa* und *Sardis*, und vor „came" in
„dressed for came"), und die geht über `<break>`, aber nur auf v2-Modellen.

## Der Testtext

217 Wörter, 1.159 Zeichen — montiert aus **vier Stellen** des Sprechtexts in
[`../../skript.md`](../../skript.md), verbunden durch drei kurze Übergänge.
Erzeugt von [`testtext_bauen.py`](testtext_bauen.py), Zeile für Zeile belegt in
[`testtext_herkunft.md`](testtext_herkunft.md).

| Baustein | Wörter | Was er prüft |
|---|---|---|
| Eröffnung bis „They were fighting water." (Absatz 1) | 107 | Tempo im Fließtext, Direktansprache, ob die Ein-Satz-Antwort als Antwort klingt |
| Dümmer / Pr 31 / Campemoor (Absatz 6) | 27 | deutsche Ortsnamen, Label ohne etablierte Sprechweise |
| Widan el-Faras (Absatz 10) | 35 | schwerster Eigenname — arabisch, Betonung auf der zweiten Silbe |
| „The wheel is not the parent of the road." (Absatz 8) | 16 | bekommt eine Pointe Betonung? |
| *drei Übergänge* | 32 | *nicht Teil des Skripts* |

**185 der 217 Wörter stehen wörtlich so in `skript.md`.** Die 32 Wörter
Übergang sind für diesen Test geschrieben — sie sind in `testtext_herkunft.md`
einzeln ausgewiesen, damit die Proben nicht für eine Vertonung des Skripts
gehalten werden.

Der Dümmer-Satz ist über die Vorgabe hinaus mitgenommen, weil „One of them"
sonst ohne Bezugswort dasteht und Dümmer der in `aussprache.md` als **kritisch**
markierte Fall ist.

Nicht im Testtext, aber vom Lexikon abgedeckt: Nebuchadnezzar, Ishtar, Susa,
Sardis, Chaco, Pueblo, Wari, Tiwanaku, Westhay, Shapwick, Pr 7 und sämtliche
BC-Jahreszahlen.

## Die Stimmen

Zwei männliche, zwei weibliche, ausgewählt nach den Katalog-Labels der
ElevenLabs-Standardstimmen: Akzent `american` (Zielmarkt US laut Repo-README)
und Verwendungszweck `informative_educational` beziehungsweise erzählnah.
**Auswahl nach Katalogangaben, keine Klangbewertung.**

| Stimme | m/w | `voice_id` | Katalog-Label |
|---|---|---|---|
| Eric | m | `cjVigY5qzO86Huf0OWal` | Smooth, Trustworthy · conversational |
| Brian | m | `nPczCjzI2devNBz1zQrb` | Deep, Resonant, Comforting |
| Matilda | w | `XrExE9yKIg1WjnnlVkGX` | Knowledgable, Professional · informative_educational |
| Bella | w | `hpp4J3VqNfWAUOO0d1Us` | Professional, Bright, Warm · informative_educational |

Lauf C läuft über **alle vier** Stimmen statt nur über „die beste" — welche die
beste ist, entscheidet das Hören.

## Was nicht lief

**Lauf D/E — die Lexikon-Proben fehlen.** Der übergebene Schlüssel kann
ausschließlich Text-to-Speech. Geprüft:

| Endpunkt | Ergebnis |
|---|---|
| `POST /v1/text-to-speech/…` | **200 — funktioniert** |
| `GET /v1/user/subscription` | 401 · fehlendes Recht `user_read` |
| `GET /v1/voices` | 401 · fehlendes Recht `voices_read` |
| `GET /v1/models` | 401 · fehlendes Recht `models_read` |
| `GET /v1/pronunciation-dictionaries` | 401 · fehlendes Recht `pronunciation_dictionaries_read` |
| `POST /v1/pronunciation-dictionaries/add-from-file` | 401 · fehlendes Recht `pronunciation_dictionaries_write` |

Umgangen: Die `voice_id`s stammen aus dem **öffentlichen** Katalog
(`/v1/voices` ohne Schlüssel) und stehen fest im Skript.

Nicht umgehbar: Ohne `pronunciation_dictionaries_write` lässt sich kein Lexikon
anlegen. Beide PLS-Dateien sind fertig gebaut und geprüft; sobald der Schlüssel
das Recht hat, erzeugt derselbe Skriptaufruf die fehlenden zwei Proben.

**Die Aussprachekorrektur ist trotzdem getestet** — über Lauf C, der die
Ersetzungen direkt im Text vornimmt. Was das Lexikon zusätzlich brächte: Die
Korrektur läge einmal zentral statt in jedem Skript, und die Schreibung im
Sprechtext bliebe unangetastet — was `aussprache.md` ausdrücklich verlangt
(„nicht die Schreibung im Skript phonetisch verfälschen, sonst bricht der
Abgleich mit `faktencheck.py`").

## Kosten

Abgerechnet wird in **Zeichen**. Der Tarif ließ sich nicht auslesen
(`user_read` fehlt), die Zahlen sind daher selbst gezählt, nicht vom Konto:

| Posten | Zeichen |
|---|---|
| Die 20 erhaltenen Proben samt ihrer Annäherungsschritte | 44.137 |
| Verworfener Lauf 1 (ohne Seed, Messungen unbrauchbar) | 18.620 |
| Verworfener Lauf 2 (ohne Seed) | 31.369 |
| Streuungsmessung ohne/mit Seed (Befund 3) | 8.113 |
| Nachprüfung der Seed-Reproduzierbarkeit (Befund 4) | 3.477 |
| **Gesamt an die API gesendet** | **105.716** |

Der hohe Anteil verworfener Läufe geht auf Befund 3 zurück: Ohne Seed war nicht
erkennbar, dass die Messungen Rauschen waren. Ein Wiederholungslauf mit dem
jetzigen Stand kostet **44.137 Zeichen**, ein Lauf ohne die Annäherungsschritte
(feste `speed`-Werte aus der Ergebnistabelle) rund **23.200**.

## Dateien

| Datei | Zweck |
|---|---|
| `k-<stimme>-speed100.mp3`, `…-speed120.mp3` | Lauf K — Kennlinie, 8 Dateien |
| `a-<stimme>-219wpm.mp3` | Lauf A — ~219 WPM, 4 Dateien |
| `b-<stimme>-195wpm.mp3` | Lauf B — ~195 WPM, 4 Dateien |
| `c-<stimme>-219wpm-korrigiert.mp3` | Lauf C — mit Aussprachekorrektur, 4 Dateien |
| `messungen.json` | alle Messwerte, Annäherungsverlauf, Zeichenverbrauch |
| `testtext_bauen.py` | montiert den Testtext aus vier Skriptstellen |
| `testtext.txt` / `testtext_korrigiert.txt` | der Testtext, roh und korrigiert |
| `testtext_herkunft.md` | Herkunftsnachweis je Baustein |
| `lexikon_bauen.py` | baut beide PLS-Dateien aus `aussprache.md` |
| `lexikon_alias.pls` (23 Regeln) / `lexikon_phoneme.pls` (13 Regeln) | die Aussprachelexika — gebaut, noch nicht hochgeladen |
| `proben_erzeugen.py` | erzeugt alle Proben, misst Tempo, schreibt `messungen.json` |

## Quellen

- [Text to Speech — Modelle und Einstellungen](https://elevenlabs.io/docs/capabilities/text-to-speech)
- [Using pronunciation dictionaries](https://elevenlabs.io/docs/eleven-api/guides/how-to/text-to-speech/pronunciation-dictionaries)
- [Create a pronunciation dictionary from a file](https://elevenlabs.io/docs/api-reference/pronunciation-dictionaries/create-from-file)
- [Prompting controls — Pausen, Betonung, Tempo](https://elevenlabs.io/docs/best-practices/prompting/controls)
- [POST /v1/text-to-speech/{voice_id}](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
