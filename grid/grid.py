from functools import lru_cache
import logging
from typing import Iterator, List, NamedTuple, Tuple, Type

from color import Color, RGB
from model import ModelBase, SetColorFunc

logger = logging.getLogger('pyramidtriangles')


def triangular_number(n: int) -> int:
    """Returns the number of elements in an equilateral triangle of n rows."""
    # Typically the triangle number is (n(n+1))/2 but our triangle has rows of 1, 3, 5...
    return n ** 2


def row_length(n: int) -> int:
    """Returns count of elements in nth row of equilateral triangle."""
    return n * 2 - 1


class TriangleGrid(object):
    def __init__(self, model: Type[ModelBase], row_count: int):
        if row_count < 1:
            raise ValueError(f'n_rows={row_count} must be positive')

        self._model = model
        self._row_count = row_count

        self._cells = []
        for cell_id in range(0, triangular_number(self.row_count)):
            self._cells.append(TriangleCell(id=cell_id, num_rows=self.row_count))

    @staticmethod
    def coordinates_to_id(row: int, column: int) -> int:
        """Converts zero-indexed (row, column) coordinates to zero-indexed ID."""
        if row < 0 or column < 0:
            raise ValueError(f'(row={row}, column={column}) must be non-negative')
        return triangular_number(row) + column

    @staticmethod
    @lru_cache(maxsize=512)
    def id_to_coordinates(cell_id: int) -> Tuple[int, int]:
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
    def row_count(self) -> int:
        """Returns the number of rows in the triangle."""
        return self._row_count

    @property
    def size(self) -> int:
        """Returns the number of cells in the triangle."""
        return len(self._cells)

    @property
    def cells(self) -> List['TriangleCell']:
        return self._cells

    def go(self):
        self._model.go()

    def clear(self):
        """Clears grid by setting all cells to 0."""
        self.set_all_cells(RGB(0, 0, 0))
        self.go()

    def get_cell_by_coordinates(self, row: int, column: int) -> 'TriangleCell':
        """Returns Cell for (row, column) coordinates, or None if coordinates are out of bounds."""
        if not 0 <= row < self.row_count or not 0 <= column < row_length(row + 1):
            logger.debug(f'(row={row}, column={column}) out of bounds for triangle with {self.row_count} rows')
            return None

        return self._cells[self.coordinates_to_id(row, column)]

    def get_cell_by_id(self, cell_id: int) -> 'TriangleCell':
        """Returns Cell for cell ID, or None if cell ID out of bounds."""
        if not 0 <= cell_id < len(self._cells):
            return None

        return self._cells[cell_id]

    def set_pixels_by_cellid(self, cell_id) -> Iterator[SetColorFunc]:
        """
        Returns an iterator to set each Pixel's color within the given cell ID.

        Example:
            for pixel in grid.set_pixels_by_cell_id(0):
                pixel(color)
                time.sleep(0.1)
        """
        if not 0 <= cell_id < len(self._cells):
            return []

        return self._model.set_pixels_by_cellid(cell_id)

    def set_cell_by_coordinates(self, row: int, column: int, color: Color):
        """Sets cell pixels to color for given coordinates."""
        cell = self.get_cell_by_coordinates(row, column)
        if cell is None:
            logger.warning(f'cell coordinates (row={row}, column={column}) invalid')
            return

        [pixel(color) for pixel in self._model.set_pixels_by_cellid(cell.id)]

    def set_cell_by_id(self, cell_id: int, color: Color):
        """Sets cell pixels to color for given ID."""
        if not 0 <= cell_id < len(self._cells):
            logger.warning(f'cell ID {cell_id} invalid')
            return
        [pixel(color) for pixel in self._model.set_pixels_by_cellid(cell_id)]


    def set_cell(self, cell, color: Color):
        "Set cell pixels to a color"
        if cell is not None:
            if not 0 <= cell.id < len(self._cells):
                logger.warning(f'cell ID {cell_id} invalid')
                return
            [pixel(color) for pixel in self._model.set_pixels_by_cellid(cell.id)]

        
    def set_cells(self, cells: List['TriangleCell'], color: Color):
        "set a list of cells to a color"
        for cell in cells:
            self.set_cell(cell, color)


    def set_all_cells(self, color: Color):
        """Sets all cell to color."""
        for cell in self.cells:
            self.set_cell_by_id(cell.id, color)

    # Convenience methods for grabbing useful parts of the triangle grid.
    @property
    def left_side_cells(self) -> List['TriangleCell']:
        return [cell for cell in self._cells if cell.is_left_edge]

    @property
    def right_side_cells(self) -> List['TriangleCell']:
        return [cell for cell in self._cells if cell.is_right_edge]

    @property
    def bottom_side_cells(self) -> List['TriangleCell']:
        return [cell for cell in self._cells if cell.is_bottom_edge]

    @property
    def up_cells(self) -> List['TriangleCell']:
        return [cell for cell in self._cells if cell.is_up]

    @property
    def down_cells(self) -> List['TriangleCell']:
        return [cell for cell in self._cells if cell.is_down]

    # Triangle Grid Helper Functions
    def edge_neighbors_by_coord(self, row: int, col: int) -> Tuple['TriangleCell', 'TriangleCell', 'TriangleCell']:
        """
        Returns a tuple of (left, middle, right) cells that share an edge with the given (row, column) cell.

        Left neighbor is the edge directly to the left of the cell, regardless of up/down orientation.
        Middle neighbor is either the top or bottom neighbor depending where the edge is.
        Right neighbor is the cell immediately to the right.
        """
        cell = self.get_cell_by_coordinates(row, col)
        if cell is None:
            return None, None, None

        left = self.get_cell_by_coordinates(row, col - 1)
        right = self.get_cell_by_coordinates(row, col + 1)

        if cell.is_up:
            middle = self.get_cell_by_coordinates(row + 1, col + 1)
        else:
            middle = self.get_cell_by_coordinates(row - 1, col - 1)

        return left, middle, right

    def edge_neighbors_by_cell(self, cell_id: int) -> Tuple['TriangleCell', 'TriangleCell', 'TriangleCell']:
        """
        Returns a tuple of (left, middle, right) cells that share an edge with the given cell ID.

        Left neighbor is the cell directly to the left.
        Middle neighbor is either the top or bottom neighbor depending where the edge is.
        Right neighbor is the cell directly to the right.
        """
        return self.edge_neighbors_by_coord(*self.id_to_coordinates(cell_id))

    def vertex_neighbors_by_coord(self, row: int, col: int) -> Tuple['TriangleCell', 'TriangleCell', 'TriangleCell']:
        """
        Returns a tuple of (left, middle, right) cells that share a vertex with the given (row, column) cell.

        Left neighbor is the cell opposite the left vertex of the given cell.
        Middle neighbor is the cell opposite the middle (up or down) vertex of the given cell.
        Right neighbor is the cell opposite the right vertex of the given cell.
        """
        cell = self.get_cell_by_coordinates(row, col)
        if cell is None:
            return None, None, None

        if cell.is_up:
            left = self.get_cell_by_coordinates(row + 1, col - 1)
            middle = self.get_cell_by_coordinates(row - 1, col - 1)
            right = self.get_cell_by_coordinates(row + 1, col + 3)
            return left, middle, right

        left = self.get_cell_by_coordinates(row - 1, col - 2)
        middle = self.get_cell_by_coordinates(row + 1, col + 1)
        right = self.get_cell_by_coordinates(row - 1, col + 1)
        return left, middle, right

    def vertex_neighbors_by_cell(self, cell_id: int) -> Tuple['TriangleCell', 'TriangleCell', 'TriangleCell']:
        """
        Returns a tuple of (left, middle, right) cells that share a vertex with the given cell ID.

        Left neighbor is the cell opposite the left vertex of the given cell.
        Middle neighbor is the cell opposite the middle (up or down) vertex of the given cell.
        Right neighbor is the cell opposite the right vertex of the given cell.
        """
        return self.vertex_neighbors_by_coord(*self.id_to_coordinates(cell_id))


    def hexagon_from_btm_cell_by_coords(self, row: int, col: int) -> Tuple['TriangleCell','TriangleCell','TriangleCell','TriangleCell','TriangleCell','TriangleCell']:
        "Given the coordinates of an up facing cell, return the surrounding cells which will make "
        "A hexagon with the specified cell as the base"
        "the tuple will begin with the btm upward facing triangle at the base of the hex"
        "the next cell in the tuple will be the next triangle in the hexagon moving counterclockwise"
        "None will be entered for cells off the grid"
        
        btm_cell = self.get_cell_by_coordinates(row, col)
        a,b,c,d,e,f  = btm_cell, None, None, None, None, None
        if a.is_left_edge:
            b = self.edge_neighbors_by_cell(a.id)[2]
            if b is not None:
                c = self.edge_neighbors_by_cell(b.id)[1]
            if c is not None:
                d = self.edge_neighbors_by_cell(c.id)[0]
            if d is not None:
                e = self.edge_neighbors_by_cell(d.id)[0]
            if e is not None:
                f = self.edge_neighbors_by_cell(e.id)[1]
        elif a.is_right_edge:
            f = self.edge_neighbors_by_cell(a.id)[0]
            if f is not None:
                e = self.edge_neighbors_by_cell(f.id)[1]
            if e is not None:
                d = self.edge_neighbors_by_cell(e.id)[2]
            if d is not None:
                c  = self.edge_neighbors_by_cell(d.id)[2]
            if c is not None:
                b = self.edge_neighbors_by_cell(c.id)[1]
        else:
            b = self.edge_neighbors_by_cell(a.id)[2]
            c = self.edge_neighbors_by_cell(b.id)[1]
            d = self.edge_neighbors_by_cell(c.id)[0]
            e = self.edge_neighbors_by_cell(d.id)[0]
            f = self.edge_neighbors_by_cell(e.id)[1]
            
        return (a,b,c,d,e,f)



class TriangleCell(NamedTuple):
    """A Cell contains multiple LED pixels."""
    id: int
    num_rows: int

    @property
    def coordinates(self) -> Tuple[int, int]:
        """Returns zero-indexed (row, column) containing the cell."""
        return TriangleGrid.id_to_coordinates(self.id)

    @property
    def is_left_edge(self) -> bool:
        """Returns True if cell is along the left edge of the greater triangle."""
        (row, column) = TriangleGrid.id_to_coordinates(self.id)
        return column == 0

    @property
    def is_right_edge(self) -> bool:
        """Returns True if cell is along the right edge of the greater triangle."""
        (row, column) = self.coordinates
        return column + 1 == row_length(row + 1)

    @property
    def is_bottom_edge(self) -> bool:
        """Returns True if cell is along the bottom edge of the greater triangle."""
        (row, column) = self.coordinates
        return row + 1 == self.num_rows and self.is_up

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
        (row, column) = TriangleGrid.id_to_coordinates(self.id)
        return column % 2 == 0

    @property
    def is_down(self) -> bool:
        """Returns True if triangle shaped cell orients with a corner downward."""
        return not self.is_up


def make_triangle(model: Type[ModelBase], row_count: int) -> TriangleGrid:
    """Helper function to build a Triangle with row_count rows."""
    return TriangleGrid(model, row_count)
