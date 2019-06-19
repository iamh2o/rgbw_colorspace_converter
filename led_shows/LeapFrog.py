import random

import led_strip
from color import RGBW
import random

class LEDstrip(object):
    def __init__(self, led_strip):
        self.name = "LEDstrip"

        # walk pixels up and downs strip
        self.cells = led_strip
        self.led_strip = led_strip
        # color to draw
        self.color = RGBW(0,10,100,0,False)
        # number of seconds to wait between frames
        self.frame_delay = .1

#        from IPython import embed; embed()

    def set_param(self, name, val):
        """
        Receive a command from OSC or other external controller
        'name' is the name of the value being set
        'val' is a floating point number between 0.0 and 1.0
        See 'doc/OSC.md' for details on the named parameters

        This example responds to three color sliders (corresponding
        to R, G and B) in the OSC controller to set the primary
        color of the show.  RGB color values range from 0-255, so
        we must convert the input value.
        """
        #THIS IS WHERE INTERACTIVE BITS GO
        #        self.color.b = RGB(255,0,0, 0, False)
        pass


    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """
        ctr = 0

        #this is a bug... I don't know why this call must be made for the show to work....
        cells = self.cells.all_cells()

        ctr2 = 0
        col_arr = [255,0,0, 0]
        v = 1
        while True:
            
            # clear whatever was drawn last frame
            self.cells.clear()

            # choose a random panel on the led strip
            #panel_id = random.choice(led_strip.ALL)
            #panel_id2 = random.choice(led_strip.ALL)
            panel_id = cells[ctr]
           
            # set the chosen panel to the current color

            print "SET" ,panel_id, self.color.rgb
            self.cells.set_cell(panel_id, self.color)

            #Example of setting random RBG
            self.color.r, self.color.g, self.color.b, self.color.w = col_arr[0:4]
            
            #example of dimming one color smoothly (cant be used with the RGB example above
#            if v <=0.0:
#                v = 1.0
#                self.color.v = v
#            if v > 0.0:
#                self.color.v = v
#                v -= .1


#            print "RESET",self.color.rgb
            random.shuffle(col_arr)

            ctr = ctr+1
            if ctr > 127:
                ctr = 0
            if ctr2 == 2:
                ctr2 = 0
            ctr2 += 1
            # then wait to draw the next frame
            yield self.frame_delay
