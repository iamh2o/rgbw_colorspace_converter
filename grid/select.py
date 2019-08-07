
from typing import Iterable, List, NamedTuple, Sequence, Tuple

from .cell import Cell, Orientation, row_length
from .grid import Grid, Query, Location


def query(grid: Grid, q: Query) -> Iterable[Cell]:
    return q(grid)


def every(grid: Grid) -> List[Cell]:
    return grid.cells


def left_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_left_edge]


def right_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_right_edge]


def bottom_edge(grid: Grid) -> List[Cell]:
    return [cell for cell in grid.cells if cell.is_bottom_edge]


def pointed(orientation: Orientation) -> Query:
    def query(grid: Grid) -> List[Cell]:
        return [cell for cell in grid.cells if cell.orientation is orientation]


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
    def hexagon_query(grid: Grid) -> Sequence[Cell]:
        def neighbors(cell) -> Neighbors:
            return Neighbors(query(grid, edge_neighbors(cell.id)))

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

        return (a, b, c, d, e, f)

    return hexagon_query
