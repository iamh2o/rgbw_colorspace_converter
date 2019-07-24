from typing import Callable, Iterator

from color import Color
import grid
from model import ModelBase


class FakeModel(ModelBase):
    def get_pixels(self, cell_id) -> Iterator[Callable[[Color], None]]:
        pass

    def go(self):
        pass


def test_coordinate_conversion():
    for curr_id in range(256):
        (row, column) = grid.TriangleGrid.id_to_coordinates(curr_id)
        reverse_id = grid.TriangleGrid.coordinates_to_id(row, column)
        assert reverse_id == curr_id


def test_builds_triangle():
    for row_count in range(1, 15):
        triangle = grid.make_triangle(FakeModel(), row_count)

        expected_cell_count = grid.triangular_number(row_count)
        assert triangle.row_count == row_count
        assert triangle.size == len(triangle.cells) == expected_cell_count,\
            f'cell count {len(triangle.cells)} != expected {expected_cell_count} with rows {row_count}'

        # Each edge has the same number of elements are the number or total rows.
        assert row_count ==\
               len(triangle.bottom_side_cells) == len(triangle.left_side_cells) == len(triangle.right_side_cells)


def test_cells_out_of_bounds():
    triangle = grid.make_triangle(FakeModel(), 2)

    assert triangle.get_cell_by_coordinates(-1, 0) is None
    assert triangle.get_cell_by_coordinates(0, -1) is None
    assert triangle.get_cell_by_coordinates(0, 1) is None  # Only (0, 0) in first row.
    assert triangle.get_cell_by_coordinates(1, 3) is None
    assert triangle.get_cell_by_coordinates(2, 0) is None  # Row 2 does not exist.

    assert triangle.get_cell_by_id(-1) is None
    assert triangle.get_cell_by_id(triangle.size) is None

    middle_cell = triangle.get_cell_by_id(2)
    assert middle_cell is not None
    for neighbor in triangle.vertex_neighbors_by_cell(2):
        assert neighbor is None


def test_cell_attributes():
    triangle = grid.make_triangle(FakeModel(), 3)
    assert len(triangle.cells) == 9

    top = triangle.get_cell_by_coordinates(0, 0)
    assert top.is_top_corner and top.is_left_edge and top.is_right_edge and top.is_up
    assert not top.is_bottom_edge

    left_corner = triangle.get_cell_by_coordinates(2, 0)
    assert left_corner.is_left_corner and left_corner.is_left_edge and left_corner.is_bottom_edge and left_corner.is_up
    assert not left_corner.is_right_edge

    right_corner = triangle.get_cell_by_coordinates(2, 4)
    assert right_corner.is_right_corner and right_corner.is_right_edge and right_corner.is_bottom_edge
    assert right_corner.is_up
    assert not right_corner.is_left_edge

    inner = triangle.get_cell_by_coordinates(1, 1)
    assert inner.is_down
    assert not inner.is_left_edge and not inner.is_right_edge and not inner.is_bottom_edge


def test_cell_neighbors():
    triangle = grid.make_triangle(FakeModel(), 5)

    # Upward facing cell
    (left, middle, right) = triangle.edge_neighbors_by_cell(6)
    assert left.id == 5
    assert middle.id == 12
    assert right.id == 7

    (left, middle, right) = triangle.vertex_neighbors_by_cell(6)
    assert left.id == 10
    assert middle.id == 2
    assert right.id == 14

    # Downward facing cell
    (left, middle, right) = triangle.edge_neighbors_by_cell(5)
    assert left.id == 4
    assert middle.id == 1
    assert right.id == 6

    (left, middle, right) = triangle.vertex_neighbors_by_cell(5)
    assert left is None
    assert middle.id == 11
    assert right.id == 3

    # Invalid cell
    (left, middle, right) = triangle.edge_neighbors_by_coord(1, -1)
    assert left is middle is right is None
    (left, middle, right) = triangle.vertex_neighbors_by_coord(1, -1)
    assert left is middle is right is None


def test_row_len():
    # (1, 1), (2, 3), (3, 5), (4, 7)...
    for (row, length) in enumerate(range(1, 16, 2), start=1):
        assert grid.row_length(row) == length


def test_triangle_number():
    for (n, number) in [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (6, 36)
    ]:
        assert grid.triangular_number(n) == number
