from abc import ABC, abstractmethod
from typing import Generator

# Will contain all available non-debug shows and debug shows.
registry = set()
debug_registry = set()


class Show(ABC):
    """
    Abstract base class for all shows.

    By inheriting from Show (e.g. `class AwesomeShow(Show):` the show will be
    found and listed as a runnable show.

    Shows can be disabled with a flag: `class UnfinishedShow(Show, disable=True):`
    Shows can be marked debug with a flag: `class IndexDebug(Show, debug=True):`
    The flags can be combined.

    Shows MUST implement `next_frame()`.
    Shows MAY override `description()` to give context about what the show does.
    """

    # This is using the relatively new __init_subclass__() which is executed for
    # every subclass of Show before __init__(). Each subclass of Show gets added
    # to the module-level registry list.
    # This could have used Show.__subclasses__() to find all shows, but this
    # approach makes it easy and clear to label shows disabled or debug.
    @classmethod
    def __init_subclass__(cls, disable=False, debug=False, **kwargs):
        # https://blog.yuo.be/2018/08/16/__init_subclass__-a-simpler-way-to-implement-class-registries-in-python/
        super().__init_subclass__(**kwargs)
        if not disable:
            registry.add(cls)
        if debug:
            debug_registry.add(cls)

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

    # next_frame returns a generator of floats, so the function should `yield` float values.
    @abstractmethod
    def next_frame(self) -> Generator[float, None, None]:
        """
        Draw the next step of the animation.  This is the main loop of the show.  Set some pixels and then 'yield' a
        number to indicate how long you'd like to wait before drawing the next frame.  Delay numbers are in seconds.
        """
        raise NotImplementedError
