from .show import Show
from ..color import HSV
from ..grid import Coordinate, Pyramid


class Roar(Show, disable=True):
    """Simple Demo Show. Move from Top of Triangle To Bottom, lighting each row at a time"""
    def __init__(self, pyramid: Pyramid, frame_delay=0.1):
        self.grid = pyramid.panel
        self.frame_delay = frame_delay

        self.n_cells = len(self.grid.cells)

    def next_frame(self):

        self.grid.clear()

        while True:
            hsv = HSV(1.0, 1, 1)

            for y in range(0, 11):
                for x in range(0, 21):
                    coord = Coordinate(x, y)
                    if coord in self.grid:
                        self.grid.set(coord, hsv)
                self.grid.go()
                yield 1.5

                hsv.h -= 0.08

            yield self.frame_delay
