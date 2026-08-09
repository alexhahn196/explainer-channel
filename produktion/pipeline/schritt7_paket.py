#!/usr/bin/env python3
"""
Schritt 7 - Upload-Paket.

Legt neben MP4, SRT und Platzhalterbild eine `upload.md` mit allem, was
beim Hochladen von Hand einzutragen ist. Der Upload laeuft bewusst nicht
automatisch: die **KI-Kennzeichnung** muss dabei gesetzt werden
(Formel §7/§8, Compliance-Entscheidung), und das Thumbnail ist zu dem
Zeitpunkt noch nicht final.

Aufruf:
    python3 produktion/pipeline/schritt7_paket.py V1
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gemeinsam import arbeit, config, hms, ordner  # noqa: E402
import vorlage                                     # noqa: E402


def mmss(s):
    s = int(round(s))
    return (f"{s//3600}:{(s%3600)//60:02d}:{s%60:02d}" if s >= 3600
            else f"{s//60}:{s%60:02d}")


def lade(video, name):
    p = arbeit(video, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def beschreibung_bauen(roh, kap_block):
    """Beschreibung fuer den Upload fertigstellen.

    Zwei Dinge, die vorher von Hand nachgezogen werden mussten:

    1. **Spendenlink raus.** Die Vorlagen in `videos-01-08.md` tragen die Zeile
       „Support the channel: [Spendenlink]" als Platzhalter fuer einen Link,
       den es nicht gibt. Ein Platzhalter in der veroeffentlichten
       Beschreibung ist schlimmer als keine Zeile.
    2. **Hashtags bleiben die letzte Zeile.** Der Kapitelblock gehoert davor,
       nicht dahinter - so sieht das V01-Paket aus, und YouTube zeigt die
       ersten drei Hashtags ueber dem Titel nur, wenn sie am Ende stehen.
    """
    zeilen = [z for z in roh.rstrip().split("\n")
              if not z.strip().lower().startswith("support the channel")]
    # nachlaufende Leerzeilen entfernen, die der entfernte Link hinterlaesst
    while zeilen and not zeilen[-1].strip():
        zeilen.pop()

    hashtags = []
    if zeilen and zeilen[-1].lstrip().startswith("#"):
        hashtags = [zeilen.pop()]
        while zeilen and not zeilen[-1].strip():
            zeilen.pop()

    if kap_block:
        zeilen += ["", "Kapitel:", kap_block]
    if hashtags:
        zeilen += [""] + hashtags
    return "\n".join(zeilen)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    a = ap.parse_args()
    cfg = config()
    nr = int(a.video[1:])
    v = vorlage.lies(a.video)
    ord_ = ordner(a.video)

    skript = lade(a.video, "skript.json")
    qs = lade(a.video, "qa_stimme.json")
    qm = lade(a.video, "qa_mix.json")
    qv = lade(a.video, "qa_video.json")
    qsrt = lade(a.video, "qa_srt.json")
    qb = lade(a.video, "qa_bild.json")
    marken = lade(a.video, "kapitelmarken.json") or []

    dateien = {n: os.path.exists(os.path.join(ord_, n)) for n in (
        f"video-{nr:02d}.mp4", f"video-{nr:02d}.srt", "PLATZHALTER_standbild.png")}

    # Kapitelmarken sind eine Entscheidung je Video, keine Eigenschaft der
    # Pipeline: videos-01-08.md empfiehlt ja bei 01/02/06/08, nein bei
    # 03/04/05/07 (Formel §7 fuehrt sie als optional). Schritt 6 erzeugt sie
    # immer; hier entscheidet sich, ob sie ins Paket kommen.
    erlaubt = [s.strip() for s in
               str(cfg.get("kapitelmarken_videos", "")).split(",") if s.strip()]
    if erlaubt and a.video not in erlaubt:
        marken = []

    kap_block = "\n".join(f"{mmss(m['zeit_s'])} {m['titel']}" for m in marken)
    beschreibung = beschreibung_bauen(v["beschreibung"], kap_block if marken else "")

    z = []
    z.append(f"# Upload — Video {nr:02d}\n")
    z.append("> Automatisch aus der Pipeline erzeugt. Alles unten wird beim Upload\n"
             "> **von Hand** eingetragen.\n")

    z.append("## Vor dem Upload zu erledigen\n")
    z.append('- [ ] **KI-Kennzeichnung setzen** („Altered or synthetic content" /')
    z.append('      „Realistic audio"). Die Stimme ist synthetisch. Formel §7 und §8')
    z.append('      führen das als Compliance-Entscheidung ohne Datenbeleg in beide')
    z.append('      Richtungen.')
    z.append('- [ ] **Thumbnail ersetzen.** Im Paket liegt nur')
    z.append('      `PLATZHALTER_standbild.png` — das ist das Standbild der Videospur,')
    z.append('      **nicht** das Thumbnail.')
    z.append(f"      Motivvorgabe: {v['thumb_motiv']}")
    z.append(f"      Thumbnail-Text: `{v['thumb_text']}` — Versalhöhe ≥ 11,5 % der")
    z.append('      Bildhöhe, Kontrast ≥ 10:1, höchstens 4 Wörter')
    z.append('      (`formel/thumbnail-checkliste.md`).')
    z.append("- [ ] Untertiteldatei hochladen (Sprache: Englisch).")
    z.append("- [ ] Sichtbarkeit/Zeitplan nach `produktion/videos-01-08.md` (5 Tage Abstand).\n")

    z.append("## Titel\n")
    z.append(f"```\n{v['titel']}\n```\n")

    z.append("## Beschreibung\n")
    z.append(f"```\n{beschreibung}\n```\n")

    z.append("## Tags\n")
    z.append("Formel §7: A hat auf **allen 8** Videos 0 Tags, B's drei gemessene Treffer\n"
             "ebenfalls 0. Sie kosten nichts — erwarte aber nichts von ihnen.\n")
    z.append("```\n" + ", ".join(v["tags"]) + "\n```\n")

    if marken:
        z.append(f"## Kapitelmarken ({len(marken)})\n")
        z.append("Formel §7: **optional, nicht Pflicht.** A's drei größte Treffer haben\n"
                 "null Kapitelmarken, B setzt sie durchgehend. Beide Muster gewinnen —\n"
                 "hier für die Nutzbarkeit gesetzt, nicht für die Reichweite.\n")
        z.append("Sie stehen bereits in der Beschreibung oben.\n")

    z.append("## Dateien im Paket\n")
    for n, da in dateien.items():
        z.append(f"- `{n}` {'✓' if da else '**FEHLT**'}")
    z.append("")

    z.append("## Messwerte dieses Renderlaufs\n")
    z.append("| Größe | Wert | Vorgabe |")
    z.append("|---|---|---|")
    if qv:
        z.append(f"| Laufzeit | {qv['dauer_hms']} ({qv['dauer_h']:.2f} h) | "
                 f"≥{cfg['laufzeit_min_h']} h, Ziel {cfg['laufzeit_ziel_von_h']}–"
                 f"{cfg['laufzeit_ziel_bis_h']} h |")
        z.append(f"| Dateigröße | {qv['groesse_mb']} MB | — |")
        z.append(f"| Bild | {qv['aufloesung']} @ {qv['fps']} fps | 1920×1080, 24–30 fps (§5) |")
        z.append(f"| Ton-Versatz | {qv['sync_versatz_s']} s | 0 |")
    if qs:
        z.append(f"| Tempo | {qs['wpm']} WPM | 120–160 WPM (§5b) |")
        z.append(f"| Sprachanteil (Lücken <1 s zugerechnet) | "
                 f"{qs['sprachanteil_vergleichbar_pct']} % | "
                 f"≥{cfg['sprachanteil_min_pct']} % (§3) |")
        z.append(f"| längste Pause | {qs['laengste_pause_s']} s | "
                 f"<{cfg['laengste_pause_max_s']} s (§3) |")
    if qm:
        z.append(f"| Abstand Stimme zu Bett | {qm['gemessener_abstand_db']} dB | "
                 f"{qm['soll_abstand_db']} dB (§5b) |")
        z.append(f"| Peak | {qm['peak_dbfs']} dBFS | <{cfg['peak_max_dbfs']} dBFS |")
    if qsrt:
        z.append(f"| Untertitelkacheln | {qsrt['kacheln']} | — |")
        z.append(f"| erste Kachel | {qsrt['erste_kachel_s']} s | "
                 f"Sprache in Sekunde 0–{cfg['sprachstart_max_s']} (§3) |")
    if skript:
        z.append(f"| CTA | {skript['bericht']['cta_anzahl']} | höchstens "
                 f"{cfg['cta_max']} (§3) |")
        z.append(f"| TTS-Zeichen | {skript['bericht']['zeichen_tts']:,} | — |"
                 .replace(",", "."))
    if qb:
        z.append(f"| Standbild dunkel | {qb['dunkelanteil_pct']} % der Fläche | "
                 f"dunkles Gesamtbild (§5) |")
    z.append("")

    z.append("## Stimme\n")
    z.append(f"`{cfg['stimme_name']}` — Fish Audio `{cfg['stimme_id']}`, "
             f"Modell {cfg['tts_modell']}, Tempo {cfg['prosody_speed']}.\n"
             f"Feste Kanalstimme, siehe `produktion/config.md`.\n")

    ziel = os.path.join(ord_, "upload.md")
    open(ziel, "w", encoding="utf-8").write("\n".join(z) + "\n")

    # Titel, Beschreibung und Tags zusaetzlich als nackte Textdateien: beim
    # Upload werden sie einzeln in die YouTube-Felder kopiert, und aus einer
    # Markdown-Datei mit Codebloecken herauszuschneiden ist fehleranfaellig.
    for name, inhalt in (("titel.txt", v["titel"]),
                         ("beschreibung.txt", beschreibung),
                         ("tags.txt", ", ".join(v["tags"]))):
        open(os.path.join(ord_, name), "w", encoding="utf-8").write(inhalt + "\n")

    print(f"\nPAKET {a.video}   {ord_}")
    for n, da in dateien.items():
        gr = (f"{os.path.getsize(os.path.join(ord_, n))/1e6:.1f} MB" if da else "FEHLT")
        print(f"  {'✓' if da else '✗'} {n:32s} {gr}")
    print(f"  ✓ upload.md                      "
          f"{os.path.getsize(ziel)/1000:.1f} kB, {len(marken)} Kapitelmarken")
    fehlend = [n for n, da in dateien.items() if not da]
    if fehlend:
        print(f"  ACHTUNG: {fehlend} fehlen")
    return 1 if fehlend else 0


if __name__ == "__main__":
    sys.exit(main())
