from typing import Type, Iterable

from grid import Address, Cell
from .base import ModelBase, DisplayColor


class NullModel(ModelBase):
    """
    Model that does nothing.

    Useful for initializing a Show that does nothing, developing a web UI...
    """
    def __repr__(self):
        return f'{__class__.__name__}'

    def set(self, cell: Cell, addr: Address, color: Type[DisplayColor]):
        pass

    def go(self):
        pass

    def activate(self, cells: Iterable[Cell]):
        pass

    def stop(self):
        pass