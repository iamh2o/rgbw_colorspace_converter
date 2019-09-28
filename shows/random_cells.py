from typing import Deque
import random

from .showbase import ShowBase
from color import RGB
from grid.cell import Cell


class Random(ShowBase):
    def __init__(self, grid, frame_delay=0.1):
        self.grid = grid
        self.frame_delay = frame_delay

#        from IPython import embed; embed()

    def shuffle(self) -> Deque[Cell]:
        cells = self.grid.cells
        random.shuffle(cells)

        return Deque(cells)

    def set_param(self, name, val):

        #Touch OSC Stuff
        if name == 'speed':
            try:
                self.frame_delay = float(val)
            except Exception as e:
                print("Bad Speed Value!", val)
                

    def next_frame(self):
        cells = self.shuffle()
        while True:
            if len(cells) == 0:
                cells = self.shuffle()

            self.grid.clear()
            self.grid.set(cells.popleft(), RGB(200, 10, 25))

            yield self.frame_delay
