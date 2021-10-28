import glob
import src.bash_proc as bash_proc
import os
import sys

# insert into rsync command arguments of source and path log file
def inst_log_arg(command, is_test_mode, path_logs_dir, uuid_drive, name_sync_dir):
    if (is_test_mode):
        command[len(command) - 3] = '--log-file=' + path_logs_dir + '/' + uuid_drive + '__TEST_MODE__' + name_sync_dir + '.txt'
    else:
        command[len(command) - 3] = '--log-file=' + path_logs_dir + '/' + uuid_drive + '__' + name_sync_dir + '.txt'


def upload_files(command, list_sync_dirs, uuid_disk, path_logs_dir, is_test_mode):
    for dir in list_sync_dirs:

        # set argument source of sync
        command[len(command) - 2] = dir

        # get name sync folder from full path
        # arg: /d/projects/bash-scripts/sync_files
        # result: sync_files
        name_sync_dir = os.path.basename(dir)  
        inst_log_arg(command, is_test_mode, path_logs_dir, uuid_disk, name_sync_dir)

        code = bash_proc.run_cmd(command)

        if (code.returncode != 0):
           sys.exit('Error\nCheck logs')


def upload_vdi(command1, command2, full_pth_src_dir, root_pth_src_drive, full_path_dest_dir, uuid_disk, path_logs_dir, is_test_mode):
    list_vdi_img = glob.glob(full_pth_src_dir + '/**/*.vdi', recursive=True) # search .vdi files

    name_dir_vdi = full_pth_src_dir.split(root_pth_src_drive)[1].strip('/') # output: /VirtualBox_VMs
    
    for i in list_vdi_img:

        # i='/cygdrive/d/VirtualBox_VMs/arch/arch.vdi, trim_path=/arch/arch.vdi
        trim_path = i.split(full_pth_src_dir)[1]
        #print(trim_path)

        # result: /cygdrive/g/dell_inspiron_3576/VirtualBox_VMs/arch/arch.vdi
        path_dest_vdi = full_path_dest_dir + '/' + name_dir_vdi + trim_path
        #print(path_dest_vdi)
        
        if (not os.path.isfile(path_dest_vdi)):
            command1[len(command1) - 2] = i
            command1[len(command1) - 1] = path_dest_vdi
            inst_log_arg(command1, is_test_mode, path_logs_dir, uuid_disk, name_dir_vdi)
            out = bash_proc.run_cmd(command1)
        else:
            command2[len(command2) - 2] = i
            command2[len(command2) - 1] = path_dest_vdi
            inst_log_arg(command2, is_test_mode, path_logs_dir, uuid_disk, name_dir_vdi)
            out = bash_proc.run_cmd(command2)

        if (out.returncode != 0):
           sys.exit('Transmission error\nExit')