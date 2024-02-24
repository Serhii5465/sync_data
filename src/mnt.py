import sys
from typing import Union, Tuple
from py_exec_cmd import exec_cmd
from src import constants


def get_recv_drive() -> Tuple[str, str]:
    """
    Iterates a list with the UUIDs of the receiver disks
    and checks if any of them are mounted.
    Returns:
        If none of the disks are mounted, the script terminates. Otherwise, 
        a tuple with the UUID partition and its path in Cygwin format will be created.
    """

    uuids = [
        constants.HITACHI_DRIVE(),
        constants.SEAGATE_DRIVE(),
        constants.WD_DRIVE()
    ]

    for i in uuids:
        recv = get_mount_point(i.get('uuid'))
        if recv is not None:
            return recv, i

    if recv is None:
        sys.exit('Receiver-disk is not mounted')


def get_mount_point(uuid_drive: str) -> Union[None, str]:
    """
    Converts UUID partition to Cygwin format path's mount point.
    If partition not mounted, script will be stops his work.
    Args:
        uuid_drive: Universal Unique Identifier of partition.

    Returns:
        If HDD not mounted, returns None. Otherwise, path to the partition of HDD receiver.
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


def get_src_drive(uuid_drive: str) -> str:
    """
    Checks if source-HDD mounted.
    Args:
        uuid_drive: Universal Unique Identifier partition of HDD-transmitter.

    Returns:
    If the hard drive is not mounted, the script terminates. Otherwise, the path to the disk in Cygwin format.
    """
    source = get_mount_point(uuid_drive)
    if source is None:
        sys.exit('Source-disk is not mounted')
    else:
        return source
