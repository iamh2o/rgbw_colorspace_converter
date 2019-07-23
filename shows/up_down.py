from .showbase import ShowBase
from color import RGB


class UpDown(ShowBase):
    def __init__(self, tri_grid, frame_delay=2):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        a = "up"

        while True:
            self.tri_grid.clear()

            if a == "up":
                print('up')
                for i in self.tri_grid.cells.up_cells:
                    print("Up", i.id)
                    self.tri_grid.cells.set_cell_by_id(i.id, RGB(0, 255, 255))
            else:
                print('down')
                for i in self.tri_grid.cells.down_cells:
                    print("down", i.id)
                    self.tri_grid.cells.set_cell_by_id(i.id, RGB(255, 0, 200))

            if a == "up":
                a = "down"
            else:
                a = "up"
            self.tri_grid.go()
            yield self.frame_delay
