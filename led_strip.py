from collections import defaultdict, namedtuple
from color import RGB

##
## LED geometry
##

# All LED (except the feet)
#ALL = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,150,160]


# Rough grouping of pixels by position on the string
LOW    = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]
MEDIUM = [43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84]
HIGH   = [85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128]
          
          



###what is this?
def make_led(model, geom_file):
    return LEDstrip(model, geom_file)
                      

##
## LED class to represent one strip
##

class LEDstrip(object):
    def __init__(self, model, geom_file=None):

        self.model = model
#        from IPython import embed; embed()
        
        self.cells = set(self.model.PANEL_MAP.keys())
        self._neighbor_map = self.load_geometry(geom_file)
#        from IPython import embed; embed()  

    def __repr__(self):
        return "Sheep(%s')" % (self.model)

    def load_geometry(self,mapfile):
        """                                                                   
        Load LED neighbor geometry                                                  
        Returns a map { led: [(top_neighbor), (bottom_neighbor)], ... }                    
        """

        dat = {}

        fh = open(mapfile,'r')
        for f in fh:
            sl = f.rstrip().split('\t')
            panel = sl[0]
            bottom = sl[1]
            top = sl[2]
            dat[panel] = {'top':top,
                          'bottom':bottom
                          }
        return dat

    def top_neighbor(self,led):
        "Return the list of leds directly above"
        tn = self._neighbor_map[led]['top']
        return tn

    def bottom_neighbor(self,led):
        "Return the LED below this one"
        bn = self._neighbor_map[led]['bottom']
        return bn
    


    def all_cells(self):
        "Return the list of valid cell IDs"
        return self.cells

    # handle setting LED here to keep the commands sent
    # to the simulator as close as possible to the actual hardware
    def _resolve(self, cell):
        """
        Translate an integer cell id into a model cell identifier
        'a' will be translated into two cells
        """
        if cell in self.cells:
              return [cell]
        else:
            return []

    def set_cell(self, cell, color):
        self.model.set_cell(cell, color)

    def set_cells(self, cells, color):
        self.model.set_cells(cells, color)

    def set_all_cells(self, color):
        self.set_cells(self.model.PANEL_MAP.keys(), color)

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
