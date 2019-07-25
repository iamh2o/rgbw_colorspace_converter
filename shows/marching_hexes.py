from .showbase import ShowBase
from color import HSV
import random as rnd
import time

class MarchingHexes(ShowBase):
    def __init__(self, tri_grid, frame_delay=0.1):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.tri_grid.cells)

    def next_frame(self):
        hsv = HSV(1.0,.9,.5)
        while True:
            self.tri_grid.clear()
            for cell in self.tri_grid.cells:
                if cell.is_up:
                    self.tri_grid.set_cells(self.tri_grid.hexagon_from_btm_cell_by_coords(cell.coordinates[0], cell.coordinates[1]), hsv) 
                    self.tri_grid.go()
                    time.sleep(1)
                    
                    if hsv.h >= 1.0:
                        hsv.h = 0.0
                    else:
                        hsv.h += 0.2

                    

            yield self.frame_delay
