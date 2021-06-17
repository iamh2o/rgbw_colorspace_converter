from __future__ import annotations
from collections.abc import Iterable

from ..grid.cell import Address, Cell
from . import DisplayColor, Model


class MirrorModel:
    """
    Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.
    """
    models: list[Model]

    def __init__(self, *models):
        self.models = list(models)

    def activate(self, cells: Iterable[Cell]):
        for m in self.models:
            m.activate(cells)

    def stop(self):
        for m in self.models:
            m.stop()

    def add_model(self, model):
        self.models.append(model)

    def set(self, cell: Cell, addr: Address, color: DisplayColor):
        for m in self.models:
            m.set(cell, addr, color)

    def go(self):
        for m in self.models:
            m.go()
