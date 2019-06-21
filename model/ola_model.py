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


def keystoint(x):                        
    return {int(k): v for k, v in x.items()}

# what should we do this callback?
def callback(state):
    print state

class OLAModel(object):
    def __init__(self, max_dmx, universe=0,model_json=None):
        # XXX any way to check if this is a valid connection?

        self.PANEL_MAP = None
        self.universe = universe
        self._map_panels(model_json)
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()
        #Keys for pixels are integers representing universes, each universe has an array of possible DMX channels
        self.pixels = {0: [0] * max_dmx,
                       1: [0] * max_dmx,
                       2: [0] * max_dmx,
                       3: [0] * max_dmx
                       }

    def _map_panels(self,f):

        # Loads a json file with mapping info describing your pixels.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        #each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]

        ds = None
        with open(f, 'r') as json_file:
            ds = json.load(json_file, object_hook=keystoint) #transform json keys to int()
#        from IPython import embed; embed()

        self.PANEL_MAP = ds

    def __repr__(self):
        return "OLAModel(universe=%d)" % self.universe

    # Model basics

    def cell_ids(self):
        # return PANEL_IDS        
        return self.PANEL_MAP.keys()

    def set_cell(self, cell, color):
        # !!!! BUG TO TRACK DOWN.... cell is coming in as an int....
        #keys to the PANEL_MAP must be strings



        #We are using the device/LED/panel/whatever ID to get the first and following three 
        #DMX address we will be sending our RGBW tuple to
        

#        from IPython import embed; embed()
        # cell is a string like "14b"
        # ignore unmapped cells
        

        cell = int(cell)
#        from IPython import embed; embed()        
        if int(cell) in self.PANEL_MAP:
            
            ux = self.PANEL_MAP[cell][0] 
            ix = self.PANEL_MAP[cell][1] - 1 # dmx is 1-based, python lists are 0-based
            
            self.pixels[ux][ix]   = color.g
            self.pixels[ux][ix+1] = color.r
            self.pixels[ux][ix+2] = color.b
            self.pixels[ux][ix+3] = color.w

    def set_cells(self, cells, color):
        for cell in cells:
            self.set_cell(cell, color)

    def go(self):
        data_to_send= {}
        for ux in self.pixels:
            data = array.array('B')
            data.extend(self.pixels[ux])
            data_to_send[ux] = data
    
        for u in data_to_send:

            self.client.SendDmx(int(u), data_to_send[u], callback)


###WHAT IS THIS
if __name__ == '__main__':
    raise Exception('mysterious code I did not understand so commented out')
#    class RGB(object):
#        def __init__(self, r,g,b):
#            self.r = r
#            self.g = g
#            self.b = b
#        def __str__(self):
#            return "RGB(%d,%d,%d)" % (self.r, self.g, self.b)
#
#    model = OLAModel(128, universe=0)
#
#    model.set_cell('13p', RGB(255,0,0))
#    model.set_cell('16p', RGB(0,0,255))
#    model.go()
#
#    data.extend(self.pixels)
