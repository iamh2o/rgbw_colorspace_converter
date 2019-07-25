from .showbase import ShowBase
from color import RGB
import random as rnd


class Random(ShowBase):
    def __init__(self, tri_grid, frame_delay=0.1):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.tri_grid.cells)

        from IPython import embed; embed()

    def next_frame(self):

        while True:
            self.tri_grid.clear()
            self.tri_grid.set_cell_by_id(rnd.randint(0, self.n_cells - 2), RGB(200, 255, 25))
            self.tri_grid.set_cell_by_id(rnd.randint(0, self.n_cells - 2), RGB(200, 10, 25))

            yield self.frame_delay
