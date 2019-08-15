import logging
from typing import Callable, Iterator, Iterable, List, Mapping, NamedTuple, Union, Type

from color import Color, RGB
from model import ModelBase, SimulatorModel
from .cell import generate, Address, Cell, Direction, Position

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
        # For ease, we set by cell ID in the simulator
        if isinstance(self.model, SimulatorModel):
            self.model.set(self.cell.id, color)
        else:
            self.model.set(self.address, color)

    def __call__(self, color: Color):
        self.set(color)


class Grid(Mapping[Location, Cell]):
    row_count: int
    _model: Type[ModelBase]
    _cells: List[Cell]

    def __init__(self, model: Type[ModelBase], row_count: int = 11):
        if row_count < 1:
            raise ValueError(f'Grid(row_count={row_count}) is invalid')

        self.row_count = row_count
        self._model = model
        self._cells = list(generate(rows=row_count).values())

    @property
    def cells(self) -> List[Cell]:
        return list(self._cells)

    def select(self, sel: Selector) -> Iterable[Cell]:
        if isinstance(sel, (int, Position)):
            cells = [self[sel]]
        elif isinstance(sel, Cell):
            cells = [sel]
        elif isinstance(sel, Iterable):
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
        return self._cells[cell_id]

    def __iter__(self):
        return (cell.position for cell in self._cells)

    def __len__(self) -> int:
        return len(self._cells)

    def __repr__(self):
        return f'<{type(self).__name__} rows={self.row_count} {self._model}>'
