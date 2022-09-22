import sys
from src.bash_process import BashProcess


class Upload:

    @staticmethod
    def insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, name_sync_dir):
        """
        Inserting in array of arguments path to folder of the log file.
        Name file depends by if Rsync in dry-run mode.
        For example,if Rsync works in dry-run mode file will be named: Wester Digital__backups_TEST_MODE.log,
        where substring 'TEST_MODE' will be signalized about this mode.
        If Rsync will be works as usual, file wile be named: Wester Digital__backups.log
        :param command: list which contains all arguments execution of the Rsync utility
        :param is_test_mode: indicates, if Rsync runs in dry-run mode
        :param path_logs_dir: full path to log file
        :param name_model_recv_drive: name model of HDD-receiver
        :param name_sync_dir: name of synced folder
        """
        if is_test_mode:
            command[
                len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '_TEST_MODE' + '.log'
        else:
            command[
                len(command) - 3] = '--log-file=' + path_logs_dir + '/' + name_model_recv_drive + '__' + name_sync_dir + '.log'

    @staticmethod
    def upload_files(args):
        """
        Synchronizes files between local storage and external drive by using Rsync.
        If there is an error of synchronization, file access rights or something similar,
        the transfer will be terminated.
        :param args: Contains following fields:
        command - list of different argument's execution for Rsync;
        list_full_path_sync_dirs - full path to specific sync. folder (Example: /cygdrive/d/installers);
        name_model_recv_drive - model HDD-receiver;
        path_logs_dir - logs' directory;
        is_dry_run - is Rsync running in dry-run mode.
        """

        command = args.get('command')
        sync_dirs = args.get('sync_dirs')
        list_sync_dirs = args.get('list_full_path_sync_dirs')
        name_model_recv_drive = args.get('name_model_recv_drive')
        path_logs_dir = args.get('path_logs_dir')
        is_test_mode = args.get('is_dry_run')

        for idx, val in enumerate(list_sync_dirs):
            # Setting argument of source sync. folder
            command[len(command) - 2] = val

            # Inserting in array the argument of name log file
            Upload.insert_log_arg(command, is_test_mode, path_logs_dir, name_model_recv_drive, sync_dirs[idx])
            print('\nStart synchronization folder ' + '\'' + sync_dirs[idx] + '\'\n')
            # Start synchronization
            code = BashProcess.run_cmd(command)

            if code.returncode != 0:
                sys.exit('Error\nCheck logs')