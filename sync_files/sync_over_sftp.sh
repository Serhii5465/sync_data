#!/bin/bash

LOCAL_ROOT_DIR=/cygdrive/d
REMOTE_ROOT_DIR=/mnt/Data/backup_dell
SYNC_DIRS=(backups raisnet virtual_disks install)
PATH_LOGS=/cygdrive/d/logs
SSH_IDENT=~/scripts/ssh-ident

REMOTE_USER=raisnet
SSH_ADDRESS=192.168.0.100
SSH_PORT=28195


<<'COMMENT'
#Test data
SSH_ADDRESS=192.168.0.103
SSH_PORT=23560

REMOTE_USER=raisnet
LOCAL_ROOT_DIR=/cygdrive/d/1
REMOTE_ROOT_DIR=/home/raisnet/2
SYNC_DIRS=(1 2)

PATH_LOGS=/cygdrive/d/logs
SSH_IDENT=~/scripts/ssh-ident
#end_of_test_data
COMMENT


function usage(){
	echo -e "Usage: $0 [OPTION]\n"
	echo "Options"
	echo "-t, 	perform a trial run with no changes made"
	echo "-u, 	upload files"
    exit 1
}


if [ "$#" -eq 0 ]; then
	usage
fi


function check_root(){
	if [ ! -d $LOCAL_ROOT_DIR ]; then
		echo "Dir $LOCAL_ROOT_DIR does not exists.Exit..."
		exit 1
	fi
}


function dry_run(){
	echo "Check for the existence of a remote directory $REMOTE_ROOT_DIR"

	if ssh -p $SSH_PORT $REMOTE_USER@$SSH_ADDRESS "[ -d $REMOTE_ROOT_DIR ]";then
		echo "Success.Remote dir exists on host $SSH_ADDRESS"
		echo -e "Performing a trial run with no changes made\nFor more information check $PATH_LOGS"

		if [[ ! -d $PATH_LOGS ]]; then
			/bin/mkdir $PATH_LOGS
		fi

	  	for i in "${SYNC_DIRS[@]}"; do
	  		if [[ -f "$PATH_LOGS/$i.txt" && -s "$PATH_LOGS/$i.txt" ]]; then
	  			> "$PATH_LOGS/$i".txt
	  		fi
	  		echo "Sync dir $i"

	 		rsync -a --human-readable \
			--stats --out-format="%t %f %''b" \
			--progress --del \
			--dry-run \
			--compress --verbose \
			--partial \
			--update \
	 		--exclude games/ \
	 		--exclude ssh/ \
	 		--exclude Snapshots/ \
			--exclude '*.vdi' \
	 		-e "$SSH_IDENT" "$LOCAL_ROOT_DIR/$i"/ $REMOTE_USER@$SSH_ADDRESS:$REMOTE_ROOT_DIR/$i >> "$PATH_LOGS/$i".txt
	  	done
	else 
	  		echo -e "Dir $REMOTE_ROOT_DIR does not exists...\nExit..."
	  		exit 1
	fi	
}


function upload(){
	for i in "${SYNC_DIRS[@]}"; do
		rsync -a --human-readable \
		--stats --out-format="%t %f %''b" \
		--progress --del \
		--compress --verbose \
		--partial \
		--update \
		--exclude ssh/ \
		--exclude games/ \
		--exclude Snapshots/ \
		--exclude '*.vdi' \
		-e "$SSH_IDENT" "$LOCAL_ROOT_DIR/$i"/ $REMOTE_USER@$SSH_ADDRESS:$REMOTE_ROOT_DIR/$i
	done
	
	upload_vdi

	if [[ -d "$PATH_LOGS" ]]; then
		echo "Deleting logs...."
		rm -rf $PATH_LOGS
	fi
}


function upload_vdi(){
	find "$LOCAL_ROOT_DIR/${SYNC_DIRS[2]}" -type f -name "*.vdi" -print0 | while read -d $'\0' file
	do
   		clip_path_vdi=$(echo $file | grep -oP '(?<=/d/).*\w+')

		echo $file
  		echo $clip_path_vdi
   		echo "$REMOTE_ROOT_DIR/$clip_path_vdi"

   		if $SSH_IDENT $SSH_ADDRESS "[ -f $REMOTE_ROOT_DIR/$clip_path_vdi ]" < /dev/null;then
		   	echo "exists"
      		rsync -a --human-readable --partial --no-whole-file --progress --stats --out-format="%t %f %''b" \
			--del --inplace \
			-e "$SSH_IDENT" \
			$file $REMOTE_USER@$SSH_ADDRESS:$REMOTE_ROOT_DIR/$clip_path_vdi 
   		else
		   	echo "no exists"
     		rsync -a --human-readable --partial --progress --stats --out-format="%t %f %''b" \
			--del --ignore-existing --sparse \
			-e "$SSH_IDENT" \
			$file $REMOTE_USER@$SSH_ADDRESS:$REMOTE_ROOT_DIR/$clip_path_vdi 
   		fi
	done
}


while getopts "uts:" opt; do
	case $opt in
		u)
			if [[ $2 == "-s" ]]; then
				echo "Incorrect input.Flag -s must be must be listed first"
				exit -1
			fi
			upload
		;;
		t)
			check_root
			dry_run
		;;
		*)
			usage
		;;
	esac
done