"""
Color

Color class that allows you to initialize a color in any of HSV, HSL, HSI, RGB, Hex color spaces.  Once initialized,
the corresponding RGBW values are calculated and you may modify the object in RGB or HSV color spaces( ie: by re-setting
any component of HSV or RGB (ie, just resetting the R value) and all RGB/HSV/RGBW values will be recalculated.
As of now, you can not work in RGBW directly as we have not written the conversions from RGBW back to one of the
standard color spaces. (annoying, but so it goes).


The main goal of this class is to translate various color spaces into RGBW for use in RGBW pixels.

The color representation is maintained in HSV internally and translated to RGB and RGBW.
Use whichever is more convenient at the time - RGB for familiarity, HSV to fade colors easily.

RGB values range from 0 to 255
HSV values range from 0.0 to 1.0 *Note the H value has been normalized to range between 0-1 in instead of 0-360 to allow
for easier cycling of values.
HSL/HSI values range from 0-360 for H, 0-1 for S/[L|I]

    >>> red = RGB(255, 0 ,0)
    >>> red2 = RGBW(255, 0, 0, 0)
    >>> green = HSV(0.33, 1.0, 1.0)
    >>> green2 = RGBW(5, 254, 0, 0)
    >>> fuchsia = RGB(180, 48, 229)
    >>> fuchsia2 = RGBW(130, 0, 182, 47)

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

Brightness can be adjusted by setting the 'v' property, even
when you're working in RGB.

For example: to gradually dim a color
(ranges from 0.0 to 1.0)

    >>> col = RGB(0,255,0)
    >>> while col.v > 0:
    ...   print col.rgb
    ...   col.v -= 0.1
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

RGBW

To get the (r,g,b,w) tuples back from a Color object, simply call Color.rgbw and you will return the (r,g,b,w) tuple.

"""
import colorsys
from copy import deepcopy
from math import fmod, cos, radians
from typing import Tuple, List, TypeVar, Union

from model import DisplayColorBase

__all__ = ['Color', 'Hex', 'HSI', 'HSL', 'HSV', 'RGB', 'RGBW']

# Constrained generic type of int or float
V = TypeVar('V', int, float)


def clamp(val: V, min_value: V, max_value: V) -> V:
    """Restrict a value between a minimum and a maximum value"""
    return max(min(val, max_value), min_value)


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Converts an RGB[0, 255] tuple to HSV[0, 1].
    """
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)


def hsv_to_rgb(hue: float, saturation: float, value: float) -> Tuple[int, int, int]:
    """
    Converts a Hue Saturation Value triple to an RGB triple.
    """
    (r, g, b) = (round(val * 255) for val in colorsys.hsv_to_rgb(hue, saturation, value))
    return r, g, b


def hsv_to_rgbw(hue: float, saturation: float, value: float) -> Tuple[int, int, int, int]:
    """
    Converts a Hue Saturation Value triple to an RGBW quadruple.

    Implemented from https://en.wikipedia.org/wiki/HSL_and_HSV#HSV_to_RGB
    Mixing of white inspired by Brian Neltner's posts.
    """
    hue = (hue * 360) % 360

    chroma = saturation * value
    x = chroma * (1 - abs((fmod(hue / 60, 2) - 1)))

    if hue <= 60:
        r, g, b = chroma, x, 0.0
    elif hue <= 120:
        r, g, b = x, chroma, 0.0
    elif hue <= 180:
        r, g, b = 0.0, chroma, x
    elif hue <= 240:
        r, g, b = 0.0, x, chroma
    elif hue <= 300:
        r, g, b = x, 0.0, chroma
    else:
        r, g, b = chroma, 0.0, x

    # Rather than mix value difference into each component, white is used
    w = value - chroma

    (r, g, b, w) = (round(val * 255) for val in (r, g, b, w))
    return r, g, b, w


def rgbw_to_hsv(r: int, g: int, b: int, w: int) -> Tuple[float, float, float]:
    """
    Converts RGBW quadruple in [0, 255] to HSV triple in [0, 1].
    """
    # Convert colors to fraction of maximum value, e.g. in [0, 1]
    r /= 255
    g /= 255
    b /= 255
    w /= 255

    maximal = max(r, g, b)
    minimal = min(r, g, b)
    chroma = maximal - minimal

    # Hue is the same for RGB and RGBW
    if chroma == 0:
        hue = 0
    elif maximal == r:
        hue = 60 * (0 + ((g - b) / (maximal - minimal)))
    elif maximal == g:
        hue = 60 * (2 + ((b - r) / (maximal - minimal)))
    else:
        hue = 60 * (4 + ((r - g) / (maximal - minimal)))

    if hue < 0:
        hue += 360

    value = chroma + w

    saturation = 0.0
    if maximal > 0.0:
        saturation = chroma / value

    return hue / 360, saturation, value


def hsi_to_rgb(hue: float, sat: float, intensity: float) -> Tuple[int, int, int]:
    """
    Converts a Hue Saturation Intensity triple to RGB triple.

    Based on https://www.neltnerlabs.com/saikoled/how-to-convert-from-hsi-to-rgb-white
    """
    hue = radians(hue * 360)

    def primary(h):
        return 1 + sat * cos(h) / cos(radians(60) - h)

    def secondary(h):
        return 1 + sat * (1 - cos(h) / cos(radians(60) - h))

    tertiary = 1 - sat

    if hue < radians(120):
        r, g, b = primary(hue), secondary(hue), tertiary

    elif hue < radians(240):
        hue -= radians(120)
        r, g, b = tertiary, primary(hue), secondary(hue)

    else:
        hue -= radians(240)
        r, g, b = secondary(hue), tertiary, primary(hue)

    # Convert fractional values to [0, 255]
    (r, g, b) = (round(val * intensity / 3 * 255) for val in (r, g, b))
    return r, g, b


def rgb_to_hsi(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Converts an RGB triple to Hue Saturation Intensity triple.

    Based on https://en.wikipedia.org/wiki/HSL_and_HSV
    """
    # Convert colors to fraction of maximum value, e.g. in [0, 1]
    r /= 255
    g /= 255
    b /= 255

    maximal = max(r, g, b)
    minimal = min(r, g, b)
    chroma = maximal - minimal
    intensity = r + g + b

    saturation = 0.0
    if intensity > 0.0:  # To prevent divide by zero
        saturation = 1 - (3 * minimal / intensity)

    hue = 0
    if chroma == 0:
        hue = 0

    elif maximal == r:
        hue = 60 * (0 + (g - b) / chroma)

    elif maximal == g:
        hue = 60 * (2 + (b - r) / chroma)

    elif maximal == b:
        hue = 60 * (4 + (r - g) / chroma)

    if hue < 0:
        hue += 360

    return hue / 360, abs(saturation), intensity


def hsi_to_rgbw(hue: float, sat: float, intensity: float) -> Tuple[int, int, int, int]:
    """
    Converts a Hue Saturation Intensity triple to RGBW quadruple.

    Based on https://www.neltnerlabs.com/saikoled/how-to-convert-from-hsi-to-rgb-white
    """
    hue = radians(hue * 360)
    w = 1 - sat

    def primary(h):
        return sat * (1 + cos(h) / cos(radians(60) - h))

    def secondary(h):
        return sat * (1 + (1 - cos(h) / cos(radians(60) - h)))

    if hue < radians(120):
        r, g, b = primary(hue), secondary(hue), 0.0

    elif hue < radians(240):
        hue -= radians(120)
        r, g, b = 0.0, primary(hue), secondary(hue)

    else:
        hue -= radians(240)
        r, g, b = secondary(hue), 0.0, primary(hue)

    # Convert fractional values to [0, 255]
    (r, g, b, w) = (round(val * intensity * 255) for val in (r, g, b, w))
    return r, g, b, w


def rgbw_to_hsi(r: int, g: int, b: int, w: int) -> Tuple[float, float, float]:
    """
    Converts RGBW quadruple to HSI triple.

    Implemented from: https://web.archive.org/web/20110918053706/http://www.had2know.com/technology/hsi-rgb-color-converter-equations.html
    Which was mentioned in Neltner comment here: https://blog.saikoled.com/post/44677718712/how-to-convert-from-hsi-to-rgb-white
    """
    # Convert colors to fraction of maximum value, e.g. in [0, 1]
    r /= 255
    g /= 255
    b /= 255
    w /= 255

    maximal = max(r, g, b)
    minimal = min(r, g, b)
    chroma = maximal - minimal
    intensity = (r + g + b) / 3 + w  # intensity of all LEDs

    saturation = 0.0
    if intensity > 0.0:  # To prevent divide by zero
        saturation = 1 - w / intensity

    hue = 0
    if chroma == 0:
        hue = 0

    elif maximal == r:
        hue = 60 * (0 + (g - b) / chroma)

    elif maximal == g:
        hue = 60 * (2 + (b - r) / chroma)

    elif maximal == b:
        hue = 60 * (4 + (r - g) / chroma)

    if hue < 0:
        hue += 360

    return hue / 360, saturation, intensity


def hsv_to_hsl(hue: float, sat_hsv: float, value: float) -> Tuple[float, float, float]:
    """
    Converts HSV triple in [0, 1] to HSL triple in [0, 1].

    Implemented from https://en.wikipedia.org/wiki/HSL_and_HSV
    """
    lightness = value - (value * sat_hsv / 2)

    sat_hsl = 0.0
    if 0.0 < lightness < 1.0:
        sat_hsl = (value - lightness) / min(lightness, 1 - lightness)

    return hue, sat_hsl, lightness


def hsl_to_hsv(hue: float, sat_hsl: float, lightness: float) -> Tuple[float, float, float]:
    """
    Converts HSL triple in [0, 1] to HSV triple in [0, 1].

    Implemented from https://en.wikipedia.org/wiki/HSL_and_HSV
    """
    value = lightness + (sat_hsl * min(lightness, 1 - lightness))

    sat_hsv = 0.0
    if value > 0.0:
        sat_hsv = 2 - (2 * lightness / value)

    return hue, sat_hsv, value


def HSI(hue: Union[int, float], saturation: float, intensity: float) -> "Color":
    """
    Create new HSI color.

    Accepts hue as int in range [0, 360] or float in range [0, 1].
    """
    if isinstance(hue, int):
        if not 0 <= hue < 360:
            raise ValueError(f"int hue {hue} must be in [0, 360]")
        hue = (hue % 360) / 360
    elif isinstance(hue, float):
        if not 0.0 <= hue <= 1.0:
            raise ValueError(f"float hue {hue} must be in [0, 1]")
    else:
        raise ValueError(f"Unexpected hue type {type(hue).__name__}")

    if not 0.0 <= saturation <= 1.0:
        raise ValueError(f"saturation {saturation} must be in [0, 1]")

    if not 0.0 <= intensity <= 1.0:
        raise ValueError(f"intensity {intensity} must be in [0, 1]")

    return RGB(*hsi_to_rgb(hue, saturation, intensity))


def RGB(r, g, b) -> "Color":
    """Create a new RGB color"""
    for val in [r, g, b]:
        if not 0 <= val < 256:
            raise ValueError(f'argument {val} must be in [0, 255]')

    return Color(rgb_to_hsv(r, g, b))


def RGBW(r, g, b, w) -> "Color":
    """Create a new RGBW color"""
    for val in [r, g, b, w]:
        if not 0 <= val < 256:
            raise ValueError(f'argument {val} must be in [0, 255]')

    return Color(rgbw_to_hsv(r, g, b, w))


def HSV(hue: Union[int, float], saturation: float, value: float) -> "Color":
    """
    Create a new HSV color

    Accepts hue as int in range [0, 360] or float in range [0, 1].
    """
    if isinstance(hue, int):
        if not 0 <= hue <= 360:
            raise ValueError(f"hue {hue} must be in [0, 360]")
        hue = (hue % 360) / 360  # Convert to range [0, 1]
    elif isinstance(hue, float):
        if not 0.0 <= hue <= 1.0:
            raise ValueError(f"hue {hue} must be in [0, 1]")
    else:
        raise ValueError(f"Unexpected hue type {type(hue).__name__}")

    if not 0.0 <= saturation <= 1.0:
        raise ValueError(f"saturation {saturation} must be in [0, 1]")

    if not 0.0 <= value <= 1.0:
        raise ValueError(f"value {value} must be in [0, 1]")

    return Color((hue, saturation, value))


def HSL(hue: Union[int, float], saturation: float, lightness: float) -> "Color":
    """
    Create new HSL color

    Accepts hue as int in range [0, 360] or float in range [0, 1].
    """
    if isinstance(hue, int):
        if not 0 <= hue < 360:
            raise ValueError(f"hue {hue} must be in [0, 360]")
        hue = (hue % 360) / 360
    elif isinstance(hue, float):
        if not 0.0 <= hue <= 1.0:
            raise ValueError(f"hue {hue} must be in [0, 1]")
    else:
        raise ValueError(f"Unexpected hue type {type(hue).__name__}")

    if not 0.0 <= saturation <= 1.0:
        raise ValueError(f"saturation {saturation} must be in [0, 1]")

    if not 0.0 <= lightness <= 1.0:
        raise ValueError(f"lightness {lightness} must be in [0, 1]")

    return Color(hsl_to_hsv(hue, saturation, lightness))


def Hex(value: str) -> "Color":
    """Create a new Color from a hex string"""
    value = value.lstrip('#')
    lv = len(value)
    rgb_t = (int(value[i:i+int(lv/3)], 16) for i in range(0, lv, int(lv/3)))
    return RGB(*rgb_t)


class Color(DisplayColorBase):
    hsv_t: List[float]

    def __init__(self, hsv: Tuple[float, float, float]):
        """
        Creates a native HSV Color.
        """
        self._set_hsv(hsv)

    def __repr__(self) -> str:
        return "rgb=%s hsv=%s" % (self.rgb, self.hsv)

    def copy(self) -> "Color":
        return deepcopy(self)

    def _set_hsv(self, hsv: Tuple[float, float, float]) -> None:
        if not len(hsv) == 3 and all([(0.0 <= t <= 1.0) for t in hsv]):
            raise ValueError(f"invalid HSV tuple '{hsv}'")

        # converts to a list for component reassignment
        self.hsv_t = list(hsv)

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        """returns an RGBW tuple in [0, 255]."""
        return hsv_to_rgbw(*self.hsv_t)

    @property
    def rgbw256(self) -> Tuple[int, int, int, int]:
        """
        Alias for rgbw(self)
        """
        return self.rgbw

    @property
    def rgb(self) -> Tuple[int, int, int]:
        """returns an RGB tuple in [0, 255]."""
        return hsv_to_rgb(*self.hsv_t)

    @property
    def rgb256(self) -> Tuple[int, int, int]:
        """
        Alias for rgb(self)
        """
        return self.rgb

    @property
    def hsv(self) -> Tuple[float, float, float]:
        """returns a hsv[0.0-1.0] tuple"""
        return self.hsv_t[0], self.hsv_t[1], self.hsv_t[2]

    @property
    def hex(self) -> str:
        """returns a hexadecimal string"""
        return '#%02x%02x%02x' % self.rgb

    @property
    def hsl(self) -> Tuple[int, float, float]:
        """returns an HSL tuple ([0, 360], [0, 1], [0, 1])."""
        (h, s, l) = hsv_to_hsl(*self.hsv_t)
        return round(h * 360), s, l

    """
    Properties representing individual HSV components
    Adjusting 'H' shifts the color around the color wheel
    Adjusting 'S' adjusts the saturation of the color
    Adjusting 'V' adjusts the brightness/intensity of the color
    """
    @property
    def h(self) -> float:
        return self.hsv_t[0]

    @h.setter
    def h(self, val: float) -> None:
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[0] = round(v, 8)

    @property
    def s(self) -> float:
        return self.hsv_t[1]

    @s.setter
    def s(self, val: float) -> None:
        v = clamp(val, 0.0, 1.0)
        self.hsv_t[1] = round(v, 8)

    @property
    def v(self) -> float:
        return self.hsv_t[2]

    @v.setter
    def v(self, val: float) -> None:
        v = clamp(val, 0.0, 1.0) 
        self.hsv_t[2] = round(v, 8)

    """
    Properties representing individual RGB components
    """
    @property
    def rgb_r(self) -> int:
        return self.rgb[0]

    @rgb_r.setter
    def rgb_r(self, r: int) -> None:
        _, g, b = self.rgb
        self._set_hsv(rgb_to_hsv(r, g, b))

    @property
    def rgb_g(self) -> int:
        return self.rgb[1]

    @rgb_g.setter
    def rgb_g(self, g: int) -> None:
        r, _, b = self.rgb
        self._set_hsv(rgb_to_hsv(r, g, b))

    @property
    def rgb_b(self) -> int:
        return self.rgb[2]

    @rgb_b.setter
    def rgb_b(self, b: int) -> None:
        r, g, _ = self.rgb
        self._set_hsv(rgb_to_hsv(r, g, b))

    def scale(self, factor: float) -> "Color":
        """
        Scales the brightness by a factor in [0,1].
        """
        factor = clamp(factor, 0.0, 1.0)
        (h, s, v) = self.hsv
        return Color((h, s, v*factor))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
