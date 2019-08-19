"""
Model to communicate with Devices listening for sACN DMX data

Pixels are representations of the addressable unit in your object. Cells can have multiple pixels in this model only
have one LED each.
"""
import logging
from typing import Union

import sacn
from color import Color
from grid.cell import Address, Cell
from .base import ModelBase, map_leds

logger = logging.getLogger("pyramidtriangles")


class sACN(ModelBase):
    def __init__(self, bind_address: str, row_count: int):
        self.sender = sacn.sACNsender(
            bind_address=bind_address,
            universeDiscovery=False,
        )
        self.sender.start()

        # dictionary which will hold an array of 512 int's for each universe, universes are keys to the arrays.
        self.leds = map_leds(row_count)
        for universe_index in self.leds:
            self.sender.activate_output(universe_index)
            self.sender[universe_index].multicast = True

    def __del__(self):
        self.sender.stop()  # If the object is destructing, close the sender connection

    def set(self, cell: Cell, addr: Address, color: Color):
        try:
            channels = self.leds[addr.universe]
        except KeyError:
            raise IndexError(
                f'attempt to set channel in undefined universe {addr.universe}')

        # our Color tuples have their channels in the same order as sACN
        for i, c in enumerate(color.rgbw):
            try:
                channels[addr.offset + i] = c
            except IndexError:
                raise IndexError(
                    f'internal error in sACN model; failed to assign to universe {addr.universe}, address {addr.offset}')

    def go(self):
        for ux in self.leds:
            self.sender[ux].dmx_data = self.leds[ux]
