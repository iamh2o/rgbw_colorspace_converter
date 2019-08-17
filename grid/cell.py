from enum import IntEnum
from functools import lru_cache
from itertools import chain
from typing import List, Mapping, NamedTuple


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


def row_length(n: int) -> int:
    """Returns count of elements in nth row of equilateral triangle."""
    return n * 2 - 1


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
    def coordinates(self) -> "Position":
        return self.position

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
    def is_up(self) -> bool:
        return self.orientation is Orientation.POINT_UP

    @property
    def is_down(self) -> bool:
        return self.orientation is Orientation.POINT_DOWN

    @property
    def is_left_edge(self) -> bool:
        """Returns True if cell is along the left edge of the greater triangle."""
        return self.col == 0

    @property
    def is_right_edge(self) -> bool:
        """Returns True if cell is along the right edge of the greater triangle."""
        (row, column) = self.position
        return column + 1 == row_length(row + 1)

    @property
    def is_bottom_edge(self) -> bool:
        """Returns True if cell is along the bottom edge of the greater triangle."""
        return self.row + 1 == self.row_count and self.is_up

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


def triangular_number(n: int) -> int:
    """Returns the number of elements in an equilateral triangle of n rows."""
    # Typically the triangle number is (n(n+1))/2 but our triangle has rows of 1, 3, 5...
    return n ** 2


class Position(NamedTuple):
    row: int
    col: int

    @classmethod
    @lru_cache(maxsize=512)
    def from_id(cls, id: int) -> "Position":
        row_below = 1
        while triangular_number(row_below) <= id:
            row_below += 1

        row = row_below - 1
        col = id - triangular_number(row)
        return cls(row, col)

    @property
    def id(self) -> int:
        return triangular_number(self.row) + self.col

    @property
    def x(self) -> int:
        return self.col

    @property
    def y(self) -> int:
        return self.row

    def adjust(self, row: int, col: int) -> "Position":
        return type(self)(self.row + row, self.col + col)


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


def generate(rows: int = 11, start: Address = Address(1, 4)) -> Mapping[Position, Cell]:
    cells = {}
    for row in range(rows - 1, -1, -1):
        row_mapping = mouth(row, start)
        cells.update(row_mapping)

        end_address = max(chain.from_iterable(
            cell.addresses for cell in row_mapping.values()))
        start = end_address.next

    return cells


def mouth(row: int, start: Address) -> Mapping[Position, Cell]:
    up = up_teeth(row, start, row + 1)
    last_up_address = up[max(up)].addresses[-1]
    first_after_gap = last_up_address.range(11)[-1]
    down = down_teeth(row, first_after_gap, row)

    return {**up, **down}


def up_teeth(row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, Cell]:
    cells = {}
    addr = start

    for i in range(length):
        pos = Position(row, i * 2)
        addrs = addr.range(pixels_per_cell)
        cells[pos] = Cell(pos, Orientation.POINT_UP, addrs)

        addr = addrs[-1].next

    return cells


def down_teeth(row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, Cell]:
    cells = {}
    addr = start

    col = length * 2 - 1
    for _ in range(length):
        pos = Position(row, col)
        addrs = addr.range(pixels_per_cell)
        cells[pos] = Cell(pos, Orientation.POINT_DOWN, addrs)

        col -= 2
        addr = addrs[-1].next

    return cells


CELLS = generate()
