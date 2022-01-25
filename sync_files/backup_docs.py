import os
import sys
from pathlib import Path

import src.bash_proc as bash_proc
import src.log as log
import src.time as time

def check_files(*list_files):
    """
    This function checks if list full.
    Otherwise, if at least one of the elements in the array missing,
    the script terminates
    :param list_files: array of verifiable files
    """

    for item in list_files:
        if not os.path.exists(item):
            msg = item + " doesn't exists"
            sys.exit(msg)
            

def upload_to_gdrive(rclone_dir, sync_dir, logs_dir):
    """
    Uploads files from local folder to Google Drive.
    Under normal conditions the process finishes work and has an exit code of 0.
    Otherwise the process has an exit code different from 0 and the script finishes terminates
    :param rclone_dir: full path to Rclone utility
    :param sync_dir: synchronized folder
    :param logs_dir: directory log file
    """

    """
    Converting Unix-like path to Windows form by using Cygpath.exe utility.
    Convertion runs in separate process.
    """
    win_style_path_sync_dir = bash_proc.get_cmd_output(['cygpath', '--windows', sync_dir])
    win_style_path_logs_dir = bash_proc.get_cmd_output(['cygpath', '--windows', logs_dir])

    date_now = time.get_time_now()

    # Process syncing folder with Gdrive
    out = bash_proc.run_cmd([rclone_dir + '/rclone.exe', 
                        'sync', 
                        '--progress', 
                        '--verbose',
                        win_style_path_sync_dir.stdout.strip('\n'), 
                        'google-drive:',
                        '--log-file=' + win_style_path_logs_dir.stdout.strip('\n') + '/' + date_now +'.log'])
    
    if out.returncode != 0:
        sys.exit('Error\nCheck logs')
    else:
        print('\nGood')


def main():
    create_subfolder = False
    # Creates log folder and retuning full path in variable
    logs_dir = log.get_logs_dir('rclone', create_subfolder)

    #Configuration file that stores all the data for the connection Rclone utility for my Google Drive
    rclone_config = str(Path.home()) + '/.config/rclone/rclone.conf'

    #Full path where located Rclone
    rclone_path_dir = '/cygdrive/c/portable/rclone'

    #Synchronized folder
    sync_dir = '/cygdrive/d/documents'

    check_files(rclone_config, rclone_path_dir, sync_dir)
    upload_to_gdrive(rclone_path_dir, sync_dir, logs_dir)

main()