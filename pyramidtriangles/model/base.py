from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping


class DisplayColor(ABC):
    """
    Abstract base class for displayable color.
    """
    @property
    @abstractmethod
    def rgb256(self) -> tuple[int, int, int]:
        """
        Emit an RGB triple in [0-255].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def rgbw256(self) -> tuple[int, int, int, int]:
        """
        Emit an RGBW quadruple in [0-255].
        """
        raise NotImplementedError

    @property
    def hsv(self):
        """
        Returns an HSV representation. Used for HSV show knobs.
        """
        raise NotImplementedError

    @abstractmethod
    def scale(self, factor: float) -> DisplayColor:
        """
        Scales the brightness by a factor in [0,1].
        """
        raise NotImplementedError


class Model(ABC):
    """Abstract base class for simulators."""
    brightness: float

    @abstractmethod
    def activate(self, cells: Iterable['Cell']):
        """
        Called after Pyramid initialization.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop model and cleanup resources."""
        raise NotImplementedError

    @abstractmethod
    def set(self, cell: 'Cell', addr: 'Address', color: DisplayColor):
        """
        Set one pixel to a particular color.

        addr is an Address, except in the case of the simulator it is a cell ID.
        """
        raise NotImplementedError

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
        raise NotImplementedError


def allocate_universes(cells: Iterable['Cell']) -> Mapping[int, list[int]]:
    universes = set()
    for cell in cells:
        universes |= cell.universes

    return {universe.id: [0] * universe.size for universe in universes}
