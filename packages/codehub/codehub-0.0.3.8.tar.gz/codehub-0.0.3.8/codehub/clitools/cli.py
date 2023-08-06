import os
import subprocess
import sys
import shutil
import fire
from codehub import api
from codehub.clitools.utils import FileUtil,gen_fire_argv
os.environ['ANSI_COLORS_DISABLED'] = "1"
DEFAULT_PACKAGE_CONFIG_FILENAME = 'package.yml'


def _run_command(args):
    return subprocess.check_call(args, shell=True)


def load_yaml(path):
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
def run_inspect(path,args):

    FileUtil.inject_fire(path)
    try:
        subprocess.check_call([sys.executable,path,*args],shell=True)
    except Exception as e:
        FileUtil.remove_fire(path)
        raise e
    FileUtil.remove_fire(path)

class PackageConfigManager:
    def __init__(self, package_dir):
        self.root_dir = package_dir
        self.package_config_file = os.path.join(package_dir, DEFAULT_PACKAGE_CONFIG_FILENAME)
        self.cfg = load_yaml(self.package_config_file)
    def run_package_script(self, name):
        scripts=self.cfg['scripts']
        if name  not in scripts.keys():
            raise Exception('Unknown command : %s'%(name))
        cmd=scripts[name]
        _run_command(cmd.strip().split())


class CLI:
    _cmd_proxies = {
        'pip': 'pip',
        'python': 'python',
        'py': 'python'
    }

    def __init__(self):
        def get_func(k, v):
            def func(*args, **kwargs):
                _run_command([v, *sys.argv[2:]])

            func.__name__ = k
            return func

        for k, v in self._cmd_proxies.items():
            setattr(self, k, get_func(k, v))

    @classmethod
    def hi(cls):
        print('Hi, welcome to use codehub !'.center(50, '*'))
    @classmethod
    def cli(cls,*args,**kwargs):
        return cls.fire('cli.py',*args,**kwargs)
    @classmethod
    def fetch(cls, address: str):
        api.fetch_if_not_exists(address)

    @classmethod
    def clean(cls, path='/'):
        api.clean(path)

    @classmethod
    def fire(cls,path,*args,**kwargs):
        def gen_fire_argv(*args, **kwargs):
            argv = []
            for arg in args:
                argv.append(str(arg))
            for k, v in kwargs.items():
                argv.append('--%s=%s' % (k, v))
            return argv
        FileUtil.inject_fire(path)
        try:
            subprocess.check_call([sys.executable, path, *gen_fire_argv(*args,**kwargs)], shell=True)
        except Exception as e:
            FileUtil.remove_fire(path)
            raise e
        FileUtil.remove_fire(path)
    @classmethod
    def run(cls, cmd):
        pcm = PackageConfigManager(os.getcwd())
        pcm.run_package_script(cmd)

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
