"""Simpe Demo Show. Move from Top of Triangle To Bottom, lighting each row at a time"""

from .showbase import ShowBase
from color import HSV
from grid import Direction, Position, hexagon, pointed_up
import random as rnd
import time


class TopDown(ShowBase):
    def __init__(self, pyramid, frame_delay=1.0):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

    def next_frame(self):
        self.grid.clear()
        decr = 1.0 / self.grid.geom.height

        hsv = HSV(1.0, 1, 1)

        for row in range(self.grid.geom.height):
            self.grid.set(
                (c for c in self.grid.cells if c.row == row), hsv)
            self.grid.go()

            hsv.h -= decr
            yield self.frame_delay
