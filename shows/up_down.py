from color import RGB
from grid import TriangleGrid
from .showbase import ShowBase


class UpDown(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 2.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        a = "up"

        while True:
            self.tri_grid.clear()

            if a == "up":
                print('up')
                for cell in self.tri_grid.up_cells:
                    print("Up", cell.id)
                    self.tri_grid.set_cell_by_id(cell.id, RGB(0, 255, 255))
            else:
                print('down')
                for cell in self.tri_grid.down_cells:
                    print("down", cell.id)
                    self.tri_grid.set_cell_by_id(cell.id, RGB(255, 0, 200))

            if a == "up":
                a = "down"
            else:
                a = "up"
            self.tri_grid.go()
            yield self.frame_delay
