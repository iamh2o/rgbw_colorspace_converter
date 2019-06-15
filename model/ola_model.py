"""
Model to communicate with OLA
Based on ola_send_dmx.py

Panels are numbered as strings of the form '12b', indicating
'business' or 'party' side of the sheep

Maps symbolic panel IDs (12b) to DMX ids

"""
import array

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
from ola.ClientWrapper import ClientWrapper

import json

# map symbolic panel IDs to DMX ids
# these are dmx base ids (red channel)
with open('data/dmx_mapping.json', 'r') as f:
    PANEL_MAP = json.load(f)

# PANEL_MAP = {
#     '13p': 1,
#     '16p': 4,
#     '17p': 7,
#     '18p': 10,
#     '19p': 13,
#     '9p' : 16,
#     '8p' : 19,
#     '7p' : 22,
#     '3p' : 25
# }

# what should we do this callback?
def callback(state):
    print state

class OLAModel(object):
    def __init__(self, max_dmx, universe=0):
        # XXX any way to check if this is a valid connection?
        self.universe = universe
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()

        self.pixels = [0] * max_dmx

    def __repr__(self):
        return "OLAModel(universe=%d)" % self.universe

    # Model basics

    def cell_ids(self):
        # return PANEL_IDS        
        return PANEL_MAP.keys()

    def set_cell(self, cell, color):
        # cell is a string like "14b"
        # ignore unmapped cells
        if cell in PANEL_MAP:
            ix = PANEL_MAP[cell] - 1 # dmx is 1-based, python lists are 0-based
            self.pixels[ix]   = color.r
            self.pixels[ix+1] = color.g
            self.pixels[ix+2] = color.b

    def set_cells(self, cells, color):
        for cell in cells:
            self.set_cell(cell, color)

    def go(self):
        data = array.array('B')
        data.extend(self.pixels)
        self.client.SendDmx(self.universe, data, callback)

if __name__ == '__main__':
    class RGB(object):
        def __init__(self, r,g,b):
            self.r = r
            self.g = g
            self.b = b
        def __str__(self):
            return "RGB(%d,%d,%d)" % (self.r, self.g, self.b)

    model = OLAModel(128, universe=0)

    model.set_cell('13p', RGB(255,0,0))
    model.set_cell('16p', RGB(0,0,255))
    model.go()

