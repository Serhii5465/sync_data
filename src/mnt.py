import sys
from typing import Union, Tuple
from py_exec_cmd import exec_cmd
from src import constants

def get_cygwin_mount_point(uuid_drive: str) -> Union[None, str]:
    """
    Converts UUID partition to Cygwin format path's mount point.
    If disk not mounted, script will be stops his work.
    Args:
        uuid_drive: Universal Unique Identifier of partition.

    Returns:
        If HDD not mounted, returns None. Otherwise, path to the HDD partition.
    """

    name_block_dev = exec_cmd.get_cmd_out(['blkid', '--uuid', uuid_drive])  # stdout example: /dev/sda1\n

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
        info_partition = exec_cmd.get_cmd_out(['grep', '/proc/partitions', '-e', name_file_blk_dev])

        # Output: ['', '', '', '', '8', '', '', '', '', '2', '976744448', 'sda2', '', '', 'D:\\\n']
        list_str = info_partition.stdout.split(' ')

        # Output: D:
        win_mnt_point = list_str[len(list_str) - 1].strip('/\/\n')

        # output: CompletedProcess(args=['cygpath', '--unix', 'D:'], returncode=0, stdout='/cygdrive/d\n', stderr='')
        unix_mnt_point = exec_cmd.get_bety_cmd_out(['cygpath', '--unix', win_mnt_point])

        # example return: /cygdrive/d/
        return unix_mnt_point

def get_mnt_point_src():
    uuid_src = [
        constants.DELL_INSPIRON_3576_SRC_DRIVE(),
        constants.MSI_GF63_SRC_DRIVE()
    ]

    mnt_point = ''
    
    for i in uuid_src:
        mnt_point = get_cygwin_mount_point(i.get('uuid'))
        if mnt_point is not None:
            i['mnt_point'] = mnt_point
            return i
    
    if mnt_point is None:
        sys.exit('Source HDD did not mount')

def get_mnt_point_dest():
    uuid_dest = [
        constants.EXT_DRIVE_1(),
        constants.EXT_DRIVE_2(),
        constants.EXT_DRIVE_3()
    ]

    mnt_point = ''

    for i in uuid_dest:
        mnt_point = get_cygwin_mount_point(i.get('uuid'))
        if mnt_point is not None:
            i['mnt_point'] = mnt_point
            return i
        
    if mnt_point is None:
        sys.exit('Receiver HDD did not mount')    