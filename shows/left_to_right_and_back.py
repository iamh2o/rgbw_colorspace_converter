from color import HSV
from .showbase import ShowBase
from grid import Grid, Direction, sweep
from grid.cell import Direction, Position, row_length
from grid import traversal
import time

class LeftToRightAndBack(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 1.0):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        n_rows = self.grid.row_count
        hsv = HSV(0.0,0.9,.5)

        pix_arr = []
        a_ctr = 0
        for points in traversal.left_to_right(n_rows):
            for (row, col) in points:
                cell = self.grid.select(Position(row=row,col=col))
                b_ctr = 0
                for pixel_address in cell[0].pixel_addresses():
                    if len(pix_arr) <= a_ctr+b_ctr:
                        pix_arr.append([])
                    pix_arr[a_ctr+b_ctr].append(pixel_address)
                    b_ctr += 1
            a_ctr += 4
        self.grid.clear()



        while True:

            for i in pix_arr:  #yes, i
                for ii in i:  #yes, ii!
                    self.grid._model.set(ii, hsv) 
                self.grid.go()
                hsv.h += .09
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                time.sleep(0.8)

            for i in reversed(pix_arr):
                for ii in reversed(i):
                    self.grid._model.set(ii, hsv)
                self.grid.go()
                hsv.h += .09
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                time.sleep(0.8)
