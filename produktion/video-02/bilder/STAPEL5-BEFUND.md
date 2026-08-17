# Stapel 5 gestoppt — 16.08.2026

> **24 Credits** (12 Motive à 2,0). 12 von 12 technisch erfolgreich, 0
> API-Fehlschläge. **4 inhaltliche Fehlschläge — der Lauf ist gestoppt.**
> Kontostand 2.453,9. Von 236 Credits der Variante C sind 150 verbraucht.

## Was hält, und zwar messbar

**`FRAMING_GRUPPE` wirkt sofort.** M43 zeigt jetzt mehrere Frauen in
hochgeschlossenen Blusen an mehreren Tischen über Glasplatten **und** den
Mann an der Tür, der die Kiste übergibt. Beim Lauf davor kam eine einzige
Frau zurück.

**Der Leuchttisch ist warm.** M60 (254,249,240) fällt jetzt zu M44
(255,255,221) und M48 (255,254,234); M45 (231,255,255) ist der letzte Cyan-
Ausreißer und läuft im Nachlauf mit.

**Der Dunkelgrund hält über sechs weitere Motive:** M56 (19,32,49), M58
(11,25,41), M61 (12,24,42), M65 (14,27,43), M67 (8,24,39) — alle im selben
Tiefblau, Blau vor Grün vor Rot.

**Die Farbausnahme der Szene funktioniert wie entworfen.** M58 hat einen
gelblichen und einen bläulichen Stern, M67 mehrere rötliche — beide zwischen
weißen Sternspecks, genau wie der Sternblock es vorsieht.

Ohne Einschränkung bestanden: M55, M56, M58, M59, M62, M66, M67.

## Ursache 1 — „als Silhouette" zählte noch als grüne Vegetation

**M61.** Verlangt waren Baumsilhouetten am Nachthimmel; die Florazeile sagt
*„mitteleuropäische Laubbäume als Silhouette."* Zurück kamen **grüne,
beleuchtete Kronen und eine leuchtend grüne Wiese**.

Das ist der Fehler von M13 zum dritten Mal. `hat_pflanzen` kannte zwei
Ausnahmen — „—" und „ohne Laub" — und nicht die dritte: ein Baum, der als
Silhouette gezeichnet werden soll, zeigt keine Blattfarbe. Betroffen waren
außerdem M01, M02 und M39, die alle Silhouetten-Flora tragen.

## Ursache 2 — die Galaxienfarbe war so ungesagt wie vorher die Sternfarbe

**M65 gegen M56.** M56 kam mit weiß-blauen Spiralen zurück, **M65 mit
regenbogenfarbenen** in Blau, Rosa, Orange und Violett. Dieselbe Lücke wie
beim Sternfeld, nur eine Objektklasse weiter: der Sternblock legt Sterne
fest und sagt nichts über Galaxien.

## Ursache 3 — zwei Fotoplatten, zwei Konventionen, und eine widersprach ihrer eigenen Szene

**M45 gegen M60.** M45 zeigt weiße Punkte auf dunklem Glas, M60 einen
**dunklen Keil auf hellem Grund** — obwohl M60s Szene *„ein scharfer heller
Punkt"* verlangte.

Bei genauerem Hinsehen hatte das Modell recht und die Szene unrecht: auf
einer Glasplatte gegen das Licht sind Sterne **dunkel**. Ein heller Punkt auf
hinterleuchtetem Glas kann nicht heller sein als das Glas. Die Szene verlangte
etwas physisch Unmögliches, und das Modell hat es stillschweigend umgedreht.

Das ist zugleich die Konvention, die für die Schemata längst gilt — dunkle
Punkte auf hellem Grund wie auf gedruckten Sternkarten.

## Ursache 4 — eine zu knappe Szene wird aufgefüllt

**M63.** Verlangt: ein feinkörniges Fleckenmuster über die ganze Fläche,
davor klein ein Satellit im Profil. Zurück kam der Satellit vor dem Muster —
**plus einer großen blassen Erdkugel links und einer Sonne mit Leuchthof
rechts**, beide nicht verlangt, der Hof gegen die Flächenregel.

Kein Block war schuld. Die Szene ließ zwei Drittel des Bildes offen, und der
Ort („Lagrangepunkt, 2013") lieferte dem Modell die naheliegende Füllung.

## Was daraufhin geändert wurde

1. **`hat_pflanzen` kennt jetzt die Silhouette.** Vier Motive mehr laufen
   ohne Laubzusage: 53 statt 49.
2. **`GALAXIEN` für vier Motive** — weißer Kern, Arme in einem einzigen
   blassen Blauweiß, je Arm eine Füllung, und keine zwei Galaxien
   verschieden gefärbt.
3. **`PLATTE` für M45 und M60** — die Platte ist ein Negativ gegen das
   Licht: heller Cremegrund, Sterne als dunkle Punkte darauf. M60s Szene
   sagt jetzt „one small hard-edged dark dot" statt „one sharp bright
   point".
4. **M61s Bäume als Bauform** — „flat shapes filled with one single
   near-black tone, their leaf edges readable only as the outline of that
   shape" statt „tree silhouettes".
5. **M63 geschlossen** — das Muster füllt das Bild „from edge to edge, with
   nothing behind it and nothing beyond it", und der Satellit ist „the only
   solid object in the picture".

## Zu wiederholen

M45, M60, M61, M63, M65 — **10 Credits.** Dazu M68 als letztes noch nie
erzeugtes Motiv (2 Credits). Danach sind alle 60 erstzustandsfähigen Motive
erzeugt, und es fehlen nur die sechs abgeleiteten Zustände.
