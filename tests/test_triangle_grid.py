import triangle_grid
from model import ModelBase


class FakeModel(ModelBase):
    def set_pixel(self, pixel, color, cell_id):
        pass

    def go(self):
        pass


def triangular_number(n):
    return (n * (n + 1)) // 2


# TODO: Figure out why cell count is off from expected
def test_builds_triangle():
    for row_count in range(1, 15):
        cell_count = triangular_number(row_count)
        print(row_count, cell_count)

        triangle = triangle_grid.make_tri(FakeModel(), row_count)
        cells = triangle.get_all_cells()
        assert len(cells) == cell_count, f'cell count {len(cells)} != expected {cell_count} with rows {row_count}'


def test_row_len():
    # (1, 1), (2, 3), (3, 5), (4, 7)...
    for (row, length) in enumerate(range(1, 16, 2), start=1):
        assert triangle_grid.row_len(row) == length
