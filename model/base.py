from abc import ABC, abstractmethod
from color import Color
from grid.cell import Address, universe_count, universe_size
from typing import Callable, List, Mapping

SetColorFunc = Callable[[Color], None]


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def set(self, addr: Address, color: Color):
        """
        Set one pixel to a particular color.
        """

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""


def map_leds(row_count: int) -> Mapping[int, List[int]]:
    count = universe_count(row_count)

    return {i + 1: [0] * universe_size(i + 1) for i in range(count)}
