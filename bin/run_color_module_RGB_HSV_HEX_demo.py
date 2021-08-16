#!/usr/bin/env python3

import os
import sys
import random
import argparse

from rgbw_colorspace_converter.colors.converters import RGB, HSV
from rgbw_colorspace_converter.tools.color_printer import print_colors

# This is all meant to work in even basic teminal sessions that do not
# have X11 running.  So, I loose a lot of flexibility in color range
# but, it is a fun challenege.  Below, I'm doing some terminal prep.
os.environ["TERM"] = "xterm-256color"  # screen
os.system("tput clear; tput init; tput civis;stty -echo; stty 100000; ")
# os.system("stty echo; stty +echo ;")


# First a hello
intro_cmd = """
echo ""
colr -c 0 "                               ╦ ╦╔╗ ╔═╗                             " "ff3100" "#6400ff";
colr -c 0 "                               ╠═╣╠╩╗╠═╝                             " "ff3100" "#6400ff";
colr -c 0 "                               ╩ ╩╚═╝╩                               " "ff3100" "#6400ff";


sleep 1;

echo "This is a testing / utility script, and kind of a little fun too.  It's not needed to use the colorspace mapping library, but it does make some minimal use of the library which could be helpful as examples. It is also kind of pretty to watch for a while. I'm mostly setting initial RGB colors, then using the HSV representation of that initial RGB to manipulate the HSV color object and use the resulting HEX tranlation to do some basic terminal color messing around.  Of course the real magic this module was made for is using the (other colorspace) -> RGBW translations.  But for that to be apaarent you need to be using RGBW LEDs, digital displays don't need the W directive (and alpha is not the same as W FWIW).  In anycase, this script will give you more info if you run with just '-h'. ";
echo "

==| -h will describe some of the simple knobs exposed to change the patterns. Most importantly, to exit: hit ctrl-c  (after the white test pattern passes).

==| IF you find your cursor has gone missing when you get back, try typing 'reset' and hit enter <---

==| There is the option to save the display setting as an HTML page and a png. Both will be saved in the directory you are running from.

"
sleep 1;
tput cnorm;
stty echo;
stty sane;
"""

os.system(intro_cmd)

# parse command line args
my_parser = argparse.ArgumentParser(description="RGBW Color Space Converter Playground")

# Add the arguments
my_parser.add_argument(
    "-p",
    "--print_color_codes",
    action="store_true",
    help="If set, the color codes of several spaces will be printed out in the bars",
    default=False,
)

my_parser.add_argument(
    "-a",
    "--outfiles_prefix",
    action="store",
    default="rgbw_csc",
    help="This is the prefix your prefix.html anbd prefix.pdf file will be named as, if you choose to record the session.",
)

my_parser.add_argument(
    "-b",
    "--print_chars",
    action="store",
    type=str,
    help="Do not print solid bars of color that span the terminal row. Instead print characters of color against a black background.(string length limit is 7chars for now)) ",
    default="____===",
)

my_parser.add_argument(
    "-d", "--debug", action="store_true", default=False, help="Turn on debugging."
)

my_parser.add_argument(
    "-c",
    "--no_capture_output",
    action="store_true",
    help="If set a html file and png of the display will be saved to files in this directory named ./rgbw_csc.(asc,html,png) ",
    default=False,
)

my_parser.add_argument(
    "-z",
    "--no_color_bars",
    action="store_true",
    help="Turn off printing full color bars.  Will need this flag to see the effect of -b.",
    default=False,
)

my_parser.add_argument(
    "-t",
    "--no_detect_terminal_width",
    action="store_true",
    help="*not working yet* If set the terminal width will NOT be detected and used as the column width per printed row.",
    default=False,
)

my_parser.add_argument("-m", "--meep", action="store_true", default=False, help="opposite of -f.")

my_parser.add_argument(
    "-f",
    "--full_experience",
    action="store_true",
    default=False,
    help="If you like more in general.",
)

my_parser.add_argument(
    "-w",
    "--col_width",
    action="store",
    default=80,
    type=int,
    help="*not working yet* Specify the number of columns of color to print on each row before moving to the next line, or appending to the prior if -n is used.",
)

my_parser.add_argument(
    "-r",
    "--random_block_len",
    action="store_true",
    help="instead of filling each row with the same color/pattern, a random length is chosen.  Works best with -n.",
    default=False,
)

my_parser.add_argument(
    "-n",
    "--no_newlines",
    action="store_true",
    help="When a line is printed, there is no newline entered, and the blocks of patterns/color wrap.",
    default=False,
)

# Execute parse_args()
args = my_parser.parse_args()

if args.full_experience and args.meep:
    ec = """echo '

    You may choose to set neither of (-f or -m)

              or just one

              but not both
    '
    """
    os.system(ec)
    raise

if args.full_experience:
    os.system("printf '\e[2t' && sleep 2 && printf '\e[1t' && sleep 1 && printf '\e[9;1t'")

if args.meep:
    os.system("printf '\e[8;18;50t' & sleep 1")

if len(args.print_chars) > 7 or len(args.print_chars) == 0:
    raise Exception("you must specify 1-7 characters only.")

ansi_bat_f = f"./{args.outfiles_prefix}.asc"
ansi_html_f = f"./{args.outfiles_prefix}.html"
ansi_png_f = f"./{args.outfiles_prefix}.png"

os.system(f"rm {ansi_bat_f} {ansi_html_f}")
os.system(
    f"""echo '<html><link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=FiraCode"><link rel="stylesheet" href="//fonts.googleapis.com/css?family=FiraCode" type="text/css"><head></head><body style="line-height: 0.5;padding: 0; border: 0; margin: 0;"> ' > {ansi_html_f} """
)


COL_WIDTH = args.col_width
check_term_size = args.no_detect_terminal_width
try:
    COL_WIDTH = os.get_terminal_size().columns
    # confusingly named command line flag, need to flip it
    if check_term_size is False:
        check_term_size = True
except Exception as e:
    del e
    check_term_size = False

# Settings that should eventually become command line arguments
no_newlines = " "  # no newline flag = " -n "
right_just_term_width = "-r 0"
random_block_len = False

global MAX_COL_WIDTH
MAX_COL_WIDTH = 0

N_ROWS = 0

print_bars = True
if args.no_color_bars is True:
    print_bars = False
capture_output = True
if args.no_capture_output is True:
    capture_output = False


def main(**kwargs):
    # reset terminal for printing.

    os.system("tput clear; tput init; tput civis;stty -echo; ")

    # Write colors module using colr!
    def _write_color(
        color,
        print_chars=kwargs["print_chars"],
        ansi_bat_f=kwargs["ansi_bat_f"],
        ansi_html_f=kwargs["ansi_html_f"],
        col_width=kwargs["col_width"],
        print_color_codes=kwargs["print_color_codes"],
        random_col_len=kwargs["random_block_len"],
        no_newlines=kwargs["no_newlines"],
        right_just_term_width=kwargs["right_just_term_width"],
        check_term_size=kwargs["check_term_size"],
        print_bars=kwargs["print_bars"],
        capture_output=kwargs["capture_output"],
        random_block_len=kwargs["random_block_len"],
    ):
        global N_ROWS
        (ret_code, col_width) = print_colors(
            color,
            print_chars=print_chars,
            ansi_bat_f=ansi_bat_f,
            ansi_html_f=ansi_html_f,
            col_width=col_width,
            print_color_codes=print_color_codes,
            random_col_len=random_col_len,
            no_newlines=no_newlines,
            right_just_term_width=right_just_term_width,
            check_term_size=check_term_size,
            print_bars=print_bars,
            capture_output=capture_output,
            random_block_len=random_block_len,
            n_row=N_ROWS,
        )
        global COL_WIDTH
        COL_WIDTH = col_width
        # Track the widest the window became
        global MAX_COL_WIDTH
        if MAX_COL_WIDTH < int(COL_WIDTH):
            MAX_COL_WIDTH = COL_WIDTH

        # track number of rows
        N_ROWS += 1
        return (ret_code, COL_WIDTH)

    def _write_msg(msg):
        if args.debug:
            os.system(f"""echo '''{msg}'''""")

    color = RGB(255, 255, 255)
    _write_msg(
        f"""EXAMPLE OF RGB WHITE: {color.rgb}. Then cycling through each of h,s,v-- white for HSV is {color.hsv} -- Note, the RGB values do not change as hsv.h changes ---- THIS    WILL    REMAIN    WHITE ----   """
    )
    try:
        while color.hsv_h < 1.0:
            (ret_code, col_w) = _write_color(color)

            color.hsv_h = color.hsv_h + 0.2

            if color.hsv_h > 0.99:
                if color.hsv_s == 0.0:
                    _write_msg("DONE CYCLING THROUGH (H)sv, NOW CYCLING THROUGH h(S)v")

                    while color.hsv_s < 1.0:
                        (ret_code, col_w) = _write_color(color)
                        color.hsv_s = color.hsv_s + 0.03
                        if ret_code != 0:
                            raise
                        if color.hsv_s > 0.99:
                            if color.hsv_v == 1.0:
                                _write_msg("DONE CYCLING THROUGH S, NOW CYCLING THROUGH hs(V)")
                            while color.hsv_v > 0.0:
                                (ret_code, col_w) = _write_color(color)
                                color.hsv_v -= 0.013
                                if ret_code != 0:
                                    raise
            if ret_code != 0:
                raise
    except Exception as e:
        print(e)
        raise

    _write_msg("And that is cycling through each of the H/S/V properties  independently")
    _write_msg("We are starting with H and V at 0 and S at 1 and cycling")

    color = HSV(h=1.0, s=0.0, v=1.0)
    while color.hsv_h < 1.0:
        _write_color(color)
        color.hsv_h = color.hsv_h + 0.025
        color.hsv_s = color.hsv_s - 0.025
        color.hsv_v = color.hsv_v + 0.025

    _write_msg("WHAT THE HELL... Slightly Random Fading!")

    color = HSV(0.5, 0.75, 0.232)
    ctr = 0.0

    _write_msg("--")

    os.system("sleep 1;")
    xctr = 90
    try:
        # I'm cycling through colors in order, but chosing the steps to move forward for H/S/V semi-randomly so some nice patterns emerge. Also, generally a good idea to throw in some negative space here and there.
        while ctr < 20.0:
            # from IPython import embed; embed();
            (ret_code, col_w) = _write_color(color)
            if color.hsv_h >= 1.0:
                color.hsv_h = 0.0
            else:
                color.hsv_h = color.hsv_h + 0.007
            if color.hsv_s <= 0.00:
                color.hsv_s = [0.0, 0.0, 0.25, 0.4, 0.5][random.randint(0, 4)]
            else:
                color.hsv_s = color.hsv_s + 0.0006

            if color.hsv_v >= 1.0:
                color.hsv_v = [0.0, 0.0, 0.0, 0.9, 0.5][random.randint(0, 4)]
            else:
                r = [
                    1.0,
                    122.0,
                    322.0,
                    155.0,
                    177.0,
                    200.0,
                    100.0,
                    300.0,
                    400.0,
                    222.0,
                    331.0,
                    55.0,
                    1.0,
                    122.0,
                    322.0,
                    155.0,
                    177.0,
                    220.0,
                    130.0,
                    300.0,
                    400.0,
                    222.0,
                    331.0,
                    355.0,
                ]
                rr = r[random.randint(0, len(r) - 1)] / 400.0

                color.hsv_v = rr
                # color.hsv_v = color.hsv_v + 0.01

            ctr = ctr + 0.005
            if ret_code != 0:
                from IPythom import embed

                embed()
                raise
        _write_msg(
            "-------------|| Note how often the RGB and RGBW codes differ ||-----------------"
        )
        os.system("sleep 1;")
        _write_msg(" Finally, 90 lines of random RGB. ")

    except Exception as e:
        del e
        _write_msg(" Thank You For Watching.")
        xctr = 100

    while xctr < 100:
        # and this is truly printing random colors 100 times.  Random can sometimes be the most dissapointing b/c,
        # with no patterns to lure you in, they are often boring.
        ret_code = _write_color(
            RGB(random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        )
        xctr = xctr + 1
        if ret_code != 0:
            cxtr = 100  # noqa

    exit_cmd = """
    echo "

    "
    colr -c 0 "                               ╦ ╦╔╗ ╔═╗                            " "#ff0000" "#0000ff";
    colr -c 0 "                               ╠═╣╠╩╗╠═╝                            " "#ff0000" "#0000ff";
    colr -c 0 "                               ╩ ╩╚═╝╩                              " "#ff0000" "#0000ff";

    echo "

    "
    tput cnorm
    stty echo



    """
    os.system(
        f"cat {ansi_bat_f} | ansi2html -i  | perl -pe 's/\/span/\/span\>\<br/g;' >> {ansi_html_f} "
    )

    iwidth = int((MAX_COL_WIDTH * 8))
    ilength = int((N_ROWS * 16))

    os.system(
        f"hti -H {ansi_html_f} -o ./rgbw_pnggen/ -s {iwidth},{ilength}; mv ./rgbw_pnggen/screenshot.png {ansi_png_f}; rm -rf ./rbgw_pnggen/"
    )
    os.system(exit_cmd)


# RUN THE SCRIPT!!

try:

    main(
        print_chars=args.print_chars,
        ansi_bat_f=ansi_bat_f,
        ansi_html_f=ansi_html_f,
        ansi_png_f=ansi_png_f,
        col_width=COL_WIDTH,
        print_color_codes=args.print_color_codes,
        random_col_len=args.random_block_len,
        no_newlines=args.no_newlines,
        right_just_term_width=right_just_term_width,
        check_term_size=check_term_size,
        print_bars=print_bars,
        capture_output=capture_output,
        random_block_len=args.random_block_len,
    )

except Exception as e:
    if args.debug:
        os.system("echo '                          Something has gone awry....................'")
        print(e)
    else:
        del e
    os.system("tput cnorm; stty echo; stty sane; ")
