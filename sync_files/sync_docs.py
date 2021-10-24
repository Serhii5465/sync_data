import sys
import os
import subprocess
from pathlib import Path
from time import gmtime, strftime

def get_cmd_output(command):
    return subprocess.run(command, capture_output=True, text=True)


def run_cmd(command):
    return subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)


def check_files(*args):
    for i in args:
        if (not os.path.exists(i)):
            msg = i + " doesn't exists"
            sys.exit(msg)
            

def upload_to_gdrive(rclone_dir, sync_dir, logs_dir, date):
    win_style_path_sync_dir = get_cmd_output(['cygpath', '--windows', sync_dir])
    win_style_path_logs_dir = get_cmd_output(['cygpath', '--windows', logs_dir])

    out = run_cmd([rclone_dir + '/rclone.exe', 
                        'sync', 
                        '--progress', 
                        '--verbose',
                        win_style_path_sync_dir.stdout.strip('\n'), 
                        'google-drive:',
                        '--log-file=' + win_style_path_logs_dir.stdout.strip('\n') + '\\' + date + '.txt'])
    
    
    if (out.returncode != 0):
        sys.exit('Error\nCheck logs')
    else:
        print('\nGood')


def main():

    home_dir = str(Path.home())

    logs_dir = '/cygdrive/d/logs/rclone'

    rclone_config = home_dir + '/.config/rclone/rclone.conf'
    rclone_path_dir = '/cygdrive/c/portable/rclone'
    sync_dir = '/cygdrive/d/documents'

    # create logs directory
    Path(logs_dir).mkdir(parents=True, exist_ok=True)

    time_now = strftime('%Y-%m-%d__%H-%M-%S', gmtime())

    check_files(rclone_config, rclone_path_dir, sync_dir)
    
    upload_to_gdrive(rclone_path_dir, sync_dir, logs_dir, time_now)


main()