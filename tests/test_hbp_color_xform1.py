from pytest import approx

from rgbw_colorspace_converter.colors.converters import RGB


def test_known_conversions_set1():
    # http://www.workwithcolor.com/color-converter-01.htm

    # ######################
    # ####################
    # TESTS 1 RGB / RGBW / HEX / HSV / HSL (HSI if I could find anyone with a converter)
    # the sig digits diverge, so will only compare w/in reasonable matches
    # http://www.workwithcolor.com/color-converter-01.htm?cp=B0CDE6&ch=208-52-80&cb=B0CDE6,FFFFFF,FFFFFF,FFFFFF,FFFFFF,FFFFFF,FFFFFF,FFFFFF,FFFFFF,FFFFFF
    c1 = RGB(176, 205, 230)

    def HSV1():
        # HSV
        hsv1 = c1.hsv
        hsv1_truth = (0.57, 0.2348, 0.902)
        assert (
            str(hsv1[0])[:4] == str(hsv1_truth[0])[:4]
        )  # rounging delta- passes as is
        assert str(hsv1[1])[:5] == str(hsv1_truth[1])[:5]
        assert (
            str(hsv1[2])[:4] == str(hsv1_truth[2])[:4]
        )  # Rounding delta- passes as is

    def HSL1():
        # HSL
        hsl1 = c1.hsl
        hsl1_truth = (207.777, 0.5192, 0.7961)
        assert (
            str(hsl1[0])[:5] == str(hsl1_truth[0])[:5]
        )  # rounging delta- passes as is
        assert str(hsl1[1])[:5] == str(hsl1_truth[1])[:5]
        assert (
            str(hsl1[2])[:5] == str(hsl1_truth[2])[:5]
        )  # Rounding delta- passes as is

    def HEX1():
        # HEX
        hex1 = c1.hex
        hex1_truth = "#b0cde6"
        assert hex1 == hex1_truth

    def RGBW1():
        # RGBW
        rgbw1 = c1.rgbw
        rgbw1_truth = (
            0,
            28,
            54,
            176,
        )  # Have to trust our well tested impelentation as there are still no other otrhogonal checks to be found
        assert rgbw1 == rgbw1_truth

    def HSi1():
        # HSi  https://www.picturetopeople.org/p2p/image_utilities.p2p/color_converter?color_space=RGB&color_channel1=176&color_channel2=205&color_channel3=230&ResultType=view
        hsi1 = c1.hsi
        hsi1_truth = (0.5778, 0.13584, 0.7987)
        assert (
            str(hsi1[0])[:5] == str(hsi1_truth[0])[:5]
        )  # rounging delta- passes as is
        assert str(hsi1[1])[:5] == str(hsi1_truth[1])[:5]
        assert (
            str(hsi1[2])[:5] == str(hsi1_truth[2])[:5]
        )  # Rounding delta- passes as is
