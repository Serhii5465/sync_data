import os
import sys
import logging
from src import hdd_info, bash_process, date, log


class SyncMusic:

    def __init__(self):
        self.get_stat_dev()

        self.__sync_dir = 'Music/'
        self.__root_unix_src_dir = '/cygdrive/d/media/'
        self.__full_path_unix_src_root = self.__root_unix_src_dir + self.__sync_dir
        self.__win_src_dir = bash_process.get_form_out_cmd(['cygpath.exe', '--windows', self.__full_path_unix_src_root])
        self.__root_dest_dir = '/storage/self/primary/'

        self.__logger = self.crt_logger()

    @property
    def sync_dir(self):
        return self.__sync_dir

    @property
    def root_unix_src_dir(self):
        return self.__root_unix_src_dir

    @property
    def full_path_unix_src_root(self):
        return self.__full_path_unix_src_root

    @property
    def win_src_dir(self):
        return self.win_src_dir

    @property
    def root_dest_dir(self):
        return self.root_dest_dir

    @property
    def logger(self):
        return self.__logger

    def get_stat_dev(self):
        """
        Verifying connection of USB device by his serial number.
        """
        serial_no = '293290c6'
        cmd_state = ['adb', 'devices']
        out = bash_process.get_form_out_cmd(cmd_state)

        if out.find(serial_no) == -1:
            sys.exit('Device not connected')

    def is_exist_rem_dir(self):
        # if directory is exist, command will be returned 0, otherwise 1
        cmd_is_exist_dir = ['adb', 'shell', '[ -d ' + self.root_dest_dir
                            + self.sync_dir + ' ] && echo 0 || echo 1']
        # if directory is empty, command will be returned 1, otherwise 0
        cmd_is_empty_dir = ['adb', 'shell',
                            'find ' + self.root_dest_dir + self.sync_dir +
                            ' -mindepth 1 -maxdepth 1 | '
                            'read && echo 0 || echo 1']  # 0 - not empty, 1 - empty

        is_exist = bash_process.get_form_out_cmd(cmd_is_exist_dir)
        is_empty = bash_process.get_form_out_cmd(cmd_is_empty_dir)

        return is_exist, is_empty

    def prep_transf(self, is_exist, is_empty):

        cmd_adb_push = ['adb', 'push', '', '']

        list_loc_files = self.get_loc_files()

        if is_exist == '1' and is_empty == '1':
            # adb push
            print('Music folder not exist')
            cmd_adb_mkdir = ['adb', 'shell', 'mkdir', self.root_dest_dir + self.sync_dir]
            bash_process.run_cmd(cmd_adb_mkdir)
            self.upload(cmd_adb_push, list_loc_files)

        if is_exist == '0' and is_empty == '1':
            # adb push
            print('Music folder exist,but empty')
            self.upload(cmd_adb_push, list_loc_files)

        if is_exist == '0' and is_empty == '0':
            # adb push --sync
            print('Music folder exist and not empty')
            list_rem_files = self.get_rem_files()

            list_del_files = ['"' + self.root_dest_dir + i +
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
                out = bash_process.get_cmd_output(cmd_del_file)
                if out.returncode != 0:
                    print(out.stderr)
                    self.__logger.error(out.stderr)

            # Utility 'find' removing empty folders
            cmd_del_empt_dir = ['adb', 'shell',
                                'find ' + self.root_dest_dir
                                + self.sync_dir + ' -type d -delete']

            str_empty_dirs = bash_process.get_form_out_cmd(cmd_del_empt_dir)
            if str_empty_dirs != '':
                print('Removing empty directories')
                list_empty_dirs = str_empty_dirs.split('\n')
                for i in list_empty_dirs:
                    print(i)
                    self.__logger.info('Deletable directory: ' + i)

    def get_loc_files(self):
        os.chdir(self.root_unix_src_dir)
        cmd_get_loc_files = ['find', self.sync_dir, '-type', 'f']
        list_loc_files = bash_process.get_form_out_cmd(cmd_get_loc_files).split('\n')
        return list_loc_files

    def get_rem_files(self):
        cmd_adb_get_rem_files = ['adb', 'shell', 'cd '
                                 + self.root_dest_dir
                                 + ' && find '
                                 + self.sync_dir
                                 + ' -type f']

        list_rem_files = bash_process.get_form_out_cmd(cmd_adb_get_rem_files).split('\n')
        return list_rem_files

    def upload(self, command, loc_files):
        msg = 'Uploading files...'
        print(msg)
        self.logger.info(msg)
        cmd_conv_path = ['cygpath.exe', '--windows', '']

        for idx, val in enumerate(loc_files):
            command[len(command) - 1] = self.root_dest_dir + val
            val = self.root_unix_src_dir + val
            cmd_conv_path[len(cmd_conv_path) - 1] = val
            val = bash_process.get_form_out_cmd(cmd_conv_path)
            command[len(command) - 2] = val
            out = bash_process.get_cmd_output(command)

            if out.returncode == 0:
                form_out = out.stdout.strip('\n')
                print(form_out)
                self.logger.info(form_out)
            else:
                form_err = out.stderr.strip('\n')
                print(form_err)
                self.logger.error(form_err)

    def crt_logger(self):
        """
        Creating file of logging and Logger object with custom preset.
        @return: instance of logger
        """
        create_subfolder = False
        date_now = date.get_time_now()
        path_logs_dir = log.get_logs_dir('adb_sync_Redmi-Note-9-Pro', create_subfolder)
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
