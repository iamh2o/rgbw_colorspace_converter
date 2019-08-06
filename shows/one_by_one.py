from color import RGB
from grid import Grid
from .showbase import ShowBase


class OneByOne(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.9):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        ncells = len(self.grid)

        while True:
            for cell in range(ncells):
                self.grid.clear()

                for pixel in self.grid.pixels(cell):
                    pixel.set(RGB(255, 255, 25))
                    yield self.frame_delay
