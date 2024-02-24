from typing import Dict

#: Wester Digital 1Tb (Maiwo External Enclosure)
def WD_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '44A6D12EA6D1216A',
        'name': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
def HITACHI_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '6624859F248572BB',
        'name': 'Hitachi (Maiwo)'
    }

#: 2.5″ Seagate Mobile 1Tb (Gembird enclosure)
def SEAGATE_DRIVE() -> Dict[str, str]:
    return {
        'uuid': 'A644C20F44C1E1E3',
        'name': 'Seagate Mobile (Gembird)'
    }

#: Samsung SSD 500Gb (MSI GF63)
def MSI_GF63_SRC_DRIVE_1() -> Dict[str, str]:
    return {
        'uuid': '01DA36B803C75B50',
        'sync_dirs': ['configs' , 'documents', 'media']
    }

#: Kingston SSD 500Gb (MSI GF63)
def MSI_GF63_SRC_DRIVE_2() -> Dict[str, str]:
    return {
        'uuid': '8E76883376881DD9',
        'sync_dirs': ['backups' , 'installers', 'vm']
    }