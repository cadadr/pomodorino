#!/usr/bin/env bash
# resize-logo.bash --- resize assets/logo.png for use with GTK

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

ls assets/icons/hicolor/ \
    | while read geom;
do
    convert -geometry $geom assets/logo.png \
            assets/icons/hicolor/$geom/apps/com.gkayaalp.pomodorino.png;
done
