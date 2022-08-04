import os
import sys
import logging
from src import bash_proc, log, date


def get_form_out_cmd(arg):
    """
    Execution command in separate process and returning output stdout
    without separator of new line
    @param arg: List of command of with arguments
    @return: Formatted output
    """
    return bash_proc.get_cmd_output(arg).stdout.strip('\n')


def upload(win_src_dir, root_unix_src_dir, root_dest_dir, sync_dir):
    """
    Preparing data and uploading them to Android device using ADB utility.
    Function verifies, if exist remote folder on smartphone and
    performs manipulation with files.
    If folder-receiver does not exist, she will be created and will be pushed files.
    If folder-receiver. exist, but she is empty, will be pushed files.
    if the receiver folder exists and is not empty, will be created instance of logger, all files and folders that are
    missing on the transmitter side will be deleted and new ones will be pushed.
    @param win_src_dir: Full path to folder-transmitter in Windows style format
    @param root_unix_src_dir: Full path to root-folder in UNIX style format, where is located folder-transmitter
    @param root_dest_dir: Full path to root-folder, where is located folder-receiver
    @param sync_dir: Name of folder-transmitter
    """

    # if directory is exist, command will be returned 0, otherwise 1
    cmd_is_exist_dir = ['adb', 'shell', '[ -d ' + root_dest_dir + sync_dir + ' ] && echo 0 || echo 1']
    # if directory is empty, command will be returned 1, otherwise 0
    cmd_is_empty_dir = ['adb', 'shell',
                        'find ' + root_dest_dir + sync_dir + ' -mindepth 1 -maxdepth 1 | read && echo 0 || echo 1']  # 0 - not empty, 1 - empty

    is_exist = get_form_out_cmd(cmd_is_exist_dir)
    is_empty = get_form_out_cmd(cmd_is_empty_dir)

    cmd_adb_push = ['adb', 'push', win_src_dir, root_dest_dir]
    cmd_adb_sync = ['adb', 'push', '--sync', win_src_dir, root_dest_dir]

    # Initialization of logger
    logger = get_logger()

    if is_exist == '1' and is_empty == '1':
        # adb push
        print('Music folder not exist')
        log_stat_files(get_diff_files(root_dest_dir, sync_dir, root_unix_src_dir), logger, 'Downloadable file: ')
        bash_proc.run_cmd(cmd_adb_push)

    if is_exist == '0' and is_empty == '1':
        # adb push
        print('Music folder exist,but empty')
        log_stat_files(get_diff_files(root_dest_dir, sync_dir, root_unix_src_dir), logger, 'Downloadable file: ')
        bash_proc.run_cmd(cmd_adb_push)

    if is_exist == '0' and is_empty == '0':
        # adb push --sync
        print('Music folder exist and not empty')

        is_upload = False
        delete_remt_files(get_diff_files(root_dest_dir, sync_dir, root_unix_src_dir, is_upload),
                          root_dest_dir,
                          sync_dir,
                          logger)

        log_stat_files(get_diff_files(root_dest_dir, sync_dir, root_unix_src_dir), logger, 'Downloadable file: ')

        print('Uploading files')
        bash_proc.run_cmd(cmd_adb_sync)


def delete_remt_files(list_miss_files, root_dest_dir, sync_dir, logger):
    """
    Deleting missing files on the local PC from the Android.
    @param list_miss_files: An array of files that are missing on the sender side.
    @param root_dest_dir: Full path to root-folder, where is located folder-receiver.
    @param sync_dir: Name of folder-transmitter.
    @param logger: Instance of logger.
    """
    if len(list_miss_files) != 0:
        cmd_del_file = ['adb', 'shell', 'rm', '']
        print('Removing files')
        for i in list_miss_files:
            print(i)
            logger.info('Deletable file: ' + i)
            cmd_del_file[len(cmd_del_file) - 1] = i
            out = bash_proc.get_cmd_output(cmd_del_file)
            if out.returncode != 0:
                print(out.stderr)
                logger.error(out.stderr)

        # Utility 'find' removing empty folders
        cmd_del_empt_dir = ['adb', 'shell', 'find ' + root_dest_dir + sync_dir + ' -type d -delete']
        str_empty_dirs = get_form_out_cmd(cmd_del_empt_dir)
        if str_empty_dirs != '':
            print('Removing empty directories')
            list_empty_dirs = str_empty_dirs.split('\n')
            for i in list_empty_dirs:
                print(i)
                logger.info('Deletable directory: ' + i)


def get_diff_files(root_dest_dir, sync_dir, root_unix_src_dir, is_upload=True):
    """
    Finds and compares files on local PC and Android device for further download (update) or deletion.
    @param root_dest_dir: Full path to root-folder, where is located folder-receiver.
    @param sync_dir: Name of folder-transmitter.
    @param root_unix_src_dir: Full path to root-folder in UNIX style format, where is located folder-transmitter
    @param is_upload: Indicates, which array will be returned. If true, function returned list of files, which
    be uploaded. Otherwise, returns list of files, which will be removed from Android device.
    @return:
    """
    # Getting list of files on Android device
    cmd_adb_get_rem_files = ['adb', 'shell', 'cd ' + root_dest_dir + ' && find ' + sync_dir + ' -type f']
    list_rem_files = get_form_out_cmd(cmd_adb_get_rem_files).split('\n')

    # Getting list of files on PC
    os.chdir(root_unix_src_dir)
    cmd_get_loc_files = ['find', sync_dir, '-type', 'f']
    list_loc_files = get_form_out_cmd(cmd_get_loc_files).split('\n')

    if not is_upload:
        # List of full paths to files, which are missing on Android
        return ['"' + root_dest_dir + i + '"' for i in list(set(list_rem_files) - set(list_loc_files))]
    else:
        # List of full paths to files, which are will be uploaded from PC to Android device
        return ['"' + root_unix_src_dir + i + '"' for i in list(set(list_loc_files) - set(list_rem_files))]


def log_stat_files(list_upl_files, logger, msg):
    """
    The function logs the full path to the file, which will be uploaded.
    @param list_upl_files: List of uploading files.
    @param logger: Instance of logger.
    @param msg: Message status of file.
    """
    for i in list_upl_files:
        logger.info(msg + i)


def get_stat_dev():
    """
    Verifying connection of USB device by his serial number.
    """
    serial_no = '293290c6'
    cmd_state = ['adb', 'devices']
    out = get_form_out_cmd(cmd_state)

    if out.find(serial_no) == -1:
        sys.exit('Device not connected')


def get_logger():
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
    get_stat_dev()

    sync_dir = 'Music/'
    root_unix_src_dir = '/cygdrive/d/media/'
    full_path_unix_src_root = root_unix_src_dir + sync_dir
    win_src_dir = bash_proc.get_cmd_output(['cygpath.exe', '--windows', full_path_unix_src_root]).stdout.strip('\n')

    root_dest_dir = '/storage/self/primary/'

    upload(win_src_dir, root_unix_src_dir, root_dest_dir, sync_dir)

main()