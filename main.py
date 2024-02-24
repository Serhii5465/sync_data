import argparse
import sys
import datetime
from typing import Dict
from pathlib import Path
from src import constants, mnt, upl

def parse_args() -> Dict[str, any]:
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external HDD')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all', action='store_true', help='Copies all files, which are locating on drive')
    group.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignoring directories which storing images of virtual machines')
    group.add_argument('-f', '--folder', help='Specifying the name of the folder to be synchronization', 
                        default=None, 
                        type=str,
                        choices=list(constants.MSI_GF63_SRC_DRIVE_1().get('sync_dirs')) + list(constants.MSI_GF63_SRC_DRIVE_2().get('sync_dirs')))


    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])
    else:
        return args

def init_mnt_point() -> Dict[str, str]:
    #: Dict[str, list[str]]: The disk UUID and a list of synchronized folders: uuid: '8E76883376881DD9', list['dir1', 'dir2']
    src_drive_1 = constants.MSI_GF63_SRC_DRIVE_1()
    src_drive_2 = constants.MSI_GF63_SRC_DRIVE_2()

    #: str: The Cygwin-style paths to the source disk: /cygdrive/d/
    root_pth_src_drive_1 = mnt.get_src_drive(src_drive_1.get('uuid'))
    root_pth_src_drive_2 = mnt.get_src_drive(src_drive_2.get('uuid'))
    
    temp_list_full_path_sync_dirs_1 = [root_pth_src_drive_1 + '/' + i for i in src_drive_1.get('sync_dirs')]
    temp_list_full_path_sync_dirs_2 = [root_pth_src_drive_2 + '/' + i for i in src_drive_2.get('sync_dirs')]

    #: Tuple(str, str): UUID partition and path to the root of partition HDD-receiver:
    #: root_pth_dest_drive: '/cygdrive/f', disk_data: {name: 'Hitachi', uuid: 'FI4353BNBUHD43' }
    root_pth_dest_drive, drive_data = mnt.get_recv_drive()

    #: str: Name model of HDD-receiver
    name_model_recv_drive = drive_data.get('name')

    #: str: The path to the root folder where backups are stored
    full_path_dest_dir = root_pth_dest_drive + '/msi_gf63_files'

    #: str: Path to the log's dir: '/cygdrive/d/logs/drive_D'
    path_logs_dir = '/cygdrive/d/logs/backup_msi_gf63/' 
    Path(path_logs_dir).mkdir(parents=True, exist_ok=True)

    #: str: Full name of log file
    path_log_file = path_logs_dir + datetime.datetime.now().strftime("%Y-%m-%d_%H\uA789%M\uA789%S") + '_' + name_model_recv_drive + '.log'

    return {
        'list_full_path_sync_dirs' : temp_list_full_path_sync_dirs_1 + temp_list_full_path_sync_dirs_2,
        'full_path_dest_dir' : full_path_dest_dir,
        'path_log_file' : path_log_file
    }


def main() -> None:
    cli_arg = parse_args()
    mnt_points = init_mnt_point()

    list_full_path_sync_dirs = mnt_points.get('list_full_path_sync_dirs')
    full_path_dest_dir = mnt_points.get('full_path_dest_dir')
    path_log_file = mnt_points.get('path_log_file')

    if cli_arg['no_vm']:
        list_full_path_sync_dirs.pop()
        
    elif cli_arg['folder']:
        list_full_path_sync_dirs = list(filter(lambda x: cli_arg['folder'] in x, list_full_path_sync_dirs))

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