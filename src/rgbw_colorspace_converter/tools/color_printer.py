import os
import random

from rgbw_colorspace_converter.colors.converters import RGB


# Write colors module using colr!
def print_colors(
    color=None,
    print_chars="_",
    ansi_bat_f=None,
    ansi_html_f=None,
    col_width=10,
    print_color_codes=False,
    random_col_len=False,
    no_newlines=False,
    right_just_term_width="",
    check_term_size=True,
    print_bars=False,
    capture_output=True,
    random_block_len=False,
    n_row=-1,
    foreground_color=None,
    background_color=None,
    cycle_chars=False,
    zigzag=False,
    zag_max=100,
    multiply_txt=True,
):

    if color is None and foreground_color is None and background_color is None:
        raise Exception(
            "\t\t\t\n\n\t\t\tYou must specify color UNLESS you specify both background_color and foreground_color independently."
        )

    if foreground_color is None:
        foreground_color = color
    if background_color is None:
        if print_bars:
            background_color = color
        else:
            background_color = RGB(1, 1, 1)

    no_newlines_flag = ""
    if no_newlines:
        no_newlines_flag = " -n "

    if check_term_size:
        col_width = os.get_terminal_size().columns - 2

    ret_code = None
    blk = RGB(1, 1, 1)

    cap_o = ""
    if capture_output is True:
        cap_o = f" | tee -a {ansi_bat_f} "

    if n_row == -1:
        os.environ["char_string"] = print_chars * int(col_width * 2)

    if n_row == 0:
        # Set the env var holding the char string to be used
        os.environ["char_string"] = print_chars * int(col_width * 2)
        while n_row < 13:
            ph = str("pleaseholddlohesaelp" * 40)[0 : col_width - 1]
            os.system(
                f"colr {right_just_term_width} {no_newlines_flag}  ' {ph} ' '{blk.hex}' 'ff00ff'; "
            )
            ll = "O" * (col_width - 2)
            cmd = f"""colr {right_just_term_width}  " {ll} " "{blk.hex}" "{blk.hex}"  2>/dev/null;"""
            ret_code = os.system(cmd)
            n_row = n_row + 1

    l = ""
    if print_color_codes is False:
        # just print colors
        r = 1
        if random_block_len:
            r = random.randint(1, int(col_width * 1.85))
            r = float(r) / float(col_width)

        cw = int(col_width * r)
        if multiply_txt:
            l = str(str(os.environ["char_string"]) * cw)[0:cw]
        else:
            l = print_chars
        if cycle_chars:
            if zigzag:
                os.environ["zag_ctr"] = str(int(os.environ["zag_ctr"]) + 1)
                if int(os.environ["zag_ctr"]) > int(zag_max):
                    os.environ["zag_ctr"] = "0"
                    if os.environ["rgbw_char_dir"] == "L":
                        os.environ["rgbw_char_dir"] = "R"
                    else:
                        os.environ["rgbw_char_dir"] = "L"

            if os.environ["rgbw_char_dir"] in ["R"]:
                os.environ["char_string"] = (
                    os.environ["char_string"][-1] + os.environ["char_string"][0:-1]
                )
            else:
                os.environ["char_string"] = (
                    os.environ["char_string"][1:] + os.environ["char_string"][0]
                )

        cmd = f"""colr  {right_just_term_width}  {no_newlines_flag} " {l} " "{foreground_color.hex}" "{background_color.hex}" {cap_o} 2>/dev/null;"""
        ret_code = os.system(cmd)
    else:
        # Prtint color codes with color blocks
        l = "                    " + str(color)
        cmd = f"""colr  " {l} " "{foreground_color.hex}" "{background_color.hex}" {cap_o} 2>/dev/null;"""
        ret_code = os.system(cmd)

    return (int(ret_code), int(col_width))
