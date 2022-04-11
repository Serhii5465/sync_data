import argparse
from src import mnt, log, upl, uuid

def prepare_sync_data(cmd_args):
    """
    Prepares all data for start synchronization:
    arrays with argument's execution for Rsync,
    checks if partition-receiver will be mount,
    creates logs' folder,
    """

# Section about: mount point,path to logs' dir, path to sync. dir
    uuid_src_drive = uuid.uuid_dell_3576_drive

    # Output: '/cygdrive/d'
    root_pth_src_drive = mnt.get_src_drive(uuid_src_drive)

    # Output: root_pth_dest_drive: '/cygdrive/f', name_model_recv_drive: 'Hitachi'
    root_pth_dest_drive, name_model_recv_drive = mnt.get_recv_drive()
    full_path_dest_dir = root_pth_dest_drive + '/dell_inspiron_3576'

    # Output: '/cygdrive/d/logs/drive_D'
    path_logs_dir = log.get_logs_dir('drive_D')

# End of section


# Section of information about different parameters of the execution Rsync

    # Dry-run mode exec. w/o creating .vdi files
    rsync_test_mode_wo_vdi = [
        'rsync',
        '--recursive',  # copy directories recursively
        '--links',  # copy symlinks as symlinks
        '--perms',  # preserve permissions
        '--times',  # preserve modification time
        '--group',  # preserve group
        '--owner',  # preserve owner (super-user only)
        '--devices',  # preserve device files (super-user only)
        '--specials',  # preserve special files
        '--human-readable',  # output numbers in a human-readable format
        '--dry-run',  # perform a trial run with no changes made
        '--stats',  # give some file-transfer stats
        '--progress',  # show progress during transfer
        '--del',  # receiver deletes during xfer, not before
        '--verbose',  # increase verbosity
        '--out-format="%t %f %''b"',
        '--exclude=Games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''',
        '',
        '',
        full_path_dest_dir
    ]

    # Basic mode exec. w/o creating .vdi files
    rsync_wo_vdi = [
        'rsync',
        '--recursive',
        '--links',
        '--perms',
        '--times',
        '--group',
        '--owner',
        '--devices',
        '--specials',
        '--human-readable',
        '--stats',
        '--progress',
        '--del',
        '--verbose',
        '--out-format="%t %f %''b"',
        '--exclude=Games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''',
        '',
        '',
        full_path_dest_dir
    ]

    # Dry-run mode exec. creating .vdi files
    rsync_test_mode_crt_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--sparse',      # handle sparse files
        '--copy-links',  # transform symlink into referent file/dir
        '',
        '',
        ''
    ]

    # Dry-run mode exec. updating .vdi files
    rsync_test_mode_upd_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--no-whole-file',  # copy files whole (w/o delta-xfer algorithm)
        '--inplace',        # rsync writes the updated data directly to the destination file.
        '--copy-links',
        '',
        '',
        ''
    ]

    # Basic mode exec. creating .vdi files
    rsync_crt_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--sparse',
        '--copy-links',
        '',
        '',
        ''
    ]

    # Basic mode exec. updating .vdi files
    rsync_upd_vdi = [
        'rsync',
        '--recursive', '--links', '--perms', '--times', '--group', '--owner', '--devices', '--specials',
        '--out-format="%t %f %''b"',
        '--progress',
        '--stats',
        '--human-readable',
        '--del',
        '--no-whole-file',
        '--inplace',
        '--copy-links',
        '',
        '',
        ''
    ]

    on_test_mode = True
    off_test_mode = False

    list_sync_dirs = [
        'backups',
        'documents',
        'installers',
        'media',
        'VirtualBox_VMs']

    """
    Appends every array's element with variable [root_pth_src_drive]
    Input: [backups, installers]
    Output: [/cygdrive/d/backups, /cygdrive/d/installers]
    """
    list_full_path_sync_dirs = [root_pth_src_drive + '/' + i for i in list_sync_dirs]

    test_mode_rsync_upl_wo_vdi = {
        'command' : rsync_test_mode_wo_vdi,
        'list_full_path_sync_dirs' : list_full_path_sync_dirs,
        'name_model_recv_drive' : name_model_recv_drive,
        'path_logs_dir' : path_logs_dir,
        'is_dry_run' : on_test_mode
    }

    base_mode_rsync_upl_wo_vdi = {
        'command' : rsync_wo_vdi,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'name_model_recv_drive': name_model_recv_drive,
        'path_logs_dir': path_logs_dir,
        'is_dry_run': off_test_mode
    }

    test_mode_rsync_upl_vdi = {
        'command1' : rsync_test_mode_crt_vdi,
        'command2' : rsync_test_mode_upd_vdi,
        'full_path_vdi_dir' : list_full_path_sync_dirs[len(list_full_path_sync_dirs) - 1],
        'root_pth_src_drive' : root_pth_src_drive,
        'full_path_dest_dir' : full_path_dest_dir,
        'name_model_recv_drive': name_model_recv_drive,
        'path_logs_dir': path_logs_dir,
        'is_dry_run': on_test_mode
    }

    base_mode_rsync_upl_vdi = {
        'command1' : rsync_crt_vdi,
        'command2' : rsync_upd_vdi,
        'full_path_vdi_dir' : list_full_path_sync_dirs[len(list_full_path_sync_dirs) - 1],
        'root_pth_src_drive' : root_pth_src_drive,
        'full_path_dest_dir' : full_path_dest_dir,
        'name_model_recv_drive': name_model_recv_drive,
        'path_logs_dir': path_logs_dir,
        'is_dry_run': off_test_mode
    }

    list_param_func = [ test_mode_rsync_upl_wo_vdi, base_mode_rsync_upl_wo_vdi, test_mode_rsync_upl_vdi, base_mode_rsync_upl_vdi ]

 # End of section

    if cmd_args['all']:
        for i in range(len(list_param_func)):
            if i < 2:
                upl.upload_files(list_param_func[i])
            else:
                upl.upload_vdi(list_param_func[i])

    if cmd_args['no_vdi']:
        list_full_path_sync_dirs.pop()
        for i in range(len(list_param_func) - 2):
            upl.upload_files(list_param_func[i])


def main():
    parser = argparse.ArgumentParser(description='Synchronization files between local storage and external USB HDD')
    parser.add_argument('-a', '--all', action='store_true', help='Copies all files, which are located on drive D')
    parser.add_argument('-n', '--no-vdi', action='store_true', help='Copies all files, ignoring virtual disk images (.vdi) used by VirtualBox')

    args = vars(parser.parse_args())

    if not args['all'] and not args['no_vdi']:
        parser.parse_args(['-h'])
    else:
        prepare_sync_data(args)

main()