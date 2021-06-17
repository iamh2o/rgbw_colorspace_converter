from __future__ import annotations
from collections.abc import Sequence
from itertools import islice

from .color import Color


class Scale:
    """
    Scale is a linear color gradient.
    """

    points: list[tuple[Color, float]]

    @classmethod
    def of(cls, *colors: Color) -> Scale:
        return cls.linear(colors)

    @classmethod
    def linear(cls, colors: Sequence[Color]) -> Scale:
        s = 1.0 / len(colors)
        return cls([(color, i * s) for i, color in enumerate(colors)])

    def __init__(self, points: Sequence[tuple[Color, float]]):
        self.points = list(points)

    def __call__(self, t: float) -> Color:
        if t < 0.0 or t > 1.0:
            raise ValueError(f"Scale must be called with 0 ≤ t ≤ 1, not {t}.")

        for (c1, p1), (c2, p2) in zip(self.points, islice(self.points, 1, None)):
            if p1 <= t <= p2:
                bias = (t - p1) / (p2 - p1)
                return c1.blend(c2, bias).clamp()
        else:
            return self.points[-1][0]
