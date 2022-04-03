import os
from src import bash_proc

def get_out_adb_cmd(arg):
    cmd = ['adb', 'shell', arg] 
    return bash_proc.get_cmd_output(cmd).stdout.strip('\n')

def run_adb_cmd(command):
    bash_proc.run_cmd(command)

def upload(src, dest, root_dest):
    arg_cmd_exist_dir = '[ -d ' + dest + ' ] && echo 0 || echo 1'  # 0 - exist, 1 - not exist 
    arg_cmd_empty_dir = 'find ' + dest + ' -mindepth 1 -maxdepth 1 | read && echo 0 || echo 1' # 0 - not empty, 1 - empty 

    is_exist = get_out_adb_cmd(arg_cmd_exist_dir)
    is_empty = get_out_adb_cmd(arg_cmd_empty_dir)

    cmd_adb_push = ['adb', 'push', src, root_dest]
    cmd_adb_sync = ['adb', 'push', '--sync', src, root_dest]

    if is_exist == '1' and is_empty == '1':
        # adb push
        print('not exist')
        run_adb_cmd(cmd_adb_push)
    if is_exist == '0' and is_empty == '1':
        # adb push
        print('exist,empty')
        run_adb_cmd(cmd_adb_push)
    if is_exist == '0' and is_empty == '0':
        # adb push --sync
        print('exist,not empty')
        run_adb_cmd(cmd_adb_sync)


def main():
    unix_src_dir = '/cygdrive/d/raisnet/Music'
    win_src_dir = bash_proc.get_cmd_output(['cygpath.exe', '--windows', unix_src_dir]).stdout.strip('\n')
    
    dest_dir = '/storage/self/primary/Music'
    root_dest_dir = os.path.dirname(dest_dir)
    upload(win_src_dir, dest_dir, root_dest_dir)

main()