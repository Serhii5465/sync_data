#!/bin/bash

UNIX_STYLE_SRC_DIR='/cygdrive/d/raisnet/music'
WIN_STYLE_SRC_DIR=$(cygpath --windows $UNIX_STYLE_SRC_DIR)

FULL_DEST_DIR='/storage/self/primary/music'
ROOT_DIR_INTRL_MEM=$(dirname $FULL_DEST_DIR)

RESULT=$(adb shell "[ -d $FULL_DEST_DIR ] || echo 1")

if [ -z "$RESULT" ]; then
    echo "Folder exists!"
    adb push --sync $WIN_STYLE_SRC_DIR $ROOT_DIR_INTRL_MEM
else
    echo "Folder not found!"
    adb push $WIN_STYLE_SRC_DIR $ROOT_DIR_INTRL_MEM
fi