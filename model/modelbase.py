from abc import ABC, abstractmethod


class ModelBase(ABC):
    """Abstract base class for simulators."""

    @abstractmethod
    def set_pixel(self, pixel, color, cell_id):
        """Set the color for a pixel."""

    @abstractmethod
    def go(self):
        """Flush all buffered data out to devices."""
