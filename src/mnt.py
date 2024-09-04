import sys
import wmi
import subprocess
from typing import List, Dict
from src import constants

def conv_path_win_to_unix(windows_path: str) -> str:
    s = subprocess.run(['cygpath', '--unix', windows_path], capture_output=True, text=True)
    return s.stdout.strip('\n')

def get_mnt_point(list_uuids: List[str]) -> Dict[str, any]:
    try:
        c = wmi.WMI()
        
        for i in c.Win32_LogicalDisk():
            for j in list_uuids:
                if i.VolumeSerialNumber and i.VolumeSerialNumber.strip() == j.get('uuid'):
                    j['mnt_point'] = conv_path_win_to_unix(i.DeviceID)
                    return j
        
        sys.exit("UUID not found")

    except Exception as e:
        sys.exit(f'An error occurred: {e}')

def get_src_drive() -> Dict[str, any]:
    uuid_src = [
        constants.DELL_INSPIRON_3576_SRC_DRIVE,
        constants.MSI_GF63_SRC_DRIVE
    ]

    return get_mnt_point(uuid_src)

def get_mnt_point_dest() -> Dict[str, any]:
    uuid_dest = [
        constants.EXT_DRIVE_1,
        constants.EXT_DRIVE_2,
        constants.EXT_DRIVE_3
    ]

    return get_mnt_point(uuid_dest)