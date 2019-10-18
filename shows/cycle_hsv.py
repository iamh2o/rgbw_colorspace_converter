from color import HSV as hsv
from grid import Grid, Pyramid, every
from .showbase import ShowBase


class CycleHSV(ShowBase):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 0.025):
        self.grid = pyramid.face
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid)

    def next_frame(self):
        while True:
            ca = hsv(0.0, 0.0, 0.0)
            while ca.v < 1.0:
                ca.v += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                yield self.frame_delay

            while ca.s < 1.0:
                ca.s += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                yield self.frame_delay

            while ca.h < 1.0:
                ca.h += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                yield self.frame_delay

            self.grid.clear()
            yield 3.0

            ca = hsv(0.0, 0.0, 1.0, False)

            while ca.s < 1.0:
                ca.s += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                yield self.frame_delay

                while ca.h < 1.0:
                    ca.h += 0.0008
                    self.grid.set(every, ca)
                    self.grid.go()
                    yield self.frame_delay

            self.grid.clear()
            yield 3.0
