from pathlib import Path
from src import date

def get_logs_dir(name_dir,add_subfolder = True):
    """
    Function creates all hierarchy parent and child's directories
    and return their all path.
    :param name_dir: creates parent log directory
    :param add_subfolder: creates specific subdir for log file.Otherwise nothing happens.
    :return: full path to log file
    """
    date_now = date.get_time_now()

    if add_subfolder:
        full_path_logs_dir = '/cygdrive/d/logs/' + name_dir + '/' + date_now
    else:
        full_path_logs_dir = '/cygdrive/d/logs/' + name_dir

    Path(full_path_logs_dir).mkdir(parents=True, exist_ok=True)

    return full_path_logs_dir