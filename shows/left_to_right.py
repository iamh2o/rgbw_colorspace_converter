from color import HSV
from .showbase import ShowBase
from grid import TriangleGrid, traversal
import time

class LeftToRight(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 0.2):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        row_count = self.tri_grid.row_count

        hsv = HSV(0.5,0.2,.75)
#        from IPython import embed; embed() 
        pix_arr = []
        a_ctr = 0
        for points in traversal.left_to_right(row_count):
 
            for (row, column) in points:
                cell = self.tri_grid.get_cell_by_coordinates(row, column)
                b_ctr = 0
                for pixel in list( self.tri_grid.set_pixels_by_cellid(cell.id) ):
                    if len(pix_arr) <= a_ctr+b_ctr:
                        pix_arr.append([])
                    pix_arr[a_ctr+b_ctr].append(pixel)
                    pixel(hsv)
                    self.tri_grid.go()
                    b_ctr += 1
            a_ctr += 4
 

        while True:
            for i in pix_arr:
                for ii in i:
                    print(ii)
                    ii(hsv)
                    self.tri_grid.go()
                time.sleep(0.2)
            
                hsv.h += .1
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                yield self.frame_delay

