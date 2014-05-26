#!/bin/bash

if [ "$(whoami)" != "root" ]; then
        echo "Sorry, you are not root, and can't update repos!!!"
        exit 1
fi

self_dir="`readlink -f ${BASH_SOURCE[0]} | xargs dirname`"

set -e

#rsync -a --human-readable --progress --delete rsync://mirrors.ustc.edu.cn/CTAN/systems/texlive/tlnet/ ${self_dir}/tlnet

rsync -a --human-readable --progress --exclude=mactex* --delete rsync://ctan.ijs.si/mirror/tlpretest/ ${self_dir}/tlnet
