# Aussprache-QA — Video 2, „How Do We Know How Far Away the Stars Are?"

> Gemessen an der fertigen Tonspur, nicht am Gehör. Zwei Spracherkenner
> (faster-whisper `small` und `medium`) hören die Spur ab, ohne den Solltext
> zu kennen; die Fundstelle wird über die vollständige Wortausrichtung
> bestimmt. Reproduzieren: `python3 aussprache_qa.py`.
>
> **Der Unterschied zu Video 1:** dort waren vier der Korrekturen aus einem
> gemessenen Hörbericht übernommen. Hier ist **keine** vorgemessen. Diese
> Prüfung ist die erste Messung überhaupt.

## Ergebnis

**24 Stellen · 0 Fehlformen · 5 abweichend · 1 überhört**

| | small | medium |
|---|---:|---:|
| Wörter erkannt | 2.068 | 2.034 |
| deckungsgleich mit dem Solltext (2.071 Sollwörter) | 1.908 · **92,1 %** | 1.907 · **92,1 %** |

Keine einzige Stelle kam als Fehlform zurück — also nichts, was der Erkenner
als ein *anderes Wort* geschrieben hätte. Die 14 Eigennamen und 10 Zahlen
sitzen bis auf die unten aufgeführten Fälle.

## Die sechs Auffälligkeiten, und warum keine ein Aussprachefehler ist

Der Erkenner ist hier nicht die letzte Instanz. Bei einem Respelling schreibt
er, was er zu hören meint — und ein Respelling ist kein Wort seines Lexikons.
Deshalb steht neben jedem Befund die **Dauer**, und die entscheidet.

| Stelle | small | medium | Dauer | ms/Zeichen | Urteil |
|---|---|---|---:|---:|---|
| `LEV-it` (Leavitt) | „Levayet." | „Leviad." | 0,43 s | 72 | als Wort gesprochen |
| `SEF-ee-id` (Cepheid) | „SFEID" | „SfEid" | 0,60 s | 67 | als Wort gesprochen |
| `AL-fuh sen-TOR-ee` | „Alfus Centauri." | „Alphus Centauri." | 1,07 s | 63 | als Wort gesprochen |
| `maj-uh-LAN-ik` | „-olanic" | „-Atlantic" | 0,62 s | 48 | als Wort gesprochen |
| `sixty-one SIG-nye` | „61 Signei." | „61 Cygnii." (sitzt) | 1,25 s | 74 | als Wort gesprochen |
| `PLY-uh-deez` | überhört | überhört | 0,53 s | 48 | als Wort gesprochen |

### Warum die Dauer der bessere Zeuge ist

Der schwerste Verdacht war `SEF-ee-id`. Der Erkenner schrieb **„SFEID"** und
**„SfEid"** — Großbuchstaben, wie eine Abkürzung. Das nährt genau den
Verdacht, den `config.md` für die TTS ohnehin führt: dass Versalien
buchstabiert werden. Bei acht Vorkommen des Kernbegriffs wäre das ein
hörbarer Fehler durch das ganze Video.

Es ist eine Frage der Dauer, nicht der Schreibung:

* drei gesprochene Silben brauchen etwa **0,6 s**
* sieben einzeln benannte Buchstaben („S-E-F-E-E-I-D") brauchen etwa
  **1,5 bis 2 s**

Gemessen an sechs Vorkommen: **0,59 · 0,60 · 0,63 · 0,75 · 0,78 · 0,88 s.**
Die Stimme spricht es als Wort. Dasselbe gilt für alle anderen fünf Fälle —
keiner liegt über 74 ms je Zeichen, die Schwelle für buchstabiertes Lesen
liegt bei 200.

**Die verallgemeinerte Lehre:** Ein Treffer des Erkenners belegt die
Lautfolge, aber nicht die Betonung — das stand schon in Video 1. Neu ist die
Rückrichtung: **ein Fehlschlag des Erkenners belegt keinen Aussprachefehler.**
Bei Respellings braucht es ein zweites, unabhängiges Maß, und die Dauer aus
dem Zeichen-Alignment ist eines. Sie ist jetzt Teil von `aussprache_qa.py`.

## Was diese Prüfung nicht kann

* **Betonung.** Der Erkenner schreibt „Leavitt", gleich ob die erste oder die
  zweite Silbe betont war. Bei `LEV-it` gegen ein falsches „le-VIT" ist die
  Dauer gleich und die Schreibung gleich. **Nicht geprüft.**
* **Vokalqualität bei normalisierender Ausgabe.** „Gaia" wird als „Gaia"
  geschrieben, ob die Stimme „GUY-uh" oder „GAY-uh" sagt. Der Befund „sitzt"
  bei Gaia bedeutet also: kein anderes Wort, nicht: die richtige Variante.
* Beides bleibt dem Hören überlassen. Diese Datei behauptet es nicht.

## Die 24 geprüften Stellen

14 Eigennamen: Leavitt, Cepheid, Cepheids, Königsberg, Hipparcos, Gaia,
Dorpat, Vega, Pleiades, SH0ES, Alpha Centauri, Magellanic, Planck, 61 Cygni.

10 Zahlen: 1543, 1700, 0.125, 0.129, 67.4, 73.0, 67.8, 118.000, 759.000,
87.000.

**`SH0ES` war der einzige Fall mit einem harten Ja-oder-Nein.** Der Name des
Teams ist mit einer **Null** geschrieben, nicht mit einem O. Ohne Korrektur
hätte die Stimme „S-H-null-E-S" gesagt. Beide Erkenner schreiben **„Shoes"**
— die Korrektur trägt.
