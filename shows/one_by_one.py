from color import RGB
from grid import TriangleGrid
from .showbase import ShowBase


class OneByOne(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 0.9):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        ncells = len(self.tri_grid.cells) - 1
        self.tri_grid.clear()

        while True:
            for cell in range(ncells):
                self.tri_grid.clear()
                print(cell)
                for pixel in self.tri_grid.set_pixels_by_cellid(cell):
                    pixel(RGB(255, 255, 25))

                yield self.frame_delay
