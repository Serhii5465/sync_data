import src.bash_proc as bash_proc
import sys

# get unix-like mount point partition disk by his uuid
def get_mount_point(uuid):

    # output CompletedProcess(args=['blkid', '--uuid', 'A0AACF26AACEF7B41'], returncode=2, stdout='', stderr='')
    name_block_dev = bash_proc.get_cmd_output(['blkid', '--uuid', uuid]) #stdout example: /dev/sda1\n

    if(name_block_dev.returncode != 0):
        return None
    else:
        # param: /dev/sda1
        # output: sda1
        name_file_blk_dev = name_block_dev.stdout.strip('\n').split('/dev/')[1] 

        # output: CompletedProcess(args=['grep', '/proc/partitions', '-e', 'sda2'], returncode=0, stdout='    8     2 976744448 sda2   D:\\\n', stderr='')
        info_partition = bash_proc.get_cmd_output(['grep', '/proc/partitions', '-e', name_file_blk_dev])

        #['', '', '', '', '8', '', '', '', '', '2', '976744448', 'sda2', '', '', 'D:\\\n']
        list_str = info_partition.stdout.split(' ')

        # output: D:
        win_mnt_point = list_str[len(list_str) - 1].strip('/\/\n')
 
        # output: CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
        unix_mnt_point = bash_proc.get_cmd_output(['cygpath', '--unix', win_mnt_point])

        # example return: /cygdrive/d/
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
    uuid_recv_drive_1 = '1078010A7800EFF0'  # Wester Digital 1Tb
    uuid_recv_drive_2 = '0280B4A880B4A397'  # Hitahci 500Gb

    curnt_uuid = ''
    recv = get_mount_point(uuid_recv_drive_1)

    if(recv is None):
        recv = get_mount_point(uuid_recv_drive_2)
        if(recv is None):
            sys.exit('Receiver-disk is not mounted')
        else:
            return recv, 'Hitachi'
    else:
        return recv, 'Wester Digital'    