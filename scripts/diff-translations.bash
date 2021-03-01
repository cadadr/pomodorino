#!/usr/bin/env bash
# diff-translations.bash --- compare PO files to the POT file

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

pick(){
    grep ^msgid $1 | sort
}

pot=$(mktemp --tmpdir XXXXXXXXXX.pot)

pick po/pomodorino.pot > $pot

for po in po/*.po; do
    bn=$(basename $po)
    tmp=$(mktemp --tmpdir XXXXXXXXXX.$bn)
    pick $po > $tmp
    diff -u $tmp $pot
done

exit $?
