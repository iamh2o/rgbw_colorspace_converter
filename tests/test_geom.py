from pyramidtriangles.grid import Coordinate, Geometry


def test_row_len():
    # (1, 1), (2, 3), (3, 5), (4, 7)...
    for (row, length) in enumerate(range(1, 16, 2), start=1):
        assert Geometry(origin=Coordinate(0, 0),
                        rows=row).row_length(row - 1) == length


def test_triangle_number():
    for (n, number) in [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
        (5, 25),
        (6, 36)
    ]:
        assert Geometry.triangular_number(n) == number


def test_apex():
    for (n, coordinate) in [
        (1, Coordinate(0, 0)),
        (2, Coordinate(1, 1)),
        (11, Coordinate(10, 10))
    ]:
        assert Geometry(origin=Coordinate(0, 0), rows=n).apex == coordinate
