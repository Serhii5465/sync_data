import glob
from src import mnt, log, upl, hdd_info

def main():
    #uuid_src_drive = hdd_info.jmicron_drive
    src_drive = mnt.get_src_drive(hdd_info.jmicron_drive.get('uuid'))

    recv_drive, name_model_recv_drive = mnt.get_recv_drive()
    path_destination = recv_drive + '/jmicron'

    logs_dir = log.get_logs_dir('jmicron')

    rsync_upl_test_mode = [
        'rsync', 
        '--recursive',          # copy directories recursively 
        '--links',              # copy symlinks as symlinks
        '--perms',              # preserve permissions
        '--times',              # preserve modification time
        '--group',              # preserve group
        '--owner',              # preserve owner (super-user only)
        '--devices',            # preserve device files (super-user only)
        '--specials',           # preserve special files
        '--human-readable',     # output numbers in a human-readable format
        '--dry-run',            # perform a trial run with no changes made
        '--stats',              # give some file-transfer stats
        '--progress',           # show progress during transfer
        '--del',                #receiver deletes during xfer, not before
        '--verbose',            #increase verbosity
        '--out-format="%t %f %''b"',
        '--exclude=dell_inspiron_3576/',
        '',
        '', 
        path_destination
    ]

    rsync_upl = [
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
        '--exclude=dell_inspiron_3576/',
        '',
        '', 
        path_destination
    ]

    list_full_path_sync_dirs = glob.glob(src_drive + '/*')

    on_test_mode = True
    off_test_mode = False

    test_mode_rsync_upl = {
        'command' : rsync_upl_test_mode,
        'list_full_path_sync_dirs' : list_full_path_sync_dirs,
        'name_model_recv_drive': name_model_recv_drive,
        'path_logs_dir': logs_dir,
        'is_dry_run': on_test_mode
    }

    base_mode_rsync_upl = {
        'command': rsync_upl,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'name_model_recv_drive': name_model_recv_drive,
        'path_logs_dir': logs_dir,
        'is_dry_run': off_test_mode
    }

    upl.upload_files(test_mode_rsync_upl)
    upl.upload_files(base_mode_rsync_upl)


main()