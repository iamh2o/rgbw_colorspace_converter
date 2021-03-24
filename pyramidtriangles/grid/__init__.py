"""
The grid package contains all the classes for navigating, selecting, and setting colors for aspects
of the triangles.

# Terminology

## Classes to set/get color on triangle panels

* Grid is an abstract mapping of Location to Cell(s). Grids are also used to lookup or set colors for
cells. These methods are available on other Grid types.

* Panel is a type of Grid for one large triangle light fixture, with 11 rows.

* Face is a type of Grid for one side of the pyramid. It contains multiple panels with significant
dead space between them.

* Pyramid represents the whole pyramid with multiple sides. Each panel is accessible, though
typically shows will address one face or one panel as their canvas. Then the data from that one
face or one panel will be mirrored to the other faces and panels. Pyramid has attributes
`pyramid.faces`, `pyramid.face`, and `pyramid.panel` to access these respectively. Every show can
access the Pyramid.

## Triangle cells

* Cell is a class referring to a "cell" (mini-triangle) within one of the panels. Cells are used to
navigate to other cells. To get/set the color of a Cell, use a type of Grid to `grid.get(cell)` or
`grid.set(cell, color)`.

* Pixel is an addressable pixel within a cell. Because cells are physically diffused together, it
is less useful to access individual pixels, though still available.

## Locations

* Coordinate is an (x, y) coordinate, where the left-bottom triangle is (0, 0). Create a
coordinate for (2, 3) with `Coordinate(2, 3)`.

* Position is a (row, column) position, where the top row is 0, and every row begins with column 0.
Create the apex position with `Position(0, 0)`.

* Cell ID is an integer to identify a single cell. It is only used by the simulator.

# Basic usage

Every Show has access to the Pyramid. Suppose the show will use one panel as a canvas and mirror
that data to all other panels.

```
class ExampleShow(Show):
    def __init__(self, pyramid):
        self.grid = pyramid.panel
```

The show can clear or initialize the grid (a replicated panel in this case).

```
self.grid.clear()               # sets all cells to black
self.grid.clear(HSV(.5,.5,.5))  # sets all cells to a color
```

Then the show will start at the triangle apex and color all cells in a vertical line.

```
apex_coordinate = self.grid.geom.apex
apex_cell = self.grid[apex_coordinate]
cells_to_paint = [apex_cell]
curr_cell = apex_cell
while curr_cell.below:
    cells_to_paint.append(curr_cell.below)
    curr_cell = curr_cell.below
self.grid.set(cells_to_paint, HSV(.6,.6,.6))
```

# Selects

The select module contains various functional tools to selecting cells. Each function returns a
list of cells when called with a grid. These call be used with a grid similar to how a Coordinate
is used.

For example, `select.every` is the simplest select. It returns every Cell in a grid. It can be
used to set every Cell a color with the following.

```
self.grid.set(select.every, HSV(.4,.4,.4))
```

Similarly, to set all bottom edge Cells the same color, use:

```
self.grid.set(select.bottom_edge, HSV(.4,.4,.4))
```

There are select function for finding the neighboring Cells to a Location, triangular inset cells,
and hexagonal neighbor cells to a base location.

Please add more select functions if you find any you use repeatedly.

# Traversals

Traversals are functional tools, similar to selects. The difference with traversals is they return
a sequence of locations.
"""
from .cell import Cell, Direction, Orientation
from .face import Face
from .geom import Address, Coordinate, Geometry, Position, Universe
from .grid import Grid, Location, Pixel, Query, Selector
from .pyramid import Pyramid
from .select import (every, on_edge, left_edge, right_edge, bottom_edge, inset, pointed,
                     pointed_up, pointed_down, edge_neighbors, vertex_neighbors, hexagon)
