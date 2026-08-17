# Stapel 2 gestoppt — 16.08.2026

> **24 Credits** (12 Motive à 2,0). 12 von 12 technisch erfolgreich, 0
> API-Fehlschläge. **4 inhaltliche Fehlschläge — der Lauf ist gestoppt.**
> Kontostand 2.549,9. Von 236 Credits der Variante C sind 54 verbraucht.

Vier Fehlschläge überschreiten die Schwelle. Drei davon haben **eine
gemeinsame Ursache**, und die trifft nicht diese zwölf Bilder, sondern 49
der 66.

## Ursache 1 — der Weltfarbsatz verspricht Laub und blauen Himmel, auch wo keiner ist

**Betrifft 49 der 62 Nicht-Schema-Motive.**

Jeder Prompt trug den Satz: *„The sky is blue, foliage and grass are green,
water takes its own real colour …"* Er stammt aus Video 1, wo fast jedes
Bild draußen spielte. In dieser Fassung zeigen **49 Motive überhaupt keine
Vegetation** — Nahaufnahmen, Innenräume, Sternfelder.

**M24 ist der Vollschaden.** Verlangt war die extreme Nahaufnahme eines
einzelnen Sterns, wie ihn ein bloßes Auge sieht. Zurück kam eine
**Tageslandschaft**: Teich, Rasen, ein Backsteingebäude, der Mond am blauen
Himmel. Gemessen: **59,9 % der Fläche blauer Himmel, 22,5 % grün.**

Der Grund, dass es gerade M24 traf: sein Ort ist „zeitlos, Blick zum
Nachthimmel", und der Nachtblock lief dort nicht mit — er galt nur für sieben
irdische Nachtbilder. **Sechzehn Motive zeigen nichts als den Weltraum, und
keines davon hatte einen Block, der das sagt.**

**M13 ist derselbe Fehler in schwächerer Form.** Verlangt waren kahle Bäume
bei Nacht. Zurück kamen **belaubte Kronen und eine leuchtend grüne Wiese**:
14,5 % der Fläche grün, und das Bild liest sich nur zu 71,4 % als dunkel
(M01 zum Vergleich: 95,4 %). Der Nachtblock allein hält das nicht auf — er
steht hinter FARBEN und redet über Helligkeit, nicht über Laub.

Dazu kam bei M13 ein zweiter Treffer derselben Art: die Florazeile sagte
*„street trees **without leaves**"*. Ein Verbot, das Laub benennt — und Laub
kam.

**M18** ist der dritte: verlangt war die Nahaufnahme einer Mikrometerskala
bei Öllampenlicht, gezeichnet wurde eine Werkstatt mit einem **Fenster voll
blauem Tageslicht** — eine zweite Lichtquelle, wo genau eine erlaubt ist.

## Ursache 2 — die Handlung stand wieder als Attribut da

**M15**, der geschützte Moment „Die Schraube". Verlangt: ein Mann sitzt am
Okular eines großen Refraktors und dreht mit der rechten Hand eine
Mikrometerschraube. Gezeichnet: ein Mann, der ein **kleines Handfernrohr in
die Luft hält**, während der große Refraktor daneben auf dem Tisch steht.

Das ist der M44-Befund aus Stichprobe 2, unverändert: **Attribute fallen
weg, Bauanweisungen bleiben.** „sitzt am Okular und dreht" ist ein Attribut.

## Was in Ordnung war

M14 (Linse durchgesägt, Hälfte verschoben, Messingschraube, harter Schatten
von rechts), M16 (zwei getrennte Sternabbilder im runden Gesichtsfeld), M19,
M20, M22, M23, M26, M27.

**Die Schriftregel hält zum zweiten Mal.** M23s Blatt und M19s Buchseite
unter der Lupe: reine Strichgruppen und graue Zeilenbänder, **kein
Buchstabe, keine Ziffer.**

## Was daraufhin geändert wurde

1. **`farben(mit_figur, mit_pflanzen)`** — der Farbsatz nennt nur noch, was
   im Bild wirklich vorkommt. Mit Pflanzen die konkreten Anker wie bisher,
   ohne Pflanzen nur noch *„Every material in the picture keeps the colour
   that material really has."* Von 66 Prompts nennen jetzt 13 Laub statt 62.
   `farben(True, True)` ist wortgleich mit dem Video-1-Satz.
2. **`WELTRAUM`-Block für 16 Motive** — beschrieben, nicht verboten: eine
   flache fast schwarze Fläche, und die einzigen hellen Formen darin sind
   die genannten Lichtquellen.
3. **`EPOCHE_NEUTRAL`** — wo weder Figur noch Pflanze im Bild ist, nennt der
   Epochensatz gar nichts mehr: *„Everything shown in this picture belongs
   to that period and place and to no other."* „Architecture and vegetation"
   in der Nahaufnahme einer Objektivlinse war derselbe Fehler wie
   „Clothing" im menschenleeren Bild.
4. **Kahle Bäume positiv beschrieben** — statt „without leaves" jetzt „each
   drawn as a bare branching silhouette of trunk and open twigs against the
   sky".
5. **M15 als Bauanweisung** — Hocker, gebeugter Oberkörper, gesenkter Kopf,
   rechtes Auge am Okular am unteren Ende **eines einzigen** langen Rohrs,
   rechte Hand um die geriffelte Messingtrommel, linke Hand flach auf dem
   Knie. Jede Hand und jedes Auge einzeln verortet.
6. **`pruefe_pflanzenworte()`** — harte Prüfung über die geteilten
   Anweisungsblöcke: ein Motiv ohne Vegetation darf dort kein Pflanzen- oder
   Baustoffwort tragen. Der motiveigene Flora- und Ortssatz ist ausgenommen,
   weil das, was dort steht, gewollt ist. 49 Motive laufen dagegen; der Lauf
   bricht sonst ab, bevor Credits fließen.

Dazu angeglichen: neun deutsche Szenentexte in `szenenplan.py`, die noch
Helligkeiten verglichen, während die englischen längst gezeichnete Größen
nannten. `szenen.md` neu erzeugt.

## Zu wiederholen

M13, M15, M18, M24 — **8 Credits.** Danach die restlichen 42 Motive.
