"""
Model to communicate with a SheepSimulator over a TCP socket

Panels are numbered as strings of the form '12b', indicating
'business' or 'party' side of the sheep

XXX Should this class be able to do range checks on cell ids?

"""
import socket

# Panels 1-44, 'p' for party, 'b' for business
PANEL_IDS = ['%dp' % i for i in range(1,44)]
PANEL_IDS.extend(['%db' % i for i in range(1,44)])

# "off" color for simulator
SIM_DEFAULT = (188,210,229) # BCD2E5

class SimulatorModel(object):
    def __init__(self, hostname, port=4444, debug=False):
        self.server = (hostname, port)
        self.debug = debug
        self.sock = None

        # map of cells to be set on the next call to go
        self.dirty = {}

        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server)
        # XXX throw an exception if the socket isn't available?

    def __repr__(self):
        return "SimulatorModel(%s, port=%d, debug=%s)" % (self.server[0], self.server[1], self.debug)

    # Model basics

    def cell_ids(self):
        return PANEL_IDS

    def set_cell(self, cell, color):
        self.dirty[cell] = color

    def set_cells(self, cells, color):
        for cell in cells:
            self.set_cell(cell, color)

    def go(self):
        "Send all of the buffered commands"
        for (cell, color) in self.dirty.items():
            if color.rgb == (0,0,0):
                r,g,b = SIM_DEFAULT
            else:
                r,g,b = color.rgb[0:3]

            num = cell[:-1]
            side = cell[-1]
            msg = "%s %s %s,%s,%s" % (side, num, r,g,b)
            if self.debug:
                print msg
            self.sock.send(msg)
            self.sock.send('\n')

        self.dirty = {}
