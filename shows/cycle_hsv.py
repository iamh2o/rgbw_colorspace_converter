import time

from color import HSV as hsv
from grid import Grid, every
from .showbase import ShowBase


class CycleHSV(ShowBase):
    def __init__(self, grid: Grid, frame_delay: float = 0.1):
        self.grid = grid
        self.frame_delay = frame_delay
        self.n_cells = len(self.grid)

    def next_frame(self):
        while True:
            ca = hsv(0.0, 0.0, 0.0, True)
            while ca.v < 1.0:
                ca.v += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            while ca.s < 1.0:
                ca.s += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            while ca.h < 1.0:
                ca.h += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

        self.grid.clear()
        time.sleep(3)

        while True:
            ca = hsv(0.0, 0.0, 0.0, False)
            while ca.v < 1.0:
                ca.v += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            while ca.s < 1.0:
                ca.s += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            while ca.h < 1.0:
                ca.h += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            self.grid.clear()
            time.sleep(3)

        while True:
            ca = hsv(0.0, 0.0, 1.0, False)

            while ca.s < 1.0:
                ca.s += 0.0008
                self.grid.set(every, ca)
                self.grid.go()
                time.sleep(.01)
                print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

                while ca.h < 1.0:
                    ca.h += 0.0008
                    self.grid.set(every, ca)
                    self.grid.go()
                    time.sleep(.01)
                    print('CA', ca.hsv, 'RGB', ca.rgb, 'RGBW', ca.rgbw)

            self.grid.clear()
            time.sleep(3)

            yield self.frame_delay
