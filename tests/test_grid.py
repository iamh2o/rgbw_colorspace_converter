from collections.abc import Iterable
from pytest import raises

from grid import (
    Position, Geometry, Cell, Address, bottom_edge, left_edge, right_edge, vertex_neighbors, edge_neighbors,
    Coordinate, Face, Panel, Universe
)
from model import Model, DisplayColor


class FakeModel(Model):
    def activate(self, cells: Iterable[Cell]):
        pass

    def set(self, cell: Cell, addr: Address, color: DisplayColor):
        pass

    def go(self):
        pass

    def stop(self):
        pass


def single_panel_grid(rows):
    geom = Geometry(origin=Coordinate(0, 0), rows=rows)
    return Face(FakeModel(),
                geom,
                [Panel(geom, Address(Universe(1, 1), 4))])


def test_triangle_counts():
    for row_count in range(1, 15):
        triangle = single_panel_grid(row_count)
        assert triangle.row_count == row_count

        expected_cell_count = Geometry.triangular_number(row_count)
        assert len(triangle) == len(triangle.cells) == expected_cell_count,\
            f'cell count {len(triangle.cells)} != expected {expected_cell_count} with rows {row_count}'

        # Each edge has the same number of elements are the number or total rows.
        assert row_count == len(bottom_edge(triangle)) == len(
            left_edge(triangle)) == len(right_edge(triangle))


def test_cells_out_of_bounds():
    triangle = single_panel_grid(2)

    with raises(KeyError):
        triangle[Coordinate(-1, 0)]
    with raises(KeyError):
        triangle[Coordinate(0, -1)]
    with raises(KeyError):
        triangle[Position(0, 1)]  # Only (0, 0) in first row.
    with raises(KeyError):
        triangle[Position(1, 3)]
    with raises(KeyError):
        triangle[Position(2, 0)]  # Row 2 does not exist.

    with raises(TypeError):
        triangle[1]


def test_cell_neighbors():
    triangle = single_panel_grid(5)

    # Upward facing cell
    (left, middle, right) = triangle.select(edge_neighbors(Coordinate(4, 2)))
    assert left.coordinate == Coordinate(3, 2)
    assert middle.coordinate == Coordinate(4, 1)
    assert right.coordinate == Coordinate(5, 2)

    (left, middle, right) = triangle.select(vertex_neighbors(Coordinate(4, 2)))
    assert left.coordinate == Coordinate(2, 1)
    assert middle.coordinate == Coordinate(4, 3)
    assert right.coordinate == Coordinate(6, 1)

    # Downward facing cell
    (left, middle, right) = triangle.select(edge_neighbors(Coordinate(3, 2)))
    assert left.coordinate == Coordinate(2, 2)
    assert middle.coordinate == Coordinate(3, 3)
    assert right.coordinate == Coordinate(4, 2)

    (left, middle, right) = triangle.select(vertex_neighbors(Coordinate(3, 2)))
    assert left is None  # left neighbor is off the panel and the whole face geometry
    assert middle.coordinate == Coordinate(3, 1)
    assert right.coordinate == Coordinate(5, 3)

    # Invalid cell
    assert not any(triangle.select(edge_neighbors(Position(1, -1))))
    assert not any(triangle.select(vertex_neighbors(Position(1, -1))))
    assert not any(triangle.select(edge_neighbors(Coordinate(2, 4))))
    assert not any(triangle.select(vertex_neighbors(Coordinate(2, 4))))


def test_build_face():
    single = Face.build(FakeModel(), [[0]])
    assert len(single.panels) == 1
    assert single.geom.height == 11

    double = Face.build(FakeModel(), [[], [0, 1]])
    assert len(double.panels) == 2
    assert double.geom.height == 2 * 11
    assert sorted(p.geom.origin for p in double.panels) == [Coordinate(0, 0),
                                                            Coordinate(22, 0)]
    assert sorted(p.start.universe.id for p in double.panels) == [1, 12]

    full = Face.build(FakeModel(), [[0], [], [0, 4]])
    assert len(full.panels) == 3
    assert full.geom.height == 3 * 11
    assert sorted(p.geom.origin for p in full.panels) == [Coordinate(0, 0),
                                                          Coordinate(22, 22),
                                                          Coordinate(88, 0)]
    assert sorted(p.start.universe.id for p in full.panels) == [1, 12, 23]
