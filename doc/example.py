import random

import sheep
from color import RGB

class ExampleShow(object):
    def __init__(self, sheep_sides):
        self.name = "ExampleShow"

        # Mirror drawing to both sides of the bus. Can also
        # treat the two sides separately.
        # choices: [both, party, business]
        self.cells = sheep_sides.both

        # color to draw
        self.color = RGB(255,0,0)
        # number of seconds to wait between frames
        self.frame_delay = 1.0

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
        # name will be 'colorR', 'colorG', 'colorB'
        rgb255 = int(val * 255)
        if name == 'colorR':
            self.color.r = rgb255
        elif name == 'colorG':
            self.color.g = rgb255
        elif name == 'colorB':
            self.color.b = rgb255

    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """
        while True:
            # clear whatever was drawn last frame
            self.cells.clear()

            # choose a random panel on the sheep
            panel_id = random.choice(sheep.ALL)

            # set the chosen panel to the current color
            self.cells.set_cell(panel_id, self.color)

            # make the neighboring panels dimmer (80% brightness)
            # first find out all of the neighboring panels
            neighbors = sheep.edge_neighbors(panel_id)

            # make a copy of the color so it's safe to change
            dim_color = self.color.copy()
            dim_color.v = 0.8

            # then set multiple panels in one call
            self.cells.set_cells(neighbors, dim_color)

            # then wait to draw the next frame
            yield self.frame_delay
