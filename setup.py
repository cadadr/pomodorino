from glob import glob
import setuptools

app_id = "com.gkayaalp.pomodorino"

with open("Readme.markdown", "r") as f:
    long_description = f.read()

def collect_data_files():
    f1 = "share/icons/hicolor/{n}x{n}/apps"
    f2 = "assets/icons/hicolor/{n}x{n}/apps/{i}.png"
    sizes = [8, 16, 22, 24, 32, 48, 64, 96, 128, 256]
    icons = [(f1.format(n=n), [f2.format(n=n, i=app_id)])
             for n in sizes]
    gsettings_schema = "data/{i}.gschema.xml".format(i=app_id)
    return [
        *icons,
        ("share/glib-2.0/schemas/", [gsettings_schema]),
        ("share/applications/", ["assets/pomodorino.desktop"]),
    ]

setuptools.setup(
    name="pomodorino",
    version="0.1.0b5",
    author="Göktuğ Kayaalp",
    author_email="self@gkayaalp.com",
    description="Simple GTK+ Pomodoro(TM) applet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gkayaalp.com/pomodorino.html",
    project_urls={
        "Bug Tracker": "https://github.com/cadadr/pomodorino/issues"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Gnome",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Utilities",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    data_files=collect_data_files(),
    entry_points={
        "console_scripts": [
            "pomodorino=pomodorino:app.main",
        ],
    },
)
