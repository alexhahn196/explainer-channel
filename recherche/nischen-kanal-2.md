# Nischen-Recherche für Kanal 2 — 2026-08-07

> Reine Analyse über die NexLev-Tools, **0 Higgsfield-Credits ausgegeben**
> (Bildpreise stammen aus `get_cost`-Messungen vom selben Tag, kostenlos).
>
> **Alle Umsatz- und RPM-Angaben von NexLev sind Schätzungen**, keine
> gemessenen Auszahlungen. Jede Zahl trägt eine Kennzeichnung:
> **[gemessen]** = direkt aus einem Tool-Ergebnis · **[geschätzt]** =
> NexLev-Modellwert oder eigene Ableitung · **[unbekannt]** = nicht ermittelbar.

## Auftrag & Rahmen

Gesucht: eine Nische für einen zweiten Kanal. Harte Filter: faceless, Stock
erlaubt, **maximal 2 Uploads/Woche**, KI-Produktion ohne Team, Zielmarkt US/EN.
Quellen: `search_niche_finder_channels` — Wildcard (158 Treffer, 50 gezogen)
plus drei thematische Queries (Business, Space, Erklärformat), dazu je Nische
ein Haltbarkeits- und ein Monetarisierungsquoten-Lauf, `get_geography_revenue`
auf die stärksten Kanäle und `youtube_channel_outliers` für bewiesene
Videoideen. Insgesamt ~150 Kanäle gesichtet, zu Nischen gruppiert (eine Nische
zählt nur mit ≥2 Trägerkanälen), vier Finalisten hart geprüft.

## Empfehlung

**History-Explainer im Ink-Explainer-Schnitt: Alltags- und Menschheitsfragen
der Geschichte, ohne Krieg, ohne benannte Personen als Kern.** Die Nische ist
die einzige, die auf *jeder* Altersstufe Kanäle mit deiner Kadenz zeigt: jung
Ink Explainer (gegr. 2026-04, **0,5 Uploads/Wo**, geschätzt ~9.560 $/Mon,
Outlier 22,91), etabliert Historically (gegr. 2023, **0,5/Wo**, ~12.956 $/Mon)
und quack doc (2023, 1,25/Wo, ~11.790 $/Mon). Nachfrage, Einstiegsfenster,
Machbarkeit und Geografie sind grün; einziger Gelb-Punkt ist der RPM (4–6 $).
Einstiegswinkel in einem Satz: konkrete, googlebare Alltagsfragen an die
Vergangenheit („Was taten Menschen vor 10.000 Jahren, wenn es eine Woche
regnete?") als 8–15-min-Erklärvideo aus KI-Standbildern mit TTS — exakt die
Pipeline, die für Kanal 1 bereits läuft.

**Zweitplatzierter mit anderem Profil: Business-/Wirtschafts-Doku** (Micro,
Big Company, keeping tabs) — höherer Kategorie-RPM (8–9,4 $ Basis), noch
niedrigere Kadenz (Median 1,1/Wo), aber deutlich höhere Skript- und
Rechercheanforderung je Video und Faktenrisiko in einer Fremdsprache.

## Scorecard der Finalisten

Ampeln nach den vorgegebenen Kriterien; in Klammern die tragende Zahl.
K.-o.-Regel: Rot bei Nachfrage, Einstiegsfenster oder Machbarkeit
disqualifiziert.

| Kriterium | History-Explainer | Space-Explainer | Business-Doku | Travel-Doku |
|---|---|---|---|---|
| 1. Nachfrage (≥3 Kanäle Outlier ≥2) | 🟢 6 Kanäle (36,4 / 22,9 / 15,0 / 2,9 / 2,7 / 2,3) | 🟢 5 (10,6 / 10,0 / 6,9 / 4,1 / 2,3) | 🟢 5 (68,9 / 11,7 / 8,4 / 2,4 / 2,0) | 🟢 4 (6,9 / 6,4 / 4,1 / 4,0) |
| 2. RPM (`rpm.total`) | 🟡 3,7–5,8 $ | 🟡 4,6–6,6 $ (Astrum Long-RPM 8,3) | 🟡 5,8–8,0 $ (Kategorie-Basis 8–9,4) | 🟡 5,7–6,1 $ |
| 3. Einstiegsfenster (junge Kanäle ≥20k Ø-Views) | 🟢 12 im 40er-Zug | 🟢 7 | 🟢 14 | 🟢 20 |
| 4. Wettbewerbsdichte | 🟡 dicht, `hasMore` bei 40 [geschätzt] | 🟡 dicht + Riesen (Astrum) | 🟡 dicht | 🟡 sehr dicht |
| 5. **Machbarkeit** (Median Uploads/Wo) | 🟢 **1,0** | 🟢 **0,5** | 🟢 **1,1** | 🔴 **2,5 → K.-o.** |
| 6. Geografie (Tier-1-Anteil der Top-5) | 🟢 80,2 % | 🟢 85,3 % | 🟢 70,3 % | 🟢 77,2 % |
| 7. Haltbarkeit (>12 Mon., ≥1.000 $/Mon) | 🟢 7 Belegkanäle | 🟢 4 | 🟢 3 | 🟢 4 (irrelevant, K.-o.) |
| Monetarisierungsquote | 70 % (28/40) | 72 % (29/40) | 75 % (30/40) | 82 % (33/40) |
| **Urteil** | **Empfehlung** | tauglich | tauglich | **disqualifiziert** |

Alle Quoten liegen über der 50-%-Warnschwelle — deutlich besser als die
Bibel-Schlaf-Nische (dort 19 von 30). Auffällig bleiben einzelne große Kanäle
ohne Freigabe: OtherWorldly History (130k Abos), Universe (456k), Geography
Geek (372k) — Einzelfälle, kein Nischenmuster.

Wettbewerbsdichte ist die schwächste Messung dieses Berichts: sie beruht auf
der Trefferdichte der Suchläufe (alle vier Nischen liefern 40+ Kanäle mit
≥10k Ø-Views und `hasMore`), nicht auf `get_similar_channels` — als
[geschätzt] zu lesen.

---

## Nische 1 — History-Explainer (Empfehlung)

### Belegkanäle

| Kanal | Link | gegr. | Abos | Views/Mon | $/Mon [geschätzt] | RPM | Up/Wo | Mon. |
|---|---|---|---|---|---|---|---|---|
| Ink Explainer | [/channel/UCpgrEMx8diLrw7YNQ6r3uUw](https://youtube.com/channel/UCpgrEMx8diLrw7YNQ6r3uUw) | 2026-04-09 | 45.500 | — | 9.560 | 3,96 | **0,5** | ja |
| Historically | [/channel/UCoZd78hRUdxxsuGiABuHF_A](https://youtube.com/channel/UCoZd78hRUdxxsuGiABuHF_A) | 2023-03-08 | 1,31 Mio. | 2,99 Mio. | 12.956 | 4,33 | **0,5** | ja |
| quack doc | [/channel/UC2NRf0-PH8IiMq5uA5FHJnA](https://youtube.com/channel/UC2NRf0-PH8IiMq5uA5FHJnA) | 2023-01-22 | 146.000 | 2,12 Mio. | 11.790 | 5,57 | 1,25 | ja |
| History Mapped Out | [/channel/UCtzvIHQyRDL2mtetu6ZWsvw](https://youtube.com/channel/UCtzvIHQyRDL2mtetu6ZWsvw) | 2023-02-27 | 175.000 | 498.000 | 2.158 | 4,33 | 1,75 | ja |
| Axen | [/channel/UC_7R-sfi7bi8dkzmSlBdUVw](https://youtube.com/channel/UC_7R-sfi7bi8dkzmSlBdUVw) | 2026-04-28 | 51.600 | — | 3.090 | 3,96 | **0,25** | ja |
| Mapped History | [/channel/UCInfdX6B8ej4f2zge4fVuWw](https://youtube.com/channel/UCInfdX6B8ej4f2zge4fVuWw) | 2020-09-17 | 11.400 | 250.000 | 1.191 | 4,77 | 1,0 | ja |

### Haltbarkeitsbefund

**Evergreen, mehrfach belegt [gemessen]:** Historically (3,4 Jahre alt,
~12.956 $/Mon), quack doc (3,5 Jahre, ~11.790 $), History Mapped Out
(3,4 Jahre, ~2.158 $), Mapped History (5,9 Jahre, ~1.191 $), Ollie Bye
(12 Jahre, ~1.260 $). Die Nische trägt Kanäle über Jahre — das Gegenteil des
Lorevia-Musters.

### Bewiesene Videoideen (Outlier der Konkurrenz [gemessen])

1. „What Did Ancient Humans Do When It Rained All Week?" — **1,1 Mio. Views,
   Outlier 2,9×**, Kanal 3 Monate alt —
   [watch?v=SD7XyG2wd1k](https://youtube.com/watch?v=SD7XyG2wd1k)
2. „Why Are We the Only Human Species Left?" — **887k, 2,3×** —
   [watch?v=OCr6NteWSQ8](https://youtube.com/watch?v=OCr6NteWSQ8)
3. „When Did Ancient Humans Start Drinking Alcohol?" — **773k, 2,0×** —
   [watch?v=9AFO6MHy8y4](https://youtube.com/watch?v=9AFO6MHy8y4)
4. Ergänzend aus dem Umfeld: „Ancient Technologies We Still Can't Explain"
   (Professor Historian, **4,5 Mio.**,
   [watch?v=kC4hErBshbc](https://youtube.com/watch?v=kC4hErBshbc)) und „The
   ENTIRE History of ROME" (Historically, **5,9 Mio.**,
   [watch?v=EHLI2WZUtXs](https://youtube.com/watch?v=EHLI2WZUtXs)).

Das Muster hinter den Treffern: eine **konkrete, naive Frage** an den Alltag
der Vergangenheit, keine Jahreszahlen-Chronik. Genau diese Sorte Thema ist
ohne Kriegsbezug, ohne lebende Personen und ohne fremdes Bildmaterial
produzierbar.

### Produktionskosten je Video [geschätzt aus gemessenen Preisen]

Format nach Ink-Explainer-Muster: 8–15 min, KI-Standbilder mit sanfter
Bewegung, TTS-Stimme, Schnitt per Pipeline.

| Posten | Preis [gemessen, `get_cost` 2026-08-07] | Menge | Summe |
|---|---|---|---|
| KI-Standbild `nano_banana_2` 16:9 2k | 2 Credits | ~50–75 (1 Bild je 8–12 s) | 100–150 Cr. |
| optional KI-Clips (Seedance 12 s, Ist-Preis) | 18 Credits | 2–3 Schlüsselszenen | 36–54 Cr. |
| **Bildkosten je Video** | | | **≈ 100–200 Cr. ≈ 4,75–9,50 €** (Top-up-Kurs) |
| TTS (~8.000–9.500 Zeichen, Fish Audio) | | | **[unbekannt]** — läuft nicht über Credits |

Bei 2 Videos/Woche: ~800–1.600 Credits/Monat — **passt ins bestehende
Ultra-Abo-Kontingent (3.000/Mon) neben Kanal 1** (~450 Cr./Mon).

### Einstiegswinkel und Abgrenzung

Ink Explainer beweist das Format, ist aber erst 12 Videos alt und deckt ein
schmales Themenband (Frühgeschichte). Offen bleiben: Alltagsgeschichte
späterer Epochen (Mittelalter-Hygiene, Essen der Antike, Schlaf vor der
Glühbirne — Letzteres schlägt eine Brücke zur Schlaf-Expertise aus Kanal 1),
Wirtschaftsalltag („Was verdiente ein römischer Bäcker?" — The Expensive Part
fährt genau das seit drei Wochen mit 80k-Views-Treffern). Stilistisch passt
die **Blaupause- oder Flat-Vector-Handschrift aus
`recherche/stile-erklaerkanal-2/`** — kein etablierter Kanal der Nische nutzt
so etwas; die meisten fahren generische KI-Malerei oder Countryballs.

**Themenleitplanke wegen des Krieg-Ausschlusses:** Die Nische als Kategorie
enthält viel Kriegsgeschichte (Historically: „WW2's BEST Soldiers"). Der
eigene Kanal bleibt bei Alltag, Technik, Ernährung, Wirtschaft, Wissenschaft —
die Outlier-Belege oben zeigen, dass genau dort die stärksten Ausreißer
liegen. Das ist kein Nachteil, sondern die Lücke.

---

## Nische 2 — Business-/Wirtschafts-Doku (zweite Wahl)

### Belegkanäle

| Kanal | Link | gegr. | Abos | $/Mon [geschätzt] | RPM | Up/Wo | Mon. |
|---|---|---|---|---|---|---|---|
| Micro | [/channel/UCJVXj8BvHykEklEeKjFwaXQ](https://youtube.com/channel/UCJVXj8BvHykEklEeKjFwaXQ) | 2024-08-15 | 197.000 | 2.926 | 5,82 | **0,25** | ja |
| Big Company | [/channel/UC6i4-GuVpkcR_1UbgfldM_g](https://youtube.com/channel/UC6i4-GuVpkcR_1UbgfldM_g) | 2022-01-23 | 452.000 | 1.601 | 5,82 | **0,25** | ja |
| keeping tabs | [/channel/UCPWbCmOE7VZZEWe7RaVEy4w](https://youtube.com/channel/UCPWbCmOE7VZZEWe7RaVEy4w) | 2026-05-07 | 7.470 | 2.301 | 4,50 | **0,25** | ja |
| Unlearning Economics | [/channel/UC4V_jMdRbbTrmBVJB6FDzgw](https://youtube.com/channel/UC4V_jMdRbbTrmBVJB6FDzgw) | 2020-04-18 | 257.000 | 1.006 | **8,05** | 0,5 | ja |
| Fallen Hi-Fi | [/channel/UCBd5qczHCJjGQ74In8Z2CKA](https://youtube.com/channel/UCBd5qczHCJjGQ74In8Z2CKA) | 2026-04-17 | 9.400 | 3.306 | 4,62 | 1,75 | ja |

**Haltbarkeit [gemessen]:** Micro (2 Jahre), Big Company (4,5 Jahre),
Unlearning Economics (6 Jahre) — alle über 1.000 $/Mon.

**Bewiesene Videoideen [gemessen, `youtube_channel_outliers`]:**
„How A Single Costco Changes Its Local Economy" (**2,9 Mio., 4,9×**,
[ldQAZNXecBY](https://youtube.com/watch?v=ldQAZNXecBY)) · „The Anti-Human
Business of Ship Breaking" (**2,9 Mio., 4,9×**,
[JRQzYaCRgnw](https://youtube.com/watch?v=JRQzYaCRgnw)) · „Why Only Three
Countries Bother Building Ships Anymore" (**2,8 Mio., 4,7×**,
[0Gk61ginOqo](https://youtube.com/watch?v=0Gk61ginOqo)).

**Produktion:** Micro-Stil lebt von Stock-Material („Stockmaterial —
Lizenzkosten [unbekannt]") plus Grafiken; mit KI-Standbildern machbar
(~100–150 Cr. wie oben). Der wahre Kostenblock ist **Recherche und Skript** —
1.500–2.500 Wörter belastbarer Wirtschaftsanalyse je Video, auf Englisch, mit
Faktenrisiko. Warum zweite Wahl: bester RPM und niedrigste Kadenz, aber der
unsichtbare Aufwand je Video ist der höchste aller Finalisten, und der
68,85-Outlier von keeping tabs beruht auf **einem einzigen Video** — starkes,
aber schmales Signal.

---

## Nische 3 — Space-Explainer (tauglich, nicht empfohlen)

Belegkanäle: Astrum Extra
([/channel/UCD_zO_MDaC7MyekAmrn6WVQ](https://youtube.com/channel/UCD_zO_MDaC7MyekAmrn6WVQ),
2016, ~26.596 $/Mon [geschätzt], 1/Wo, Long-RPM 8,3) · Bluntly Explained
([/channel/UC4ZpfvppuvCefRu3T7p0ojg](https://youtube.com/channel/UC4ZpfvppuvCefRu3T7p0ojg),
2026-04, ~3.267 $, 1/Wo, Outlier 10,58) · Causality
([/channel/UC0w1d6Hny6WWtrq8nASNKSA](https://youtube.com/channel/UC0w1d6Hny6WWtrq8nASNKSA),
2026-05, ~2.174 $, 0,5/Wo, Outlier 9,98) · Universe Dimensions
([/channel/UC5kNK793CSXYHEpG-BAqWfQ](https://youtube.com/channel/UC5kNK793CSXYHEpG-BAqWfQ),
2024, ~2.448 $, 0,5/Wo) · Digital Astronaut (2018, ~1.869 $, 0,5/Wo).

Bewiesene Ideen: „What NASA Saw At the Edge of... Everything" (4,4 Mio.,
[bh1lcn2SPNg](https://youtube.com/watch?v=bh1lcn2SPNg)) · „Sunsets from
Different Alien Worlds" (2,2 Mio.,
[oiiwPbxzIy0](https://youtube.com/watch?v=oiiwPbxzIy0)) · „The Fermi Paradox
Has A Disturbing Solution" (707k,
[-P_A3h77zOM](https://youtube.com/watch?v=-P_A3h77zOM)).

Produktion: günstigste aller vier — NASA/ESA-Material ist gemeinfrei, Rest
KI-Bilder (~50–100 Cr. ≈ 2,40–4,75 €). Warum nicht empfohlen: Astrums Netzwerk
dominiert die Spitze, die Wissenschafts-Faktenprüfung ist anspruchsvoll, und
ein gesichteter Belegkanal (Astral Curiosity) lebt von
Brian-Cox-Fremdmaterial — in der Nische ist das Wiederverwerten realer
Personen verbreitet, genau was du ausschließt. Der saubere Weg (eigene
Skripte, eigenes Bild) existiert (Bluntly Explained, Causality), ist aber
gegen die Riesen der schwerere Kampf als bei History.

---

## Verworfen und warum

| Nische / Kanal | Grund |
|---|---|
| **Travel-Doku** (Travpedia, Nations Uncovered, 9 weitere) | **K.-o. Machbarkeit: Median 2,5 Uploads/Wo** über 11 Belegkanäle — trotz einzelner Niedrigkadenz-Gewinner. Zudem Stock-Lizenzkosten [unbekannt] |
| **True Crime** (Dead End Files ~19.400 $/Mon, 9 weitere) | K.-o.-Ausschluss: Monetarisierungsbeschränkungen — größter Einzelcluster der Wildcard, bewusst liegengelassen |
| **KI-Wildlife** (Wild Bird Survival ~17.107 $, Wildlife zone) | Machbarkeit rot (5,8–7,8 Uploads/Wo) **und** RPM 1,55 rot — deckt sich mit `kostenvergleich-formate.md` |
| **Military/Geopolitik** (San English, Heroes In Uniform, 4 weitere) | K.-o.-Ausschluss Krieg |
| **Christian Educational** (Simplifying the Bible, Time Routes, 2 weitere) | Median-Kadenz ~3,5/Wo → Machbarkeit rot; zudem Kannibalisierungsrisiko mit Kanal 1 |
| **Celebrity/Filme/TV/Anime** (Golden FilmRetro, Sitcom Mind, Okens, The Vintage Cut) | K.-o.: fremdes IP bzw. reale Personen als Kern |
| **Sport-Kommentar** (True Talk Football, Boxing Vibe, Brandon Alex) | reale Personen + Fremdmaterial |
| **Disaster-Dokus** (Vanished Worlds, The Watchroom) | sensible Ereignisse |
| **HOA/Reddit-Drama** (Karen Karma) | nur 1 Kanal im Fenster — ein Treffer, kein Markt |
| **Rural Real Estate** (Backroad Estates, RPM 9,12, 1,5/Wo) | nur 1 Kanal — ein Treffer, kein Markt. **Beobachten:** höchster RPM der ganzen Wildcard |

## Datenlücken & Vorbehalte

- **Alle $-Angaben sind NexLev-Schätzmodelle.** Wo `get_geography_revenue`
  andere Werte lieferte als die Suche (Historically: 25.290 gegen 12.956 $),
  habe ich den konservativeren Suchwert berichtet — die Abweichung zeigt die
  Modellunsicherheit.
- **Tier-1-Anteile** beziehen sich auf die fünf größten Zuschauerländer
  (Summe = 100 %), nicht auf alle Länder — reale Anteile liegen etwas
  niedriger.
- **Wettbewerbsdichte** ohne `get_similar_channels` gemessen — nur
  Trefferdichte, als Schätzung markiert.
- **keeping tabs**: Outlier 68,85 aus einem einzigen Video — Signal, kein
  Beweis.
- **TTS-Kosten in Euro** für alle Formate [unbekannt] (Fish Audio läuft nicht
  über Credits).
- Die 4-Monats-Entdeckungslisten enthalten nur Kanäle ≥2.000 $/Mon — über
  gescheiterte junge Kanäle derselben Nischen sagt dieser Bericht nichts
  (Überlebenden-Verzerrung der Discovery).

## Skizze: Faktenprüfung als Pipeline-Schritt (Ergänzung 2026-08-07)

> Konzept und Zahlen, kein Code. Analogie: `qa_namen.py` prüft bei Kanal 1
> die Aussprache aller Eigennamen nach der TTS; hier prüft ein Schritt
> `faktencheck.py` die Belegbarkeit aller Tatsachenbehauptungen **vor** der
> TTS — und blockiert den Render wie heute ein zu breiter Thumbnail-Text.

### Wie der Schritt arbeiten würde

1. **Zerlegen.** Nach Schritt 1 (Text) wird das Skript in Sätze zerlegt und
   jeder Satz einer von drei Klassen zugeordnet: *harte Behauptung* (enthält
   Zahl, Datum, Messwert), *weiche Behauptung* (Tatsachenaussage ohne Zahl),
   *Erzählung* (Anrede, Szene, Frage — nicht prüfpflichtig). Die Klassifik
   ist mit einer Heuristik machbar (unten gemessen), sauberer per
   LLM-Durchgang.
2. **Quellenpflicht.** Das Skriptformat bekommt neben `skript.json` eine
   `quellen.json`: jede harte Behauptung trägt eine Quellen-ID (URL + Zitat +
   Abrufdatum). Ink Explainer macht genau das öffentlich vor — „all sources
   always cited" steht in der Kanalbeschreibung, die Quellen stehen in jeder
   Videobeschreibung. Das ist in der Nische also nicht Kür, sondern der
   Standard des besten jungen Kanals.
3. **Maschinenprüfung.** Für Behauptungen der Form *Entität + Zahl* („Qesem
   Cave, Feuernutzung vor 400.000 Jahren") ruft der Schritt Wikipedia/Wikidata
   ab und prüft, ob die Zahl im Toleranzband der Quelle liegt. Ergebnis je
   Behauptung: `belegt` / `abweichend` / `nicht auffindbar`.
4. **Blockierregel.** Harte Behauptung **ohne Quelle** oder mit Prüfergebnis
   `abweichend` → Rückgabewert 1, Render startet nicht — dieselbe Mechanik,
   mit der `thumbnail.py` heute einen zu breiten Text stoppt. `nicht
   auffindbar` blockiert nicht, sondern landet auf der Mensch-Checkliste in
   `upload.md`, neben „KI-Kennzeichnung setzen".

### Erreichbare Quellen — aus dem Container gemessen [gemessen 2026-08-07]

| Quelle | Status | Verwendbarkeit |
|---|---|---|
| Wikipedia REST-API (`en.wikipedia.org/api/rest_v1`) | **200** | Kernquelle für Entität+Zahl-Prüfung |
| Wikidata (`Special:EntityData/*.json`) | **200** | strukturierte Daten (Jahreszahlen, Orte) |
| archive.org (Suche/API) | **200** | Primärtexte, alte Bücher |
| Crossref (`api.crossref.org`) | **200** | Paper-Metadaten: existiert die zitierte Studie? |
| bible-api.com | **200** | (bereits in der Pipeline von Kanal 1) |
| Semantic Scholar API | **429** | erreichbar, aber ratenlimitiert — bräuchte API-Schlüssel |
| Google Scholar | 200 | erreichbar, aber Scraping bricht deren Nutzungsbedingungen — **nicht verwenden** |
| Britannica | **403** | blockiert |

Die Maschinenprüfung ist also machbar: Wikipedia + Wikidata + Crossref
decken die Formen ab, die ein History-Explainer-Skript braucht. Crossref
prüft dabei nur, **dass** eine zitierte Studie existiert — nicht, was in ihr
steht; Volltexte sind meist hinter Bezahlschranken → Mensch.

### Wie viele Behauptungen ein Skript enthält [gemessen]

Gezählt am Transkript des stärksten Ink-Explainer-Videos („What Did Ancient
Humans Do When It Rained All Week?", 1,1 Mio. Views, **2.413 Wörter**,
200 Sätze), Heuristik wie oben beschrieben:

| Klasse | Anzahl | Beispiel |
|---|---|---|
| harte Behauptungen (Zahl/Datum) | **22** | „controlled fire use going back at least 400,000 years at a site called Qesem Cave in Israel" |
| weiche Behauptungen | **20** | „Archaeologists have found layers of flood sediment inside occupied caves" |
| Erzählung/Anrede/Frage | 158 | „Imagine you haven't eaten in 2 days." |

Die Heuristik hat dabei sichtbar 2–4 falsche Treffer (das „2 days" im
Einstieg ist Szene, keine Behauptung) — realistisch **~18–20 harte plus ~20
weiche Behauptungen je 2.400 Wörter**, also grob **1 prüfpflichtige Aussage
je 60 Wörter**. Auf das geplante 1.500-Wort-Skript skaliert:
**~25 Behauptungen je Video** (davon ~12 harte).

### Maschine gegen Mensch [geschätzt]

- **Maschinell belegbar: etwa die Hälfte.** Alle Behauptungen mit benannter
  Entität und Zahl (Qesem Cave, Ötzi 5.300 Jahre, „25-mal schnellerer
  Wärmeverlust") sind Wikipedia/Wikidata-prüfbar. Am gezählten Skript: ~10–12
  der ~25.
- **Mensch nötig: die andere Hälfte.** Weiche Behauptungen („Höhlen liegen
  oft an Flussläufen"), zusammenfassende Formulierungen („the archaeological
  record is very clear on this") und alles, wo die Maschine `nicht
  auffindbar` meldet. Hier prüft ein Mensch gegen die hinterlegte Quelle —
  oder beschafft erst eine.
- **Nicht delegierbar:** die Entscheidung, ob eine Zuspitzung noch von der
  Quelle gedeckt ist. Das ist Redaktionsurteil, keine Abfrage.

### Zeitaufwand je Video [geschätzt]

| Posten | Ansatz | Zeit |
|---|---|---|
| Maschinenlauf sichten (10–12 Bestätigungen stichprobenartig gegenlesen) | 1–2 min je Stichprobe, ~5 Stichproben | ~10 min |
| ~13 Mensch-Behauptungen gegen Quelle prüfen | 3–5 min je Behauptung | 40–65 min |
| Quellen nachbeschaffen für 2–3 Behauptungen ohne Beleg | 5–10 min je | 15–30 min |
| **Summe je Video** | | **≈ 1–1,75 h** |

Zum Vergleich: Der Renderlauf von Kanal 1 braucht ~25 min Rechenzeit. Die
Faktenprüfung wäre damit der **teuerste Einzelschritt der Pipeline** — und
zugleich der Unterschied zwischen dem Ink-Explainer-Modell („all sources
cited") und der KI-Doku-Massenware, gegen die YouTube zunehmend vorgeht.
Wer die 1–1,75 h nicht einplant, sollte die Nische nicht anfassen; bei
2 Videos/Woche sind das **2–3,5 h Redaktionsarbeit wöchentlich** als fester
Block neben der Maschine.

### Was der Schritt bewusst nicht leistet

Er beweist nicht, dass eine Aussage *wahr* ist — er erzwingt, dass sie
*belegt* ist und die Belege zur Veröffentlichung vorliegen (Videobeschreibung
wie bei Ink Explainer). Falsche Quellen, veraltete Forschung und
Fehlinterpretationen fängt nur das Redaktionsurteil. Die Blockierregel senkt
das Risiko, sie beseitigt es nicht.

## Umgang mit unsicheren Fakten: Treffer gegen schwache Videos (Ergänzung 2026-08-07)

> Gezählt an sechs Transkripten — je Kanal das stärkste gegen ein schwaches
> Video. Zwei Zählungen: **epistemische Marker** (echte
> Unsicherheits-Kennzeichnung: „we don't know", „the most common theory",
> „historians believe", „probably/apparently") und die **Glatt-Quote** —
> der Anteil der Sätze mit Zahl oder Datum, die *ohne jede* Absicherung
> daherkommen. Alles [gemessen], Heuristik per Wortliste; ASR-Transkripte
> enthalten Hörfehler.

### Die Zahlen

| Kanal | Video | Wörter | epist. Marker je 1.000 W | Glatt-Quote der Zahlsätze | Quellen |
|---|---|---|---|---|---|
| Ink Explainer | **TOP** „Rained All Week" (1,1 Mio.) | 2.413 | **3,7** | 57 % (13/23) | **16 akademische Quellen mit DOI in der Beschreibung** |
| Ink Explainer | schwach „Got Sick" (25k) | 1.415 | 2,1 | 83 % (10/12) | 5 Quellen-Marker im Sprechtext („We know this because ancient Egyptian medical texts from 1500 BCE…") |
| Historically | **TOP** „History of Rome" (6,1 Mio.) | 6.600 | **2,4** | 88 % (46/52) | **keine** — Beschreibung enthält nur Giveaway, Mitglieder-Werbung, Timestamps, Musiklizenz |
| Historically | schwach „Dumbest Heist" (790k) | 2.100 | 0,5 | 86 % (12/14) | keine |
| quack doc | **TOP** „Deadly Disease Teil 1" (1,7 Mio.) | 5.606 | **0,7** | 69 % (29/42) | **keine** — nur Disclaimer: „based on the research and opinions of the creator" |
| quack doc | schwach „Teil 2" (81k) | 5.513 | 0,2 | 70 % (21/30) | keine |

Das quack-doc-Paar ist das sauberste Kontrollpaar der Messung: **dieselbe
Serie, dasselbe Format, Teil 1 mit 1,7 Mio. gegen Teil 2 mit 81k.**

### Drei Befunde

**1. Die drei Kanäle fahren drei verschiedene Ehrlichkeits-Modelle.**
Ink Explainer markiert Unsicherheit fünfmal so oft wie quack doc und legt als
einziger Quellen offen — vollständige akademische Zitate mit DOI-Links
(Journal of Archaeological Science, PNAS, Science), dazu ein eigener Block,
der die erwähnten Forscher und Fundstätten erklärt. Historically behauptet
glatt durch (88 % der Zahlsätze ungesichert) und zitiert nichts — trägt das
aber als Comedy-Format („Condensed **Dramatized** History"), das erkennbar
zuspitzt. quack doc behauptet fast alles glatt, nennt keine Quellen und
schiebt einen Disclaimer davor. Alle drei verdienen fünfstellig — **YouTube
erzwingt keines der Modelle.**

**2. Innerhalb jedes Kanals ist das Treffer-Video das vorsichtigere.** Ink
3,7 gegen 2,1 · Historically 2,4 gegen 0,5 · quack doc 0,7 gegen 0,2 — die
Richtung ist dreimal dieselbe, auch im Serien-Kontrollpaar. Absicherung
(„we're not entirely sure how reliably humans could start fire") kostet
erkennbar keine Reichweite. **Vorsicht bei der Deutung:** n = 6, ein Paar je
Kanal, Thema und Alter der Videos sind nicht kontrolliert — das ist eine
konsistente Korrelation, kein Kausalbeweis. Die sichere Lesart ist die
Negation: *Die These „glattes Behaupten gewinnt, Absichern kostet Klicks"
wird von diesen Daten nicht gestützt — eher das Gegenteil.*

**3. Quellenarbeit ist Inks Alleinstellungsmerkmal, nicht der
Nischenstandard.** Von den drei Kanälen zitiert genau einer — und es ist
der jüngste mit der niedrigsten Kadenz und ~9.560 $/Monat nach vier Monaten.
Historically kompensiert mit Marke und Humor, quack doc mit Volumen und
Themenhärte (dessen Katalog — Dashcam-Tode, Serienmörder, Kriegsverbrechen —
fiele übrigens großteils unter unsere eigenen Ausschlüsse und taugt nur
bedingt als Vorbild). Für einen neuen Kanal ohne Marke ist Inks Weg der
einzige der drei, der kopierbar ist.

### Konsequenz für die eigene Pipeline

Der Befund verzahnt sich direkt mit der Faktenprüfungs-Skizze oben: Die
Blockierregel kann um eine zweite, weichere Regel ergänzt werden — **eine
harte Behauptung gilt auch dann als gedeckt, wenn sie im Skript ausdrücklich
als unsicher markiert ist** („the most common theory is…"). Das ist maschinell
prüfbar (dieselbe Wortliste wie diese Messung), entspricht dem Stil der
Treffer-Videos und senkt den menschlichen Prüfaufwand: Was ehrlich als offen
gekennzeichnet ist, braucht keinen Beleg — nur was als Fakt auftritt.

## Nächste Schritte

1. Entscheidung History-Explainer ja/nein; bei ja: Teardown der 12
   Ink-Explainer-Videos nach dem Muster von `teardown/` für Kanal 1
   (Transkripte sind über NexLev ziehbar, 0 Credits).
2. Stilentscheidung aus `recherche/stile-erklaerkanal-2/` (Blaupause vs.
   Flat-Vector) gegen die Thumbnails der Nische testen.
3. In 4 Wochen `get_daily_analytics` auf Ink Explainer, Axen und Historically:
   wächst die junge Kohorte weiter?
4. Auf Wunsch: Top-Kanäle und Outlier-Videos ins NexLev-Swipefile übernehmen
   (nicht ausgeführt, da nicht beauftragt).
