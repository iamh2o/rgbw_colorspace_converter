from typing import Callable, Iterator

from color import Color
import triangle_grid
from model import ModelBase


class FakeModel(ModelBase):
    def get_pixels(self, cell_id) -> Iterator[Callable[[Color], None]]:
        pass

    def go(self):
        pass


def test_coordinate_conversion():
    for curr_id in range(256):
        (row, column) = triangle_grid.TriangleGrid.id_to_coordinates(curr_id)
        reverse_id = triangle_grid.TriangleGrid.coordinates_to_id(row, column)
        assert reverse_id == curr_id


def test_builds_triangle():
    for row_count in range(1, 15):
        triangle = triangle_grid.make_triangle(FakeModel(), row_count)

        expected_cell_count = triangle_grid.triangular_number(row_count)
        assert triangle.row_count == row_count
        assert len(triangle.cells) == expected_cell_count,\
            f'cell count {len(triangle.cells)} != expected {expected_cell_count} with rows {row_count}'

        # Each edge has the same number of elements are the number or total rows.
        assert row_count ==\
               len(triangle.bottom_side_cells) == len(triangle.left_side_cells) == len(triangle.right_side_cells)


def test_cell_attributes():
    triangle = triangle_grid.make_triangle(FakeModel(), 3)
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


def test_row_len():
    # (1, 1), (2, 3), (3, 5), (4, 7)...
    for (row, length) in enumerate(range(1, 16, 2), start=1):
        assert triangle_grid.row_length(row) == length


def test_triangle_number():
    for (n, number) in [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (6, 36)
    ]:
        assert triangle_grid.triangular_number(n) == number
