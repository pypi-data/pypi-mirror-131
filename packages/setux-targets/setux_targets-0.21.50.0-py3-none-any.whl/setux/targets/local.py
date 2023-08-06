from shutil import copy
from pathlib import Path

from setux.core.errors import ExecError
from .base import BaseTarget
from . import error, info, debug


# pylint: disable=arguments-differ


class Local(BaseTarget):
    def __init__(self, **kw):
        kw['name'] = kw.get('name', 'local')
        super().__init__(**kw)

    def set_local(self):
        self.local = self
        return self.local

    def run(self, *arg, **kw):
        arg, kw = self.parse(*arg, **kw)
        check = kw.pop('check', False)
        ret, out, err =  super().run(*arg, **kw)
        self.trace(' '.join(arg), ret, out, err, **kw)
        if check and ret:
            raise ExecError(' '.join(arg), ret, out, err)
        return ret, out, err

    def read(self, path, mode='rt', critical=True, report='normal'):
        if report=='normal':
            info(f'\tread {path}')
        return open(path, mode).read()

    def write(self, path, content, mode='wt', report='normal'):
        if report=='normal':
            info(f'\twrite {path}')
        dest = path[:path.rfind('/')]
        self.run(f'mkdir -p {dest}', report=report)
        with open(path, mode) as out:
            out.write(content)
        return open(path, mode=mode.replace('w','r')).read() == content

    def do_send(self, local, remote):
        local =  Path(local)
        assert local.is_file()
        remote = Path(remote) if remote else local
        if remote == local: return True
        ret, out, err = super().run(f'mkdir -p {remote.parent}')
        if ret: return False
        try:
            copy(local, remote)
            return True
        except:
            return False

    def fetch(self, remote, local, quiet=False):
        if remote == local: return True
        if not quiet: info(f'\tfetch {local} <- {remote}')
        try:
            copy(remote, local)
            return True
        except:
            return False

    def do_sync(self, src, dst=None):
        if dst == src: return
        assert Path(src).is_dir()
        if not src.endswith('/'): src+='/'
        if dst:
            self.dir(dst).set()
            info(f'\tsync {src} -> {dst}')
            return self.rsync(f'{src} {dst}')
        else:
            debug(f'\tskipped {src} -> {dst}')
            return True

    def export(self, path):
        error("can't export on local")

    def remote(self, module, export_path=None, **kw):
        error("can't remote on local")

    def __str__(self):
        return f'Local({self.name})'
