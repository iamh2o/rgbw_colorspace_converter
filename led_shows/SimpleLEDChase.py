import random

import led_strip
from color import RGBW
import random as r

class SimpleLEDChase(object):
    def __init__(self, led_strip):
        self.name = "SimpleLEDChase"

        # walk pixels up and downs strip
        self.cells = led_strip
        self.led_strip = led_strip

        self.frame_delay = .3

#        from IPython import embed; embed()

    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """
        cells = self.cells.all_cells()


        led1 = str(r.randrange(len(self.cells.all_cells())))
        print "XC", led1, self.cells.bottom_neighbor(led1)
        df = {"LED1": {
                'lead_cell' : int(led1),
                'following_cell' : int(self.cells.bottom_neighbor(led1))
                }
              }



        while True:
            self.cells.clear()
            print df["LED1"]['lead_cell'], df["LED1"]['following_cell'], len(self.cells.all_cells())
          
            self.cells.set_cell(str(df["LED1"]['lead_cell']), RGBW(255,255,255,255)) 
            self.cells.set_cell(str(df["LED1"]['following_cell']), RGBW(255,0,0,0,False))

 
            if df["LED1"]['lead_cell'] >= len(self.cells.all_cells())+50:
                print "HERE"
                df["LED1"]['lead_cell'] = 2
                df["LED1"]['following_cell'] = 1

            df["LED1"]['lead_cell'] += r.randrange(0,5)
            df["LED1"]['following_cell'] += r.randrange(0,5)   
            
#            if df["LED1"]['lead_cell'] > 63:
#                df["LED1"]['lead_cell'] = 1
#            if df["LED1"]['following_cell'] > 63:
#                df["LED1"]['following_cell'] = 1
            # then wait to draw the next frame
            yield self.frame_delay
