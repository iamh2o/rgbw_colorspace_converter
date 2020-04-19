from color import HSV
from .show import Show
from grid import Grid, Pyramid, left_to_right


class LeftToRight(Show):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 0.2):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

    def next_frame(self):
        hsv = HSV(0.5, 0.2, .75)
#        from IPython import embed; embed()
        pix_arr = []
        a_ctr = 0

        for points in left_to_right(self.grid.geom):
            for pos in points:
                b_ctr = 0
                for pixel in list(self.grid.pixels(pos)):
                    if len(pix_arr) <= a_ctr+b_ctr:
                        pix_arr.append([])
                    pix_arr[a_ctr+b_ctr].append(pixel)
                    pixel(hsv)
                    self.grid.go()
                    b_ctr += 1
            a_ctr += 4

        while True:
            for i in pix_arr:
                for ii in i:
                    print(ii)
                    ii(hsv)
                    self.grid.go()
                yield 0.2

                hsv.h += .1
                if hsv.h >= 1.0:
                    hsv.h = 0.0
                yield self.frame_delay
