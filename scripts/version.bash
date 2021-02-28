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

sed -Ei 's/^(version = ).*/\1"'"$V"'"/' pyproject.toml
grep -H ^version pyproject.toml

sed -Ei 's/^(VERSION = ).*/\1"'"$V"'"/' pomodorino/app.py
grep -H ^VERSION pomodorino/app.py
