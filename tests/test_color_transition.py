from rgbw_colorspace_converter.colors.converters import RGB
from rgbw_colorspace_converter.colors.util.morph import color_transition


def test_color_transition():
    start = RGB(255, 0, 0)
    end = RGB(0, 255, 0)
    steps = 25

    count = 0
    previous = start
    for color in color_transition(start, end, steps=steps):
        count += 1
        assert color.rgb_r <= previous.rgb_r
        previous = color
    assert count == steps
