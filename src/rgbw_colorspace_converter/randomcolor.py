"""
randomColor.py

Python translation of randomColor.js
http://llllll.li/randomColor/
https://github.com/davidmerfield/randomColor

randomColor generates attractive colors by default. More specifically,
it produces bright colors with a reasonably high saturation.

    c = random_color()
    print c.rgb

You can also specify a hue or luminosity to constrain
the colors generated:

Hue can be: 'red', 'orange', 'yellow', 'green', 'blue', 'purple',
'pink' or 'monochrome'

    c = random_color('red')

Luminosity can be: 'bright', 'light', 'dark', 'random'

    c = random_color(luminosity='light')

"""


from collections import namedtuple
from numbers import Number
import itertools
import random

from color import HSV

__all__ = ["random_color"]


def random_within(_min, _max):
    "Return a random number within two values, inclusive of those values"
    return random.randrange(int(_min), int(_max) + 1)


ColorDef = namedtuple(
    "ColorDef", ["hue_range", "lower_bounds", "saturation_range", "brightness_range"]
)


def define_color(hue_range, lower_bounds):
    s_min = lower_bounds[0][0]
    s_max = lower_bounds[-1][0]

    b_min = lower_bounds[-1][1]
    b_max = lower_bounds[0][1]

    return ColorDef(
        hue_range=hue_range,
        lower_bounds=lower_bounds,
        saturation_range=(s_min, s_max),
        brightness_range=(b_min, b_max),
    )


def make_color_bounds():
    COLOR_BOUNDS = [
        # name,   hue_range, lower_bounds
        ("monochrome", None, [[0, 0], [100, 0]]),
        (
            "red",
            [-26, 18],
            [
                [20, 100],
                [30, 92],
                [40, 89],
                [50, 85],
                [60, 78],
                [70, 70],
                [80, 60],
                [90, 55],
                [100, 50],
            ],
        ),
        (
            "orange",
            [19, 46],
            [[20, 100], [30, 93], [40, 88], [50, 86], [60, 85], [70, 70], [100, 70]],
        ),
        (
            "yellow",
            [47, 62],
            [
                [25, 100],
                [40, 94],
                [50, 89],
                [60, 86],
                [70, 84],
                [80, 82],
                [90, 80],
                [100, 75],
            ],
        ),
        (
            "green",
            [63, 178],
            [
                [30, 100],
                [40, 90],
                [50, 85],
                [60, 81],
                [70, 74],
                [80, 64],
                [90, 50],
                [100, 40],
            ],
        ),
        (
            "blue",
            [179, 257],
            [
                [20, 100],
                [30, 86],
                [40, 80],
                [50, 74],
                [60, 60],
                [70, 52],
                [80, 44],
                [90, 39],
                [100, 35],
            ],
        ),
        (
            "purple",
            [258, 282],
            [
                [20, 100],
                [30, 87],
                [40, 79],
                [50, 70],
                [60, 65],
                [70, 59],
                [80, 52],
                [90, 45],
                [100, 42],
            ],
        ),
        (
            "pink",
            [283, 334],
            [[20, 100], [30, 90], [40, 86], [60, 84], [80, 80], [90, 75], [100, 73]],
        ),
    ]

    dat = {}
    for (name, hue_range, lower_bounds) in COLOR_BOUNDS:
        dat[name] = define_color(hue_range, lower_bounds)
    return dat


COLOR_DICT = make_color_bounds()


def get_color_info(hue):
    # XXX takes int 0-360

    # hacky method of not having to store two ranges for red
    if 334 <= hue <= 360:
        hue -= 360

    for (name, color) in list(COLOR_DICT.items()):
        if color.hue_range and hue >= color.hue_range[0] and hue <= color.hue_range[1]:
            return color

    raise Exception("No color found for hue=%d" % hue)


def get_saturation_range(hue):
    # takes a hue int[0-360]
    # XXX what's the valid range for saturation values?
    try:
        return get_color_info(hue).saturation_range  # XXX
    except Exception as e:
        del e
        print("exception in get_saturation_range for hue=", hue)
        return (0, 100)


def get_hue_range(cin):
    # XXX what format is this?
    # returns (hue_min, hue_max)
    if isinstance(cin, Number):
        i = int(cin)
        if 0 > i > 360:
            return (i, i)

    if isinstance(cin, str):
        if cin in COLOR_DICT:
            return COLOR_DICT[cin].hue_range

    return (0, 360)


def pairwise(iterable):  # from the itertools documentation
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def get_minimum_brightness(h, s):
    # h is int[0,360]
    # s is ????
    lower_bounds = get_color_info(h).lower_bounds

    for (sv1, sv2) in pairwise(lower_bounds):
        s1, v1 = sv1
        s2, v2 = sv2

        if s1 <= s <= s2:
            m = (v2 - v1) / (s2 - s1)
            b = v1 - (m * s1)
            return m * s + b

    return 0


def pick_brightness(h, s, luminosity=None):
    b_min = get_minimum_brightness(h, s)
    b_max = 100

    if luminosity == "dark":
        b_max = b_min + 20
    elif luminosity == "light":
        b_min = (b_max + b_max) / 2
    elif luminosity == "random":
        b_min = 0
        b_max = 100

    # print "brightness range:", (b_min, b_max)

    return random_within(b_min, b_max)


def pick_saturation(h, hue=None, luminosity=None):
    if luminosity == "random":
        return random_within(0, 100)

    if hue == "monochrome":
        return 0

    (s_min, s_max) = get_saturation_range(h)

    if luminosity == "bright":
        s_min = 55
    elif luminosity == "dark":
        s_min = s_max - 10
    elif luminosity == "light":
        s_max = 55

    return random_within(s_min, s_max)


def pick_hue(hue):
    (hue_min, hue_max) = get_hue_range(hue)
    h = random_within(hue_min, hue_max)

    if h < 0:
        h += 360

    return h


def random_color(hue=None, luminosity=None):
    """
    Return a random color, by default a bright and highly
    saturated color.

    'hue' can be: 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'monochrome'
    'luminosity' can be: 'bright', 'light', 'dark', 'random'
    """
    h = pick_hue(hue)
    s = pick_saturation(h, hue, luminosity)
    v = pick_brightness(h, s, luminosity)

    h = h / 360
    s = s / 100
    v = v / 100

    return HSV(h, s, v)
