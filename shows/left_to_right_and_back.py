from color import HSV
from .showbase import ShowBase
from grid import Grid, Direction, sweep
from grid.cell import Direction, Position
from grid import traversal
import time


class LeftToRightAndBack(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 1.0):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        n_rows = self.grid.row_count
        hsv = HSV(0.0, 0.9, .5)

        pix_arr = []
        a_ctr = 0
        for points in traversal.left_to_right(n_rows):
            for (row, col) in points:
                cell_pixels = self.grid.pixels(Position(row=row, col=col), Direction.LEFT_TO_RIGHT)
                b_ctr = 0
                for pixel in cell_pixels:
                    if len(pix_arr) <= a_ctr+b_ctr:
                        pix_arr.append([])
                    pix_arr[a_ctr+b_ctr].append(pixel)
                    b_ctr += 1
            a_ctr += 4
        self.grid.clear()

        while True:

            for i in pix_arr:  # yes, i
                for ii in i:  # yes, ii!
                    ii(hsv)
                self.grid.go()
                hsv.h += .09
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                time.sleep(0.8)

            for i in reversed(pix_arr):
                for ii in reversed(i):
                    ii(hsv)
                self.grid.go()
                hsv.h += .09
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                time.sleep(0.8)
            yield 0.1
