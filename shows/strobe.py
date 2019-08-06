import time

from .showbase import ShowBase
from color import RGB
from grid import every


class Strobe(ShowBase):
    def __init__(self, grid, frame_delay=0.02):
        self.grid = grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid._cells)

    def next_frame(self):
        while True:
            self.grid.clear()
            self.grid.set(every, RGB(200, 5, 5))
            self.grid.go()
            time.sleep(0.02)
            self.grid.set(every, RGB(100, 100, 100))
            self.grid.go()
            time.sleep(0.02)
            self.grid.set(every, RGB(5, 5, 255))
            self.grid.go()
            time.sleep(0.02)
            self.grid.set(every, RGB(100, 100, 100))
            self.grid.go()
            time.sleep(0.02)

            yield self.frame_delay
