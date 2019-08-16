
from color import Color
from grid.cell import Address, Cell
from .base import ModelBase


class MirrorModel(ModelBase):
    """
    Proof of concept that dealing with mirroring across multiple backend models is best done at this layer.
    """

    def __init__(self, *models):
        self.models = list(models)

    def add_model(self, model):
        self.models.append(model)

    def set(self, cell: Cell, addr: Address, color: Color):
        for m in self.models:
            m.set(addr, color)

    def go(self):
        for m in self.models:
            m.go()
