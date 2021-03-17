from __future__ import annotations
from collections.abc import Iterator, Sequence

from .cell import Direction, Position
from .grid import Geometry


def sweep(direction: Direction, geom: Geometry) -> Iterator[Sequence[Position]]:
    """
    Generates a left-to-right or right-to-left vertical sequence of coordinates.
    """

    if direction is Direction.NATURAL:
        raise ValueError('Direction.NATURAL is invalid with traversal.sweep()')

    row_count = geom.rows
    row_lengths = range(geom.row_length(row_count - 1))
    if direction == Direction.RIGHT_TO_LEFT:
        row_lengths = reversed(row_lengths)

    for bottom_column in row_lengths:
        row_to_start = row_count - 1 - bottom_column

        coordinates = []
        for curr_column in range(bottom_column + 1):
            curr_row = row_to_start + curr_column
            if not 0 <= curr_row < row_count:
                continue
            if curr_column >= geom.row_length(curr_row):
                continue

            coordinates.append(Position(curr_row, curr_column))

        yield coordinates


def left_to_right(geom: Geometry) -> Iterator[Sequence[Position]]:
    return sweep(Direction.LEFT_TO_RIGHT, geom)


def right_to_left(geom: Geometry) -> Iterator[Sequence[Position]]:
    return sweep(Direction.RIGHT_TO_LEFT, geom)
