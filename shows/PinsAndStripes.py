from morph import color_transition
import sheep
from color import HSV, RGB
import time


class PinsAndStripes(object):
    def __init__(self, sheep_sides):
        self.name = "Pinwheel"
        self.sheep = sheep_sides.both
        self.speed = 0.08
        self.color = HSV(0.66, 0.7, 0.9)

    def next_frame(self):
        current_cell = 0
        end_color = self.color.copy()
        end_color.s = 0.2
        while True:
            cells = sheep.FRONT_SPIRAL[current_cell+1:] + sheep.FRONT_SPIRAL[:current_cell]
            self.sheep.set_cell(sheep.FRONT_SPIRAL[current_cell], self.color)
            s = 0.3
            for cell, color in zip(cells, color_transition(end_color, self.color, len(cells))):
                self.sheep.set_cell(cell, color)
            current_cell = (current_cell + 1) % len(sheep.FRONT_SPIRAL)
            yield self.speed

