import random

from color import Color, HSV
from grid import Grid, inset
from .showbase import ShowBase


class Stargate(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.25):
        self.grid = grid
        self.frame_delay = frame_delay
        self.hue = 0

    def generate_color(self) -> Color:
        hue = self.hue
        self.hue += random.uniform(0.1, 0.2)
        if self.hue >= 1:
            self.hue -= 1

        return HSV(hue, random.uniform(0.7, 0.9), 0.7)

    def next_frame(self):
        self.grid.clear()
        yield self.frame_delay

        colors = [self.generate_color()]

        while True:
            for distance, color in enumerate(colors):
                self.grid.set(inset(distance), color)

            self.grid.go()
            yield self.frame_delay

            colors.insert(0, self.generate_color())
            if len(colors) > 4:
                colors.pop()
