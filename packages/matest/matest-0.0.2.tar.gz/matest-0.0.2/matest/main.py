import os
import sys
import json
import importlib

from core import Mobj, wrap_run


class Matest(Mobj):

    def load_plugins(self, p='plugins'):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), p)
        self.modules = {}
        sos = [self.shortopts]
        for mn in [md[:-3] for md in os.listdir(path) if md[0] == 'm' and md.endswith('.py')]:
            cp  = os.path.join(self.base_path, 'conf', f"{mn}.json")
            if os.path.exists(cp):
                self.modules[mn] = None
                with open(cp, 'r', encoding='utf-8') as f:
                    conf = json.load(f)
                if 'argv' in conf:
                    ops = [f"{k}{v['require']}" for k, v in conf['argv'].items() if self.shortopts.find(k)<0]
                    sos.append(''.join(ops))
        self.shortopts =  ''.join(sos)

    def load_conf(self):
        super(Matest, self).load_conf()
        self.load_plugins()

    def _pre(self, cmd):
        super(Matest, self)._pre(cmd if isinstance(cmd, str) else ' '.join(cmd))
        return [m for m in self.modules.keys() if m.startswith(self.optd['-r'])][0]

    @wrap_run
    def run(self, cmd):
        if cmd in self.modules:
            if self.modules[cmd] is None:
                # 动态导入module
                self.modules[cmd] = importlib.import_module(f".{cmd}", package='plugins')
            # 动态导入class
            mclass = getattr(self.modules[cmd], cmd.capitalize())
            # 动态方法
            mclass().run((self.opts, self.args, self.optd))


if __name__ == '__main__':
    Matest().run(sys.argv[1:])
