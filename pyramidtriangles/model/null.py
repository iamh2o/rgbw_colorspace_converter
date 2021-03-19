from __future__ import annotations
from collections.abc import Iterable

from ..grid import Address, Cell
from . import DisplayColor


class NullModel:
    """
    Model that does nothing.

    Useful for initializing a Show that does nothing, developing a web UI...
    """
    def __repr__(self):
        return f'{NullModel.__name__}'

    def set(self, cell: Cell, addr: Address, color: DisplayColor):
        pass

    def go(self):
        pass

    def activate(self, cells: Iterable[Cell]):
        pass

    def stop(self):
        pass
