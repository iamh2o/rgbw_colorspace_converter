from __future__ import annotations
from collections.abc import Iterable, MutableMapping
from itertools import chain
from typing import NamedTuple, Optional

from ..model import Model
from .cell import Cell, Orientation
from .geom import Address, Coordinate, Geometry, Universe
from .grid import Grid

PIXELS_PER_CELL: int = 8
PIXELS_IN_ROW_TURNAROUND: int = 11


class Panel(NamedTuple):
    """
    Panel represents an assembled panel in the pyramid frame.

    A Face contains a set of Panels. Panel isn't expected to be used often outside of that class.
    """

    geom: Geometry
    start: Address

    def cells(self, within: Geometry) -> list[Cell]:
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

    def _cells_in_row(self, within: Geometry, y: int, start: Address) -> list[Cell]:
        row = Coordinate(0, y).pos(self.geom).row

        cells = self._up_pointed_cells_in_row(within, row, y, start)
        last_up_address = cells[-1].addresses[-1]
        first_address_after_gap = last_up_address.range(
            PIXELS_IN_ROW_TURNAROUND)[-1]
        cells.extend(self._down_pointed_cells_in_row(
            within, row, y, first_address_after_gap))

        return cells

    def _up_pointed_cells_in_row(self, within: Geometry, row: int, y: int, start: Address) -> list[Cell]:
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

    def _down_pointed_cells_in_row(self, within: Geometry, row: int, y: int, start: Address) -> list[Cell]:
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


# a spec for Face.build() corresponding to our real full pyramid sides
# [0] one panel at the top, [] nothing in the middle, [0, 4] positions of the bottom two panels
FULL_FACE_SPEC = [[0], [], [0, 4]]


class Face(Grid):
    """
    Face is a side of the overall pyramid. It is a kind of Grid, so it can be used in the same way.

    A face is built from a specification (see `build()`).
    """

    _cells: MutableMapping[Coordinate, Cell]
    panels: list[Panel]
    geom: Geometry

    @classmethod
    def build(cls,
              model: Model,
              spec: list[list[int]],
              start: Address = Address(Universe(1, 1), 4),
              rows_per_panel: int = 11) -> Face:
        """
        Build a Face from a panel placement spec.

        Each item the spec is a list representing a row (of panels), starting from the top.
        [[], [], []]  # represents 3 empty rows

        Adding a position to the list indicates a panel exists in that row at that position.
        [[0], [], [4]]  # represents 3 rows, panel at beginning or first row and a panel at 4th spot of 3rd row.
        """

        overall_geom = Geometry(origin=Coordinate(0, 0),
                                rows=(len(spec) * rows_per_panel))
        panel_rows: list[list[Panel]] = [[] for _ in range(len(spec))]
        addr = start

        # Work row-by-row, panel-by-panel, generating all panels so we can use
        # the offset of the previous to generate the next. Later, we'll filter
        # out ones missing from the spec.
        for r in reversed(range(len(spec))):
            panel_row = panel_rows[r]
            panels_in_row = (r + 1) * 2 - 1

            if r + 1 == len(panel_rows):
                origin = Coordinate(0, 0)
            else:
                leftmost_panel_in_row_below = panel_rows[r + 1][0]
                origin = leftmost_panel_in_row_below.geom.apex.adjust(+1, +1)

            for i in range(panels_in_row):
                geom = Geometry(origin=origin, rows=rows_per_panel)
                panel = Panel(geom=geom, start=addr)

                panel_row.append(panel)

                origin = origin.adjust(x=(geom.width + 1))

                if i in spec[r]:
                    # if this panel is included, update the starting address
                    # of the next panel
                    highest_universe = max(cell.highest_universe
                                           for cell in panel.cells(overall_geom))
                    next_id = highest_universe.id + 1
                    universe = Universe(base=next_id, id=next_id)
                    addr = Address(universe, start.offset)

        # Exclude panels that aren't in the spec
        real_panels = []
        for row_spec, row_panels in zip(spec, panel_rows):
            for i, panel in enumerate(row_panels):
                if i in row_spec:
                    real_panels.append(panel)

        return Face(model, overall_geom, real_panels)

    def __init__(self, model: Model, geom: Geometry, panels: Iterable[Panel]):
        self.model = model
        self.geom = geom
        self.panels = list(panels)
        self._cells = {}

        for panel in self.panels:
            for cell in panel.cells(geom):
                self._cells[cell.coordinate] = cell

    @property
    def cells(self) -> list[Cell]:
        return list(self._cells.values())

    def _cell(self, coordinate: Coordinate) -> Optional[Cell]:
        return self._cells.get(coordinate)

    @property
    def next_address(self) -> Address:
        lowest_addr = min(min(cell.addresses) for cell in self.cells)
        highest_universe = max(cell.highest_universe for cell in self.cells)

        next_id = highest_universe.id + 1
        return Address(Universe(next_id, next_id), lowest_addr.offset)
