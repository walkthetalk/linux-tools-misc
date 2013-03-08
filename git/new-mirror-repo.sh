#!/usr/bin/env sh

set -e

if [ "`whoami`" != "root" ]; then
	echo "ERROR: you should use root!"
	exit 1
fi

SERVER_DIR="/srv/git"
REPO_NAME="$1"
REPO_ADDR="$2"
REPO_DIR="${SERVER_DIR}/${REPO_NAME}.git"

git clone --mirror ${REPO_ADDR} ${REPO_DIR}
touch ${REPO_DIR}/git-daemon-export-ok
echo "
[gitweb]
        owner = Yi Qingliang
[daemon]
        uploadpack = true
        uploadarch = true
        receivepack = true
" >> ${REPO_DIR}/config
