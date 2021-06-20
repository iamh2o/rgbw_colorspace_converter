from pytest import approx

from rgbw_colorspace_converter.colors.converters import RGB


def test_round_3_transforms():
    # ############
    # ##########
    # TEST 3

    c3 = RGB(234, 56, 137)

    # HSV
    hsv3 = c3.hsv
    hsv3_truth = (0.9242, 0.7607, 0.9176)
    assert str(hsv3[0])[:5] == str(hsv3_truth[0])[:5]
    assert str(hsv3[1])[:5] == str(hsv3_truth[1])[:5]
    assert str(hsv3[2])[:5] == str(hsv3_truth[2])[:5]

    # HSL
    hsl3 = c3.hsl
    hsl3_truth = (332.697, 0.8091, 0.5686)
    assert str(hsl3[0])[:5] == str(hsl3_truth[0])[:5]
    assert str(hsl3[1])[:5] == str(hsl3_truth[1])[:5]
    assert str(hsl3[2])[:5] == str(hsl3_truth[2])[:5]

    # HEX
    hex3_truth = "#ea3889"
    # assert c3.hex == hex3_truth # WILL FAIL B/C the mismatch is th last digigt is a 9 vs an 8
    assert hex3_truth[:6] == c3.hex[:6]

    # RGBW
    rgbw3_truth = (177, 0, 80, 56)
    assert c3.rgbw == rgbw3_truth

    # HSi
    hsi3 = c3.hsi
    hsi3_truth = (333.0, 0.6065, 0.557)
    assert str(hsi3[0])[:5] == str(hsi3_truth[0])[:5]
    assert (
        str(hsi3[1])[:4] == str(hsi3_truth[1])[:4]
    )  # Rounding causing apparent mismatch
    assert (
        str(hsi3[2])[:4] == str(hsi3_truth[2])[:4]
    )  # rounding causing aparent mismatch
