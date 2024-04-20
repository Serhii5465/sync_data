import argparse
import sys
import datetime
from typing import Dict
from pathlib import Path
from src import mnt, upl

def parse_args(dict_src: Dict[str, any]) -> Dict[str, any]:
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external HDD')
    group = parser.add_mutually_exclusive_group()

    if '347E0E947E0E4F54' in dict_src.get('uuid'):
        group.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignoring directories which storing images of virtual machines')

    group.add_argument('-a', '--all', action='store_true', help='Copies all files, which are locating on drive')
    group.add_argument('-f', '--folder', help='Specifying the name of the folder to be synchronization', 
                        default=None, 
                        type=str,
                        choices=list(dict_src.get('sync_dirs')))
    
    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])
    else:
        return args

def init_presets(dict_src: Dict[str, any]) -> Dict[str, any]:
    dict_dest = mnt.get_mnt_point_dest()

    # Example output: ['/cygdrive/d/configs', '/cygdrive/d/vm']
    temp_list_full_path_sync_dirs = [dict_src.get('mnt_point') + i for i in dict_src.get('sync_dirs')]

    # /cygdrive/e/msi_gf63_files
    full_path_dest_dir = dict_dest.get('mnt_point') + dict_src.get('name_dest_dir')

    path_logs_dir = '/cygdrive/d/logs/' + dict_src.get('log_name')
    Path(path_logs_dir).mkdir(parents=True, exist_ok=True)

    path_log_file = path_logs_dir + '/' + datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S") + '_' + dict_dest.get('label') + '.log'
    
    return {
        'list_full_path_sync_dirs' : temp_list_full_path_sync_dirs,
        'full_path_dest_dir' : full_path_dest_dir,
        'path_log_file' : path_log_file
    }

def main() -> None:
    dict_src = mnt.get_mnt_point_src()
    
    args = parse_args(dict_src)
    dict_presets = init_presets(dict_src)

    list_full_path_sync_dirs = dict_presets.get('list_full_path_sync_dirs')
    full_path_dest_dir = dict_presets.get('full_path_dest_dir')
    path_log_file = dict_presets.get('path_log_file')

    if 'no_vm' in args:
        if args['no_vm'] is True:
            for i in list_full_path_sync_dirs:
                if 'vm' in i:
                    list_full_path_sync_dirs.remove(i)

    elif args['folder']:
        list_full_path_sync_dirs = list(filter(lambda x: args['folder'] in x, list_full_path_sync_dirs))

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
            '--exclude=Hyper-V',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '--exclude=logs/',
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
            '--exclude=Hyper-V',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '--exclude=logs/',
            '--log-file=',
            '',
            full_path_dest_dir
        ]
    
    # Appending path to log file to rsync's arguments
    rsync_test_mode_upl[len(rsync_test_mode_upl) - 3] += path_log_file
    rsync_base_mode_upl[len(rsync_base_mode_upl) - 3] += path_log_file

    dict_rsync_test_mode = {
        'command': rsync_test_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'path_log_file': path_log_file,
        'is_dry_run': True
    }

    dict_rsync_base_mode = {
        'command': rsync_base_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'path_log_file': path_log_file,
        'is_dry_run': False
    }
    
    upl.upload_files(dict_rsync_test_mode)
    upl.upload_files(dict_rsync_base_mode)


main()