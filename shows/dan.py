import sheep
from color import HSV

class Dan(object):
    def __init__(self, sheep_sides):
        self.name = 'Dan'
        self.cells = sheep_sides.both
        self.color = HSV(1,1,0)
        self.frame_delay = 0.1

    def next_frame(self):
        while True:
            self.cells.clear()
            if self.color.v <= 0.5:
                self.color.v += 0.1
                self.color.h += 0.1
                self.cells.set_cells(sheep.ALL, self.color)
                yield self.frame_delay
            else:
                self.color.v -= 0.01
                self.color.h -= 0.01
                self.cells.set_cells(sheep.ALL, self.color)
                yield self.frame_delay
                