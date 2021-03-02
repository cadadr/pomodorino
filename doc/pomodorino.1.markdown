---
title: POMODORINO
section: 1
header: User Manual
footer: pomodorino v0.1.0b8
date: March 1, 2021
---

# NAME

pomodorino - Simple pomodoro timer applet.

# SYNOPSIS

**pomodorino [OPTION]**

# DESCRIPTION

Pomodorino is a lightweight, simple Pomodoro timer system tray
application written using Python 3 and GTK 3.

What sets it apart is that it’s totally FOSS (licensed under GPLv3+)
and really lightweight.  Alternative Linux apps that I could find were
either paid and proprietrary or they used rather heavy technologies
like Electron.

Using Pomodorino should be rather straight-forward if you know about
the Pomodoro Technique(R) (which is a registered trademark of
Francesco Cirillo).

# OPTIONS

Pomodorino itself does not have any command line arguments at this
point, but the following arguments can be used to configure GTK+, like
with other GTK+ applications:

**-h, --help**
: Show help options

**--help-all**
: Show all help options

**--help-gapplication**
: Show GApplication options

**--help-gtk**
: Show GTK+ Options

**--display=DISPLAY**
: X display to use

# USAGE

The main interface of Pomodorino is its system tray indicator’s menu.
These menu items allow you to start and pause pomodoros and breaks,
skip breaks, cancel an ongoing pomodoro or break, or to reset the
timer.

When you cancel a phase, Pomodorino returns to the state prior to that
phase.  E.g., if you cancel an ongoing pomodoro, Pomodorino will
return to the state where a pomodoro period is pending, which can be
then started again using the menu.

When you reset, the whole state is cleared, the number of pomodoros
and breaks is reset, and it is as if you just started Pomodorino.
Configuration values are not affected by this, they are not reset.

The configuration popup window can be accessed through the indicator
menu, and contains some useful options.  You can change the durations
of pomodoros, long breaks and short breaks through this interface.  It
is also possible to enable or disable desktop notifications here, and
by default they are enabled.  For now, desktop notifications are the
only interface by which Pomodorino alerts you when phases start and
finish, so it’s advisable to not disable desktop notifications.

Another option is the feature termed ‘ease-in period’.  Essentially,
the ease-in period is a short break that precedes the first pomodoro
of a session.  This can be enabled in the configuration popup.  The
purpose of this feature is to help get started with the work, and
frame some short amount of time before it to focus.

When you’re done with your configurations, you can simply close the
settings popup.  Your settings will be saved permanently.

User settings are saved through GSettings, but users of custom desktop
setups may opt to using alternatives like xsettingsd to replace it.

Finally, Pomodorino can be closed using the ‘Quit’ menu item.

# ENVIRONMENT

Pomodorino recognises some environment variables, mostly for debugging
purposes.

**DEBUG_LOCALE_DIR**
: Setting this environment variable to a directory path results in
: that path being set as the locale directory.  This is useful when
: testing locale changes.

**DEBUG_CHECK_GETTEXT**
: If this variable is present in the environment, Pomodorino will
: print the value of the `LANGUAGE` variable and a sample translated
: string, then, it will exit without starting the application.
: This is useful in testing whether locales are accessed or
: installed correctly.  You can set `LANGUAGE` along with this
: to test with different locales.

**DEBUG_CLOCK_RESOLUTION**
: This variable can be used to modify the length of a second
: for Pomodorino, in terms of milliseconds.  Normally,
: Pomodorino assumes a second is 1000 milliseconds long,
: as expected, but while testing it may be useful to have
: it go quicker.

# REPORTING BUGS

Issues can be reported at the issue tracker, available at the URL
<https://github.com/cadadr/pomodorino/issues>.

# COPYING

Copyright (C) 2019, 2020, 2021  Göktuğ Kayaalp <self at gkayaalp dot com>

Permission is granted to make and distribute verbatim copies  of  this
document  provided the copyright notice and this permission notice are
preserved on all copies.

Permission is granted to copy and distribute modified versions of this
document  under the conditions for verbatim copying, provided that the
entire resulting derived work is distributed under the terms of a per‐
mission notice identical to this one.

Permission is granted to copy and distribute translations of this doc‐
ument into another language, under the above conditions  for  modified
versions, except that this permission notice may be stated in a trans‐
lation approved by the Free Software Foundation.

# AUTHORS

Göktuğ Kayaalp <self at gkayaalp dot com> is the original author of
Pomodorino and this manpage.
