from .showbase import ShowBase
from color import HSV
from grid import hexagon, pointed_up
import random as rnd
import time


class MarchingHexes(ShowBase):
    def __init__(self, pyramid, frame_delay=0.1):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

        self.n_cells = len(self.grid.cells)

    def next_frame(self):
        hsv = HSV(1.0, 1, 1)

        while True:
            self.grid.clear()
            up = self.grid.select(pointed_up)
            rnd.shuffle(up)

            for cell in up:
                self.grid.set(hexagon(cell.position), hsv)
                self.grid.go()
                yield 1.0

                hsv.h = 0.0 if hsv.h >= 1.0 else hsv.h + 0.2

            yield self.frame_delay
