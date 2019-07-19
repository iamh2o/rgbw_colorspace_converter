from math import atan2, cos, degrees, sin, sqrt, radians
from typing import Callable, NamedTuple

from . import linear


class RGB(NamedTuple):
    """
    RGB is an sRGB color.
    """

    r: float  # [0-1]
    g: float  # [0-1]
    b: float  # [0-1]

    @property
    def valid(self) -> bool:
        return 0.0 <= self.r <= 1.0 and 0.0 <= self.g <= 1.0 and 0.0 <= self.b <= 1.0

    def clamp(self) -> "RGB":
        def c(v: float) -> float:
            return max(0.0, min(v, 1.0))

        return RGB(c(self.r), c(self.g), c(self.b))


class Lab(NamedTuple):
    """
    Lab is a color in the CIE L*a*b* perceptually-uniform color space.
    """

    l: float
    a: float
    b: float


class HCL(NamedTuple):
    """
    HCL is a color in the CIE L*C*h° color space, a polar projection of L*a*b*.
    It's basically a superior HSV.
    """

    h: float  # hue [0-360)
    c: float  # chroma [0-1]
    l: float  # luminance [0-1]


class XYZ(NamedTuple):
    """
    XYZ is a color in CIE's standard color space.
    """

    x: float
    y: float
    z: float


class LinearRGB(NamedTuple):
    """
    RGB is a linear color.
    """

    r: float  # [0-1]
    g: float  # [0-1]
    b: float  # [0-1]


# Reference white points

D50 = XYZ(0.96422, 1.00000, 0.82521)
D65 = XYZ(0.95047, 1.00000, 1.08883)


def hcl_to_lab(hcl: HCL) -> Lab:
    h_rad = radians(hcl.h)
    a = hcl.c * cos(h_rad)
    b = hcl.c * sin(h_rad)
    return Lab(hcl.l, a, b)


def lab_to_hcl(lab: Lab) -> HCL:
    t = 1.0e-4
    h = (
        degrees(atan2(lab.b, lab.a)) % 360.0
        if abs(lab.b - lab.a) > t and abs(lab.a) > t
        else 0.0
    )
    c = sqrt(lab.a ** 2 + lab.b ** 2)
    l = lab.l

    return HCL(h, c, l)


def lab_to_xyz(lab: Lab, white_ref: XYZ = D65) -> XYZ:
    def finv(t: float) -> float:
        return (
            t ** 3
            if t > 6.0 / 29.0
            else 3.0 * 6.0 / 29.0 * 6.0 / 29.0 * (t - 4.0 / 29.0)
        )

    l2 = (lab.l + 0.16) / 1.16
    return XYZ(
        white_ref.x * finv(l2 + lab.a / 5.0),
        white_ref.y * finv(l2),
        white_ref.z * finv(l2 - lab.b / 2.0),
    )


def xyz_to_lab(xyz: XYZ, white_ref: XYZ = D65) -> Lab:
    def f(t: float) -> float:
        return (
            t ** (1 / 3)
            if t > 6.0 / 29.0 * 6.0 / 29.0 * 6.0 / 29.0
            else t / 3.0 * 29.0 / 6.0 * 29.0 / 6.0 + 4.0 / 29.0
        )

    fy = f(xyz.y / white_ref.y)
    return Lab(
        1.16 * fy - 0.16,
        5.0 * (f(xyz.x / white_ref.x) - fy),
        2.0 * (fy - f(xyz.z / white_ref.z)),
    )


def xyz_to_linear_rgb(xyz: XYZ) -> LinearRGB:
    return LinearRGB(
        3.2404542 * xyz.x - 1.5371385 * xyz.y - 0.4985314 * xyz.z,
        -0.9692660 * xyz.x + 1.8760108 * xyz.y + 0.0415560 * xyz.z,
        0.0556434 * xyz.x - 0.2040259 * xyz.y + 1.0572252 * xyz.z,
    )


def linear_rgb_to_xyz(rgb: LinearRGB) -> XYZ:
    return XYZ(
        0.4124564 * rgb.r + 0.3575761 * rgb.g + 0.1804375 * rgb.b,
        0.2126729 * rgb.r + 0.7151522 * rgb.g + 0.0721750 * rgb.b,
        0.0193339 * rgb.r + 0.1191920 * rgb.g + 0.9503041 * rgb.b,
    )


def linear_rgb_to_srgb(
    rgb: LinearRGB, delinearize: Callable[[float], float] = linear.delinearize
) -> RGB:
    return RGB(delinearize(rgb.r), delinearize(rgb.g), delinearize(rgb.b))


def srgb_to_linear_rgb(
    rgb: RGB, linearize: Callable[[float], float] = linear.linearize
) -> LinearRGB:
    return LinearRGB(linearize(rgb.r), linearize(rgb.g), linearize(rgb.b))
