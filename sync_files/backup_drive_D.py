""" Requires python >= 3.7 to work method get_cmd_output 
Changed in version 3.7:
Added the capture_output parameter.
"""


from genericpath import isfile
import subprocess
import sys
import glob
import os
from pathlib import Path
from time import gmtime, strftime


# store stdout command in variable
def get_cmd_output(command):
    return subprocess.run(command, capture_output=True, text=True)


# get output command in real time
def run_cmd(command):
    return subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)
    

# get unix-like mount point partition disk by his uuid
def get_mount_point(uuid):
    name_block_dev = get_cmd_output(['blkid', '--uuid', uuid]) #stdout example: /dev/sda1\n
    
    if(name_block_dev.returncode != 0):
        return name_block_dev

    #print(name_block_dev.stdout.strip("\n"))

    # output: CompletedProcess(args=['cygpath', '--windows', '/dev/sda2'], returncode=0, stdout='\\\\.\\D:\n', stderr='')
    win_mnt_point = get_cmd_output(['cygpath', '--windows', name_block_dev.stdout.strip('\n')])

   # print(win_mnt_point)
    #print(win_mnt_point.stdout.strip('\n')[4:]) # D:

    # output CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
    unix_mnt_point = get_cmd_output(['cygpath', '--unix', win_mnt_point.stdout.strip('\n')[4:]])

    #print(unix_mnt_point)
    #print(unix_mnt_point.stdout.strip('\n')) # /cygdrive/d
    
    #return unix_mnt_point.stdout.strip('\n')
    # output CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
    return unix_mnt_point 


# insert into rsync command arguments of source and path log file
def insert_arg_cmd(command, source, sync_dir, destination, uuid_disk, logs_dir, test_mode):
    
    if(source.endswith('.vdi')): # check if source variable contains string of full path to .vdi file 
        command[len(command) - 2] = source 
        command[len(command) - 1] = destination
    else:                       # otherwise source contains sync folder
        command[len(command) - 2] = source + sync_dir  
    
    if (test_mode):
        command[len(command) - 3] = '--log-file=' + logs_dir + '/' + uuid_disk + '__TEST_MODE__' + sync_dir + '.txt'
    else:
        command[len(command) - 3] = '--log-file=' + logs_dir + '/' + uuid_disk + '__' + sync_dir + '.txt'

    
#upload files without .vdi images
def upload(command, path_src, list_sync_dirs, uuid_disk, logs_dir, test_mode):
    for i in range(len(list_sync_dirs)):

        insert_arg_cmd(command, path_src, list_sync_dirs[i], None, uuid_disk, logs_dir, test_mode)
        code = run_cmd(command)

        if (code.returncode != 0):
           sys.exit('Error\nCheck logs')

        
def upload_vdi(command1, command2, path_src, sync_dir, uuid_disk, destination, logs_dir, test_mode):

    list_vdi_img = glob.glob(path_src + sync_dir + '/**/*.vdi', recursive=True) # search .vdi files
    
    for i in list_vdi_img:
        clip_path_vdi_img = i[11:] # i='/cygdrive/d/VirtualBox_VMs/arch/arch.vdi, clip_path_vdi_img=/VirtualBox_VMs/arch/arch.vdi

        print(i)
        print(clip_path_vdi_img)
        out = ''
        print(destination + clip_path_vdi_img) # /cygdrive/g/dell_inspiron_3576/VirtualBox_VMs/arch/arch.vdi

        path_vdi_recv = destination + clip_path_vdi_img

        if (not os.path.isfile(path_vdi_recv)):
            insert_arg_cmd(command1, i, sync_dir, path_vdi_recv, uuid_disk, logs_dir, test_mode)
            print(command1)
            print('create')
            out = run_cmd(command1) # create file
        else:
            insert_arg_cmd(command2, i, sync_dir, path_vdi_recv, uuid_disk, logs_dir, test_mode)
            print(command2)
            print('update')
            out = run_cmd(command2) # update file

        if (out.returncode != 0):
            sys.exit('Transmission error\nExit\n')


def main():
    uuid_recv_drive_1 = '01D7B5F7EF7D6100'  # Wester Digistal 1Tb
    uuid_recv_drive_2 = '01D7B5E18B1C3670'  # Hitahci 500Gb
    
    source = '/cygdrive/d/'

    logs_dir = source + 'logs'

    list_sync_dirs = [
        'backups', 
        'documents', 
        'install', 
        'raisnet',
        'VirtualBox_VMs']

    destination = get_mount_point(uuid_recv_drive_1)

    # create logs directory
    Path(logs_dir).mkdir(parents=True, exist_ok=True)

    cur_uuid = ''

    if(destination.returncode != 0):
        destination = get_mount_point(uuid_recv_drive_2)
        if(destination.returncode != 0):
            sys.exit('No mounted devices found')
        else:
            cur_uuid = uuid_recv_drive_2
            destination = destination.stdout.strip('\n')
    else:
        cur_uuid = uuid_recv_drive_1
        destination = destination.stdout.strip('\n')

    destination += '/dell_inspiron_3576' # full path destination
   
    rsync_test_mode_wo_vdi = [
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
        '--exclude=games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''',
        '',
        '', 
        destination
    ]

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
        '--exclude=games/',
        '--exclude=Snapshots/',
        '--exclude=Logs/',
        '''--exclude=*.vdi''', 
        '',
        '', 
        destination
    ]

    rsync_test_mode_crt_vdi = [
        'rsync', 
        '--recursive', '--links', '--perms','--times', '--group', '--owner', '--devices', '--specials', # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run', 
        '--out-format="%t %f %''b"',
        '--progress', 
        '--stats',
        '--human-readable',
        '--del',
        '--sparse',                 # handle sparse files
        '--copy-links',             # transform symlink into referent file/dir
        '',
        '',
        ''
    ]

    rsync_test_mode_upd_vdi = [
        'rsync', 
        '--recursive', '--links', '--perms','--times', '--group', '--owner', '--devices', '--specials', # archive mode; equals -rlptgoD or -a (--archive) (no -H,-A,-X)
        '--dry-run', 
        '--out-format="%t %f %''b"',
        '--progress', 
        '--stats',
        '--human-readable',
        '--del',
        '--no-whole-file',      # copy files whole (w/o delta-xfer algorithm)   
        '--inplace',            # rsync writes the updated data directly to the destination file.
        '--copy-links',
        '',
        '',
        ''
    ]

    rsync_crt_vdi = [
        'rsync', 
        '--recursive', '--links', '--perms','--times', '--group', '--owner', '--devices', '--specials',
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

    rsync_upd_vdi = [
        'rsync', 
        '--recursive', '--links', '--perms','--times', '--group', '--owner', '--devices', '--specials', 
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

    upload(rsync_test_mode_wo_vdi, source, list_sync_dirs, cur_uuid, logs_dir, True)
    upload(rsync_wo_vdi, source, list_sync_dirs, cur_uuid, logs_dir, False)

    upload_vdi(rsync_test_mode_crt_vdi, rsync_test_mode_upd_vdi, source, list_sync_dirs[len(list_sync_dirs) - 1], cur_uuid, destination, logs_dir, True)
    upload_vdi(rsync_crt_vdi, rsync_upd_vdi, source, list_sync_dirs[len(list_sync_dirs) - 1], cur_uuid, destination, logs_dir, False)


main()