from color import Color
from grid import Grid, Position, Geometry, Cell, Address
from model import ModelBase


class FakeModel(ModelBase):
    def set(self, cell: Cell, addr: Address, color: Color):
        pass

    def go(self):
        pass


def test_coordinate_symmetry():
    for curr_id in range(256):
        assert Position.from_id(curr_id).id == curr_id


def test_cell_attributes():
    triangle = Grid(model=FakeModel(), geom=Geometry(rows=3))
    assert len(triangle.cells) == 9

    top = triangle[Position(0, 0)]
    assert top.is_top_corner and top.is_left_edge and top.is_right_edge and top.is_up and top.is_edge
    assert not top.is_bottom_edge

    left_corner = triangle[Position(2, 0)]
    assert left_corner.is_left_corner and left_corner.is_left_edge and left_corner.is_bottom_edge and left_corner.is_up
    assert not left_corner.is_right_edge

    right_corner = triangle[Position(2, 4)]
    assert right_corner.is_right_corner and right_corner.is_right_edge and right_corner.is_bottom_edge
    assert right_corner.is_up
    assert not right_corner.is_left_edge

    inner = triangle[Position(1, 1)]
    assert inner.is_down
    assert not inner.is_left_edge and not inner.is_right_edge and not inner.is_bottom_edge and not inner.is_edge
