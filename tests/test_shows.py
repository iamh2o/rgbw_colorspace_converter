import shows


def test_load_shows():
    names = {name for (name, cls) in shows.load_shows()}
    assert {
        shows.LeftToRight.__name__,
        shows.LeftToRightAndBack.__name__,
        shows.Random.__name__,
        shows.UpDown.__name__,
    }.issubset(names)
