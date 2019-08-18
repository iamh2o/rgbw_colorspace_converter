import logging
from typing import Callable, Iterator, Iterable, List, Mapping, NamedTuple, Union, Type

from color import Color, RGB
from model import ModelBase
from .cell import generate, Address, Cell, Direction, Position
from .geom import Geometry

logger = logging.getLogger('pyramidtriangles')

Location = Union[Position, int]

Query = Callable[['Grid'], Iterable[Cell]]
Selector = Union[Location,
                 Cell,
                 Iterable[Cell],
                 Query]


class Pixel(NamedTuple):
    cell: Cell
    address: Address
    model: Type[ModelBase]

    def set(self, color: Color):
        self.model.set(self.cell, self.address, color)

    def __call__(self, color: Color):
        self.set(color)


class Grid(Mapping[Location, Cell]):
    geom: Geometry
    _model: Type[ModelBase]
    _cells: List[Cell]

    def __init__(self, model: Type[ModelBase], geom: Geometry = Geometry(rows=11)):
        if geom.rows < 1:
            raise ValueError(f'Geometry(rows={geom.rows}) is invalid')

        self.geom = geom
        self._model = model

        cells_by_id = {cell.id: cell
                       for cell in generate(geom).values()}
        self._cells = [cells_by_id[i] for i in range(len(cells_by_id))]

    @property
    def row_count(self) -> int:
        return self.geom.rows

    @property
    def cells(self) -> List[Cell]:
        return list(self._cells)

    def select(self, sel: Selector) -> Iterable[Cell]:
        if isinstance(sel, (int, Position)):
            cells = [self[sel]]
        elif isinstance(sel, Cell):
            cells = [sel]
        elif isinstance(sel, Iterable) and not isinstance(self, str):
            cells = sel
        elif callable(sel):
            cells = sel(self)
        else:
            raise TypeError(f'invalid Cell selector {sel}')

        return cells

    def pixels(self, sel: Selector, direction: Direction = Direction.NATURAL) -> Iterator[Pixel]:
        """
        Yield the settable pixels of one or more cells.
        """

        for cell in self.select(sel):
            for addr in cell.pixel_addresses(direction):
                yield Pixel(cell, addr, self._model)

    def set(self, sel: Selector, color: Color):
        for pixel in self.pixels(sel):
            pixel.set(color)

    def go(self):
        """
        Flush the underlying model (render its current state).
        """
        self._model.go()

    def clear(self, color: Color = RGB(0, 0, 0)):
        self.set(self.cells, color)
        self.go()

    def __getitem__(self, loc: Location) -> Cell:
        cell_id = loc if isinstance(loc, int) else loc.id
        if cell_id < 0:
            raise KeyError(cell_id)

        try:
            cell = self._cells[cell_id]
        except IndexError:
            raise KeyError(cell_id)
        else:
            if isinstance(loc, Position) and loc != cell.position:
                logger.warning('got wrong cell: expected %r, got %r',
                            loc, cell.position)
                raise KeyError(loc)
            return cell

    def __iter__(self):
        return (cell.position for cell in self._cells)

    def __len__(self) -> int:
        return len(self._cells)

    def __repr__(self):
        return f'<{type(self).__name__} rows={self.row_count} {self._model}>'
