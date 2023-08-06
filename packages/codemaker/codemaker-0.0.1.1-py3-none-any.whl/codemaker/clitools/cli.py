import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire
from codemaker.makecode import gencode,write_yaml
DEFAULT_MAKER_FILE='maker.yaml'
class CLI:
    def hi(cls):
        print('Hi, I am codemaker.'.center(50, '*'))
    def maketmpl(self,target=None,overwrite=False):
        if not target:
            target=DEFAULT_MAKER_FILE
        if os.path.exists(target) and not overwrite:
            raise FileExistsError(target)
        write_yaml(dict(
            exts=['.py','.txt'],
            params=dict(
                foo='foo value'
            ),
        ),target)
    def gencode(self,src,dst,maker=DEFAULT_MAKER_FILE,overwrite=False,exists_ok=True):
        return gencode(src,dst,maker,overwrite=overwrite,exists_ok=exists_ok)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()