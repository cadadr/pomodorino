# Pomodorino --- Simple Pomodoro timer app
# Copyright (C) 2019  Göktuğ Kayaalp <self at gkayaalp dot com>
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

"""gui.py --- Pomodorino GUI

"""

from enum import Enum, unique

import copy
import os
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, GdkPixbuf

import notify2

VERSION = "0.1.0-alpha"

@unique
class States(Enum):
    INITIAL = 1
    POMODORO = 2
    AFTER_POMODORO = 3
    SHORT_BREAK = 4
    LONG_BREAK = 5
    AFTER_BREAK = 6

# TODO(2019-12-06): internationalise
STATE_LABELS = {
    States.INITIAL: "Start Pomodoro!",
    States.POMODORO: "Pomodoro in progress.",
    States.AFTER_POMODORO: "Start a {} break",
    States.SHORT_BREAK: "Short break in progress.",
    States.LONG_BREAK: "Long break in progress.",
    States.AFTER_BREAK: "Start New Pomodoro!",
}

MULTI_BUTTON_START = "_Start"
MULTI_BUTTON_CANCEL = "_Cancel"

BUTTON_LABELS = {
    States.INITIAL: MULTI_BUTTON_START,
    States.POMODORO: MULTI_BUTTON_CANCEL,
    States.AFTER_POMODORO: MULTI_BUTTON_START,
    States.SHORT_BREAK: MULTI_BUTTON_CANCEL,
    States.LONG_BREAK: MULTI_BUTTON_CANCEL,
    States.AFTER_BREAK: MULTI_BUTTON_START,
}

PHASE_SECONDS_DEFAULTS = {
    States.INITIAL: 0,
    States.POMODORO: 25 * 60,
    States.AFTER_POMODORO: 0,
    States.SHORT_BREAK: 5 * 60,
    States.LONG_BREAK: 15 * 60,
    States.AFTER_BREAK: 0,
}

SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT = False


class Window(Gtk.ApplicationWindow):

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


    def get_state_label(self):
        l = STATE_LABELS[self.app.state]
        if self.app.state == States.AFTER_POMODORO:
            l = l.format(self.app.break_kind())
        return l


    def get_button_label(self):
        return BUTTON_LABELS[self.app.state]


    # We parameterise x so that there can be only one place where the
    # timer string is generated.  Otherwise, self.update() has to do
    # it too, and that results in inconsistencies.
    #
    # It’s sad that you can’t refer to self within the argument list;
    # that’s why I needed the first if clause.
    def get_timer_label(self, x = None):
        if not x:
            x = self.app.timer_seconds

        if x == 0:
            x = self.app.phase_seconds[self.app.next_state()]
        return ("%02d : %02d" % divmod(x, 60))


    def get_pomodoro_count_label(self):
        return "Pomodoros completed: {}".format(self.app.pomodoro_count)


    def setup(self):
        self.vbox = Gtk.VBox(spacing = 20)
        self.state_label = Gtk.Label(label=self.get_state_label())
        self.timer_label = Gtk.Label(label=self.get_timer_label())
        self.pomodoro_count_label = Gtk.Label(label=self.get_pomodoro_count_label())
        self.level = Gtk.LevelBar()
        self.action_bar = Gtk.ActionBar()
        self.multi_button = Gtk.Button(label=self.get_button_label(), use_underline=True)
        self.pause_button = Gtk.ToggleButton(label="_Pause", use_underline=True)
        self.menu_button = Gtk.MenuButton()
        self.menu = Gtk.Builder.new_from_string(self.MENU_XML, -1).get_object("app-menu")
        self.popup = Gtk.Menu.new_from_model(self.menu)

        self.multi_button.connect("clicked", lambda x: self.on_multi_button(x, None))
        self.pause_button.connect("toggled", lambda x: self.app.on_pause(x, None))

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


    def on_multi_button(self, action, param):
        if action.get_label() == MULTI_BUTTON_START:
            self.app.on_advance(action, param)
        else:
            self.app.on_cancel(action, param)


    def update(self, args):
        self.state_label.set_label(self.get_state_label())
        self.multi_button.set_label(self.get_button_label())
        if self.app.time_elapsed == 0:
            self.timer_label.set_label(self.get_timer_label())
            self.pause_button.set_sensitive(False)
        else:
            self.timer_label.set_label(
                self.get_timer_label(self.app.timer_seconds - self.app.time_elapsed)
            )
            self.pause_button.set_sensitive(True)
        self.pomodoro_count_label.set_label(self.get_pomodoro_count_label())
        self.level.set_max_value(self.app.timer_seconds)
        self.level.set_value(self.app.time_elapsed)



class Settings(Gtk.Window):

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
            "Pomodoro length (minutes):", States.POMODORO)
        self.short_break_spinner = self.make_time_spinner_and_attach(
            "Short break length (minutes):", States.SHORT_BREAK)
        self.long_break_spinner = self.make_time_spinner_and_attach(
            "Long break length (minutes):", States.LONG_BREAK)

        self.add_label("Desktop notifications:")
        self.suppress_desktop_notifs_switch = Gtk.Switch()
        self.suppress_desktop_notifs_switch.connect(
            "state_set", lambda x, y: self.app.on_suppress_desktop_notifs_switch_set(x, y)
        )
        # Don’t expand to fill:
        self.suppress_desktop_notifs_switch.set_halign(Gtk.Align.CENTER)
        self.add_control(self.suppress_desktop_notifs_switch)

        self.defaults_button = Gtk.Button.new_with_mnemonic(label="De_faults")
        self.defaults_button.connect("clicked", lambda x: self.app.on_defaults(x, None))
        self.grid.attach(self.defaults_button, 1, self.grid_row, 1, 1)

        self.undo_button = Gtk.Button.new_with_mnemonic(label="_Undo")
        self.undo_button.connect(
            "clicked", lambda x: self.app.on_settings_undone(x, None))
        self.grid.attach(self.undo_button, 0, self.grid_row, 1, 1)

        self.done_button = Gtk.Button.new_with_mnemonic(label="_Done")
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


class App(Gtk.Application):

    app_id = "com.gkayaalp.pomodorino"
    app_name = "Pomodorino"  # TODO(2019-12-06): internationalise?

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id=self.app_id, **kwargs)
        self.title = self.app_name
        self.window = None
        self.previous_state = None
        self.state = States.INITIAL
        self.pomodoro_count = 0
        self.phase_seconds = copy.deepcopy(PHASE_SECONDS_DEFAULTS)
        self.timer_seconds = self.phase_seconds[self.state]
        self.time_elapsed = 0
        self.suppress_desktop_notifications = SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT

        logo_path = os.path.join(os.path.dirname(__file__), "../assets/logo.png")
        self.logo = GdkPixbuf.Pixbuf.new_from_file_at_scale(logo_path, 64, 64, True)

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
            self.window = Window(application=self, title=self.title)
        self.window.set_default_icon(self.logo)
        self.window.present()


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


    def on_advance(self, action, param):
        self.advance_state()
        self.window.update(None)
        self.start_timer()


    def start_timer(self):
        message = STATE_LABELS[self.previous_state]
        if self.previous_state == States.AFTER_POMODORO:
            message = message.format(self.break_kind())
        if self.timer_seconds > 0:
            self.current_timer = GLib.timeout_add(1000, self.tick)
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
            self.window.update(None)
            return False
        else:
            self.time_elapsed += 1
            self.window.update(None)
            return True


    def send_desktop_notification(self, message):
        if not self.suppress_desktop_notifications:
            n = notify2.Notification(self.title, message)
            n.show()
        else:
            print("Suppressed desktop notification:", message)


    def on_settings(self, action, param):
        self.pre_settings_record = (
            copy.deepcopy(self.phase_seconds), self.suppress_desktop_notifications
        )
        self.settings_popup = Settings(transient_for=self.window,
                                       title="Pomodorino Settings",
                                       application=self)
        self.settings_popup.present()


    def on_settings_undone(self, action, param):
        self.phase_seconds, self.suppress_desktop_notifications = self.pre_settings_record
        self.settings_popup.update()


    def on_minutes_adjusted(self, action, param):
        value = action.get_value_as_int()
        self.phase_seconds[param] = value * 60
        self.window.update(None)


    def on_suppress_desktop_notifs_switch_set(self, action, param):
        self.suppress_desktop_notifications = not param


    def on_defaults(self, action, param):
        self.phase_seconds = copy.deepcopy(PHASE_SECONDS_DEFAULTS)
        self.suppress_desktop_notifications = SUPPRESS_DESKTOP_NOTIFICATIONS_DEFAULT
        self.settings_popup.update()


    def on_reset(self, action, param):
        if self.current_timer:
            GLib.source_remove(self.current_timer)
        self.state = States.INITIAL
        self.timer_seconds = 0
        self.time_elapsed = 0
        self.pomodoro_count = 0
        self.window.update(None)


    def on_cancel(self, action, param):
        if self.current_timer:
            GLib.source_remove(self.current_timer)
        self.time_elapsed = 0
        self.state = self.previous_state
        self.timer_seconds = self.phase_seconds[self.state]
        self.window.update(None)


    def on_pause(self, action, param):
        if action.get_active() and self.current_timer:
            GLib.source_remove(self.current_timer)
        else:
            self.start_timer()


    def on_about(self, action, param):
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
        about_dialog.present()


    def on_quit(self, action, param):
        self.quit()


def main():
    app = App()
    app.run(sys.argv)


if __name__ == '__main__':
    main()
