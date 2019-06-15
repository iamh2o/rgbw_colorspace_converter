from collections import defaultdict, namedtuple
from color import RGB

##
## Sheep geometry
##

# All panels (except the feet)
ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42, 43]

# Rough grouping of panels by height on the bus, forming horizontal bands
LOW    = [3, 8, 9, 14, 18, 23, 22, 31, 30, 34, 37, 43, 42]
MEDIUM = [1, 2, 7, 13, 16, 17, 20, 21, 26, 27, 28, 29, 33, 35, 36, 40, 41]
HIGH   = [4, 5, 6, 12, 11, 15, 19, 25, 24, 32, 39]

# Vertical stripes, ordered from front to rear
# Note that this is a list of lists!
VSTRIPES = [[1,2,3],
            [4,5,6,7,8,9],
            [11,12,13,14],
            [15,16,17,18,23],
            [19,20,21,22],
            [24,25,26,27,28,29,30,31],
            [32,35,36,33,34,37,43],
            [39,40,41,42]]

# Front spiral, panels arranged clockwise
FRONT_SPIRAL = [13,16,17,18,14,9,8,7]

# From tom's "sheep tailoring" diagram (link?)
# Split the sheep into four rough quadrants
SHOULDER    = [4,5,1,6,2,7,3,8,9]
RACK        = [11,12,13,16,15,14,18,17,21,20,19]
LOIN        = [23,22,31,30,29,28,27,34,33,26,25,24]
LEG         = [37,43,42,41,35,40,39,32]


def load_geometry(mapfile):
    """
    Load sheep neighbor geometry
    Returns a map { panel: [(edge-neighbors), (vertex-neighbors)], ... }
    """
    with open(mapfile, 'r') as f:
        def blank_or_comment(l):
            return l.startswith('#') or len(l) == 0
        lines = [l.strip() for l in f.readlines()]
        lines = [l for l in lines if not blank_or_comment(l)]

    def to_ints(seq):
        return [int(x) for x in seq]

    def p(raw):
        "returns a tuple containing ([a,a,a], [b,b,b]) given a raw string"
        raw = raw.strip()
        if ' ' not in raw:
            return (to_ints(raw.split(',')), None)
        else:
            # print ">>%s<<" % raw
            a,b = raw.split()
            return (to_ints(a.split(',')), to_ints(b.split(',')))

    dat = defaultdict(list)
    for line in lines:
        # print line
        (num, rest) = line.split(' ', 1)
        dat[int(num)] = p(rest.strip())
    return dat

_neighbor_map = load_geometry('data/geom.txt')

def edge_neighbors(panel):
    "Return the list of panel ids that share an edge with a given panel"
    try:
        return _neighbor_map[panel][0]
    except Exception, e:
        return []

def vertex_neighbors(panel):
    "Return the list of panel ids that share a vertex (but not an edge) with a given panel"
    try:
        return _neighbor_map[panel][1]
    except Exception, e:
        return []

##
## Convenience wrapper to pass around three separate sheep objects
##
SheepSides = namedtuple('SheepSides', ['both', 'party', 'business'])

def make_sheep(model):
    return SheepSides(both=Sheep(model, 'a'),
                      party=Sheep(model, 'p'),
                      business=Sheep(model, 'b'))

##
## Sheep class to represent one or both sides of the sheep
##
VALID_SIDES=set(['a', 'b', 'p'])

class Sheep(object):
    def __init__(self, model, side):
        self.model = model
        if side not in VALID_SIDES:
            raise Exception("%s is not a valid side. use one of a,b,p")
        self.side = side
        self.cells = set(ALL)

    def __repr__(self):
        return "Sheep(%s, side='%s')" % (self.model, self.side)

    def all_cells(self):
        "Return the list of valid cell IDs"
        return ALL

    # handle setting both sides here to keep the commands sent
    # to the simulator as close as possible to the actual hardware
    def _resolve(self, cell):
        """
        Translate an integer cell id into a model cell identifier
        'a' will be translated into two cells
        """
        if cell in self.cells:
            if self.side == 'a':
                return [str(cell)+'b', str(cell)+'p']
            else:
                return [str(cell) + self.side]
        else:
            return []

    def set_cell(self, cell, color):
        # a single set_cell call may result in two panels being set
        c = self._resolve(cell)
        if c:
            # print "setting", c
            self.model.set_cells(c, color)

    def set_cells(self, cells, color):
        resolved = []
        for c in cells:
            resolved.extend(self._resolve(c))
        # print "setting", resolved
        self.model.set_cells(resolved, color)

    def set_all_cells(self, color):
        self.set_cells(ALL, color)

    def clear(self):
        ""
        self.set_all_cells(RGB(0,0,0))
        self.go()

    def go(self):
        self.model.go()

    # convenience methods in case you only have a sheep object
    def edge_neighbors(self, cell):
        return edge_neighbors(cell)

    def vertex_neighbors(self, cell):
        return vertex_neighbors(cell)
