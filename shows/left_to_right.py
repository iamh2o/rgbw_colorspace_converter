from color import RGB
from .showbase import ShowBase
from grid import TriangleGrid, row_length


class LeftToRight(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        while True:
            self.tri_grid.clear()

            for row in range(self.tri_grid.row_count):
                for column in range(row_length(row)):
                    print(f"column={column} row={row}")

                    cell = self.tri_grid.get_cell_by_coordinates(row, column)
                    self.tri_grid.set_cell_by_id(cell.id, RGB(255, 255, 25))

            yield self.frame_delay
