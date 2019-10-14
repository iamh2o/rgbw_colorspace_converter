from randomcolor import random_color
from .showbase import ShowBase
from grid import Grid, Pyramid, inset


class Warp(ShowBase):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 0.2):
        self.grid = pyramid.face
        self.frame_delay = frame_delay
        self.color = random_color(hue='purple')

        # Not sure of the proper formula for this, but allows running on normal or mega triangle.
        self.max_distance = 0
        while self.grid.select(inset(self.max_distance)):
            self.max_distance += 1


    def set_param(self, name, val):
        if name == 'hue':
            try:
                self.color = random_color(hue=str(val))
            except Exception as e:
                print("Bad Hue Value!", val, e)

        if name == 'speed':
            try:
                self.frame_delay = float(val)
            except Exception as e:
                print("Bad Speed Value!", val)

    def next_frame(self):
        while True:
            for distance in range(self.max_distance):
                self.grid.clear()
                self.grid.set(inset(distance), self.color)
                self.grid.go()
                yield self.frame_delay
