from glob import glob
import src.log as log
import src.mnt as mnt
import src.upl as upl

def main():
    uuid_src_drive = 'F0F8E0EBF8E0B0D0'
    src_drive = mnt.get_src_drive(uuid_src_drive)

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
        '',
        '', 
        path_destination
    ]

    list_sync_dirs = glob(src_drive + '/*')
    
    upl.upload_files(rsync_upl_test_mode, list_sync_dirs, name_model_recv_drive, logs_dir, True)
    upl.upload_files(rsync_upl, list_sync_dirs, name_model_recv_drive, logs_dir, False)


main()