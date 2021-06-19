"""
Color

Color class that allows you to ** initialize ** a color in any of HSL, HSV, RGB, Hex and HSI color spaces.  Once initialized,with one of these specific types, you get a Color object back (or possibly a subclass of the Color objext- RGB or HSV- all the same ).  This object will automatically report the color space values for all color spaces based on what you entered.  Notably, it will also translate to RGBW!

Further, from the returned object, you may modify it in 2 ways-  via the r/g/b properties of the RGB Color object, or via the h/s/v properties of the HSV color object. Any changes in any of the r/g/b or h/s/v properties (even if mixed and matched) will automatically re-calculate the correct values for the other color space represnetations, which can then be accessed.  You can not modify the other color space object properties and get the same effect (yet).



The main goal of this package is to translate various color spaces into RGBW for use in RGBW LED or DMX/RGB accepting hardware.  There is a strange dearth of translators from ANY color space to RGBW.


The color representation is maintained in HSV interanlly and translates to RGB (and RGBW and the other spaces).
Use whichever is more convenient at the time - RGB for familiarity, HSV to fade and move more naturally through the color space.  We have found, once used to it, HSV is the far superiour space to work in.

RGB values range from 0 to 255
HSV values range from 0.0 to 1.0  # Note- any of the HS* color spaces which used 360degree represntations for H, we normalize to 0-1 to be easier to use in loops and be consistent with the S/[L|V|I] values.

# INITIALIZING COLOR OBJECTS -- it is not advised to init Color directly. These below all basically return a valid Color obj
# RGBW can not be initialized directly-  it is calculate from the initialized, or modified values of the color objs below
from rgbw_colorspace_converter.colors.converters import RGB, HSV, HSL, HSI, Hex

    >>> red   = RGB(255, 0 ,0)
    >>> green = HSV(0.33, 1.0, 1.0)

Colors may also be specified as hexadecimal string:

    >>> blue  = Hex('#0000ff')

Both RGB and HSV components are available as attributes
and may be set.

    >>> red.rgb_r
    255

    >>> red.rgb_g = 128
    >>> red.rgb
    (255, 128, 0)

    >>> red.hsv
    (0.08366013071895424, 1.0, 1.0)

These objects are mutable, so you may want to make a
copy before changing a Color that may be shared

    >>> red = RGB(255,0,0)
    >>> purple = red.copy()
    >>> purple.rgb_b = 255
    >>> red.rgb
    (255, 0, 0)
    >>> purple.rgb
    (255, 0, 255)

Brightness can be adjusted by setting the 'v' property in the HSV object, even
when you're working in RGB, b/c again, the specific color spaces are all simply reporting the values for
the spaces they represent for the color being defined.  An RGB code has a HSV translation, if you then modify that HSV code, the RGB translation will change too.   This is a good use case if you work in RGB. It is hard to dim a color evenly in RGB, but if you create an RGB color you like, you can simply cycle down the color.hsv_v value and the color.rgb values will change to represent even dimming.

A trite example: to gradually dim a color
(ranges from 0.0 to 1.0)

    >>> col = RGB(0,255,0)
    >>> while col.hsv_v > 0:
    ...   print col.rgb
    ...   col.hsv_v -= 0.1
    ...
    (0, 255, 0)
    (0, 229, 0)
    (0, 204, 0)
    (0, 178, 0)
    (0, 153, 0)
    (0, 127, 0)
    (0, 102, 0)
    (0, 76, 0)
    (0, 51, 0)
    (0, 25, 0)

A more complex example is if you wished to move through HUE space in HSV and display that in RGB (or RGBW)

RGBW

To get the (r,g,b,w) tuples back from a Color object, simpy call Color.rgbw and you will return the (r,g,b,w) tuple.

"""

import colorsys
import math
from copy import deepcopy

__all__ = ["RGB", "HSV", "Hex", "Color", "HSI", "HSL"]


def clamp(val, min_value, max_value):
    "Restrict a value between a minimum and a maximum value"
    return max(min(val, max_value), min_value)


def is_hsv_tuple(hsv):
    "check that a tuple contains 3 values between 0.0 and 1.0"
    return len(hsv) == 3 and all([(0.0 <= t <= 1.0) for t in hsv])


def is_hsi_tuple(hsi):
    ret = True
    if len(hsi) != 3:
        ret = False
    if hsi[0] < 0 or hsi[0] > 360:
        ret = False
    if hsi[1] < 0.0 or hsi[1] > 1.0:
        ret = False
    if hsi[2] < 0.0 or hsi[2] > 1.0:
        ret = False

    return ret


def is_rgbw_tuple(rgbw):
    "check that rgbw tuple is as expected"
    return len(rgbw) == 4 and all([(0 <= t <= 255) for t in rgbw])


def is_rgb_tuple(rgb):
    "check that a tuple contains 3 values between 0 and 255"
    return len(rgb) == 3 and all([(0 <= t <= 255) for t in rgb])


def rgb_to_hsv(rgb):
    "convert a rgb[0-255] tuple to hsv[0.0-1.0]"
    f = float(255)
    return colorsys.rgb_to_hsv(rgb[0] / f, rgb[1] / f, rgb[2] / f)


def hsv_to_rgb(hsv):
    assert is_hsv_tuple(hsv), "malformed hsv tuple:" + str(hsv)
    _rgb = colorsys.hsv_to_rgb(*hsv)
    r = int(_rgb[0] * 0xFF)
    g = int(_rgb[1] * 0xFF)
    b = int(_rgb[2] * 0xFF)
    return (r, g, b)


def constrain(val, min, max):
    ret = val
    if val <= min:
        ret = min
    if val >= max:
        ret = max
    return ret


# https://www.neltnerlabs.com/saikoled/how-to-convert-from-hsi-to-rgb-white
def hsi2rgb(H, S, I):
    r = 0.0
    g = 0.0
    b = 0.0

    H = math.fmod(H, 360.0)
    H = 3.14159 * H / 180.0
    S = constrain(S, 0.0, 1.0)
    I = constrain(I, 0.0, 1.0)

    if H < 2.09439:
        r = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        g = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        b = 255.0 * I / 3.0 * (1.0 - S)
    elif H < 4.188787:
        H = H - 2.09439
        g = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        b = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        r = 255.0 * I / 3.0 * (1.0 - S)
    else:
        H = H - 4.188787
        b = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        r = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        g = 255.0 * I / 3.0 * (1.0 - S)

    return (
        constrain(int(r * 3.0), 0, 255),
        constrain(int(g * 3.0), 0, 255),
        constrain(int(b * 3.0), 0, 255),
    )  # for some reason, the rgb numbers need to be X3...


# https://www.neltnerlabs.com/saikoled/how-to-convert-from-hsi-to-rgb-white
def DELhsi2rgb(H, S, I):
    r = 0.0
    g = 0.0
    b = 0.0

    H = math.fmod(H, 360.0)
    H = 3.14159 * H / 180.0
    S = constrain(S, 0.0, 1.0)
    I = constrain(I, 0.0, 1.0)

    if H < 2.09439:
        r = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        g = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        b = 255.0 * I / 3.0 * (1.0 - S)
    elif H < 4.188787:
        H = H - 2.09439
        g = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        b = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        r = 255.0 * I / 3.0 * (1.0 - S)
    else:
        H = H - 4.188787
        b = 255.0 * I / 3.0 * (1.0 + S * math.cos(H) / math.cos(1.047196667 - H))
        r = (
            255.0
            * I
            / 3.0
            * (1.0 + S * (1.0 - math.cos(H) / math.cos(1.047196667 - H)))
        )
        g = 255.0 * I / 3.0 * (1.0 - S)

    return (
        constrain(int(r * 3.0), 0, 255),
        constrain(int(g * 3.0), 0, 255),
        constrain(int(b * 3.0), 0, 255),
    )  # for some reason, the rgb numbers need to be X3...


# https://www.neltnerlabs.com/saikoled/how-to-convert-from-hsi-to-rgb-white
def hsi2rgbw(H, S, I):
    r = 0
    g = 0
    b = 0
    w = 0
    cos_h = 0.0
    cos_1047_h = 0.0

    H = float(math.fmod(H, 360))  # cycle H around to 0-360 degrees
    H = 3.14159 * H / 180.0  # Convert to radians.
    S = constrain(S, 0.0, 1.0)
    I = constrain(I, 0.0, 1.0)

    if H < 2.09439:
        cos_h = math.cos(H)
        cos_1047_h = math.cos(1.047196667 - H)
        r = S * 255.0 * I / 3.0 * (1.0 + cos_h / cos_1047_h)
        g = S * 255.0 * I / 3.0 * (1.0 + (1.0 - cos_h / cos_1047_h))
        b = 0.0
        w = 255.0 * (1.0 - S) * I
    elif H < 4.188787:
        H = H - 2.09439
        cos_h = math.cos(H)
        cos_1047_h = math.cos(1.047196667 - H)
        g = S * 255.0 * I / 3.0 * (1.0 + cos_h / cos_1047_h)
        b = S * 255.0 * I / 3.0 * (1.0 + (1.0 - cos_h / cos_1047_h))
        r = 0.0
        w = 255.0 * (1.0 - S) * I
    else:
        H = H - 4.188787
        cos_h = math.cos(H)
        cos_1047_h = math.cos(1.047196667 - H)
        b = S * 255.0 * I / 3.0 * (1.0 + cos_h / cos_1047_h)
        r = S * 255.0 * I / 3.0 * (1.0 + (1.0 - cos_h / cos_1047_h))
        g = 0.0
        w = 255.0 * (1.0 - S) * I

    return (
        int(constrain(r * 3, 0, 255)),
        int(constrain(g * 3, 0, 255)),
        int(constrain(b * 3, 0, 255)),
        int(constrain(w, 0, 255)),
    )  # for some reason, the rgb numbers need to be X3...


# https://en.wikipedia.org/wiki/HSL_and_HSV
def hsv2hsl(h, s, v):
    h = constrain(h, 0.0, 360.0)
    s = constrain(s, 0.0, 1.0)
    v = constrain(v, 0.0, 1.0)

    Hhsl = h
    Lhsl = v - (v * s / 2.0)
    Shsl = 0
    if Lhsl > 0.0 and Lhsl < 1.0:
        Shsl = (v - Lhsl) / min(Lhsl, 1.0 - Lhsl)

    # somehow swapped these in the calc.  Come back and fix
    actual_l = Shsl
    actual_s = Lhsl

    return (Hhsl, actual_l, actual_s)


# https://en.wikipedia.org/wiki/HSL_and_HSV
def hsl2hsv(h, s, l):
    h = constrain(h, 0.0, 360.0)
    s = constrain(s, 0.0, 1.0)
    l = constrain(l, 0.0, 1.0)

    Hhsv = h
    Vhsv = l + (s * min(l, 1.0 - l))
    Shsv = 0
    if Vhsv > 0.0:
        Shsv = 2.0 - (2.0 * l / Vhsv)
    return (Hhsv, Shsv, Vhsv)


# https://en.wikipedia.org/wiki/HSL_and_HSV
def rgb2hsi(red, green, blue):
    r = constrain(float(red) / 255.0, 0.0, 1.0)
    g = constrain(float(green) / 255.0, 0.0, 1.0)
    b = constrain(float(blue) / 255.0, 0.0, 1.0)
    intensity = 0.33333 * (r + g + b)

    M = max(r, g, b)
    m = min(r, g, b)
    C = M - m  # noqa

    saturation = 0.0
    if intensity == 0.0:
        saturation = 0.0
    else:
        saturation = 1.0 - (m / intensity)

    hue = 0
    if M == m:
        hue = 0
    if M == r:
        if M == m:
            hue = 0.0
        else:
            hue = 60.0 * (0.0 + ((g - b) / (M - m)))
    if M == g:
        if M == m:
            hue = 0.0
        else:
            hue = 60.0 * (2.0 + ((b - r) / (M - m)))
    if M == b:
        if M == m:
            hue = 0.0
        else:
            hue = 60.0 * (4.0 + ((r - g) / (M - m)))
    if hue < 0.0:
        hue = hue + 360

    return (constrain(float(hue) / 360.0, 0.0, 1.0), abs(saturation), intensity)


def HSI(h, s, i):
    "Create new HSI color"
    t = (h, s, i)
    assert is_hsi_tuple(t)
    rgb_t = hsi2rgb(h, s, i)
    return RGB(rgb_t[0], rgb_t[1], rgb_t[2])


def RGB(r, g, b):
    "Create a new RGB color"
    t = (r, g, b)
    assert is_rgb_tuple(t)
    return Color(rgb_to_hsv(t))


def HSV(h, s, v):
    "Create a new HSV color"
    return Color((h, s, v))


def HSL(h, s, l):
    "Create new HSL color"
    (h, s, v) = hsl2hsv(h, s, l)
    return Color((h, s, v))


def Hex(value):
    "Create a new Color from a hex string"
    value = value.lstrip("#")
    lv = len(value)
    rgb_t = (int(value[i : i + int(lv / 3)], 16) for i in range(0, lv, int(lv / 3)))
    return RGB(*rgb_t)


class Color(object):
    "You should not really call the Color object directly, you get one in return from instantiating a specific color objext and interact with it that way"

    def __init__(self, hsv_tuple):
        self._set_hsv(hsv_tuple)

    def __repr__(self):
        return f"rgb={self.rgb} rgbw={self.rgbw} hsv={self.hsv} hsl={self.hsl} hsi={self.hsi} hex={self.hex} ||"

    def copy(self):
        return deepcopy(self)

    def _set_hsv(self, hsv_tuple):
        assert is_hsv_tuple(hsv_tuple)
        # convert to a list for component reassignment
        self.hsv_t = list(hsv_tuple)

    @property
    def rgbw(self):
        "returns a tuple of 4 values each in the range of 0-255"
        hsi = rgb2hsi(self.rgb[0], self.rgb[1], self.rgb[2])
        return hsi2rgbw(hsi[0], hsi[1], hsi[2])

    @property
    def hsi(self):
        "return HSI Tuple"
        return rgb2hsi(self.rgb[0], self.rgb[1], self.rgb[2])

    @property
    def hsl(self):
        return hsv2hsl(self.hsv_t[0], self.hsv_t[1], self.hsv_t[2])

    @property
    def rgb(self):
        "returns a rgb[0-255] tuple"
        return hsv_to_rgb(self.hsv_t)

    @property
    def hsv(self):
        "returns a hsv[0.0-1.0] tuple"
        return tuple(self.hsv_t)

    @property
    def hex(self):
        "returns a hexadecimal string"
        return "#%02x%02x%02x" % self.rgb

    """
    Properties representing individual HSV compnents
    Adjusting 'H' shifts the color around the color wheel
    Adjusting 'S' adjusts the saturation of the color
    Adjusting 'V' adjusts the brightness/intensity of the color
    """

    @property
    def hsv_h(self):
        return self.hsv_t[0]

    @hsv_h.setter
    def hsv_h(self, val):
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[0] = round(v, 8)

    @property
    def hsv_s(self):
        return self.hsv_t[1]

    @hsv_s.setter
    def hsv_s(self, val):
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[1] = round(v, 8)

    @property
    def hsv_v(self):
        return self.hsv_t[2]

    @hsv_v.setter
    def hsv_v(self, val):
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[2] = round(v, 8)

    """
    Properties representing individual RGB components
    """

    @property
    def rgb_r(self):
        return self.rgb[0]

    @rgb_r.setter
    def rgb_r(self, val):
        assert 0 <= val <= 255
        r, g, b = self.rgb
        new = (val, g, b)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    @property
    def rgb_g(self):
        return self.rgb[1]

    @rgb_g.setter
    def rgb_g(self, val):
        assert 0 <= val <= 255
        r, g, b = self.rgb
        new = (r, val, b)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    @property
    def rgb_b(self):
        return self.rgb[2]

    @property
    def rgb_rgb(self):
        return self.rgb

    # @rgb_rgb.setter
    # def rgb_rgb(self, t):
    # print('experimental- not functioning')
    # pass
    # new = t
    # assert is_rgb_tuple(new)
    # self._set_hsv(rgb_to_hsv(new))

    @rgb_b.setter
    def rgb_b(self, val):
        assert 0 <= val <= 255
        r, g, b = self.rgb
        new = (r, g, val)
        assert is_rgb_tuple(new)
        self._set_hsv(rgb_to_hsv(new))

    """
    Properties representing individual RGBW components
    """

    @property
    def rgbw_r(self):
        return self.rgbw[0]

    @property
    def rgbw_g(self):
        return self.rgbw[1]

    @property
    def rgbw_b(self):
        return self.rgbw[2]

    @property
    def rgbw_w(self):
        return self.rgbw[3]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
