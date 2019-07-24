import time

from color import RGB
from .showbase import ShowBase
from grid import TriangleGrid, row_length


class LeftToRightAndBack(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        fwd = True
        while True:
            if fwd:
                self.tri_grid.clear()

                for row in range(self.tri_grid.row_count):
                    for column in range(row_length(row)):
                        cell = self.tri_grid.get_cell_by_coordinates(row, column)

                        r = 255
                        g = 0
                        for pixel in self.tri_grid.get_pixels(cell.id):
                            pixel(RGB(r, g, 0))
                            time.sleep(.2)
                            self.tri_grid.go()
                            g += 40
                            r -= 3

                fwd = False

            else:
                for row in reversed(range(self.tri_grid.row_count)):
                    for column in range(row_length(row)):
                        cell = self.tri_grid.get_cell_by_coordinates(row, column)

                        g = 255
                        b = 0
                        for pixel in self.tri_grid.get_pixels(cell.id):
                            pixel(RGB(0, g, b))
                            time.sleep(.2)
                            self.tri_grid.go()
                            g -= 40
                            b += 40
                fwd = True

            yield self.frame_delay
