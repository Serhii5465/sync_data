import argparse, sys
from typing import List, Dict
from src import bash_process

class SyncRaspberry:

    def __init__(self) -> None:
        self.__root_dir_src = '/cygdrive/d/projects/dissertation/test/'
        self.__root_dir_dest = '~/projects/'

        self.__proj_prs_serial_port = {
            'dir' : 'master_uart',
            'id' : 'uart'
        }

        self.__proj_tcp_client = {
            'dir' : 'master_tcp_client',
            'id' : 'tcp'
        }

        self.__id_vb_rasp_1 = 'raspivb1'
        self.__id_vb_rasp_2 = 'raspivb2'
        self.__id_vb_rasp_3 = 'raspivb3'
        self.__id_board_rasp = 'raspi'

        self.__rsync_cmd = [
            'rsync',
            '--recursive',
            '--perms',
            '--times',
            '--group',
            '--owner',
            '--human-readable',
            '--stats',
            '--progress',
            '--del',
            '--verbose',
            '--out-format="%t %f %''b"',
            '--exclude=node_modules',
            '--exclude=.gitignore',
            '--exclude=logs',
            '',
            ''
        ]

    @property
    def root_dir_src(self) -> str:
        return self.__root_dir_src
    
    @property
    def root_dir_dest(self) -> str:
        return self.__root_dir_dest

    @property
    def proj_prs_serial_port(self) -> Dict[str, str]:
        return self.__proj_prs_serial_port

    @property
    def proj_tcp_client(self) -> Dict[str, str]:
        return self.__proj_tcp_client

    @property
    def id_vb_rasp_1(self) -> str:
        return self.__id_vb_rasp_1

    @property
    def id_vb_rasp_2(self) -> str:
        return self.__id_vb_rasp_2

    @property
    def id_vb_rasp_3(self) -> str:
        return self.__id_vb_rasp_3

    @property
    def id_board_rasp(self) -> str:
        return self.__id_board_rasp

    @property
    def rsync_cmd(self) -> List[str]:
        return self.__rsync_cmd 

    def sync_files(self) -> None:
        parser = argparse.ArgumentParser(description='Synchronization files of projects between PC \
                                          and Raspberry Pi OS (VirtualBox/Raspberry Pi 1 Model B+)')

        obj_proj_list = [self.proj_prs_serial_port, self.proj_tcp_client]

        choise_type_list = []
        choise_dest_list = [self.id_vb_rasp_1, self.id_vb_rasp_2, self.id_vb_rasp_3, self.id_board_rasp]

        for i in obj_proj_list:
            choise_type_list.append(i.get('id'))

        parser.add_argument('-t', '--type', help='Project selection to be copied', required=True, 
                            choices=choise_type_list)
        
        parser.add_argument('-d', '--dest', help='The platform to which the project will be copied', required=True, 
                            choices=choise_dest_list)

        args = vars(parser.parse_args())

        for i in choise_dest_list:
            if i == args['dest']:
                self.rsync_cmd[len(self.rsync_cmd) - 1] =  i + ':' + self.root_dir_dest

        for i in obj_proj_list:
            if i.get('id') == args['type']:
                self.rsync_cmd[len(self.rsync_cmd) - 2] = self.root_dir_src + i.get('dir') + '/'
                self.rsync_cmd[len(self.rsync_cmd) - 1] += i.get('dir')
                break

        out = bash_process.run_cmd(self.rsync_cmd)

        if out.returncode != 0:
            sys.exit('Error uploading')
        else:
            print('\nGood')

def main():
    rasp = SyncRaspberry()
    rasp.sync_files()

main()