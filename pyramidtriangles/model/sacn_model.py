"""
Model to communicate with Devices listening for sACN DMX data

Pixels are representations of the addressable unit in your object. Cells can have multiple pixels in this model only
have one LED each.
"""
from __future__ import annotations
from logging import getLogger
from collections.abc import Iterable, Mapping

import sacn

from . import DisplayColor

logger = getLogger(__name__)


class sACN:
    def __init__(self, bind_address: str, brightness: float = 1.0):
        self.brightness = brightness
        self.sender = sacn.sACNsender(
            bind_address=bind_address,
            universeDiscovery=False,
        )
        # dict of DMX universe to a list of DMX channels
        self.universes = {}

    def activate(self, cells: Iterable['Cell']):
        """Called after Pyramid initialization."""
        self.sender.start()
 
        # dictionary which will hold an array of 512 ints for each universe, universes are keys to the arrays.
        self.universes = allocate_universes(cells)
        for universe_index in sorted(self.universes):
            logger.debug('Activating sACN universe %d (%d channels)', universe_index, len(self.universes[universe_index]))
            self.sender.activate_output(universe_index)
            self.sender[universe_index].multicast = True

    def stop(self):
        for universe_index in self.universes:
            self.sender.deactivate_output(universe_index)
        self.sender.stop()

    def __del__(self):
        """Model will stop if it is garbage collected."""
        self.stop()

    def set(self, cell, addr: 'Address', color: DisplayColor):
        color = color.scale(self.brightness)
        try:
            channels = self.universes[addr.universe.id]
        except KeyError:
            raise IndexError(f'attempt to set channel in undefined universe {addr.universe.id}')

        # our Color tuples have their channels in the same order as sACN
        for i, c in enumerate(color.rgbw256):
            if not 0 <= c < 256:
                raise ValueError(f"bad RGBW value {c}")
            try:
                channels[addr.offset + i] = c
            except IndexError:
                raise IndexError(
                    f'internal error in sACN model; failed to assign to universe {addr.universe.id}, address {addr.offset}')

    def go(self):
        """
        Sends out DMX data for each universe.

        This could be optimized to just send data that has changed.
        """
        for universe_id, channels in self.universes.items():
            self.sender[universe_id].dmx_data = channels


def allocate_universes(cells: Iterable['Cell']) -> Mapping[int, list[int]]:
    """
    Returns a dict from DMX universe_id -> [[0], [0], [0]] for the size of the universe
    """
    universes = set()
    for cell in cells:
        universes |= cell.universes
    return {u.id: [0] * u.size for u in universes}
