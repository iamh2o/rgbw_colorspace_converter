from __future__ import annotations
from typing import Protocol, runtime_checkable
from collections.abc import Iterable, Mapping


@runtime_checkable
class DisplayColor(Protocol):
    """
    Duck type for displayable color.
    """
    @property
    def rgb256(self) -> tuple[int, int, int]:
        """
        Emit an RGB triple in [0-255].
        """
        return 0, 0, 0

    @property
    def rgbw256(self) -> tuple[int, int, int, int]:
        """
        Emit an RGBW quadruple in [0-255].
        """
        return 0, 0, 0, 0

    @property
    def hsv(self) -> tuple[float, float, float]:
        """
        Returns an HSV representation. Used for HSV show knobs.
        """
        return 0.0, 0.0, 0.0

    def scale(self, factor: float) -> DisplayColor:
        """
        Scales the brightness by a factor in [0,1].
        """
        return self


@runtime_checkable
class Model(Protocol):
    """Duck type for any kind of model."""
    brightness: float

    def activate(self, cells: Iterable['Cell']):
        """
        Called after Pyramid initialization.
        """
        ...

    def stop(self):
        """Stop model and cleanup resources."""
        ...

    def set(self, cell: 'Cell', addr: 'Address', color: DisplayColor):
        """
        Set one pixel to a particular color.

        addr is an Address, except in the case of the simulator it is a cell ID.
        """
        ...

    def go(self):
        """Flush all buffered data out to devices."""
        ...


def allocate_universes(cells: Iterable['Cell']) -> Mapping[int, list[int]]:
    universes = set()
    for cell in cells:
        universes |= cell.universes

    return {universe.id: [0] * universe.size for universe in universes}
