from typing import Dict

#: Wester Digital 1Tb (Maiwo External Enclosure)
def EXT_DRIVE_1() -> Dict[str, str]:
    return {
        'uuid': '94B42285B4226A46',
        'name': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
def EXT_DRIVE_2() -> Dict[str, str]:
    return {
        'uuid': '56384C06384BE419',
        'name': 'Hitachi (Maiwo)'
    }

#: 2.5″ Wester Digital Mobile 320Gb (Gembird enclosure)
def EXT_DRIVE_3() -> Dict[str, str]:
    return {
        'uuid': '845A6F615A6F4ECC',
        'name': 'Wester Digital (Gembird)'
    }

# #: Samsung SSD 500Gb (MSI GF63)
# def MSI_GF63_SRC_DRIVE_1() -> Dict[str, str]:
#     return {
#         'uuid': '01DA36B803C75B50',
#         'sync_dirs': ['configs' , 'documents', 'media']
#     }

# #: Kingston SSD 500Gb (MSI GF63)
# def MSI_GF63_SRC_DRIVE_2() -> Dict[str, str]:
#     return {
#         'uuid': '8E76883376881DD9',
#         'sync_dirs': ['backups' , 'installers', 'vm']
#     }

def MSI_GF63_SRC_DRIVE() -> Dict[str, str]:
    return {
        'uuid': '347E0E947E0E4F54',
        'sync_dirs': ['configs' , 'documents', 'media', 'backups', 'installers', 'vm']
    }