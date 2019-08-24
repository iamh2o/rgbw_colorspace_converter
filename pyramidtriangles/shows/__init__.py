from __future__ import annotations
import importlib
from logging import getLogger
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from random import choice
from typing import cast

# These imports include submodules under the `shows` namespace.
from .show import Show
from .knobs import KnobValue

logger = getLogger(__name__)


# This function, like the original version, dynamically imports all files in
# this directory so individual show files don't need to be imported.
@lru_cache(maxsize=None)
def load_shows() -> list[tuple[str, type[Show]]]:
    """Return a sorted list of (name, class) tuples of all Show subclasses."""
    for name in Path(__file__).parent.glob('[!_]*.py'):
        try:
            importlib.import_module(f'pyramidtriangles.shows.{name.stem}')
        except ImportError as e:
            logger.warning(f"failed to import {name}: {e}")

    return sorted([(cls.__name__, cast(type[Show], cls)) for cls in show.registry])


def random_shows(no_repeat: float = 1/3) -> Iterator[tuple[str, type[Show]]]:
    """
    Returns an infinite sequence of randomized shows.

    It remembers the last `no_repeat` proportion of items to avoid replaying
    shows too soon. `no_repeat` defaults to 1/3 of the number of shows.

    Shows marked `debug=True` are not included in the sequence.
    """
    seq = load_shows()  # sequence of tuples of (name, class)
    seen = []

    while True:
        (name, cls) = choice(seq)
        if name not in seen and name not in show.debug_registry:
            seen.append(name)
            if len(seen) >= no_repeat * len(seq):
                seen.pop(0)
            yield name, cls
