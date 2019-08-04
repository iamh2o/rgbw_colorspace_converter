from itertools import chain
from typing import List, Mapping, NamedTuple


class Position(NamedTuple):
    row: int
    col: int

    @property
    def x(self) -> int:
        return self.col

    @property
    def y(self) -> int:
        return self.row


UNIVERSES = {
    1: 512,
    2: 512,
    3: 44 * 4,
    4: 512,
    5: 512,
    6: 44 * 4,
    7: 512,
    8: 512,
    9: 44 * 4,
    10: 512,
    11: 512,
}


class Address(NamedTuple):
    universe: int
    offset: int

    @property
    def next(self) -> "Address":
        next_offset = self.offset + 4
        if next_offset >= UNIVERSES[self.universe]:
            return Address(self.universe + 1, 0)

        return Address(self.universe, next_offset)

    def range(self, len: int) -> List["Address"]:
        addrs = [self]
        for _ in range(len - 1):
            addrs.append(addrs[-1].next)

        return addrs


def generate(rows: int = 11, start: Address = Address(1, 4)) -> Mapping[Position, List[Address]]:
    cells = {}
    for row in range(rows - 1, -1, -1):
        row_mapping = mouth(row, start)
        cells.update(row_mapping)

        end_address = max(chain.from_iterable(row_mapping.values()))
        start = end_address.next

    return cells


def mouth(row: int, start: Address) -> Mapping[Position, List[Address]]:
    up = up_teeth(row, start, row + 1)
    last_up_address = up[max(up)][-1]
    first_after_gap = last_up_address.range(11)[-1]
    down = down_teeth(row, first_after_gap, row)

    return {**up, **down}


def up_teeth(row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, List[Address]]:
    cells = {}
    addr = start

    for i in range(length):
        addrs = addr.range(pixels_per_cell)
        cells[Position(row, i * 2)] = addrs
        addr = addrs[-1].next

    return cells


def down_teeth(row: int, start: Address, length: int, pixels_per_cell: int = 8) -> Mapping[Position, List[Address]]:
    cells = {}
    addr = start

    col = length * 2 - 1
    for i in range(length):
        addrs = addr.range(pixels_per_cell)
        cells[Position(row, col)] = addrs
        col -= 2
        addr = addrs[-1].next

    return cells


CELLS = generate()
