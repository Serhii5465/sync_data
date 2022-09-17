import os
import sys
from src.data.rclone_conf import RcloneConf
from src.bash_process import BashProcess
from src.date import Date
from src.log import Log

class BackupDocuments:

    def __init__(self) -> None:
        self.__rclone = RcloneConf()
        self.check_files(self.__rclone.conf, self.__rclone.sync_dir, self.__rclone.prog_dir)
        self.__logs_dir = Log.get_logs_dir('rclone', add_subfolder=False)

    @property
    def rclone(self):
        return self.__rclone

    @property
    def logs_dir(self):
        return self.__logs_dir

    def check_files(self, *list_files):
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
        win_style_path_sync_dir = BashProcess.get_cmd_output(['cygpath', '--windows', self.__rclone.sync_dir])
        win_style_path_logs_dir = BashProcess.get_cmd_output(['cygpath', '--windows', self.logs_dir])

        date_now = Date.get_time_now()

        # Process syncing folder with Gdrive
        out = BashProcess.run_cmd([self.__rclone.prog_dir + '/rclone.exe',
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