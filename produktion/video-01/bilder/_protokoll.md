# Prüfprotokoll Hauptlauf (Fortsetzung)

| Stapel | Motive | bestanden | durchgefallen |
|---|---|---|---|
| 1 | M02–M14 | 8/11 | M02, M09, M10 |
| 2 | M02, M09, M10, M15–M22 | 8/11 | M10, M16, M22 |
| 3 | M10, M16, M22, M23–M31 | **10/11** | M24 |

## Stapel 3 im Einzelnen

**Alle drei Nachläufe bestanden.** M10 zeigt die Marsch ohne Steg, ohne Hütte
und ohne Boot; M16 hat keine Buchstabenform mehr; M22 trägt nur noch ein
Signalobjekt. Der `KEIN_SIGNAL`-Zusatz wirkt in allen drei Fällen.

**Durchgefallen: M24** — verlangt ist der Blick *unter* die Wasseroberfläche
mit einer zweiten, älteren Bohlenlinie darunter. Geliefert ist eine Brücke von
der Seite über dem Wasser. Einzelfall, keine gemeinsame Ursache.

## Die Größenregel ist verstanden — M29 bestätigt die These

| Motiv | Vordergrund | Größenregel |
|---|---|---|
| **M08** | offene Moorfläche, keine Leitlinie | **greift** |
| M06 | Wasserlauf zieht diagonal durchs Bild | versagt |
| M62 | Straßenbett als Fluchtlinie zur Bildmitte | versagt |
| **M29** | **Grabungsschnitt als dominante Diagonale** | **versagt** |

**Befund für den Machart-Block künftiger Videos:** Die Größenangabe für eine
kleine Figur setzt sich nur durch, wenn das Bild keine dominante Leitlinie
enthält. Sobald eine Fluchtlinie, ein Weg oder ein Grabenrand durchs Bild
zieht, richtet das Modell die Figur daran aus und skaliert sie auf
Normalgröße — unabhängig davon, wie die Größenvorgabe formuliert ist (drei
Formulierungen geprüft: Bruchzahl, Beschreibung, Bildanteil).

**Konsequenz:** Wer eine kleine Figur braucht, muss den Bildaufbau ändern,
nicht den Prompt. Entweder die Leitlinie aus der Szene nehmen oder die
Figurengröße als gegeben hinnehmen.
