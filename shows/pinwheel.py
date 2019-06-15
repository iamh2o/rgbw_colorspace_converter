import sheep
from color import HSV, RGB

class Pinwheel(object):
    def __init__(self, sheep_sides):
        self.name = "Pinwheel"
        self.sheep = sheep_sides.both

        self.speed = 0.08
        self.color = HSV(0, 1.0, 1.0)

    def next_frame(self):
        last_cell = None
        while True:
            for cell in sheep.FRONT_SPIRAL:
                if last_cell:
                    self.sheep.set_cell(last_cell, RGB(0,0,0))
                self.sheep.set_cell(cell, self.color)
                last_cell = cell
                self.color.h = (self.color.h + 0.025) % 1

                yield self.speed
