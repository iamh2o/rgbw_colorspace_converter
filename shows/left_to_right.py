from color import HSV, RGB
from .showbase import ShowBase
from grid import Grid, left_to_right, every
import time
from randomcolor import random_color


class LeftToRight(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 1):
        self.grid = grid
        self.frame_delay = frame_delay
        self.color = random_color(hue=str('blue'))
        


    def set_param(self, name, val):
        if name == 'flash':
            try:
                self.grid.set(every, RGB(255, 0, 0))
                self.grid.go()
            except Exception as e:
                print("Bad Hue flash!", val, e)

        if name == 'speed':
            try:
                self.frame_delay = float(val)
            except Exception as e:
                print("Bad Speed Value!", val)

        if name == "change_primary_hsv":
            try:
#                from IPython import embed; embed() 
                self.color = HSV(val[0],val[1],val[2])
            except Exception as e:
                print("Bad HSVColor Values!", val)


    def next_frame(self):
        row_count = self.grid.row_count

        pix_arr = []
        a_ctr = 0
        for points in left_to_right(row_count):

            for pos in points:
                cell = self.grid[pos]
                b_ctr = 0
                for pixel in list(self.grid.pixels(cell.id)):
                    if len(pix_arr) <= a_ctr+b_ctr:
                        pix_arr.append([])
                    pix_arr[a_ctr+b_ctr].append(pixel)
#                    pixel(self.color)
 #                   self.grid.go()
                    b_ctr += 1
            a_ctr += 4

        while True:
            self.grid.clear()

            for i in pix_arr:
                for ii in i:
                    print(ii)
                    ii(self.color)
                    self.grid.go()
                time.sleep(self.frame_delay)

                self.color.h += .1
                if self.color.h >= 1.0:
                    self.color.h = 0.9
            yield self.frame_delay
