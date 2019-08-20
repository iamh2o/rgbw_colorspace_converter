from itertools import chain

from color import HSV as hsv
from grid import Grid, every
from .showbase import ShowBase


class IndexDebug(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.05):
        self.grid = grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid)

    def next_frame(self):
        coordinates = sorted([cell.coordinate for cell in self.grid.cells],
                             key=lambda c: (c.y, c.x))
        highest_universe = max(u.id
                               for u in chain.from_iterable(cell.universes
                                                            for cell in self.grid.cells))

        while True:
            for coord in coordinates:
                cell = self.grid[coord]
                hue = 1.0 - (cell.position.row / self.grid.row_count) * 0.9

                self.grid.clear()
                self.grid.set(cell, hsv(hue, 0.8, 0.9))
                self.grid.go()
                yield self.frame_delay

            self.grid.clear()

            for coord in coordinates:
                cell = self.grid[coord]
                universe = max(u.id for u in cell.universes)
                hue = universe / (highest_universe + 1)

                self.grid.set(cell, hsv(hue, 0.8, 0.9))
                self.grid.go()
                yield self.frame_delay

            self.grid.clear()
