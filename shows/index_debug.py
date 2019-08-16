from color import HSV as hsv
from grid import Grid, every
from .showbase import ShowBase


class IndexDebug(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.05):
        self.grid = grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid)

    def next_frame(self):
        while True:
            for cell in sorted(self.grid.cells):
                universe = max(a.universe for a in cell.addresses)
                hue = 1.0 - (cell.position.row / self.grid.row_count) * 0.9

                self.grid.clear()
                self.grid.set(cell.position, hsv(hue, 0.8, 0.9))
                self.grid.go()
                yield self.frame_delay

            for cell in sorted(self.grid.cells):
                universe = max(a.universe for a in cell.addresses)
                hue = min(0.9, (universe - 1) * 0.1)

                self.grid.set(cell, hsv(hue, 0.8, 0.9))
                self.grid.go()
                yield self.frame_delay
