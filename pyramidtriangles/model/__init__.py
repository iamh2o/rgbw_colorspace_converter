"""
This package contains models which connect
"""
from __future__ import annotations
from typing import Protocol, runtime_checkable
from collections.abc import Iterable


@runtime_checkable
class DisplayColor(Protocol):
    """
    Duck type for displayable color. Basically a type interface.

    Any color type should implement these methods, which are used for display, configuration, and brightness scaling.
    """
    @property
    def rgb256(self) -> tuple[int, int, int]:
        """
        Emit an RGB triple in [0-255]. Used by the simulator model.
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
    """
    Duck type for any kind of model. Basically a type interface.

    Any model type should implement these methods, which the ShowRunner uses.
    """
    brightness: float

    def activate(self, cells: Iterable['Cell']) -> None:
        """Called after Pyramid initialization."""
        ...

    def stop(self) -> None:
        """Stop model and cleanup resources."""
        ...

    def set(self, cell: 'Cell', addr: 'Address', color: DisplayColor) -> None:
        """
        Set one pixel to a particular color.

        sACN uses the address. The simulator uses the cell.
        """
        ...

    def go(self) -> None:
        """Flush all buffered data out to devices."""
        ...
