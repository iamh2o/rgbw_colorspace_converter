"""
Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.

Completely agnostic as to what the cell ids look like, they are just passed through to the underlying model.
"""
from .modelbase import ModelBase


class MirrorModel(ModelBase):
    def __init__(self, *models):
        self.models = []
        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, model):
        self.models.append(model)

    # Model basics
    def set_pixel(self, pixel, color, cellid=None):
        for m in self.models:
            m.set_pixel(pixel, color, cellid)

    def go(self):
        for m in self.models:
            m.go()
