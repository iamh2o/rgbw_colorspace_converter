
from color import RGBW


class UpDown(object):
    def __init__(self, tri_grid):
        self.name = "UpDown"

        # walk pixels up and downs strip
        self.cells = tri_grid

        self.frame_delay = 2

#        from IPython import embed; embed()


    col = 0
    def next_frame(self):
        """
        Draw the next step of the animation.  This is the main loop
        of the show.  Set some pixels and then 'yield' a number to
        indicate how long you'd like to wait before drawing the next
        frame.  Delay numbers are in seconds.
        """

#        from IPython import embed; embed() 
        self.cells.clear()

        col = 255
        a = "up"
        while True:
            self.cells.clear()
#            from IPython import embed; embed()    

            if a in "up":
                print 'up'
                for i in self.cells.get_up_cells():
                    print "Up", i.get_id()
                    self.cells.set_cell(i.get_id(), RGBW(col,25,255,25)) 
            else:
                print 'down'
                for i in self.cells.get_down_cells():
                    print "down",i.get_id()
                    self.cells.set_cell(i.get_id(), RGBW(col,222,0,205))


            if a in "up":
                a = "down"
            else:
                a = "up"
            yield self.frame_delay
