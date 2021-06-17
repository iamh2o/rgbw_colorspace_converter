from ..color import RGB
from ..grid import Grid, Pyramid, Orientation, every, pointed
from . import Show


class UpDown(Show):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 2.0):
        self.grid = pyramid.face
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
