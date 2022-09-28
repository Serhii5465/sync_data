import glob
import os
from typing import List

from src import mnt, log, upl
from src.hdd_info import HDDInfo


class BackupJmicron:
    """
    Class represents information for synchronization 2.5" external HDD Western Digital
    with 3.5" external HDDs in Maiwo Enclosure.
    """

    def __init__(self) -> None:
        #: str: UUID partition of source-HDD
        self.__src_drive = mnt.get_src_drive(HDDInfo().jmicron_drive.get('uuid'))

        #: Tuple: UUID partition and path to the root of partition HDD-receiver
        self.__recv_drive, self.__disk_data = mnt.get_recv_drive()

        #: str: Name model HDD-receiver
        self.__name_model_recv_drive = self.__disk_data.get('name')

        #: str: Full path to the root dir of sync on HDD-receiver
        self.__path_destination = self.__recv_drive + '/jmicron'

        #: Path to the log dir
        self.__logs_dir = log.get_logs_dir('jmicron')

        #: list(str): List of arguments of execution Rsync in dry-run mode
        self.__rsync_upl_test_mode = [
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
            '--out-format="%t %f %''b"',
            '',
            '',
            self.__path_destination
        ]

        #: list(str): List of arguments of execution Rsync in base mode
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
    def src_drive(self) -> str:
        return self.__src_drive

    @property
    def logs_dir(self) -> str:
        return self.__logs_dir

    @property
    def name_model_recv_drive(self) -> str:
        return self.__name_model_recv_drive

    @property
    def path_destination(self) -> str:
        return self.__path_destination

    @property
    def rsync_upl_test_mode(self) -> List[str]:
        return self.__rsync_upl_test_mode

    @property
    def rsync_upl(self) -> List[str]:
        return self.__rsync_upl

    def prep_tranf(self) -> None:
        """
        Prepares data for synchronization.
        """

        #: Finds paths all dirs, which located in the root of partition.
        list_full_path_sync_dirs = glob.glob(self.src_drive + '/*')

        #: Retrieved names dirs from paths.
        list_sync_dirs = [os.path.basename(i) for i in list_full_path_sync_dirs]

        test_mode_rsync_upl = {
            'command': self.rsync_upl_test_mode,
            'sync_dirs': list_sync_dirs,
            'list_full_path_sync_dirs': list_full_path_sync_dirs,
            'name_model_recv_drive': self.name_model_recv_drive,
            'path_logs_dir': self.logs_dir,
            'is_dry_run': True
        }

        base_mode_rsync_upl = {
            'command': self.rsync_upl,
            'sync_dirs': list_sync_dirs,
            'list_full_path_sync_dirs': list_full_path_sync_dirs,
            'name_model_recv_drive': self.name_model_recv_drive,
            'path_logs_dir': self.logs_dir,
            'is_dry_run': False
        }

        upl.upload_files(test_mode_rsync_upl)
        upl.upload_files(base_mode_rsync_upl)


def main():
    jmicron = BackupJmicron()
    jmicron.prep_tranf()


main()
