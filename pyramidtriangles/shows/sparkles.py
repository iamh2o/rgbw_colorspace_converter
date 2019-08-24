from random import choices, randint

from ..dudek.HelperClasses import Faders
from ..dudek.HelperFunctions import randColor, oneIn, randColorRange
from .show import Show


class Sparkles(Show):
    def __init__(self, pyramid, frame_delay=0.1):
        self.grid = pyramid.face
        self.faders = Faders(self.grid)
        self.frame_delay = frame_delay
        self.color = randColor()
        self.spark_num = 45

    def next_frame(self):

        for i in range(self.spark_num):
            self.add_new_sparkle()

        while True:
            self.faders.cycle_faders(refresh=True)

            while self.faders.num_faders() < self.spark_num:
                self.add_new_sparkle()

            if oneIn(100):
                self.color = randColorRange(self.color, 30)

            yield self.frame_delay  # random time set in init function

    def add_new_sparkle(self):
        cell = choices(self.grid.cells)
        self.faders.add_fader(color=randColorRange(self.color, 30),
                              pos=(cell[0].coordinate.x, cell[0].coordinate.y),
                              change=1.0 / randint(3, 10),
                              intense=0,
                              growing=True)
