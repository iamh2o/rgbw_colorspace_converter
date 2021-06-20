from pytest import approx

from rgbw_colorspace_converter.colors.converters import RGB


def test_round_2_conversions():
    # #######################
    # ####################
    # TESTS 2  RGB / RGBW / HEX / HSV / HSL

    c2 = RGB(69, 13, 152)

    # HSV
    hsv2 = c2.hsv
    hsv2_truth = (0.7338, 0.9145, 0.5961)
    assert str(hsv2[0])[:5] == str(hsv2_truth[0])[:5]
    assert str(hsv2[1])[:5] == str(hsv2_truth[1])[:5]
    assert str(hsv2[2])[:5] == str(hsv2_truth[2])[:5]

    # HSL
    hsl2 = c2.hsl
    hsl2_truth = (264.173, 0.8424, 0.3235)
    assert str(hsl2[0])[:5] == str(hsl2_truth[0])[:5]
    assert str(hsl2[1])[:5] == str(hsl2_truth[1])[:5]
    assert str(hsl2[2])[:5] == str(hsl2_truth[2])[:5]

    # HEX
    hex2_truth = "#450d98"
    assert c2.hex == hex2_truth

    # RGBW

    rgbw2_truth = (56, 0, 138, 12)
    assert c2.rgbw == rgbw2_truth

    # HSi
    hsi2 = c2.hsi
    hsi2_truth = (264.173, 0.833, 0.3059)
    assert str(hsi2[0])[:5] == str(hsi2_truth[0])[:5]
    assert str(hsi2[1])[:5] == str(hsi2_truth[1])[:5]
    assert str(hsi2[2])[:5] == str(hsi2_truth[2])[:5]
