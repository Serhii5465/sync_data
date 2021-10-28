from pathlib import Path
from time import gmtime, strftime
import src.log as log
import src.bash_proc as bash_proc
import sys
import os


def check_files(*args):
    for i in args:
        if (not os.path.exists(i)):
            msg = i + " doesn't exists"
            sys.exit(msg)
            

def upload_to_gdrive(rclone_dir, sync_dir, logs_dir, date):
    win_style_path_sync_dir = bash_proc.get_cmd_output(['cygpath', '--windows', sync_dir])
    win_style_path_logs_dir = bash_proc.get_cmd_output(['cygpath', '--windows', logs_dir])

    out = bash_proc.run_cmd([rclone_dir + '/rclone.exe', 
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
    logs_dir = log.get_logs_dir('rclone')

    rclone_config = str(Path.home()) + '/.config/rclone/rclone.conf'
    rclone_path_dir = '/cygdrive/c/portable/rclone'
    sync_dir = '/cygdrive/d/documents'

    time_now = strftime('%Y-%m-%d__%H-%M-%S', gmtime())

    check_files(rclone_config, rclone_path_dir, sync_dir)
    
    upload_to_gdrive(rclone_path_dir, sync_dir, logs_dir, time_now)


main()