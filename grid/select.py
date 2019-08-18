from typing import Iterable, List, NamedTuple, Sequence

from .cell import Cell, Orientation
from .grid import Grid, Position, Query, Location


def query(grid: Grid, q: Query) -> Iterable[Cell]:
    return q(grid)


def every(grid: Grid) -> List[Cell]:
    return grid.cells


def on_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_edge]


def left_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_left_edge]


def right_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_right_edge]


def bottom_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_bottom_edge]


def inset(distance: int) -> Query:
    """
    Selects an inner triangle, `distance` cells away from the edges.
    """

    def query(grid: Grid) -> List[Cell]:
        # find the top point
        top_row = distance * 2
        top_col = grid.geom.midpoint(top_row)
        cells = {grid[Position(top_row, top_col)]}
        edge_cells = set()

        bottom_row = grid.row_count - distance - 1
        for prev_row in range(top_row, bottom_row):
            prev_cells = [c for c in cells if c.row == prev_row]
            edge_cells = {min(prev_cells), max(prev_cells)}
            midpoint = grid.geom.midpoint(prev_row)

            for cell in edge_cells:
                below = cell.below
                if below is None:
                    continue

                # TODO(lyra): grid[grid[]] ugh
                if cell.col <= midpoint:
                    cells.add(grid[below])
                    cells.add(grid[grid[below].left])
                if cell.col >= midpoint:
                    cells.add(grid[below])
                    cells.add(grid[grid[below].right])

        if not edge_cells:
            return []

        for col in range(min(edge_cells).col, max(edge_cells).col + 1):
            cells.add(grid[Position(bottom_row, col)])

        return list(cells)

    return query


def pointed(orientation: Orientation) -> Query:
    def query(grid: Grid) -> List[Cell]:
        return [cell for cell in grid.cells if cell.orientation is orientation]

    return query


def pointed_up(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_up]


def pointed_down(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_down]


class Neighbors(NamedTuple):
    left: Cell
    middle: Cell
    right: Cell


def edge_neighbors(loc: Location) -> Query:
    """
    Queries a tuple of (left, middle, right) cells that share an edge with the given (row, column) cell.

    Left neighbor is the edge directly to the left of the cell, regardless of up/down orientation.
    Middle neighbor is either the top or bottom neighbor depending where the edge is.
    Right neighbor is the cell immediately to the right.
    """

    def query(grid: Grid) -> Neighbors:
        cell = grid.get(loc)
        if cell is None:
            return Neighbors(None, None, None)

        pos = cell.position

        left = grid.get(pos.adjust(0, -1))
        middle = (grid.get(pos.adjust(1, 1))
                  if cell.is_up
                  else grid.get(pos.adjust(-1, -1)))
        right = grid.get(pos.adjust(0, 1))

        return Neighbors(left, middle, right)

    return query


def vertex_neighbors(loc: Location) -> Query:
    """
    Queries a tuple of (left, middle, right) cells that share a vertex with the given (row, column) cell.

    Left neighbor is the cell opposite the left vertex of the given cell.
    Middle neighbor is the cell opposite the middle (up or down) vertex of the given cell.
    Right neighbor is the cell opposite the right vertex of the given cell.
    """

    def query(grid: Grid) -> Neighbors:
        cell = grid.get(loc)
        if cell is None:
            return Neighbors(None, None, None)

        pos = cell.position

        if cell.is_up:
            left = grid.get(pos.adjust(1, -1))
            middle = grid.get(pos.adjust(-1, -1))
            right = grid.get(pos.adjust(1, 3))
        else:
            left = grid.get(pos.adjust(-1, -2))
            middle = grid.get(pos.adjust(1, 1))
            right = grid.get(pos.adjust(-1, 1))

        return Neighbors(left, middle, right)

    return query


def hexagon(base_loc: Location) -> Query:
    """
    Selector for hexagon pattern of cells surrounding a starting cell.

    Given a starting location, returns a function
        func(Grid) -> [Neighbor, Neighbor, Neighbor, Neighbor, Neighbor, Neighbor]
    The neighbors, surrounding cells, make a hexagon with the starting location cell as the base. For neighbor cells
    off the grid, 'None' is returned.

    For example, starting with an up-facing cell, numbered with 1's here, there would be a total of 6 neighbors in the
    hexagon (including cell 1), in a clock-wise order. Here's an attempt at a drawing of neighbors 1, 2, 3, 4, 5, and 6:

      5 444 3
     555 4 333
     666 1 222
      6 111 2
    """
    def hexagon_query(grid: Grid) -> Sequence[Cell]:
        # Helper function that returns edge neighbors (sharing a wall with) of a given cell.
        def neighbors(cell) -> Neighbors:
            return Neighbors(*query(grid, edge_neighbors(cell.id)))

        btm_cell = grid[base_loc]
        a, b, c, d, e, f = btm_cell, None, None, None, None, None

        if a.is_left_edge:
            b = neighbors(a).right
            if b is not None:
                c = neighbors(b).middle
            if c is not None:
                d = neighbors(c).left
            if d is not None:
                e = neighbors(d).left
            if e is not None:
                f = neighbors(e).middle

        elif a.is_right_edge:
            f = neighbors(a).left
            if f is not None:
                e = neighbors(f).middle
            if e is not None:
                d = neighbors(e).right
            if d is not None:
                c = neighbors(d).right
            if c is not None:
                b = neighbors(c).middle
        else:
            b = neighbors(a).right
            c = neighbors(b).middle
            d = neighbors(c).left
            e = neighbors(d).left
            f = neighbors(e).middle

        hexa = list(filter(None, [a, b, c, d, e, f]))
        return hexa

    return hexagon_query
