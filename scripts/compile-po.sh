#!/bin/sh
# compile-po.sh --- compile .po files

modir=assets/mo
appid=com.gkayaalp.pomodorino
log=po/compile.report

mkdir -p $modir

echo "Translation log, $(date)" > $log

for po in po/*.po; do
    lang=$(basename -s .po $po)
    outdir="$modir/$lang/LC_MESSAGES"
    mkdir -p $outdir
    msgfmt --statistics -v -o "$outdir/$appid.mo" $po 2>> $log
done

cat $log
