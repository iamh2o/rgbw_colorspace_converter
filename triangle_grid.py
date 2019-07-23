from color import RGB


def make_tri(model, n_rows):
    return TriangleGrid(model, n_rows)


def calc_last_row_len(max_row):
    row_len = 1
    curr_row = 1

    while curr_row < max_row:
        if max_row == 1:
            row_len = 1
        else:
            row_len += 2
        curr_row += 1
    return row_len

##
## Triangle Grid class to represent one strip
##


# Some reading on grids http://www-cs-students.stanford.edu/~amitp/game-programming/grids/
class TriangleGrid(object):
    def __init__(self, model, n_rows):
        self._model = model
        self._n_rows = n_rows
        self._len_of_last_row = calc_last_row_len(n_rows)

        self._triangle_grid = [[None for i in range(self._len_of_last_row)] for j in range(self._n_rows)]  #B/C this way of building a 2d array give you buggy garbage where setting [0][0] assigns all rows at posn [0] the value you are seetting[[None]*self.len_of_last_row]*self.n_rows
        self._build_triangle_array_and_grid(n_rows)

    def __str__(self):
        return str("ME")

    def __repr__(self):
        print("what is this for?")

        #OMG, this is such a nighmare... but it works...
    def _build_triangle_array_and_grid(self, n_rows):
        self._cells = []
        if n_rows < 1:
            raise Exception('row num must be 1+', n_rows)
        if n_rows > 16:
            raise Exception('row num must be <15')
        if len(self._cells) > 0:
            raise Exception('You have already built a triangle grid, clear this one first')

        #By 'Y' I mean column..... sorry
        grid_y_start_pos = (int(self._len_of_last_row)-1)//2
        grid_y_curr_pos = grid_y_start_pos

        row_len = 0
        end_cell_id = 0
        cell_id = 0
        end_cell_id = 0
        top_pixel = 73 #pointy top
        btm_pixel = 67 #flat btm
        curr_row = 0
        while curr_row < n_rows:
#            print "Curr Row:", curr_row
            left_set = False
            cells_added = 0
            up_down = 'up'
            l_corner = False
            r_corner = False
            top = False
            if curr_row == n_rows:
                l_corner = True
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
                    top = True
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

                tco = None #triagnel cell object
                if up_down == 'up':
                    tco = TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [top_pixel, top_pixel-1, top_pixel-2, top_pixel-3, top_pixel-4, top_pixel-5])
                    self._cells.append(tco)
                    top_pixel -= 6
                    up_down = 'down'
                else:
                    if curr_row >1:
                        tco = TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [btm_pixel, btm_pixel+1, btm_pixel+2, btm_pixel+3, btm_pixel+4, btm_pixel+5])
                        self._cells.append(tco)
                        btm_pixel += 6
                    else:
                        tco = TriangleCell(cell_id,  curr_row, up_down, top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, [btm_pixel, btm_pixel-1, btm_pixel-2, btm_pixel-3, btm_pixel-4, btm_pixel-5])
                        self._cells.append(tco)
                        btm_pixel -= 6
                    up_down = 'up' 

                #Add Cell To Triangle Grid!
                tco.add_row_col(curr_row, grid_y_curr_pos)
                self._triangle_grid[curr_row][grid_y_curr_pos] = tco
                grid_y_curr_pos += 1

                if l_corner is True:
                    l_corner = False
                loop_start = False

                row_pos += 1

                cell_id +=1

            if cell_id == end_cell_id:
                up_down = 'up'
            end_cell_id += 2 + cells_added

            grid_y_curr_pos = grid_y_start_pos - curr_row-1 

            curr_row += 1
            btm_pixel -= 2 #(curr_row*6)+7
            if curr_row > 1:
                btm_pixel -= (curr_row*6)+9+9

            top_pixel -= (curr_row*6)+9

    def go(self):
        self._model.go()

    def clear(self):
        self.set_all_cells(RGB( 0, 0, 0))
        self.go()

    def get_cells(self):
        return self._cells

    def get_triangle_grid(self):
        return self._triangle_grid

    def get_cell_by_grid_coords(self, rown, coln):
        "RETURNS cell object or None if no cell is mapped to the coord"

        if rown > self._n_rows:
            return None
        elif coln > self._len_of_last_row:
            return None
        else:
            return self._triangle_grid[rown][coln]

    def get_cell_by_id(self, cell_id):
        return self._cells[cell_id+1]

    def get_cell_by_array_posn(self, arr_pos):
        return self._cells[arr_pos]

    def set_cell(self, cell, color):
        if cell is None:
            print("WARNING: Skipping 'Nonetype' cell")
        else:
            for pixel in cell.get_pixels():
                self._model.set_pixel(pixel, color, cell.get_id())

    def set_cell_by_cellid(self, cell, color):
        for pixel in self._cells[cell].get_pixels():
            self._model.set_pixel(pixel, color, cell)

    def get_all_cells(self):
        "Return the list of valid cell IDs"
        return self._cells

    def set_cells_by_cellid(self, cells, color):
        for cell in cells:
            for pixel in self._cells[cell].get_pixels():
                self._model.set_pixel(pixel, color, cell.get_id())

    def set_cells(self, cells, color):
        for cell in cells:
            if cell is None:
                print("WARNING: Skipping 'Nonetype' cell")
            else:
                for pixel in cell.get_pixels():
                    self._model.set_pixel(pixel, color, cell.get_id())

    def set_all_cells(self, color):
        for cell in self._cells:
            for pixel in cell.get_pixels():
                self._model.set_pixel(pixel, color, cell.get_id())

    def set_pixel(self, pixel, color, cellid):
        self._model.set_pixel(pixel, color, cellid)  ###Have to pass the cellid through b/c the simulator does not understand pixels

    def clear(self):
        self.set_all_cells(RGB( 0, 0, 0))
        self.go()

    def go(self):
        self._model.go()

    # convenience methods for grabbing useful parts of the triangle grid

    def get_left_side_cells(self):
        cells = []
        for i in self._cells:
            if i.is_left_edge():
                cells.append(i)
        return cells
            
    def get_right_side_cells(self):
        cells = []
        for i in self._cells:
            if i.is_right_edge():
                cells.append(i)
        return cells

    def get_bottom_side_cells(self):
        cells = []
        for i in self._cells:
            if i.is_bottom_edge():
                cells.append(i)
        return cells

    def get_up_cells(self):
        cells = []
        for i in self._cells:
            if i.is_up():
                cells.append(i)
        return cells

    def get_down_cells(self):
        cells = []
        for i in self._cells:
            if i.is_down():
                cells.append(i)
        return cells

    def is_edge(self, cell):
        if cell._l_edge:
            return True
        elif cell._r_edge: 
            return True
        elif cell._btm_side: 
            return True
        else:
            return False

    # Triangle Grid Helper Functions

    def get_edge_neighbors_by_coord(self, row, col):
        "returned in a tuple of (left neighbor, middle neighbor, right neighbor)"
        "Where left is the edge directly to the left of the cell, regardless of up/down orientation"
        "Where middle is either the top or bottom neighbor depending where the edge is. the cell knows its up/down orientation"
        "Right neighbor is the cell immediately to the right."
        cell = self.get_cell_by_grid_coords(row, col)
        if cell is None:
            return None
        else:
            l = None
            m = None
            r = None
            if cell.is_up():
                l = self.get_cell_by_grid_coords(row, col-1)
                m = self.get_cell_by_grid_coords(row+1, col)
                r = self.get_cell_by_grid_coords(row, col+1)
            else:
                l = self.get_cell_by_grid_coords(row, col-1)
                m = self.get_cell_by_grid_coords(row-1, col)
                r = self.get_cell_by_grid_coords(row, col+1)
        return (l, m, r)

    def  get_edge_neighbors_by_cell(self, cell):
        return self.get_edge_neighbors_by_coord(cell.get_row_num(), cell.get_col_pos())

    def get_vertex_neighbors_by_coord(self, row, col):
        "Return the neighbors whose vertexes are point to point"
        "Uses same logic as edge_neighbors, left, middle, right"
        cell = self.get_cell_by_grid_coords(row, col)
        if cell is None:
            return None
        else:
            l = None
            m = None
            r = None
            if cell.is_up():
                l = self.get_cell_by_grid_coords(row+1, col-1)
                m = self.get_cell_by_grid_coords(row-1, col)
                r = self.get_cell_by_grid_coords(row+1, col+1)
            else:
                l = self.get_cell_by_grid_coords(row-1, col-1)
                m = self.get_cell_by_grid_coords(row+1, col)
                r = self.get_cell_by_grid_coords(row-1, col+1)

            return (l, m, r)

    def get_vertex_neighbors_by_cell(self, cell):
        return self.get_vertex_neighbors_by_coord(cell.get_row_num(), cell.get_col_pos())

    def get_hexagon_from_btm_cell_by_coords(self, row, col):
        "Given the coordinates of an up facing cell, return the surrounding cells which will make "
        "A hexagon with the specified cell as the base"
        "the tuple will begin with the upper left cell, then it's upper neighbor, then its upper right"
        "neighbor.... and so on"

        cell = self.get_cell_by_grid_coords(row, col)
        if cell is None:
            return None
        else:
            a = self.get_cell_by_grid_coords(row, col-1)
            b =self.get_cell_by_grid_coords(row-1, col-1)
            c =self.get_cell_by_grid_coords(row-1, col)
            d =self.get_cell_by_grid_coords(row-1, col+1)
            e =self.get_cell_by_grid_coords(row, col+1)
            return (cell, a, b, c, d, e)

    def get_hexagon_from_btm_cell_by_cell(self, cell):
        return self.get_hexagon_from_btm_cell_by_coords(cell.get_row_num(), cell.get_col_pos())


class TriangleCell(object):
    def __init__(self,  cell_id,  row, up_down, is_top, l_corner, r_corner, is_l_edge, is_r_edge, is_btm_edge, row_pos, pixels=[]):

        self._id = cell_id
        self._row_n = row
        self._row_pos = row_pos
        self._l_edge = is_l_edge
        if cell_id in [1, 3]:
            self._l_edge = True
        self._r_edge = is_r_edge
        if cell_id in [1, 3]:
            self._r_edge= True
        self._top_cell = is_top
        self._btm_right = r_corner
        self._btm_left = l_corner
        self._pointy_side = up_down
        self._btm_side = is_btm_edge
        self._up_down = up_down
        self._pixels = pixels #do we really need a pixel class?

    def add_row_col(self, r, c):
        self._grid_row_n = r
        self._grid_col_n = c

    def get_id(self):
        return self._id

    def get_pixels(self,oriented=True):
        if oriented:
            if self._up_down is 'up':
                return self._pixels
            else:
                if self._row_n == 2:   ####FIXME  Something wrrong with bottom cells in row 2 and maybe deeper
                    return self._pixels
                else:
                    return self._pixels[::-1]
        else:
            return self._pixels

    def get_row_num(self):
        return self._grid_row_n
    def get_col_pos(self):
        return self._grid_col_n
    def is_left_edge(self):
        return self._l_edge
    def is_right_edge(self):
        return self._r_edge
    def is_bottom_edge(self):
        return self._btm_side
    def is_top(self):
        return self._top_cell
    def is_right_btm_corner(self):
        return self._btm_right
    def is_left_btm_corner(self):
        return self._btm_left
    def row_num(self):
        return self._row_n
    def is_up(self):
        return self._up_down in "up"
    def is_down(self):
        return self._up_down in "down"


class TriangleCellPixel(object):
    def __init__(self):
        pass
