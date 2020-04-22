#!/bin/sh
# update_pot.sh --- Update gettext message catalogue

xgettext --sort-output --join-existing --from-code UTF-8                \
         --language=Python --output=po/pomodorino.pot                   \
         --copyright-holder="Göktuğ Kayaalp <self at gkayaalp dot com>" \
         --package-name=Pomodorino                                      \
         --msgid-bugs-address="<self at gkayaalp dot com>"              \
         pomodorino/*.py
