import sys
from typing import Dict
from src import bash_process


def insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, name_sync_dir) -> None:
    """
    Inserts in array of arguments path to folder of the log file.
    Name file depends on if Rsync in dry-run mode.
    For example, if Rsync works in dry-run mode file will be named: Wester Digital__backups_TEST_MODE.log,
    where substring 'TEST_MODE' will be signalized about this mode.
    If Rsync will be works as usual, file wile be named: Wester Digital__backups.log
    Args:
        command: List which contains all arguments execution of the Rsync utility.
        is_test_mode: Indicates, if Rsync runs in dry-run mode.
        path_logs_dir: Full path to log file.
        name_model_recv_drive: Name model of HDD-receiver.
        name_sync_dir: Name of sync folder.
    """
    if is_test_mode:
        command[
            len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '_TEST_MODE' + '.log'
    else:
        command[
            len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '.log'


def upload_files(data_sync: Dict[str, any]) -> None:
    """
    Retrieves values from dictionary represented by data_sync and
    synchronizes files between local storage and external drive by using Rsync.
    If there is an error of synchronization, file access rights or something similar,
    the transfer will be terminated.
    Args:
        data_sync: contains info about: Rsync launch options; folders and
        their full paths; model of HDD-receiver; full path
        to log directory; whether Rsync works in dry-run mode.
    """
    command = data_sync.get('command')
    sync_dirs = data_sync.get('sync_dirs')
    list_sync_dirs = data_sync.get('list_full_path_sync_dirs')
    name_model_recv_drive = data_sync.get('name_model_recv_drive')
    path_logs_dir = data_sync.get('path_logs_dir')
    is_test_mode = data_sync.get('is_dry_run')

    for idx, val in enumerate(list_sync_dirs):
        # Setting argument of source sync. folder
        command[len(command) - 2] = val

        # Inserting in array the argument of name log file
        insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, sync_dirs[idx])
        print('\nStart syncing the ' + '\'' + sync_dirs[idx] + '\'' + ' folder\n')
        # Start synchronization
        code = bash_process.run_cmd(command)

        if code.returncode != 0:
            sys.exit('Error\nCheck logs')
