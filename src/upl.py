import sys
from typing import Dict
from src import bash_process, date


def upload_files(data_sync: Dict[str, any]) -> None:
    """
    Retrieves values from dictionary represented by data_sync and
    synchronizes files between local storage and external drive by using Rsync.
    If there is an error of synchronization, file access rights or something similar,
    the transfer will be terminated.
    Args:
        data_sync: contains info about: Rsync launch options;
        full paths to synchronized folders; full path
        to log file; whether Rsync works in dry-run mode.
    """
    command = data_sync.get('command')
    list_sync_dirs = data_sync.get('list_full_path_sync_dirs')
    path_log_file = data_sync.get('path_log_file')
    is_test_mode = data_sync.get('is_dry_run')

    f = None

    if is_test_mode == True:
        f = open(path_log_file, 'w')
        f.write("TEST MODE\n")
    else:
        f = open(path_log_file, 'a')
        f.write("\n\nUPLOADING MODE\n")
    
    f.close()

    for idx, val in enumerate(list_sync_dirs):
        # Setting argument of source sync. folder
        command[len(command) - 2] = val

        print('\nStart syncing the ' + '\'' + list_sync_dirs[idx] + '\'' + ' folder\n')
        
        # Start synchronization
        code = bash_process.run_cmd(command)

        if code.returncode != 0:
            sys.exit('Error\nCheck logs')
