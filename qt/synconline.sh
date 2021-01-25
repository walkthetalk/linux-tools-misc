#!/bin/bash

if [ "$(whoami)" != "root" ]; then
        echo "Sorry, you are not root, and can't update repos!!!"
        exit 1
fi

self_dir="`readlink -f ${BASH_SOURCE[0]} | xargs dirname`"

set -e

PathList=(
	windows_x86/desktop/licenses
	windows_x86/desktop/qt6_601
	windows_x86/desktop/qt6_601_src_doc_examples
	windows_x86/desktop/tools_cmake
	windows_x86/desktop/tools_conan
	windows_x86/desktop/tools_generic
	windows_x86/desktop/tools_ifw
	windows_x86/desktop/tools_maintenance
	windows_x86/desktop/tools_mingw/qt.tools.win64_mingw810
	windows_x86/desktop/tools_mingw/Updates.xml
	windows_x86/desktop/tools_ninja
	windows_x86/desktop/tools_qtcreator/qt.tools.qtcreator
	windows_x86/desktop/tools_qtcreator/Updates.xml
	windows_x86/root/qt
)

#MIRRORS="mirrors.ustc.edu.cn/qtproject"
MIRRORS="mirrors.bit.edu.cn/qtproject"
#MIRRORS="mirrors.tuna.tsinghua.edu.cn/qt"
#MIRRORS="mirrors.hust.edu.cn/qtproject"

for p in ${PathList[@]};do
	echo $p
	CURDIR=${self_dir}/onlinerepo/`dirname $p`
	mkdir -p ${CURDIR}
	rsync -a --human-readable --progress \
		--exclude=*msvc* \
		--exclude=*backup_official* \
		--exclude=Updates_backup_* \
		--exclude=*debug_info* \
		rsync://${MIRRORS}/online/qtsdkrepository/$p ${CURDIR}
done
