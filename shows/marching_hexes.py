from .showbase import ShowBase
from color import HSV
from grid import hexagon, pointed_up
import random as rnd
import time


class MarchingHexes(ShowBase):
    def __init__(self, grid, frame_delay=0.1):
        self.grid = grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.grid.cells)

    def next_frame(self):
        hsv = HSV(1.0, 1, 1)

        while True:
            self.grid.clear()

            for cell in self.grid.select(pointed_up):
                self.grid.set(hexagon(cell.position), hsv)
                self.grid.go()
                time.sleep(1)

                hsv.h = 0.0 if hsv.h >= 1.0 else hsv.h + 0.2

            yield self.frame_delay
