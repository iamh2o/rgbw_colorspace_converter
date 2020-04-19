from abc import ABC, abstractmethod
from functools import lru_cache
from random import choice
from typing import Iterator, Tuple, List, cast, Type, Generator


class Show(ABC):
    """
    Abstract base class for shows.

    By inheriting from Show (e.g. `class AwesomeShow(Show):` your show will be found and listed as a runnable
    show.
    Your show MUST implement next_frame().
    Your show MAY override other methods (just description() right now) that will give context about your show.
    """

    @property
    def name(self) -> str:
        """Returns the name of the show."""
        return type(self).__name__

    @staticmethod
    def description() -> str:
        """
        Returns a show's description when overridden, or empty string.
        """
        return ''

    @abstractmethod
    def next_frame(self) -> Generator[float, None, None]:
        """
        Draw the next step of the animation.  This is the main loop of the show.  Set some pixels and then 'yield' a
        number to indicate how long you'd like to wait before drawing the next frame.  Delay numbers are in seconds.
        """


@lru_cache(maxsize=None)
def load_shows() -> List[Tuple[str, Show]]:
    """Return a sorted list of tuples (name, class) of Show subclasses."""
    return sorted([(cls.__name__, cast(Show, cls)) for cls in Show.__subclasses__()])


def random_shows(no_repeat: float = 1/3) -> Iterator[Tuple[str, Type[Show]]]:
    """
    Return an infinite sequence of randomized shows.

    Remembers the last 'no_repeat' proportion of items to avoid replaying shows too soon. no_repeat defaults to 1/3 of
    the sequence.
    """
    seq = load_shows()  # sequence of tuples of (name, class)
    seen = []

    while True:
        show = choice(seq)
        while show[0] in seen or 'Debug' in show[0]:
            show = choice(seq)

        seen.append(show[0])
        if len(seen) >= no_repeat*len(seq):
            seen.pop(0)

        yield show
