#!/bin/sh
# run.sh --- test run with proper environment

# POSIX strict-ish mode, beware eager pipelines!
set -eu
IFS=$'\n\t'

fakehome="$PWD/.fake_home"

mkdir -p "$fakehome/.local/share"
XDG_DATA_HOME="$fakehome/.local/share"

for s in 8x8 16 22 24 32 48 64 96 128 256 512; do
    geom="${s}x${s}"
    mkdir -p "$XDG_DATA_HOME/icons/hicolor/$geom/apps/"
    convert -geometry "$geom" assets/logo.png "$fakehome/$geom.png"
    cp "$fakehome/$geom.png" \
       "$XDG_DATA_HOME/icons/hicolor/$geom/apps/com.gkayaalp.pomodorino.png"
done

mkdir -p "$fakehome/.local/share/glib-2.0/schemas"
GSETTINGS_SCHEMA_DIR="$fakehome/.local/share/glib-2.0/schemas"
cp data/com.gkayaalp.pomodorino.gschema.xml "$GSETTINGS_SCHEMA_DIR/"

glib-compile-schemas "$GSETTINGS_SCHEMA_DIR"
gtk-update-icon-cache

export XDG_DATA_HOME GSETTINGS_SCHEMA_DIR

poetry run pomodorino
