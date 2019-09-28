from grid import Coordinate, Geometry, traversal


def geom(rows):
    return Geometry(origin=Coordinate(0, 0), rows=rows)


def test_left_to_right():
    sequence = list(traversal.left_to_right(geom(1)))
    assert sequence == [[(0, 0)]]

    sequence = list(traversal.left_to_right(geom(2)))
    assert sequence == [[(1, 0)], [(0, 0), (1, 1)], [(1, 2)]]

    sequence = list(traversal.left_to_right(geom(3)))
    assert sequence == [[(2, 0)], [(1, 0), (2, 1)], [
        (0, 0), (1, 1), (2, 2)], [(1, 2), (2, 3)], [(2, 4)]]


def test_right_to_left():
    for rows in range(1, 12):
        sequence = list(traversal.right_to_left(geom(rows)))
        expected = list(reversed(list(traversal.left_to_right(geom(rows)))))
        assert sequence == expected
