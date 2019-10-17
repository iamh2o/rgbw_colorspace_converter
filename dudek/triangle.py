from collections import defaultdict
from dudek.HelperFunctions import distance, ROTATE_CLOCK, ROTATE_COUNTER, ROTATE_COORD_CLOCK
from grid import Coordinate
from random import choice

"""
Model to communicate with a Triangle simulator over a TCP socket

Parameters for each Triangle: (X,Y), corner, direction
Corner: connector attachment is 'L' = Left, 'R' = Right, 'C' = Center
Direction: As viewed from corner, lights go 'L' = Left, 'R' = Right
Processing file needs to be similarly adjusted
"""
NUM_BIG_TRI = 6

BIG_COORD = [((0, 0), 'L', 'L'),
             ((1, 1), 'L', 'L'),
             ((2, 0), 'L', 'L'),
             ((4, 0), 'L', 'L'),
             ((5, 1), 'L', 'L'),
             ((6, 0), 'L', 'L')]

TRI_GEN = 12    # Size of Big Triangles - Fixed at 12


def load_triangles(model):
    return Triangle(model)


class Triangle:
    """
    Triangle coordinates are stored in a hash table.
    Keys are (x,y) coordinate tuples
    Values are (strip, pixel) tuples, sometimes more than one.

    Frames implemented to shorten messages:
    Send only the pixels that change color
    Frames are hash tables where keys are (x,y) coordinates
    and values are (r,g,b) colors
    """
    def __init__(self, model):
        self.model = model
        self.cellmap = self.add_strips(BIG_COORD)
        self.curr_frame = {}
        self.next_frame = {}
        self.init_frames()

    def __repr__(self):
        return "Triangles(%s)" % self.model

    def all_cells(self):
        """Return the list of all valid coords"""
        return self.cellmap.keys()

    def cell_exists(self, coord):
        """Return boolean of whether cell exists"""
        return coord in self.cellmap

    def set_cell(self, coord, color):
        if self.cell_exists(coord):
            self.next_frame[coord] = color

    def set_cells(self, coords, color):
        for coord in coords:
            self.set_cell(coord, color)

    def set_all_cells(self, color):
        self.set_cells(self.all_cells(), color)

    def black_cell(self, coord):
        self.set_cell(coord, (0, 0, 0))

    def black_cells(self, coords):
        self.set_cells(coords, (0, 0, 0))

    def black_all_cells(self):
        self.set_all_cells((0, 0, 0))

    def clear(self):
        self.force_frame()
        self.black_all_cells()
        self.go()

    def go(self, fract=1):
        self.send_frame(fract)
        self.model.go(fract)
        self.update_frame()

    def send_delay(self, delay):
        self.model.send_delay(delay)

    def update_frame(self):
        for coord in self.next_frame:
            self.curr_frame[coord] = self.next_frame[coord]

    def send_frame(self, fract=1):
        for coord, color in self.next_frame.items():
            if fract != 1 or (coord in self.curr_frame and self.curr_frame[coord] != color):  # Has the color changed?
                self.model.set(Coordinate(*self.cellmap[coord]), color)

    def force_frame(self):
        for coord in self.curr_frame:
            self.curr_frame[coord] = (-1, -1, -1)  # Force update

    def init_frames(self):
        for coord in self.cellmap:
            self.curr_frame[coord] = (0, 0, 0)
            self.next_frame[coord] = (0, 0, 0)

    def get_rand_cell(self):
        return choice(self.all_cells())

    def get_strip_from_coord(self, coord):
        """pulls the first strip that fits a coordinate"""
        choices = self.cellmap[coord]
        (strip, fix) = choices[0]
        return strip

    def add_strips(self, coord_table):
        cellmap = defaultdict(list)
        for strip, (big_coord, corner, direction) in enumerate(coord_table):
            cellmap = self.add_strip(cellmap, strip, big_coord, corner, direction)
        return cellmap

    def add_strip(self, cellmap, strip, big_coord, corner, direction):
        """Stuff the cellmap with a Triangle strip, going row by column"""
        (x_offset, y_offset) = big_coord
        x_offset *= TRI_GEN
        y_offset *= TRI_GEN

        if not point_up(big_coord):
            y_offset += (TRI_GEN - 1)

        for y in range(TRI_GEN):
            for x in range(row_width(y)):
                xcoord = x_offset + x + y
                ycoord = y_offset + y if point_up(big_coord) else y_offset - y
                coord = (xcoord, ycoord)
                fix = self.calc_fix(coord, big_coord, corner, direction)
                cellmap[coord].append((strip, fix))

        return cellmap

    def calc_fix(self, coord, big_coord, corner, direction):
        """This heavy lifter function converts coordinates in fixtures"""
        (x, y) = coord
        (big_x, big_y) = big_coord

        x -= (big_x * TRI_GEN)    # Remove big-grid offsets
        y -= (big_y * TRI_GEN)    # Remove big-grid offsets

        # Fix downward pointing grids
        if not point_up(big_coord):    # odd = pointing down
            y = TRI_GEN - y - 1
            direction = 'R' if direction == 'L' else 'L'  # Swap the light direction: L -> R and R -> L

        rowflip = 1 if direction == 'R' else 0  # Left-right direction of wiring

        # y row coordinate first. We're building up LEDs one row at a time.
        fix = 0
        for row in range(y):
            fix += row_width(row)

        # add x column coordinate. Even rows serpentine back
        if y % 2 == rowflip:    # even
            fix += (row_width(y) - (x-y) - 1)
        else:   # odd
            fix += (x-y)

        # Coordinate transformation depending on how the Triangle is hung
        if corner == 'C':
            return ROTATE_CLOCK[fix]
        elif corner == 'R':
            if direction == 'L':
                return fix
            else:
                return ROTATE_COUNTER[fix]

        else:
            if direction == 'L':
                return ROTATE_COUNTER[fix]
            else:
                return fix

    def get_row(self, row):
        """Return all (x,y) coordinates on a row (y)
           Terrible hack here because not all keys are well-defined tuples"""
        return [(coord[0], coord[1]) for coord in self.all_cells() if isinstance(coord, tuple) and row == coord[1]]

    def is_on_board(self, coord):
        """Return true if coordinate is between min and max of that row"""
        (x, y) = coord
        row_cells = self.get_row(y)

        if not row_cells:
            return False

        row_xs = [row_x for (row_x, row_y) in row_cells]
        min_x, max_x = min(row_xs), max(row_xs)

        return min_x <= x <= max_x

    def six_mirror(self, coord):
        """Return the six-fold mirror coordinates"""
        mirrors = sum([[cell, vert_mirror(cell)] for cell in self.mirror_coords(coord)], [])
        return mirrors

    def mirror_coords(self, coord):
        """Return the coordinate with its two mirror coordinates"""
        if not self.cell_exists(coord):
            return [coord] * 3  # Don't mirror
        return [coord, self.rotate_left(coord), self.rotate_right(coord)]

    def rotate_right(self, coord):
        """Rotates a coord right in its triangle space"""
        return self.rotate_left(self.rotate_left(coord))

    def rotate_left(self, coord):
        """Rotates a coord left in its triangle space"""
        strip = self.get_strip_from_coord(coord)
        reduced_coord = reduce_coord(coord, strip)
        rotated_coord = ROTATE_COORD_CLOCK[reduced_coord]
        expanded_coord = expand_coord(rotated_coord, strip)
        #print coord, reduced_coord, rotated_coord, expanded_coord
        return expanded_coord


##
## tri cell primitives
##
def point_up(coord):
    (x, y) = coord
    return (x+y) % 2 == 0


def get_big_coord(strip):
    ((big_x, big_y), corner, direction) = BIG_COORD[strip]
    return big_x, big_y


def row_width(row):
    return ((TRI_GEN - row - 1) * 2) + 1


def vert_mirror(coord):
    """Return the vertical mirror"""
    (x, y) = coord
    return row_width(y) - x - 1, y


def min_max_row():
    """Return the (minimum, maximum) row (y) values"""
    big_ys = [big_y for ((big_x, big_y), corner, direction) in BIG_COORD]
    min_y, max_y = min(big_ys), max(big_ys)

    return min_y * TRI_GEN, (max_y * TRI_GEN) + (TRI_GEN - 1)


def min_max_column():
    """Return the (minimum, maximum) column (x) values"""
    big_xs = [big_x for ((big_x, big_y), corner, direction) in BIG_COORD]
    min_x, max_x = min(big_xs), max(big_xs)

    return min_x * TRI_GEN, (max_x + 2) * TRI_GEN


def get_base(strip):
    (big_x, big_y) = get_big_coord(strip)
    return big_x * TRI_GEN, big_y * TRI_GEN


def get_all_func(get_func):
    """
    Iterator over all Triangles
    Function must return a list of coordinates
    """
    return sum([get_func(tri) for tri in range(NUM_BIG_TRI)], [])


def reduce_coord(coord, strip=0):
    """Reduces a coordinate to (0,0) space"""
    (big_x, big_y) = get_big_coord(strip)
    (x, y) = coord

    x -= big_x * TRI_GEN
    y -= big_y * TRI_GEN

    if not point_up(get_big_coord(strip)):
        y = TRI_GEN - 1 - y

    return x, y


def expand_coord(coord, strip=0):
    """Expands a reduced coordinate back to its big-tri space"""
    (big_x, big_y) = get_big_coord(strip)
    (x, y) = coord

    if not point_up(get_big_coord(strip)):
        y = TRI_GEN - 1 - y

    x += big_x * TRI_GEN
    y += big_y * TRI_GEN

    return x, y


def center(strip=0):
    """Return a Triangle's center coordinate. Handles point-down triangles too"""
    coeff = 0.4 if point_up(get_big_coord(strip)) else 0.6
    (x, y) = get_base(strip)
    return x + TRI_GEN - 1, y + int(coeff * TRI_GEN)


def all_centers():
    return [center(strip) for strip in range(NUM_BIG_TRI)]


def corners(strip=0):
    """Return the 3 corner coordinates of a Triangle"""
    pad = TRI_GEN - 1
    (x, y) = get_base(strip)
    if point_up(get_big_coord(strip)):
        return [(x, y), (x+pad, y+pad), (x+pad+pad, y)]    # L,C,R
    else:
        return [(x, y+pad), (x+pad, y), (x+pad+pad, y+pad)]    # L,C,R


def all_corners():
    """Return the corners of all triangles"""
    return get_all_func(corners)


def left_corner(strip=0):
    return corners(strip)[0]


def center_corner(strip=0):
    return corners(strip)[1]


def right_corner(strip=0):
    return corners(strip)[2]


def all_left_corners():
    return [left_corner(strip) for strip in range(NUM_BIG_TRI)]


def all_center_corners():
    return [center_corner(strip) for strip in range(NUM_BIG_TRI)]


def all_right_corners():
    return [right_corner(strip) for strip in range(NUM_BIG_TRI)]


def edge(strip=0):
    """Return the edge pixel coordinates of a Triangle. Uses the 3 corners to draw each linear edge"""
    corns = corners(strip)
    width = row_width(0)-1

    if point_up(get_big_coord(strip)):
        return tri_in_line(corns[0], 1, width) + tri_in_line(corns[1], 5, width) + tri_in_line(corns[2], 3, width)
    else:
        return tri_in_line(corns[0], 5, width) + tri_in_line(corns[1], 1, width) + tri_in_line(corns[2], 3, width)


def all_edges():
    """Return all the edge pixels"""
    return get_all_func(edge)


def neighbors(coord):
    """Return a list of the three tris neighboring a tuple at a given coordinate"""
    (x, y) = coord

    if (x+y) % 2 == 0:  # Even
        _neighbors = [(1, 0), (0, -1), (-1, 0)]    # Point up
    else:
        _neighbors = [(1, 0), (0, 1), (-1, 0)]     # Point down

    return [(x+dx, y+dy) for (dx, dy) in _neighbors]


def tri_in_line(coord, direction, distance=0):
    """
    Return the coord and all pixels in the direction
    along the distance
    """
    cells = [coord]
    for i in range(distance):
        coord = tri_nextdoor(coord, direction)
        cells.append(coord)
    return cells


def tri_in_direction(coord, direction, distance=1):
    """
    Return the coordinates of the tri in a direction from a given tri.
    Direction is indicated by an integer
    There are 6 directions along hexagonal axes

     2  /\  1
     3 |  | 0
     4  \/  5

    """
    for i in range(distance):
        coord = tri_nextdoor(coord, direction)
    return coord


def tri_nextdoor(coord, direction):
    """
    Return the coordinates of the adjacent tri in the given direction
    Even (point up) and odd (point down) tri behave different
    Coordinates determined from a lookup table
    """
    _evens = [(1, 0), (1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1)]
    _odds  = [(1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0), (1, 0)]

    (x, y) = coord

    if (x+y) % 2 == 0:  # Even
        (dx, dy) = _evens[direction % 6]
    else:
        (dx, dy) = _odds[direction % 6]

    return x+dx, y+dy


def get_rand_neighbor(coord):
    """
    Return a random neighbors
    Neighbor may not be in bounds
    """
    return choice(neighbors(coord))


def clock(coord, center_coord):
    """Return the clockwise cell (dir + 2)"""
    return get_adj_cell(coord, center_coord, 2)


def counterclock(coord, center_coord):
    """Return the counterclockwise cell (dir + 1)"""
    return get_adj_cell(coord, center_coord, 1)


def get_adj_cell(coord, center_coord, clock_pos):
    _neighbors = neighbors(coord)
    closest = near_neighbor(coord, center_coord)

    for i in range(3):
        if closest == _neighbors[i]:
            return _neighbors[(i + clock_pos) % 3]

    print("can't find a cell for {} pos".format(clock_pos))
    return coord


def near_neighbor(coord, center_coord):
    """Return the neighbor of coord that is closest to center"""
    nearest = sorted(neighbors(coord), key=lambda cell: distance(cell, center_coord))[0]
    return nearest


def get_ring(center_coord, size):
    """Return a list of coordinates that make up a centered ring"""
    size = 1 + (2 * size)  # For hex shape

    t = tri_in_direction(center_coord, 4, size)
    results = []
    for i in range(6):
        for j in range(size):
            results.append(t)
            t = tri_nextdoor(t, i)
    return results


def tri_shape(start, size):
    """
    Return a list of coordinates that make up a triangle
    Triangle's left corner will be the 'start' pixel
    start's location will determine whether triangle points up or down
    Update: rewritten so cells go around in a loop
    """
    size = 2 * (size - 1)
    x = 1 if point_up(start) else 0

    return (tri_in_line(start, x, size) +
            tri_in_line(tri_in_direction(start, x, size), x+4, size) +
            tri_in_line(tri_in_direction(start, x-1, size), x+2, size))


def nested_triangles(start):
    """
    Return a list of lists of coordinates,
    A list of concentric triangles with the largest first
    with each triangle centered in the middle
    Triangle's left corner will be the 'start' pixel
    """
    left_corn = start
    direction = 1 if point_up(start) else 5

    cells = []
    for size in range(TRI_GEN, 0, -3):
        cells.append(tri_shape(left_corn, size))
        left_corn = tri_in_direction(tri_in_direction(left_corn, direction, 2), 0, 2)

    return cells


def inset_triangles(start, num_triangles=TRI_GEN):
    """
    Return a list of lists of coordinates,
    A list of inset triangles with the largest first
    with each triangle offset by 'direction'
    Triangle's left corner will be the 'start' pixel
    """
    left_corn = start

    cells = []
    for size in range(num_triangles, 0, -2):
        cells.append(tri_shape(left_corn, size))
        left_corn = tri_in_direction(left_corn, 0, 2)

    return cells
