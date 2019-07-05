
from color import RGBW


class LeftToRightAndBack(object):
    def __init__(self, tri_grid):
        self.name = "LeftToRightAndBack"

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

        from IPython import embed; embed() 

        xlen = len(self.tri_grid._triangle_grid)
        ylen = len(self.tri_grid._triangle_grid[0])
        x =0
        y = 0
        fwd = True
        pix=0
        rev_pix = 5
        while True:

            if fwd is True:
                self.tri_grid.clear()

                print "XY", x, y
                if y < ylen:
                    for rows in self.tri_grid._triangle_grid:
                        cell = self.tri_grid._triangle_grid[x][y]
                        print "AAA", x , y, rows
                        if cell is None:
                            pass
                        else:
                            self.tri_grid.set_pixel(cell.get_pixels()[pix], RGBW(255,0,255,25))
                        x += 1
                    x = 0
                    y += 1
                    if pix == 5:
                        pix = 0
                    else:
                        pix += 1
                else:
                    x = 0
                    y = ylen-1
                    fwd = False
            else:

                if y >= 0:
                    for rows in self.tri_grid._triangle_grid:
                        print "BBB", x , y, rows

                        cell = self.tri_grid._triangle_grid[x][y]
                        print "cCC", x , y, rows
                        if cell is None:
                            pass
                        else:
                            self.tri_grid.set_pixel(cell.get_pixels()[rev_pix], RGBW(255,0,25,255))
                        x += 1
                        
                    y -= 1
                    x=0
                    if rev_pix == 0:
                        rev_pix = 4
                    else:
                        rev_pix -= 1
                else:
                    y=0
                    x=0
                    fwd = True

        
            yield self.frame_delay
