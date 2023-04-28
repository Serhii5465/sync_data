import argparse
import sys
from typing import List
from src import mnt, upl, log
from src.hdd_info import HDDInfo


class BackupDriveD:
    """
    Class represents information for synchronization of partition on HDD Dell Inspiron
    with 3.5" external HDDs in Maiwo Enclosure.
    """
    def __init__(self) -> None:
        #: str: UUID partition of HDD-source
        self.__uuid_src_drive = HDDInfo().dell_3576_drive.get('uuid')

        #: str Path to the root of partition HDD-source: '/cygdrive/d'
        self.__root_pth_src_drive = mnt.get_src_drive(self.__uuid_src_drive)

        #: Tuple(str, str): UUID partition and path to the root of partition HDD-receiver:
        #: root_pth_dest_drive: '/cygdrive/f', disk_data: {name: 'Hitachi', uuid: 'FI4353BNBUHD43' }
        self.__root_pth_dest_drive, self.__disk_data = mnt.get_recv_drive()

        #: str: Name model of HDD-receiver
        self.__name_model_recv_drive = self.__disk_data.get('name')

        #: str: UUID of partition HDD-receiver
        self.__uuid_recv_drive = self.__disk_data.get('uuid')

        #: str: Full path to the root dir of sync on HDD-receiver
        self.__full_path_dest_dir = self.__root_pth_dest_drive + '/dell_inspiron_3576'

        #: str: Path to the log's dir: '/cygdrive/d/logs/drive_D'
        self.__path_logs_dir = log.get_logs_dir('drive_D')

        #: list(str): List of arguments of execution Rsync in dry-run mode
        self.__rsync_test_mode_upl = [
            'rsync',
            '--recursive',  # copy directories recursively
            '--perms',  # preserve permissions
            '--times',  # preserve modification time
            '--group',  # preserve group
            '--owner',  # preserve owner (super-user only)
            '--devices',  # preserve device files (super-user only)
            '--specials',  # preserve special files
            '--human-readable',  # output numbers in a human-readable format
            '--dry-run',  # perform a trial run with no changes made
            '--stats',  # give some file-transfer stats
            '--progress',  # show progress during transfer
            '--del',  # receiver deletes during xfer, not before
            '--verbose',  # increase verbosity
            '--copy-links',  # transform symlink into referent file/dir
            '--out-format="%t %f %''b"',
            '--exclude=Hyper-V',
            '--exclude=cygwin64/',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '--exclude=dell_inspiron_3576/',
            '',  # path to log file
            '',  # source
            self.__full_path_dest_dir
        ]

        #: list(str): List of arguments of execution Rsync in base mode
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
            '--exclude=Hyper-V',
            '--exclude=cygwin64/',
            '--exclude=games/',
            '--exclude=Snapshots/',
            '--exclude=Logs/',
            '--exclude=dell_inspiron_3576/',
            '',
            '',
            self.__full_path_dest_dir
        ]

        #: list(str): The list of synchronizable folders.
        self.__list_sync_dirs = [
            'backups',
            'documents',
            'installers',
            'media',
            'virtual_machines',
            'hyper_v_export_vm'
        ]

    @property
    def uuid_src_drive(self) -> str:
        return self.__uuid_src_drive

    @property
    def root_pth_src_drive(self) -> str:
        return self.__root_pth_src_drive

    @property
    def name_model_recv_drive(self) -> str:
        return self.__name_model_recv_drive

    @property
    def uuid_recv_drive(self):
        return self.__uuid_recv_drive

    @property
    def full_path_dest_dir(self) -> str:
        return self.__full_path_dest_dir

    @property
    def path_logs_dir(self) -> str:
        return self.__path_logs_dir

    @property
    def rsync_test_mode_upl(self) -> List[str]:
        return self.__rsync_test_mode_upl

    @property
    def rsync_base_mode_upl(self) -> List[str]:
        return self.__rsync_base_mode_upl

    @property
    def list_sync_dirs(self) -> List[str]:
        return self.__list_sync_dirs

    def prepare_sync_data(self) -> None:
        """
        Prepares data for synchronization.
        """

        parser = argparse.ArgumentParser(description='Synchronization files between local storage and external USB HDD')
        parser.add_argument('-a', '--all', action='store_true', help='Copies all files, which are located in drive D')
        parser.add_argument('-n', '--no_vm', action='store_true', help='Copies all files, ignore directories which are using to store Virtualbox and Hyper-V virtual machines')

        args = vars(parser.parse_args())

        if not args['all'] and not args['no_vm']:
            parser.parse_args(['-h'])

        #: Creates list of full paths to folders for sync.
        list_full_path_sync_dirs = []

        if self.uuid_recv_drive == HDDInfo().jmicron_drive.get('uuid') and args['all']:
            print('\nThe directory \'VirtualBox_VMs\' cannot be copied to the \'Jmicron\' drive \ndue to his insufficient capacity.' 
                  'Run the script for this drive with the \'-n\' parameter.')
            sys.exit()

        if args['no_vm']:
            list_full_path_sync_dirs = [self.root_pth_src_drive + '/'
                                         + self.list_sync_dirs[i] for i in range(0, len(self.list_sync_dirs) - 2)]
        elif args['all']:
            list_full_path_sync_dirs = [self.root_pth_src_drive + '/' + i for i in self.list_sync_dirs]

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

        upl.upload_files(dict_rsync_test_md)
        upl.upload_files(dict_rsync_base_md)


def main():
    backup = BackupDriveD()
    backup.prepare_sync_data()


main()
