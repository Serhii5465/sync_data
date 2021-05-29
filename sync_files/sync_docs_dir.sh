#!/bin/bash

RCLONE_CONFIG=~/.config/rclone/rclone.conf
RCLONE_PATH_DIR=/cygdrive/c/portable/rclone-v1.53.2-windows-amd64
SYNC_DIR=/cygdrive/d/documents

if [[ ! -f $RCLONE_CONFIG ]]; then
    printf "Rclone's config doesn't exists\nExit...."
    exit 1
fi

if [[ ! -d $RCLONE_PATH_DIR ]]; then
    printf "Directory's Rclone doesn't exists\nExit...."
    exit 1
fi

if [[ ! -d $RCLONE_PATH_DIR ]]; then
    printf "Directory's documents doesn't exists\nExit...."
    exit 1
fi

upload_to_gdrive ()
{
    WIN_STYLE_PATH_SYNC_DIR=$(cygpath -w ${SYNC_DIR})
    $RCLONE_PATH_DIR/rclone sync -P --verbose  $WIN_STYLE_PATH_SYNC_DIR google-drive:
}

upload_to_gdrive