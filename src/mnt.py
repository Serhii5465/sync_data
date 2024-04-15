import sys
from typing import Union
from cyg_mnt_point import mnt 
from src import constants

def get_mnt_point_src() -> Union[dict, None]:
    """
    Get the mount point of the source drive based on its UUID.

    This function iterates through a list of source drive UUIDs and retrieves their corresponding mount points.
    If a mount point is found for a UUID, the function returns a dictionary containing the UUID and its mount point.
    Otherwise, the function stops the program with an error message.

    Returns:
        dict: A dictionary containing the UUID and its mount point if found.

    Raises:
        SystemExit
    """
    uuid_src = [
        constants.DELL_INSPIRON_3576_SRC_DRIVE(),
        constants.MSI_GF63_SRC_DRIVE()
    ]

    mnt_point = ''
    
    for i in uuid_src:
        mnt_point = mnt.get_cygwin_mount_point(i.get('uuid'))
        if mnt_point is not None:
            i['mnt_point'] = mnt_point
            return i
    
    if mnt_point is None:
        sys.exit('Source HDD did not mount')

def get_mnt_point_dest() -> Union[dict, None]:
    uuid_dest = [
        constants.EXT_DRIVE_1(),
        constants.EXT_DRIVE_2(),
        constants.EXT_DRIVE_3()
    ]

    mnt_point = ''

    for i in uuid_dest:
        mnt_point = mnt.get_cygwin_mount_point(i.get('uuid'))
        if mnt_point is not None:
            i['mnt_point'] = mnt_point
            return i
        
    if mnt_point is None:
        sys.exit('Receiver HDD did not mount')    