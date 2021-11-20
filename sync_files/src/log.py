import os
from pathlib import Path
import src.time as time

def get_logs_dir(name_dir):
    date_now = time.get_time_now()

    full_path_logs_dir = '/cygdrive/d/logs/' + name_dir + '/' + date_now

    Path(os.path.dirname(full_path_logs_dir)).mkdir(parents=True, exist_ok=True)

    return full_path_logs_dir