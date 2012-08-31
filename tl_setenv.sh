#!/bin/bash

# Author: Yi Qingliang
# this file is used for setting environment of the texlive.

if [ "$0" == "${BASH_SOURCE}" ]; then
	echo "ERROR: you need source this file, but not execute it directly!!!"
	exit 1
fi

TL_MAIN_DIR="`readlink -fe "${BASH_SOURCE}" | xargs dirname`"

PATH=${TL_MAIN_DIR}/bin/x86_64-linux:$PATH; export PATH
MANPATH=${TL_MAIN_DIR}/texmf/doc/man:$MANPATH; export MANPATH
INFOPATH=${TL_MAIN_DIR}/texmf/doc/info:$INFOPATH; export INFOPATH
OSFONTDIR="/usr/share/fonts:$OSFONTDIR"; export OSFONTDIR
