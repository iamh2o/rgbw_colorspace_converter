from itertools import cycle

from color import HSV
from grid import Coordinate, Grid, Pyramid, every
from .show import Show


class IndexDebug(Show, debug=True):
    def __init__(self, pyramid: Pyramid, frame_delay: float = 0.05):
        self.pyramid = pyramid
        self.frame_delay = frame_delay

    def next_frame(self):
        self.pyramid.clear()
        yield self.frame_delay

        def coordinates(grid: Grid) -> list[Coordinate]:
            return sorted([cell.coordinate for cell in grid.cells],
                          key=lambda c: (c.y, c.x))

        faces = [(face, cycle(coordinates(face)))
                 for face in self.pyramid.faces]
        highest_universe = max(cell.highest_universe.id
                               for cell in self.pyramid.cells)

        while True:
            for face, coordinates in faces:
                face.set(every, HSV(0, 0, 0))

                cell = face[next(coordinates)]
                hue = cell.highest_universe.id / (highest_universe + 1)

                face.set(cell, HSV(hue, 1.0, 0.8))

            yield self.frame_delay
