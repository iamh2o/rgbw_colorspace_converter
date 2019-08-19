from enum import IntEnum
from functools import lru_cache
from itertools import chain
from typing import List, Mapping, Optional, NamedTuple

from .geom import Geometry


class Orientation(IntEnum):
    POINT_UP = 1
    POINT_DOWN = -1

    def invert(self) -> "Orientation":
        return Orientation.POINT_UP if self is Orientation.POINT_DOWN else Orientation.POINT_DOWN


class Direction(IntEnum):
    LEFT_TO_RIGHT = 1
    NATURAL = 0
    RIGHT_TO_LEFT = -1

    def natural_for(self, orientation: Orientation) -> bool:
        """
        Returns true if the order of pixel addresses within the cell
        matches the desired direction.
        """

        return self is Direction.NATURAL or self == orientation


class Cell(NamedTuple):
    """
    A Cell stores the properties of a "cell" (mini-triangle) within one of
    the panels.
    """

    position: "Position"
    orientation: Orientation
    addresses: List["Address"]

    row_count = 11  #why is this hard coded? (jem)
    

    def pixel_addresses(self, direction: Direction = Direction.LEFT_TO_RIGHT) -> List["Address"]:
        return (self.addresses
                if direction.natural_for(self.orientation)
                else reversed(self.addresses))

    @property
    def coordinate(self) -> "Coordinate":
        return Coordinate.from_pos(self.position, self.geom)

    @property
    def row(self) -> int:
        return self.position.row

    @property
    def col(self) -> int:
        return self.position.col

    @property
    def id(self) -> int:
        return self.position.id

    @property
    def above(self) -> Optional["Position"]:
        return self.position.adjust(row=-1, col=-1) if self.row > 0 else None

    @property
    def below(self) -> Optional["Position"]:
        return self.position.adjust(row=1, col=1) if self.row + 1 < self.geom.rows else None

    @property
    def left(self) -> Optional["Position"]:
        return self.position.adjust(col=-1) if self.col > 0 else None

    @property
    def right(self) -> Optional["Position"]:
        return self.position.adjust(col=1) if self.col + 1 < self.geom.row_length(self.row) else None

    @property
    def is_up(self) -> bool:
        return self.orientation is Orientation.POINT_UP

    @property
    def is_down(self) -> bool:
        return self.orientation is Orientation.POINT_DOWN

    @property
    def is_edge(self) -> bool:
        return self.is_left_edge or self.is_right_edge or self.is_bottom_edge

    @property
    def is_left_edge(self) -> bool:
        """Returns True if cell is along the left edge of the greater triangle."""
        return self.col == 0

    @property
    def is_right_edge(self) -> bool:
        """Returns True if cell is along the right edge of the greater triangle."""
        return self.col + 1 == self.geom.row_length(self.row)

    @property
    def is_bottom_edge(self) -> bool:
        """Returns True if cell is along the bottom edge of the greater triangle."""
        return self.row + 1 == self.geom.rows and self.is_up

    @property
    def is_top_corner(self) -> bool:
        """Returns True if cell is the top corner of the greater triangle."""
        return self.id == 0

    @property
    def is_right_corner(self) -> bool:
        """Returns True if cell is the right corner of the greater triangle."""
        return self.is_bottom_edge and self.is_right_edge

    @property
    def is_left_corner(self) -> bool:
        """Returns True if cell is the left corner of the greater triangle."""
        return self.is_bottom_edge and self.is_left_edge

    def __hash__(self):
        return hash((type(self), self.position))


class Position(NamedTuple):
    """
    Position is (row, column) where the top row is 0, and every row begins with column 0.

    Position(0, 0) is the apex of the triangle.
    """
    row: int
    col: int

    @classmethod
    @lru_cache(maxsize=512)
    def from_id(cls, id: int) -> "Position":
        row_below = 1
        while Geometry.triangular_number(row_below) <= id:
            row_below += 1

        row = row_below - 1
        col = id - Geometry.triangular_number(row)
        return cls(row, col)

    @property
    def id(self) -> int:
        return Geometry.triangular_number(self.row) + self.col

    def adjust(self, row: int = 0, col: int = 0) -> "Position":
        return type(self)(self.row + row, self.col + col)


class Coordinate(NamedTuple):
    """
    Coordinate is (x, y) such that the left-most, bottom triangle is (0, 0).

    For Coordinate(x, y), the triangle above is Coordinate(x, y + 1), left is Coordinate(x - 1, y), below is
    Coordinate(x, y - 1), and right is Coordinate(x + 1, y).

    Coordinate differs from `Position`. Position(0, 0) is the apex of the whole triangle, whereas Coordinate(0, 0)
    refers to the left corner.

    Coordinates are a different way to spatially reason than Position.
    """
    x: int
    y: int

    @classmethod
    def from_pos(cls, pos: Position, geom: Geometry) -> "Coordinate":
        y = geom.rows - 1 - pos.row
        x = pos.col + y
        return cls(x, y)

    def pos(self, geom: Geometry):
        return Position(geom.rows - 1 - self.y, self.x - self.y)


class Address(NamedTuple):
    """
    Address refers to a cell's DMX address within one of the
    triangle panels.
    """

    universe: int
    offset: int

    @property
    def next(self) -> "Address":
        next_offset = self.offset + 4
        if next_offset >= universe_size(self.universe):
            return Address(self.universe + 1, 0)

        return Address(self.universe, next_offset)

    def skip(self, n: int) -> "Address":
        addr = self
        for _ in range(n):
            addr = addr.next

        return addr

    def range(self, len: int) -> List["Address"]:
        addrs = [self]
        for _ in range(len - 1):
            addrs.append(addrs[-1].next)

        return addrs


def universe_count(row_count: int, start: Address = Address(1, 4)) -> int:
    return row_count  # XXX(lyra): I don't think this is real


def universe_size(universe_id: int) -> int:
    """
    Gives the number of connected channels in each DMX universe.

    Every third universe is shorter. (Also, not all channels are
    visible; some correspond to the strip segments between rows.)
    """

    return 512 if universe_id % 3 != 0 else (44 * 4)


def generate(geom: Geometry, start: Address = Address(1, 4)) -> Mapping[Position, Cell]:
    cells = {}
    for row in range(geom.rows - 1, -1, -1):
        row_mapping = mouth(geom, row, start)
        cells.update(row_mapping)

        end_address = max(chain.from_iterable(
            cell.addresses for cell in row_mapping.values()))
        start = end_address.next

    return cells


def mouth(geom: Geometry, row: int, start: Address) -> Mapping[Position, Cell]:
    up = up_teeth(geom, row, start, row + 1)
    last_up_address = up[max(up)].addresses[-1]
    first_after_gap = last_up_address.range(11)[-1]
    down = down_teeth(geom, row, first_after_gap, row)

    return {**up, **down}


def up_teeth(geom: Geometry, row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, Cell]:
    cells = {}
    addr = start

    for i in range(length):
        pos = Position(row, i * 2)
        addrs = addr.range(pixels_per_cell)
        cells[pos] = Cell(pos, Orientation.POINT_UP, addrs, geom)

        addr = addrs[-1].next

    return cells


def down_teeth(geom: Geometry, row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, Cell]:
    cells = {}
    addr = start

    col = length * 2 - 1
    for _ in range(length):
        pos = Position(row, col)
        addrs = addr.range(pixels_per_cell)
        cells[pos] = Cell(pos, Orientation.POINT_DOWN, addrs, geom)

        col -= 2
        addr = addrs[-1].next

    return cells
