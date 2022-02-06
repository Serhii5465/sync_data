import glob
import os
import sys
from src import bash_proc

def insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, name_sync_dir):
    """
    Inserting in array of arguments path to folder of the log file.
    Name file depends by if Rsync in dry-run mode.
    For example,if Rsync works in dry-run mode file will be named: Wester Digital__backups_TEST_MODE.log,
    where substring 'TEST_MODE' will be signalized about this mode.
    If Rsync will be works as usual, file wile be named: Wester Digital__backups.log
    :param command: list which contains all arguments execution of the Rsync utility
    :param is_test_mode: indicates, if Rsync runs in dry-run mode
    :param path_logs_dir: full path to log file
    :param name_model_recv_drive: name model of HDD-receiver
    :param name_sync_dir: name of synced folder
    """
    if is_test_mode:
        command[len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '_TEST_MODE' +'.log'
    else:
        command[len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '.log'


def upload_files(args):
    """
    Synchronizes files between local storage and external drive by using Rsync.
    If there is an error of synchronization, file access rights or something similar,
    the transfer will be terminated.
    :param args: Contains following fields:
    command - list of different argument's execution for Rsync;
    list_full_path_sync_dirs - full path to specific sync. folder (Example: /cygdrive/d/installers);
    name_model_recv_drive - model HDD-receiver;
    path_logs_dir - logs' directory;
    is_dry_run - is Rsync running in dry-run mode.
    """

    command = args.get('command')
    list_sync_dirs = args.get('list_full_path_sync_dirs')
    name_model_recv_drive = args.get('name_model_recv_drive')
    path_logs_dir = args.get('path_logs_dir')
    is_test_mode = args.get('is_dry_run')

    for dir in list_sync_dirs:
        # Setting argument of source sync. folder
        command[len(command) - 2] = dir

        """
        # Getting name of sync folder from full path
        # Arg: /d/projects/bash-scripts/sync_files
        # Output: sync_files
        """
        name_sync_dir = os.path.basename(dir)

        #Inserting in array the argument of name log file
        insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, name_sync_dir)
        # Start synchronization
        code = bash_proc.run_cmd(command)

        if (code.returncode != 0):
           sys.exit('Error\nCheck logs')


def upload_vdi(args):
    """
    Uploading files of VirtualBox to external HDD. if file doesn't exist on
    receiver, Rsync will be creates it. Otherwise, Rsync will be updates it.
    For creating big parse file be like VDI, Rsync in first execution will be starts with
    argument --sparse.
    For updates existing VDI, Rsync will be works with agruments --no-whole-file and --inplace.
    For more detail information: https://linux.die.net/man/1/rsync
    :param args: Contains following fields:
    command1 - list of different argument's execution  Rsync for creating VDI files;
    command2 - list of different argument's execution  Rsync for updating VDI files;
    full_path_vdi_dir - path to dir with VDI files (Example: /cygdrive/d/VirtualBox_VMs);
    root_pth_src_drive - drive partition letter in UNIX-format (Example: /cygdrive/d/);
    full_path_dest_dir - full path to folder-destination;
    name_model_recv_drive - model HDD-receiver;
    path_logs_dir - logs' directory;
    is_dry_run - is Rsync running in dry-run mode.
    """

    command1 = args.get('command1')
    command2 = args.get('command2')
    full_pth_src_dir = args.get('full_path_vdi_dir')
    root_pth_src_drive = args.get('root_pth_src_drive')
    full_path_dest_dir = args.get('full_path_dest_dir')
    name_model_recv_drive = args.get('name_model_recv_drive')
    path_logs_dir = args.get('path_logs_dir')
    is_test_mode = args.get('is_dry_run')

    # Recursive search .vdi files
    list_vdi_img = glob.glob(full_pth_src_dir + '/**/*.vdi', recursive=True)

    """
    Getting sync. folder from full path
    Arg: /cygdrive/d/VirtualBox_VMs
    Output: VirtualBox_VMs
    """
    name_dir_vdi = full_pth_src_dir.split(root_pth_src_drive)[1].strip('/')

    for i in list_vdi_img:

        """
        Getting VDI file from path and save its in [trim_path] variable
        i='/cygdrive/d/VirtualBox_VMs/arch/arch.vdi, trim_path=/arch/arch.vdi
        """
        trim_path = i.split(full_pth_src_dir)[1]

        """
        Concating all variable to variable, which contains path to the VDI file
        Result: /cygdrive/g/dell_inspiron_3576/VirtualBox_VMs/arch/arch.vdi
        """
        path_dest_vdi = full_path_dest_dir + '/' + name_dir_vdi + trim_path

        # Creating VDI file
        if not os.path.isfile(path_dest_vdi):
            command1[len(command1) - 2] = i
            command1[len(command1) - 1] = path_dest_vdi
            insert_log_arg(command1, is_test_mode, path_logs_dir, name_model_recv_drive, name_dir_vdi)
            out = bash_proc.run_cmd(command1)
        # Updating VDI file
        else:
            command2[len(command2) - 2] = i
            command2[len(command2) - 1] = path_dest_vdi
            insert_log_arg(command2, is_test_mode, path_logs_dir, name_model_recv_drive, name_dir_vdi)
            out = bash_proc.run_cmd(command2)

        if out.returncode != 0:
           sys.exit('Transmission error\nExit')