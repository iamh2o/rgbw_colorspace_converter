from abc import ABC, abstractmethod
from color import Color
from typing import Callable, Iterator

SetColorFunc = Callable[[Color], None]


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def set_pixels_by_cellid(self, cell_id) -> Iterator[SetColorFunc]:
        """
        Returns an iterator to set each Pixel's color within the given cell ID.

        Example:
            for pixel in grid.set_pixels_by_cell_id(0):
                pixel(color)
                time.sleep(0.1)
        """

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
