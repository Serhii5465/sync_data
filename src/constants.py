from typing import Dict

#: Wester Digital 1Tb (Maiwo External Enclosure)
def EXT_DRIVE_1() -> Dict[str, str]:
    return {
        'uuid': '94B42285B4226A46',
        'label': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
def EXT_DRIVE_2() -> Dict[str, str]:
    return {
        'uuid': '56384C06384BE419',
        'label': 'Hitachi (Maiwo)'
    }

#: 2.5″ Wester Digital Mobile 320Gb (Gembird enclosure)
def EXT_DRIVE_3() -> Dict[str, str]:
    return {
        'uuid': '845A6F615A6F4ECC',
        'label': 'Wester Digital (Gembird)'
    }

#: Test
# def EXT_DRIVE_3() -> Dict[str, str]:
#     return {
#         'uuid': 'BA6AE7766AE72DB7',
#         'label': 'Wester Digital (Gembird)'
#     }

def MSI_GF63_SRC_DRIVE() -> Dict[str, any]:
    return {
        'uuid': '347E0E947E0E4F54',
        'sync_dirs': ['shared', 'local' , 'gdrive_share', 'media', 'backups', 'installers', 'vm'],
        'log_name' : 'backup_msi_gf63',
        'name_dest_dir' : 'msi_gf63_files'
    }

def DELL_INSPIRON_3576_SRC_DRIVE() -> Dict[str, any]:
    return {
        'uuid': '345837F85837B806',
        'sync_dirs': ['local' , 'backups', 'gdrive_share'],
        'log_name' : 'backup_dell_inspiron_3576',
        'name_dest_dir' : 'dell_inspiron_3576_files'
    }