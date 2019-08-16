from abc import ABC, abstractmethod
from color import Color
from grid.cell import Address, universe_count, universe_size, Cell
from typing import List, Mapping


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def set(self, cell: Cell, addr: Address, color: Color):
        """
        Set one pixel to a particular color.

        addr is an Address, except in the case of the simulator it is a cell ID.
        """

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""


def map_leds(row_count: int) -> Mapping[int, List[int]]:
    count = universe_count(row_count)

    return {i + 1: [0] * universe_size(i + 1) for i in range(count)}
