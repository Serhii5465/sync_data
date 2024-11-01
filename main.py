import argparse
import os
import sys
import datetime
import posixpath
import subprocess
from typing import Dict
from src import mnt, upl, constants, mnt

def parse_args(dict_src: Dict[str, any]) -> Dict[str, any]:
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external HDD')
    group = parser.add_mutually_exclusive_group()

    if '7E0E4F54' in dict_src.get('uuid'):
        group.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignoring directories which storing images of virtual machines')

    group.add_argument('-a', '--all', action='store_true', help='Copies all files, which are locating on drive')
    group.add_argument('--folder', help='Specifying the name of the folder to be synchronization', 
                        default=None,
                        nargs='+',
                        choices=list(dict_src.get('sync_dirs')))
    
    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])
    else:
        return args

def init_presets(dict_src: Dict[str, any]) -> Dict[str, any]:
    dict_dest = mnt.get_mnt_point_dest()
    
    # output: [/d/configs', '/d/vm']
    temp_list_full_path_sync_dirs = [posixpath.join(dict_src.get('mnt_point'), i) for i in dict_src.get('sync_dirs')]

    # /e/msi_gf63_files
    full_path_dest_dir = posixpath.join(dict_dest.get('mnt_point'), dict_src.get('name_dest_dir'))

    path_logs_dir = posixpath.join(dict_src.get('mnt_point'), 'logs', dict_src.get('log_name'))
    subprocess.run(['mkdir', '-p', path_logs_dir], stderr=sys.stderr, stdout=sys.stdout)

    path_log_file_dry_run_mode = posixpath.join(path_logs_dir, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + dict_dest.get('label') + '_DRY_RUN.log')
    path_log_file_upload_mode = posixpath.join(path_logs_dir, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '_' + dict_dest.get('label') + '_UPLOAD.log')

    return {
        'list_full_path_sync_dirs' : temp_list_full_path_sync_dirs,
        'full_path_dest_dir' : full_path_dest_dir,
        'path_log_file_dry_run_mode' : path_log_file_dry_run_mode,
        'path_log_file_upload_mode' : path_log_file_upload_mode
    }

def main() -> None:
    dict_src = mnt.get_src_drive()

    args = parse_args(dict_src)
    dict_presets = init_presets(dict_src)

    list_full_path_sync_dirs = dict_presets.get('list_full_path_sync_dirs')
    full_path_dest_dir = dict_presets.get('full_path_dest_dir')
    path_log_file_dry_run = dict_presets.get('path_log_file_dry_run_mode')
    path_log_file_upload = dict_presets.get('path_log_file_upload_mode')

    path_exception_file_rsync = posixpath.join(mnt.conv_path_win_to_unix(os.path.dirname(os.path.realpath(__file__))), constants.FILE_RSYNC_EXCLUSION)

    if 'no_vm' in args:
        if args['no_vm'] is True:
            list_full_path_sync_dirs = [item for item in list_full_path_sync_dirs if 'vm' not in item]

    if args['folder']:
        list_full_path_sync_dirs = [item for item in list_full_path_sync_dirs if os.path.basename(item) in args['folder']]

    rsync_test_mode_upl = [
            'rsync',
            '--recursive',          # copy directories recursively
            '--perms',              # preserve permissions
            '--times',              # preserve modification time
            '--group',              # preserve group
            '--owner',              # preserve owner (super-user only)
            '--specials',           # preserve special files
            '--human-readable',     # output numbers in a human-readable format
            '--dry-run',            # perform a trial run with no changes made
            '--stats',              # give some file-transfer stats
            '--progress',           # show progress during transfer
            '--del',                # receiver deletes during xfer, not before
            '--verbose',            # increase verbosity
            '--copy-links',         # transform symlink into referent file/dir
            '--out-format="%t %f %''b"',
            '--exclude-from=',
            '--log-file=',          # path to log file
            '',                     # source
            full_path_dest_dir
        ]
    
    #: list(str): List of launch options Rsync in base mode
    rsync_base_mode_upl = [
            'rsync',
            '--recursive',
            '--perms',
            '--times',
            '--group',
            '--owner',
            '--specials',
            '--human-readable',
            '--stats',
            '--progress',
            '--del',
            '--verbose',
            '--copy-links',
            '--out-format="%t %f %''b"',
            '--exclude-from=',
            '--log-file=',
            '',
            full_path_dest_dir
        ]
    
    # Appending exception files
    rsync_test_mode_upl[len(rsync_test_mode_upl) - 4] += path_exception_file_rsync
    rsync_base_mode_upl[len(rsync_base_mode_upl) - 4] += path_exception_file_rsync

    # Appending path to log file to rsync's arguments
    rsync_test_mode_upl[len(rsync_test_mode_upl) - 3] += path_log_file_dry_run
    rsync_base_mode_upl[len(rsync_base_mode_upl) - 3] += path_log_file_upload

    dict_rsync_test_mode = {
        'command': rsync_test_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
    }

    dict_rsync_base_mode = {
        'command': rsync_base_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs
    }
    
    upl.upload_files(dict_rsync_test_mode)
    upl.upload_files(dict_rsync_base_mode)

if __name__ == "__main__":
    main()  