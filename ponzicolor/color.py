from __future__ import annotations
from dataclasses import dataclass, astuple
from typing import Union

from model import DisplayColor
from . import blend
from .space import (
    RGB,
    HSV,
    Lab,
    HCL,
    XYZ,
    LinearRGB,
    hcl_to_lab,
    lab_to_hcl,
    lab_to_xyz,
    xyz_to_lab,
    xyz_to_linear_rgb,
    linear_rgb_to_xyz,
    srgb_to_linear_rgb,
    linear_rgb_to_srgb,
    srgb_to_hsv,
    hsv_to_srgb,
    hsv_to_rgbw,
)


@dataclass(frozen=True)
class Color(DisplayColor):
    r: float  # [0-1]
    g: float  # [0-1]
    b: float  # [0-1]
    w: float  # [0-1]

    @classmethod
    def white(cls, w: float) -> Color:
        return cls(0.0, 0.0, 0.0, w)

    @classmethod
    def from_hex(cls, h: str) -> Color:
        if h.startswith("#"):
            h = h[1:]
        if len(h) == 6:
            h += "00"
        return Color(*tuple(int(h[i: i + 2], 16) / 255 for i in range(0, 8, 2)))

    @classmethod
    def from_rgb(cls, rgb: RGB) -> Color:
        return cls(rgb.r, rgb.g, rgb.b, 0.0)

    @classmethod
    def from_hsv(cls, hsv: HSV) -> Color:
        return cls.from_rgb(hsv_to_srgb(hsv))

    @classmethod
    def from_linear_rgb(cls, rgb: LinearRGB) -> Color:
        return cls.from_rgb(linear_rgb_to_srgb(rgb))

    @classmethod
    def from_xyz(cls, xyz: XYZ) -> Color:
        return cls.from_linear_rgb(xyz_to_linear_rgb(xyz))

    @classmethod
    def from_lab(cls, lab: Lab) -> Color:
        return cls.from_xyz(lab_to_xyz(lab))

    @classmethod
    def from_hcl(cls, hcl: HCL) -> Color:
        return cls.from_lab(hcl_to_lab(hcl))

    @property
    def valid(self) -> bool:
        return all(0.0 <= c <= 1.0 for c in astuple(self))

    def clamp(self) -> Color:
        def c(v: float) -> float:
            return max(0.0, min(v, 1.0))

        return Color(c(self.r), c(self.g), c(self.b), c(self.w))

    def blend(self, other: Color, bias: float) -> Color:
        return Color.from_hcl(
            blend.hcl(self.hcl, other.hcl, bias)
        )

    @property
    def rgb256(self) -> tuple[int, int, int]:
        """
        Called to emit an RGB triple in [0-255].

        Used in DisplayColor interface.
        """
        def c(v: float) -> int:
            return int(v * 255.0 + 0.5)

        rgb = self.rgb
        return c(rgb.r), c(rgb.g), c(rgb.b)

    @property
    def rgbw256(self) -> tuple[int, int, int, int]:
        """
        Called to emit an RGBW quadruple in [0-255].

        Used in DisplayColor interface.
        """
        return self.dmx

    def scale(self, factor: float) -> Color:
        """
        Scales the brightness by a factor in [0,1].

        Used in DisplayColor interface.
        """
        factor = max(0.0, min(factor, 1.0))
        hsv = self.hsv
        return color(HSV(hsv.h, hsv.s, hsv.v * factor))

    @property
    def dmx(self) -> tuple[int, int, int, int]:
        """
        Emit RGBW [0-255] tuple.
        """
        r, g, b, w = self.r, self.g, self.b, self.w

        # If white element unused, re-blend to RGBW before emitting.
        if w == 0.0 and max(r, g, b) != 0.0:
            rgbw = hsv_to_rgbw(self.hsv)
            r, g, b, w = rgbw.r, rgbw.g, rgbw.b, rgbw.w

        def c(v: float) -> int:
            return int(v * 255.0 + 0.5)
        return c(r), c(g), c(b), c(w)

    @property
    def hex(self) -> str:
        def c(v: float) -> int:
            return int(v * 255.0 + 0.5)
        return "#%02X%02X%02X%02X" % (c(self.r), c(self.g), c(self.b), c(self.w))

    @property
    def rgb(self) -> RGB:
        return RGB(self.r, self.g, self.b)

    @property
    def linear_rgb(self) -> LinearRGB:
        return srgb_to_linear_rgb(self.rgb)

    @property
    def hsv(self) -> HSV:
        return srgb_to_hsv(self.rgb)

    @property
    def xyz(self) -> XYZ:
        return linear_rgb_to_xyz(self.linear_rgb)

    @property
    def lab(self) -> Lab:
        return xyz_to_lab(self.xyz)

    @property
    def hcl(self) -> HCL:
        return lab_to_hcl(self.lab)

    @property
    def hue(self) -> float:
        return self.hcl.h


def color(chroma: Union[str, RGB, Lab, HCL, HSV]) -> Color:
    if isinstance(chroma, str):
        return Color.from_hex(chroma)
    if isinstance(chroma, HCL):
        return Color.from_hcl(chroma)
    elif isinstance(chroma, Lab):
        return Color.from_lab(chroma)
    elif isinstance(chroma, RGB):
        return Color.from_rgb(chroma)
    elif isinstance(chroma, HSV):
        return Color.from_hsv(chroma)
    else:
        raise TypeError("%r is not an RGB, Lab, HCL, or HSV color" % (chroma,))


def white(w: float) -> Color:
    return Color.white(w)
