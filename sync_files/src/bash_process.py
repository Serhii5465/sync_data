import subprocess
import sys
from typing import List


def get_cmd_output(command: List[str]) -> subprocess.CompletedProcess:
    """
    Execution Unix command in separate process and waits for it to be completed.
    Parameter 'capture_output' is responsible for capture stdout/stderr and store their
    outputs in variable.
    Parameter 'text=True' interpreters outputs stdout/stderr in human-readable format.
    Args:
        command: Array with arguments execution of command.

    Returns:
        Instance of CompletedProcess class.
    """
    return subprocess.run(command, capture_output=True, text=True)


def run_cmd(command: List[str]) -> subprocess.CompletedProcess:
    """
    Execution Unix command in separate process and waits for it to be completed.
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


def get_form_out_cmd(command: List[str]) -> str:
    """
    Execution Unix command in separate process and waits for it to be completed.
    Args:
        command: Array with arguments execution of command.

    Returns:
         Output stdout without delimiter of new line.
    """
    return get_cmd_output(command).stdout.strip('\n')
