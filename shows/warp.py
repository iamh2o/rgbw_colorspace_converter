from color import HSV
from .showbase import ShowBase
from grid import TriangleGrid, traversal


class Warp(ShowBase):
    def __init__(self, grid: TriangleGrid, frame_delay: float = 0.2):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        row_count = self.grid.row_count

        while True:
            for points in traversal.concentric(row_count):
                self.grid.clear()

                for (row, column) in points:
                    self.grid.set_cell_by_coordinates(row, column, HSV(.1, .5, .9))

                self.grid.go()
                yield self.frame_delay
