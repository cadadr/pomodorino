#!/bin/sh
# compare-with-pot.sh --- find differences from pot in po files.

pick(){
    grep ^msgid $1
}

pot=$(mktemp --tmpdir XXXXXXXXXX.pot)

pick po/pomodorino.pot > $pot

for po in po/*.po; do
    bn=$(basename $po)
    tmp=$(mktemp --tmpdir XXXXXXXXXX.$bn)
    pick $po > $tmp
    diff -u $tmp $pot
done
