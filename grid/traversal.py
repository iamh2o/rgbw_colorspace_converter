from typing import Iterator, List, Tuple

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
