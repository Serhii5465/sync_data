import glob
import os
from src.mnt import Mount
from src.hdd_info import HddInfo
from src.log import Log
from src.upl import Upload

class BackupJmicron:

    def __init__(self) -> None:
        self.__src_drive = Mount.get_src_drive(HddInfo.jmicron_drive().get('uuid'))

        self.__recv_drive, self.__disk_data = Mount.get_recv_drive()
        self.__name_model_recv_drive = self.__disk_data.get('name')
        self.__path_destination = self.__recv_drive + '/jmicron'

        self.__logs_dir = Log.get_logs_dir('jmicron')

        self.__rsync_upl_test_mode = [
            'rsync',
            '--recursive',          # copy directories recursively
            '--perms',              # preserve permissions
            '--times',              # preserve modification time
            '--group',              # preserve group
            '--owner',              # preserve owner (super-user only)
            '--devices',            # preserve device files (super-user only)
            '--specials',           # preserve special files
            '--human-readable',     # output numbers in a human-readable format
            '--dry-run',            # perform a trial run with no changes made
            '--stats',              # give some file-transfer stats
            '--progress',           # show progress during transfer
            '--del',                # receiver deletes during xfer, not before
            '--verbose',            # increase verbosity
            '--out-format="%t %f %''b"',
            '',
            '',
            self.__path_destination
        ]

        self.__rsync_upl = [
            'rsync',
            '--recursive',
            '--links',
            '--perms',
            '--times',
            '--group',
            '--owner',
            '--devices',
            '--specials',
            '--human-readable',
            '--stats',
            '--progress',
            '--del',
            '--verbose',
            '--out-format="%t %f %''b"',
            '',
            '',
            self.__path_destination
        ]

    @property
    def src_drive(self):
        return self.__src_drive

    @property
    def logs_dir(self):
        return self.__logs_dir

    @property
    def name_model_recv_drive(self):
        return self.__name_model_recv_drive

    @property
    def path_destination(self):
        return self.__path_destination

    @property
    def rsync_upl_test_mode(self):
        return self.__rsync_upl_test_mode

    @property
    def rsync_upl(self):
        return self.__rsync_upl

def main():
    jmicron = BackupJmicron()

    list_full_path_sync_dirs = glob.glob(jmicron.src_drive + '/*')
    list_sync_dirs = [os.path.basename(i) for i in list_full_path_sync_dirs]

    print(list_sync_dirs)

    test_mode_rsync_upl = {
        'command': jmicron.rsync_upl_test_mode,
        'sync_dirs': list_sync_dirs,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'name_model_recv_drive': jmicron.name_model_recv_drive,
        'path_logs_dir': jmicron.logs_dir,
        'is_dry_run': True
    }

    base_mode_rsync_upl = {
        'command': jmicron.rsync_upl,
        'sync_dirs': list_sync_dirs,
        'list_full_path_sync_dirs': list_full_path_sync_dirs,
        'name_model_recv_drive': jmicron.name_model_recv_drive,
        'path_logs_dir': jmicron.logs_dir,
        'is_dry_run': False
    }

    Upload.upload_files(test_mode_rsync_upl)
    Upload.upload_files(base_mode_rsync_upl)


main()