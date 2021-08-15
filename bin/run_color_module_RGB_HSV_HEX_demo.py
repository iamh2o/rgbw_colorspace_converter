#!/usr/bin/env python3

import os
import sys
import random

from rgbw_colorspace_converter.colors.converters import RGB, HSV
from rgbw_colorspace_converter.tools import color_printer


os.environ["TERM"] = "xterm-256color"  # screen
os.system("tput clear; tput init; tput civis;stty -echo; ")

capture_output = True
ansi_bat_f = "./rgbw_csc.asc"
ansi_html_f = "./rgbw_csc.html"
os.system(f"rm {ansi_bat_f} {ansi_html_f}")
os.system(
    f"""echo '<html><link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=FiraCode"><link rel="stylesheet" href="//fonts.googleapis.com/css?family=FiraCode" type="text/css"><head></head><body style="line-height: 0.5;padding: 0; border: 0; margin: 0;"> ' > {ansi_html_f} """
)

## The following code is basically a mess as it grew from a small testing example to somethign that made pretty patterns.
# But until is needs more features, or stops working, here it is :-)

intro_cmd = """
echo ""
colr -c 0 "                               ╦ ╦╔╗ ╔═╗                             " "ff3100" "#6400ff";
colr -c 0 "                               ╠═╣╠╩╗╠═╝                             " "ff3100" "#6400ff";
colr -c 0 "                               ╩ ╩╚═╝╩                               " "ff3100" "#6400ff";


sleep 1;

echo "This is a testing / utility script, and kind of a little fun too.  It's not needed to use the library, but it does make some minimal use of the library, and is kind of pretty to watch for a while.  I'm mostly setting initial RGB colors, then using the HSV representation of that initial RGB to manipulate the HSV color object and use the resulting HEX tranlation to do some basic terminal color messing around.  Of course the real magic this module was made for is using the RGBW code translations with the proper hardware.  In anycase, this script will give you more info if you run with just '-h'. ";
echo "


To Exit: hit ctrl-c  (after the white test pattern passes)

*IF* you find your cursor has gone missing, try typing 'reset' and hit enter <-----

"
sleep 0
"""

os.system(intro_cmd)

print_codes = "no"
global col_width
col_width = 79
if len(sys.argv) == 2:
    print_codes = sys.argv[1].lower()
    c = None
    if sys.argv[1] in ["-h", "help", "h", "--h", "--help", "-help"]:
        os.system(
            """echo "

 This toy takes 3 positional arguments:
            (1)'yes' or 'no' to indicate if you want color codes printed in adddition to colors.
            (2)An integer > 0 to define the width of the term to fill (probably ~  80).  This indicate how many cols/characters of color to print before newline -or-  if you enter 'w' instead, the width of your screen will be detected.
            (3)EMPTY or '-n'.  Empty means new lines will be printed after every N characters printed as set above. -n means no newlines are printed.
             OH!  And idf you specify 'yes' for printing the color codes- options 2 and 3 are disabled.

            "
            """
        )
        os.system("stty echo; stty +echo ;")
        raise Exception("please set command line args")

if len(sys.argv) == 1:
    os.system(
        """echo '

        SETTING PRESETS 'no' w and ' '.  Type -h if you wish slightly confusing instructions.

        '
"""
    )
    sys.argv.append("no")
    sys.argv.append("w")
    sys.argv.append(" ")

    # First argument. -h prints help. Otherwise yes or no to print color codes
    print_codes = sys.argv[1].lower()


# Col width, or num characters to print
attempt_discovery_of_term_size = True
try:
    col_width = os.get_terminal_size().columns - 2
except Exception as e:
    del e
    attempt_discovery_of_term_size = False

try:
    if len(sys.argv) > 2:
        if sys.argv[2] == "w":
            pass
        else:
            if attempt_discovery_of_term_size:
                col_width = int(sys.argv[2])

except Exception as e:
    os.system(
        """echo '''

you must specify an integer >0 for argument 2.  Or specify 'w' for auto detection of your screen width.

'
"""
    )
    col_width = 80
    del e
    os.system("stty echo; stty +echo ;")
    # raise

# Only applies to color only mode.  Will not break for newlines after #cols printed. aka, the blocks append
no_newlines = " "
right_just_term_width = "-r 0"

try:
    if len(sys.argv) < 4:
        no_newlines = " "
    else:
        no_newlines = sys.argv[3] + " "
        right_just_term_width = ""
except Exception as e:
    os.system(
        """echo '''
 You must leave argument 3 blank or specify '-n'

'''
"""
    )
    del e
    os.system("stty echo; stty +echo ;")
    raise

ri = False
if len(sys.argv) == 5:
    ri = True


# Write colors module using colr!
def _write_color(color):
    if attempt_discovery_of_term_size:
        # col_width = os.get_terminal_size().columns - 2
        pass
    ret_code = 0

    cap_o = ""
    if capture_output is True:
        cap_o = f" >> {ansi_bat_f} "

    l = ""
    cmd = ""
    if print_codes == "no":
        # just print colors
        r = 1
        if ri:
            r = random.randint(1, 54)
        print_char_str = "===>||><||<==="
        len_pcs = len(print_char_str)
        l = print_char_str * (int(col_width / len_pcs) * r)
        cmd = f"""colr {right_just_term_width}  {no_newlines} " {l} " "{color.hex}" "{color.hex}" >> {ansi_bat_f} 2>/dev/null;"""
        ret_code = os.system(cmd)
    else:
        # Prtint color codes with color blocks
        l = "                    " + str(color)
        cmd = f"""colr  " {l} " "000000" "{color.hex}" {cap_o} 2>/dev/null;"""
        ret_code = os.system(cmd)

        # if capture_output is True:
        os.system(f"tail -n 1 {ansi_bat_f}")
        # os.system(f"tail -n 1 {ansi_bat_f} | ansi2html -i >> {ansi_html_f}")
    return int(ret_code)


# Write any messages


def _write_msg(msg):
    os.system(f"""echo '''{msg}'''""")


color = RGB(255, 255, 255)
_write_msg(
    f"""EXAMPLE OF RGB WHITE: {color.rgb}. Then cycling through each of h,s,v-- white for HSV is {color.hsv} -- Note, the RGB values do not change as hsv.h changes ---- THIS    WILL    REMAIN    WHITE ----   """
)
try:
    while color.hsv_h < 1.0:
        _write_color(color)
        color.hsv_h = color.hsv_h + 0.2

        if color.hsv_h > 0.99:
            if color.hsv_s == 0.0:
                _write_msg("DONE CYCLING THROUGH (H)sv, NOW CYCLING THROUGH h(S)v")

                while color.hsv_s < 1.0:
                    _write_color(color)
                    color.hsv_s = color.hsv_s + 0.03

                    if color.hsv_s > 0.99:
                        if color.hsv_v == 1.0:
                            _write_msg("DONE CYCLING THROUGH S, NOW CYCLING THROUGH hs(V)")
                        while color.hsv_v > 0.0:
                            _write_color(color)
                            color.hsv_v -= 0.013
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
        ret_code = _write_color(color)
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
            os.system("stty echo; stty +echo ;")
            raise

    _write_msg("-------------|| Note how often the RGB and RGBW codes differ ||-----------------")
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
        cxtr = 100


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
stty +echo




"""
os.system(f"hti -H {ansi_html_f} -o ./zzz -s 800,6500")
os.system(exit_cmd)
