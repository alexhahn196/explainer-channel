# Video 1 — Abschlussbericht

> Stand 15.08.2026. Das Video ist fertig montiert und geprüft.
> **Nichts wurde zu YouTube hochgeladen.**

## Das Ergebnis

| | |
|---|---|
| Datei | `video-01.mp4`, **142,4 MB**, MD5 `26402718c0675a5b7b1065ae08f75e08` |
| Laufzeit | **8:59,3** — 139 Einstellungen |
| Bild | 1920×1080, 30 fps, H.264, mittlere Bitrate 2.050 kb/s |
| Ton | AAC 192 kb/s, 44,1 kHz, mono |
| Stimme | ElevenLabs **Eric** `cjVigY5qzO86Huf0OWal`, `eleven_multilingual_v2` |
| **Seed** | **4242** — ohne ihn streut die Laufzeit um bis zu 23 WPM |
| `speed` | 1,1955 · stability 0,5 · similarity_boost 0,75 · style 0,0 |
| Gemessenes Tempo | **213,8 WPM** über die ganze Spur |
| TTS-Zeichen | **10.078** gesendet (Grenze war 20.000) |
| Bilder | **84 von 84**, `nano_banana_2` → substituiert zu `nano_banana_flash`, 16:9, 2k |
| **Credits** | **228 von 500** |

Die Videodatei liegt **im Repository**, in vier Teilen unter
[`produktion/auslieferung/`](../auslieferung/) — zusammensetzen mit
`sh zusammensetzen.sh`, das Skript prüft die Prüfsumme.

**Nachtrag 17.08.2026:** Der ursprüngliche Weg war ein Dateihoster, und der Link
`gofile.io/d/3D8jBNJc` ist **verfallen**. Damit war dieses Video zwei Tage lang
nirgends abholbar, obwohl der Bericht es als gesichert auswies. Die Datei lag im
Container noch vollständig vor, mit unveränderter Prüfsumme; sie ist jetzt im
Repository.

## Was geprüft wurde, und wie

Nicht „ffmpeg lief durch", sondern jedes Mal die inhaltliche Frage.

| Prüfung | Weg | Ergebnis |
|---|---|---|
| Steht an jeder Stelle das richtige Bild? | 35 Stichproben aus dem fertigen Video, Farbhistogramm gegen alle 84 Motive | **35/35** |
| Aussprache aller Eigennamen | zwei lokale Spracherkenner, volle Ausrichtung gegen den Solltext | **22 Stellen, 0 Fehlformen** |
| Signalfarbe | `tuerkis.py`, Zusammenhangskomponenten | **kein Bild über der Obergrenze** |
| Nachtmotive | mittlere Helligkeit gegen die Tagszene M56 (133,9) | M57 **55,5** · M79 **69,4** · M80 **47,0** |
| Untertitel | Überlappung, Lücken, Zeilenlänge | 173 Blöcke, **0 Überlappungen** |
| Videodatei | vollständiger Dekodierlauf | **fehlerfrei** |

### Die Aussprache im Einzelnen

Die kritische Stelle sitzt: **Dümmer** wird als *Diemer* gehört, nie als
*dumber* — das war der eine Fehler, der nicht stehenbleiben durfte. Alle sieben
Zahlformate kommen als Ziffernpaare. Zwei Abweichungen bleiben:

- **Susa** klingt als *Suso* / *Susu* — die Endsilbe ist zu rund geraten.
- **Widan el-Faras** hören die beiden Erkenner verschieden (*Wiedan El Farras*
  gegen *Huitan el Faras*); erkennbar ist der Name bei beiden.

**Betonung ist auf diesem Weg nicht prüfbar.** Ein Erkenner schreibt
„Tiwanaku", gleich ob die erste oder die dritte Silbe betont war. Das steht
hier ausdrücklich, weil der Bericht sonst mehr zu wissen vorgäbe als er weiß.

## Der Schnitt sitzt am Wort, nicht am Rechenwert

`szenen.md` ist auf 219 WPM gerechnet und ergibt 8:34. Die fertige Spur läuft
8:58 — **24 Sekunden mehr**. Die Einstellungen gleichmäßig zu strecken wäre
falsch gewesen: die Schnitte liegen auf Satzgrenzen, gestreckt läge am Ende
jeder Schnitt mehrere Sekunden neben seinem Satz.

Stattdessen ist jede der 139 Einstellungen **an ihrem eigenen Wortlaut
verankert**. `szenen.md` nennt zu jeder den Text, und aus den
ElevenLabs-Zeitmarken ist bekannt, wann jedes Zeichen gesprochen wird. Die 24
Sekunden verteilen sich damit von selbst dorthin, wo tatsächlich länger
gesprochen wird. Keine Einstellung liegt unter 1 s oder über 9 s.

## Was schiefging und was daraus zu lernen ist

### Der wiederkehrende Mechanismus

**Was der Prompt nicht benennt, rät das Modell aus der nächstliegenden
Bildkonvention.** Dreimal derselbe Fehler in verschiedener Kleidung:

1. Fehlende Epochenzeile → ägyptische Kleidung im Chaco Canyon.
2. Fehlende Pflanzenangabe → Saguaro-Kakteen in den Anden (M67, M70).
3. Fehlende Architekturangabe → römische Bogenbrücke bei den Inka.

Behoben durch Benennen: Epoche, **Flora je Kulturraum** (acht Räume, 51
Motive), **Bogenverbot** für Inka-Bauten.

### Wo ich mir selbst im Weg stand

- Der SIGNAL-Block enthielt einen Satz, den ich selbst geschrieben hatte:
  *„If no single object needs marking, the turquoise is absent."* Ein Freibrief
  zum Weglassen — dreizehn Bilder nahmen ihn. Nach der Entscheidung vom
  15.08. ist das kein Fehler mehr, sondern die Regel: Türkis ist **erlaubt,
  nie Pflicht, höchstens eins.**
- Die Verdunkelungsformel für M57 war so scharf, dass das Modell die
  kennzeichnende babylonische Architektur fallen ließ und eine Lehmziegelgasse
  lieferte. Dunkelheit fordern, ohne den Bildinhalt wegzudrücken.
- Die Flora-Zeile las sich als Auftrag, Pflanzen zu setzen, und holte eine
  Dattelpalme in eine Innenstadtszene. Jetzt ausdrücklich als Einschränkung
  formuliert.

### Wo das Messen das Auge schlug

**M80 hätte ich durchgehen lassen.** Mond und brennende Laterne im Bild — es
sah nach Nacht aus. Gemessen lag es mit mittlerer Helligkeit **138 über der
Tagszene M56 mit 134**. Erst die Zahl zeigte es.

Umgekehrt: der Türkis-Zähler meldete 13 Verstöße, von denen **genau einer echt
war** (M38 mit drei Gegenständen). Die anderen zwölf waren ein Objekt, das an
inneren Konturlinien zerfiel.

**Beides zusammen ist die Lehre:** messen, wo das Auge täuscht — nachsehen, wo
die Zahl täuscht. Der Türkis-Zähler ist darum ausdrücklich als **Vorfilter**
dokumentiert, nicht als Urteil.

### Zwei Messversuche, die nichts taugten

Ehrlichkeitshalber, weil beide fast in den Bericht gerutscht wären:

1. **Stilabweichung messen.** Anteil exakt einfarbiger 3×3-Umgebungen: liegt
   bei *jedem* Bild bei 0 %, weil der Generator ein schwaches Rauschen über
   alle Flächen legt. Dann die Verteilung des lokalen Gradienten: misst
   Szenendichte statt Schattierung — M12, längst angenommen, lag höher als das
   beanstandete M69. **Die Stilprüfung blieb Augenschein.**
2. **Aussprache-Ortung über Ankerwörter.** Kurze Anker wie „to the" treffen
   dutzendfach; die Prüfung für *Ishtar* landete fünf Absätze zu früh, und drei
   gemeldete Fehlformen waren reine Ortungsfehler. Ersetzt durch die
   vollständige Ausrichtung gegen den Solltext.

## Was offen bleibt

- **Kein Thumbnail.** `config.md` führt den Thumbnail-Stil ausdrücklich als
  nicht gemessen. Vier Kandidatenbilder liegen in
  `upload/thumbnail-kandidaten/` in 1280×720; welches taugt und welcher Text
  daraufgehört, ist eine Entscheidung, keine Ableitung.
- **Susa und Widan el-Faras** wie oben — hörbar unsauber, nicht falsch.
- **KI-Kennzeichnung** beim Hochladen von Hand setzen: „Altered or synthetic
  content". Stimme und Bilder sind vollständig erzeugt.
