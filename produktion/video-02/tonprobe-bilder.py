#!/usr/bin/env python3
"""Was die zwei Fassungen an Bildern VERLANGEN.

Die Frage des Zusatzes vom 16.08.2026 ist nicht, wie der Text klingt,
sondern was er dem Bildplan aufzwingt. Vorgabe: hoechstens 10 % der
Laufzeit als Schema. Video 1 lag bei 26 %, der Sterne-Entwurf bei 58 %.

Die Zuordnung unten ist ein Urteil, keine Messung — sie sagt, welches
Bild eine Stelle verlangt, wenn man sie nicht anders zeigen kann.
Bei der bestehenden Fassung sind es die Motive aus szenenplan.py; bei
der neuen die Motive, die sie noetig machen wuerde.
"""
from __future__ import annotations

import pathlib

HIER = pathlib.Path(__file__).resolve().parent
WPM = 219

# (Wortlaut-Anfang, Art, Begruendung)
# Art: "welt" = Ort, Mensch, Gegenstand · "schema" = Zeichnung
ALT = [
 ("Look up tonight and pick a star. Any star you like.", "welt",
  "Nachthimmel ueber einer Strasse"),
 ("Now ask yourself: how far away is that thing?", "welt",
  "Person von hinten unter dem Himmel"),
 ("If you draw a blank, you're in good company.", "welt", "dieselbe Person"),
 ("In a survey of more than three thousand people,", "schema",
  "vier Figurenumrisse, Sonne und Stern uebereinander (M03)"),
 ("Asked to put a number on the nearest star,", "schema",
  "sechs Figuren, fuenf leere Gedankenblasen (M04)"),
 ("Of those who did, only one in five landed", "schema",
  "Raster aus hundert Punkten, drei markiert (M05)"),
 ("So how do astronomers know? Here's the answer,", "schema",
  "das Parallaxendreieck (M06)"),
 ("No probe flies out there. No radar comes back.", "schema",
  "Sonde und Radarschuessel durchgestrichen (M07)"),
 ("You measure an angle, twice, half a year apart", "schema",
  "Parallaxendreieck erneut (M06)"),
 ("And you already own the trick. Hold up your thumb", "welt",
  "Daumen vor der Wand (M09)"),
 ("Now swap eyes. Your thumb jumps against the wall", "welt",
  "derselbe Daumen, versetzt (M10)"),
 ("— because each of your eyes looks from its own spot.", "schema",
  "zwei Augen im Profil mit Sichtlinien (M11)"),
 ("To do the same with a star, you need two viewpoints", "schema",
  "Sonne, Erdbahn, zwei Erden (M12)"),
 ("Photograph a near star from both.", "welt",
  "Sternfeld, Stern links (M13)"),
 ("it jumps — just like your thumb did.", "welt",
  "dasselbe Feld, Stern rechts (M14)"),
 ("Half of that jump, as an angle, is called the parallax.", "schema",
  "Parallaxendreieck erneut (M06)"),
 ("One clean rule ties it to distance:", "schema",
  "zwei Sterne mit grossem und kleinem Versatz (M15)"),
 ("Simple? You'd think so. The catch:", "schema",
  "Zeitstrahl mit zwei Marken (M16)"),
 ("Copernicus set the Earth moving in 1543,", "welt",
  "Mann in Talar an der Armillarsphaere (M17)"),
 ("and the objection came at once:", "schema",
  "zwei Sternhimmel gegeneinander versetzt (M18)"),
]

NEU = [
 ("You're outside, and it's dark. Look up. Pick a star.", "welt",
  "Nachthimmel ueber einer Wohnstrasse"),
 ("Now answer me: how far away is your star?", "welt",
  "Person von hinten, Kopf im Nacken"),
 ("Nothing comes. You're not alone in that. More than three thousand", "welt",
  "Passanten auf einem Platz, achselzuckend, einer zeigt nach oben — "
  "die Zahlen traegt die Stimme, nicht die Grafik"),
 ("So there you stand in the street with no answer.", "welt",
  "dieselbe Person, wieder allein in der Strasse"),
 ("What you need is a triangle. Here is how you build yours.", "schema",
  "AUSNAHME: das Parallaxendreieck. Die Antwort des Videos, ohne "
  "Zeichnung nicht zu zeigen"),
 ("Put your thumb up, arm straight out, and shut your left eye.", "welt",
  "Daumen vor der Wand mit Bildhaken"),
 ("Now swap eyes. Your thumb jumped.", "welt",
  "derselbe Daumen, jetzt rechts vom Haken"),
 ("Your two eyes sit apart, and each one looks past your thumb", "welt",
  "Nahaufnahme des Gesichts von der Seite, ein Auge zu"),
 ("Now you need two spots much further apart. Stand in this street", "welt",
  "dieselbe Strasse im Januar, Schnee, kahle Baeume"),
 ("Come back in July and stand on the same flagstone.", "welt",
  "dieselbe Strasse im Juli, identischer Ausschnitt — Zustandspaar"),
 ("You never lifted a foot, and you have moved three hundred million", "welt",
  "Fuesse auf demselben Pflasterstein, von oben"),
 ("Photograph a near star from both ends of your ride, and it jumps.", "welt",
  "Sternfeld, der eine Stern versetzt — Zustandspaar wie beim Daumen"),
 ("A man in Königsberg spent two years catching that jump", "welt",
  "Sternwarte bei Nacht, Kuppel, kahle Baeume"),
 ("His telescope had its main lens sawn clean in half,", "welt",
  "Nahaufnahme der zersaegten Objektivlinse"),
 ("Night after night he turned the screw", "welt",
  "Mann am Okular, Hand an der Mikrometerschraube"),
 ("until two images of one faint star lay exactly on top of each other.",
  "welt", "Blick durchs Okular: zwei Sternbilder, dann deckungsgleich"),
 ("Then he read the screw off by lamplight.", "welt",
  "Nahaufnahme Skala und Zeiger, Oellampe daneben"),
 ("That reading was the jump. Half of it, drawn as an angle,", "schema",
  "AUSNAHME: der Winkel am Dreieck, kurz — Rueckgriff auf die erste "
  "Ausnahme, kein neues Bild"),
 ("Small jump, far star. That is the whole rule,", "welt",
  "zurueck zur Person in der Strasse, Blick nach oben"),
]


def rechne(name: str, stellen: list, text: str) -> None:
    w = len(text.split())
    # Wortanteil je Stelle aus der Position der Anfaenge im Text
    worte = text.split()
    # Ueber die ganze Anfangsphrase ankern, nicht ueber das erste Wort.
    # Ein einzelnes "A" oder "Your" trifft sonst irgendwo im Text — derselbe
    # Fehler wie seinerzeit in aussprache_qa.py.
    def norm(x):
        return x.strip(".,:;—?!\u2019'\"").lower()

    starts, ab = [], 0
    for anfang, _, _ in stellen:
        phrase = [norm(x) for x in anfang.split()][:5]
        treffer = None
        for k in range(ab, len(worte) - len(phrase) + 1):
            if [norm(x) for x in worte[k:k+len(phrase)]] == phrase:
                treffer = k
                break
        if treffer is None:
            raise SystemExit(f"Anker nicht gefunden: {anfang[:60]!r}")
        starts.append(treffer)
        ab = treffer + 1
    laengen = [(starts[i+1] if i+1 < len(starts) else w) - starts[i]
               for i in range(len(starts))]
    sek = [x / WPM * 60 for x in laengen]
    ges = sum(sek)
    s_sek = sum(t for t, (_, art, _) in zip(sek, stellen) if art == "schema")
    n_s = sum(1 for _, art, _ in stellen if art == "schema")
    print(f"\n### {name}")
    print(f"{len(stellen)} Bildstellen · {ges:.0f} s · "
          f"Schema {n_s} von {len(stellen)} = "
          f"**{s_sek/ges*100:.0f} % der Laufzeit**")
    print()
    print("| s | Art | Bild | Wortlaut |")
    print("|---:|---|---|---|")
    for (anfang, art, bild), t in zip(stellen, sek):
        kennz = "**Schema**" if art == "schema" else "Welt"
        print(f"| {t:.1f} | {kennz} | {bild} | {anfang[:52]}… |")


if __name__ == "__main__":
    alt = (HIER / "tonprobe-alt.txt").read_text(encoding="utf-8")
    neu = (HIER / "tonprobe-neu.txt").read_text(encoding="utf-8")
    rechne("Bestehend", ALT, alt)
    rechne("Neu", NEU, neu)
