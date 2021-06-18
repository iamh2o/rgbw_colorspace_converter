#!/bin/bash
source ~/.bashrc
conda activate HBP

[ ! -d "./bin" ] && echo "You must execute this command from the repo root directory(where the README.md lives)"; sleep 2;

if [[ "$1" == "-h" ]]; then
    echo "

This is a testing / utility script, and kind of a little fun too.  It's not needed to use the library, but the python script it calls does have some simple examples of manipulating HBPcolor objects and using the resulting RGB codes for a simple terminal display.  Of course the real magic is using the RGBW codes with the proper hardware.  In anycase, this script takes TWO(2) positional arguments. Well, or none.  If you run the scrip with no arguments it will set pleasant defaults for you. The first argument is if youd like the RGB/RGBW/HSV/HSL/HSI/HEX codes printed with the color patterns:  either type 'yes' or 'no'(defauly=no).  The second is how many columns in the terminal do you wish to fill.  Setting it to be pretty full, but not wrapping is suggested.  This argument is simply an int (default=70).  Oh- and for laziness sake.  Please execuite this script from the root package directory.

This also being my first pip package, I'm not sure if this will be available in the standard install.  It will definitely be available if you run the development install.
"
exit 33;
fi

echo "---------------------------------- | WELCOME | --------------------------------"
colr "                                    ╦ ╦╔╗ ╔═╗                                  " "255,50,0" "100,0,255"
colr "                                    ╠═╣╠╩╗╠═╝                                  " "255,50,0" "100,0,255"
colr "                                    ╩ ╩╚═╝╩                                    " "255,50,0" "100,0,255"

sleep 3;

yn='no'
if [[ "$1" == "yes" ]]; then
    yn='yes'
else
    yn='no'
fi

cols=70
if [[ "$2" == "" ]]; then
    cols=70
else
    cols=$2
fi


python ./bin/emit_color_fofn.py $yn $cols

cat emit_color.cmds | parallel -j 1 -k


echo "------------------------------------ | FIN | -----------------------------------"
colr "                                    ╦ ╦╔╗ ╔═╗                                  " "255,0,0" "0,0,255"
colr "                                    ╠═╣╠╩╗╠═╝                                  " "255,0,0" "0,0,255"
colr "                                    ╩ ╩╚═╝╩                                    " "255,0,0" "0,0,255"

#rm emit_color.cmds
