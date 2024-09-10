FILE_RSYNC_EXCLUSION = 'exclude.txt'

#: Wester Digital 1Tb (Maiwo External Enclosure)
EXT_DRIVE_1 = {
        'uuid': 'E8C8FEE8',
        'label': 'Wester Digital (Maiwo)'
    }

#: Hitachi 500Gb (Maiwo External Enclosure)
EXT_DRIVE_2 = {
        'uuid': '049B6C01',
        'label': 'Hitachi (Maiwo)'
    }

#: 2.5″ Wester Digital Mobile 320Gb (Gembird enclosure)
EXT_DRIVE_3 = {
        'uuid': '5A6F4ECC',
        'label': 'Wester Digital (Gembird)'
    }

MSI_GF63_SRC_DRIVE = {
        'uuid': '7E0E4F54',
        'sync_dirs': ['shared_files', 'local', 'gdrive_share', 'media', 'backups', 'installers', 'vm'],
        'log_name' : 'backup_msi_gf63',
        'name_dest_dir' : 'msi_gf63_files'
    }

DELL_INSPIRON_3576_SRC_DRIVE = { 
        'uuid': '5837B806',
        'sync_dirs': ['local' , 'backups', 'gdrive_share'],
        'log_name' : 'backup_dell_inspiron_3576',
        'name_dest_dir' : 'dell_inspiron_3576_files'
    }