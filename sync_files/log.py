from pathlib import Path

def get_logs_dir(name):
    home_dir = str(Path.home())

    full_path_logs_dir = home_dir + '/logs/' + name

    Path(full_path_logs_dir).mkdir(parents=True, exist_ok=True)

    return full_path_logs_dir