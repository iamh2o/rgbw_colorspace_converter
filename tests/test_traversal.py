from grid import traversal


def test_left_to_right():
    sequence = list(traversal.left_to_right(1))
    assert [[(0, 0)]] == sequence

    sequence = list(traversal.left_to_right(2))
    assert [[(1, 0)], [(0, 0), (1, 1)], [(1, 2)]] == sequence

    sequence = list(traversal.left_to_right(3))
    assert [[(2, 0)], [(1, 0), (2, 1)], [(0, 0), (1, 1), (2, 2)], [(1, 2), (2, 3)], [(2, 4)]] == sequence


def test_right_to_left():
    for rows in range(1, 12):
        sequence = list(traversal.right_to_left(rows))
        expected = list(reversed(list(traversal.left_to_right(rows))))
        assert expected == sequence
