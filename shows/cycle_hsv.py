from .showbase import ShowBase
from color import HSV as hsv
from color1 import HSV as hsv1

import random as rnd
import time

class CycleHSV(ShowBase):
    def __init__(self, tri_grid, frame_delay = 0.1):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.tri_grid.get_cells())
#        from IPython import embed; embed()


    def next_frame(self):

        self.tri_grid.clear()
        time.sleep(3)

        while True:
            self.ca= hsv(0.0,0.0,0.0)
            self.cb= hsv1(0.0,0.0,0.0)
            while self.ca.v < 1.0:
                self.ca.v += 0.0008
                self.tri_grid.set_all_cells(self.ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', self.ca.hsv)

            while self.ca.s < 1.0:
                self.ca.s += 0.0008
                self.tri_grid.set_all_cells(self.ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', self.ca.hsv)
                
            while self.ca.h < 1.0:
                self.ca.h += 0.0008
                self.tri_grid.set_all_cells(self.ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', self.ca.hsv)

            self.tri_grid.clear()
            time.sleep(3)

            while self.cb.v < 1.0:
                self.cb.v += 0.0008
                self.tri_grid.set_all_cells(self.cb)
                self.tri_grid.go()
                time.sleep(.01)
                print('CB', self.cb.hsv)

            while self.cb.s < 1.0:
                self.cb.s += 0.0008
                self.tri_grid.set_all_cells(self.cb)
                self.tri_grid.go()
                time.sleep(.01)
                print('CB', self.cb.hsv)

            while self.cb.h < 1.0:
                self.cb.h += 0.0008
                self.tri_grid.set_all_cells(self.cb)
                self.tri_grid.go()
                time.sleep(.01)
                print('CB', self.cb.hsv)

            self.tri_grid.clear()
            time.sleep(3)

            yield self.frame_delay
