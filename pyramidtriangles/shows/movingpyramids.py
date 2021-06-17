from . import Show
from ..color import HSV
from ..dudek.triangle import all_left_corners, tri_in_direction, inset_triangles, all_center_corners
from ..grid.cell import Coordinate
from ..util import choose_random_hsv


class MovingPyramids(Show, disable=True):
    def __init__(self, pyramid, frame_delay=.5):
        self.tri = pyramid.face
        self.time = 0
        self.speed = frame_delay
        self.color = choose_random_hsv()

    def next_frame(self):
        while True:
            self.tri.clear()

            self.draw_inset_triangles()

            self.time += 1

            # self.color = (self.color + 2) % maxColor
            self.color.h += .01
            yield self.speed

    def draw_inset_triangles(self):
        for i, corner in enumerate(all_left_corners()):
            x = self.get_offset(12, self.time*2)
            corner = tri_in_direction(corner, 0, x)

            for j, triangle in enumerate(inset_triangles(corner, 12-x)):
                for p in triangle:
                    color = HSV(.2, 1, 1)
                    self.tri.set(Coordinate(*p), color)
                # self.tri.set(map(lambda pair: Coordinate(*pair), triangle), wheel(color))

        for i, corner in enumerate(all_center_corners()):
            x = self.get_offset(12, self.time*2)
            corner = self.push_down_one(tri_in_direction(corner, 3, x-2))

            for j, triangle in enumerate(inset_triangles(corner, x)):
                # color = self.color + (j * 80) + (i * 200)
                color = self.color
                color.s += .2
                self.tri.set(map(lambda pair: Coordinate(*pair), triangle), color)

    @staticmethod
    def push_down_one(coord):
        x, y = coord
        return x-1, y

    @staticmethod
    def get_offset(width, time):
        x = time % (width * 2)
        if x > width:
            x = (width * 2) - x
        return x
