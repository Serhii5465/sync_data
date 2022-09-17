from src.bash_process import BashProcess

class AdbPaths:
    def __init__(self) -> None:
        self.__sync_dir = 'Music/'
        self.__root_unix_src_dir = '/cygdrive/d/media/'
        #self.__root_unix_src_dir = '/cygdrive/d/downloads/Nox/'
        self.__full_path_unix_src_root = self.__root_unix_src_dir + self.__sync_dir
        self.__win_src_dir = BashProcess.get_form_out_cmd(['cygpath.exe', '--windows', self.__full_path_unix_src_root])
        self.__root_dest_dir = '/storage/self/primary/'
        #self.__root_dest_dir = '/storage/emulated/0/'

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
        return self.__win_src_dir

    @property
    def root_dest_dir(self):
        return self.__root_dest_dir