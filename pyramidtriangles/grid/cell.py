from __future__ import annotations
from collections.abc import Iterable
from enum import IntEnum
from typing import Optional, NamedTuple

from .geom import Address, Coordinate, Geometry, Position, Universe


class Orientation(IntEnum):
    POINT_UP = 1
    POINT_DOWN = -1

    def invert(self) -> Orientation:
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

    def invert(self) -> Direction:
        if self is Direction.LEFT_TO_RIGHT:
            return Direction.RIGHT_TO_LEFT
        elif self is Direction.RIGHT_TO_LEFT:
            return Direction.LEFT_TO_RIGHT
        else:
            return Direction.NATURAL


class Cell(NamedTuple):
    """
    A Cell stores the properties of a "cell" (mini-triangle) within one of
    the panels.
    """

    coordinate: Coordinate
    orientation: Orientation
    addresses: list[Address]
    geom: Geometry
    real: bool

    def pixel_addresses(self, direction: Direction = Direction.LEFT_TO_RIGHT) -> Iterable[Address]:
        return (self.addresses
                if direction.natural_for(self.orientation)
                else reversed(self.addresses))

    @property
    def x(self) -> int:
        return self.coordinate.x

    @property
    def y(self) -> int:
        return self.coordinate.y

    @property
    def position(self) -> Position:
        return self.coordinate.pos(self.geom)

    @property
    def row(self) -> int:
        return self.position.row

    @property
    def col(self) -> int:
        return self.position.col

    @property
    def id(self) -> int:
        # XXX: deprecated; only used for simulator
        return self.position.id

    # TODO(lyra): use Coordinate below instead of Position

    @property
    def above(self) -> Optional[Position]:
        return self.position.adjust(row=-1, col=-1) if self.row > 0 else None

    @property
    def below(self) -> Optional[Position]:
        return self.position.adjust(row=1, col=1) if self.row + 1 < self.geom.rows else None

    @property
    def left(self) -> Optional[Position]:
        return self.position.adjust(col=-1) if self.col > 0 else None

    @property
    def right(self) -> Optional[Position]:
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

    @property
    def universes(self) -> set[Universe]:
        return {a.universe for a in self.addresses}

    @property
    def highest_universe(self) -> Universe:
        return max(self.universes)

    def __hash__(self):
        return hash((Cell, self.position))
