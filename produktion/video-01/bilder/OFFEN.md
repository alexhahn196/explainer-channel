# Offener Stand des Bildlaufs

**Erzeugt: 29 von 84.** Verbraucht: 86 Credits von der Grenze 500.

## Noch zu erzeugen (55)

M23 M24 M26 M27 M28 M29 M30 M31 M32 M33 M34 M35 M36 M37 M38 M39 M40 M41 M42 M43 M44 M45 M46 M47 M48 M50 M51 M52 M54 M56 M57 M58 M59 M60 M61 M63 M64 M65 M66 M67 M68 M69 M70 M71 M73 M74 M75 M76 M77 M78 M79 M80 M81 M82 M83

## Nachzulaufen (3)

| Motiv | Grund |
|---|---|
| M10 | türkises Boot in einer Landschaft, die unberührt sein soll |
| M16 | Signalelement liest sich als Buchstabe „P" |
| M22 | zwei türkise Objekte statt einem |

Für alle drei genügt der Zusatz `KEIN_SIGNAL` in `bildplan.py`
(`OHNE_SIGNAL`-Menge erweitern) — bei M10 zusätzlich „no boat, no canoe" im
Szenentext.

## So geht es weiter

`bildplan.py` erzeugt alle 84 Prompts deterministisch aus `szenen.md` plus den
Stilfestlegungen. `python3 bildplan.py` schreibt `bildplan.json`; daraus je
Motiv das Feld `prompt` an `generate_image_batch` (nano_banana_2, 16:9, 2k,
2,0 Credits je Bild), Stapel zu höchstens 11.

Prüfliste je Bild: Figur vorhanden wo vorgesehen · Brauen · Kopf etwa ⅕ ·
genau eine Lichtquelle beziehungsweise gerichteter harter Schatten · keine
verformten Hände · kein Text · nicht angeschnitten. Abbruchschwelle: mehr als
drei Fehlschläge in einem Stapel.
