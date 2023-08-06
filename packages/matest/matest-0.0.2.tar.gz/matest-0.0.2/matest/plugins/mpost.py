from core import Mobj, wrap_run, singleton


@singleton
class Mpost(Mobj):

    @wrap_run
    def run(self, cmd):
        print(f'P2.{self.optd}')
