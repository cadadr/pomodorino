# Pomodorino

<p align="center"><img src="assets/logo.png" width=64px alt="Pomodorino logo" /></p>

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

- Python 3
- [PyGObject](https://pygobject.readthedocs.io/en/latest/)
- [notify2](https://pypi.org/project/notify2/)
- [dbus-python](https://pypi.org/project/dbus-python/)

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

Building the Debian package is simple:

1. Install `devscripts`:

       $ sudo apt-get install devscripts

2. Run the following command to invoke `debuild`:

       $ debuild -i -us -uc -b

3. Relevant files, including the Debian package itself, will be output
   to the parent directory of your working directory.

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

The preparation for using `run.sh` is as follows:

1. Create a virtual environment:

       $ python3 -m venv .venv

2. Install Pomodorino’s dependencies:

       $ ./.venv/bin/pip install -r requirements.txt

3. Run Pomodorino:

       $ ./run.sh

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
