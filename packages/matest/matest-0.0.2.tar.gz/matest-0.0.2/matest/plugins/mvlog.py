import time
import threading

from PIL import ImageGrab
import numpy as np
import cv2

from core import Mobj, wrap_run


class Mvlog(Mobj):

    def _pre(self, cmd):
        super(Mvlog, self)._pre(cmd)
        ps = self.conf['params']
        if '-d' in self.optd:
            ps['duration'] = int(self.optd['-d'])
        if '-f' in self.optd:
            ps['fps'] = int(self.optd['-f'])
        self._running = True
        self.mp4 = time.strftime("./output/%m%d%H.mp4", time.localtime())
        self.fps, self.duration = ps['fps'], ps['duration']
        self.n = 0
        x, y, w, h = ps['region']
        self.region = (x, y, w+x, h+y)
        self.vw = cv2.VideoWriter(self.mp4, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (w, h))


    def start(self):
        t = threading.Thread(target = self._run)
        t.start()

    def stop(self):
        self._running = False

    def _run(self):
        self.ts = time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
        sleeps, ot, totals = round(1 / self.fps, 4), 0.0, self.fps*self.duration
        while self._running and self.n < totals:
            self.n += 1
            t1 = time.time()
            im = cv2.cvtColor(np.asarray(ImageGrab.grab(self.region)), cv2.COLOR_RGB2BGR)
            self.vw.write(im)
            if self.n % self.fps == 0:
                print(f'\r录制中: {self.n/totals:3.0%} 回车退出', end='')
            st = sleeps - (time.time() - t1)
            if st > ot:
                time.sleep(st-ot)
                ot = 0.0
            elif st < 0:
                ot = -st
        self.te = time.strftime("%y-%m-%d %H:%M:%S", time.localtime())
        print(f'\n开始：{self.ts}\n结束：{self.te}')

    @wrap_run
    def run(self, cmd):
        i = input('按 g键 并回车 开始录屏:')
        if i == 'g':
            self.start()
            input('等 回车 退出')
            if self._running:
                self.stop()
                time.sleep(1)
