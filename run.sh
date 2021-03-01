#!/bin/sh
# run.sh --- test run with proper environment

# POSIX strict-ish mode, beware eager pipelines!
set -eu
IFS=$'\n\t'

fakehome="$PWD/.fake_home"

mkdir -p "$fakehome/.local/share"
XDG_DATA_HOME="$fakehome/.local/share"

cp -r assets/icons/ "$XDG_DATA_HOME/icons"

mkdir -p "$fakehome/.local/share/glib-2.0/schemas"
GSETTINGS_SCHEMA_DIR="$fakehome/.local/share/glib-2.0/schemas"
cp data/com.gkayaalp.pomodorino.gschema.xml "$GSETTINGS_SCHEMA_DIR/"

glib-compile-schemas "$GSETTINGS_SCHEMA_DIR"
gtk-update-icon-cache

export XDG_DATA_HOME GSETTINGS_SCHEMA_DIR
export PYTHONPATH="$PWD/src"
export DEBUG_LOCALE_DIR=data/gettext
export DEBUG_CLOCK_RESOLUTION=10

./.venv/bin/python src/pomodorino/app.py
