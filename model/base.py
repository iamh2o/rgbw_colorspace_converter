from abc import ABC, abstractmethod
from color import Color
from grid.cell import Address, Cell
from typing import Iterable, List, Mapping


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def set(self, cell: Cell, addr: Address, color: Color):
        """
        Set one pixel to a particular color.

        addr is an Address, except in the case of the simulator it is a cell ID.
        """
        raise NotImplementedError

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
        raise NotImplementedError


class NullModel(ModelBase):
    """
    Discards all set's and go's.
    """

    def set(self, cell: Cell, addr: Address, color: Color):
        pass

    def go(self):
        pass


def allocate_universes(cells: Iterable[Cell]) -> Mapping[int, List[int]]:
    universes = set()
    for cell in cells:
        universes |= cell.universes

    return {universe.id: [0] * universe.size for universe in universes}
