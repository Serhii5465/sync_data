import os
import sys
from pathlib import Path
from typing import List
from src import bash_process, date, log


class BackupDocuments:
    """
    The class is responsible for synchronizing the local folder with Google Drive using the Rclone utility.
    """
    def __init__(self) -> None:
        """
        Initializes the value of the path variables and verifies their authenticity.
        """

        #: str: Path to Rclone's config
        self.__rclone_conf = str(Path.home()) + '/.config/rclone/rclone.conf'

        #: str: The root dir, where located exe file Rclone
        self.__rclone_prog_dir = '/cygdrive/c/portable/rclone'

        #: The root of the folder to be synchronized
        self.__sync_dir = '/cygdrive/d/documents'

        self.check_files(self.__rclone_prog_dir, self.__rclone_conf, self.__sync_dir)

        #: Path to logs dir.
        self.__logs_dir = log.get_logs_dir('rclone', add_subfolder=False)

    @property
    def logs_dir(self) -> str:
        return self.__logs_dir

    @property
    def sync_dir(self):
        return self.__sync_dir

    def check_files(self, *list_files: List[str]) -> None:
        """
        Verifies if the path to a folder or file is valid. If at least one path is broken,
        the script terminates.
        Args:
            *list_files: List of full paths to folders and files.
        """
        for i in list_files:
            if not os.path.exists(i):
                msg = i + " doesn't exists"
                sys.exit(msg)

    def upload_to_gdrive(self) -> None:
        """
        Uploads files from local folder to Google Drive.
        Under normal conditions the process finishes work and has an exit code of 0.
        Otherwise, the process has an exit code different from 0 and the script terminates.
        """
        #: Converting Unix-like path to Windows form by using Cygpath.exe utility.
        win_style_path_sync_dir = bash_process.get_cmd_output(['cygpath', '--windows', self.sync_dir])
        win_style_path_logs_dir = bash_process.get_cmd_output(['cygpath', '--windows', self.logs_dir])

        date_now = date.get_time_now()

        out = bash_process.run_cmd([self.__rclone_prog_dir + '/rclone.exe',
                                    'sync',
                                    '--progress',
                                    '--verbose',
                                    win_style_path_sync_dir.stdout.strip('\n'),
                                    'google-drive:',
                                    '--log-file=' + win_style_path_logs_dir.stdout.strip(
                                        '\n') + '/' + date_now + '.log'])

        if out.returncode != 0:
            sys.exit('Error\nCheck logs')
        else:
            print('\nGood')


def main():
    doc = BackupDocuments()
    doc.upload_to_gdrive()


main()
