from typing import NamedTuple, Optional, Tuple, Union

from . import blend
from .space import (
    RGB,
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
)


class Color(NamedTuple):
    r: float  # [0-1]
    g: float  # [0-1]
    b: float  # [0-1]
    w: float  # [0-1]

    @classmethod
    def white(cls, w: float) -> "Color":
        return cls(0.0, 0.0, 0.0, w)

    @classmethod
    def from_hex(cls, h: str) -> "Color":
        if h.startswith("#"):
            h = h[1:]
        if len(h) == 6:
            h += "00"
        return Color(*tuple(int(h[i : i + 2], 16) / 255 for i in range(0, 8, 2)))

    @classmethod
    def from_rgb(cls, rgb: RGB, w: float = 0.0) -> "Color":
        return cls(rgb.r, rgb.g, rgb.b, w)

    @classmethod
    def from_linear_rgb(cls, rgb: LinearRGB, w: float = 0.0) -> "Color":
        return cls.from_rgb(linear_rgb_to_srgb(rgb), w)

    @classmethod
    def from_xyz(cls, xyz: XYZ, w: float = 0.0) -> "Color":
        return cls.from_linear_rgb(xyz_to_linear_rgb(xyz), w)

    @classmethod
    def from_lab(cls, lab: Lab, w: float = 0.0) -> "Color":
        return cls.from_xyz(lab_to_xyz(lab), w)

    @classmethod
    def from_hcl(cls, hcl: HCL, w: float = 0.0) -> "Color":
        return cls.from_lab(hcl_to_lab(hcl), w)

    @property
    def valid(self) -> bool:
        return all(0.0 <= c <= 1.0 for c in self)

    def clamp(self) -> "Color":
        def c(v: float) -> float:
            return max(0.0, min(v, 1.0))

        return Color(c(self.r), c(self.g), c(self.b), c(self.w))

    def blend(self, other: "Color", bias: float) -> "Color":
        return Color.from_hcl(
            blend.hcl(self.hcl, other.hcl, bias), w=blend.scale(self.w, other.w, bias)
        )

    @property
    def dmx(self) -> Tuple[int, int, int, int]:
        def c(v: float) -> int:
            return int(v * 255.0 + 0.5)

        return (c(self.r), c(self.g), c(self.b), c(self.w))

    @property
    def hex(self) -> str:
        return "#%02X%02X%02X%02X" % self.dmx

    @property
    def rgb(self) -> RGB:
        return RGB(self.r, self.g, self.b)

    @property
    def linear_rgb(self) -> LinearRGB:
        return srgb_to_linear_rgb(self.rgb)

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


def color(chroma: Union[str, RGB, Lab, HCL], white: float = 0.0) -> Color:
    if isinstance(chroma, str):
        return Color.from_hex(chroma)
    if isinstance(chroma, HCL):
        return Color.from_hcl(chroma, white)
    elif isinstance(chroma, Lab):
        return Color.from_lab(chroma, white)
    elif isinstance(chroma, RGB):
        return Color.from_rgb(chroma, white)
    else:
        raise TypeError("%r is not an RGB, Lab, or HCL color" % (chroma,))


def white(w: float) -> Color:
    return Color.white(w)
