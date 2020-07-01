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

# flake8: noqa E402  # impossible to satisfy because of Gtk bullshit

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib, GdkPixbuf
import notify2

from pomodorino.settingsmodal import SettingsModal
from pomodorino.indicator import Indicator

from enum import Enum, unique

import copy
import gettext
import locale
import os
import sys

APP_ID = "com.gkayaalp.pomodorino"

CWD = "."
try:
    CWD = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
except NameError:
    pass

LOCALE_DIR = os.path.abspath(os.path.join(CWD, '../assets/mo'))

try:
    locale.setlocale(locale.LC_ALL, '')
    locale.bindtextdomain(APP_ID, LOCALE_DIR)

    # HACK(2020-04-23): gettext.find uses envvars instead of the locale
    # module. This is a workaround.
    os.environ["LANGUAGE"] = locale.getlocale(locale.LC_MESSAGES)[0].split("_")[0]
except locale.Error:
    pass

gettext.bindtextdomain(APP_ID, LOCALE_DIR)
gettext.textdomain(APP_ID)
gettext.install(APP_ID)
_ = gettext.gettext



VERSION = "0.1.0-beta1"

CLOCK_RESOLUTION = 1000

@unique
class States(Enum):
    INITIAL = 1
    POMODORO = 2
    AFTER_POMODORO = 3
    SHORT_BREAK = 4
    LONG_BREAK = 5
    AFTER_BREAK = 6


PHASE_SECONDS_DEFAULTS = {
    States.INITIAL: 0,
    States.POMODORO: 25 * 60,
    States.AFTER_POMODORO: 0,
    States.SHORT_BREAK: 5 * 60,
    States.LONG_BREAK: 15 * 60,
    States.AFTER_BREAK: 0,
}

SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT = False
EASE_IN_MODOE_ENABLED_DEFAULT = False

BUTTON_LABELS = {
    States.INITIAL: _("Get going!"),
    States.POMODORO: _("Cancel"),
    States.AFTER_POMODORO: _("Start break"),
    States.SHORT_BREAK: _("Cancel"),
    States.LONG_BREAK: _("Cancel"),
    States.AFTER_BREAK: _("Start new pomodoro"),
}


class App(Gtk.Application):

    app_id = APP_ID
    app_name = "Pomodorino"

    states = States

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=self.app_id, **kwargs)
        self.title = self.app_name
        self.indicator = None
        self.current_timer = None
        self.previous_state = None
        self.paused = False
        self.settings_popup = None
        self.about_dialog = None
        self.state = States.INITIAL
        self.pomodoro_count = 0
        self.phase_seconds = copy.deepcopy(PHASE_SECONDS_DEFAULTS)
        self.timer_seconds = self.phase_seconds[self.state]
        self.time_elapsed = 0
        self.suppress_desktop_notifications = SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT
        self.ease_in_mode_enabled = EASE_IN_MODOE_ENABLED_DEFAULT

        self.logo_path = "../assets/logo.png"
        self.logo_path = os.path.join(CWD, self.logo_path)

        self.logo = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.logo_path, 64, 64, True)

        notify2.init(self.app_id)

        self.action_support = "actions" in notify2.get_server_caps()
        if not self.action_support:
            print(_("Notifications server does not support actions"))


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
        if not self.indicator:
            self.indicator = Indicator(application=self)
        self.send_desktop_notification(_("Pomodorino is ready!"))
        self.hold()


    def next_state(self):
        if self.state == States.INITIAL:
            if self.ease_in_mode_enabled:
                return States.SHORT_BREAK
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


    def advance_state(self):
        self.previous_state = self.state
        self.state = self.next_state()
        self.timer_seconds = self.phase_seconds[self.state]
        self.time_elapsed = 0


    def on_advance(self, action, param=None):
        self.advance_state()
        self.indicator.update()
        self.start_timer()


    def on_skip_break(self, action, param=None, *args):
        if self.ease_in_mode_enabled:
            assert self.state in [States.AFTER_POMODORO, States.INITIAL]
        else:
            assert self.state == States.AFTER_POMODORO
        
        self.advance_state()    # after_pomodoro -> break
        self.advance_state()    # break -> pomodoro
        assert self.state == States.AFTER_BREAK

        if self.ease_in_mode_enabled and self.pomodoro_count == 0:
            self.send_desktop_notification(_("Skipped ease-in period"))
        else:
            self.send_desktop_notification(_("Skipped a break"))

        self.indicator.update()


    def start_timer(self):
        message = None

        if self.paused:
            message = _("Resume")
        elif self.state == States.POMODORO:
            message = _("Started new pomodoro")
        elif self.state == States.SHORT_BREAK:
            if self.ease_in_mode_enabled and self.previous_state == States.INITIAL:
                message = _("Started ease-in period")
            else:
                message = _("Started short break")
        elif self.state == States.LONG_BREAK:
            message = _("Started long break")

        if self.timer_seconds > 0:
            self.current_timer = GLib.timeout_add(CLOCK_RESOLUTION, self.tick)

        if message:
            self.send_desktop_notification(message)

        self.paused = False


    def tick(self):
        if self.time_elapsed == self.timer_seconds:
            self.time_elapsed = 0
            self.current_timer = None
            self.advance_state()
            if self.state == States.AFTER_POMODORO:
                self.pomodoro_count += 1
                self.send_desktop_notification(
                    _("Completed pomodoro"),
                    # TODO(2020-05-03): does not work for some reason
                    # ("skip", _("Skip the break"), lambda *a: print(a), None)
                )
            elif self.state == States.AFTER_BREAK:
                if self.previous_state == States.SHORT_BREAK:
                    if self.ease_in_mode_enabled and self.pomodoro_count == 0:
                        self.send_desktop_notification(_("Completed ease-in period"))
                    else:
                        self.send_desktop_notification(_("Completed short break"))
                else:
                    self.send_desktop_notification(_("Completed long break"))
            self.indicator.update()
            return False
        else:
            self.time_elapsed += 1
            self.indicator.update()
            return True


    def send_desktop_notification(self, message, action=None):
        if not self.suppress_desktop_notifications:
            n = notify2.Notification(self.title, message)
            n.set_icon_from_pixbuf(self.logo)
            if action and self.action_support:
                action, label, callback, data = action
                n.add_action(action, label, callback, data)
            n.show()
        else:
            print(_("Suppressed desktop notification:"), message)


    def on_settings(self, action, param=None):
        if not self.settings_popup:
            self.pre_settings_record = (
                copy.deepcopy(self.phase_seconds), self.suppress_desktop_notifications
            )
            self.settings_popup = SettingsModal(title=_("Pomodorino Settings"),
                                                application=self)
            self.settings_popup.present()
            self.settings_popup.connect('destroy', self.on_settings)
        else:
            self.settings_popup.close()
            self.settings_popup = None

        self.indicator.menu_settings.set_sensitive(not self.settings_popup)


    def on_settings_undone(self, action, param=None):
        self.phase_seconds, self.suppress_desktop_notifications = self.pre_settings_record
        self.settings_popup.update()


    def on_minutes_adjusted(self, action, param=None):
        value = action.get_value_as_int()
        self.phase_seconds[param] = value * 60
        self.indicator.update()


    def on_suppress_desktop_notifs_switch_set(self, action, param=None):
        self.suppress_desktop_notifications = not param


    def on_ease_in_mode_switch_set(self, action, param=None):
        self.ease_in_mode_enabled = param
        self.indicator.update()


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


    def on_cancel(self, action, param=None):
        if self.current_timer:
            GLib.source_remove(self.current_timer)
        self.time_elapsed = 0
        self.state = self.previous_state
        self.timer_seconds = self.phase_seconds[self.state]
        self.paused = False
        self.indicator.update()


    def on_pause(self, action, param=None):
        if action.get_sensitive() and self.current_timer:
            GLib.source_remove(self.current_timer)
            self.current_timer = None
            self.paused = True
        else:
            self.start_timer()
        self.indicator.update()


    def on_about(self, action, param=None):
        if not self.about_dialog:
            self.about_dialog = Gtk.AboutDialog()
            self.about_dialog.set_logo(self.logo)
            self.about_dialog.set_authors(["Göktuğ Kayaalp <self@gkayaalp.com>"])
            self.about_dialog.set_comments(_("Simple Pomodoro Timer."))
            self.about_dialog.set_copyright(
                _("Copyright (C) 2019, 2020 Göktuğ Kayaalp <self@gkayaalp.com>"))
            self.about_dialog.set_license_type(Gtk.License.GPL_3_0)
            self.about_dialog.set_website("https://www.gkayaalp.com/pomodorino.html")
            self.about_dialog.set_website_label(_("Website: {}").format(
                self.about_dialog.get_website()))
            self.about_dialog.set_program_name(self.app_name)
            self.about_dialog.set_version(VERSION)
            # about_dialog.set_documenters(...)
            # about_dialog.set_translator_credits(...)
            # about_dialog.set_artists(...)
            self.about_dialog.connect('destroy', self.on_about)
            self.about_dialog.show()

        else:
            self.about_dialog.close()
            self.about_dialog = None

        self.indicator.menu_about.set_sensitive(not self.about_dialog)


    # HACK(2020-04-23): Must not depend on button label.
    def on_multi(self, action, param=None):  # noqa: E301
        if action.get_label() == _("Cancel"):
            self.on_cancel(action, param)
        else:
            self.on_advance(action, param)


    def on_quit(self, action, param=None):
        self.release()
        self.quit()


    def get_multi_button_label(self):
        if self.ease_in_mode_enabled:
            if self.state == States.INITIAL:
                return _("Ease in!")
            if self.pomodoro_count == 0 and self.state == States.AFTER_BREAK:
                return BUTTON_LABELS[States.INITIAL]
        return BUTTON_LABELS[self.state]


    # TODO(2020-04-22): window removed, this can go into the
    # Indicator.
    #
    # We parameterise x so that there can be only one place where the
    # timer string is generated.  Otherwise, MainWindow.update() has to do
    # it too, and that results in inconsistencies.
    #
    # It’s sad that you can’t refer to self within the argument list;
    # that’s why I needed the first if clause.
    def get_timer_label(self, x=None):  # noqa: E301
        if not x:
            x = self.timer_seconds

        if x == 0:
            x = self.phase_seconds[self.next_state()]
        return ("%02d : %02d" % divmod(x, 60))


    def get_pomodoro_count_label(self):
        return _("Pomodoros completed: {}").format(self.pomodoro_count)




def main():
    app = App()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
