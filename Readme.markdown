# Pomodorino

<p align="center"><img src="assets/logo.png" width=64px alt="Pomodorino logo" /></p>

<p align="center">
  <a href="https://github.com/cadadr/pomodorino/actions/workflows/build.yml"><img src="https://github.com/cadadr/pomodorino/actions/workflows/build.yml/badge.svg" alt="Build debian package" /></a>

  <a href="https://github.com/cadadr/pomodorino/releases/latest">
    <img src="https://img.shields.io/github/v/release/cadadr/pomodorino?label=Latest%20release" alt="latest release" /></a>

  <a href="https://github.com/cadadr/pomodorino/releases/tag/latest">
    <img src="https://img.shields.io/github/v/release/cadadr/pomodorino?include_prereleases&amp;label=Latest%20dev%20release" alt="latest development release" /></a>
</p>

Pomodorino is a lightweight, simple Pomodoro timer system tray
application written using Python 3 and GTK 3.

What sets it apart is that it’s totally FOSS (licensed under GPLv3+)
and really lightweight.  Alternative Linux apps that I could find were
either paid and proprietrary or they used rather heavy technologies
like Electron.

Using Pomodorino should be rather straight-forward if you know about
the [Pomodoro Technique®][pt] (which is a registered trademark of
Francesco Cirillo).

For more information, see the [manual](./doc/pomodorino.1.markdown) and
the [wiki](https://github.com/cadadr/pomodorino/wiki).

[pt]: https://en.wikipedia.org/wiki/Pomodoro_Technique


<table>
       <tr>
              <td>
                     <img src="assets/screenshots/about.png"
                          alt="'About' popup" />
              </td>
              <td>
                     <img src="assets/screenshots/menu.png"
                          alt="Main menu" />
              </td>
              <td>
                     <img src="assets/screenshots/settings.png"
                          alt="Settings dialog" />
              </td>
       </tr>
</table>

## Dependencies

Pomodorino is mainly based on Python 3 and GTK+3.

- [Python 3](https://www.python.org)
- [PyGObject](https://pygobject.readthedocs.io/en/latest/)
- [notify2](https://pypi.org/project/notify2/)
- [dbus-python](https://pypi.org/project/dbus-python/)
- [libayatana-appindicator](https://github.com/AyatanaIndicators/libayatana-appindicator)
  - on Debian: `gir1.2-ayatanaappindicator3-0.1`

## Building and Installation

### Building the sources

This project uses `setuptools` for builds, and the procedure is
straightforward.

1. Optionally, create a virtual environment:

       $ python3 -m venv .venv
       $ ./.bin/venv/activate

2. Install the `build` package, and Pomodorino’s dependencies:

       $ pip install build
       $ pip install -r requirements.txt

3. Run build:

       $ python -m build

4. You may install the package using the wheel file generated under
   ‘dist/’, tho this is discouraged as data files will not be
   installed and the application will crash.  You can use `./run.sh`,
   as detailed below, to run without installing.

### Building a Debian package

**Note**: *The Debian package files [will soon move to a separate
repository](https://github.com/cadadr/pomodorino/issues/59).*

Building the Debian package is simple:

1. Install `devscripts`:

       $ sudo apt-get install devscripts

2. Run the following command to invoke `debuild`:

       $ debuild -i -us -uc -b

3. Relevant files, including the Debian package itself, will be output
   to the parent directory of your working directory.

### Building and Installing on Arch Linux

A `PKGBUILD` is [provided on AUR](https://aur.archlinux.org/packages/pomodorino/):

    $ git clone https://aur.archlinux.org/packages/pomodorino/
    $ cd pomodorino
    $ makepkg -s

This will produce a `.tar.zst` file, which you can then install as
follows:

    $ sudo pacman -U *.tar.zst

Of course, you can also use any of the [AUR helpers] instead of manually
building and installing.

[AUR helpers]: https://wiki.archlinux.org/title/AUR_helpers

### Running from source repository

A script, `run.sh`, is included to help with testing, it sets up an
environment in which Pomodorino can be run without a global
installation, out of a virtual environment.  The script assumes that
the virtual environment is at `$PWD/.venv`, but it’s trivial to modify
if you wish to keep the virtual environment elsewhere.  **Beware**
what by default this script sets up Pomodorino such that the clock is
run 100x faster than normal, in order to facilitate testing.  In order
to use `run.sh` for general use of Pomodorino, you should modify the
script to not export the variable `DEBUG_CLOCK_RESOLUTION`.

If you just run

       $ ./run.sh

it will set up a virtual environment at `.venv` and run Pomodorino in
it.

### Note for Gnome 3, Gnome 40, and Elementary users

These desktops sadly do not support system tray icons, which is
currently the main user interface of Pomodorino. There is an
[extension](https://github.com/ubuntu/gnome-shell-extension-appindicator)
that you can install, which would allow you to use Pomodorino
on these desktops.  I will [add a main window in the future](https://github.com/cadadr/pomodorino/issues/58)
and also plan to support a [global keybindings based interface](https://github.com/cadadr/pomodorino/issues/55)
which will not only remedy this issue but make the app more accessible,
as the extension is not great with screen readers.

### Note about accessibility features

I am working to improve accessibility of Pomodorino on the
[`better-accessibility` branch](https://github.com/cadadr/pomodorino/tree/basic-accessibility).
Any accessibility-related issues and patches are totally welcome!

### Note about potential rewrite

I am [considering to rewrite this in Rust or Vala](https://github.com/cadadr/pomodorino/issues/48)
because packaging Python apps is difficult and too delicate. Pomodorino is
still pretty small SLoC-wise, so that shouldn't be that big of a disruption
to any users, if anybody's using it at this stage.

## Contributing & Issues

Contributions are welcome!  Please submit a pull request or e-mail a
patch. Explain clearly your changes and the rationale for them, and
include a clear commit message, prefixed with the relevant filename.

Please write your commit message as in the example below:

    path/to/file.ext: imperative-mood summary of changes

    Optionally further explain the change.

A commit that only adds one file should read as follows:

    Add path/to/file

A commit that only removes one file should read as follows:

    Remove path/to/file

When including paths, if multiple files under a common directory are
concerned, the directory’s path itself will suffice:

    src/pomodorino: reticulate splines

If your patch fixes a typo, please indicate the fix in the message as
follows:

    ; path/to/file: fix typo `orig' -> `fixed'

Please do not send whitespace-only patches or patches that touch
whitespace in places other than where it actually makes changes.

Please write elaborate commit messages and pull request texts that
sufficiently detail and motivate your changes.  Please care to make
atomic commits, and please create separate issues and / or pull
requests if you’re reporting multiple problems and / or suggesting
multiple features.

Issues can be reported at the [issue
tracker](https://github.com/cadadr/pomodorino/issues).

## Licence

Pomodorino is licenced under GNU General Public Licence, version 3 or
later.

    Pomodorino --- Simple Pomodoro timer app
    Copyright (C) 2019, 2020, 2021  Göktuğ Kayaalp <self at gkayaalp dot com>

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

[Pomodorino’s logo](./assets/logo-unresized.png) as of v0.1.0b8 release was
kindly provided to me by [Neville Park](https://nevillepark.ca/), who
made it available under the terms of the [Creative Commons 0
Licence](https://creativecommons.org/publicdomain/zero/1.0/legalcode),
the text of which is also reproduced in the
[COPYING.CC0](./COPYING.CC0) file locally.
