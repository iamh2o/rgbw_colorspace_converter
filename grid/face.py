from itertools import chain
from typing import Iterable, Mapping, List, NamedTuple, Optional, Type

from model.base import ModelBase

from .cell import Cell, Orientation
from .geom import Address, Coordinate, Geometry, Position
from .grid import Grid, Location, Pixel, Query, Selector

PIXELS_PER_CELL: int = 8
PIXELS_IN_ROW_TURNAROUND: int = 11


class Panel(NamedTuple):
    """
    Panel represents an assembled panel in the pyramid frame.
    """

    geom: Geometry
    start: Address

    def cells(self, within: Geometry):
        """
        Generate the panel's cells. `within` is the overall Face's geometry.
        """

        cells = []
        addr = self.start

        for y in range(self.geom.rows):
            row_cells = self._cells_in_row(within, y, addr)
            cells.extend(row_cells)

            last_address = max(chain.from_iterable(
                cell.addresses for cell in row_cells))
            addr = last_address.next

        return cells

    def _cells_in_row(self, within: Geometry, y: int, start: Address) -> List[Cell]:
        row = Coordinate(0, y).pos(self.geom).row

        cells = self._up_pointed_cells_in_row(within, row, y, start)
        last_up_address = cells[-1].addresses[-1]
        first_address_after_gap = last_up_address.range(
            PIXELS_IN_ROW_TURNAROUND)[-1]
        cells.extend(self._down_pointed_cells_in_row(
            within, row, y, first_address_after_gap))

        return cells

    def _up_pointed_cells_in_row(self, within: Geometry, row: int, y: int, start: Address) -> List[Cell]:
        cells = []
        addr = start

        offset = int((self.geom.width - self.geom.row_length(row)) / 2)
        for i in range(row + 1):
            coord = Coordinate(self.geom.origin.x + offset + i * 2,
                               self.geom.origin.y + y)
            addrs = addr.range(PIXELS_PER_CELL)

            cells.append(Cell(coord, Orientation.POINT_UP,
                              addrs, within, real=True))

            addr = addrs[-1].next

        return cells

    def _down_pointed_cells_in_row(self, within: Geometry, row: int, y: int, start: Address) -> List[Cell]:
        cells = []
        addr = start

        offset = int((self.geom.width - self.geom.row_length(row)) / 2)
        x = offset + self.geom.row_length(row) - 2
        for _ in range(row):
            coord = Coordinate(self.geom.origin.x + x, self.geom.origin.y + y)
            addrs = addr.range(PIXELS_PER_CELL)

            cells.append(Cell(coord, Orientation.POINT_DOWN,
                              addrs, within, real=True))

            x -= 2
            addr = addrs[-1].next

        return cells


class Face(Grid):
    """
    Face is a side of the overall pyramid.
    """

    _cells: Mapping[Coordinate, Cell]
    panels: List[Panel]
    geom: Geometry

    def __init__(self, model: Type[ModelBase], geom: Geometry, panels: Iterable[Panel]):
        self.model = model
        self.geom = geom
        self.panels = list(panels)
        self._cells = {}

        for panel in self.panels:
            for cell in panel.cells(geom):
                self._cells[cell.coordinate] = cell

    @property
    def cells(self) -> List[Cell]:
        return list(self._cells.values())

    def _cell(self, coordinate: Coordinate) -> Optional[Cell]:
        return self._cells.get(coordinate)
