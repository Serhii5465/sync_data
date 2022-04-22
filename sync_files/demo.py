from src import bash_proc
from glob import glob
from os import path

out = bash_proc.get_cmd_output(['adb', 'shell', 'ls -A -1 /storage/self/primary/1'])
list1 = out.stdout.strip('\n').split('\n')
print(list1)

list2 = [(path.basename(path.dirname(i))) for i in glob('/cygdrive/d/downloads/1/*/', recursive=True)] 
print(list2)

diff = list(set(list1) - set(list2))