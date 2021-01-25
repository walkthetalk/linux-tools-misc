SET QT_DIR=D:\develop\qt
SET SRC_DIR=D:\develop\source\qt6.0.1
SET DST_DIR=D:\develop\build\qt6.0.1

SET PATH=%PATH%;%QT_DIR%\Tools\CMake_64\bin;%QT_DIR%\Tools\mingw810_64\bin;%QT_DIR%\Tools\Ninja
cd %SRC_DIR%
configure -prefix %DST_DIR% -release -nomake tests -nomake examples
