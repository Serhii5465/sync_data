import subprocess
import sys

def get_cmd_output(command):
    """
    Execution Unix command in separate process.
    Wait for command to complete, then return instance's [CompletedProcess] class.
    Parameter [capture_output] is responsible for capture stdout/stderr and store their
    outputs in variable.
    Parameter [text=True] interpreters outputs stdout/stderr in human-readable format.
    Default value [text] = False, and it means all inputs/output is accepted as binary data.
    :param command: array which contains name Unix utility and her argument's execution
    :return: instance of [CompletedProcess]
    """
    return subprocess.run(command, capture_output=True, text=True)


# get output command in real time
def run_cmd(command):
    """
    Execution Unix command with arguments in separate process.
    Wait for command to complete, then return instance of the [CompletedProcess] class.
    Parameter [stderr = sys.stderr] implies that all errors events will be redirected to
    standard error stream.
    Parameter [stdout=sys.stdout] implies that all output data will be redirected to
    standard output stream.
    :param command: array which contains name Unix utility and her argument's execution
    :return: instance of [CompletedProcess]
    """
    return subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)