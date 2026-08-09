# Produktions-Pipeline

Erzeugt aus einem Videoblock in `produktion/videos-01-08.md` ein fertiges
Upload-Paket: MP4, SRT, Platzhalterbild, `upload.md`.

```bash
export FISH_KEY='…'
python3 produktion/pipeline/render.py V1 --bild pfad/zum/standbild.png
```

Für Video 02–08 identisch, nur mit anderem Parameter. Jeder Schritt ist auch
einzeln aufrufbar (`--nur 3`, `--ab 5`) und setzt wieder auf: bereits erzeugte
Chunks werden nicht neu generiert.

**`--bild` ist Pflicht, sobald ein geprüftes Standbild existiert.** Ohne das
Argument erzeugt Schritt 4 ein einfaches Ersatzbild und überschreibt damit das
vorhandene `PLATZHALTER_standbild.png` — der nackte Aufruf `render.py V3`
zerstört also stillschweigend ein bereits abgenommenes Motiv.

| Schritt | Datei | Was er tut |
|---|---|---|
| 1 | `schritt1_text.py` | Korpus (WEBBE) holen, Hook + CTA + Gebet voranstellen, Versalien für die TTS entschärfen |
| 2 | `schritt2_tts.py` | Chunks an Satzenden, parallel synthetisieren, sample-exakt fügen, vermessen |
| 3 | `schritt3_bett.py` | Klangbett loopen und unterlegen, Pegel messen |
| 4 | `schritt4_bild.py` | Standbild prüfen/erzeugen (PLATZHALTER) |
| 5 | `schritt5_video.py` | Videospur mit Zoom, Montage zu MP4, Sync prüfen |
| 6 | `schritt6_srt.py` | Untertitel mit gemessenen Zeiten, Kapitelmarken |
| — | `qa_namen.py` | Aussprache-QA der Eigennamen (läuft nach Schritt 6 automatisch mit) |
| 7 | `schritt7_paket.py` | `upload.md` mit Titel, Beschreibung, Tags, Kapitelmarken, Messwerten |
| — | `rhotik.py` | Akzentmessung einer Stimme (F3-Formant), nur bei Stimmwechsel nötig |

Alle festen Werte stehen in `produktion/config.md` und **nur dort**. Die
Zwischenstände liegen unter `produktion/arbeit/` und sind nicht im Repository.

---

## Wo die Dokumente deine Vorgabe geschlagen haben

Auftrag: *„Bei Widerspruch gewinnen die Dokumente — sag mir wo."* Drei Stellen.

### 1. Videospur: „statisch" war nicht wählbar

Du hast „sehr langsamer Zoom **oder statisch**" freigestellt.

> **Formel §5, PFLICHT:** „Ein Standmotiv mit **sanfter Bewegung**, kein
> Szenenschnitt. 11 von 11 Stichproben zeigen Bewegung, aber immer ruhige:
> Feuerflackern, driftende Wolken, funkelnde Sterne, langsamer Zoom."
> `teardown/produktions-spec.md` sagt es noch direkter: „Nie ein echtes Standbild."

Umgesetzt ist deshalb der Zoom. Er kostet fast nichts: das Bild bewegt sich so
langsam, dass die Bildspur trotzdem bei rund 20 kbit/s landet.

### 2. Vorlauf: 4 Sekunden Bett allein wären ein Verstoß gewesen

`stimmtest/musik-prompt.md` schreibt „Vorlauf 4 s Bett allein, 3 s Einblende".

> **Formel §3, PFLICHT:** „Sprache beginnt in Sekunde 0–3. Kein Musikintro,
> kein Logo, kein Vorspann." (n=24; Gewinner 0,1–3,1 s.)

4 s Bett allein sind genau das verbotene Musikintro. `musik-prompt.md` steht
nicht in der Verbindlichkeitsliste, Formel §3 schon — deshalb **1,5 s Vorlauf
mit 1,5 s Einblende**. Die Stimme setzt bei 1,5 s ein.

### 3. Reihenfolge: Gebet nach hinten

Du hast gesagt „Eingangsgebet voranstellen". Das Gebet steht vor dem Korpus,
aber **hinter** Hook und CTA — sonst wäre die CTA-Vorgabe gerissen:

> **Formel §3, PFLICHT:** „CTA: maximal 2 pro Video", laut Vorlage „beide in
> den ersten 60 s".

Das Gebet dauert bei diesem Tempo 1 min 52 s. Vor die CTAs gesetzt, hätte
CTA 1 erst bei 105 s gelegen. Jetzt: Hook 0–21 s, CTA 1 bis 32 s, CTA 2 bis
38 s, Gebet bis 116 s, dann Psalm 1. Formel §3 hält ausdrücklich fest, dass
ein **festes** Schema Hook→CTA→Gebet→Lesung *nicht* belegt ist — die
Reihenfolge ist also eine Planungsentscheidung innerhalb belegter Grenzen,
kein Datenbefund.

---

## Wo die Dokumente sich untereinander widersprechen

Aufgelöst nach der Verbindlichkeitsliste in `produktion/videos-01-08.md`
(Formel v2.1 → erfolgsregeln → produktions-spec).

| Thema | Widerspruch | Verwendet |
|---|---|---|
| Laufzeitband | Formel §2: 3,4–3,8 h · erfolgsregeln M6: 3,2–4,0 h · produktions-spec: 2,5–3,5 h | **3,4–3,8 h** (Formel §2). Ergebnis 3,58 h liegt über der produktions-spec-Obergrenze 3,5 h. |
| Sprechtempo | Formel §5b: 120–160 WPM · produktions-spec: 135–145 WPM | Beides erfüllt: gemessen **140,4 WPM**. |
| Bett-Loop | musik-prompt: „mit übergeblendeter Naht" | Nicht nötig: die Naht der verwendeten Datei springt um 0,0016 — der größte Samplesprung *innerhalb* des Betts ist 0,0998, also 60-mal größer. |

### Die 12-dB-Regel ist nicht gemessen

Du hast sie als „die einzige harte Abmischregel **aus den Daten**" vorgegeben.
Halb richtig, und die Hälfte ist wichtig:

- **Aus den Daten stammt:** „Stimme in 6/6 Fällen klar über dem Bett"
  (Formel §5b) — rein qualitativ, ein Höreindruck.
- **Nicht aus den Daten stammt: die Zahl 12.** `regeln/daten/stimm_stichprobe.json`
  enthält keinen einzigen dB-, RMS- oder LUFS-Wert. Die 12 dB stehen erstmals in
  `stimmtest/musik-prompt.md` und sind dort abgeleitet, nicht gemessen.

Umgesetzt und exakt eingehalten (12,0 dB) — aber als getroffene Entscheidung,
nicht als Datenbefund. Wenn dir die Stimme zu weit vorn oder zu weit hinten
sitzt, ist das eine Geschmacksfrage ohne Datenkonflikt: `abstand_soll_db` in
`config.md` ändern.

---

## Wo kein Dokument etwas sagt

Hier hat die Pipeline entschieden, weil sie entscheiden musste:

- **Encoding.** `regeln/erfolgsregeln.md` führt ausdrücklich als Negativbefund,
  dass es zu Codec, Bitrate, Auflösung und Dateigröße **keine** Daten gibt.
  Gewählt: H.264, CRF 28, AAC 192 kbit/s. Für ein fast unbewegtes dunkles Bild
  reicht das; der Ton ist der einzige Teil, der Bitrate braucht.
- **Chunk-Größe und Nahtqualität.** Kein Dokument kennt Chunks. 1800 Zeichen,
  nur an Satzenden, Pegel zwischen den Chunks angeglichen.
- **Zoom-Zyklus 300 s, Faktor 1,04.** „Langsam" ist belegt, eine Zahl nicht.
- **Absolute Lautheit (LUFS).** Belegt ist nur der *Abstand*, nie ein Zielpegel.
- **99 Kapitelmarken.** Belegt sind bei B 40–93 Marken; 99 liegt knapp darüber.
  Formel §7 führt Kapitelmarken ohnehin als optional (A's drei größte Treffer
  haben null).

## Zwei belegte Dinge, die bewusst fehlen

Beide stehen in Formel §5 und `produktions-spec` als belegtes Muster, aber
nicht als PFLICHT — und du hast sie nicht beauftragt:

- **Eingebrannte Untertitel** (weiß, zentriert, unteres Drittel; 6 von 11
  Stichproben). Die Pipeline liefert stattdessen eine SRT-Spur. Ein Burn-in
  würde die Bildbitrate vervielfachen und muss pro Video neu gerendert werden.
- **Kanal-Wasserzeichen** klein in einer Ecke (6 von 11).

Beides ist nachrüstbar, sollte aber eine bewusste Entscheidung sein.
