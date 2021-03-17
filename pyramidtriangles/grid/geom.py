from __future__ import annotations
from functools import lru_cache
from typing import NamedTuple, Union


class Position(NamedTuple):
    """
    Position is (row, column) where the top row is 0, and every row begins with column 0.

    Position(0, 0) is the apex of the triangle.
    """
    row: int
    col: int

    @classmethod
    @lru_cache(maxsize=512)
    def from_id(cls, id: int) -> Position:
        row_below = 1
        while Geometry.triangular_number(row_below) <= id:
            row_below += 1

        row = row_below - 1
        col = id - Geometry.triangular_number(row)
        return Position(row, col)

    @property
    def id(self) -> int:
        return Geometry.triangular_number(self.row) + self.col

    def adjust(self, row: int = 0, col: int = 0) -> Position:
        return Position(self.row + row, self.col + col)

    def __add__(self, other: Position) -> Position:
        if not isinstance(other, Position):
            raise TypeError('invalid: %r + %r' % (self, other))

        return Position(self.row + other.row, self.col + other.col)


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
    @lru_cache(maxsize=2048)
    def from_pos(cls, pos: Position, geom: Geometry) -> Coordinate:
        y = geom.rows - 1 - pos.row
        x = pos.col + y
        return Coordinate(x, y)

    def pos(self, geom: Geometry):
        return Position(geom.rows - 1 - self.y, self.x - self.y)

    def adjust(self, x: int = 0, y: int = 0) -> Coordinate:
        return Coordinate(self.x + x, self.y + y)

    def __str__(self) -> str:
        return f'<{self.x}, {self.y}>'


CHANNELS_PER_PIXEL: int = 4


class Universe(NamedTuple):
    """
    Universe is a DMX universe.

    The base gives the universe ID of the first universe of a panel.
    (This is used for the universe-length arithmetic.)
    """

    base: int
    id: int

    @property
    def size(self) -> int:
        """
        Gives the number of connected channels in each DMX universe.

        Every third universe in a panel is shorter. (Also, not all channels
        are visible; some correspond to the strip segments between rows.)
        """

        return 512 if (self.id - (self.base - 1)) % 3 != 0 else (44 * 4)

    @property
    def next(self) -> Universe:
        return Universe(self.base, self.id + 1)

    def __str__(self) -> str:
        return f'{self.id}'


class Address(NamedTuple):
    """
    Address refers to a cell's DMX address within one of the
    triangle panels.
    """

    universe: Universe
    offset: int

    @classmethod
    def first(cls, universe: Universe = Universe(1, 1), offset: int = 4):
        return Address(universe=universe, offset=offset)

    @property
    def next(self) -> Address:
        next_offset = self.offset + CHANNELS_PER_PIXEL
        if next_offset >= self.universe.size:
            return Address(self.universe.next, 0)

        return Address(self.universe, next_offset)

    def skip(self, n: int) -> Address:
        addr = self
        for _ in range(n):
            addr = addr.next

        return addr

    def range(self, len: int) -> list[Address]:
        addrs = [self]
        for _ in range(len - 1):
            addrs.append(addrs[-1].next)

        return addrs

    def __str__(self) -> str:
        return f'{self.universe}:{self.offset}'


class Geometry(NamedTuple):
    """
    Geometry represents the dimensions of a panel or side of the pyramid.
    """

    origin: Coordinate  # bottom-leftmost cell coordinate
    rows: int

    def __contains__(self, loc: Union[Coordinate, Position]) -> bool:
        if isinstance(loc, Coordinate):
            if loc.x < 0 or loc.y < 0:
                return False
            coord = loc
        elif isinstance(loc, Position):
            if loc.row < 0 or loc.col < 0:
                return False
            coord = Coordinate.from_pos(loc, self)
        else:
            raise TypeError(
                f'`{loc!r} in Geometry` is invalid (not a Coordinate or a Position)')

        # convert to relative coordinate
        rel = Coordinate(coord.x - self.origin.x, coord.y - self.origin.y)
        rel_pos = rel.pos(self)

        try:
            return (0 <= rel_pos.col < self.row_length(rel_pos.row) and
                    0 <= rel_pos.row < self.rows)
        except IndexError:
            return False

    def row_length(self, n: int) -> int:
        if n < 0 or n >= self.rows:
            raise IndexError(f'row {n} out of range ({self.rows} rows total)')

        return (n + 1) * 2 - 1

    def midpoint(self, row: int) -> int:
        length = self.row_length(row)
        return int(length - (length / 2))

    @property
    def height(self) -> int:
        return self.rows

    @property
    def width(self) -> int:
        return self.row_length(self.rows - 1)

    @property
    def cell_count(self) -> int:
        return sum(self.row_length(i) for i in range(self.rows))

    @property
    def apex(self) -> Coordinate:
        """
        The <x, y> coordinate of the top of the triangle.
        """
        return Coordinate(self.origin.x + self.midpoint(self.rows - 1),
                          self.origin.y + (self.rows - 1))

    @staticmethod
    def triangular_number(n: int) -> int:
        """Returns the number of elements in an equilateral triangle of n rows."""
        # Typically the triangle number is (n(n+1))/2 but our triangle has rows of 1, 3, 5...
        return n ** 2
