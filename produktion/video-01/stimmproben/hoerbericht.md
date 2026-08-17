# Prüfbericht Stimmproben Video 1

> ## ⚠️ Das ist kein Hörbericht
>
> **Ich kann keine Audiodateien anhören.** Ich habe kein Gehör, und in dieser
> Sitzung gibt es kein Werkzeug, das mir einen Klangeindruck vermitteln könnte.
> Ein Bericht, der so täte, als hätte ich die 20 Proben gehört, wäre erfunden —
> und an dieser Entscheidung hängen 139 Einstellungen.
>
> Was stattdessen gemacht wurde: die Dateien **vermessen**. Zwei
> Spracherkenner (Whisper `small` und `medium`, lokal, 0 Credits) und eine
> Akustikanalyse (Pausen, Grundfrequenz, Pegel, Defekte). Beides sind
> Instrumentenwerte, keine Ohren.
>
> **Was das trägt:** Aussprache, Satzgrenzen, Verständlichkeit unter Tempo,
> die drei Betonungsmerkmale an der Pointe, technische Defekte. Das sind die
> Fragen mit messbaren Antworten — und es ist mehr, als ich zunächst erwartet
> hatte.
>
> **Was es nicht trägt:** ob eine Fassung „wach" oder „gehetzt" **wirkt**.
> Alter, Timbre, Register, Sympathie einer Stimme. Ob eine Aussprache „richtig
> genug" ist. Das steht in keiner Zeile dieser Datei und bleibt deinen Ohren.

**Grundlage:** 20 Proben in `elevenlabs/`, Testtext `elevenlabs/testtext.txt`
(217 Wörter), Sollwerte aus [`../aussprache.md`](../aussprache.md).
Rohdaten in `asr_ergebnis.json`, `akustik_ergebnis.json`, `auswertung.json`.

---

## 1. Tempo — Lauf A (~219 WPM) gegen Lauf B (~195 WPM)

### Bleiben Satzgrenzen hörbar? — Ja, unverändert

| Stimme | Lauf | Dauer | Pausen | Median-Pause | längste | Sprechanteil |
|---|---|---|---|---|---|---|
| Eric | A | 60,7 s | 31 | 0,52 s | 0,78 s | 74,7 % |
| Eric | B | 67,1 s | 31 | 0,50 s | 0,82 s | 76,3 % |
| Brian | A | 61,2 s | 33 | 0,39 s | 0,67 s | 79,0 % |
| Brian | B | 66,4 s | 33 | 0,41 s | 0,74 s | 79,0 % |
| Matilda | A | 59,3 s | 38 | 0,41 s | 0,73 s | 73,8 % |
| Matilda | B | 68,8 s | 41 | 0,45 s | 0,80 s | 74,4 % |
| Bella | A | 60,5 s | 34 | 0,31 s | 0,57 s | 81,3 % |
| Bella | B | 65,2 s | 35 | 0,31 s | 0,57 s | 82,3 % |

**Der Befund:** Die Pausenzahl ist zwischen A und B praktisch identisch
(Eric 31/31, Brian 33/33), die Median-Pausenlänge ebenso. Rechnet man die
absolute Pausenzeit aus, bleibt sie nahezu konstant — bei Eric 15,4 s gegen
15,9 s, obwohl die Datei 6,4 s länger ist.

**`speed` staucht die Artikulation, nicht die Pausen.** Die Satzgrenzen sind
bei 219 WPM genauso lang wie bei 195 WPM. Die schnelle Fassung verliert
strukturell nichts.

### Werden Wortenden verschluckt? — Nicht messbar mehr als bei 195

Wortfehlerrate der Erkennung gegen den Solltext. Der Erkenner ist über alle
Proben derselbe, also ist die **Differenz** zwischen A und B aussagekräftig.

| Stimme | A (~219) small | B (~195) small | A medium | B medium |
|---|---|---|---|---|
| Eric | 3,69 % | 3,69 % | 2,76 % | 2,76 % |
| Brian | 5,07 % | 5,07 % | 3,69 % | 3,69 % |
| Matilda | 4,15 % | 4,61 % | 4,15 % | 2,76 % |
| Bella | 4,15 % | 3,23 % | 2,76 % | 3,23 % |

Bei Eric und Brian ist die Fehlerrate **exakt gleich**. Bei Matilda und Bella
liegt der Unterschied bei 1–3 Wörtern von 217 und wechselt je nach Erkenner
die Richtung — das ist Rauschen, kein Effekt.

Zum Vergleich Lauf K bei `speed=1.0` (167–178 WPM): Eric 2,76 %, Brian 3,23 %,
Matilda 4,61 %, Bella 3,23 % — also **kein besserer Wert trotz deutlich
langsamerem Tempo.** Die Restfehlerquote von 3–5 % geht fast vollständig auf
die vier Eigennamen zurück, die der Erkenner ohnehin nicht kennt.

### Was das für die Szenenliste heißt

**Objektiv spricht nichts gegen 219 WPM.** Weder Satzgrenzen noch
Verständlichkeit verschlechtern sich messbar gegenüber 195 WPM. Die
Neuberechnung auf 9:37 und 139 Einstellungen wäre nach diesen Zahlen nicht
nötig.

**Was diese Zahlen nicht beantworten:** ob 219 WPM *gehetzt wirkt*. Ein
Erkenner versteht auch Sprache noch mühelos, die einem Zuhörer zu schnell ist.
Das ist genau der Punkt, an dem meine Messung endet und dein Ohr anfängt.

---

## 2. Aussprache — Lauf A (ohne) gegen Lauf C (mit Korrektur)

Gezeigt wird, was zwei Erkenner geschrieben haben, die den Sollwert **nicht
kennen**. Schreibt ein Erkenner „Dummer", wo „Dümmer" stehen soll, ist das ein
Beleg für die in `aussprache.md` benannte Fehlform.

### Dümmer — Soll: `DUEM-uh`, Notlösung `DEE-mer`, **nie** wie *dumber*

| Stimme | A ohne (small / medium) | C mit (small / medium) |
|---|---|---|
| Eric | **Dummer** / **Dömer** | Diemer / Diemer |
| Brian | **Dummer** / **Domer** | Diemer / Diemer |
| Matilda | **Dummer** / **Domer** | Diemer / Diemer |
| Bella | **Dummer** / **Domer** | Diemer / Diemer |

**Ohne Korrektur fällt der kritische Fall bei allen vier Stimmen aus** — beide
Erkenner hören durchgehend einen /ʌ/- oder /ɒ/-Vokal, also genau *dumber*.
`aussprache.md` markiert das als „darf nie stehen bleiben".

**Mit Korrektur greift die Notlösung bei allen vier**: „Diemer" heißt, der
Vokal ist auf /iː/ gewechselt. Der Lexikon-Eintrag `Deemer` tut also genau das,
wofür er gedacht war. Das ü ist damit nicht erreicht — die Notlösung ersetzt
es, sie rettet es nicht.

### Campemoor — Soll: `KAHM-puh-mohr`, dreisilbig, zweites Glied *Moor*

| Stimme | A ohne (small / medium) | C mit (small / medium) |
|---|---|---|
| Eric | Campemore / Campemore | Kampumor / Campoumour |
| Brian | Campomor / Campemour | Kampoumore / Campoumore |
| Matilda | **Campmore** / **Campmoor** | Kampumor / Campoumore |
| Bella | Campomor / Campemore | Kampoumore / Kampumor |

Das zweite Glied wird durchgehend als „-more"/„-mor" gehört, nicht als
englisches „-moor" mit /uː/ — die in `aussprache.md` benannte Fehlform tritt
also **nicht** auf.

**Ein Ausreißer: Matilda verschluckt ohne Korrektur die Mittelsilbe** —
„Campmore" und „Campmoor" sind zweisilbig, das „-pe-" fehlt. Mit Korrektur ist
es wieder da („Kampumor", „Campoumore"). Bei den anderen drei Stimmen ist die
Mittelsilbe schon ohne Korrektur vorhanden.

### Pr 31 — Soll: `P-R thirty-one`, Buchstaben einzeln

| Stimme | A ohne | C mit |
|---|---|---|
| Eric | PR 31 / PR 31 | PR 31 / PR 31 |
| Brian | PR 31 / PR 31 | PR 31 / PR 31 |
| Matilda | PR-31 / PR 31 | PR-31 / PR 31 |
| Bella | PR 31 / PR 31 | PR31 / PR 31 |

**Sitzt bei allen vier Stimmen schon ohne Korrektur.** Kein Erkenner schreibt
ein Wort wie „per" oder „pur" — die Buchstaben werden einzeln gesprochen. Die
Korrektur ändert hier **nichts**, weil nichts zu ändern war. Das ist der eine
der vier Prüfpunkte, an dem sich die Aussprachekorrektur als überflüssig
erweist.

### Widan el-Faras — Soll: `wih-DAAN el FA-rass`, Betonung 2. Silbe

| Stimme | A ohne (small / medium) | C mit (small / medium) |
|---|---|---|
| Eric | **Wieden** El Farras / **Wieden** el Fares | Wiedan El Farras / Ouidan el Faras |
| Brian | **Wieden** Elpharis / **Wieden**-El-Faris | Vidan El Farras / Vidan el Faras |
| Matilda | **Wieden** el **Ferris** / **Wieden**-el-**Ferris** | Wichdan El Farras / Wichtan el Farras |
| Bella | **Wieden** El Farris / **Wieden** el Faras | Wiedan El Faras / Wiedon el Faras |

**Ohne Korrektur fällt der schwerste Eigenname bei allen vier aus.** Beide
Erkenner schreiben durchgehend „Wieden" — das ist /ˈwiːdən/ mit Betonung auf
der **ersten** Silbe und einem Schwa in der zweiten. Soll ist „wih-DAAN":
Betonung auf der zweiten Silbe, dort ein volles /aː/.

**Mit Korrektur wandert die Betonung.** Aus „Wieden" wird „Wiedan", „Vidan",
„Ouidan", „Wichdan" — die zweite Silbe bekommt einen vollen Vokal. Das ist die
gewünschte Richtung, aber das Ergebnis streut deutlich stärker als bei Dümmer;
die Respelling-Schreibung `wih-Dahn` wird offenbar nicht von jeder Stimme
gleich gelesen.

Beim zweiten Glied ist Bella am nächsten am Soll: „Faras" bei beiden Erkennern
in Lauf C. Matilda ist am weitesten weg — „Ferris" statt „FA-rass" in beiden
Erkennern und beiden Läufen. Brian verschmilzt in Lauf A „el" mit dem Namen zu
„Elpharis".

### 3807 BC — nicht prüfbar

**Diese Stelle kommt im Testtext nicht vor.** Der Testtext ist aus vier Stellen
des Skripts montiert; die BC-Jahreszahlen stehen in Absätzen, die nicht dabei
sind. Das Alias-Lexikon deckt sie ab (10 Lesart-Regeln), geprüft ist davon
bisher keine einzige. Dasselbe gilt für Pr 7, Nebuchadnezzar, Ishtar, Susa,
Sardis, Chaco, Pueblo, Wari, Tiwanaku, Westhay und Shapwick.

### Was die Korrektur tatsächlich ändert

| Stelle | Ohne Korrektur | Mit Korrektur | Wirkung |
|---|---|---|---|
| Dümmer | fällt bei 4/4 aus | bei 4/4 auf /iː/ umgestellt | **wirkt, einheitlich** |
| Campemoor | Mittelsilbe fehlt bei 1/4 | bei 4/4 dreisilbig | **wirkt, wo nötig** |
| Pr 31 | sitzt bei 4/4 | unverändert | **ohne Wirkung, weil unnötig** |
| Widan el-Faras | Betonung falsch bei 4/4 | Betonung wandert, Ergebnis streut | **wirkt teilweise** |

---

## 3. Die Pointe

„The wheel is not the parent of the road. The wheel is a guest on it."

Drei Merkmale, jeweils gegen die eigene Grundlinie derselben Datei:
**Pause** davor gegen die Median-Pause · **Tonhöhenhub** innerhalb der Pointe
gegen den Hub im übrigen Text · **Pegel** gegen den Rest.

| Stimme | Lauf | Pause davor | Faktor | Hub-Verhältnis | Pegel | Merkmale |
|---|---|---|---|---|---|---|
| Eric | A | 0,72 s | 1,38× | 1,21× | −0,47 dB | ✓ ✓ · = 2/3 |
| Eric | B | 0,74 s | 1,48× | 1,27× | +0,14 dB | ✓ ✓ · = 2/3 |
| Brian | A | 0,39 s | **1,00×** | 1,17× | +0,49 dB | · ✓ · = 1/3 |
| Brian | B | 0,55 s | 1,34× | 1,26× | +0,14 dB | ✓ ✓ · = 2/3 |
| Matilda | A | 0,51 s | 1,23× | **0,88×** | +0,83 dB | ✓ · · = 1/3 |
| Matilda | B | 0,67 s | 1,49× | 1,10× | +0,43 dB | ✓ ✓ · = 2/3 |
| Bella | A | 0,49 s | **1,58×** | **3,21×** | −0,43 dB | ✓ ✓ · = 2/3 |
| Bella | B | 0,56 s | 1,81× | 2,66× | −1,93 dB | ✓ ✓ · = 2/3 |

**Je Stimme, Lauf A:**

- **Eric** — bekommt eine deutliche Pause (0,72 s, 38 % über seiner
  Median-Pause) und etwas mehr Tonhöhenbewegung als sonst (1,21×). Kein
  Pegelanstieg. Zwei der drei Merkmale.
- **Brian** — bekommt bei 219 WPM **gar keine zusätzliche Pause** (Faktor
  exakt 1,00×), nur leicht mehr Tonhöhenbewegung. Bei 195 WPM erscheint die
  Pause (1,34×). Von den vier Stimmen die schwächste Markierung im schnellen
  Lauf.
- **Matilda** — bekommt eine Pause, aber **weniger Tonhöhenbewegung als im
  übrigen Text** (0,88×). Die Pointe ist bei ihr melodisch flacher als ihr
  Normalsatz. Dafür der größte Pegelanstieg der vier (+0,83 dB, in Lauf C
  +1,36 dB).
- **Bella** — die deutlichste Markierung: längste relative Pause (1,58×) und
  ein Tonhöhenhub, der **mehr als das Dreifache** ihres sonstigen Hubs beträgt
  (24,5 gegen 7,7 Halbtöne). Bemerkenswert, weil Bella über den ganzen Text die
  **flachste** Stimme der vier ist (8,1 Halbtöne Gesamtspanne gegen 13,2 bei
  Eric) — sie hebt sich fast ausschließlich an der Pointe.

Der Pegel ist bei keiner Stimme ein brauchbarer Marker: alle vier bleiben
innerhalb ±2 dB.

**Läuft der Satz durch wie der Rest?** Nach diesen Zahlen: bei Bella am
klarsten nicht, bei Eric klar nicht, bei Brian im schnellen Lauf am ehesten
doch.

---

## 4. Technische Mängel

| Prüfung | Ergebnis über alle 20 Proben |
|---|---|
| Übersteuerung (Samples ≥ −0,004 dBFS) | **0** in allen 20 Dateien |
| Spitzenpegel | −1,32 bis −6,16 dBFS, überall Headroom |
| Sprungstellen / Knacken | **0** in allen 20 Dateien |
| Abriss am Dateiende | **kein Verdacht** in allen 20 Dateien |
| Auffällig lange Pausen | 8 Pausen über 0,85 s — **alle an Satzgrenzen**, siehe unten |
| Sprechdauer gegen Dateidauer | identisch — keine angehängte Auslaufstille |

**Keine Zeitmarken für Defekte zu melden — es gibt keine Fundstellen.** Die
Detektoren haben in keiner der 20 Dateien Übersteuerung, Knacken oder Abrisse
gefunden.

Die längsten Pausen, mit Zeitmarke und Kontext:

| Datei | Dauer | bei | davor / danach |
|---|---|---|---|
| `c-eric-219wpm-korrigiert` | 1,16 s | 51,42 s | „…laid as pavement." / „And in that German bog country…" |
| `k-eric-speed100` | 1,04 s | 34,41 s | „…They were fighting water." / „The same answer turns up…" |
| `k-matilda-speed100` | 0,90 s | 51,68 s | „…something else entirely." / „The quarry is called…" |
| `c-matilda-219wpm-korrigiert` | 0,86 s | 52,44 s | „…laid as pavement." / „And in that German bog country…" |

**Alle acht Pausen über 0,85 s sitzen an einem Satzende** — und überwiegend an
den drei Nahtstellen der Textmontage, also dort, wo der Testtext einen
Themensprung macht. Das sind keine unnatürlichen Pausen, sondern die Reaktion
auf die Übergänge, die ich für den Test geschrieben habe. In den Läufen A und B
liegt die längste Pause bei 0,78 s beziehungsweise 0,82 s.

**Grenze dieser Aussage:** Ein Detektor findet, wofür er gebaut ist.
Übersteuerung, Sample-Sprünge und Abrisse sind erfasst. **Nicht** erfasst sind
Artefakte, die sich nicht als Pegel- oder Stetigkeitsfehler zeigen — etwa ein
metallischer Beiklang, ein falsch gebundener Übergang oder ein Zischlaut, der
zu hart sitzt. „Keine Defekte gefunden" heißt hier **nicht** „klingt sauber".

### Kadenz — enden alle Sätze gleich?

Tonhöhenänderung in den letzten 300 ms vor jeder Pause, über alle Sätze:

| Stimme | Lauf | Sätze | Median | Streuung | Anteil fallend |
|---|---|---|---|---|---|
| Eric | A | 30 | −6,01 HT | 4,96 | 80 % |
| Brian | A | 31 | −1,77 HT | **3,78** | 87 % |
| Matilda | A | 37 | −4,20 HT | 4,39 | 89 % |
| Bella | A | 34 | −0,17 HT | **6,91** | **53 %** |

Brian hat die gleichförmigsten Satzenden (geringste Streuung, 87 % fallend),
Bella die variabelsten (größte Streuung, nur 53 % fallend — bei ihr endet fast
jeder zweite Satz steigend oder gleichbleibend). Ob geringe Streuung als
„mechanisch" gehört wird, ist eine Hörfrage; die Streuung selbst ist gemessen.

---

## Die Stimmen — soweit messbar

**Die verlangte Kurzcharakterisierung nach Alter, Ton und Register kann ich
nicht liefern.** Alter und Klangfarbe sind aus einer Messung nicht ableitbar.
Was sich objektiv angeben lässt, ist die Tonlage:

| Stimme | m/w | Grundfrequenz (Median) | Spanne p10–p90 | Einordnung der Tonlage |
|---|---|---|---|---|
| Brian | m | **86–90 Hz** | 10,7 HT | am unteren Rand des männlichen Bereichs (typisch 85–155 Hz) |
| Eric | m | 136–145 Hz | **13,2 HT** | mittlerer männlicher Bereich, größte Tonhöhenspanne der vier |
| Matilda | w | 190–206 Hz | 12,3 HT | mittlerer weiblicher Bereich |
| Bella | w | 214–219 Hz | **8,1 HT** | oberer weiblicher Bereich, kleinste Gesamtspanne — außer an der Pointe |

---

## Die zwei messbaren Ranglisten

### Wenigste Aussprachefehler

Gezählt über die drei im Testtext prüfbaren Stellen in Lauf A (ohne Korrektur),
gegen die Sollwerte aus `aussprache.md`. Dümmer und Widan el-Faras fallen bei
**allen vier** aus und trennen daher nicht.

| Stimme | Dümmer | Campemoor | Pr 31 | Widan | Abweichungen | WER (medium) |
|---|---|---|---|---|---|---|
| **Bella** | ✗ | ✓ | ✓ | ✗ | **2** | **2,76 %** |
| **Eric** | ✗ | ✓ | ✓ | ✗ | **2** | **2,76 %** |
| Brian | ✗ | ✓ | ✓ | ✗ (+„Elpharis") | 2 | 3,69 % |
| Matilda | ✗ | ✗ (Silbe fehlt) | ✓ | ✗ („Ferris") | 3 | 4,15 % |

→ **Bella und Eric.** Beide mit zwei Abweichungen und der niedrigsten
Wortfehlerrate. Brian liegt gleichauf bei der Zahl, verschmilzt aber „el" mit
dem Namen und hat die höhere Fehlerrate; Matilda hat zusätzlich die
verschluckte Mittelsilbe in Campemoor und die deutlichste Abweichung bei
Widan („Ferris").

### Tragen die Pointe am deutlichsten

Gemessen in Lauf A über Pausenfaktor und Tonhöhenhub-Verhältnis:

| Stimme | Pausenfaktor | Hub-Verhältnis |
|---|---|---|
| **Bella** | **1,58×** | **3,21×** |
| **Eric** | **1,38×** | **1,21×** |
| Brian | 1,00× | 1,17× |
| Matilda | 1,23× | 0,88× |

→ **Bella und Eric.** Bella mit Abstand am deutlichsten auf beiden Merkmalen.
Brian markiert die Pointe bei 219 WPM gar nicht durch eine Pause, Matilda
spricht sie melodisch flacher als ihren Normalsatz.

---

## Was offen bleibt

1. **Der Klangeindruck.** Alles unter „wirkt", „klingt", „passt" — nicht
   gemessen, nicht behauptet.
2. **Ob 219 WPM gehetzt wirkt.** Die Zahlen sagen: strukturell verliert die
   schnelle Fassung nichts. Ob sie sich zu schnell anhört, sagen sie nicht.
3. **Elf Eigennamen und alle BC-Jahreszahlen.** Nicht im Testtext, also
   ungeprüft — darunter Nebuchadnezzar, Tiwanaku und „3807 BC".
4. **Das Aussprachelexikon.** Läufe D und E fehlen weiterhin, dem Schlüssel
   fehlt `pronunciation_dictionaries_write`. Geprüft ist bisher nur die
   Korrektur im Text.

## Werkzeuge

| Datei | Zweck |
|---|---|
| `asr_lauf.py` | Spracherkennung, Whisper `small` + `medium`, lokal |
| `akustik.py` | Pausen, Grundfrequenz (YIN, auf 0,03 % gegengeprüft), Pegel, Defekte |
| `auswertung.py` | verbindet beides zu den vier Prüfpunkten, rechnet die Wortfehlerrate |
| `asr_ergebnis.json` · `akustik_ergebnis.json` · `auswertung.json` | Rohdaten |
