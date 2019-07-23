from .showbase import ShowBase
from color import RGB


class OneByOne(ShowBase):
    def __init__(self, tri_grid, frame_delay=0.25):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        ncells = len(self.tri_grid.cells) - 1
        self.tri_grid.clear()
        cell_n = 0

        while True:
            self.tri_grid.clear()
            print(cell_n)
            self.tri_grid.set_cell_by_id(self.tri_grid.cells[cell_n].id, RGB(255, 255, 25))

            if cell_n >= ncells:
                cell_n = -1
            cell_n += 1

            yield self.frame_delay
