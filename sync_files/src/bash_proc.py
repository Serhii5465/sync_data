import subprocess
import sys

# store stdout command in variable
def get_cmd_output(command):
    return subprocess.run(command, capture_output=True, text=True)


# get output command in real time
def run_cmd(command):
    return subprocess.run(command, stderr=sys.stderr, stdout=sys.stdout)