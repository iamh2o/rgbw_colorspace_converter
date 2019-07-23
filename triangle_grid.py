from functools import lru_cache
from typing import NamedTuple

from color import RGB


@lru_cache(maxsize=128)
def triangular_number(n):
    """Returns the number of elements in an equilateral triangle of n rows."""
    # Typically the triangle number is (n(n+1))/2 but our triangle has rows of 1, 3, 5...
    return n ** 2


def row_length(n):
    """Returns count of elements in nth row of equilateral triangle."""
    return n * 2 - 1


class TriangleGrid(object):
    def __init__(self, model, row_count):
        if row_count < 1:
            raise ValueError(f'n_rows={row_count} must be positive')

        self._model = model
        self._row_count = row_count

        self._cells = []
        for cell_id in range(0, triangular_number(self.row_count)):
            self._cells.append(TriangleCell(id=cell_id, num_rows=self.row_count))

    @staticmethod
    def coordinates_to_id(row, column):
        """Converts zero-indexed (row, column) coordinates to zero-indexed ID."""
        if row < 0 or column < 0:
            raise ValueError(f'(row={row}, column={column}) must be non-negative')
        return triangular_number(row) + column

    @staticmethod
    @lru_cache(maxsize=512)
    def id_to_coordinates(cell_id):
        """Converts zero-indexed ID to zero-indexed (row, column) coordinates."""
        if cell_id < 0:
            raise ValueError(f'cell_id={cell_id} must be non-negative')

        current_row = 1
        while triangular_number(current_row) <= cell_id:
            current_row += 1
        return current_row - 1, cell_id - triangular_number(current_row - 1)

    def __repr__(self):
        """String representation of object."""
        return f'{__class__.__name__} (n_rows={self.row_count}, model={self._model})'

    @property
    def row_count(self):
        """Returns the number of rows in the triangle."""
        return self._row_count

    @property
    def cells(self):
        return self._cells

    def go(self):
        self._model.go()

    def clear(self):
        """Clears grid by setting all cells to 0."""
        for cell in self._cells:
            self.set_cell_by_id(cell, RGB(0, 0, 0))
        self.go()

    def get_cell_by_coordinates(self, row, column):
        """Returns Cell for (row, column) coordinates, or ValueError if coordinates are out of bounds."""
        if row > self.row_count or column > row_length(self.row_count):
            raise ValueError(f'(row={row}, column={column}) out of bounds for triangle with {self.row_count} rows')

        return self._cells[self.coordinates_to_id(row, column)]

    def get_cell_by_id(self, cell_id):
        return self._cells[cell_id]

    def set_cell_by_id(self, cell_id, color):
        for pixel in self._model.get_pixels(cell_id):
            pixel.set_color(color)

    def get_pixels(self, cell_id):
        return self._model.get_pixels(cell_id)

    # Convenience methods for grabbing useful parts of the triangle grid.
    @property
    def left_side_cells(self):
        return [cell for cell in self._cells if cell.is_left_edge]

    @property
    def right_side_cells(self):
        return [cell for cell in self._cells if cell.is_right_edge]

    @property
    def bottom_side_cells(self):
        return [cell for cell in self._cells if cell.is_bottom_edge]

    @property
    def up_cells(self):
        return [cell for cell in self._cells if cell.is_up]

    @property
    def down_cells(self):
        return [cell for cell in self._cells if cell.is_down]

    # Triangle Grid Helper Functions
    def get_edge_neighbors_by_coord(self, row, col):
        """
        Returns a tuple of (left neighbor, middle neighbor, right neighbor).
        Left neighbor is the edge directly to the left of the cell, regardless of up/down orientation
        Middle neighbor is either the top or bottom neighbor depending where the edge is. the cell knows its up/down orientation
        Right neighbor is the cell immediately to the right.
        """
        cell = self.get_cell_by_coordinates(row, col)

        if cell.is_up:
            left = self.get_cell_by_coordinates(row, col - 1)
            middle = self.get_cell_by_coordinates(row + 1, col)
            right = self.get_cell_by_coordinates(row, col + 1)
            return left, middle, right

        left = self.get_cell_by_coordinates(row, col - 1)
        middle = self.get_cell_by_coordinates(row - 1, col)
        right = self.get_cell_by_coordinates(row, col + 1)
        return left, middle, right

    def get_edge_neighbors_by_cell(self, cell_id):
        return self.get_edge_neighbors_by_coord(*self.id_to_coordinates(cell_id))

    def get_vertex_neighbors_by_coord(self, row, col):
        """Return the neighbors whose vertexes are point to point."""
        cell = self.get_cell_by_coordinates(row, col)

        if cell.is_up:
            left = self.get_cell_by_coordinates(row + 1, col - 1)
            middle = self.get_cell_by_coordinates(row - 1, col)
            right = self.get_cell_by_coordinates(row + 1, col + 1)
            return left, middle, right

        left = self.get_cell_by_coordinates(row - 1, col - 1)
        middle = self.get_cell_by_coordinates(row + 1, col)
        right = self.get_cell_by_coordinates(row - 1, col + 1)
        return left, middle, right

    def get_vertex_neighbors_by_cell(self, cell_id):
        return self.get_vertex_neighbors_by_coord(*self.id_to_coordinates(cell_id))


class TriangleCell(NamedTuple):
    """A Cell contains multiple LED pixels."""
    id: int
    num_rows: int

    @property
    def row(self) -> int:
        """Returns zero-indexed row containing of the cell."""
        (row, column) = TriangleGrid.id_to_coordinates(self.id)
        return row

    @property
    def row_position(self) -> int:
        """Returns zero-indexed position of the cell within a triangle row."""
        (row, column) = TriangleGrid.id_to_coordinates(self.id)
        return column

    @property
    def is_left_edge(self) -> bool:
        """Returns True if cell is along the left edge of the greater triangle."""
        return self.row_position == 0

    @property
    def is_right_edge(self) -> bool:
        """Returns True if cell is along the right edge of the greater triangle."""
        return self.row_position == row_length(self.row + 1) - 1

    @property
    def is_bottom_edge(self) -> bool:
        """Returns True if cell is along the bottom edge of the greater triangle."""
        return self.row + 1 == self.num_rows and self.is_up

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
    def is_up(self) -> bool:
        """Returns True if triangle shaped cell orients with a corner upward."""
        return self.row_position % 2 == 0

    @property
    def is_down(self) -> bool:
        """Returns True if triangle shaped cell orients with a corner downward."""
        return not self.is_up


def make_triangle(model, row_count) -> TriangleGrid:
    """Helper function to build a Triangle with row_count rows."""
    return TriangleGrid(model, row_count)
