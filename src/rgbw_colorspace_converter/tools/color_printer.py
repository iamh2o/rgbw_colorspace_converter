import os
import random


# Write colors module using colr!
def print_colors(
    color,
    print_char="_",
    ansi_bat_f=None,
    ansi_html_f=None,
    col_width=78,
    print_codes="no",
    random_col_len=False,
    no_newlines=False,
    right_just_term_width="",
):

    global std_out_only
    global cmd_suffix
    cmd_suffix = ""
    std_out_only = True
    if ansi_bat_f not in [None]:
        std_out_only = False
        cmd_suffix = " >> {ansi_bat_f} "

    ret_code = 0
    cmd = ""

    if print_codes == "no":
        # just print colors
        r = 1
        if random_col_len:
            r = random.randint(1, 54)
        print_chars = print_char * (col_width * r)
        cmd = f"""colr {right_just_term_width}  {no_newlines} " {print_chars} " "{color.hex}" "{color.hex}"  {cmd_suffix} 2>/dev/null;"""
        ret_code = os.system(cmd)
    else:
        # Prtint color codes with color blocks
        print_chars = "                    " + str(color)
        cmd = f"""colr  " {print_chars} " "000000" "{color.hex}" {cmd_suffix} 2>/dev/null;"""
        ret_code = os.system(cmd)

    if std_out_only is False:
        os.system(f"tail -n 1 {ansi_bat_f} &")
        os.system(f"tail -n 1 {ansi_bat_f} | ansi2html -i >> {ansi_html_f} &")

    return int(ret_code)
