# Stapel 3 gestoppt — 16.08.2026

> **24 Credits** (12 Motive à 2,0; M24 lief als Wiederholung mit). 12 von 12
> technisch erfolgreich, 0 API-Fehlschläge. **4 inhaltliche Fehlschläge — der
> Lauf ist gestoppt.** Kontostand 2.517,9. Von 236 Credits der Variante C
> sind 86 verbraucht.

## Ursache 1 — die Szene nennt einen Gegenstand, der in Wirklichkeit beschriftet ist

**Betrifft M30 und M39.**

Beide Prompts verlangten *„a two-euro coin"*. Zurück kamen zwei Münzen mit
einer großen **2** und dem Wort **EURO** darauf — lesbar, in beiden Bildern.
Das Verbot am Prompt-Ende (*„no text, no letters, no numbers"*) hat das
Modell wie immer übergangen.

Das ist die älteste Fehlerart des Projekts in neuer Gestalt. Bisher hieß sie:
*ein Wort, das etwas benennt, was nicht im Bild sein soll.* Jetzt heißt sie:
**ein Wort, das einen Gegenstand benennt, der die Schrift mitbringt.** Das
Modell zeichnet die echte Ware, und die echte Ware ist geprägt.

Dazu bei M30 ein zweiter Bruch: die Münze trägt **Verläufe** — metallischer
Schimmer auf Rand und Fläche, gegen die Flächenregel.

M39 hat außerdem **zwei Münzen** statt einer.

## Ursache 2 — niemand hat je gesagt, wie ein Stern in dieser Reihe aussieht

**Betrifft 14 Motive.** Gemessen am Anteil farbiger Pixel unter den hellen
Punkten:

| Motiv | helle Fläche | davon farbig | Grundton |
|---|---:|---:|---|
| M10 | 2,63 % | **0,0 %** | 13/26/43 (tiefblau) |
| M29 | 0,24 % | **60,3 %** | 21/23/27 |
| M36 | 1,94 % | **81,2 %** | 23/25/30 |

M10 hat weiße Sterne, weil sein Szenentext *„white star shapes"* sagt. M29
und M36 sagen nichts — und bekamen buntes Konfetti in Gelb, Blau und Rot.
**Drei Sternfelder in einem Video, die aus drei Kanälen stammen könnten.**
Das ist genau der Fall, der schwerer wiegt als die Textlosigkeit einzelner
Schemata.

Kein falscher Satz war schuld, sondern ein **fehlender**.

## Ursache 3 — eine Bedingung, die innerhalb eines Bildes wechselt

**Betrifft M28**, das einzige dreiteilige Motiv.

Die Florazeile ist richtig und je Vignette getrennt: *„bare limes, then
fynbos scrub, then snow-covered birches."* Trotzdem steht in der linken,
ausdrücklich kahlen Vignette ein **voll belaubter grüner Baum**.

Der Grund ist die Regel von gestern, eine Stufe feiner: Der Farbsatz nennt
Laub nur noch, wo Vegetation vorkommt — und M28 zählt als „mit Vegetation",
weil die mittlere Vignette Fynbos zeigt. Die Zusage galt damit auch für die
beiden anderen. **Die Bedingung ist je Motiv gestellt, M28 aber zeigt drei
Orte in einem Motiv.**

## Was in Ordnung war

**M24 sitzt jetzt** — Scheibe und Ring flächig, saubere Kanten, kein
Leuchthof mehr. M31 (weißes Observatorium, Tafelberg, Meer, tief stehende
Sonne), M32, M33 (Strichreihen wieder ohne einen Buchstaben), M35 (Birken
und Kiefern wie in der Flora verlangt, Mond hinter dünnen Wolken), M37, M38.

## Was daraufhin geändert wurde

1. **Beide Münzen als Form beschrieben**, nicht als Ware: *„one single small
   round metal coin standing upright on its edge, drawn flat - one solid
   pale ring for its rim and one solid gold circle inside it, both faces
   smooth and bare, and only the rim carries fine even notches."* Das Wort
   Euro kommt nicht mehr vor; „one single" hält die Anzahl.
2. **Neue Risikogruppe „Aufschrift-Träger"** in der Vokabelprüfung: euro,
   dollar, cent, banknote, newspaper, poster, calendar, keyboard und
   weitere. Wer so einen Gegenstand braucht, beschreibt ihn als Form.
3. **`STERNFELD` für 14 Motive** — die erste Regel, die sagt, wie ein Stern
   dieser Reihe aussieht: *„plain five-pointed star shapes of one and the
   same white, all filled with that one white and differing from one another
   only in size … no halo, no ray and no glow."* Und ausdrücklich: was die
   Szene einem einzelnen Stern an Farbe gibt (M58 gelblich und bläulich, M67
   rötlich), folgt der Szene. Der Block nennt nur, was in allen vierzehn
   gilt.
4. **`GEMISCHTE_FLORA = {"M28"}`** — wo eine Bedingung innerhalb eines Bildes
   wechselt, gilt die vorsichtigere Fassung. Die Vegetation der einzelnen
   Vignetten steht ohnehin in der Florazeile.

## Zu wiederholen

M28, M29, M30, M36, M39 — **10 Credits.** Danach die restlichen 24 Motive in
zwei Stapeln.
