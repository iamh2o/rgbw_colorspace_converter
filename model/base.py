from abc import ABC, abstractmethod
from typing import Iterable, List, Mapping, Tuple
from grid.cell import Cell
from grid.geom import Address


class DisplayColorBase(ABC):
    """
    Abstract base class for displayable color.
    """
    @property
    @abstractmethod
    def rgb256(self) -> Tuple[int, int, int]:
        """
        Called to emit an RGB triple in [0-255].
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def rgbw256(self) -> Tuple[int, int, int, int]:
        """
        Called to emit an RGBW quadruple in [0-255].
        """
        raise NotImplementedError

    @abstractmethod
    def scale(self, factor: float) -> "DisplayColorBase":
        """
        Scales the brightness by a factor in [0,1].
        """
        raise NotImplementedError


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def activate(self, cells: Iterable[Cell]):
        """
        Called after Pyramid initialization.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        """Stop model and cleanup resources."""
        raise NotImplementedError

    @abstractmethod
    def set(self, cell: Cell, addr: Address, color: DisplayColorBase):
        """
        Set one pixel to a particular color.

        addr is an Address, except in the case of the simulator it is a cell ID.
        """
        raise NotImplementedError

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
        raise NotImplementedError


def allocate_universes(cells: Iterable[Cell]) -> Mapping[int, List[int]]:
    universes = set()
    for cell in cells:
        universes |= cell.universes

    return {universe.id: [0] * universe.size for universe in universes}
