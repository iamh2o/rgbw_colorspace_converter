from random import shuffle

from color import RGB
from grid import Grid
from .showbase import ShowBase


class OneByOne(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.9):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        while True:
            cells = self.grid.cells
            shuffle(cells)

            for cell in cells:
                self.grid.clear()
                self.grid.set(cell, RGB(255, 255, 25))
                yield self.frame_delay
