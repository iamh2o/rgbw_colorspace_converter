from color import RGB
from .showbase import ShowBase
from grid import TriangleGrid, traversal


class LeftToRightAndBack(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        row_count = self.tri_grid.row_count
        fwd = True

        while True:
            if fwd:
                sequence = traversal.left_to_right(row_count)
            else:
                sequence = traversal.right_to_left(row_count)

            for points in sequence:
                self.tri_grid.clear()

                for (row, column) in points:
                    print(f'row={row} column={column}')
                    self.tri_grid.set_cell_by_coordinates(row, column, RGB(255, 255, 25))

                self.tri_grid.go()
                yield self.frame_delay

            fwd = not fwd  # Flips direction
