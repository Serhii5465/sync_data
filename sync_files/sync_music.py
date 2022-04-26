import os
from src import bash_proc

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
    if the receiver folder exists and is not empty, all files and folders that are
    missing on the transmitter side will be deleted and new ones will be pushed.
    @param win_src_dir: Full path to folder-transmitter in Windows style format
    @param root_unix_src_dir: Full path to root-folder, where is located folder-transmitter in UNIX style format
    @param root_dest_dir: Full path to root-folder, where is located folder-receiver
    @param sync_dir: Name of folder-transmitter
    """

    # if directory is exist, command will be returned 0, otherwise 1
    cmd_exist_dir = ['adb', 'shell', '[ -d ' + root_dest_dir + sync_dir + ' ] && echo 0 || echo 1']
    # if directory is empty, command will be returned 1, otherwise 0
    cmd_empty_dir = ['adb', 'shell', 'find ' + root_dest_dir + sync_dir + ' -mindepth 1 -maxdepth 1 | read && echo 0 || echo 1'] # 0 - not empty, 1 - empty

    is_exist = get_form_out_cmd(cmd_exist_dir)
    is_empty = get_form_out_cmd(cmd_empty_dir)

    cmd_adb_push = ['adb', 'push', win_src_dir, root_dest_dir]
    cmd_adb_sync = ['adb', 'push', '--sync', win_src_dir, root_dest_dir]

    if is_exist == '1' and is_empty == '1':
        # adb push
        print('not exist')
        bash_proc.run_cmd(cmd_adb_push)
    if is_exist == '0' and is_empty == '1':
        # adb push
        print('exist,empty')
        bash_proc.run_cmd(cmd_adb_push)
    if is_exist == '0' and is_empty == '0':
        # adb push --sync
        print('exist,not empty')

        list_rem_files = get_form_out_cmd(['adb', 'shell', 'cd ' + root_dest_dir + ' && find ' + sync_dir + ' -type f']).split('\n')

        os.chdir(root_unix_src_dir)
        list_loc_files = get_form_out_cmd(['find', sync_dir, '-type', 'f']).split('\n')

        list_miss_files = ['"' + root_dest_dir + i + '"' for i in list(set(list_rem_files) - set(list_loc_files))]

        if len(list_miss_files) != 0:
            cmd_del_file = ['adb', 'shell', 'rm', '']

            print('Removing files')
            for i in list_miss_files:
                print(i)
                cmd_del_file[len(cmd_del_file) - 1] = i
                bash_proc.run_cmd(cmd_del_file)

            # Utility find removing empty folders
            empty_dirs = get_form_out_cmd(['adb', 'shell', 'find ' + root_dest_dir + sync_dir + ' -type d -delete'])
            if empty_dirs != '':
                print(empty_dirs)

        bash_proc.run_cmd(cmd_adb_sync)


def main():
    sync_dir = 'Music/'
    root_unix_src_dir = '/cygdrive/d/media/'
    full_path_unix_src_root = root_unix_src_dir + sync_dir
    win_src_dir = bash_proc.get_cmd_output(['cygpath.exe', '--windows', full_path_unix_src_root]).stdout.strip('\n')

    root_dest_dir = '/storage/self/primary/'

    upload(win_src_dir, root_unix_src_dir, root_dest_dir, sync_dir)

main()