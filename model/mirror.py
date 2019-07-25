"""
Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.

Completely agnostic as to what the cell ids look like, they are just passed through to the underlying model.
"""
from itertools import zip_longest
from typing import Iterator

from color import Color
from .modelbase import ModelBase, SetColorFunc


class MirrorModel(ModelBase):
    def __init__(self, *models):
        self.models = []
        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, model):
        self.models.append(model)

    def set_pixels_by_cellid(self, cell_id) -> Iterator[SetColorFunc]:
        generators = zip_longest([model.set_pixels_by_cellid(cell_id) for model in self.models])

        def set_color(color: Color):
            pixels = next(generators)
            for pixel in pixels:
                pixel.set_color(color)
        yield set_color

    def go(self):
        for m in self.models:
            m.go()
