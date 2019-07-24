"""
Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.

Completely agnostic as to what the cell ids look like, they are just passed through to the underlying model.
"""
from itertools import zip_longest
from typing import Callable, Iterator

from color import Color
from .modelbase import ModelBase


class MirrorModel(ModelBase):
    def __init__(self, *models):
        self.models = []
        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, model):
        self.models.append(model)

    def get_pixels(self, cell_id) -> Iterator[Callable[[Color], None]]:
        generators = zip_longest([model.get_pixels(cell_id) for model in self.models])

        def set_color(color: Color):
            pixels = next(generators)
            for pixel in pixels:
                pixel.set_color(color)
        yield set_color

    def go(self):
        for m in self.models:
            m.go()
