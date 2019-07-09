"""
Model to communicate with OLA
Based on ola_send_dmx.py

Pixels are representations of the addressible unit in your object. Cells can have multiple pixels in this model only have one LED each.



"""
import array
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
from ola.ClientWrapper import ClientWrapper
import json


def keystoint(x):                        
    return {int(k): v for k, v in list(x.items())}

# what should we do this callback?
def callback(state):
    print(state)

class OLAModel(object):
    def __init__(self, max_dmx, model_json=None):
        # XXX any way to check if this is a valid connection?

        self.PIXEL_MAP = None
        self._map_leds(model_json)
        self.wrapper = ClientWrapper()
        self.client = self.wrapper.Client()
        #Keys for LEDs are integers representing universes, each universe has an array of possible DMX channels
        #Pixels are an LED represented by 4 DMX addresses
        
        #initilizing just 4 universes!!! Need to make this more configurable.
        self.leds = {0: [0] * max_dmx,
                       1: [0] * max_dmx,
                       2: [0] * max_dmx,
                       3: [0] * max_dmx,
                       4: [0] * max_dmx
                       }

    def _map_leds(self, f):

        # Loads a json file with mapping info describing your leds.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        #each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]

        ds = None
        with open(f, 'r') as json_file:
            ds = json.load(json_file, object_hook=keystoint) #transform json keys to int()
#        from IPython import embed; embed()

        self.PIXEL_MAP = ds
#        for i in ds:


            
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
        data_to_send= {}
        for ux in self.leds:
            data = array.array('B')
            data.extend(self.leds[ux])
            data_to_send[ux] = data

        for u in data_to_send:
            self.client.SendDmx(int(u), data_to_send[u], callback)

        


if __name__ == '__main__':
    raise Exception('mysterious code I did not understand so commented out')

