#!/usr/bin/env bash
# appimage.bash --- generate AppImage

# This script was adapted from
# <https://github.com/AppImage/AppImageKit/wiki/Bundling-Python-apps>.

# bash strict mode
set -euo pipefail
IFS=$'\n\t'

### Variables:
VERSION="0.1.0b2"
PYVERSION="3.8.3"
SRCDIR="${SRCDIR:-$PWD}"
OUTDIR="${OUTDIR:-$SRCDIR/dist}"
WHEEL="${WHEEL:-$OUTDIR/pomodorino-$VERSION-py3-none-any.whl}"
ICON="${ICON:-$SRCDIR/assets/logo.png}"
DESKTOP="${DESKTOP:-$SRCDIR/assets/pomodorino.desktop}"

### Functions:

die(){
    x=$?
    echo "$0: error: $@"
    exit $x
}

check(){
    echo "Check dependencies:"
    which wget || die "wget not found"
    which convert || die "imagemagick not found"
    echo Done
}

python_appimage_url(){
    ver="$1"
    minor="${ver:0:3}"
    arch="$2"
    echo "https://github.com/niess/python-appimage/releases/download/\
python$minor/python$ver-cp38-cp38-manylinux1_$arch.AppImage"
}

appimagetool_url(){
    base="https://github.com"
    # find out latest continuous build release
    read cur < <( \
        wget -q https://github.com/probonopd/go-appimage/releases -O - \
            | grep "appimagetool-.*-x86_64.AppImage" \
            | head -n 1 | cut -d '"' -f 2 \
    )
    echo "$base$cur"
}




### Make temp dir and cd into it:
dir="$(mktemp --directory --tmpdir pomodorino-appimage-XXXXXXXXXXXXXXXXXXX)"

cd "$dir"
[ "$dir" = "$PWD" ] || die "failed to cd to build dir: $dir"

### Downloads:

echo Begin downloads

echo Downloading 64 bit Python-AppImage...
wget -nv -O Python_x86_64.AppImage "$(python_appimage_url $PYVERSION x86_64)"

echo Downloading 32 bit Python-AppImage...
wget -nv -O Python_i686.AppImage "$(python_appimage_url $PYVERSION i686)"

echo Downloading appimagetool...
wget -nv -O appimagetool.AppImage "$(appimagetool_url)"

chmod 750 *.AppImage

echo "In $dir:"
ls -lA

echo "Downloads complete."



### Build Pomodorino AppImage

build()(
    arch="$1"
    builddir="build_$arch"

    [ "$PWD" = "$dir" ] || die "wrong pwd: $PWD"

    echo
    echo $arch build:
    echo Make $arch build dir at $builddir...
    mkdir "$builddir"
    cd "$builddir" || die "failed to cd to $arch build dir at $PWD/$builddir"

    echo Extract Python_$arch.AppImage...
    ../Python_$arch.AppImage --appimage-extract > /dev/null
    test -d squashfs-root || die "failed extracting ../Python_$arch.AppImage"

    echo Modify $PWD/squashfs-root...
    t="squashfs-root/opt/python3.8/lib/python3.8/site-packages"

    # HACK(2020-07-08): for some reason just using pip installs the
    # dependencies but not pomosorino itself.
    ./squashfs-root/AppRun -m pip -q install --upgrade  --target $t "$WHEEL"
    mv $t/bin/pomodorino squashfs-root/usr/bin/
    rmdir $t/bin
    sed -i -e 's|/opt/python3.8/bin/python3.8|/usr/bin/pomodorino|g' \
        ./squashfs-root/AppRun

    rm squashfs-root/usr/share/applications/python$PYVERSION.desktop
    rm squashfs-root/python$PYVERSION.desktop
    cp $DESKTOP squashfs-root/usr/share/applications/
    cp $DESKTOP squashfs-root/
    cp $ICON pomodorino.png
    for X in 64 128 256 512; do
        convert -resize 128x128 pomodorino.png pomodorino_$X.png
        mkdir -p squashfs-root/usr/share/icons/hicolor/${X}x${X}/apps/
        cp pomodorino_$X.png \
           squashfs-root/usr/share/icons/hicolor/${X}x${X}/apps/pomodorino.png
    done
    mv pomodorino.png squashfs-root/

    echo Pack it back up
    VERSION="$VERSION" ../appimagetool.AppImage squashfs-root/
    out="Pomodorino-$VERSION-$arch.AppImage"
    cp "$out" "$OUTDIR"
    echo $arch AppImage ready at: $OUTDIR/$out
)

build x86_64
#build i686
