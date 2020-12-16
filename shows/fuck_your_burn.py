from itertools import repeat, chain
from collections.abc import Iterable

from color import HSV
from grid import Position, Pyramid
import ponzicolor
from ponzicolor import Color
from randomcolor import random_color
from .show import Show


class FuckYourBurn(Show):
    def __init__(self, pyramid: Pyramid):
        self.grid = pyramid.panel
        self.frame_delay = 1.0
        self.background_color = HSV(0, 0, 0)
        self.foreground_color = random_color(hue='green')

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

    @property
    def background(self):
        vals = self.background_color.hsv
        return Color.from_hsv(ponzicolor.space.HSV(h=vals[0]*360, s=vals[1], v=vals[2]))

    @property
    def foreground(self):
        vals = self.foreground_color.hsv
        return Color.from_hsv(ponzicolor.space.HSV(h=vals[0]*360, s=vals[1], v=vals[2]))

    def next_frame(self):

        letters = (self.fu, self.ck, self.yo, self.ur, self.bu, self.rn)

        self.grid.clear(self.background)

        # Function variable to return past frame's letters, as an optimization for clearing them
        def prev() -> Iterable[Position]:
            return []

        for curr in chain.from_iterable(repeat(letters)):
            background = self.background
            foreground = self.foreground

            # Fade out
            for i in range(1, 11):
                if not prev():
                    continue
                color = foreground.blend(background, i/10).clamp()
                [self.grid.set(pos, color) for pos in prev()]
                self.grid.go()
                yield 0.01

            # Fade in
            for i in range(1, 11):
                color = background.blend(foreground, i/10).clamp()
                [self.grid.set(pos, color) for pos in curr()]
                self.grid.go()
                yield 0.01

            prev = curr
            yield self.frame_delay
