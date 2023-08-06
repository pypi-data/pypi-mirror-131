from setux.core.target import CoreTarget
from setux.core.deployers import Sender, Syncer
from . import logger, info, error


class BaseTarget(CoreTarget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.context = dict()

    def __call__(self, command, **kw):
        ret, out, err = self.run(command, **kw)
        info('\n\t'.join(out))
        return ret

    def send(self, local, remote=None):
        try:
            Sender(self, local=local, remote=remote or local)()
        except Exception as x:
            error(f'send {local} -> {remote} ! {x}')
            return False
        return True

    def sync(self, src, dst=None):
        try:
            Syncer(self, src=src, dst=dst or src)()
        except Exception as x:
            error(f'sync {src} -> {dst} ! {x}')
            return False
        return True

