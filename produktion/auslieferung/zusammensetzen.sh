#!/bin/sh
# Setzt die beiden Videos aus ihren Teilen zusammen und prueft die Pruefsumme.
#
# Warum die Videos ueberhaupt zerlegt hier liegen: eine einzelne Datei von
# 144 MB laesst GitHub nicht durch (harte Grenze 100 MB je Datei). Und der
# Weg ueber einen Dateihoster hat sich als untauglich erwiesen — der
# GoFile-Link zu Video 2 war nach wenigen Stunden tot, der zu Video 1
# ebenfalls. Vier Teile je Video kommen mit rund 36 MB durch und verfallen
# nicht.
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

pruefe video-01.mp4 26402718c0675a5b7b1065ae08f75e08
pruefe video-02.mp4 0f8d29e369313381f084b17f72c4ff5b

echo
echo "Fertig. Die Teile koennen nach der Pruefung geloescht werden:"
echo "  rm *.part"
