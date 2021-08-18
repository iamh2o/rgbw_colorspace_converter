#!/usr/bin/env python
import os
import argparse

from rgbw_colorspace_converter.colors.converters import RGB, HSV
from rgbw_colorspace_converter.tools.color_printer import print_colors

my_parser = argparse.ArgumentParser(
    description="RGB ANSI Colord Text Printer.  You can specify RGB or HSV systems, not both."
)

my_parser.add_argument(
    "-t",
    "--text",
    action="store",
    default="so it goes",
    help="The text you want to print, in quotes",
)
my_parser.add_argument(
    "-brgb",
    "--background_color_rgb",
    action="store",
    default="255,255,9",
    help="color to paint the background  ie: 255,0,100.  csv no spaces.",
)
my_parser.add_argument(
    "-trgb",
    "--text_color_rgb",
    action="store",
    default="9,255,255",
    help="color to paint text, ie: 255,0,100.  csv, no spaces.",
)


my_parser.add_argument(
    "-bhsv",
    "--background_color_hsv",
    action="store",
    default=None,
    help="color to paint the background in HSV  ie: 0.9,0.3,0.6. csv, no spaces.",
)
my_parser.add_argument(
    "-thsv",
    "--text_color_hsv",
    action="store",
    default=None,
    help="color to paint text, ie: 0.9,0.3,0.6.   csv no spaces.",
)
my_parser.add_argument(
    "-pcc",
    "--print_color_codes",
    action="store_true",
    default=False,
    help="Print out color codes below formatted text",
)

args = my_parser.parse_args()

color_t = None
color_b = None
if args.background_color_hsv is not None and args.text_color_hsv is not None:
    color_b = HSV(
        float(args.background_color_hsv.split(",")[0]),
        float(args.background_color_hsv.split(",")[1]),
        float(args.background_color_hsv.split(",")[2]),
    )
    color_t = HSV(
        float(args.text_color_hsv.split(",")[0]),
        float(args.text_color_hsv.split(",")[1]),
        float(args.text_color_hsv.split(",")[2]),
    )
else:
    print(args.background_color_rgb, args.text_color_rgb)
    color_b = RGB(
        int(args.background_color_rgb.split(",")[0]),
        int(args.background_color_rgb.split(",")[1]),
        int(args.background_color_rgb.split(",")[2]),
    )
    color_t = RGB(
        int(args.text_color_rgb.split(",")[0]),
        int(args.text_color_rgb.split(",")[1]),
        int(args.text_color_rgb.split(",")[2]),
    )


print_colors(
    print_chars=args.text,
    foreground_color=color_t,
    background_color=color_b,
    multiply_txt=False,
)

if args.print_color_codes:
    print(
        f"\nText: rgb:{color_t.rgb} hsv:{color_t.hsv} hex:{color_t.hex} \n\nBackground: {color_b.rgb} hsv:{color_b.hsv} hex:{color_b.hex}\n"
    )
print(color_b.rgb)
