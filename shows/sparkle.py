import sheep
from color import RGB

import random

class Sparkle(object):
    def __init__(self, sheep_sides):
        self.name = "Sparkle"
        self.sheep = sheep_sides.both

        self.speed = 0.05
        self.color = RGB(0,255,0)

        # set background to dim white
        self.background = RGB(255,255,255)
        self.background.v = 0.2

        self.neighbor_count = None

    def set_param(self, name, val):
        # name will be 'colorR', 'colorG', 'colorB'
        rgb255 = int(val * 0xff)
        if name == 'colorR':
            self.color.r = rgb255
        elif name == 'colorG':
            self.color.g = rgb255
        elif name == 'colorB':
            self.color.b = rgb255

    def clear(self):
        self.sheep.set_all_cells(self.background)

    def next_frame(self):
        while True:

            color = self.color.copy()
            start = random.choice(sheep.ALL)

            for i in range(random.randint(3,5)):

                neighbors = sheep.edge_neighbors(start)
                if len(neighbors) > 2:
                    edges = random.sample(neighbors, 2)
                else:
                    edges = []

                self.clear()
                color.v = 1.0
                self.sheep.set_cell(start, color)
                color.v = 0.8
                self.sheep.set_cells(edges, color)
                yield self.speed

            self.clear()
            yield 1.0

