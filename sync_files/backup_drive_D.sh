#!/bin/bash

UUID_DEST_DRIVE_1=B20A20BD0A208109  
UUID_DEST_DRIVE_2=42D49812D4980A75

NAME_DEV_DEST_DRIVE_1=$(blkid --uuid $UUID_DEST_DRIVE_1) #output example: /dev/sdc3
NAME_DEV_DEST_DRIVE_2=$(blkid --uuid $UUID_DEST_DRIVE_2) #output example: /dev/sde2

LOGS_DIR=/cygdrive/d/logs

SYNC_DIRS=(backups documents install raisnet VirtualBox_VMs)

if [[ ! -d $LOGS_DIR ]]; then
    mkdir -p $LOGS_DIR
fi


get_mount_point ()
{
    local FULL_NAME_BLOCK_DEV=$1 #/dev/sda1

    local NAME_PART_DISK=$(echo $FULL_NAME_BLOCK_DEV | cut -c 6-) #sda1

    local WINDOWS_MOUNT_POINT=$(cat /proc/partitions | awk '$4 == "'$NAME_PART_DISK'" {print $5}') #D:\

    local UNIX_MOUNT_POINT=$(cygpath --unix $WINDOWS_MOUNT_POINT) #/cygdrive/d/
    echo "$UNIX_MOUNT_POINT"
}


upload ()
{
    local SOURCE=/cygdrive/d
    local DESTINATION=$(get_mount_point "$1")/dell_inspiron_3576

    local DATE_NOW=$(date '+%d.%m.%Y_%H-%M-%S')
    local PATH_DIR_ACTUAL_LOG=$LOGS_DIR/"$DATE_NOW"_____"$2"

    mkdir $PATH_DIR_ACTUAL_LOG

    echo $DESTINATION

    local COUNT_SUCCESS_CODE=0

    #test upload files without .vdi 
    for ((i = 0; i < $((${#SYNC_DIRS[@]}-1)); i++)); 
    do
        rsync -a --human-readable --progress --stats --verbose \
        --out-format="%t %f %''b" --delete --itemize-changes --dry-run \
        --exclude=games/ --log-file="$PATH_DIR_ACTUAL_LOG"/"${SYNC_DIRS[$i]}".txt $SOURCE/${SYNC_DIRS[$i]} $DESTINATION 

        if [[ "$?" -eq 0 ]]; then
            COUNT_SUCCESS_CODE=$((COUNT_SUCCESS_CODE + 1))
        fi
    done
    
    #test upload .vdi files
    rsync -a --human-readable --progress --stats --verbose \
    --out-format="%t %f %''b" --delete --itemize-changes --dry-run \
    --ignore-existing --copy-links --exclude=Snapshots/ --exclude=Logs/ \
    --log-file="$PATH_DIR_ACTUAL_LOG"/"${SYNC_DIRS[4]}".txt $SOURCE/${SYNC_DIRS[4]} $DESTINATION 

    if [[ "$?" -eq 0 ]]; then
        COUNT_SUCCESS_CODE=$((COUNT_SUCCESS_CODE + 1))
    fi

    if [[ "$COUNT_SUCCESS_CODE" -lt "${#SYNC_DIRS[@]}" ]]; then
        printf "ПОТРАЧЕНО.ЧЕКАЙ ЛОГИ\nEXIT...."
        exit 1
    fi  


    printf "\n\n\nOK.START UPLOADING\n\n\n"
    sleep 5


    #upload files without .vdi 
    for ((i = 0; i < $((${#SYNC_DIRS[@]}-1)); i++)); 
    do
        rsync -a --human-readable --progress --stats --verbose \
        --out-format="%t %f %''b" --delete --itemize-changes \
        --exclude=games/ $SOURCE/${SYNC_DIRS[$i]} $DESTINATION 
    done

    #upload .vdi files
    rsync -a --human-readable --progress --stats --verbose \
    --out-format="%t %f %''b" --delete --itemize-changes  \
    --ignore-existing --copy-links --exclude=Snapshots/ --exclude=Logs/ $SOURCE/${SYNC_DIRS[4]} $DESTINATION 
}


if [[ -z $NAME_DEV_DEST_DRIVE_1 ]]; then
    printf "Not found drives\nRetrying search...\n\n\n"
else
    echo "FOUND"
    upload $NAME_DEV_DEST_DRIVE_1 $UUID_DEST_DRIVE_1
    exit 0
fi


if [[ -z $NAME_DEV_DEST_DRIVE_2 ]]; then
    printf "\nNOT FOUND DRIVES\nEXIT\n"
    exit 1
else
    echo "FOUND"
    upload $NAME_DEV_DEST_DRIVE_2 $UUID_DEST_DRIVE_2
    exit 0
fi