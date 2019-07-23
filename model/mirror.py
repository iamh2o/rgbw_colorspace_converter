"""
Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.

Completely agnostic as to what the cell ids look like, they are just passed through to the underlying model.
"""
from itertools import zip_longest

from typing import Iterator, List, Type

from .modelbase import ModelBase, PixelBase


class MirrorPixel(PixelBase):
    def __init__(self, pixel_generators: List[Iterator[Type[PixelBase]]]):
        self.generator = zip_longest(pixel_generators)

    def set_color(self, color):
        pixels = next(self.generator)
        for pixel in pixels:
            pixel.set_color(color)


class MirrorModel(ModelBase):
    def __init__(self, *models):
        self.models = []
        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, model):
        self.models.append(model)

    def get_pixels(self, cell_id):
        return [model.get_pixels(cell_id) for model in self.models]

    def go(self):
        for m in self.models:
            m.go()
