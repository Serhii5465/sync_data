import sys, uu, re
from src import bash_proc, hdd_info

def get_mount_point(uuid_drive):
    """
    Converts UUID partition to UNIX-format path's mount point.
    If partition not mounted, script will be stops his work.
    :param uuid_drive: universally unique identifier partition of HDD
    :return: Unix-like format path to the mount point of specific partition
    """

    name_block_dev = bash_proc.get_cmd_output(['blkid', '--uuid', uuid_drive]) #stdout example: /dev/sda1\n

    """
    Checking if partition is mounted
    Output: CompletedProcess(args=['blkid', '--uuid', 'A0AACF26AACEF7B41'], returncode=2, stdout='', stderr='')
    """
    if name_block_dev.returncode != 0:
        return None
    else:
        # param: /dev/sda1
        # output: sda1
        name_file_blk_dev = name_block_dev.stdout.strip('\n').split('/dev/')[1] 

        """
        Finding by using utility Grep the mount point in Windows
        Output: CompletedProcess(args=['grep', '/proc/partitions', '-e', 'sda2'], returncode=0, stdout='    8     2 976744448 sda2   D:\\\n', stderr='')
        """
        info_partition = bash_proc.get_cmd_output(['grep', '/proc/partitions', '-e', name_file_blk_dev])

        #Output: ['', '', '', '', '8', '', '', '', '', '2', '976744448', 'sda2', '', '', 'D:\\\n']
        list_str = info_partition.stdout.split(' ')

        # Output: D:
        win_mnt_point = list_str[len(list_str) - 1].strip('/\/\n')
 
        # output: CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
        unix_mnt_point = bash_proc.get_cmd_output(['cygpath', '--unix', win_mnt_point])

        # example return: /cygdrive/d/
        return unix_mnt_point.stdout.strip('\n') 



def get_src_drive(uuid_drive):
    """
    Checks if source-HDD mounted
    :param uuid_drive: universally unique identifier of the source-partition drive
    :return: if false, script terminates.
    Otherwise, return full path to mount point of source-partition drive
    """
    source = get_mount_point(uuid_drive)
    if source is None:
        sys.exit('Source-disk is not mounted')
    else:
        return source


def get_recv_drive():
    """
    Function checks if mounted one of HDD-receivers and returns
    path of mount point of the partition-receiver and info about HDD (name and UUID).
    Otherwise, if no one of HDD-receivers not mounted,
    script will be finishes.
    :return: 1: path to the mount point; 2: information about disk
    """
    
    uuids = [
        hdd_info.wd_drive,
        hdd_info.hitachi_drive,
        hdd_info.jmicron_drive
    ]

    for i in uuids:
        recv = get_mount_point(i.get('uuid'))
        if recv is not None:
            return recv, i        
        
    if recv is None:
        sys.exit('Receiver-disk is not mounted')