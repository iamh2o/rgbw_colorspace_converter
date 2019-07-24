from abc import ABC, abstractmethod
from color import Color
from typing import Callable, Iterator


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def get_pixels(self, cell_id) -> Iterator[Callable[[Color], None]]:
        """Returns iterator for Pixel setting functions in a Cell"""

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
