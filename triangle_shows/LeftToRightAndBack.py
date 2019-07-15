
from color import RGBW
import time

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

#        from IPython import embed; embed() 

        xlen = len(self.tri_grid._triangle_grid)
        ylen = len(self.tri_grid._triangle_grid[0])
        x =0
        y = 0
        fwd = True
        pix=0
        while True:

            if fwd is True:
                self.tri_grid.clear()

                if y < ylen:
                    for rows in self.tri_grid._triangle_grid:
                        cell = self.tri_grid._triangle_grid[x][y]

                        if cell is None:
                            pass
                        else:
                            r=255
                            g = 0
                            for pix in range(6):
                                self.tri_grid.set_pixel(cell.get_pixels()[pix], RGBW(r, g, 0, 1), cell.get_id())
                                time.sleep(.2)
                                self.tri_grid.go()
                                g += 40
                                r -= 3
                        x += 1
                    x = 0
                    y += 1

                else:
                    x = 0
                    y = ylen-1
                    fwd = False
            else:

                if y >= 0:
                    for rows in self.tri_grid._triangle_grid:

                        cell = self.tri_grid._triangle_grid[x][y]

                        if cell is None:
                            pass
                        else:
                            g = 255
                            b = 0
                            for pix in range(6):
                                self.tri_grid.set_pixel(cell.get_pixels()[5-pix], RGBW(0, g, b, 1), cell.get_id())
                                time.sleep(.2)
                                self.tri_grid.go()
                                g -=40
                                b += 40
                        x += 1
                        
                    y -= 1
                    x=0
                else:
                    y=0
                    x=0
                    fwd = True

        
            yield self.frame_delay
