import os
import sys
from pathlib import Path
from src import bash_process,date,log


class BackupDocuments:

    def __init__(self) -> None:
        self.__rclone_conf = str(Path.home()) + '/.config/rclone/rclone.conf'
        self.__rclone_prog_dir = '/cygdrive/c/portable/rclone'
        self.__sync_dir = '/cygdrive/d/documents'

        self.check_files(self.__rclone_prog_dir, self.__rclone_conf, self.__sync_dir)
        self.__logs_dir = log.get_logs_dir('rclone', add_subfolder=False)

    @property
    def logs_dir(self):
        return self.__logs_dir

    @staticmethod
    def check_files(*list_files):
        """
        This function checks if list full.
        Otherwise, if at least one of the elements in the array missing,
        the script terminates
        :param list_files: array of verifiable files
        """
        for item in list_files:
            if not os.path.exists(item):
                msg = item + " doesn't exists"
                sys.exit(msg)

    def upload_to_gdrive(self):
        """
        Uploads files from local folder to Google Drive.
        Under normal conditions the process finishes work and has an exit code of 0.
        Otherwise the process has an exit code different from 0 and the script finishes terminates
        :param rclone_dir: full path to Rclone utility
        :param sync_dir: synchronized folder
        :param logs_dir: directory log file
        """

        """
        Converting Unix-like path to Windows form by using Cygpath.exe utility.
        Convertion runs in separate process.
        """
        win_style_path_sync_dir = bash_process.get_cmd_output(['cygpath', '--windows', self.__sync_dir])
        win_style_path_logs_dir = bash_process.get_cmd_output(['cygpath', '--windows', self.logs_dir])

        date_now = date.get_time_now()

        # Process syncing folder with Gdrive
        out = bash_process.run_cmd([self.__rclone_prog_dir + '/rclone.exe',
                                 'sync',
                                 '--progress',
                                 '--verbose',
                                 win_style_path_sync_dir.stdout.strip('\n'),
                                 'google-drive:',
                                 '--log-file=' + win_style_path_logs_dir.stdout.strip('\n') + '/' + date_now + '.log'])

        if out.returncode != 0:
            sys.exit('Error\nCheck logs')
        else:
            print('\nGood')

def main():
    doc = BackupDocuments()
    doc.upload_to_gdrive()

main()