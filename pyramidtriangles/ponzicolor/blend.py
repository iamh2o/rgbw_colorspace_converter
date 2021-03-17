from .space import HCL, Lab

# Blending colors depends on what color space the colors are represented in.


def hcl(a: HCL, b: HCL, t: float) -> HCL:
    h = _interpolate_angle(a.h, b.h, t)
    c = scale(a.c, b.c, t)
    l = scale(a.l, b.l, t)
    return HCL(h, c, l)


def lab(a: Lab, b: Lab, t: float) -> Lab:
    return Lab(l=scale(a.l, b.l, t), a=scale(a.a, b.a, t), b=scale(a.b, b.b, t))


def scale(a: float, b: float, t: float) -> float:
    return a + t * (b - a)


def _interpolate_angle(a: float, b: float, t: float) -> float:
    delta = ((b - a) % 360.0 + 540.0) % 360.0 - 180
    return (a + t * delta + 360.0) % 360.0
