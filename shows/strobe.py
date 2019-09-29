import time
from randomcolor import random_color

from .showbase import ShowBase
from color import RGB
from grid import every


class Strobe(ShowBase):
    def __init__(self, grid, frame_delay=0.2):
        self.grid = grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid._cells)
        self.pri_color = RGB(0, 255, 255)
        self.secondary_color = RGB(100,100,100)
    

    def set_param(self, name, val):
        if name == 'flash':
            try:
                self.grid.set(every, RGB(255, 0, 0))
                self.grid.go()
            except Exception as e:
                print("Bad Hue flash!", val, e)



        if name == 'hue':
            try:
                self.color = random_color(hue=str(val))
            except Exception as e:
                print("Bad Hue Value!", val, e)
                
        if name == 'speed':
            try:
                self.frame_delay = float(val)
            except Exception as e:
                print("Bad Speed Value!", val)
                
        if name == "change_primary_hsv":
            try:
                self.pri_color = HSV(val[0],val[1],val[2])
            except Exception as e:
                print("Bad HSVColor Values!", val)

        if name == "change_secondary_hsv":
            try:
                self.secondary_color = HSV(val[0],val[1],val[2])
            except Exception as e:
                print("Bad HSVColor Values!", val)

    

    def next_frame(self):
        while True:
            self.grid.clear()
            self.grid.set(every, self.pri_color)
            self.grid.go()
            time.sleep(self.frame_delay)

            self.grid.set(every, self.secondary_color)
            self.grid.go()
            time.sleep(self.frame_delay)

            

            yield self.frame_delay
