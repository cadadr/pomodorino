#!/bin/sh
# run.sh --- test run with proper environment

# POSIX strict-ish mode, beware eager pipelines!
set -eu
IFS=$'\n\t'

glib-compile-schemas data/
export GSETTINGS_SCHEMA_DIR=data/

poetry run pomodorino
