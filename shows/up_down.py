from color import RGB
from grid import Grid, Orientation, every, pointed
from .showbase import ShowBase


class UpDown(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 2.0):
        self.grid = grid
        self.frame_delay = frame_delay

    def next_frame(self):
        orientation = Orientation.POINT_UP

        while True:
            self.grid.set(every, RGB(0, 0, 0))

            color = (RGB(0, 255, 255)
                     if orientation is Orientation.POINT_UP
                     else RGB(255, 0, 200))
            self.grid.set(pointed(orientation), color)

            self.grid.go()
            orientation = orientation.invert()
            yield self.frame_delay
