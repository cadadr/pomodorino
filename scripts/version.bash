#!/usr/bin/env bash
# version.bash --- update version number

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

if [ $# = 0 ]; then
    echo "$0: usage: $0 MIN.MAJ.PATH([ab][1-9]+)?"
    exit 1
fi

V="$1"

sed -Ei 's/^(    version=).*/\1"'"$V"'",/' setup.py
grep -H '^    version' setup.py

sed -Ei 's/^(VERSION = ).*/\1"'"$V"'"/' src/pomodorino/app.py
grep -H ^VERSION src/pomodorino/app.py

sed -Ei "s/^(footer: pomodorino ).*/\\1v$V/" doc/pomodorino.1.markdown
grep -H ^footer: doc/pomodorino.1.markdown

echo
echo Do not forget to update changelogs\!
