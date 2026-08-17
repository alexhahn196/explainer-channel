# Auslieferung — die fertigen Videos, zerlegt

> **Beide Videos liegen hier vollständig**, aufgeteilt in je vier Teile.
> Zusammensetzen: `sh zusammensetzen.sh` — das Skript prüft dabei die
> Prüfsumme jeder Datei.
>
> **Nichts wurde zu YouTube hochgeladen.**

## Warum zerlegt

Ein einzelnes 144-MB-Video lässt GitHub nicht durch: die harte Grenze liegt
bei **100 MB je Datei**. Vier Teile je Video kommen mit rund 36 MB durch.

Der Weg über einen Dateihoster hat sich als untauglich erwiesen. Der
GoFile-Link zu Video 2 (`gofile.io/d/L5O1u46m`) war **nach wenigen Stunden
tot** — „this content does not exist". Der zu Video 1
(`gofile.io/d/3D8jBNJc`) mit derselben Ursache. Ein Link, der verfällt, ist
keine Sicherung; das Repository ist einer.

## Die Dateien

| Video | Teile | Summe | MD5 der zusammengesetzten Datei |
|---|---|---|---|
| `video-01.mp4` | `video-01.mp4.00.part` … `.03.part` | 149.320.007 B = 142,4 MB | `26402718c0675a5b7b1065ae08f75e08` |
| `video-02.mp4` | `video-02.mp4.00.part` … `.03.part` | 151.231.124 B = 144,2 MB | `0f8d29e369313381f084b17f72c4ff5b` |

Beide Prüfsummen sind die aus den Abschlussberichten
(`video-01/ABSCHLUSS.md`, `video-02/ABSCHLUSS.md`) — die Dateien sind also
nachweislich dieselben, die dort beschrieben und geprüft wurden. Sie sind
**nicht** neu gerendert worden; sie lagen im Container noch vollständig vor.

## Von Hand zusammensetzen

Wer das Skript nicht benutzen will:

```sh
cat video-01.mp4.*.part > video-01.mp4
cat video-02.mp4.*.part > video-02.mp4
md5sum video-01.mp4 video-02.mp4
```

Die Reihenfolge ergibt sich aus dem Namen; `*` sortiert `.00`, `.01`, `.02`,
`.03` richtig. Erzeugt wurden die Teile mit
`split -n 4 -d --additional-suffix=.part`.

## Was in den Videos steckt

| | Video 1 | Video 2 |
|---|---|---|
| Titel | Who Built the First Roads and Why? | How Do We Know How Far Away the Stars Are? |
| Laufzeit | 8:59,3 | 10:16,2 |
| Einstellungen | 139 | 159 aus 66 Motiven |
| Bild | 1920×1080, 30 fps, H.264 | 1920×1080, 30 fps, H.264 |
| Ton | AAC 192 kb/s, 44,1 kHz, mono | AAC 154 kb/s, 44,1 kHz, mono |
| Stimme | ElevenLabs Eric, Seed 4242 | ElevenLabs Eric, Seed 4242 |
| Tempo | 213,8 WPM | 202,0 WPM |
| Credits | 228 | 222 |

Die Textbausteine für den Upload — Titel, Beschreibung mit
KI-Kennzeichnung, Kapitel, Untertitel, Thumbnail-Kandidaten — liegen je
Video unter `video-0X/upload/`.

**Beim Hochladen ist die KI-Kennzeichnung zu setzen.** Bild und Stimme sind
in beiden Videos erzeugt.
