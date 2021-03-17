from __future__ import annotations
from logging import getLogger
import queue
from collections.abc import MutableMapping, Iterable, Mapping
from dataclasses import dataclass, asdict
from typing import Union

from ..model import DisplayColor

logger = getLogger(__name__)

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
    Mediates setting/getting of knob values to ensure thread safety.
    """
    def __init__(self):
        self.queue = queue.Queue()
        # Holds name -> default knob values
        self.knobs = dict()
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
        return len(self.values)

    def __iter__(self):
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
        .
        .
        .
        ]

        Actual JSON encoding is left to cherrypy as part of a larger message.
        """
        ret = []
        for (name, knob) in self.knobs.items():
            knob_type = type(knob).__name__
            knob_value = asdict(knob)
            if isinstance(knob_value['default'], DisplayColor):
                hsv = knob_value['default'].hsv
                # JSON encoder doesn't know how to serialize an HSV type
                knob_value['default'] = {'h': hsv[0], 's': hsv[1], 'v': hsv[2]}
            ret.append({'name': name, 'value': knob_value, 'type': knob_type})
        return ret
