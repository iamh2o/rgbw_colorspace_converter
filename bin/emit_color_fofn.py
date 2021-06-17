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
    cmd = f""" echo "Color Codes: {color} ";  colr "          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" "{color.rgb_r},{color.rgb_g},{color.rgb_b}" "{color.rgb_r},{color.rgb_g},{color.rgb_b}"; sleep 0.1; """
    out_f.write(f"{cmd}\n")


def _write_msg(msg):
    out_f.write(f"{msg}\n")


color = RGB(255, 255, 255)

_write_msg(
    f"""'STARTING OFF WITH WHITE, ',{color} , 'and cycling through each of h,s,v-- white for HSV is {color.hsv}\n\n' """
)

while color.hsv_h < 1.0:
    print("X", color)
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.005

    if color.hsv_h > 0.99:
        if color.hsv_s == 0.0:
            _write_msg(
                "echo ' DONE CYCLING THROUGH H, NOW CYCLING THROUGH S'; sleep 2;"
            )

            while color.hsv_s < 1.0:
                _write_color(color)
                color.hsv_s = color.hsv_s + 0.005

                if color.hsv_s > 0.99:
                    if color.hsv_v == 1.0:
                        _write_msg(
                            "echo ' DONE CYCLING THROUGH S, NOW CYCLING THROUGH V'; sleep 2;"
                        )
                    while color.hsv_v > 0.0:
                        _write_color(color)
                        color.hsv_v -= 0.005


_write_msg(
    "echo ' And that is cycling through each of the HSV comonents independently'; sleep 4;"
)
_write_msg(
    "echo ' For kicks, here is starting with H and V at 0 and S at 1 and cycling '; sleep 2"
)
color = HSV(h=0.0, s=1.0, v=0.0)
while color.hsv_h < 1.0:
    _write_color(color)
    color.hsv_h = color.hsv_h + 0.005
    color.hsv_h = color.hsv_h - 0.005
    color.hsv_h = color.hsv_h + 0.005


_write_msg("Note how often the RGB and RGBW codes differ")

out_f.close()
