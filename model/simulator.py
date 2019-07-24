"""
Model to communicate with a Simulator over a TCP socket.

XXX Should this class be able to do range checks on cell ids?
"""
import logging
import socket
import json
from typing import Callable, Iterator

from color import Color
from .modelbase import ModelBase

SIM_DEFAULT = (188, 210, 229)  # BCD2E5, "off" color for simulator
logger = logging.getLogger("pyramidtriangles")


class SimulatorModel(ModelBase):
    def __init__(self, hostname, port=4444, model_json=None):
        self.hostname = hostname
        self.port = port

        self._map_leds(model_json)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostname, self.port))

        # map of cells to be set on the next call to go
        self.dirty = {}

    def __repr__(self):
        return f'{__class__.__name__} (hostname={self.hostname}, port={self.port})'

    # Loaders
    def _map_leds(self, f):
        # Loads a json file with mapping info describing your LEDs.
        # The json file is formatted as a dictionary of numbers each key in the dict is a fixtureUID.
        # Each array that fixtureUID returns is of the format [universeUID, DMXstart#].
        with open(f, 'r') as json_file:
            self.CELL_MAP = json.load(json_file, object_hook=lambda d: {int(k): v for (k, v) in d.items()})

    # Model basics
    def get_pixels(self, cell_id: int) -> Iterator[Callable[[Color], None]]:
        def set_color(color: Color):
            self.set_cell(cell_id, color)
        return iter([set_color])

    def set_cell(self, cell: int, color: Color):
        cell += 1  # Simulator cells not 0 based
        if cell not in self.CELL_MAP:
            raise ValueError(f'Cell {cell} not in CELL_MAP')

        ux = self.CELL_MAP[cell][0]
        ix = self.CELL_MAP[cell][1] - 1
        sim_key = cell
        # The simulator does not care about universes, but does care about UIDs. I'm manufacturing one by joining the
        # Universe and fixture ID into the key.
        self.dirty[sim_key] = color

    def go(self):
        for num in self.dirty:
            r = self.dirty[num].rgb[0]
            g = self.dirty[num].rgb[1]
            b = self.dirty[num].rgb[2]
            msg = f'b {num} {r},{g},{b}\n'

            logger.debug(msg)
            self.sock.send(msg.encode())

        self.dirty = {}
