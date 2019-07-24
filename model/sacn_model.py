"""
Model to communicate with Devices listening for sACN DMX data

Pixels are representations of the addressable unit in your object. Cells can have multiple pixels in this model only
have one LED each.
"""
import json
import logging
from typing import Callable, Iterator

from color import Color
import sacn
from .mapping import PixelMap
from .modelbase import ModelBase

logger = logging.getLogger("pyramidtriangles")


class sACN(ModelBase):
    def __init__(self, model_json: str, pixelmap: PixelMap):
        # XXX any way to check if this is a valid connection?

        # Must supply an IP address to bind to that is in the same subnet as the devices routing the universes.  Might
        # have to assign a second IP to the eth adapter to get this to work (this is what I had to do on my mac)
        self.sender = sacn.sACNsender(bind_address="192.168.1.113", universeDiscovery=False)
        self.sender.start()
        self.PIXEL_MAP = None
        # dictionary which will hold an array of 512 int's for each universe, universes are keys to the arrays.
        self.leds = {}
        self._map_leds(model_json)
        self._pixelmap = pixelmap

        # Keys for LEDs are integers representing universes, each universe has an array of possible DMX channels
        # Pixels are an LED represented by 4 DMX addresses

    def __del__(self):
        self.sender.stop()  # If the object is destructing, close the sender connection

    def _map_leds(self, f):
        # Loads a json file with mapping info describing your LEDs.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        # each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]
        # initializing just 4 universes!!! Need to make this more configurable.
        with open(f, 'r') as json_file:
            self.PIXEL_MAP = json.load(json_file, object_hook=lambda d: {int(k): v for (k, v) in d.items()})

        for i in self.PIXEL_MAP:
            universe = int(self.PIXEL_MAP[i][0])
            if universe not in self.leds.keys():
                self.sender.activate_output(universe)
                self.sender[universe].multicast = True
                self.leds[universe] = [0] * 512

    def get_pixels(self, cell_id) -> Iterator[Callable[[Color], None]]:
        for pixel in self._pixelmap[cell_id]:
            if pixel not in self.PIXEL_MAP:
                logger.warning(f'{pixel} not in sACN pixel ID map')

            ux = self.PIXEL_MAP[pixel][0]
            ix = self.PIXEL_MAP[pixel][1] - 1  # dmx is 1-based, python lists are 0-based

            def set_color(color):
                self.leds[ux][ix] = color.r
                self.leds[ux][ix + 1] = color.g
                self.leds[ux][ix + 2] = color.b
                self.leds[ux][ix + 3] = color.w
            yield set_color

    def go(self):
        for ux in self.leds:
            self.sender[ux].dmx_data = self.leds[ux]
