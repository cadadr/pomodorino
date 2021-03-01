#!/usr/bin/env bash
# refresh-translations.bash --- update POT files and merge into PO files

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

echo Extract messages...
xgettext --sort-output --from-code UTF-8                                \
         --language=Python --output=po/pomodorino.pot                   \
         --copyright-holder="Göktuğ Kayaalp <self at gkayaalp dot com>" \
         --package-name=Pomodorino                                      \
         --msgid-bugs-address="<self at gkayaalp dot com>"              \
         pomodorino/*.py

for pofile in po/*.po; do
    echo Update $pofile...
    msgmerge --update --sort-output $pofile po/pomodorino.pot
done

