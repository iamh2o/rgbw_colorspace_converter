import os
import sys
import random

from rgbw_colorspace_converter.colors.converters import RGB, HSV


## Command line args.  I'm lazy and not using arg parse.

intro_cmd = """
echo "---------------------------------- | WELCOME | --------------------------------";
colr "                                    ╦ ╦╔╗ ╔═╗                                  " "ff3100" "#6400ff";
colr "                                    ╠═╣╠╩╗╠═╝                                  " "ff3100" "#6400ff";
colr "                                    ╩ ╩╚═╝╩                                    " "ff3100" "#6400ff";

sleep 2;

echo "This is a testing / utility script, and kind of a little fun too.  It's not needed to use the library, but it does make some minimal use of the library, and is kind of pretty to watch for a while.  I'm mostly setting initial RGB colors, then using the HSV representation of that initial RGB to manipulate the HSV color object and use the resulting HEX tranlation to do some basic terminal color messing around.  Of course the real magic this module was made for is using the RGBW code translations with the proper hardware.  In anycase, this script will give you more info if you run with just '-h'. ";

"""

os.system(intro_cmd)


print_codes = "no"
try:
    print_codes = sys.argv[1].lower()
    if print_codes in ["-h", "help", "h", "--h", "--help", "-help"]:
        print(
            "This toy takes 3 positional arguments:\n\t(1)'yes' or 'no' to indicate if you want color codes printed in adddition to colors.\n\t(2)An integer > 0 (and probably ideally like 80, and huge is a bad idea).  To indicate how many cols/characters of color to print before newline.\n\t(3)EMPTY or '-n'.  Empty means new lines will be printed after every N characters printed as set above. -n means no newlines are printed.\n\n"
        )
        raise ("please set command line args")
    if print_codes not in ["yes", "no"]:
        raise Exception("the first argumnet must be 'yes' or 'no'")
except Exception as e:
    print(
        f"Arg 1 must be 'yes' or 'no' only.  No will only print colors. 'yes' will also print the various color codes",
        e,
    )

col_width = 70
try:
    col_width = int(sys.argv[2])
except Exception as e:
    print("you must specify an integer >0 for argument 2")
    print(e)
    raise

# Only applies to color only
no_newlines = " "
try:
    no_newlines = sys.argv[3] + " "
except Exception as e:
    print("you must leave argument 3 blank or specify '-n'")
    print(e)
    raise


# Write colors
def _write_color(color):

    black_hex = RGB(0, 0, 0).hex
    l = ""
    cmd = ""
    if print_codes == "no":
        # just print colors
        l = "X" * col_width
        cmd = f"""colr {no_newlines}"{l}" "{color.hex}" "{color.hex}"; """
        os.system(cmd)
    else:
        # Prtint color codes with color blocks
        l = "                    " + str(color)
        cmd = f"""colr "{l}" "{black_hex}" "{color.hex}" ; """
        os.system(cmd)


# Write any messages
def _write_msg(msg):
    cmd = f"colr '''{msg}'''"
    os.system(cmd)


color = RGB(255, 255, 255)
_write_msg(
    f"""'STARTING OFF WITH WHITE, ',{color} , 'and cycling through each of h,s,v-- white for HSV is {color.hsv} -- Note, the RGB values do not change as hsv.h changes ---- THIS    WILL    REMAIN    WHITE ----   ' ;"""
)

while color.hsv_h < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.1

    if color.hsv_h > 0.99:
        if color.hsv_s == 0.0:
            _write_msg(
                "echo ' DONE CYCLING THROUGH (H)sv, NOW CYCLING THROUGH h(S)v ';"
            )

            while color.hsv_s < 1.0:
                _write_color(color)
                color.hsv_s = color.hsv_s + 0.1

                if color.hsv_s > 0.99:
                    if color.hsv_v == 1.0:
                        _write_msg(
                            "echo ' DONE CYCLING THROUGH S, NOW CYCLING THROUGH hs(V)';"
                        )
                    while color.hsv_v > 0.0:
                        _write_color(color)
                        color.hsv_v -= 0.1

_write_msg(
    "echo ' And that is cycling through each of the HSV comonents independently'; "
)
_write_msg(
    "echo ' For kicks, here is starting with H and V at 0 and S at 1 and cycling '; "
)

color = HSV(h=1.0, s=0.0, v=1.0)
while color.hsv_h < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.05
    color.hsv_s = color.hsv_s - 0.05
    color.hsv_v = color.hsv_v + 0.05

_write_msg("echo ''; echo ''; echo 'WHAT THE HELL!!!! Less Sequential fading!!!'; ")
color = HSV(0.5, 0.75, 0.232)
ctr = 0.0
_write_msg(
    f"'-------------|| THIS WILL GO ON FOR SOME TIME- CTRL+C WILL FREE YOU ||----------------------';sleep(3);"
)

try:
    while ctr < 10.0:
        # from IPython import embed; embed();
        _write_color(color)
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
    _write_msg(
        f"echo {ctr}'-------------|| Note how often the RGB and RGBW codes differ ||----------------------'"
    )
except Exception as e:
    print(e)

xctr = 0
while xctr < 90:
    _write_color(
        RGB(random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
    )

    xctr = xctr + 1

exit_cmd = """
\n\n\n\n
echo "------------------------------------ | FIN | -----------------------------------";
colr "                                    ╦ ╦╔╗ ╔═╗                                  " "#ff0000" "#0000ff";
colr "                                    ╠═╣╠╩╗╠═╝                                  " "#ff0000" "#0000ff";
colr "                                    ╩ ╩╚═╝╩                                    " "#ff0000" "#0000ff";
\n\n\n\n
"""

os.system(exit_cmd)
