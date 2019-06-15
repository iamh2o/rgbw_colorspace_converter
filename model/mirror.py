"""
Proof of concept that dealing with mirroring across
multiple backend models is best done at this layer.

Completely agnostic as to what the cell ids look like,
they are just passed through to the underlying model
"""
class MirrorModel(object):
    def __init__(self, *models):
        self.models = []
        if models:
            for m in models:
                self.add_model(m)

    def add_model(self, model):
        self.models.append(model)

    # Model basics
    def cell_ids(self):
        if len(self.models) > 0:
            return self.models[0].cell_ids()
        else:
            return []
    
    def set_cell(self, cell, color):
        for m in self.models:
            m.set_cell(cell, color)

    def set_cells(self, cells, color):
        for m in self.models:
            m.set_cells(cells, color)

    def go(self):
        for m in self.models:
            m.go()