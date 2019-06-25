import numpy as np
from color import RGBW


class Sides(object):
    def __init__(self, tri_grid):
        self.name = "Sides"

        # walk pixels up and downs strip
        self.cells = tri_grid

        self.frame_delay = 3


    col = 0
    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """

#        from IPython import embed; embed() 
        self.cells.clear()

        col = 255
        a = "up"
        C = [[255,0,0,0],[0,255,0,0], [0,0,255,0], [120,120,20,20]]
        ctr = 0
        while True:
            self.cells.clear()
#            from IPython import embed; embed()    


            for i in self.cells.get_left_side_cells():
                self.cells.set_cell(i.id, RGBW(C[1][0],C[1][1],C[1][2],C[1][3]))
                
            np.random.shuffle(C)
            for i in self.cells.get_right_side_cells():
                    self.cells.set_cell(i.id, RGBW(C[1][0],C[1][1],C[1][2],C[1][3]))



            np.random.shuffle(C)
            for i in self.cells.get_bottom_side_cells():
                self.cells.set_cell(i.id, RGBW(C[1][0],C[1][1],C[1][2],C[1][3]))

            np.random.shuffle(C)

            yield self.frame_delay
