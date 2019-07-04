from collections import defaultdict, namedtuple
from color import RGBW


def make_tri(model, n_rows):
    return TriangleGrid(model,n_rows)


##
## Triangle Grid class to represent one strip
##

class TriangleGrid(object):
    def __init__(self, model, n_rows):

        self.model = model
        self.n_rows = n_rows
        self.build_triangle_array(n_rows)
#        self.build_triangle_grid()
#        from IPython import embed; embed()

    def __str__(self):
        return str("ME")

    def __repr__(self):
        print "what is this for?"
#        raise Exception('what is this for?')

    def build_triangle_grid(self):
#        from IPython import embed; embed()  

        self.model_grid = [[None]*self.last_row_len]*self.n_rows

        row_len = len(self.model_grid[0])
        bottom_row_idx = self.n_rows-1

        last_cell = len(self.cells)-1

        row_idx = bottom_row_idx

        next_row_len = row_len -2
        row_pos = row_len-1
        row_pos_offset = 2


        while last_cell >=0:
#            from IPython import embed; embed()

            print self.cells[last_cell]
            self.model_grid[row_idx][row_pos] = self.cells[last_cell]
                       
            row_pos -= 1
            last_cell -= 1
            
            if row_pos == next_row_len:
                row_pos = row_len - row_pos_offset
            
                

    def build_triangle_array(self,n_rows):
        self.cells = []
        if n_rows < 1:
            raise Exception('row num must be 1+', n_rows)
        if n_rows > 16:
            raise Exception('row num must be <15')
        if len(self.cells) > 0:
            raise Exception('You have already built a triangle grid, clear this one first')

        row_len = 0
        end_cell_id = 0
        cell_id = 0
        end_cell_id = 0
        top_pixel = 73 #pointy top
        btm_pixel= 67 #flat btm
        curr_row = 0
        while curr_row < n_rows:
#            print "Curr Row:", curr_row
            left_set = False
            cells_added = 0
            up_down = 'up'
            l_corner=False
            r_corner=False
            top = False
            if curr_row == n_rows:
                l_corner= True
            else:
                l_corner = False

            is_l_edge = False
            is_r_edge = False
            is_btm_edge = False

            loop_start = True
            row_pos = 1
            while cell_id <= end_cell_id:
                if curr_row == n_rows and cell_id == end_cell_id+1:
                    r_corner = True
                else:
                    r_corner = False

                if curr_row == 0:
                    top =  True
                else:
                    top = False
                if loop_start is True:
                    is_l_edge = True
                else:
                    is_l_edge = False
                
                if cell_id == end_cell_id+1:
                    is_r_edge = True
                else:
                    is_r_edge = False
                if curr_row == n_rows:
                    if up_down in 'up':
                        is_btm_edge = True
                    else:
                        is_btm_edge = False
                else:
                    is_btm_edge = False
                cells_added += 1

                print "XXXX", cell_id, top_pixel, btm_pixel, curr_row
                if up_down == 'up':
                    self.cells.append(TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [top_pixel, top_pixel-1, top_pixel-2, top_pixel-3, top_pixel-4, top_pixel-5]))
                    top_pixel -= 6                
                    up_down = 'down'
                else:
                    if curr_row >1:
                        self.cells.append(TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [btm_pixel, btm_pixel+1, btm_pixel+2, btm_pixel+3, btm_pixel+4, btm_pixel+5]))
                        btm_pixel +=6
                    else:
                        self.cells.append(TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [btm_pixel, btm_pixel-1, btm_pixel-2, btm_pixel-3, btm_pixel-4, btm_pixel-5]))
                        btm_pixel -= 6
                    up_down = 'up' 


                if l_corner is True:
                    l_corner = False
                loop_start = False
                self.last_row_len = row_pos
                row_pos += 1

                cell_id +=1
            if cell_id == end_cell_id:
                up_down = 'up'
                
            end_cell_id += 2 + cells_added
            
            curr_row += 1
            btm_pixel -= 2 #(curr_row*6)+7
            if curr_row >1:
                btm_pixel -=  (curr_row*6)+9+9
                
            top_pixel -= (curr_row*6)+9
#        from IPython import embed; embed()
#        raise

    def go(self):
        self.model.go()

    def clear(self):
        self.set_all_cells(RGBW(0,0,0,0))
        self.go()

    def get_cell_by_id(self, cell_id):
        return self.cells[cell_id+1]

    def get_cell_by_array_posn(self,arr_pos):
        return self.cells[arr_pos]

    def set_all_cells(self, color):
        for i in self.cells:
            for ii in i.get_pixels():
                self.set_cell(ii,color)

    def set_cell(self,cell, color):
        #from IPython import embed; embed()
#        try:
        for pixel in self.cells[cell].get_pixels():
            print cell, pixel
            self.model.set_pixel(pixel, color)
#        except:
#            from IPython import embed; embed()     

    def set_cells(self, cells, color):
        for cell in cells:
            for pixel  in self.cells[cell].get_pixels():
                self.model.set_pixel(pixel,color)

    def all_cells(self):
        "Return the list of valid cell IDs"
        return self.cells

    def set_cells(self, cells, color):
        for cell in cells:
            for pixel in self.cells[cell].get_pixels():
                self.model.set_pixel(pixel, color)

    def set_all_cells(self, color):
        for cell in self.cells:
            for pixel in cell.get_pixels():
                self.model.set_pixel(pixel, color)

    def clear(self):
        ""
        self.set_all_cells(RGBW(0,0,0,0))
        self.go()

    def go(self):
        self.model.go()

    # convenience methods for grabbing useful parts of the triangle grid

    def get_left_side_cells(self):
        cells = []
        for i in self.cells:
            if i.is_left_edge():
                cells.append(i)
        return cells
            
    def get_right_side_cells(self):
        cells = []
        for i in self.cells:
            if i.is_right_edge():
                cells.append(i)
        return cells

    def get_bottom_side_cells(self):
        cells = []
        for i in self.cells:
            if i.is_bottom_edge():
                cells.append(i)
        return cells

    def get_up_cells(self):
        cells = []
        for i in self.cells:
            if i.is_up():
                cells.append(i)
        return cells

    def get_down_cells(self):
        cells = []
        for i in self.cells:
            if i.is_down():
                cells.append(i)
        return cells

    def is_edge(self):
        if self.l_edge: return True
        if self.r_edge: return True
        if self.btm_side: return True


class TriangleCellGrid(object):
    def __init__(self):
        pass



class TriangleCell(object):
    def __init__(self,  cell_id,  row, up_down, is_top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, pixels=[]):

        self.id = cell_id
        self.row_n = row
        self.row_pos = row_pos
        self.l_edge = is_l_edge
        if cell_id in [1,3]:
            self.l_edge = True
        self.r_edge = is_r_edge
        if cell_id in [1,3]:
            self.r_edge= True
        self.top_cell = is_top
        self.btm_right = r_corner
        self.btm_left = l_corner
        self.pointy_side = up_down
        self.btm_side = is_btm_edge
        self.up_down = up_down
        self.pixels = pixels #do we really need a pixel class?

    def get_id(self):
        return self.id

    def get_pixels(self,oriented=True):
        if oriented:
            if self.up_down is 'up':
                return self.pixels
            else:
                return self.pixels[::-1]
        else:
            return self.pixels

    def get_row_num(self):
        return self.row_n
    def get_row_pos(self):
        return self.row_pos
    def get_row_num(self):
        return self.row_num
    def is_left_edge(self):
        return self.l_edge
    def is_right_edge(self):
        return self.r_edge
    def is_bottom_edge(self):
        return self.btm_side
    def is_top(self):
        return self.top_cell
    def is_right_btm_corner(self):
        return self.btm_right
    def is_left_btm_corner(self):
        return self.btm_left
    def row_num(self):
        return self.row_n
    def is_up(self):
        return self.up_down in "up"
    def is_down(self):
        return self.up_down in "down"



class TriangleCellPixel(object):
    def __init__(self):
        pass
