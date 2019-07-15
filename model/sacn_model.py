"""
Model to communicate with Devices listening for sACN DMX data

Pixels are representations of the addressible unit in your object. Cells can have multiple pixels in this model only have one LED each.
"""

import array
import sacn
import time
import json


def keystoint(x):                        
    return {int(k): v for k, v in list(x.items())}

# what should we do this callback?
def callback(state):
    print(state)

class sACN(object):
    def __init__(self, max_dmx, model_json=None):
        # XXX any way to check if this is a valid connection?
        
        self.sender = sacn.sACNsender(bind_address="192.168.1.210", universeDiscovery=False)  # Must supply an IP address to bind to that is in the same subnet as the devices routiung the universes.  Might haave to assign a second IP to the eth adapter to get this to work (this is what I had to do on my mac)
        self.sender.start()
        self.PIXEL_MAP = None
        self.leds = {}  # dictionary which will hold an array of 512 int's for each universe, universes are keys to the arrays.
        self._map_leds(model_json)

        #Keys for LEDs are integers representing universes, each universe has an array of possible DMX channels
        #Pixels are an LED represented by 4 DMX addresses
        
        
    def __del__(self):
        self.sender.stop()  # If the object is destructing, close the sender connection


    def _map_leds(self, f):

        # Loads a json file with mapping info describing your leds.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        #each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]
       #initilizing just 4 universes!!! Need to make this more configurable.                                                       


        ds = None
        with open(f, 'r') as json_file:
            ds = json.load(json_file, object_hook=keystoint) #transform json keys to int()
#        from IPython import embed; embed()

        self.PIXEL_MAP = ds
        
        for i in self.PIXEL_MAP:
            universe = int(self.PIXEL_MAP[i][0])
            if universe not in self.leds.keys():
                self.sender.activate_output(universe)
                self.sender[universe].multicast = True
                self.leds[universe] = [0] * 512

    def __repr__(self):
        raise Exception('What is going on here... universes are no longer a property of the model')
#        return "OLAModel(universe=%d)" % self.universe

    # Model basics

    def pixel_ids(self):
        # return LED_IDS        
        return list(self.PIXEL_MAP.keys())

    def set_pixel(self, pixel, color, cellid=None):

#        from IPython import embed; embed()        
        if pixel in self.PIXEL_MAP:            
            ux = self.PIXEL_MAP[pixel][0] 
            ix = self.PIXEL_MAP[pixel][1] - 1 # dmx is 1-based, python lists are 0-based
            
            self.leds[ux][ix]   = color.g
            self.leds[ux][ix+1] = color.r
            self.leds[ux][ix+2] = color.b
            self.leds[ux][ix+3] = color.w
        else:
            print("WARNING: {0} not in pixel ID MAP".format(pixel))

    def set_pixelss(self, pixels, color):
        for pixel in pixels:
            self.set_pixel(pixel, color)

    def go(self):
        for ux in self.leds:
            self.sender[ux].dmx_data = self.leds[ux]


if __name__ == '__main__':
    raise Exception('mysterious code I did not understand so commented out')

