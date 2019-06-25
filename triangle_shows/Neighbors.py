import random as r
from color import RGBW


class Neighbors(object):
    def __init__(self, tri_grid):
        self.name = "Neighbors"

        # walk pixels up and downs strip
        self.tri_grid = tri_grid

        self.frame_delay = 0.4

#        from IPython import embed; embed()



    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """


        self.tri_grid.clear()

        cell_n = r.randint(1,len(self.tri_grid.cells)-1)

        while True:
#            from IPython import embed; embed()    
#            self.tri_grid.clear()

            if cell_n > len(self.tri_grid.cells)-1:
                cell_n = 1
            print cell_n
            self.tri_grid.set_cell(self.tri_grid.cells[cell_n].get_id(), RGBW(100,255,100,25)) 
            if cell_n > 4:
                cell_n = cell_n-3 
            else:
                if cell_n < len(self.tri_grid.cells)-2:
                    cell_n = cell_n+2
                else:
                    cell_n = 99
            if self.tri_grid.get_cell_by_id(cell_n).is_up():
                if cell_n < 160:
                    cell_n += 100
                else:
                    cell_n -= 1

            if cell_n in [22, 112,44, 75, 90,188]:
                self.tri_grid.clear()
                cell_n = 1
            cell_n += r.randint(0,9)
            
            yield self.frame_delay
