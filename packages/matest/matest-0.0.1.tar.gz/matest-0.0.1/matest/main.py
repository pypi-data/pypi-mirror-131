import os
import sys
import getopt
import importlib

class Matest(object):
    plugins = {}

    @classmethod
    def init(cls):
        cls.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugin')
        # [cls.load_plugin(m) for m in os.listdir(path) if m.endswith('.py')]

    @classmethod
    def load_plugin(cls, m):
        pass
        # _m = importlib.import_module(f'plugin.{m[:-3]}')

    @classmethod
    def run(cls, argv):
        print(f'Hello world: {argv}')


if __name__ == '__main__':
    Matest.Run(sys.argv[1:])
