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

"""settingsmodal.py --- Settings window

"""

from gettext import gettext as _

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from pomodorino.common import *


class SettingsModal(Gtk.Window):

    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.app = kwargs['application']
        self.setup()


    def setup(self):
        self.set_modal(True)
        self.set_border_width(20)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(10)
        self.grid.set_column_spacing(10)
        # This is incremented by self.add_control().
        self.grid_row = 0

        self.pomodoro_spinner = self.make_time_spinner_and_attach(
            _("Pomodoro length (minutes):"), States.POMODORO)
        self.short_break_spinner = self.make_time_spinner_and_attach(
            _("Short break length (minutes):"), States.SHORT_BREAK)
        self.long_break_spinner = self.make_time_spinner_and_attach(
            _("Long break length (minutes):"), States.LONG_BREAK)

        self.add_label(_("Desktop notifications:"))
        self.suppress_desktop_notifs_switch = Gtk.Switch()
        self.suppress_desktop_notifs_switch.connect(
            "state_set", lambda x, y: self.app.on_suppress_desktop_notifs_switch_set(x, y)
        )
        # Don’t expand to fill:
        self.suppress_desktop_notifs_switch.set_halign(Gtk.Align.CENTER)
        self.add_control(self.suppress_desktop_notifs_switch)

        self.defaults_button = Gtk.Button.new_with_mnemonic(label=_("De_faults"))
        self.defaults_button.connect("clicked", lambda x: self.app.on_defaults(x, None))
        self.grid.attach(self.defaults_button, 1, self.grid_row, 1, 1)

        self.undo_button = Gtk.Button.new_with_mnemonic(label=_("_Undo"))
        self.undo_button.connect(
            "clicked", lambda x: self.app.on_settings_undone(x, None))
        self.grid.attach(self.undo_button, 0, self.grid_row, 1, 1)

        self.done_button = Gtk.Button.new_with_mnemonic(label=_("_Done"))
        self.done_button.connect("clicked", lambda _: self.close())
        self.add_control(self.done_button)

        self.add(self.grid)

        self.set_resizable(False)

        self.update()

        self.show_all()


    def add_label(self, text):
        label = Gtk.Label(label=text)
        label.set_halign(Gtk.Align.START)
        self.grid.attach(label, 0, self.grid_row, 2, 1)


    def add_control(self, control):
        self.grid.attach(control, 3, self.grid_row, 1, 1)
        self.grid_row += 1


    def make_time_spinner_and_attach(self, text, state):
        self.add_label(text)

        spinner = Gtk.SpinButton.new_with_range(1.0, 6000.0, 1.0)

        spinner.set_digits(0)
        spinner.set_snap_to_ticks(True)
        spinner.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)

        spinner.connect("value_changed", lambda x: self.app.on_minutes_adjusted(x, state))

        self.add_control(spinner)

        return spinner


    def update(self):
        def f(x):
            minutes, _ = divmod(x, 60)
            return minutes

        self.pomodoro_spinner.set_value(f(self.app.phase_seconds[States.POMODORO]))
        self.short_break_spinner.set_value(f(self.app.phase_seconds[States.SHORT_BREAK]))
        self.long_break_spinner.set_value(f(self.app.phase_seconds[States.LONG_BREAK]))
        self.suppress_desktop_notifs_switch.set_active(
            not self.app.suppress_desktop_notifications)


