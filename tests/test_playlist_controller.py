import pytest

from pyramidtriangles.core import PlaylistController


def second(items):
    return items[1]


@pytest.fixture
def playlist():
    PlaylistController.setup_database()
    p = PlaylistController()
    p.clear()
    return p


def test_controller(playlist):
    assert playlist.current_playlist() == []

    playlist.append('Show 1')
    assert list(map(second, playlist.current_playlist())) == ['Show 1']
    playlist.append('Show 2')
    assert list(map(second, playlist.current_playlist())) == ['Show 1', 'Show 2']
    playlist.append('Show 3')
    assert list(map(second, playlist.current_playlist())) == ['Show 1', 'Show 2', 'Show 3']
    playlist.append('Show 4')
    assert list(map(second, playlist.current_playlist())) == ['Show 1', 'Show 2', 'Show 3', 'Show 4']

    (second_id, _) = playlist.current_playlist()[1]
    playlist.delete(second_id)
    assert list(map(second, playlist.current_playlist())) == ['Show 1', 'Show 3', 'Show 4']

    playlist.clear()
    assert playlist.current_playlist() == []


def test_controller_looping(playlist):
    playlist.append('Show 1')
    playlist.append('Show 2')
    playlist.append('Show 3')
    playlist.append('Show 4')
    playlist.delete(playlist.current_playlist()[1][0])
    assert list(map(second, playlist.current_playlist())) == ['Show 1', 'Show 3', 'Show 4']

    assert [playlist.next(), playlist.next(), playlist.next(), playlist.next(), playlist.next()] == \
           ['Show 1', 'Show 3', 'Show 4', 'Show 1', 'Show 3']


def test_controller_empty(playlist):
    assert playlist.current_playlist() == []
    # Effective no-op
    playlist.clear()
    assert playlist.next() is None


def test_controller_bad_delete_ignored(playlist):
    assert playlist.current_playlist() == []
    playlist.delete(0)


def test_controller_set_next(playlist):
    assert playlist.current_playlist() == []
    playlist.set_next(0)
    assert playlist.next() is None

    playlist.append('Show 1')
    playlist.append('Show 2')
    playlist.append('Show 3')
    playlist.append('Show 4')

    for (i, show) in enumerate(['Show 1', 'Show 2', 'Show 3']):
        index = playlist.current_playlist()[i][0]
        playlist.set_next(index)
        assert playlist.next() == show


def test_controller_settings(playlist):
    id1 = playlist.append('Show 1')
    assert playlist.get_settings(id1) == {}

    setting1 = {"Speed": 0.5}
    playlist.set_settings(id1, setting1)
    assert playlist.get_settings(id1) == setting1

    setting2 = {
        "Color": {
            "h": 1.0,
            "s": 1.0,
            "v": 1.0,
        },
    }
    playlist.set_settings(id1, setting2)
    assert playlist.get_settings(id1) == setting2
