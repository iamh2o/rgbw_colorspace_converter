import shows


def test_load_shows():
    names = {name for (name, cls) in shows.load_shows()}
    assert {
        "LeftToRight",
        "LeftToRightAndBack",
        "OneByOne",
        "Random",
        "UpDown"
    }.issubset(names)
