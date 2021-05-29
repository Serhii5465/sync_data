#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

function init_ethernet
{
   dhclient eth0
   ip route show  
}


function mount_dir
{
   cd ~
   mkdir .ssh
   chmod 600 .ssh
   cp /home/key/id_rsa ~/.ssh/
   chown user:user .ssh/id_rsa

   adress=192.168.0.106

   sshfs -o IdentityFile=/home/user/.ssh/id_rsa,nonempty,allow_other \
   usr123@$adress:/backup/ /home/partimag/ -p 55720
}


init_ethernet
mount_dir