"""
Model to communicate with OLA
Based on ola_send_dmx.py

Pixels are representations of the addressable unit in your object. Cells can have multiple pixels in this model only
have one LED each.
"""
import array
import json
import logging
from typing import Iterator

import ola
from .base import ModelBase
from .mapping import PixelMap

logger = logging.getLogger("pyramidtriangles")


# XXX(lyra): this is no longer a valid ModelBase
class OLAModel(ModelBase):
    def __init__(self, max_dmx, model_json: str, pixelmap: PixelMap):
        # XXX any way to check if this is a valid connection?

        self.PIXEL_MAP = None
        self._map_leds(model_json)
        self._pixelmap = pixelmap
        self.wrapper = ola.ClientWrapper()
        self.client = self.wrapper.Client()
        # Keys for LEDs are integers representing universes, each universe has an array of possible DMX channels
        # Pixels are an LED represented by 4 DMX addresses
        
        # initializing just 4 universes!!! Need to make this more configurable.
        self.leds = {
            0: [0] * max_dmx,
            1: [0] * max_dmx,
            2: [0] * max_dmx,
            3: [0] * max_dmx,
            4: [0] * max_dmx
        }

    def _map_leds(self, f):
        # Loads a json file with mapping info describing your leds.
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird
        # each key in the dict is a fixtureUID.
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]
        with open(f, 'r') as json_file:
            self.PIXEL_MAP = json.load(json_file, object_hook=lambda d: {int(k): v for (k, v) in d.items()})

    # Model basics
    def set_pixels_by_cellid(self, cell_id) -> Iterator[SetColorFunc]:
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
        data_to_send = {}
        for ux in self.leds:
            data = array.array('B')
            data.extend(self.leds[ux])
            data_to_send[ux] = data

        for u in data_to_send:
            self.client.SendDmx(int(u), data_to_send[u], lambda state: print(state))
