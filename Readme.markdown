# Pomodorino

<img src="assets/logo.png" width=64px alt="Pomodorino logo"/>

**WORK IN PROGRESS**

Pomodorino is a lightweight, simple Pomodoro timer system tray
application written using Python 3 and GTK 3.

What sets it apart is that it’s totally FOSS (licensed under GPLv3+)
and really lightweight.  Alternative Linux apps that I could find were
either paid and proprietrary or they used rather heavy technologies
like Electron.

Using Pomodorino should be rather straight-forward if you know about
the [Pomodoro Technique®][pt] (which is a registered trademark of
Francesco Cirillo).

[pt]: https://en.wikipedia.org/wiki/Pomodoro_Technique


<img src="assets/screenshots/grouped.png" alt="screenshots of indicator menu and application windows" />

## Dependencies

- Python 3
- [PyGObject](https://pygobject.readthedocs.io/en/latest/)
- [notify2](https://pypi.org/project/notify2/)
- [dbus-python](https://pypi.org/project/dbus-python/)

## Installation

### Source installation

We use [Poetry] for project management, so installing that is a
prerequisite:

    pip3 install --user poetry

[Poetry]:https://python-poetry.org/

After that, at the project root, run the following commands:

    poetry install
    poetry build
    pip3 install ./dist/pomodorino-0.1.0b1-py3-none-any.whl

where the `0.1.0b1` bit is the package version; so update the command
as necessary if the current version is different.

These steps should’ve installed Pomodorino and it’s dependencies under
some path that’s known to Python, possibly `~/.local/share` and
`~/.local/bin`. Add that latter one to the `PATH` environment
variable.

For FreeDesktop environments, there is [a .desktop
file](assets/pomodorino.desktop) included under the `assets/`
directory. You can copy that and the icon to appropriate places to
have a menu entry for running Pomodorino:

    cp assets/pomodorino.desktop ~/.local/share/applications
    cp assets/logo.png ~/.local/share/icons/hicolor/512x512/apps/pomodorino.png

## Contributing & Issues

Contributions are welcome!  This section will be expanded prior to
initial publication.

Please report issues at the [issue
tracker](https://github.com/cadadr/pomodorino/issues).

## Licence

Pomodorino is licenced under GPLv3 or later.

    Pomodorino --- Simple Pomodoro timer app
    Copyright (C) 2019, 2020  Göktuğ Kayaalp <self at gkayaalp dot com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
