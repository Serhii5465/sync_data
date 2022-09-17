from pathlib import Path


class RcloneConf:
    def __init__(self) -> None:
        self.__conf = str(Path.home()) + '/.config/rclone/rclone.conf'
        self.__prog_dir = '/cygdrive/c/portable/rclone'
        self.__sync_dir = '/cygdrive/d/documents'

    @property
    def conf(self):
        return self.__conf

    @property
    def prog_dir(self):
        return self.__prog_dir

    @property
    def sync_dir(self):
        return self.__sync_dir

