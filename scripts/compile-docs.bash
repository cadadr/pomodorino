#!/usr/bin/env bash
# compile-docs.bash --- compile documentation

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

pandoc -s -t man -f markdown-smart -o doc/pomodorino.1 \
       doc/pomodorino.1.markdown
