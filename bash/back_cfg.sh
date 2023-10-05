#!/bin/bash

logging(){
    printf "$1" | tee -a "$2"
}

log_file="$1"
root="$2"
dir_cygwin_cfg="${root}cygwin_cfg/"

if [[ ! -d "$dir_cygwin_cfg" ]]; then
    mkdir -p "$dir_cygwin_cfg"
fi

logging "Backuping Cygwin environment\n" "$log_file"

# Backup Cygwin configs
rsync --recursive --perms  --times --group --owner --specials --human-readable \
--stats --progress --del --verbose --out-format="%t %f %b" --log-file="$log_file" \
--exclude=.git --exclude=.gitignore --exclude=README.md \
~ /etc/fstab "$dir_cygwin_cfg" 

logging "\n\nBackuping Git configs\n" "$log_file"

# Backup Git configs
name_user=$(whoami)
root_dir_src="/cygdrive/c/Users/${name_user}/"
root_dir_dest="${root}git_cfg"
list_files=(".ssh" ".bash_profile" ".bashrc" ".gitconfig" ".bash_history")

for i in ${list_files[@]}; do
    rsync --recursive --perms  --times --group --owner --specials --human-readable \
    --stats --progress --del --verbose --out-format="%t %f %b" --log-file="$log_file" \
    "${root_dir_src}${i}" "${root_dir_dest}"
done 

# Backup Cygwin packages
logging "\nBackuping Cygwin packages list\nRetrieving installed packages and their version...\n" "$log_file"

logging "$(cygcheck --check-setup --dump-only)\nFormating list and saving it to file...\n" "$log_file"

file_form_list="${dir_cygwin_cfg}list_packages.txt"
cygcheck --check-setup --dump-only | tail -n +3 | awk 'NR==1{printf $1}{printf ",%s", $1}' >> "$file_form_list"
logging "The backup file of installed packages is saved in the $file_form_list\n" "$log_file"