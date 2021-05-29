#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

cd ~
mkdir .ssh
chmod 600 .ssh
cp /home/key/id_rsa ~/.ssh/
chown user:user .ssh/id_rsa
sshfs -o IdentityFile=/home/user/.ssh/id_rsa,nonempty,allow_other raisnet@192.168.0.100:/mnt/Data/dell/snapshots/ /home/partimag/ -p 28195