from .showbase import ShowBase
from color import RGB
import time


class LeftToRightAndBack(ShowBase):
    def __init__(self, tri_grid, frame_delay=1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        xlen = len(self.tri_grid._triangle_grid)
        ylen = len(self.tri_grid._triangle_grid[0])
        x = 0
        y = 0
        fwd = True
        pix = 0
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
                            for pixel in self.tri_grid.get_pixels(cell.id):
                                pixel.set_color(RGB(r, g, 0))
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
                            for pixel in self.tri_grid.get_pixels(cell.id):
                                pixel.set_color(RGB(0, g, b))
                                time.sleep(.2)
                                self.tri_grid.go()
                                g -= 40
                                b += 40
                        x += 1
                        
                    y -= 1
                    x = 0
                else:
                    y = 0
                    x = 0
                    fwd = True

            yield self.frame_delay
