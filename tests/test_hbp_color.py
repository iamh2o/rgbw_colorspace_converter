from pytest import approx

import hbp_colorspace_converter.hbp_colorspace_converter as color


def test_bidirectional_conversions():
    hsv = hsi = hsl = (40 / 359, 0.4, 0.5)

    # Approximate because rounding error
    rgb = color.hsv_to_rgb(*hsv)
    assert color.rgb_to_hsv(*rgb) == approx(hsv, 0.05)

    rgbw = color.hsv_to_rgbw(*hsv)
    assert color.rgbw_to_hsv(*rgbw) == approx(hsv, 0.05)

    rgb = color.hsi_to_rgb(*hsi)
    assert color.rgb_to_hsi(*rgb) == approx(hsi, 0.05)

    rgbw = color.hsi_to_rgbw(*hsi)
    assert color.rgbw_to_hsi(*rgbw) == approx(hsi, 0.05)

    hsv = color.hsl_to_hsv(*hsl)
    assert color.hsv_to_hsl(*hsv) == approx(hsl, 0.05)


def test_known_conversions():
    # Values from http://colorizer.org/
    hsv = (40 / 359, 0.57, 0.2287)
    assert color.hsv_to_rgb(*hsv) == (58, 47, 25)
    assert color.hsv_to_hsl(*hsv) == approx((40 / 359, 0.4, 0.16), 0.05)


def test_old_and_new():
    hsv = (40 / 359, 0.4, 0.3)

    direct_rgbw = color.hsv_to_rgbw(*hsv)
    indirect_rgbw = color.hsi_to_rgbw(*color.rgb_to_hsi(*color.hsv_to_rgb(*hsv)))
    assert direct_rgbw == approx(indirect_rgbw, 2) == (31, 20, 0, 45)
