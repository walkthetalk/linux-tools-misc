#!/usr/bin/env sh
set -e

selfname="`readlink -f $0`"
DSTDIR="`dirname $selfname`"
echo "dst dir is $DSTDIR"

#ADDR="git://code.qt.io/qt/"
ADDR="https://github.com/qt"
echo "src is $ADDR"

PROS=(
qt5
qtwebview
qtivi-qface
qtivi-taglib
qtlocation-mapboxgl
qtwebglplugin
qtwebkit
qtivi
qtdocgallery
qtwinextras
qtandroidextras
qtmacextras
qtapplicationmanager
qtknx
qttranslations
qtrepotools
qtspeech
qtquick1
qtdeviceutilities
qtcanvas3d
qtscript
qtdatavis3d
qtcoap
qtwayland
qtopcua
qtnetworkauth
qtimageformats
qtvoiceassistant
qtwebchannel
qtquicktimeline
qtpurchasing
qtgraphicaleffects
qtgamepad
qtsensors
qtlottie
qtxmlpatterns
qtremoteobjects
qtmultimedia
qtconnectivity
qtscxml
qtmqtt
qtwebengine-chromium
qttools
qtqa
qtquickcontrols2
qtdeclarative
qtdoc
qtactiveqt
qtx11extras
qtsvg
qtserialport
qtquickcontrols
qtvirtualkeyboard
qtserialbus
qtwebsockets
qtcharts
qtlocation
qtwebengine
qtbase
qtquick3d
qt3d
)

for i in ${PROS[*]}; do
	echo "downloading $i"
	if not [ -d "$DSTDIR/$i" ]; then
		git clone ${ADDR}/${i}.git
	else
		cd $DSTDIR/$i
		git pull ${ADDR}/${i}.git
		cd ..
	fi
done
