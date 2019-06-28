
from color import RGBW


class OneByOne(object):
    def __init__(self, tri_grid):
        self.name = "OneByOne"

        # walk pixels up and downs strip
        self.tri_grid = tri_grid

        self.frame_delay = 0.1

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
        ncells = len(self.tri_grid.cells)
        self.tri_grid.clear()
        cell_n = 0
        col = 0
        while True:
#            from IPython import embed; embed()    
            self.tri_grid.clear()
            self.tri_grid.set_cell(self.tri_grid.cells[cell_n].get_id(), RGBW(col,255,25,25)) 
            
            cell_n += 1

            if cell_n > ncells-1:
                #self.tri_grid.cells.clear()   
                cell_n = 0
            if col == 255:
                col = 0
            yield self.frame_delay
