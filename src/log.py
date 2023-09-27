from pathlib import Path

def get_logs_dir(dir: str) -> str:
    """
    Function creates all hierarchy parent and child's directories
    and return their all path.

    Args:
        dir: Name parent log's directory.

    Returns:
        Full path to log's dir.
    """

    full_path_logs_dir = '/cygdrive/d/logs/' + dir + '/'

    Path(full_path_logs_dir).mkdir(parents=True, exist_ok=True)

    return full_path_logs_dir
