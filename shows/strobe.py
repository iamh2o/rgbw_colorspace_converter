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
        self.pri_color 
    

    def set_param(self, name, val):
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

    

    def next_frame(self):
        while True:
            self.grid.clear()
            self.grid.set(every, RGB(255, 5, 5))
            self.grid.go()
            time.sleep(self.frame_delay)

            self.grid.set(every, RGB(100, 100, 100))
            self.grid.go()
            time.sleep(self.frame_delay)

            

            yield self.frame_delay
