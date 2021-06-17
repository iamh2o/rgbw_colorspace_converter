import os
import sys
from hbp_colorspace_converter.hbp_colorspace_converter import RGB, Color, HSV


code = sys.argv[1]

if code not in ["A", "B", "C", "D", "E", "?"]:
    os.system(
        """echo "


    Not a valid choice.  You're getting A.

"""
    )


out_f = open("emit_color.cmds", "w")


def _write_color(color):
    cmd = f""" echo "{color}";  colr "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" "{color.rgb_r},{color.rgb_g},{color.rgb_b}" "{color.rgb_r},{color.rgb_g},{color.rgb_b}"; """
    out_f.write(f"{cmd}\n")


def _write_msg(msg):
    out_f.write(f"{msg}\n")
    out_f.write("sleep 2;")


color = RGB(255, 255, 255)

_write_msg(
    f"""'STARTING OFF WITH WHITE, ',{color} , 'and cycling through each of h,s,v-- white for HSV is {color.hsv}\n\n' -- Note, the RGB values do not change as hsv.h changes ;"""
)

while color.hsv_h < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.01

    if color.hsv_h > 0.99:
        if color.hsv_s == 0.0:
            _write_msg("echo ' DONE CYCLING THROUGH H, NOW CYCLING THROUGH S';")

            while color.hsv_s < 1.0:
                _write_color(color)
                color.hsv_s = color.hsv_s + 0.001

                if color.hsv_s > 0.99:
                    if color.hsv_v == 1.0:
                        _write_msg(
                            "echo ' DONE CYCLING THROUGH S, NOW CYCLING THROUGH V';"
                        )
                    while color.hsv_v > 0.0:
                        _write_color(color)
                        color.hsv_v -= 0.01


_write_msg(
    "echo ' And that is cycling through each of the HSV comonents independently'; "
)
_write_msg(
    "echo ' For kicks, here is starting with H and V at 0 and S at 1 and cycling '; "
)
color = HSV(h=1.0, s=0.0, v=1.0)
while color.hsv_h < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.005
    color.hsv_s = color.hsv_s - 0.005
    color.hsv_v = color.hsv_v + 0.005


_write_msg("echo ''; echo ''; echo 'WHAT THE HELL!!!! SOME INVERSES TOO!!!'; sleep 5;")
color = HSV(h=0.5, s=0.75, v=0.25)
ctr = 0.0
while ctr < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.005
    if color.hsv_h == 1.0:
        color.hsv_h == 0.0
    color.hsv_s = color.hsv_s - 0.005
    if color.hsv_s == 0.0:
        color.hsv_s = 0.9
    color.hsv_v = color.hsv_v + 0.005
    if color.hsv_v == 1.0:
        color.hsv_v = 0.1

    ctr = ctr + 0.005

    _write_color(HSV(1.0 - color.hsv_h, 1.0 - color.hsv_s, 1.0 - color.hsv_v))


_write_msg("echo 'Note how often the RGB and RGBW codes differ'")

out_f.close()
