from abc import ABC, abstractmethod
from functools import lru_cache
from random import choice
from typing import Iterator, List, Tuple


class ShowBase(ABC):
    """Abstract base class to register Shows"""

    @abstractmethod
    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop of the show.  Set some pixels and then 'yield' a
        number to indicate how long you'd like to wait before drawing the next frame.  Delay numbers are in seconds.
        """


@lru_cache(maxsize=None)
def load_shows() -> List[Tuple[str, type]]:
    """Return a sorted list of tuples (name, class) of ShowBase subclasses."""
    shows = [(cls.__name__, cls) for cls in ShowBase.__subclasses__()]
    return sorted(shows, key=lambda x: x[0])  # sort show tuples by name before returning them


def random_shows(no_repeat: float = 1/3) -> Iterator[Tuple[str, type]]:
    """
    Return an infinite sequence of randomized shows.

    Remembers the last 'no_repeat' proportion of items to avoid replaying shows too soon. no_repeat defaults to 1/3 of
    the sequence.
    """
    seq = load_shows()  # sequence of tuples of (name, class)
    seen = []

    while True:
        show = choice(seq)
        while show[0] in seen:
            show = choice(seq)

        seen.append(show[0])
        if len(seen) >= no_repeat*len(seq):
            seen.pop(0)

        yield show
