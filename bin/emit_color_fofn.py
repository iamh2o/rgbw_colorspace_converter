import os
import sys
import random
from hbp_colorspace_converter.hbp_colorspace_converter import RGB, Color, HSV


print_color = sys.argv[1]
col_width = 70
try:
    col_width = sys.argv[2]
except Exception as e:
    print(e)
    raise


out_f = open("emit_color.cmds", "w")


def _write_color(color):

    leng = int(col_width)
    l = ""
    cmd = ""

    if print_color == "no":
        l = "X" * leng
        cmd = f"""colr "{l}" "{color.rgb_r},{color.rgb_g},{color.rgb_b}" "{color.rgb_r},{color.rgb_g},{color.rgb_b}"; """
    else:
        l = "                    " + str(color)
        cmd = f"""colr "{l}" "0,0,0" "{color.rgb_r},{color.rgb_g},{color.rgb_b}"; """
    out_f.write(f"{cmd}\n")


def _write_msg(msg):

    out_f.write(f"{msg}\n")


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


out_f.close()
