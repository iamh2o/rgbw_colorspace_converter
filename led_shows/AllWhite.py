import random

import led_strip
from color import RGBW
import random
import time

class AllWhite(object):
    def __init__(self, led_strip):
        self.name = "AllWhite"
        # walk pixels up and downs strip
        self.cells = led_strip
        self.led_strip = led_strip
        # number of seconds to wait between frames
        self.frame_delay = 10


    def next_frame(self):
        ctr = 0
        while True:
            if ctr == 0:
                print "ALL"
                self.led_strip.set_all_cells(RGBW(255,255,255,255))
            elif ctr == 1:
                print "White"
                self.led_strip.set_all_cells(RGBW(0,0,0,255, False))
            elif ctr == 2:
                print "RGB"
                self.led_strip.set_all_cells(RGBW(255,255,255,0))
                
            ctr += 1
            if ctr > 2:
                ctr = 0


            yield self.frame_delay
