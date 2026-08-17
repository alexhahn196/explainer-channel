#!/bin/sh
# Setzt die Neumontage von Video 2 aus ihren Teilen zusammen und prueft die
# Pruefsumme.
#
# Warum zerlegt: eine einzelne Datei von 97 MB kaeme zwar noch unter die
# harte GitHub-Grenze von 100 MB, aber nur knapp - und die Vierteilung ist
# hier bereits die Hausform (siehe ../auslieferung/). Vier Teile je 24 MB
# bleiben es deshalb auch dann, wenn die Datei spaeter wieder waechst.
#
# Aufruf:  sh zusammensetzen.sh
set -e

cd "$(dirname "$0")"

pruefe() {
    name="$1"
    soll="$2"
    printf '%s: ' "$name"
    cat "$name".*.part > "$name"
    ist=$(md5sum "$name" | cut -d' ' -f1)
    if [ "$ist" = "$soll" ]; then
        printf 'zusammengesetzt, MD5 stimmt (%s)\n' "$ist"
    else
        printf 'FEHLER — MD5 %s, erwartet %s\n' "$ist" "$soll"
        exit 1
    fi
}

pruefe video-02.mp4 c2bcdc13ff1f960a3ebe07a63f783ef7

echo
echo "Fertig. Die Teile koennen nach der Pruefung geloescht werden:"
echo "  rm *.part"
