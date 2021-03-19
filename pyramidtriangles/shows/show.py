from __future__ import annotations
import queue
from abc import ABC, abstractmethod
from collections.abc import Generator, MutableMapping, Iterable, Mapping
from dataclasses import dataclass
from logging import getLogger
from typing import Union

from ..model import DisplayColor
from ..grid import Pyramid

logger = getLogger(__name__)

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

    @abstractmethod
    def __init__(self, pyramid: Pyramid) -> None:
        if not self.__knobs:
            self.__knobs = KnobCollection()

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

    @property
    def knobs(self) -> KnobCollection:
        """
        Returns the show's KnobMediator. Creates a new one if needed.
        """
        try:
            return self.__knobs
        except AttributeError:
            self.__knobs = KnobCollection()
            return self.__knobs

    # next_frame returns a generator of floats, so the function should `yield` float values.
    @abstractmethod
    def next_frame(self) -> Generator[float, None, None]:
        """
        Draw the next step of the animation.  This is the main loop of the show.  Set some pixels and then 'yield' a
        number to indicate how long you'd like to wait before drawing the next frame.  Delay numbers are in seconds.
        """
        ...


KnobType = Union['ValueKnob', 'HSVKnob']
KnobValue = Union[int, float, DisplayColor]
# Generic type of int or float
V = Union[int, float]


@dataclass
class ValueKnob:
    """
    Configurable knob for an int or float value.
    """
    default: V
    min: V
    max: V
    step: V


@dataclass
class HSVKnob:
    """
    Configurable knob for an HSV value.
    """
    default: DisplayColor


class KnobCollection(MutableMapping):
    """
    Mediates setting/getting of knob values to ensure thread safety. Each show
    will have its own KnobCollection at show.knobs.
    """
    def __init__(self):
        self.queue = queue.Queue()
        # Holds name -> default knob values
        self.knobs: dict[str, KnobType] = dict()
        # Holds name -> current knob values, which gets updated
        self.values = dict()

    def _process_queue(self):
        """
        Process queue of submitted knob values. Values updates are put in a
        queue for thread-safety.
        """
        while True:
            try:
                (name, value) = self.queue.get_nowait()
                if name not in self.values.keys():
                    logger.warning(f"{type(self).__name__}: knob name '{name}' in queue but not registered")
                    continue  # skipping

                if isinstance(value, (int, float, DisplayColor)):
                    self.values[name] = value
                else:
                    raise TypeError(f"Unexpected knob value type {type(value)}")
            except queue.Empty:
                break

    def register(self, name: str, knob: Union[ValueKnob, HSVKnob]):
        """Register a knob for the show by name."""
        if not name:
            raise ValueError("Cannot register knob with empty name")
        if name in self.knobs or name in self.values:
            raise ValueError(f"Knob with name '{name}' already registered")

        self.knobs[name] = knob
        self.values[name] = knob.default

    def __getitem__(self, name: str) -> KnobValue:
        """
        Allows getting a knob value in a show with `self.knobs['Knob name']`.
        """
        self._process_queue()
        return self.values[name]

    def __setitem__(self, name: str, value: KnobValue):
        """
        Allows setting a knob value in a show with `self.knobs['Knob name'] = value`.
        """
        # Values are going to be updated via web, which runs many threads.
        # All value updates are put in a queue for thread-safety.
        self.queue.put_nowait((name, value))

    def __delitem__(self, _):
        raise NotImplementedError

    def __len__(self):
        """Enables len(knobs)"""
        return len(self.values)

    def __iter__(self):
        """Enables iterating over knobs"""
        return iter(self.values)

    @property
    def json_array(self) -> Iterable[Mapping[str, Union[str, dict[str, float]]]]:
        """
        Creates a JSON array of configured knobs and default values.

        [{
          name: 'Speed',
          value: {
            default: {
              h: 1.0,
              s: 1.0,
              v: 1.0,
            },
          },
          type: 'HSVKnob',
        },
        ...]

        Actual JSON encoding is left to cherrypy as part of a larger message.
        """
        ret = []
        for (name, knob) in self.knobs.items():
            knob_type = type(knob).__name__
            if isinstance(knob.default, DisplayColor):
                hsv = knob.default.hsv
                # JSON encoder doesn't know how to serialize an HSV type
                knob.default = {'h': hsv[0], 's': hsv[1], 'v': hsv[2]}
            ret.append({'name': name, 'value': knob, 'type': knob_type})
        return ret
