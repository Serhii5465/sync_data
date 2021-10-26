from call_bash_func import get_cmd_output
import sys


# get unix-like mount point partition disk by his uuid
def get_mount_point(uuid):
    # output CompletedProcess(args=['blkid', '--uuid', 'A0AACF26AACEF7B41'], returncode=2, stdout='', stderr='')
    name_block_dev = get_cmd_output(['blkid', '--uuid', uuid]) #stdout example: /dev/sda1\n
    
    if(name_block_dev.returncode != 0):
        return None
    else:
        # output: CompletedProcess(args=['cygpath', '--windows', '/dev/sda2'], returncode=0, stdout='\\\\.\\D:\n', stderr='')
        win_mnt_point = get_cmd_output(['cygpath', '--windows', name_block_dev.stdout.strip('\n')])

        # output CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
        unix_mnt_point = get_cmd_output(['cygpath', '--unix', win_mnt_point.stdout.strip('\n')[4:]])

        # example return: /cygdrive/d 
        return unix_mnt_point.stdout.strip('\n') 


# get path mount point of drive-source
def get_src_drive(uuid):
    source = get_mount_point(uuid)

    if(source is None):
        sys.exit('Source-disk is not mounted')
    else:
        return source


# check if one of disk-receiver mounted and get his path of mount point  
def get_recv_drive():
    #uuid_recv_drive_1 = '01D7B5F7EF7D6100'  # Wester Digistal 1Tb
    #uuid_recv_drive_2 = '01D7B5E18B1C3670'  # Hitahci 500Gb

    uuid_recv_drive_1 = 'CC6A7CA06A7C894A1'  
    uuid_recv_drive_2 = 'CC6A7CA06A7C894A1'  

    curnt_uuid = ''
    recv = get_mount_point(uuid_recv_drive_1)

    if(recv is None):
        recv = get_mount_point(uuid_recv_drive_2)
        if(recv is None):
            sys.exit('Receiver-disk is not mounted')
        else:
            return recv, uuid_recv_drive_2
    else:
        return recv, uuid_recv_drive_1    