from color import RGB
from .showbase import ShowBase
from grid import TriangleGrid, row_length


class LeftToRight(ShowBase):
    def __init__(self, tri_grid: TriangleGrid, frame_delay: float = 1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        row_count = self.tri_grid.row_count

        while True:
            # Sequence:
            # [[(row-1, 0)],
            #  [(row-2, 0), (row-1, 1)],
            #  [(row-3, 0), (row-2, 1), (row-1, 2)]], ...
            for bottom_column in range(row_length(row_count)):
                self.tri_grid.clear()
                row_to_start = row_count - 1 - bottom_column

                for curr_column in range(bottom_column + 1):
                    curr_row = row_to_start + curr_column
                    if not 0 <= curr_row < row_count:
                        continue
                    if curr_column >= row_length(curr_row + 1):
                        continue

                    print(f"row={curr_row} column={curr_column}")
                    self.tri_grid.set_cell_by_coordinates(curr_row, curr_column, RGB(255, 255, 25))
                    self.tri_grid.go()

                yield self.frame_delay
