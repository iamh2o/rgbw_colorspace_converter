
from color import RGBW


class LeftToRight(object):
    def __init__(self, tri_grid):
        self.name = "LeftToRight"

        # walk pixels up and downs strip
        self.tri_grid = tri_grid

        self.frame_delay = 1.0

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

        xlen = len(self.tri_grid._triangle_grid)
        ylen = len(self.tri_grid._triangle_grid[0])
        x =0
        y = 0
        while True:
            self.tri_grid.clear()

            print "XY", x, y
            if y < ylen:
                for rows in self.tri_grid._triangle_grid:
                    cell = self.tri_grid._triangle_grid[x][y]
                    print "AAA", x , y, rows
                    if cell is None:
                        pass
                    else:
                        self.tri_grid.set_cell_by_cellid(cell.get_id(), RGBW(255,255,25,25))
                    x += 1
                x = 0
                y += 1
            else:
                x = 0
                y = 0
        
        
            yield self.frame_delay
