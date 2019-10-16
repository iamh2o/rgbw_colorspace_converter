from math import sin, tau

from dudek.HelperFunctions import randColor, gradient_wheel, maxColor
from dudek.triangle import min_max_column, min_max_row
from .showbase import ShowBase


class Waves(ShowBase):
    def __init__(self, trimodel):
        self.tri = trimodel
        self.time = 0
        self.speed = 0.1
        self.color = randColor()
        self.min_x, self.max_x = min_max_column()
        self.min_y, self.max_y = min_max_row()

    def next_frame(self):
        while True:

            for x in range(self.min_x, self.max_x):
                for y in range(self.min_y, self.max_y + 1):
                    att = (sin(tau * (x + self.min_x + self.time) * (y + self.min_y + self.time) / (self.max_y * self.max_x)) + 1) * 0.5
                    self.tri.set_cell((x, y), gradient_wheel(self.color + (x * 10), att))

            self.time += 1

            self.color = (self.color + 5) % maxColor

            yield self.speed
