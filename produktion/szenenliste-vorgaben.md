# Szenenliste — Vorgaben für die Kamerafahrt

**Stand 2026-08-17.** Verbindlich für **alle** künftigen Videos dieses
Kanals.

> Eine konkrete Szenenliste gibt es noch nicht — die Pipeline ist auf dieses
> Format noch nicht umgebaut (`README.md`: „nicht gebaut"). Diese Datei legt
> **jetzt** fest, wie eine Einstellung ihre Kamerafahrt angibt, damit die
> erste Szenenliste das Feld von Anfang an richtig trägt und die Frage nicht
> je Video neu verhandelt wird.

## Die Regel in einem Satz

**Voreinstellung ist `statisch`. Eine Fahrt wird begründet, nicht
weggelassen.**

Bei 3–4 s je Einstellung und 120–300 Einstellungen je Video entsteht die
Bewegung durch den **Schnitt**. Das Vorbild bewegt die Kamera „fast nur auf
Karten" (`recherche/stil-ink-explainer.md`, Zeile 84). Eine Fahrt, die nichts
zeigt, ist Zierrat — und ein statisches Bild ist messbar **das schärfste**,
das aus der Quelle zu holen ist (Kantenschärfe 0,964 gegen 0,908 bei Fahrt).

Es gibt hier **keine Bewegungspflicht.** Die Formel-§5-Vorgabe „Standmotiv
mit sanfter Bewegung" stammt aus BibelTube und gilt für diesen Kanal
ausdrücklich nicht (`README.md`, `config.md`).

## Wann eine Fahrt gerechtfertigt ist

Wenn die Bewegung **etwas zeigt, das ein Standbild nicht zeigt**:

| Zulässig | Beispiel |
|---|---|
| eine Karte abfahren | Handelsweg von A nach B nachziehen |
| eine Zeitleiste entlanggehen | Jahreszahlen nacheinander in den Blick holen |
| ein Diagramm erschließen | vom Ganzen auf den entscheidenden Teil zu |
| auf ein Detail zugehen, das der Text gerade nennt | „und genau hier saß der Fehler" |

Nicht zulässig als Begründung: „damit sich etwas bewegt", „gegen
Langeweile", „weil die Einstellung sonst leer wirkt". Wenn eine Einstellung
leer wirkt, ist sie zu lang oder das Bild ist falsch.

## Die Felder je Einstellung

| Feld | Werte | Vorgabe |
|---|---|---|
| `fahrt` | `statisch` \| `fahrt` | **`statisch`** |
| `zoom_von` / `zoom_bis` | 1,00–1,15 | `1.00` / `1.06` |
| `schwenk_x` / `schwenk_y` | −1,0 … +1,0 | `0.0` |
| `grund` | Freitext | **Pflicht, sobald `fahrt`** |

`schwenk_x`/`schwenk_y` geben an, wie weit der Ausschnitt bis zum Ende an den
Rand des **verfügbaren** Wegs wandert; `0` bleibt mittig, `±1` geht bis an
den Rand. Der verfügbare Weg entsteht erst durch den Zoom — **ein reiner
Schwenk braucht deshalb `zoom_von = zoom_bis > 1.0`** (z. B. beide `1.08`).
`kamerafahrt.py` lehnt einen Schwenk ohne Zoom mit einer Fehlermeldung ab.

### Grenzen

- **`zoom_bis` höchstens 1,15.** Darüber wird bei 2752‑px‑Quellen echtes
  Detail hochgerechnet: scharf bleibt eine Fahrt nur bis
  Quellbreite ÷ Ausgabebreite = 2752 ÷ 1920 ≈ **1,43**, und schon vorher
  wird es weich. `kamerafahrt.quelle_pruefen()` warnt automatisch.
- **Fahrt nicht unter 2 s.** Kürzer wirkt sie wie ein Ruck, nicht wie eine
  Kamerabewegung.
- **Nicht zwei Fahrten hintereinander in dieselbe Richtung** — das liest
  sich als eine einzige, vom Schnitt zerhackte Bewegung.

## Wie es gerendert wird

Ausschließlich über
[`produktion/pipeline/kamerafahrt.py`](pipeline/kamerafahrt.py):

```python
kamerafahrt.bauen(bild, ziel, dauer_s, cfg,
                  art="fahrt", zoom_von=1.0, zoom_bis=1.06, schwenk_x=0.0)
```

**Keinen `zoompan`-Aufruf von Hand schreiben.** Der Grund steht im Kopf von
`kamerafahrt.py` und ausführlich in
[`recherche/kamerafahrt-proben/README.md`](../recherche/kamerafahrt-proben/README.md):
`zoompan` rastet den Ausschnitt auf ganze Quellpixel, das Bild zittert dann
um einen ganzen Pixel — bei unserer Bildwelt (flache Grafiken, harte
Konturen) deutlich sichtbar. Gemessen 0,998 px; über den Standardweg
0,150 px.

## Was das Bild mitbringen muss

- **Mindestens 2074 px Breite** bei 1920 px Ausgabe und Zoom bis 1,08
  (= Ausgabebreite × größter Zoomfaktor), sonst wird die Fahrt am Ende
  weich. Unsere Quellen liefern 2752 px.
- Eine zu kleine Quelle ist ein **Schärfe**-, kein Zitterproblem — das
  Zittern ist vom Standardweg unabhängig von der Quellgröße erledigt.
- Motive mit sehr feinem, regelmäßigem Muster (Raster, enge Schraffuren)
  besser `statisch`: dort erzeugt jede Skalierung Moiré, und das fällt in
  Bewegung stärker auf als im Standbild.
