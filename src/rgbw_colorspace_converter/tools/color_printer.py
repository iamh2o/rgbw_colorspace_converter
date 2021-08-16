import os
import random


# Write colors module using colr!
def print_colors(
    color,
    print_chars="_",
    ansi_bat_f=None,
    ansi_html_f=None,
    col_width=78,
    print_codes="no",
    random_col_len=False,
    no_newlines=False,
    right_just_term_width="",
    check_term_size=True,
    print_bars=False,
    capture_output=True,
    random_block_len=False,
):

    if check_term_size:
        col_width = os.get_terminal_size().columns - 2

    ret_code = None
    bgcolor = "111111"
    if print_bars is True:
        bgcolor = color.hex

    cap_o = ""
    if capture_output is True:
        cap_o = f" | tee -a {ansi_bat_f} "

    l = ""
    if print_codes == "no":
        # just print colors
        r = 1
        if random_block_len:
            r = random.randint(1, col_width)

        len_pcs = len(print_chars)
        l = print_chars * (int(col_width / len_pcs) * r)
        cmd = f"""colr {right_just_term_width}  {no_newlines} " {l} " "{color.hex}" "{bgcolor}"  {cap_o} 2>/dev/null;"""
        ret_code = os.system(cmd)
    else:
        # Prtint color codes with color blocks
        l = "                    " + str(color)
        cmd = f"""colr  " {l} " "000000" "{color.hex}" {cap_o} 2>/dev/null;"""
        ret_code = os.system(cmd)

    return (int(ret_code), int(col_width))
