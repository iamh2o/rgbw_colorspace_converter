from __future__ import division

import sheep
from color import RGB

# Roughly alternating sets of panels
A = [1, 3, 4, 7, 9, 12, 16, 18, 19, 21, 22, 24, 27, 30, 33, 35, 37, 39, 42]
B = [2, 5, 6, 8, 11, 13, 14, 15, 17, 20, 23, 25, 26, 28, 29, 31, 32, 34, 36, 40, 41, 43]

class Hypnagogy(object):
    def __init__(self, sheep_sides):
        self.name = "Hypnagogy"
        self.cells = sheep_sides.both

        self.hertz = 30
        self.speed = 1 / self.hertz
        print "Running at %d Hertz (%f delay)" % (self.hertz, self.speed)

        self.color1 = RGB(255,148,0) # orange
        self.color2 = RGB(148,0,255) # purple

    # XXX needs to play better with OSC speed control
    # def set_param(self, name, val):
    #     # name will be 'colorR', 'colorG', 'colorB'
    #     rgb255 = int(val * 0xff)
    #     if name == 'colorR':
    #         self.color.r = rgb255
    #     elif name == 'colorG':
    #         self.color.g = rgb255
    #     elif name == 'colorB':
    #         self.color.b = rgb255

    def next_frame(self):
        while True:
            self.cells.set_cells(A, self.color1)
            self.cells.set_cells(B, self.color2)
            yield self.speed
            self.cells.set_cells(B, self.color1)
            self.cells.set_cells(A, self.color2)
            yield self.speed

