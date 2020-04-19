from color import HSV
from .show import Show
from grid import Grid, Pyramid, Direction, Position, traversal
from util import choose_random_hsv
import random


class Tendrils(Show):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 1.0):
        self.grid = pyramid.face
        self.frame_delay = frame_delay

    def set_pix(self, xyhsv, col, pix_arr):
        print(xyhsv, col)
        try:
            pixs = pix_arr[xyhsv[0]][xyhsv[1]]
            if type(pixs) is list():
                pass
            else:
                pixs = [pixs]

            for addr in pixs:
                print(addr)
                print(xyhsv[0], xyhsv[1], col)
#                self.grid._model.set(addr, xyhsv[2])
                addr(xyhsv[2])

        except Exception as e:
            print(e)

        xyhsv[0] = xyhsv[0]+1
        xyhsv[1] = xyhsv[1]
        xyhsv[2] = xyhsv[2]
        return(xyhsv)

    def next_frame(self):
        n_rows = self.grid.row_count
        row_len = 21  # row_length(n_rows)
        hsv = HSV(0.0, 0.9, .5)

        pix_rows = 21  # n_rows *  2 -1
        pix_col = 11 * 8  # upfacing cells * 8 LEDs
        # This thing is not recognizing pix_col in the first range method...?!?!?
        pix_arr = [[None for i in range(88)] for j in range(pix_rows)]

        a_ctr = 0
        for points in traversal.left_to_right(self.grid.geom):
            for (row, col) in points:
                cell = self.grid.select(Position(row=row, col=col))
                cell_pixels = self.grid.pixels(
                    Position(row=row, col=col), Direction.LEFT_TO_RIGHT)
                b_ctr = 0
                y_coord = 19-(row*2)+1
                if cell[0].is_down:
                    y_coord += 1
                for pixel in cell_pixels:
                    try:
                        pix_arr[y_coord][a_ctr+b_ctr] = pixel
                    except:
                        print("FAILING MAP")
                    b_ctr += 1
            a_ctr += 4

        self.grid.clear()

        while True:
            (x1, x2, x3, x4) = (random.randint(0, 87), random.randint(
                0, 87), random.randint(0, 87), random.randint(0, 87))
            (hsv1, hsv2, hsv3, hsv4) = (choose_random_hsv(),
                                        choose_random_hsv(), choose_random_hsv(), choose_random_hsv())

            (y1, y2, y3, y4) = (0, 0, 0, 0)
            s1 = [y1, x1, hsv1]
            s2 = [y2, x2, hsv2]
            s3 = [y3, x3, hsv3]
            s4 = [y4, x4, hsv4]

            for ccol in range(0, n_rows*2-1):
                print(ccol)
                s1 = self.set_pix(s1, ccol, pix_arr)
                s2 = self.set_pix(s2, ccol, pix_arr)
                s3 = self.set_pix(s3, ccol, pix_arr)
                s4 = self.set_pix(s4, ccol, pix_arr)
                self.grid.go()
                yield 0.5
            s1[2] = self.inc_hsv_s(s1[2])
            s2[2] = self.inc_hsv_s(s2[2])
            s3[2] = self.inc_hsv_s(s3[2])
            s4[2] = self.inc_hsv_s(s4[2])

            yield self.frame_delay

    def inc_hsv_s(self, hsv):
        hsv.s += 0.04
        if hsv.s >= 1.0:
            hsv.s = 0
        return hsv
