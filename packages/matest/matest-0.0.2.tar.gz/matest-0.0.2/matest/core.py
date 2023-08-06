import os
import abc
import json
import getopt
from functools import wraps


def wrap_run(func):
    @wraps(func)
    def _(self, cmd):
        cmd = self._pre(cmd)
        data = func(self, cmd)
        return self._clean(data)
    return _


def singleton(cls):
    _instance = {}

    def _(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return _


class Mobj(metaclass = abc.ABCMeta):
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.load_conf()

    def load_conf(self):
        conf = os.path.join(self.base_path, 'conf', f'{self.__class__.__name__.lower()}.json')
        with open(conf, 'r', encoding='utf-8') as f:
            self.conf = json.load(f)
        # 注册一个字母的短命令，可少写两个字母
        setattr(self, self.conf['short_run'], self.run)
        self.shortopts = ''.join([f"{k}{v['require']}" for k, v in self.conf['argv'].items()])
        self.context = self.conf.get('context', {})

    def _pre(self, cmd):
        if isinstance(cmd, tuple):
            # 被main调用
            self.opts, self.args, self.optd = cmd
        else:
            # list是直接调用; str在jupyter引用调用
            argv = cmd if isinstance(cmd, list) else cmd.split(' ')
            self.opts, self.args = getopt.gnu_getopt(argv, self.shortopts)
            self.optd = {k: v for k, v in self.opts}

    def _clean(self, data):
        return data

    @abc.abstractmethod
    def run(self, cmd):
        pass


if __name__ == '__main__':
    pass
