import sys
import subprocess
from typing import Dict

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

    for idx, val in enumerate(list_sync_dirs):
        # Setting argument of source sync. folder
        command[len(command) - 2] = val

        print('\nStart syncing the ' + '\'' + list_sync_dirs[idx] + '\'' + ' folder\n')
        
        # Start synchronization
        out = subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)

        if out.returncode != 0:
            sys.exit('Error\nCheck logs')
