from color import HSV
from .showbase import ShowBase
from grid import Grid, concentric


class Warp(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.2):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        while True:
            for points in concentric(self.grid.row_count):
                self.grid.clear()

                for pos in points:
                    self.grid.set(pos, HSV(.1, .5, .9))

                self.grid.go()
                yield self.frame_delay
