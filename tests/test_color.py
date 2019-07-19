from typing import NamedTuple

from pytest import approx

from ponzicolor.color import color
from ponzicolor.space import (
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
from ponzicolor.linear import delinearize, linearize


class Case(NamedTuple):
    hex: str
    rgb: RGB
    lrgb: LinearRGB
    xyz: XYZ
    lab: Lab
    hcl: HCL


cases = [
    Case(
        "#ffffff",
        RGB(1.0, 1.0, 1.0),
        LinearRGB(1, 1, 1),
        XYZ(0.950470, 1.000000, 1.088830),
        Lab(1.000000, 0.000000, 0.000000),
        HCL(0.0000, 0.000000, 1.000000),
    ),
    Case(
        "#80ffff",
        RGB(0.5, 1.0, 1.0),
        LinearRGB(0.21404114048223255, 1, 1),
        XYZ(0.626296, 0.832848, 1.073634),
        Lab(0.931390, -0.353319, -0.108946),
        HCL(197.1371, 0.369735, 0.931390),
    ),
    Case(
        "#ff80ff",
        RGB(1.0, 0.5, 1.0),
        LinearRGB(1, 0.21404114048223255, 1),
        XYZ(0.669430, 0.437920, 0.995150),
        Lab(0.720892, 0.651673, -0.422133),
        HCL(327.0661, 0.776450, 0.720892),
    ),
    Case(
        "#ffff80",
        RGB(1.0, 1.0, 0.5),
        LinearRGB(1, 1, 0.21404114048223255),
        XYZ(0.808654, 0.943273, 0.341930),
        Lab(0.977637, -0.165795, 0.602017),
        HCL(105.3975, 0.624430, 0.977637),
    ),
    Case(
        "#8080ff",
        RGB(0.5, 0.5, 1.0),
        LinearRGB(0.21404114048223255, 0.21404114048223255, 1),
        XYZ(0.345256, 0.270768, 0.979954),
        Lab(0.590453, 0.332846, -0.637099),
        HCL(297.5843, 0.718805, 0.590453),
    ),
    Case(
        "#ff8080",
        RGB(1.0, 0.5, 0.5),
        LinearRGB(1, 0.21404114048223255, 0.21404114048223255),
        XYZ(0.527613, 0.381193, 0.248250),
        Lab(0.681085, 0.483884, 0.228328),
        HCL(25.2610, 0.535049, 0.681085),
    ),
    Case(
        "#80ff80",
        RGB(0.5, 1.0, 0.5),
        LinearRGB(0.21404114048223255, 1, 0.21404114048223255),
        XYZ(0.484480, 0.776121, 0.326734),
        Lab(0.906026, -0.600870, 0.498993),
        HCL(140.2920, 0.781050, 0.906026),
    ),
    Case(
        "#808080",
        RGB(0.5, 0.5, 0.5),
        LinearRGB(0.21404114048223255, 0.21404114048223255, 0.21404114048223255),
        XYZ(0.203440, 0.214041, 0.233054),
        Lab(0.533890, 0.000000, 0.000000),
        HCL(0.0000, 0.000000, 0.533890),
    ),
    Case(
        "#00ffff",
        RGB(0.0, 1.0, 1.0),
        LinearRGB(0.0, 1.0, 1.0),
        XYZ(0.538014, 0.787327, 1.069496),
        Lab(0.911132, -0.480875, -0.141312),
        HCL(196.3762, 0.501209, 0.911132),
    ),
    Case(
        "#ff00ff",
        RGB(1.0, 0.0, 1.0),
        LinearRGB(1.0, 0.0, 1.0),
        XYZ(0.592894, 0.284848, 0.969638),
        Lab(0.603242, 0.982343, -0.608249),
        HCL(328.2350, 1.155407, 0.603242),
    ),
    Case(
        "#ffff00",
        RGB(1.0, 1.0, 0.0),
        LinearRGB(1.0, 1.0, 0.0),
        XYZ(0.770033, 0.927825, 0.138526),
        Lab(0.971393, -0.215537, 0.944780),
        HCL(102.8512, 0.969054, 0.971393),
    ),
    Case(
        "#0000ff",
        RGB(0.0, 0.0, 1.0),
        LinearRGB(0.0, 0.0, 1.0),
        XYZ(0.180437, 0.072175, 0.950304),
        Lab(0.322970, 0.791875, -1.078602),
        HCL(306.2849, 1.338076, 0.322970),
    ),
    Case(
        "#00ff00",
        RGB(0.0, 1.0, 0.0),
        LinearRGB(0.0, 1.0, 0.0),
        XYZ(0.357576, 0.715152, 0.119192),
        Lab(0.877347, -0.861827, 0.831793),
        HCL(136.0160, 1.197759, 0.877347),
    ),
    Case(
        "#ff0000",
        RGB(1.0, 0.0, 0.0),
        LinearRGB(1.0, 0.0, 0.0),
        XYZ(0.412456, 0.212673, 0.019334),
        Lab(0.532408, 0.800925, 0.672032),
        HCL(39.9990, 1.045518, 0.532408),
    ),
    Case(
        "#000000",
        RGB(0.0, 0.0, 0.0),
        LinearRGB(0.0, 0.0, 0.0),
        XYZ(0.000000, 0.000000, 0.000000),
        Lab(0.000000, 0.000000, 0.000000),
        HCL(0.0000, 0.000000, 0.000000),
    ),
]


def test_linear_rgb():
    for c in cases:
        actual = srgb_to_linear_rgb(c.rgb)
        assert actual.r == approx(c.lrgb.r, 0.0001)
        assert actual.g == approx(c.lrgb.g, 0.0001)
        assert actual.b == approx(c.lrgb.b, 0.0001)
    for c in cases:
        actual = linear_rgb_to_srgb(c.lrgb)
        assert actual.r == approx(c.rgb.r, 0.0001)
        assert actual.g == approx(c.rgb.g, 0.0001)
        assert actual.b == approx(c.rgb.b, 0.0001)


def test_xyz():
    for c in cases:
        actual = linear_rgb_to_xyz(srgb_to_linear_rgb(c.rgb))
        assert actual.x == approx(c.xyz.x, 0.0001)
        assert actual.y == approx(c.xyz.y, 0.0001)
        assert actual.z == approx(c.xyz.z, 0.0001)
    for c in cases:
        actual = linear_rgb_to_srgb(xyz_to_linear_rgb(c.xyz))
        assert actual.r == approx(c.rgb.r, 0.0001, 0.0001)
        assert actual.g == approx(c.rgb.g, 0.0001, 0.0001)
        assert actual.b == approx(c.rgb.b, 0.0001, 0.0001)


def test_lab():
    for c in cases:
        actual = xyz_to_lab(linear_rgb_to_xyz(srgb_to_linear_rgb(c.rgb)))
        assert actual.l == approx(c.lab.l, 0.0001, 0.0001)
        assert actual.a == approx(c.lab.a, 0.0001, 0.0001)
        assert actual.b == approx(c.lab.b, 0.0001, 0.0001)
    for c in cases:
        actual = linear_rgb_to_srgb(xyz_to_linear_rgb(lab_to_xyz(c.lab)))
        assert actual.r == approx(c.rgb.r, 0.0001, 0.0001)
        assert actual.g == approx(c.rgb.g, 0.0001, 0.0001)
        assert actual.b == approx(c.rgb.b, 0.0001, 0.0001)


def test_hcl():
    for c in cases:
        actual = lab_to_hcl(xyz_to_lab(linear_rgb_to_xyz(srgb_to_linear_rgb(c.rgb))))
        assert actual.h == approx(c.hcl.h, 0.0001, 0.0001)
        assert actual.c == approx(c.hcl.c, 0.0001, 0.0001)
        assert actual.l == approx(c.hcl.l, 0.0001, 0.0001)
    for c in cases:
        actual = linear_rgb_to_srgb(xyz_to_linear_rgb(lab_to_xyz(hcl_to_lab(c.hcl))))
        assert actual.r == approx(c.rgb.r, 0.0001, 0.0001)
        assert actual.g == approx(c.rgb.g, 0.0001, 0.0001)
        assert actual.b == approx(c.rgb.b, 0.0001, 0.0001)


def test_blend():
    assert color("#2E4057").blend(color("#048BA8"), 0.1).hex == "#2F476000"
    assert color("#2E4057").blend(color("#048BA8"), 0.2).hex == "#2F4E6900"
    assert color("#2E4057").blend(color("#048BA8"), 0.3).hex == "#2F557100"
    assert color("#2E4057").blend(color("#048BA8"), 0.4).hex == "#2E5C7A00"
    assert color("#2E4057").blend(color("#048BA8"), 0.5).hex == "#2B648200"
    assert color("#2E4057").blend(color("#048BA8"), 0.6).hex == "#286B8A00"
    assert color("#2E4057").blend(color("#048BA8"), 0.7).hex == "#23739200"
    assert color("#2E4057").blend(color("#048BA8"), 0.8).hex == "#1D7B9A00"
    assert color("#2E4057").blend(color("#048BA8"), 0.9).hex == "#1483A100"

    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.1).hex == "#DCD8E600"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.2).hex == "#D8D3E300"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.3).hex == "#D3CDE000"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.4).hex == "#CFC8DD00"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.5).hex == "#CBC2DA00"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.6).hex == "#C6BCD700"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.7).hex == "#C2B7D400"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.8).hex == "#BEB1D000"
    assert color("#E1DEE9").blend(color("#B6A6CA"), 0.9).hex == "#BAACCD00"

    assert color("#DD403A").blend(color("#B8B42D"), 0.1).hex == "#DE4E3200"
    assert color("#DD403A").blend(color("#B8B42D"), 0.2).hex == "#DD5B2A00"
    assert color("#DD403A").blend(color("#B8B42D"), 0.3).hex == "#DB682300"
    assert color("#DD403A").blend(color("#B8B42D"), 0.4).hex == "#D9741C00"
    assert color("#DD403A").blend(color("#B8B42D"), 0.5).hex == "#D5801600"
    assert color("#DD403A").blend(color("#B8B42D"), 0.6).hex == "#D18B1200"
    assert color("#DD403A").blend(color("#B8B42D"), 0.7).hex == "#CC961300"
    assert color("#DD403A").blend(color("#B8B42D"), 0.8).hex == "#C6A01900"
    assert color("#DD403A").blend(color("#B8B42D"), 0.9).hex == "#BFAA2200"

    assert color("#3D348B").blend(color("#E6AF2E"), 0.1).hex == "#6A328B00"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.2).hex == "#8E2F8700"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.3).hex == "#AC2F7F00"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.4).hex == "#C5347300"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.5).hex == "#D8416600"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.6).hex == "#E6535800"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.7).hex == "#EE694A00"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.8).hex == "#F0803D00"
    assert color("#3D348B").blend(color("#E6AF2E"), 0.9).hex == "#EE973200"

    assert color("#191716").blend(color("#E6AF2E"), 0.1).hex == "#2E221C00"
    assert color("#191716").blend(color("#E6AF2E"), 0.2).hex == "#432F2100"
    assert color("#191716").blend(color("#E6AF2E"), 0.3).hex == "#593C2500"
    assert color("#191716").blend(color("#E6AF2E"), 0.4).hex == "#6E4A2800"
    assert color("#191716").blend(color("#E6AF2E"), 0.5).hex == "#83582B00"
    assert color("#191716").blend(color("#E6AF2E"), 0.6).hex == "#98682D00"
    assert color("#191716").blend(color("#E6AF2E"), 0.7).hex == "#AC782F00"
    assert color("#191716").blend(color("#E6AF2E"), 0.8).hex == "#C08A2F00"
    assert color("#191716").blend(color("#E6AF2E"), 0.9).hex == "#D49C2F00"

    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.1).hex == "#BEE9C100"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.2).hex == "#BDE6C000"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.3).hex == "#BBE2C000"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.4).hex == "#BADFC000"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.5).hex == "#B9DBBF00"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.6).hex == "#B9D8BE00"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.7).hex == "#B8D4BE00"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.8).hex == "#B7D0BD00"
    assert color("#BFEDC1").blend(color("#B6C9BB"), 0.9).hex == "#B7CDBC00"


def test_linearize():
    assert linearize(0.000000) == approx(0.000000)
    assert linearize(0.040000) == approx(0.003096, 0.0001)
    assert linearize(0.100000) == approx(0.010023, 0.0001)
    assert linearize(0.200000) == approx(0.033105, 0.0001)
    assert linearize(0.250000) == approx(0.050876, 0.0001)
    assert linearize(0.500000) == approx(0.214041, 0.0001)
    assert linearize(0.750000) == approx(0.522522, 0.0001)
    assert linearize(1.000000) == approx(1.000000, 0.0001)


def test_delinearize():
    assert delinearize(0.000000) == approx(0.000000, 0.0001, 0.0001)
    assert delinearize(0.003000) == approx(0.038760, 0.0001, 0.0001)
    assert delinearize(0.010000) == approx(0.099853, 0.0001, 0.0001)
    assert delinearize(0.050000) == approx(0.247801, 0.0001, 0.0001)
    assert delinearize(0.100000) == approx(0.349190, 0.0001, 0.0001)
    assert delinearize(0.200000) == approx(0.484529, 0.0001, 0.0001)
    assert delinearize(0.250000) == approx(0.537099, 0.0001, 0.0001)
    assert delinearize(0.500000) == approx(0.735357, 0.0001, 0.0001)
    assert delinearize(0.750000) == approx(0.880825, 0.0001, 0.0001)
    assert delinearize(1.000000) == approx(1.000000, 0.0001, 0.0001)
