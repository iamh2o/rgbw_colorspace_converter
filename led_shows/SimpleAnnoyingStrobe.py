import random

import led_strip
from color import RGBW
import random
import time

class LEDstrip(object):
    def __init__(self, led_strip):
        self.name = "LEDstrip"
        # walk pixels up and downs strip
        self.cells = led_strip
        self.led_strip = led_strip
        # number of seconds to wait between frames
        self.frame_delay = .05

#        from IPython import embed; embed()
        
    
    def next_frame(self):
#        from IPython import embed; embed()   
#        raise
        print "A"
        a = True
        while (True):
            print ".x"
            if a is True:
                self.led_strip.set_all_cells(RGBW(255,255,25,25))
            else:
                self.led_strip.set_all_cells(RGBW(0,0,0,0))

            if a is True:
                a=False
            else:
                a=True
            yield self.frame_delay
