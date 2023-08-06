import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire
from codemaker.makecode import gencode,write_yaml
DEFAULT_MAKER_FILENAME='maker.yaml'
class CLI:
    def hi(cls):
        print('Hi, I am codemaker.'.center(50, '*'))
    def maketmpl(self,target=None,overwrite=False):
        if not target:
            target=DEFAULT_MAKER_FILENAME
        if os.path.exists(target) and not overwrite:
            raise FileExistsError(target)
        write_yaml(dict(
            exts=['.py','.txt'],
            params=dict(
                foo='foo value'
            ),
        ),target)
    def gencode(self,src,dst,maker=DEFAULT_MAKER_FILENAME,overwrite=False,exists_ok=True,**kwargs):
        return gencode(src,dst,maker,overwrite=overwrite,exists_ok=exists_ok,**kwargs)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()