"""
Model to communicate with a SheepSimulator over a TCP socket

Panels are numbered as strings of the form '12b', indicating
'business' or 'party' side of the sheep

XXX Should this class be able to do range checks on cell ids?

"""
import socket
import json

def keystoint(x):
    return {int(k): v for k, v in list(x.items())}

# "off" color for simulator
SIM_DEFAULT = (188, 210, 229) # BCD2E5

class SimulatorModel(object):
    def __init__(self, hostname, port=4444, debug=False, model_json=None, keys_int=False):

        self.keys_int = keys_int
        self.CELL_MAP = None
        self._map_leds(model_json)

        self.server = (hostname, port)
        self.debug = debug
        self.sock = None

        # map of cells to be set on the next call to go
        self.dirty = {}

        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server)
        # XXX throw an exception if the socket isn't available

    def __repr__(self):
        return "SimulatorModel(%s, port=%d, debug=%s)" % (self.server[0], self.server[1], self.debug)

    # Loaders
    def _map_leds(self, f):
        # Loads a json file with mapping info describing your leds.                                           
        # The json file is formatted as a dictionary of numbers (as strings sadly, b/c json is weird  
        #each key in the dict is a fixtureUID.                                      
        # each array that fixtureUID returns is of the format [universeUID, DMXstart#]                         
        ds = None

        if self.keys_int:
            with open(f, 'r') as json_file:
                ds = json.load(json_file, object_hook=keystoint)
        else:
            with open(f, 'r') as json_file:
                ds = json.load(json_file)

        self.CELL_MAP = ds



    # Model basics

    def cell_ids(self):
        return list(self.CELL_IDS.keys())


    
    def set_cell(self, cell, color):

        cell = cell +1 #Simulator cells not 0 based
        try:
            if cell  in self.CELL_MAP:
                ux = self.CELL_MAP[cell][0]
                ix = self.CELL_MAP[cell][1] - 1 #
                sim_key = cell
            #The simulator does not care about universes, but does care about UIDs. I'm manufacturing one by joinng the Universe and fixture ID into the key.
                self.dirty[sim_key] = color
            else:
                print("WARNING: {0} not in cell ID MAP".format(cell))

        except:
            pass


    def set_pixel(self, pixel, color, cellid):

        self.set_cell(cellid, color)

    def set_cells(self, cells, color):
        for cell in cells:
            self.set_cell(cell, color)

    def go(self):
        "Send all of the buffered commands"

        for num in self.dirty:
            color = self.dirty[num]        
            msg = "%s %s %s,%s,%s\n" % ('b', num, color.r, color.g, color.b)
#            print msg
            if self.debug:
                print(msg)
            self.sock.send(msg.encode())

        self.dirty = {}
