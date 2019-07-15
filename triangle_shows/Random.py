
from color import RGBW
import random as rnd

class Random(object):
    def __init__(self, tri_grid):
        self.name = "Random"

        # walk pixels up and downs strip
        self.tri_grid = tri_grid

        self.frame_delay = 0.1

#        from IPython import embed; embed()

        self.n_cells = len(self.tri_grid.get_cells())

    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """


        self.tri_grid.clear()
        while True:
            self.tri_grid.clear()
            self.tri_grid.set_cell_by_cellid(rnd.randint(1, self.n_cells-2), RGBW(200, 255, 25, 25))
            self.tri_grid.set_cell_by_cellid(rnd.randint(1, self.n_cells-2), RGBW(200, 10, 25, 25))

            yield self.frame_delay
