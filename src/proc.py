import subprocess
import sys
from typing import List

def run_cmd(command: List[str]) -> subprocess.CompletedProcess:
    """
    Execution command in separate process and waits for it to be completed.
    Parameter 'stderr=sys.stderr' implies that all errors events will be redirected to
    standard error stream.
    Parameter 'stdout=sys.stdout' implies that all output data will be redirected to
    standard output stream.
    Args:
        command: Array with arguments execution of command.

    Returns:
        Instance of CompletedProcess class.
    """
    return subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)