# Zustandspaar-Probe und Umbau des Anweisungsteils — 16.08.2026

> **6 Credits** (drei Bilder à 2,0): zwei Bild-zu-Bild-Versuche für M05, ein
> Neulauf für M01. Die beiden Montagen kosten nichts. Kontostand 2.573,9.
> Von 236 Credits der Variante C sind 30 verbraucht.

## 1. Bild zu Bild: die Machart bleibt, der bewegte Gegenstand nicht

Die Frage war: bleibt die Machart erhalten, und ist es wirklich dasselbe
Bild mit einer Änderung — oder nur ein ähnliches?

**Die Machart bleibt vollständig.** Strichstärke, flache Füllung, Palette,
harte Schatten — nichts davon rutscht. Das ist der klare Gewinn gegenüber
dem Textweg.

**Der Hintergrund bleibt bitgleich, wo ihn nichts verdeckt.** Gemessen an
M04: im Spaltenband, in dem der Haken sitzt, sind 0,7–0,9 % der Pixel
verändert; Türrahmen und Wandfläche stehen unberührt. Das Modell fasst
tatsächlich nur an, was es anfassen soll.

**Der bewegte Gegenstand wird trotzdem neu gezeichnet.** Und genau der ist
bei einem Zustandspaar der Punkt.

| | was zurückkam |
|---|---|
| Versuch A, „die Hand rutscht nach rechts" | Hand zerfallen: die Faust hängt unter der Ärmellinie, die Manschette sitzt neben der Hand statt am Handgelenk |
| Versuch B, Faust und Daumen als Bauform beschrieben | Hand sauber und formgleich — aber der Arm ist kürzer und **waagerecht** statt schräg |

Versuch B ist brauchbar. Er ist nur nicht dasselbe Bild: der Armwinkel ist
ein zweiter sichtbarer Unterschied, und am Schnitt liest sich das als „er
hat den Arm bewegt". Die Parallaxe sagt das Gegenteil — der Arm steht
still, der Blick wechselt.

## 2. Der dritte Weg: rechnen statt zeichnen lassen

`zustandspaare.py`. Der springende Gegenstand wird im ersten Bild
freigestellt, die Lücke mit dem fortgesetzten Untergrund geschlossen, und
derselbe Pixelblock an der neuen Stelle wieder eingesetzt.

Gemessen an M04 → M05: **Haken, Türrahmen und die dunklere Wandfläche oben
rechts sind zu 100,0 % bitgleich.** Verändert ist ausschließlich, wo der Arm
war und wo er jetzt ist. Der Daumen ist nicht eine zweite Zeichnung
derselben Hand, sondern dieselbe.

M10 → M11 ist derselbe Fall in leicht: ein Stern wandert um 1.392 px,
95,9 % des Bildes bleiben bitgleich, das übrige Sternfeld steht exakt still.
Aus Text war das der Fall, der nie konvergieren konnte.

Zwei Dinge, die beim Bauen gemessen und verworfen wurden: die Lücke mit dem
Zeilenmittel zu füllen und sie zeilenweise zu interpolieren. Beides
hinterließ einen sichtbaren Fleck in der Form des entfernten Gegenstands,
weil die Flächen einen schwachen Verlauf aus dem Modell tragen. Die Füllung
rechnet den Untergrund jetzt flächig weiter.

**Grenze des Verfahrens:** es taugt für eine Verschiebung in der Bildebene.
Wo sich der Gegenstand selbst ändert — M46/M47, der Stern, der kleiner
wird — muss der zweite Zustand anders entstehen.

## 3. Der Anweisungsteil, umgebaut

Fünf unabhängige Lesungen desselben figurenlosen Prompts, danach jeder Fund
gegen die Belege aus Stapel 1 geprüft. Übernommen wurde, was mehrfach und
unabhängig gefunden wurde:

| Stelle | vorher | jetzt, ohne Figur |
|---|---|---|
| MACHART | „the same line weight on figures, clothing, props and background alike" | „on objects, architecture, vegetation and background alike" |
| MACHART | „explainer video made for adults" | „explainer video" |
| FARBEN | „and clothing is dyed with the dyes the named period and place really had" | „and painted surfaces, brick, glass and metal keep the colours those materials really have in the place shown" |
| Epochensatz | „Clothing, tools, architecture and vegetation all belong to …" | „Architecture and vegetation belong to …" |
| FRAMING | „no people in this picture at all" allein | „this is a picture of a place and of the things in it, seen empty and still - no people in this picture at all" |
| FLÄCHE | „every surface — rock, stone blocks, earth, water, sky and vegetation alike" | „every surface in this picture, whatever it shows" |

Der Wortlaut aus Video 1 bleibt unverändert stehen; er gilt weiter für alle
Bilder **mit** Figur, und damit ist Video 1 nachvollziehbar geblieben.

**Nicht übernommen**, je mit Grund:

- *„no hand-drawn jitter"* — „hand" steht hier in einem festen Fachwort für
  eine Strichart, nicht als Körperteil. Kein Beleg.
- *„no palms and no conifer backdrop"* — ein Verbot, ja, aber es ist die
  Hälfte einer positiven Florabeschreibung und die Antwort auf einen echten
  Schaden aus Video 1 (aus den Anden wurde Arizona). Wegnehmen hieße, eine
  belegte Reparatur aufzugeben.
- *„The sky is blue"* im Nachtbild — trifft zu, ist aber schon gelöst: der
  Nachtblock steht hinter FARBEN und überschreibt ihn.
- *„sepia-tint", „never cute", „no gradient"* — benennen Eigenschaften,
  keine zeichenbaren Dinge. Der belegte Mechanismus betrifft Substantive
  für Dinge.

Neu als harte Prüfung in `bildplan2.py`: `pruefe_personenworte()`. Ein
Prompt für ein figurenloses Bild darf kein Personenwort enthalten — einzige
Ausnahme ist der Framing-Satz selbst, der die Leere ausspricht. 43 Prompts
laufen dagegen, der Lauf bricht sonst ab, bevor Credits fließen.

## 4. M01, neu

Verlangt war ein Blick von unten in den Nachthimmel über einer heutigen
Wohnstraße. Zurück kam: **keine Person**, heutige Reihenhäuser mit
Backsteinfassade und modernen Fenstern, Lindenkronen in Silhouette, der
Himmel über zwei Dritteln des Bildes, ein Stern deutlich größer als die
übrigen. Die Ursache aus Stapel 1 ist damit belegt behoben.

Abweichungen, die keine Fehlschläge sind: die Dachlinie steht höher als
„along the bottom edge", und einzelne Fassaden tragen einen schwachen
Verlauf.

## 5. Bewerten wurde durch Beschreiben ersetzt

M11s „fainter" war nicht der einzige Fall. Sechs Szenentexte verglichen
Helligkeiten; alle sechs benennen jetzt eine gezeichnete Größe:

- M01 „a little brighter than the rest" → „drawn about twice as wide"
- M46 „large and bright" → „drawn three times the width of all the others"
- M47 „shrunk to a small dull point" → „now drawn the same small width as the others"
- M50 „thirteen stand out noticeably brighter" → „thirteen are drawn twice as wide"
- M61 „bright stars wrapped in faint nebula" → „large white stars wrapped in a thin pale veil"
- M69 „flares brilliantly … brighter than its core" → „drawn larger and whiter than that galaxy's own centre"

Dazu M10/M11: „a rectangular patch of the night sky" wurde als rechteckiger
Gegenstand gezeichnet, ein gerahmter Bildschirm mit Fuß. Steht jetzt als
„the night sky over the whole frame".

## Offen

Sieben weitere Zustandspaare. Ob sie montiert oder über Bild zu Bild
erzeugt werden, ist die eine Entscheidung, die diese Probe vorbereitet hat.
