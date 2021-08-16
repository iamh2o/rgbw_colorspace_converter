from rgbw_colorspace_converter.colors.converters import RGB, HSV
from rgbw_colorspace_converter.tools.color_printer import print_colors
import rgbw_colorspace_converter.colors.util.morph as clrmorph

red_color_obj = RGB(255, 255, 0)
blue_color_obj = RGB(0, 0, 255)
path_between = clrmorph.color_transition(red_color_obj, blue_color_obj, steps=12)
for color_step in path_between:
    print_colors(color_step, check_term_size=False)
    print(
        f"\t [ HSV ]: {color_step.hsv} \t [ RGB ]:{color_step.rgb} \t [ HEX ]:{color_step.hex}\n"
    )
