from color import RGB
from .showbase import ShowBase
from grid import Grid, Direction, sweep


class LeftToRightAndBack(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 1.0):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        fwd = True

        while True:
            direction = Direction.LEFT_TO_RIGHT if fwd else Direction.RIGHT_TO_LEFT
            sequence = sweep(direction, self.grid.row_count)

            for points in sequence:
                self.grid.clear()

                for pos in points:
                    self.grid.set(pos, RGB(255, 255, 25))

                self.grid.go()
                yield self.frame_delay

            fwd = not fwd  # Flips direction
