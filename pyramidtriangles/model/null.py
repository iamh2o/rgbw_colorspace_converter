from __future__ import annotations
from collections.abc import Iterable

from . import DisplayColor


class NullModel:
    """
    Model that does nothing.

    Useful for initializing a Show that does nothing, developing a web UI, and tests.
    """
    def __repr__(self):
        return self.__name__

    def set(self, cell: 'Cell', addr: 'Address', color: DisplayColor) -> None:
        ...

    def go(self) -> None:
        ...

    def activate(self, cells: Iterable['Cell']) -> None:
        ...

    def stop(self) -> None:
        ...
