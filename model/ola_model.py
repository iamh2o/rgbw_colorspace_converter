"""
Model to communicate with OLA
Based on ola_send_dmx.py

Cells are representations of the addressible unit in your object. Cells in this model only have one LED each.



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
    def __init__(self, max_dmx, model_json=None):
        # XXX any way to check if this is a valid connection?

        self.CELL_MAP = None
        self._map_leds(model_json)
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()
        #Keys for LEDs are integers representing universes, each universe has an array of possible DMX channels
        #Cells have one LED each. Each LED has 4 DMX addresses
        self.leds = {0: [0] * max_dmx,
                       1: [0] * max_dmx,
                       2: [0] * max_dmx,
                       3: [0] * max_dmx
                       }

    def _map_leds(self,f):

        # Loads a json file with mapping info describing your leds.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        #each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]

        ds = None
        with open(f, 'r') as json_file:
            ds = json.load(json_file, object_hook=keystoint) #transform json keys to int()
#        from IPython import embed; embed()

        self.CELL_MAP = ds
#        for i in ds:


            
    def __repr__(self):
        raise Exception('What is going on here... universes are no longer a property of the model')
#        return "OLAModel(universe=%d)" % self.universe

    # Model basics

    def cell_ids(self):
        # return LED_IDS        
        return self.CELL_MAP.keys()

    def set_cell(self, cell, color):
        print "THIS IS THE CELL ID:", cell
#        from IPython import embed; embed()        
        if cell in self.CELL_MAP:            
            ux = self.CELL_MAP[cell][0] 
            ix = self.CELL_MAP[cell][1] - 1 # dmx is 1-based, python lists are 0-based
            
            self.leds[ux][ix]   = color.g
            self.leds[ux][ix+1] = color.r
            self.leds[ux][ix+2] = color.b
            self.leds[ux][ix+3] = color.w
        else:
            print("WARNING: {0} not in cell ID MAP".format(cell))

    def set_cells(self, cells, color):
        for cell in cells:
            self.set_cell(cell, color)

    def go(self):
        data_to_send= {}
        for ux in self.leds:
            data = array.array('B')
            data.extend(self.leds[ux])
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
#    data.extend(self.leds)
