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

"""common.py --- Constants

"""

from enum import Enum, unique


VERSION = "0.1.0-alpha"

CLOCK_RESOLUTION = 1000

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

