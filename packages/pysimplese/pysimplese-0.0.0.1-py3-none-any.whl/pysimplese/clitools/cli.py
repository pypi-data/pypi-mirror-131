import os
import subprocess
import sys

os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire
def _run_command(args):
    return subprocess.check_call(" ".join(args), shell=True)
class CLI:
    def hi(cls):
        print('Hi, welcome to use pysimplese !'.center(50, '*'))

    @classmethod
    def cmd(cls, *args, **kwargs):
        _run_command(sys.argv[2:])

    @classmethod
    def testsysargv(cls, *args, **kwargs):
        import sys
        print("sys.argv:", sys.argv)
        print("executable:", sys.executable)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()