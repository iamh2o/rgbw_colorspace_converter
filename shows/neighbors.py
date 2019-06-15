import sheep
from color import RGB

class Neighbors(object):
    def __init__(self, sheep_sides):
        self.name = "Test neighbors"
        self.sheep = sheep_sides.both

        self.color = RGB(0,255,0)
        self.speed = 1.0

    def set_param(self, name, val):
        # name will be 'colorR', 'colorG', 'colorB'
        rgb255 = int(val * 0xff)
        if name == 'colorR':
            self.color.r = rgb255
        elif name == 'colorG':
            self.color.g = rgb255
        elif name == 'colorB':
            self.color.b = rgb255

    def next_frame(self):
        while True:
            for cellnum in sheep.ALL:
                self.sheep.clear() # unnecessary for it to do a go here?

                col = self.color.copy()
                # set the primary panel to the base color
                self.sheep.set_cell(cellnum, col)

                # set edge neighbors to 80% brightness
                col.v = 0.8
                self.sheep.set_cells(sheep.edge_neighbors(cellnum), col)

                # set vertex neighbors to 20% brightness
                col.v = 0.2
                self.sheep.set_cells(sheep.vertex_neighbors(cellnum), col)

                yield self.speed
