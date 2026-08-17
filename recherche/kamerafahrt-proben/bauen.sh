#!/bin/bash
# Baut die drei Probeclips aus EINEM vorhandenen Bild.
# Identische Laufzeit, identische Bewegungsamplitude, identische Kodierung -
# der einzige Unterschied ist der Weg, auf dem die Kamerafahrt entsteht.
set -euo pipefail

REPO=/home/user/explainer-channel
QUELLE="$REPO/recherche/stile-erklaerkanal/stil-1-flatvector-szeneA.png"
AUS=/tmp/claude-0/-home-user-explainer-channel/e8958594-fe41-504a-b4de-0632065fe225/scratchpad/jitter
FPS=24
SEK=6
N=$((FPS * SEK))          # 144 Frames
ZOOM=0.08                 # 1,00 -> 1,08
PAN=0.35                  # Anteil des freien Wegs, den der Schwenk nutzt

# Alle drei Clips gleich kodieren. CRF 16 statt der 28 aus config.md:
# sonst vergleicht man Kamerafahrt UND Codec gleichzeitig.
ENC=(-c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p
     -x264-params "keyint=48:min-keyint=48:scenecut=0" -an -movflags +faststart)

# Kosinus-Rampe, in beiden Fahrten identisch. zoompan zaehlt `on` ab 1.
RAMPE="(1-cos(PI*on/$N))/2"
Z="1+$ZOOM*$RAMPE"
XE="(iw-iw/zoom)*(0.5+$PAN*$RAMPE)"
YE="(ih-ih/zoom)/2"

echo "== Arbeitsvorlagen =="
# (a) genau wie schritt4_bild.py::zuschneiden(): 16:9 beschneiden, LANCZOS
#     auf 1920x1080 - die 2752 px der Quelle sind ab hier weg.
ffmpeg -y -loglevel error -i "$QUELLE" \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080" \
  "$AUS/vorlage-1080.png"

# (b) Ueberabtastung: die Quelle einmal auf 4x Ausgabebreite bringen und die
#     Fahrt dort rechnen. Danach wird nur noch herunterskaliert.
ffmpeg -y -loglevel error -i "$QUELLE" \
  -vf "scale=7680:4320:force_original_aspect_ratio=increase:flags=lanczos,crop=7680:4320" \
  "$AUS/vorlage-7680.png"

for f in vorlage-1080 vorlage-7680; do
  printf "   %-16s " "$f.png"
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
          -of csv=p=0 "$AUS/$f.png"
done

echo
echo "== (a) bisheriger Weg: zoompan auf 1920, Ausschnitt wird HOCHskaliert =="
time ffmpeg -y -loglevel error -loop 1 -framerate $FPS -t $SEK -i "$AUS/vorlage-1080.png" \
  -vf "zoompan=z='$Z':x='$XE':y='$YE':d=1:s=1920x1080:fps=$FPS,format=yuv420p" \
  "${ENC[@]}" "$AUS/probe-a-bisher.mp4"

echo
echo "== (b) Korrektur: zoompan auf 7680, Ausgabe 3840, dann lanczos auf 1920 =="
time ffmpeg -y -loglevel error -loop 1 -framerate $FPS -t $SEK -i "$AUS/vorlage-7680.png" \
  -vf "zoompan=z='$Z':x='$XE':y='$YE':d=1:s=3840x2160:fps=$FPS,scale=1920:1080:flags=lanczos,format=yuv420p" \
  "${ENC[@]}" "$AUS/probe-b-korrigiert.mp4"

echo
echo "== (c) statisch: kein zoompan, ein sauber herunterskaliertes Bild =="
time ffmpeg -y -loglevel error -loop 1 -framerate $FPS -t $SEK -i "$QUELLE" \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,format=yuv420p" \
  "${ENC[@]}" "$AUS/probe-c-statisch.mp4"

echo
echo "== Ergebnis =="
for f in probe-a-bisher probe-b-korrigiert probe-c-statisch; do
  printf "%-22s " "$f.mp4"
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate,nb_frames \
    -show_entries format=duration,size -of default=nw=1:nk=1 "$AUS/$f.mp4" | tr '\n' ' '
  echo
done
