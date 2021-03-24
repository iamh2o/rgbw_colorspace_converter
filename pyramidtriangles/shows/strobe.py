from . import Show
from ..color import RGB
from ..grid import every


class Strobe(Show):
    def __init__(self, pyramid, frame_delay=0.02):
        self.grid = pyramid.face
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid.cells)

    def next_frame(self):
        while True:
            self.grid.clear()
            self.grid.set(every, RGB(200, 5, 5))
            yield self.frame_delay

            self.grid.set(every, RGB(100, 100, 100))
            yield self.frame_delay

            self.grid.set(every, RGB(5, 5, 255))
            yield self.frame_delay

            self.grid.set(every, RGB(100, 100, 100))
            yield self.frame_delay
