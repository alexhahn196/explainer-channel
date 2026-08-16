# Zweiter Stichprobenlauf — 16.08.2026, Risikofälle der Erzählfassung

> **14 Credits** (5 Motive à 2,0 plus 2 Nachläufe). 7 von 7 technisch
> erfolgreich, 0 Fehlschläge. Angesagt waren 8 Credits für vier Fälle;
> daraus wurden fünf Fälle (M68 kam dazu) und zwei Nachläufe.

## Der Befund in einem Satz

**Die Handschrift-Falle ist eine Ebene tiefer, als sie aussah.** Nicht das
Verbot war das Problem — die *Beschreibung* war es, sobald sie nach
Schreibschrift klang.

## Je Bild

### M68 — bestanden, ohne Einschränkung, und der Schlüssel zum Rest

Reine Strichgruppen in zwei Spalten, die rechte kürzer, im Entstehen.
**Kein Buchstabe, keine Ziffer, nirgends.** Das Durchlicht sitzt: die
Glasplatte ist die hellste Fläche, Blatt und Hand von unten beleuchtet,
kein Schatten nach unten.

Seine Formulierung nannte *keine* Bögen, *keine* Schleifen, *keine*
Wortlängen — nur „kurze gleichmäßige Striche, untereinander, in Zeilen
ausgerichtet, jede Eintragung eine kleine Gruppe von Strichen". Das ist
die Formulierung, die trägt.

### M33 — erst durchgefallen, im Nachlauf bestanden

Der erste Versuch beschrieb „Bögen und Schleifen", „durchgehend und
flüssig", „gruppiert zu Wortlängen". Das Ergebnis: eine volle Seite
**lesbarer englischer Handschrift**. Unter der Lupe stehen dort unter
anderem *The*, *word*, *time*, *know*, *rolling*, *learn* — und, das ist
der Kern, **`loops` und `word`, also Wörter aus meinem eigenen Prompt.**

Das ist derselbe Mechanismus wie bei Video 1, nur eine Stufe früher: dort
schrieb das Modell Promptwörter ab, weil ein Verbot ignoriert wurde; hier
schrieb es Promptwörter ab, weil die Beschreibung selbst nach Schrift
klang und die nächstliegenden Wörter die des Prompts waren.

Nach M68s Vorlage umformuliert — dichte Reihen kurzer gleich hoher
Striche in Gruppen von drei bis acht, nichts Geschwungenes, keine Ober-
und Unterlängen — kam das Blatt sauber zurück: reine Strichreihen, aus
der Entfernung als beschriebenes Papier lesbar, unter der Lupe ohne ein
einziges Zeichen.

### M51 — erst teilweise, im Nachlauf bestanden

Die **Unterschrift war von Anfang an richtig**: eine einzige durchgehende
Tintenschleife, kein abgesetztes Zeichen. Diese Formulierung blieb
unverändert.

Die Zeile darüber leckte dagegen wieder Promptwörter — lesbar sind dort
*ink*, *trace*, *word*, *run*. Nach derselben Umformulierung wie bei M33
sind es Striche.

### M28 — bestanden, ohne Einschränkung

Drei gleich breite Hochformat-Felder mit dünnen Trennlinien, ein
durchgehendes Sternfeld darüber. Die Flora stimmt in allen drei Feldern:
kahle Linden und Kastanien links, silbriges Fynbos-Buschwerk mit
Tafelberg in der Mitte, verschneite Birken mit ihrer typischen weißen
Rinde rechts. Nacht ist Nacht — der Nachtblock war nötig, ohne ihn hätte
`FARBEN` blauen Himmel versprochen.

### M44 — die geprüfte Regel besteht, drei Szenendetails nicht

**Das Licht von unten funktioniert.** Die hellen Flächen liegen auf
Kinnunterseite, Kiefer und unteren Wangen, Stirn und Oberkopf bleiben im
Schatten, alles hartkantig und flächig. Genau das hatte der erste
Stichprobenlauf ignoriert — die Formulierung über Kinn und Wangen trägt.

Nicht bestanden: der **Blick ist nicht gesenkt** (sie sieht in die
Kamera), die **Lupe fehlt**, und die Figur **liest sich nicht als Frau**
(kurzes Haar, breiter Bau). Alle drei standen als Attribut im Prompt
(„den Blick gesenkt", „eine Lupe in der Hand") — zu wenig. Sie stehen
jetzt als Bauanweisung da: Kopf nach vorn und unten geneigt, Gesicht von
schräg oben, rechte Hand hält die Lupe am Griff, Haarknoten im Nacken.
**Nicht nachgeprüft** — M44 läuft im Hauptlauf mit und wird dort geprüft.

## Was in die Regeln gewandert ist

`szenenplan.py`, Konstante `SCHRIFT`, gilt für alle sechs Motive mit
beschriebenem Papier (M19, M23, M32, M33, M51, M68):

> Auf dem Blatt stehen dichte waagerechte Reihen kurzer, gleichmäßig
> geneigter Striche von immer derselben Höhe, in kleinen Gruppen von drei
> bis acht mit schmalen Lücken dazwischen; alle Striche sind gleich lang,
> keiner ist geschwungen, keiner trägt Ober- oder Unterlänge, und keine
> Gruppe wiederholt eine andere.

**Die verallgemeinerte Lehre:** Jedes Wort der Szenenbeschreibung kann auf
dem Papier landen. Es genügt nicht, Text zu verbieten oder Schrift zu
beschreiben — die Beschreibung darf kein Vokabular verwenden, das man
nicht im Bild sehen möchte. „Bögen", „Schleifen", „Wortlängen" haben
Schreibschrift herbeigerufen; „Striche", „Gruppen", „gleiche Höhe" nicht.
