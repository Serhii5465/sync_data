import argparse
import sys
from typing import Dict, List
from src import mnt, upl, log, date, hdd_info


def parse_args(list_dirs: Dict[str, str], id_recv_drive: str, root_pth_src_drive: str) -> List[str]:
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external USB HDD')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--all', action='store_true', help='Copies all files, which are located in drive D')
    group.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignore directories which are using to store Virtualbox and Hyper-V virtual machines')
    # group.add_argument('-f', '--folder', help='Specifying the name of the folder to be synchronized', 
    #                     default=None, 
    #                     type=str,
    #                     choices=list_dirs.keys())

    args = vars(parser.parse_args())

    if len(sys.argv) == 1:
        parser.parse_args(['-h'])

    #: Creates list of full paths to folders for sync.
    list_full_path_sync_dirs = []
    list_name_dirs = []

    # if id_recv_drive == hdd_info.JMICRON_DRIVE().get('uuid') and (args['all'] == True or args['folder'] == 'vb' or args['folder'] == 'hv'):
    if id_recv_drive == hdd_info.JMICRON_DRIVE().get('uuid') and args['all'] == True:
        print('\nThe directory of virtual machines cannot be copied to the \'Jmicron\' driver due to his insufficient capacity.\n' 
                'Run the script for this drive with the \'-n\' parameter.')
        sys.exit()

    if args['all']:
        list_name_dirs = list(list_dirs.values())

    elif args['no_vm']:
        list_name_dirs = list(list_dirs.values())
        del list_name_dirs[len(list_name_dirs) - 2: len(list_name_dirs)]

    # elif args['folder']:
    #     list_name_dirs.append(list_dirs.get(args['folder']))

    # Concatenate folder names with root path of the source drive
    list_full_path_sync_dirs = [root_pth_src_drive + '/' + i for i in list_name_dirs]

    return list_full_path_sync_dirs



def main() -> None:
    #: str: UUID partition of HDD-source
    uuid_src_drive = hdd_info.MSI_GF63_DRIVE().get('uuid')

    #: str Path to the root of partition HDD-source: '/cygdrive/d'
    root_pth_src_drive = mnt.get_src_drive(uuid_src_drive)

    #: Tuple(str, str): UUID partition and path to the root of partition HDD-receiver:
    #: root_pth_dest_drive: '/cygdrive/f', disk_data: {name: 'Hitachi', uuid: 'FI4353BNBUHD43' }
    root_pth_dest_drive, drive_data = mnt.get_recv_drive()

    #: str: Name model of HDD-receiver
    name_model_recv_drive = drive_data.get('name')

    #: str: UUID of partition HDD-receiver
    uuid_recv_drive = drive_data.get('uuid')

    #: str: Full path to the root dir of sync on HDD-receiver
    full_path_dest_dir = root_pth_dest_drive + '/msi_gf63_files'

    #: str: Path to the log's dir: '/cygdrive/d/logs/drive_D'
    path_logs_dir = log.get_logs_dir('backup_msi_gf63')

    #: dict[str, str] : Dictionary with information of synchronized folders.
    list_sync_dirs = {
            'backups' : 'backups',
            'configs' : 'configs',
            'documents' : 'documents',
            'installers' : 'installers',
            'media' : 'media',
            'vb' : 'virtual_machines',
            # 'hv' : 'hyper_v_export_vm'
        }
    
    #: list(str): List of arguments of execution Rsync in dry-run mode
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
    
    #: list(str): List of arguments of execution Rsync in base mode
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
    
    #: list(str): List of full paths to folders which will be sync
    list_dirs = parse_args(list_sync_dirs, uuid_recv_drive, root_pth_src_drive)

    #: str: Full name of log file
    path_log_file = path_logs_dir + date.time_now() + '_' + name_model_recv_drive + '.log'

    # Appending path to log file to rsync's arguments
    rsync_test_mode_upl[len(rsync_test_mode_upl) - 3] += path_log_file
    rsync_base_mode_upl[len(rsync_base_mode_upl) - 3] += path_log_file

    dict_rsync_test_md = {
        'command': rsync_test_mode_upl,
        'list_full_path_sync_dirs': list_dirs,
        'path_log_file': path_log_file,
        'is_dry_run': True
    }

    dict_rsync_base_md = {
        'command': rsync_base_mode_upl,
        'list_full_path_sync_dirs': list_dirs,
        'path_log_file': path_log_file,
        'is_dry_run': False
    }

    upl.upload_files(dict_rsync_test_md)
    upl.upload_files(dict_rsync_base_md)

main()