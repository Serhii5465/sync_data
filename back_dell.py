import os
import sys
from typing import Dict, List
from src import mnt, upl, log, date, hdd_info, bash_process, script_path


def find_mnt_pt() -> Dict[str, str]:
    uuid_src_drive = hdd_info.DELL_INSPIRON_DRIVE().get('uuid')

    root_pth_src_drive = mnt.get_src_drive(uuid_src_drive) + '/'

    root_pth_dest_drive, drive_data = mnt.get_recv_drive()

    name_model_recv_drive = drive_data.get('name')
  
    full_path_dest_dir = root_pth_dest_drive + '/dell_inspiron_files/'

    return {
        'root_src' : root_pth_src_drive,
        'model_drive_recv' : name_model_recv_drive,
        'path_dest_dir' : full_path_dest_dir
    }


def main() -> None:
    mnt_data = find_mnt_pt()

    root_src = mnt_data.get('root_src')
    model_drive_recv = mnt_data.get('model_drive_recv')
    path_dest_dir = mnt_data.get('path_dest_dir')

    path_log = log.get_logs_dir('backup_dell_inspiron') + date.time_now() + '_' + model_drive_recv + '.log'

    list_sync_dirs = ['system', 'documents']

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
            '--exclude=autohotkey_scripts',
            '--exclude=services',
            '--exclude=adb',
            '--exclude=cygwin64',
            '--log-file=',          # path to log file
            '',                     # source
            path_dest_dir
        ]
    
    rsync_base_mode_upl = [
            'rsync',
            '--recursive',          # copy directories recursively
            '--perms',              # preserve permissions
            '--times',              # preserve modification time
            '--group',              # preserve group
            '--owner',              # preserve owner (super-user only)
            '--specials',           # preserve special files
            '--human-readable',     # output numbers in a human-readable format
            '--stats',              # give some file-transfer stats
            '--progress',           # show progress during transfer
            '--del',                # receiver deletes during xfer, not before
            '--verbose',            # increase verbosity
            '--copy-links',         # transform symlink into referent file/dir
            '--out-format="%t %f %''b"',
            '--exclude=autohotkey_scripts',
            '--exclude=services',
            '--exclude=adb',
            '--exclude=cygwin64',
            '--log-file=',          # path to log file
            '',                     # source
            path_dest_dir
        ]

    rsync_test_mode_upl[len(rsync_test_mode_upl) - 3] += path_log
    rsync_base_mode_upl[len(rsync_base_mode_upl) - 3] += path_log

    list_full_path_sync_dirs = [root_src + i for i in list_sync_dirs]
    
    dict_rsync_test_md = {
        'command': rsync_test_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'path_log_file': path_log,
        'is_dry_run': True
    }

    dict_rsync_base_md = {
        'command': rsync_base_mode_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'path_log_file': path_log,
        'is_dry_run': False
    }

    upl.upload_files(dict_rsync_test_md)
    upl.upload_files(dict_rsync_base_md)

    cmd_back_cfg = ['bash', script_path.get_path() + '/bash/back_cfg.sh', path_log, path_dest_dir]

    out = bash_process.run_cmd(cmd_back_cfg)

    if out.returncode != 0:
        sys.exit('Error\nCheck logs')


main()