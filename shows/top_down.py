"""Simpe Demo Show. Move from Top of Triangle To Bottom, lighting each row at a time"""

from .showbase import ShowBase
from color import HSV
from grid import hexagon, pointed_up
import random as rnd
import time
from grid.cell import Direction, Position, row_length


class TopDown(ShowBase):
    def __init__(self, grid, frame_delay=0.1):
        self.grid = grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.grid.cells)
#        from IPython import embed; embed()

    def next_frame(self):

        self.grid.clear()

        while True:
            hsv = HSV(1.0, 1, 1)

            for row in range (0,11):
                for col in range (0, row_length(row+1)): ### row+1 b/c the row_length function expects 1 indexed row nums
                    self.grid.set(self.grid.select(Position(row=row, col=col)), hsv)
                self.grid.go()
                time.sleep(1.5)

                hsv.h -= 0.08

            yield self.frame_delay
