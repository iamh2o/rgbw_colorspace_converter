from __future__ import annotations
from abc import abstractmethod
from collections.abc import Callable, Iterator, Iterable, Mapping
from logging import getLogger
from typing import NamedTuple, Optional, Union

from ..color import HSV
from ..model import DisplayColor, Model
from .cell import Cell, Direction
from .geom import Address, Coordinate, Geometry, Position

logger = getLogger(__name__)

# Types
Location = Union[Coordinate, Position]
Query = Callable[..., Iterable[Cell]]
Selector = Union[Location, Cell, Iterable[Cell], Query]


class Pixel(NamedTuple):
    cell: Cell
    address: Address
    model: Model

    def set(self, color: DisplayColor):
        self.model.set(self.cell, self.address, color)

    def __call__(self, color: DisplayColor):
        self.set(color)


class Grid(Mapping[Location, Cell]):
    """
    Grid represents our triangular cells in a coordinate system.

    A Grid may correspond to a single panel, or an entire side of
    the pyramid.
    """

    geom: Geometry
    model: Model

    @property
    def row_count(self) -> int:
        return self.geom.rows

    @property
    @abstractmethod
    def cells(self) -> list[Cell]:
        raise NotImplementedError

    @abstractmethod
    def _cell(self, coordinate: Coordinate) -> Optional[Cell]:
        raise NotImplementedError

    def select(self, sel: Selector) -> Iterable[Cell]:
        """
        Select cells within the grid.

        The selector `sel` may be a query (like `inset(1)`), a Coordinate,
        a Position, or a list thereof.
        """
        if isinstance(sel, (int, Coordinate, Position)):
            try:
                cells = [self[sel]]
            except KeyError:
                # FIXME(lyra): Face is sparse; coordinates not on a panel
                # don't have a corresponding Cell
                cells = []
        elif isinstance(sel, Cell):
            cells = [sel]
        elif isinstance(sel, Iterable) and not isinstance(self, str):
            cells = list(sel)  # FIXME(lyra)
        elif callable(sel):
            cells = list(sel(self))
        else:
            raise TypeError(f'invalid Cell selector {sel!r}')

        return cells

    def pixels(self, sel: Selector, direction: Direction = Direction.NATURAL) -> Iterator[Pixel]:
        """
        Yield the settable pixels of one or more cells.
        """

        for cell in self.select(sel):
            for addr in cell.pixel_addresses(direction):
                yield Pixel(cell, addr, self.model)

    def set(self, sel: Selector, color: DisplayColor):
        for pixel in self.pixels(sel):
            pixel.set(color)

    def clear(self, color: DisplayColor = HSV(0, 0, 0)):
        self.set(self.cells, color)
        self.go()

    def go(self):
        """
        Flush the underlying model (render its current state).
        """
        self.model.go()

    def _normalize_location(self, loc: Location) -> Coordinate:
        if isinstance(loc, Coordinate):
            return loc
        elif isinstance(loc, Position):
            return Coordinate.from_pos(loc, self.geom)
        else:
            raise TypeError(f'invalid Grid location {loc!r}')

    def __getitem__(self, loc: Location) -> Cell:
        coordinate = self._normalize_location(loc)
        cell = self._cell(coordinate)

        if cell is None:
            if coordinate not in self.geom:
                raise KeyError(f'{coordinate} is not within {self.geom}')

            return Cell(coordinate, None, [], self.geom, real=False)

        return cell

    def __iter__(self):
        return (cell.coordinate for cell in self.cells)

    def __len__(self) -> int:
        return len(self.cells)

    def __repr__(self):
        return f'<{Grid.__name__} rows={self.row_count} {self.model}>'
