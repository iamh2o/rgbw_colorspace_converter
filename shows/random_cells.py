from collections import deque
import random

from .show import Show
from color import RGB
from grid import Cell, Grid, Pyramid


class Random(Show):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay=0.1):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

    def shuffle(self) -> deque[Cell]:
        cells = self.grid.cells
        random.shuffle(cells)

        return deque(cells)

    def next_frame(self):
        cells = self.shuffle()
        while True:
            if len(cells) == 0:
                cells = self.shuffle()

            self.grid.clear()
            self.grid.set(cells.popleft(), RGB(200, 10, 25))

            yield self.frame_delay
