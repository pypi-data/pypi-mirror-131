import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire
from freehub.clitools.cli import Cli as fhcli
def _complete_address(address):
    if not '/' in address:
        address = 'tmpl/' + address
    else:
        address = address
    return address
class CLI:
    '''
    fetch code templates on github or gitee

    demo of codetmpl:
        codetmpl list;
        codetmpl export python_package ./
    '''
    def hi(cls):
        print('Hi, I am codetmpl.'.center(50, '*'))
    @classmethod
    def list(cls):
        fhcli.ls('tmpl')
    @classmethod
    def export(cls,tmpl:str,target='.'):
        '''
        :param tmpl: template path
        :param target: output path
        :return:
        '''
        tmpl=tmpl.replace('\\','/')
        address=_complete_address(tmpl)
        fhcli.download(address,target)
def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()