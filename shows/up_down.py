from color import RGB, HSV
from grid import Grid, Orientation, pointed_up, pointed_down
from .showbase import ShowBase
import time

class UpDown(ShowBase):
    grid: Grid

    def __init__(self, pyramid: Pyramid, frame_delay: float = 2.0):
        self.grid = pyramid.face
        self.frame_delay = frame_delay
        self.up_color = RGB(0, 255, 255)
        self.down_color = RGB(255, 0, 200)



    def set_param(self, name, val):
        if name == 'hue':
            try:
                self.color = random_color(hue=str(val))
            except Exception as e:
                print("Bad Hue Value!", val, e)

        if name == 'speed':
            try:
                self.frame_delay = float(val)
            except Exception as e:
                print("Bad Speed Value!", val)
                
        if name == 'flash':
            try:
                self.grid.set(every, RGB(255, 0, 0))
                self.grid.go()
            except Exception as e:
                print("Bad Hue flash!", val, e)

        if name == "change_primary_hsv":
            try:
                self.up_color = HSV(val[0],val[1],val[2])
            except Exception as e:
                print("Bad HSVColor Values!", val)

        if name == "change_secondary_hsv":
            try:
                self.down_color = HSV(val[0],val[1],val[2])
            except Exception as e:
                print("Bad HSVColor Values!", val)
                



    def next_frame(self):

        ctr = True
        while True:
            if ctr is True:
                self.grid.set(pointed_up, self.up_color)
                self.grid.set(pointed_down, self.down_color)
                ctr = False
            else:
                self.grid.set(pointed_up, self.down_color)
                self.grid.set(pointed_down, self.up_color)
                ctr = True
            self.grid.go()

            yield self.frame_delay
