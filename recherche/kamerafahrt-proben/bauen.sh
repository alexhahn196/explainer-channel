#!/bin/bash
# Baut die drei Probeclips aus EINEM vorhandenen Bild.
# Identische Laufzeit, identische Bewegung, identische Kodierung - der
# einzige Unterschied ist der Weg, auf dem die Kamerafahrt entsteht.
#
# (a) baut den Filter so, wie er FRUEHER in schritt5_video.py stand.
# (b) und (c) rufen produktion/pipeline/kamerafahrt.py auf, also genau das,
#     was die Pipeline heute tut - die Clips sind kein Modell davon,
#     sondern dasselbe Programm.
set -euo pipefail

REPO=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
QUELLE="$REPO/recherche/stile-erklaerkanal/stil-1-flatvector-szeneA.png"
AUS="${1:-.}"
FPS=24
SEK=6
N=$((FPS * SEK))          # 144 Frames
ZOOM_BIS=1.08
SCHWENK=0.7               # Anteil des freien Wegs, waagerecht

# Alle drei Clips gleich kodieren. CRF 16 statt der 28 aus config.md:
# sonst vergleicht man Kamerafahrt UND Codec gleichzeitig.
CRF=16
PRESET=slow

echo "== (a) bisheriger Weg: Bild auf 1920 herunterrechnen, dann zoompan =="
# schritt4_bild.py::zuschneiden() - ab hier sind die 2752 px der Quelle weg
ffmpeg -y -loglevel error -i "$QUELLE" \
  -vf "scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080" \
  "$AUS/vorlage-1080.png"
# ... und der Filter, wie er frueher in zyklus_bauen() gebaut wurde
R="(1-cos(PI*on/$N))/2"
time ffmpeg -y -loglevel error -loop 1 -framerate $FPS -t $SEK -i "$AUS/vorlage-1080.png" \
  -vf "zoompan=z='1+0.08*$R':x='(iw-iw/zoom)*(0.5+0.35*$R)':y='(ih-ih/zoom)/2':d=1:s=1920x1080:fps=$FPS,format=yuv420p" \
  -c:v libx264 -preset $PRESET -crf $CRF -pix_fmt yuv420p -g 48 -an \
  "$AUS/probe-a-bisher.mp4"
rm -f "$AUS/vorlage-1080.png"

echo
echo "== (b) Korrektur - kamerafahrt.py, art=fahrt =="
time python3 "$REPO/produktion/pipeline/kamerafahrt.py" "$QUELLE" \
  "$AUS/probe-b-korrigiert.mp4" --dauer $SEK --art fahrt \
  --zoom-bis $ZOOM_BIS --schwenk-von 0 --schwenk $SCHWENK --crf $CRF --fps $FPS

echo
echo "== (c) statisch - kamerafahrt.py, art=statisch =="
time python3 "$REPO/produktion/pipeline/kamerafahrt.py" "$QUELLE" \
  "$AUS/probe-c-statisch.mp4" --dauer $SEK --art statisch --crf $CRF --fps $FPS

echo
echo "== Ergebnis =="
for f in probe-a-bisher probe-b-korrigiert probe-c-statisch; do
  printf "%-22s " "$f.mp4"
  ffprobe -v error -select_streams v:0 -count_frames \
    -show_entries stream=width,height,nb_read_frames \
    -show_entries format=duration,size -of default=nw=1:nk=1 "$AUS/$f.mp4" \
    | tr '\n' ' '
  echo
done
