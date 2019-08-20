from randomcolor import random_color
from .showbase import ShowBase
from grid import Grid, Pyramid, inset


class Warp(ShowBase):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 0.2):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

        # Not sure of the proper formula for this, but allows running on normal or mega triangle.
        self.max_distance = 0
        while self.grid.select(inset(self.max_distance)):
            self.max_distance += 1

    def next_frame(self):
        color = random_color(hue='purple')

        while True:
            for distance in range(self.max_distance):
                self.grid.clear()
                self.grid.set(inset(distance), color)
                self.grid.go()
                yield self.frame_delay
