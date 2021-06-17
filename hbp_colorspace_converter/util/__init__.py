import random

from ..color import HSV


def choose_random_hsv():
    return HSV(
        random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)
    )


# http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
def make_interpolator(in_min, in_max, out_min, out_max):
    """Return a function that translates from one range to another"""
    # Figure out how wide each range is
    inSpan = in_max - in_min
    outSpan = out_max - out_min

    # Compute the scale factor between left and right values
    scaleFactor = float(outSpan) / float(inSpan)

    return lambda value: out_min + (value - in_min) * scaleFactor
