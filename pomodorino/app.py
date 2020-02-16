# Pomodorino --- Simple Pomodoro timer app
# Copyright (C) 2019, 2020  Göktuğ Kayaalp <self at gkayaalp dot com>
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

"""app.py --- Pomodorino GTK app

"""

import copy
import os
import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, GdkPixbuf
import notify2

from pomodorino.common import *
from pomodorino.mainwindow import MainWindow
from pomodorino.settingsmodal import SettingsModal
from pomodorino.indicator import Indicator

class App(Gtk.Application):

    app_id = "com.gkayaalp.pomodorino"
    app_name = "Pomodorino"  # TODO(2019-12-06): internationalise?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=self.app_id, **kwargs)
        self.title = self.app_name
        self.window = None
        self.indicator = None
        self.current_timer = None
        self.previous_state = None
        self.paused = False
        self.state = States.INITIAL
        self.pomodoro_count = 0
        self.phase_seconds = copy.deepcopy(PHASE_SECONDS_DEFAULTS)
        self.timer_seconds = self.phase_seconds[self.state]
        self.time_elapsed = 0
        self.suppress_desktop_notifications = SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT

        self.logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo.png")
        self.logo = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.logo_path, 64, 64, True)

        notify2.init(self.app_id)


    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("settings", None)
        action.connect("activate", self.on_settings)
        self.add_action(action)

        action = Gio.SimpleAction.new("reset", None)
        action.connect("activate", self.on_reset)
        self.add_action(action)

        action = Gio.SimpleAction.new("cancel", None)
        action.connect("activate", self.on_cancel)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)


    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title=self.title)
        self.window.set_default_icon(self.logo)

        if not self.indicator:
            self.indicator = Indicator(application=self)

        self.window.present()
        self.hold()


    def next_state(self):
        if self.state == States.INITIAL:
            return States.POMODORO

        if self.state == States.POMODORO:
            return States.AFTER_POMODORO

        if self.state == States.AFTER_POMODORO:
            if self.pomodoro_count % 4 == 0:
                return States.LONG_BREAK
            return States.SHORT_BREAK

        if self.state == States.AFTER_BREAK:
            return States.POMODORO

        return States.AFTER_BREAK


    def break_kind(self):
        n = None
        # In this case we’re already on a break state, so we don’t
        # need to peek ahead.
        if self.previous_state == States.AFTER_POMODORO:
            n = self.state
        else:
            n = self.next_state()

        if n == States.LONG_BREAK:
            return "long"
        return "short"


    def advance_state(self):
        self.previous_state = self.state
        self.state = self.next_state()
        self.timer_seconds = self.phase_seconds[self.state]
        self.time_elapsed = 0


    def on_advance(self, action, param=None):
        self.advance_state()
        self.indicator.update()
        self.window.update()
        self.start_timer()


    def start_timer(self):
        message = STATE_LABELS[self.previous_state]
        if self.previous_state == States.AFTER_POMODORO:
            message = message.format(self.break_kind())
        if self.timer_seconds > 0:
            self.current_timer = GLib.timeout_add(CLOCK_RESOLUTION, self.tick)
        self.paused = False
        self.send_desktop_notification(message)


    def tick(self):
        if self.time_elapsed == self.timer_seconds:
            self.time_elapsed = 0
            self.current_timer = None
            self.advance_state()
            if self.state == States.AFTER_POMODORO:
                self.pomodoro_count += 1
                self.send_desktop_notification("Completed pomodoro!")
            elif self.state == States.AFTER_BREAK:
                self.send_desktop_notification(
                    "Completed {} break!".format(self.break_kind()))
            self.indicator.update()
            self.window.update()
            return False
        else:
            self.time_elapsed += 1
            self.indicator.update()
            self.window.update()
            return True


    def send_desktop_notification(self, message):
        if not self.suppress_desktop_notifications:
            n = notify2.Notification(self.title, message)
            n.show()
        else:
            print("Suppressed desktop notification:", message)


    def on_settings(self, action, param=None):
        self.pre_settings_record = (
            copy.deepcopy(self.phase_seconds), self.suppress_desktop_notifications
        )
        self.settings_popup = SettingsModal(transient_for=self.window,
                                            title="Pomodorino Settings",
                                            application=self)
        self.settings_popup.present()


    def on_settings_undone(self, action, param=None):
        self.phase_seconds, self.suppress_desktop_notifications = self.pre_settings_record
        self.settings_popup.update()


    def on_minutes_adjusted(self, action, param=None):
        value = action.get_value_as_int()
        self.phase_seconds[param] = value * 60
        self.indicator.update()
        self.window.update()


    def on_suppress_desktop_notifs_switch_set(self, action, param=None):
        self.suppress_desktop_notifications = not param


    def on_defaults(self, action, param=None):
        self.phase_seconds = copy.deepcopy(PHASE_SECONDS_DEFAULTS)
        self.suppress_desktop_notifications = SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT
        self.settings_popup.update()


    def on_reset(self, action, param=None):
        if self.current_timer:
            GLib.source_remove(self.current_timer)
        self.state = States.INITIAL
        self.timer_seconds = 0
        self.time_elapsed = 0
        self.pomodoro_count = 0
        self.indicator.update()
        self.window.update()


    def on_cancel(self, action, param=None):
        if self.current_timer:
            GLib.source_remove(self.current_timer)
        self.time_elapsed = 0
        self.state = self.previous_state
        self.timer_seconds = self.phase_seconds[self.state]
        self.indicator.update()
        self.window.update()


    def on_pause(self, action, param=None):
        if action.get_active() and self.current_timer:
            GLib.source_remove(self.current_timer)
            self.current_timer = None
            self.paused = True
        else:
            self.start_timer()
        self.indicator.update()


    def on_pause_from_menu(self, action, param=None):
        self.window.pause_button.set_active(not self.paused)
        self.indicator.update()


    def on_about(self, action, param=None):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_authors(["Göktuğ Kayaalp <self@gkayaalp.com>"])
        about_dialog.set_comments("Simple Pomodoro Timer.")
        about_dialog.set_copyright("Copyright (C) 2019 Göktuğ Kayaalp <self@gkayaalp.com>")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_website("https://www.gkayaalp.com/pomodorino.html")
        about_dialog.set_website_label("Website: {}".format(
            about_dialog.get_website()))
        about_dialog.set_program_name(self.app_name)
        about_dialog.set_version(VERSION)
        # about_dialog.set_documenters(...)
        # about_dialog.set_translator_credits(...)
        # about_dialog.set_artists(...)

        # So this works for some reason...
        about_dialog.run()
        about_dialog.destroy()


    def on_window_destroyed(self, action, param=None):
        self.window.hide()
        self.indicator.update()
        return True             # Don’t destroy the window


    def on_show_window(self, action, param=None):
        self.window.show()
        self.indicator.update()


    def on_multi(self, action, param=None):
        if action.get_label() == MULTI_BUTTON_START:
            self.on_advance(action, param)
        else:
            self.on_cancel(action, param)


    def on_quit(self, action, param=None):
        self.release()
        self.quit()


    def get_multi_button_label(self):
        return BUTTON_LABELS[self.state]


    def get_state_label(self):
        l = STATE_LABELS[self.state]
        if self.state == States.AFTER_POMODORO:
            l = l.format(self.break_kind())
        return l

    # We parameterise x so that there can be only one place where the
    # timer string is generated.  Otherwise, MainWindow.update() has to do
    # it too, and that results in inconsistencies.
    #
    # It’s sad that you can’t refer to self within the argument list;
    # that’s why I needed the first if clause.
    def get_timer_label(self, x = None):
        if not x:
            x = self.timer_seconds

        if x == 0:
            x = self.phase_seconds[self.next_state()]
        return ("%02d : %02d" % divmod(x, 60))


    def get_pomodoro_count_label(self):
        return "Pomodoros completed: {}".format(self.pomodoro_count)




def main():
    app = App()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
