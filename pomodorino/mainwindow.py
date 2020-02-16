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

"""gui.py --- Main window

"""

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

from pomodorino.common import *


class MainWindow(Gtk.ApplicationWindow):

    MENU_XML = """
    <?xml version="1.0" encoding="UTF-8"?>
    <interface>
      <menu id="app-menu">
        <section>
            <item>
                <attribute name="label">Reset</attribute>
                <attribute name="action">app.reset</attribute>
            </item>
            <item>
                <attribute name="label">Settings</attribute>
                <attribute name="action">app.settings</attribute>
            </item>
            <item>
                <attribute name="label">About</attribute>
                <attribute name="action">app.about</attribute>
            </item>
            <item>
                <attribute name="label">Quit</attribute>
                <attribute name="action">app.quit</attribute>
            </item>
        </section>
      </menu>
    </interface>
    """

    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.app = kwargs['application']
        self.setup()


    def setup(self):
        self.vbox = Gtk.VBox(spacing = 20)
        self.state_label = Gtk.Label(label=self.app.get_state_label())
        self.timer_label = Gtk.Label(label=self.app.get_timer_label())
        self.pomodoro_count_label = Gtk.Label(label=self.app.get_pomodoro_count_label())
        self.level = Gtk.LevelBar()
        self.action_bar = Gtk.ActionBar()
        self.multi_button = Gtk.Button(label=self.app.get_multi_button_label(),
                                       use_underline=True)
        self.pause_button = Gtk.ToggleButton(label="_Pause", use_underline=True)
        self.menu_button = Gtk.MenuButton()
        self.menu = Gtk.Builder.new_from_string(self.MENU_XML, -1).get_object("app-menu")
        self.popup = Gtk.Menu.new_from_model(self.menu)

        self.multi_button.connect("clicked", lambda x: self.app.on_multi(x, None))
        self.pause_button.connect("toggled", lambda x: self.app.on_pause(x, None))

        self.connect("destroy", self.app.on_window_destroyed)
        self.connect("delete-event", self.app.on_window_destroyed)

        self.add(self.vbox)
        self.vbox.set_margin_top(10)
        self.vbox.add(self.state_label)
        self.vbox.add(self.timer_label)
        self.vbox.add(self.pomodoro_count_label)
        self.pomodoro_count_label.set_margin_right(10)
        self.pomodoro_count_label.set_margin_left(10)
        self.vbox.add(self.level)
        self.level.set_margin_right(10)
        self.level.set_margin_left(10)
        self.vbox.add(self.action_bar)

        self.action_bar.add(self.multi_button)
        self.action_bar.add(self.pause_button)
        self.action_bar.add(self.menu_button)
        self.menu_button.set_popup(self.popup)

        self.set_resizable(False)
        self.pause_button.set_sensitive(False)

        self.show_all()


    def update(self):
        self.state_label.set_label(self.app.get_state_label())
        self.multi_button.set_label(self.app.get_multi_button_label())
        if self.app.time_elapsed == 0:
            self.timer_label.set_label(self.app.get_timer_label())
            self.pause_button.set_sensitive(False)
        else:
            self.timer_label.set_label(
                self.app.get_timer_label(self.app.timer_seconds - self.app.time_elapsed)
            )
            self.pause_button.set_sensitive(True)
        self.pomodoro_count_label.set_label(self.app.get_pomodoro_count_label())
        self.level.set_max_value(self.app.timer_seconds)
        self.level.set_value(self.app.time_elapsed)


