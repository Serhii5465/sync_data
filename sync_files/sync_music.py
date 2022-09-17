import os
import sys
import logging
from src.data.hdd_info import HddInfo
from src.bash_process import BashProcess
from src.data.adb_paths import AdbPaths
from src.date import Date
from src.log import Log


class SyncMusic:

    def __init__(self):
        self.__bash_proc = BashProcess()
        self.get_stat_dev()
        self.__hdd_info = HddInfo()
        self.__adb_paths = AdbPaths()
        self.__logger = self.get_logger()

    @property
    def hdd_info(self):
        return self.__hdd_info

    @property
    def bash_proc(self):
        return self.__bash_proc

    @property
    def adb_paths(self):
        return self.__adb_paths

    @property
    def logger(self):
        return self.__logger

    def get_stat_dev(self):
        """
        Verifying connection of USB device by his serial number.
        """
        serial_no = '293290c6'
        cmd_state = ['adb', 'devices']
        out = self.__bash_proc.get_form_out_cmd(cmd_state)

        if out.find(serial_no) == -1:
            sys.exit('Device not connected')

    def is_exist_rem_dir(self):
        # if directory is exist, command will be returned 0, otherwise 1
        cmd_is_exist_dir = ['adb', 'shell', '[ -d ' + self.adb_paths.root_dest_dir
                            + self.adb_paths.sync_dir + ' ] && echo 0 || echo 1']
        # if directory is empty, command will be returned 1, otherwise 0
        cmd_is_empty_dir = ['adb', 'shell',
                            'find ' + self.adb_paths.root_dest_dir + self.adb_paths.sync_dir +
                            ' -mindepth 1 -maxdepth 1 | '
                            'read && echo 0 || echo 1']  # 0 - not empty, 1 - empty

        is_exist = BashProcess.get_form_out_cmd(cmd_is_exist_dir)
        is_empty = BashProcess.get_form_out_cmd(cmd_is_empty_dir)

        return is_exist, is_empty

    def prep_transf(self, is_exist, is_empty):

        cmd_adb_push = ['adb', 'push', '', '']

        list_loc_files = self.get_loc_files()

        if is_exist == '1' and is_empty == '1':
            # adb push
            print('Music folder not exist')
            cmd_adb_mkdir = ['adb', 'shell', 'mkdir', self.adb_paths.root_dest_dir + self.adb_paths.sync_dir]
            BashProcess.run_cmd(cmd_adb_mkdir)
            self.upload(cmd_adb_push, list_loc_files)

        if is_exist == '0' and is_empty == '1':
            # adb push
            print('Music folder exist,but empty')
            self.upload(cmd_adb_push, list_loc_files)

        if is_exist == '0' and is_empty == '0':
            # adb push --sync
            print('Music folder exist and not empty')
            list_rem_files = self.get_rem_files()

            list_del_files = ['"' + self.adb_paths.root_dest_dir + i +
                              '"' for i in list(set(list_rem_files) -
                                                set(list_loc_files))]

            list_upl_files = list(set(list_loc_files) - set(list_rem_files))

            self.delete_remt_files(list_del_files)
            self.upload(cmd_adb_push, list_upl_files)

    def delete_remt_files(self, files):
        if len(files) != 0:
            cmd_del_file = ['adb', 'shell', 'rm', '']
            msg = 'Removing files...'
            print(msg)
            self.logger.info(msg)
            for i in files:
                print(i)
                self.__logger.info('Deletable file: ' + i)
                cmd_del_file[len(cmd_del_file) - 1] = i
                out = BashProcess.get_cmd_output(cmd_del_file)
                if out.returncode != 0:
                    print(out.stderr)
                    self.__logger.error(out.stderr)

            # Utility 'find' removing empty folders
            cmd_del_empt_dir = ['adb', 'shell',
                                'find ' + self.adb_paths.root_dest_dir
                                + self.adb_paths.sync_dir + ' -type d -delete']

            str_empty_dirs = BashProcess.get_form_out_cmd(cmd_del_empt_dir)
            if str_empty_dirs != '':
                print('Removing empty directories')
                list_empty_dirs = str_empty_dirs.split('\n')
                for i in list_empty_dirs:
                    print(i)
                    self.__logger.info('Deletable directory: ' + i)

    def get_loc_files(self):
        os.chdir(self.adb_paths.root_unix_src_dir)
        cmd_get_loc_files = ['find', self.adb_paths.sync_dir, '-type', 'f']
        list_loc_files = BashProcess.get_form_out_cmd(cmd_get_loc_files).split('\n')
        return list_loc_files

    def get_rem_files(self):
        cmd_adb_get_rem_files = ['adb', 'shell', 'cd '
                                 + self.adb_paths.root_dest_dir
                                 + ' && find '
                                 + self.adb_paths.sync_dir
                                 + ' -type f']

        list_rem_files = BashProcess.get_form_out_cmd(cmd_adb_get_rem_files).split('\n')
        return list_rem_files

    def upload(self, command, loc_files):
        msg = 'Uploading files...'
        print(msg)
        self.logger.info(msg)
        cmd_conv_path = ['cygpath.exe', '--windows', '']

        for idx, val in enumerate(loc_files):
            command[len(command) - 1] = self.adb_paths.root_dest_dir + val
            val = self.adb_paths.root_unix_src_dir + val
            cmd_conv_path[len(cmd_conv_path) - 1] = val
            val = BashProcess.get_form_out_cmd(cmd_conv_path)
            command[len(command) - 2] = val
            out = BashProcess.get_cmd_output(command)

            if out.returncode == 0:
                form_out = out.stdout.strip('\n')
                print(form_out)
                self.logger.info(form_out)
            else:
                form_err = out.stderr.strip('\n')
                print(form_err)
                self.logger.error(form_err)

    def get_logger(self):
        """
        Creating file of logging and Logger object with custom preset.
        @return: instance of logger
        """
        create_subfolder = False
        date_now = Date.get_time_now()
        path_logs_dir = Log.get_logs_dir('adb_sync_Redmi-Note-9-Pro', create_subfolder)
        full_path_log_file = path_logs_dir + '/' + date_now + '.log'

        log_format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename=full_path_log_file,
                            level=logging.INFO,
                            format=log_format)

        return logging.getLogger()

def main():
    sync_music = SyncMusic()

    is_exist, is_empty = sync_music.is_exist_rem_dir()
    sync_music.prep_transf(is_exist, is_empty)

main()