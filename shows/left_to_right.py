from .showbase import ShowBase
from color import RGB


class LeftToRight(ShowBase):
    def __init__(self, tri_grid, frame_delay=1.0):
        self.tri_grid = tri_grid
        self.frame_delay = frame_delay

    def next_frame(self):
        xlen = len(self.tri_grid._triangle_grid)
        ylen = len(self.tri_grid._triangle_grid[0])
        x = 0
        y = 0
        while True:
            self.tri_grid.clear()

            print(f"x={x} y={y}")
            if y < ylen:
                for rows in self.tri_grid._triangle_grid:
                    cell = self.tri_grid._triangle_grid[x][y]
                    print("AAA", x, y, rows)
                    if cell is None:
                        pass
                    else:
                        self.tri_grid.set_cell_by_cellid(cell.get_id(), RGB( 255, 25, 25))
                    x += 1
                x = 0
                y += 1
            else:
                x = 0
                y = 0

            yield self.frame_delay
