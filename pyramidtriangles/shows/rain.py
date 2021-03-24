from random import randint, choice

from ..color import HSV, RGB
from ..dudek.HelperFunctions import randColorRange, oneIn, upORdown, gradient_wheel
from ..dudek.triangle import tri_nextdoor, min_max_row, min_max_column, TRI_GEN
from ..grid import Coordinate, Pyramid, every
from . import Show


class RainDrop:
    def __init__(self, trimodel, coord):
        self.tri = trimodel
        self.coord = coord
        self.color = randColorRange(1000, 100)  # First number = hue blue

#       from IPython import embed; embed()

    def draw(self):
        if Coordinate(*self.coord) in self.tri:
            color = HSV(.8, 1.0, 1.0)
            self.tri.set(Coordinate(*self.coord), color)

    def move(self, dir):
        for i in range(2):  # Prevents back+forth flicker of drops
            self.coord = tri_nextdoor(self.coord, dir)

    def hit_ground(self, ground_level):
        x, y = self.coord
        return y < ground_level


class Rain(Show, disable=True):
    def __init__(self, pyramid: Pyramid, frame_delay=1.0):
        self.tri = pyramid.face
        self.speed = frame_delay
        self.raindrops: list[RainDrop] = []
        self.freq = randint(3, 10)
        self.rain_dir = self.get_random_rain_dir()
        self.ground_level = self.get_ground_level()
        self.possible_starts = self.get_possible_starts()

    def next_frame(self):
        while True:
            self.tri.clear()

            for i in range(self.freq):  # just a repeat loop to generate a lot of raindrop
                raindrop = RainDrop(self.tri, choice(self.possible_starts))
                self.raindrops.append(raindrop)

            for r in self.raindrops:
                r.draw()
                r.move(self.rain_dir)
                if r.hit_ground(self.ground_level):
                    self.raindrops.remove(r)

            if oneIn(10):
                self.rain_dir = self.get_random_rain_dir()

            if oneIn(10):
                self.freq = upORdown(self.freq, 1, 3, 10)

            if oneIn(20):
                self.lightning()

            yield self.speed

    def lightning(self):
        self.tri.set(every, RGB(*gradient_wheel(300)))  # yellow

    @staticmethod
    def get_random_rain_dir():
        return choice([4, 5])

    @staticmethod
    def get_ground_level():
        min_y, max_y = min_max_row()
        return min_y

    @staticmethod
    def get_possible_starts():
        min_x, max_x = min_max_column()
        min_y, max_y = min_max_row()
        possible_starts = [(x, max_y) for x in range(min_x - TRI_GEN, max_x + TRI_GEN)]
        return possible_starts
