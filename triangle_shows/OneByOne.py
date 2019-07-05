
from color import RGBW


class OneByOne(object):
    def __init__(self, tri_grid):
        self.name = "OneByOne"

        # walk pixels up and downs strip
        self.tri_grid = tri_grid

        self.frame_delay = 1.5

#        from IPython import embed; embed()


    col = 0
    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """

#        from IPython import embed; embed() 
        ncells = len(self.tri_grid.get_cells())-1
        self.tri_grid.clear()
        cell_n = 0
        col = 0
        while True:

            self.tri_grid.clear()
            print cell_n
            self.tri_grid.set_cell(self.tri_grid.get_cells()[cell_n].get_id(), RGBW(255,255,25,25)) 

            if cell_n >= ncells:
                cell_n = -1
            cell_n += 1

            yield self.frame_delay
