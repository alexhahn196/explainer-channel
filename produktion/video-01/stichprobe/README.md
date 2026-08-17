# Stichprobenlauf — hält der Balkenkopf über 14 Bilder?

> Lauf 2026-08-14, vor dem Produktionslauf der 84 Motive aus
> [`../szenen.md`](../szenen.md). **14 Bilder, 28 Credits**
> (`nano_banana_2`, 16:9, 2k, Preflight 2,0 Cr/Bild — Kontostand danach
> 3.039,9). Keine Videos, keine Renders.
>
> Grundlage: [`recherche/stil-uf-element/README.md`](../../../recherche/stil-uf-element/README.md)
> (V2-Machart, Element `ab1406ea-8d08-421e-a8b8-5d3ef88042cf`) und
> [`recherche/stil-unknown-frequencies.md`](../../../recherche/stil-unknown-frequencies.md).

## Antwort vorweg

**Das Element hält in 11 von 11 Figurenbildern** — der Balken ist in jeder
Ansicht da und bei 160×90 auffindbar. Aber **zwei Ansichten sind
produktionsuntauglich**, und beide betreffen Motive, die in `szenen.md` stehen:

| | Ergebnis |
|---|---|
| **Rückenansicht** (M55) | **Geht nicht.** Das Modell dreht die Figur frontal, statt sie von hinten zu zeigen. |
| **Figur klein im Bild, ohne Bildtext** (M62, M29) | **Geht so nicht.** Zwei riesige Geisterköpfe am Himmel, Komposition gespiegelt. |
| **Figur klein im Bild, mit Bildtext** (dieselbe Szene) | **Geht.** Der Text besetzt das obere Drittel — die Geisterköpfe bleiben aus. |
| alle übrigen zehn Ansichten | halten |

Und der Zusatzbefund ist ein klares Ja: **Bildtext und Balkenkopf konkurrieren
nicht.** Beide Textbilder sind fehlerfrei gesetzt.

## Was geprüft wurde

| Nr | Motiv | Schwierigkeit | Urteil |
|---|---|---|---|
| 01 | M84 | Nahaufnahme des Kopfes | **hält** — Balken formatfüllend, sauber |
| 02 | M55 | Rückenansicht | **fällt durch** — Figur frontal gedreht |
| 03 | M49 | starke Seitenansicht + Kopftuch | **hält** — Balken im Profil verkürzt, korrekt |
| 04 | M62 | Figur klein im Bild | **fällt durch** — Geisterköpfe, Spiegelkomposition |
| 05 | M78 | zwei Figuren | **hält** — beide identisch, bester Wert im Lauf |
| 06 | M75 | Bronzehelm | **hält** — Balken unter dem Helm klar sichtbar |
| 07 | M07 | kniend | **hält**, mit Vorbehalt (ein schwarzer Punkt als Auge) |
| 08 | M27 | gebückt + Regenkapuze | **hält** — Balken neigt korrekt mit dem Kopf |
| 09 | M14 | dynamische Pose + Fellkapuze | **hält**, aber **Palette bricht** |
| 10 | M30 | ohne Figur: Schema | **hält** — Palette exakt, sparsam |
| 11 | M45 | ohne Figur: Landschaft | hält, aber **zwei ungefragte Kleinfiguren** |
| 12 | M52 | ohne Figur: dichte Fläche | **hält** — Palette exakt |
| 13 | M14 + Jahreszahl | Bildtext, Kopf mittelgroß | **hält** — Text und Balken vertragen sich |
| 14 | M62 + Ortsname | Bildtext, Kopf klein | **hält** — und behebt den Fehler von 04 |

## Messwerte

Rohausgabe: [`_messwerte.txt`](_messwerte.txt) · Skript:
[`_messen.py`](_messen.py) · Miniaturen: [`_mini/`](_mini) ·
Kontaktbogen: [`_kontaktbogen-160x90.png`](_kontaktbogen-160x90.png)

### Warum halbautomatisch gemessen wurde — und was das für den Vergleich heißt

Die Messung aus `stil-uf-element/_bewertung.py` **lässt sich auf dieses Material
nicht übertragen.** Ich habe es zweimal versucht und beide Male falsche Zahlen
bekommen:

1. **Unverändert übernommen:** findet den Balken nur in 9 von 14 Bildern.
   Geneigte Balken (kniend, gebückt) fallen durch das Seitenverhältnis-Sieb der
   achsenparallelen Bounding-Box. Und weil Kopf und Papiergrund beide `#F2EDE3`
   sind, läuft die helle Fläche über Hals, Arme und Horizont hinaus — gemessene
   Kopfhöhen bis **91 % der Bildhöhe** sind das Ergebnis.
2. **Mit PCA für geneigte Balken nachgebaut:** findet Balken auch in den drei
   **figurlosen** Bildern — jede längliche Indigofläche (Bohle, Löwe,
   Wasserlauf) wird als Balken erkannt. Lagewerte über 1,0 (Balken außerhalb des
   Kopfes) im Ergebnis.

Deshalb ist die Kopfregion je Bild **von Hand gesetzt** (Tabelle `KOPF` im
Skript, relative Koordinaten, nachlesbar und reproduzierbar) und **nur der
Balken darin automatisch vermessen**. Die Kopfabgrenzung ist damit Augenmaß,
keine Messung — das begrenzt die Genauigkeit der Verhältniswerte auf schätzungs­-
weise ±5 %, und Streuungsunterschiede unterhalb dieser Schwelle sind nicht
aussagekräftig.

**Der Elementtest hat vier gleichartige Szenen gemessen, dieser Lauf elf
absichtlich verschiedene.** Die 0,13–1,4 % von dort sind deshalb kein fairer
Maßstab; der belastbare Vergleich ist die Zeile „alle vier inkl. der geneigten
Szene A" mit 12,4 / 3,8 / 12,2 %.

| Maß | Elementtest, B/C/D frontal | Elementtest, alle vier | **dieser Lauf, n = 11** |
|---|---:|---:|---:|
| Balkenbreite / Kopfbreite | 0,28 % | 12,4 % | **14,7 %** |
| Balkendicke / Kopfhöhe | 1,38 % | 3,8 % | **13,7 %** |
| Lage des Balkens im Kopf | 0,13 % | 12,2 % | **21,1 %** |

### Der überraschendste Einzelwert

Die **gedrehten und geneigten** Ansichten streuen **weniger** als die frontalen:

| Maß | aufrecht/frontal (n = 6) | Profil, kniend, gebückt (n = 5) |
|---|---:|---:|
| Balkenbreite / Kopfbreite | 16,3 % | **8,5 %** |
| Balkendicke / Kopfhöhe | 16,9 % | **7,2 %** |
| Lage des Balkens im Kopf | 27,3 % | **9,3 %** |

Das ist nicht der erwartete Befund — und er hat einen benennbaren Grund: Unter
den frontalen Bildern stecken die zwei Extremfälle des Laufs. Bei **01** füllt
der Kopf 55 % der Bildhöhe (Nahaufnahme), bei **06** beschneidet der Bronzehelm
den Kopf von oben, sodass die Lage auf 0,219 rutscht statt auf die üblichen
~0,52. Nimmt man diese beiden heraus, liegt die Lage-Streuung der frontalen
Bilder bei **1,3 %** — praktisch auf dem Niveau des Elementtests.

**Für die Produktion heißt das: Haltung ist nicht das Risiko. Bildausschnitt und
Kopfbedeckung sind es.**

## Die zwei Ausfälle im Detail

### 1. Rückenansicht (Bild 02, Motiv M55)

Angefordert war „seen from behind, walking away from the viewer". Geliefert
wurde eine Figur, deren **Beine wegführen, deren Kopf aber frontal zur Kamera
steht** — mit vollständigem Balken. Das Modell weigert sich, das Gesicht zu
verbergen, solange das Element im Prompt steht.

**Das ist kein Fehler, sondern die Bauart des Elements.** Ein Referenzbild mit
genau einer Ansicht (Front und Profil, laut Figurenblatt) hat keine
Rückenansicht, die es reproduzieren könnte.

**Empfehlung — M55 umformulieren.** Zwei Wege:

- **A (empfohlen):** Die Figur steht **seitlich am Bildrand** und blickt die
  Straße entlang, statt von hinten gezeigt zu werden. Das erhält den Bildinhalt
  („vor ihr wächst das Tor auf") und liefert eine Ansicht, die das Element kann.
  Prompt-Baustein: `<<<ID>>> stands at the left edge of the frame in profile,
  looking down the street towards the gate in the distance.`
- **B:** Die Figur weglassen und die Straße leer zeigen — die Prozession in
  Einstellung 94–95 bringt sie ohnehin zurück.

**Rückenansichten gehören generell aus der Szenenliste.** Betroffen ist nur M55;
kein weiteres der 84 Motive verlangt sie.

### 2. Figur klein im Bild ohne Bildtext (Bild 04, Motive M62 und M29)

Zwei Fehler auf einmal: **zwei überlebensgroße Köpfe schweben am Himmel**, und
die Komposition ist an der Bildmitte **gespiegelt** (zwei Fluchtpunkte, doppelte
Kakteen). Die eigentliche kleine Figur links ist korrekt — sie geht nur unter.

Die Deutung liegt nahe, ist aber **nicht belegt**: Wenn die Szene die Figur
klein verlangt, füllt das Modell den leeren oberen Bildbereich mit dem, was es
als wichtigstes Element im Prompt hat — dem Referenzkopf.

**Der Gegentest im selben Lauf stützt das.** Bild 14 hat **denselben
SCENE-Text**, nur mit der Schlagzeile `CHACO CANYON` im oberen Drittel. Ergebnis:
saubere Komposition, eine kleine Figur, keine Geisterköpfe, keine Spiegelung.

**Empfehlung:** Bei jedem Motiv, in dem die Figur unter etwa 15 % der Bildhöhe
misst, **das obere Bilddrittel belegen** — durch Bildtext (siehe unten) oder
durch einen Bildinhalt, der dort hingehört (Felskante, Horizontband, Himmel mit
Wolkenkante). Zusätzlich in den Prompt: `exactly one character in the frame, no
floating heads, no duplicated or mirrored composition.`

Betroffen sind in `szenen.md` **M62** (Einstellungen 104–105) und **M29**
(44–46, Figur als Maßstab).

## Der Zusatzversuch: Bildtext

**Beide Textbilder sind fehlerfrei.** Das ist bemerkenswert, weil unsere Prompts
bisher durchgehend `no text, no letters` enthielten und der Elementtest
ausdrücklich offenließ, ob der Balken neben einer Schlagzeile trägt.

| | Bild 13 | Bild 14 |
|---|---|---|
| Text | `3807 BC` | `CHACO CANYON` |
| Schrift | gemeißelte Antiqua, scharfe Serifen | runde Grotesk |
| Rechtschreibung | korrekt | korrekt |
| Farbe | Indigo `#1F3A5F` wie bestellt | Indigo wie bestellt |
| Versalhöhe | ~13 % der Bildhöhe (bestellt: 10 %) | ~7 % (bestellt: 10 %) |
| Position | oben links, wie bestellt | oben mittig, wie bestellt |
| Konkurrenz zum Balken | **keine** — Text links, Figur rechts | **keine** — Text oben, Figur unten links |

**Warum sie sich nicht beißen:** Text und Balken sind **dieselbe Farbe**. Statt
zu konkurrieren, lesen sie als ein System — der Balken wirkt wie ein
Schriftelement im Gesicht. Das ist ein Glücksfall der Palette, kein Verdienst
der Gestaltung, und er trägt nur, solange der Text indigo bleibt.

**Empfehlung:** Bildtext **aufnehmen**, aber sparsam. Das Vorbild fährt 1–7
Wörter bei 10,4 % Versalhöhe; für uns reichen **Jahreszahlen und Ortsnamen an
den Stationswechseln** — das wären rund zwölf der 84 Motive. Die Versalhöhe
gehört als Bruchteil der Bildhöhe in den Prompt, nicht als „large".

## Weitere Befunde, die vor dem Produktionslauf zählen

1. **Die Palette bricht bei Waldszenen.** In Bild 09 und 13 sind Baumstämme,
   Fell und Boden **braun und grau** — obwohl `No brown, no slate grey` wörtlich
   im Prompt steht. Im Kontaktbogen bei 160×90 fallen genau diese beiden Bilder
   sofort als „anderer Kanal" auf. **Das ist der schwerste Stilfehler des Laufs.**
   Gegenmittel: Braun nicht nur verbieten, sondern **ersetzen** —
   `all wood and bark rendered in warm amber #E0A93B, never brown`.
2. **Die Dichtebremse hält bei Architektur nicht.** Bild 02 (Babylon) zeigt
   zwei vollständig durchgestaltete Häuserwände statt „at most 5 distinct
   objects". Der Befund des Elementtests — Sachszenen geraten 1,5- bis
   1,7-mal dichter — bestätigt sich; die Obergrenze müsste für Architektur auf
   **N = 3** herunter, nicht auf 5.
3. **Figurlose Bilder bekommen ungefragt Figuren.** Bild 11 (Landschaft) enthält
   zwei kleine, **realistisch proportionierte** Menschen ohne Balkenkopf — ein
   Stilbruch. Für alle 47 figurlosen Motive gehört in den Prompt:
   `no people, no figures, no characters anywhere in the frame.`
4. **Ein Auge ist zurückgekehrt.** In Bild 07 sitzt ein kleiner schwarzer Punkt
   unter dem Balken. Das Figurenblatt sagt „no eyes are visible at all". Einzelfall
   in 11 Bildern, aber die Klausel gehört in jeden Prompt mit Figur.
5. **Statisten funktionieren wie gewünscht.** In Bild 03 und 06 tragen die
   Nebenfiguren teils Amber-Köpfe ohne Balken, teils den Balken — beides liest
   sauber und hält die Hauptfigur unterscheidbar. Kein Handlungsbedarf.

## Was das für die Szenenliste heißt

Vor dem Produktionslauf sind **vier Änderungen** in `szenen.md` fällig:

| Motiv | Einstellungen | Änderung |
|---|---|---|
| **M55** | 92–93 | Rückenansicht ersetzen durch Seitenansicht am Bildrand |
| **M62** | 104–105 | Bildtext `CHACO CANYON` aufnehmen (behebt die Geisterköpfe) |
| **M29** | 44–46 | oberes Bilddrittel belegen oder Figur größer setzen |
| **M14, M81** | 19–20, 134–135 | Braunverbot durch Amber-Ersatz schärfen (Waldszenen) |

Dazu drei Prompt-Bausteine für **alle** Motive: Duplikatsperre, Ersatzregel für
Braun, und für die 47 figurlosen Motive die Personensperre.

## Was dieser Lauf nicht leistet

- **Elf Bilder sind elf Datenpunkte.** Dass die Rückenansicht scheitert, ist an
  **einem** Versuch gemessen. Ein zweiter Anlauf mit anderer Formulierung könnte
  gelingen — geprüft ist das nicht.
- **Die Kopfabgrenzung ist Augenmaß.** Die Verhältniswerte tragen den Vergleich
  „hält / hält nicht", nicht eine Streuungsangabe auf zwei Nachkommastellen.
- **Keine Wiederholung je Prompt.** Ob Bild 04 bei erneutem Lauf wieder
  Geisterköpfe erzeugt oder ob es ein Einzelfall war, ist offen. Der Gegentest
  mit Text spricht für einen systematischen Zusammenhang, beweist ihn aber nicht.
- **Nicht geprüft: die zweite Ebene.** Alle 14 Bilder sind einlagig. Ob sich
  Figur und Hintergrund für die Parallax-Motive sauber getrennt generieren
  lassen, steht weiter aus — das betrifft 38 der 84 Motive.
