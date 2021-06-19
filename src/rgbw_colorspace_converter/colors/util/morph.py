"""
Functions to generate attractive 'morphs' between colors

All morphs are simple linear progressions between 2 or more points
in the HSV colorspace.  These functions merely produce sequences of
colors - determining the time each color should be shown or
the overall duration of the animation is a detail that the library
user must handle.

All functions take and return Color objects

There are two main functions you'll want to use.  The first
generates a simple linear transition between two Colors:

- color_transition(start_color, end_color, steps=20)

The second generates a transition between a list of colors:

- multistep_color_transition(rgb_points, steps=20, continuous=False)

Takes a list of Color points and returns a sequence that
transitions between all points.
Can optionally generate a sequence that cycles, returning an
infinite list of colors useful for indefinite length
animations
"""


import itertools

from math import ceil

from rgbw_colorspace_converter.colors.converters import HSV
from rgbw_colorspace_converter.colors.converters import Color

__all__ = ["color_transition", "multistep_color_transition"]

# http://stackoverflow.com/questions/477486/python-decimal-range-step-value
def frange(start, stop=None, step=1):
    """frange generates a set of floating point values over the
    range [start, stop) with step size step

    frange([start,] stop [, step ])"""
    if stop is None:
        for x in range(int(ceil(start))):
            yield x
    else:
        # create a generator expression for the index values
        indices = (i for i in range(0, int((stop - start) / step)))
        # yield results
        for i in indices:
            yield start + step * i


def should_wrap(p1, p2):
    # is the distance going in a negative direction around the hsv circle shorter?
    if p1 > p2:
        p1, p2 = p2, p1
    return abs(p2 - p1) > abs((p1 + 1) - p2)


def hsv_transition(h1, h2, steps=20, wrap=False):
    """
    Transition between two values in even increments
    If wrap=True, treat 0.0 == 1.0 and try to determine
    the shortest distance around the colorspace
    (only for hue in HSV, I don't think anything else
    needs to wrap.
    """
    # print "transition:", h1, h2, steps
    if h1 == h2:
        return itertools.repeat(h1, steps + 1)  # XXX check number of steps!
    else:
        if wrap and should_wrap(h1, h2):
            if h1 < h2:
                h1 += 1.0
            else:
                h2 += 1.0

        dh = abs(h1 - h2)
        step_size = dh / steps
        if h1 > h2:
            step_size *= -1
        return frange(h1, h2, step_size)


def pairwise(iterable):  # from the itertools documentation
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def color_transition(start_color, end_color, steps=20):
    """
    Takes two Color objects and produce a sequence of colors that
    transition between them.  `steps` specifies the number of
    intermediate steps in the sequence.
    """
    assert isinstance(start_color, Color), "start_color must be a Color instance"
    assert isinstance(end_color, Color), "end_color must be a Color instance"

    h1, s1, v1 = start_color.hsv
    h2, s2, v2 = end_color.hsv

    h_seq = hsv_transition(h1, h2, steps, wrap=True)
    s_seq = hsv_transition(s1, s2, steps)
    v_seq = hsv_transition(v1, v2, steps)

    for (h, s, v) in zip(h_seq, s_seq, v_seq):
        yield HSV(h % 1, s, v)


def multistep_color_transition(color_list, steps=20, continuous=False):
    """
    Takes a list of Colors and returns a sequence of Colors that
    transitions between them.
    `steps` indicates the number of intermediate steps between each
    color in the list.
    `continuous` will create an infinite sequence
    """
    if continuous and color_list[0] != color_list[-1]:
        # smooth things out with a transition back to the first color
        color_list.append(color_list[0])
    transitions = [color_transition(a, b, steps) for (a, b) in pairwise(color_list)]
    chain = itertools.chain.from_iterable(transitions)
    if continuous:
        chain = itertools.cycle(chain)
    return chain
