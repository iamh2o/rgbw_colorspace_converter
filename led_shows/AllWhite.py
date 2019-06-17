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
        while (True):
            self.led_strip.set_all_cells(RGBW(255,255,25,25))
            yield self.frame_delay
