#!/usr/bin/env python

from rgbw_colorspace_converter.colors.converters import RGB, HSV
from rgbw_colorspace_converter.tools.color_printer import print_colors
import rgbw_colorspace_converter.colors.util.morph as clrmorph

# Initializing a YELLOW color object and a BLUE color object.
yellow_color_obj = RGB(255, 255, 0)
blue_color_obj = RGB(0, 0, 255)
# Using a utility function to find a path betwwn the 2 colors
path_between = clrmorph.color_transition(yellow_color_obj, blue_color_obj, steps=12)

print(
    "Note how clear the HSV system changes are, only requiring one value to change, where RGB is pretty counterintuitive in the transition"
)
for color_step in path_between:
    print_colors(color_step, check_term_size=False)
    print(
        f"\t [ HSV ]: {color_step.hsv} \t [ RGB ]:{color_step.rgb} \t [ HEX ]:{color_step.hex}\n"
    )
