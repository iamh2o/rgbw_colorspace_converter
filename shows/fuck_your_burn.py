from itertools import repeat, chain

from color import RGB
from grid import Grid, Position, Pyramid
from randomcolor import random_color
from .show import Show


class FuckYourBurn(Show):
    grid: Grid

    def __init__(self, pyramid: Pyramid):
        self.grid = pyramid.panel
        self.frame_delay = 1.0

    @staticmethod
    def description() -> str:
        return 'FUCK YOUR BURN, two letters at a time, on repeat'

    @staticmethod
    def fu():
        positions = (
            (5, 2), (5, 3), (5, 4), (5, 5),
            (6, 2), (6, 3),
            (7, 2), (7, 3), (7, 4), (7, 5), (7, 8), (7, 9), (7, 12), (7, 13),
            (8, 2), (8, 3), (8, 8), (8, 9), (8, 12), (8, 13),
            (9, 2), (9, 3), (9, 8), (9, 9), (9, 12), (9, 13),
            (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13)
        )
        return [Position(row, col) for row, col in positions]

    @staticmethod
    def ck():
        positions = (
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            (5, 0), (5, 1),
            (6, 0), (6, 1), (6, 8), (6, 9), (6, 12),
            (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13),
            (8, 8), (8, 9), (8, 11), (8, 12),
            (9, 8), (9, 9), (9, 12), (9, 13)
        )
        return [Position(row, col) for row, col in positions]

    @staticmethod
    def yo():
        positions = (
            (5, 2), (5, 3), (5, 6), (5, 7),
            (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
            (7, 4), (7, 5), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13),
            (8, 4), (8, 5), (8, 8), (8, 9), (8, 12), (8, 13),
            (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13),
        )
        return [Position(row, col) for row, col in positions]

    @staticmethod
    def ur():
        positions = (
            (4, 0), (4, 1), (4, 4), (4, 5),
            (5, 0), (5, 1), (5, 4), (5, 5),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12),
            (7, 8), (7, 9), (7, 12), (7, 13),
            (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13),
            (9, 8), (9, 9), (9, 11), (9, 12),
            (10, 8), (10, 9), (10, 13), (10, 14)
        )
        return [Position(row, col) for row, col in positions]

    @staticmethod
    def bu():
        positions = (
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4),
            (5, 0), (5, 1), (5, 4), (5, 5),
            (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5),
            (7, 0), (7, 1), (7, 4), (7, 8), (7, 9), (7, 12), (7, 13),
            (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 8), (8, 9), (8, 12), (8, 13),
            (9, 8), (9, 9), (9, 12), (9, 13),
            (10, 8), (10, 9), (10, 10), (10, 11), (10, 12), (10, 13)
        )
        return [Position(row, col) for row, col in positions]

    @staticmethod
    def rn():
        positions = (
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            (3, 0), (3, 1), (3, 4), (3, 5),
            (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            (5, 0), (5, 1), (5, 3), (5, 4),
            (6, 0), (6, 1), (6, 5), (6, 6),
            (7, 8), (7, 9), (7, 10), (7, 14),
            (8, 8), (8, 9), (8, 11), (8, 12), (8, 14), (8, 15),
            (9, 8), (9, 9), (9, 13), (9, 14), (9, 15)
        )
        return [Position(row, col) for row, col in positions]

    def next_frame(self):
        background = RGB(0, 0, 0)
        color = random_color(hue='purple')

        letters = (self.fu, self.ck, self.yo, self.ur, self.bu, self.rn)

        while True:
            self.grid.clear(background)

            def prev():
                return []

            for curr in chain.from_iterable(repeat(letters)):
                [self.grid.set(pos, background) for pos in prev()]
                [self.grid.set(pos, color) for pos in curr()]
                prev = curr

                self.grid.go()
                yield self.frame_delay
