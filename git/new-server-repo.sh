#!/usr/bin/env sh

set -e

SERVER_DIR="/srv/git"
REPO_NAME="$1"
REPO_DIR="${SERVER_DIR}/${REPO_NAME}.git"

mkdir ${REPO_DIR}
touch ${REPO_DIR}/git-daemon-export-ok
echo "
[gitweb]
        owner = Yi Qingliang
[daemon]
        uploadpack = true
        uploadarch = true
        receivepack = true
" >> ${REPO_DIR}/config

sudo chown -R git:git ${REPO_DIR}

