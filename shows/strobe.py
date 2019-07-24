from .showbase import ShowBase
from color import RGB
import time


class Strobe(ShowBase):
    def __init__(self, tri_grid, frame_delay = 0.002):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.tri_grid.get_cells())

    def next_frame(self):

        while True:
            self.tri_grid.clear()
            self.tri_grid.set_all_cells(RGB(200, 5, 5))
            self.tri_grid.go()
            time.sleep(0.02)
            self.tri_grid.set_all_cells(RGB(100, 100, 100))
            self.tri_grid.go()
            time.sleep(0.01)
            self.tri_grid.set_all_cells(RGB(5, 5, 255))
            self.tri_grid.go()
            time.sleep(0.02)
            self.tri_grid.set_all_cells(RGB(100, 100, 100))
            self.tri_grid.go()
            time.sleep(0.01)

            yield self.frame_delay
