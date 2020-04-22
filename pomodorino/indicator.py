# Pomodorino --- Simple Pomodoro timer app
# Copyright (C) 2020  Göktuğ Kayaalp <self at gkayaalp dot com>
#
# This file is part of Pomodorino.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""indicator.py --- Pomodorino systray applet

"""

from gettext import gettext as _

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3

from pomodorino.common import *


# This can’t be a subclass of AppIndicator3.Indicator because the damn
# thing keeps crashing w/ fucking segfault when I try to pass in the
# App instance.
class Indicator:

    def __init__(self, *args, **kwargs):
        self.app = kwargs["application"]
        self.i = AppIndicator3.Indicator.new(
            self.app.app_id, self.app.logo_path,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )

        self.menu = None
        self.build_menu()

        self.i.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.i.set_title(self.app.app_name)
        self.i.set_menu(self.menu)
        self.i.props.label_guide = "00:00"
        self.i.props.label = "--:--"

        self.update()


    def build_menu(self):
        self.menu = Gtk.Menu()

        self.menu_progress = Gtk.MenuItem("")
        self.menu_progress.set_sensitive(False)

        self.menu_multi = Gtk.MenuItem.new_with_mnemonic(self.app.get_multi_button_label())
        self.menu_multi.connect('activate', self.app.on_multi)

        self.menu_pause = Gtk.MenuItem(_("Pause"))
        self.menu_pause.connect('activate', self.app.on_pause)

        self.menu_reset = Gtk.MenuItem(_('Reset'))
        self.menu_reset.connect('activate', self.app.on_reset)

        self.menu_settings = Gtk.MenuItem(_('Settings'))
        self.menu_settings.connect('activate', self.app.on_settings)

        self.menu_quit = Gtk.MenuItem(_('Quit'))
        self.menu_quit.connect('activate', self.app.on_quit)

        self.menu_about = Gtk.MenuItem(_('About'))
        self.menu_about.connect('activate', self.app.on_about)

        self.menu.append(self.menu_progress)
        self.menu.append(self.menu_multi)
        self.menu.append(self.menu_pause)
        self.menu.append(self.menu_reset)
        self.menu.append(self.menu_settings)
        self.menu.append(self.menu_quit)
        self.menu.append(self.menu_about)

        self.menu.show_all()


    def update(self):
        progress_label = "{}/{} ({})".format(
            self.app.get_timer_label(self.app.timer_seconds - self.app.time_elapsed),
            self.app.get_timer_label(),
            self.app.pomodoro_count
        )

        self.i.props.label = "{}".format(
            self.app.get_timer_label(self.app.timer_seconds - self.app.time_elapsed)
        )

        self.menu_progress.set_label(progress_label)
        self.menu_multi.set_label(self.app.get_multi_button_label())

        self.menu_pause.set_sensitive(not (self.app.time_elapsed == 0))

        if self.app.paused:
            self.menu_pause.set_label(_("Resume"))
        else:
            self.menu_pause.set_label(_("Pause"))
