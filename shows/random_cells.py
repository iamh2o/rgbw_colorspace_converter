from .showbase import ShowBase
from color import RGBW
import random as rnd


class Random(ShowBase):
    def __init__(self, tri_grid, frame_delay = 0.1):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.tri_grid.get_cells())
        from IPython import embed; embed()

    def next_frame(self):
        while True:
            self.tri_grid.clear()
            self.tri_grid.set_cell_by_cellid(rnd.randint(1, self.n_cells-2), RGBW(200, 255, 25, 25))
            self.tri_grid.set_cell_by_cellid(rnd.randint(1, self.n_cells-2), RGBW(200, 10, 25, 25))

            yield self.frame_delay
