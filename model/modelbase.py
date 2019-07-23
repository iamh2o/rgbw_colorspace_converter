from abc import ABC, abstractmethod
from typing import Iterator, Type


# TODO: Maybe just use a function instead of a class.
class PixelBase(ABC):
    @abstractmethod
    def set_color(self, color):
        """Set the color for a pixel."""


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def get_pixels(self, cell_id) -> Iterator[Type[PixelBase]]:
        """Returns iterator for Pixels in a Cell"""

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
