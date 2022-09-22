import argparse
import glob
from src.mnt import Mount
from src.hdd_info import HddInfo
from src.upl import Upload
from src.log import Log


class BackupDriveD:

    def __init__(self) -> None:
        self.__uuid_src_drive = HddInfo.dell_3576_drive().get('uuid')

        # Output: '/cygdrive/d'
        self.__root_pth_src_drive = Mount.get_src_drive(self.__uuid_src_drive)

        # Output: root_pth_dest_drive: '/cygdrive/f', disk_data: {name: 'Hitachi', uuid: 'FI4353BNBUHD43' }
        self.__root_pth_dest_drive, self.__disk_data = Mount.get_recv_drive()

        self.__name_model_recv_drive = self.__disk_data.get('name')

        self.__full_path_dest_dir = self.__root_pth_dest_drive + '/dell_inspiron_3576'

        # Output: '/cygdrive/d/logs/drive_D'
        self.__path_logs_dir = Log.get_logs_dir('drive_D')

        self.__rsync_test_mode_upl = [
            'rsync',
            '--recursive',              # copy directories recursively
            '--perms',                  # preserve permissions
            '--times',                  # preserve modification time
            '--group',                  # preserve group
            '--owner',                  # preserve owner (super-user only)
            '--devices',                # preserve device files (super-user only)
            '--specials',               # preserve special files
            '--human-readable',         # output numbers in a human-readable format
            '--dry-run',                # perform a trial run with no changes made
            '--stats',                  # give some file-transfer stats
            '--progress',               # show progress during transfer
            '--del',                    # receiver deletes during xfer, not before
            '--verbose',                # increase verbosity
            '--copy-links',             # transform symlink into referent file/dir
            '--out-format="%t %f %''b"',
            '--exclude=cygwin64/',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '',                         # path to log file
            '',                         # source
            self.__full_path_dest_dir
        ]

        self.__rsync_base_mode_upl = [
            'rsync',
            '--recursive',
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
            '--copy-links',
            '--out-format="%t %f %''b"',
            '--exclude=cygwin64/',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '',
            '',
            self.__full_path_dest_dir
        ]

        self.__list_sync_dirs = [
            'backups',
            'documents',
            'installers',
            'media',
            'VirtualBox_VMs']

    @property
    def uuid_src_drive(self):
        return self.__uuid_src_drive

    @property
    def root_pth_src_drive(self):
        return self.__root_pth_src_drive

    @property
    def name_model_recv_drive(self):
        return self.__name_model_recv_drive

    @property
    def full_path_dest_dir(self):
        return self.__full_path_dest_dir

    @property
    def path_logs_dir(self):
        return self.__path_logs_dir

    @property
    def rsync_test_mode_upl(self):
        return self.__rsync_test_mode_upl

    @property
    def rsync_base_mode_upl(self):
        return self.__rsync_base_mode_upl

    @property
    def list_sync_dirs(self):
        return self.__list_sync_dirs

    def prepare_sync_data(self):
        list_full_path_sync_dirs = [self.__root_pth_src_drive + '/' + i for i in self.__list_sync_dirs]

        dict_rsync_test_md = {
            'command': self.rsync_test_mode_upl,
            'sync_dirs': self.list_sync_dirs,
            'list_full_path_sync_dirs': list_full_path_sync_dirs,
            'name_model_recv_drive': self.name_model_recv_drive,
            'path_logs_dir': self.path_logs_dir,
            'is_dry_run': True
        }

        dict_rsync_base_md = {
            'command': self.rsync_base_mode_upl,
            'sync_dirs': self.list_sync_dirs,
            'list_full_path_sync_dirs': list_full_path_sync_dirs,
            'name_model_recv_drive': self.name_model_recv_drive,
            'path_logs_dir': self.path_logs_dir,
            'is_dry_run': False
        }

        Upload.upload_files(dict_rsync_test_md)
        Upload.upload_files(dict_rsync_base_md)


def main():
    backup = BackupDriveD()
    backup.prepare_sync_data()

main()