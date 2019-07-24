import time

from color import HSV as hsv
from grid import TriangleGrid
from .showbase import ShowBase


class CycleHSV(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 0.1):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.tri_grid.cells)
#        from IPython import embed; embed()

    def next_frame(self):

        self.tri_grid.clear()
        time.sleep(3)

        while True:
            ca = hsv(0.0, 0.0, 0.0)
            while ca.v < 1.0:
                ca.v += 0.0008
                self.tri_grid.set_all_cells(ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', ca.hsv)

            while ca.s < 1.0:
                ca.s += 0.0008
                self.tri_grid.set_all_cells(ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', ca.hsv)

            while ca.h < 1.0:
                ca.h += 0.0008
                self.tri_grid.set_all_cells(ca)
                self.tri_grid.go()
                time.sleep(.01)
                print('CA', ca.hsv)

            self.tri_grid.clear()
            time.sleep(3)

            yield self.frame_delay
