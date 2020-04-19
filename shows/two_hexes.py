from .show import Show
from color import HSV
from grid import hexagon
from grid.cell import Position, row_length


class TwoHexes(Show):
    def __init__(self, grid, frame_delay=0.1):
        self.grid = grid
        self.frame_delay = frame_delay

        self.n_cells = len(self.grid.cells)

        from IPython import embed; embed()        
    def next_frame(self):
        row = 11
        while True:
            hsv1 = HSV(1.0, 1, 1)
            hsv2 = HSV(0.5, 1, 1)
            self.grid.clear()

            h1_c = 0
            h2_c = row_length(11)-1
            for i in range (1,12):
                self.grid.clear()
                h1 = hexagon(Position(row=10,col=h1_c))
                h2 = hexagon(Position(row=10,col=h2_c))
                #self.grid.set(h1, hsv1)
                self.grid.set(h2, hsv2)
                self.grid.go()
                yield 5.0
                h1_c += 1
                h2_c -= 1


            yield self.frame_delay
