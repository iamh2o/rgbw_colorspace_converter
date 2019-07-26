from typing import Iterable, Iterator, List, Tuple

from .grid import row_length


def left_to_right(row_count: int) -> Iterator[List[Tuple[int, int]]]:
    """Generates a left-to-right vertical sequence of coordinates."""

    if not row_count > 0:
        raise ValueError(f'traversal requires row_count({row_count}) > 0')

    # Forward sequence:
    # [[(row-1, 0)],
    #  [(row-2, 0), (row-1, 1)],
    #  [(row-3, 0), (row-2, 1), (row-1, 2)]], ...
    for bottom_column in range(row_length(row_count)):
        row_to_start = row_count - 1 - bottom_column

        coordinates = []
        for curr_column in range(bottom_column + 1):
            curr_row = row_to_start + curr_column
            if not 0 <= curr_row < row_count:
                continue
            if curr_column >= row_length(curr_row + 1):
                continue

            coordinates.append((curr_row, curr_column))

        yield coordinates


def right_to_left(row_count: int) -> Iterator[List[Tuple[int, int]]]:
    """Generates a right-to-left vertical sequence of coordinates."""

    if not row_count > 0:
        raise ValueError(f'traversal requires row_count({row_count}) > 0')

    for bottom_column in reversed(range(row_length(row_count))):
        row_to_start = row_count - 1 - bottom_column

        coordinates = []
        for curr_column in range(bottom_column + 1):
            curr_row = row_to_start + curr_column
            if not 0 <= curr_row < row_count:
                continue
            if curr_column >= row_length(curr_row + 1):
                continue

            coordinates.append((curr_row, curr_column))

        yield coordinates


def concentric(row_count: int) -> Iterator[Iterable[Tuple[int, int]]]:
    """Concentric traversal out to in."""

    if not row_count > 0:
        raise ValueError(f'traversal requires row_count({row_count}) > 0')

    for i in range(row_count // 2):
        bottom_row = row_count - 1 - i
        # Increases 0, 2, 4,...
        left_column = i * 2

        # Accumulate for bottom row
        bottoms = []
        for col in range(left_column, row_length(bottom_row + 1) - left_column):
            bottoms.append((bottom_row, col))

        # Accumulate i-th column of each row
        lefts = []
        # Accumulate (n-i)th column of each row
        rights = []

        for row in range(left_column, bottom_row):
            # Decreases last, last - 2, last - 4,...
            right_column = row_length(row + 1) - 1 - left_column

            if left_column <= right_column:
                lefts.append((row, left_column))
                rights.append((row, right_column))

            if left_column + 1 <= right_column:
                lefts.append((row, left_column + 1))
                rights.append((row, right_column - 1))

        yield set().union(bottoms, lefts, rights)
