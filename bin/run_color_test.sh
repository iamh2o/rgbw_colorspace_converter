#!/bin/bash

[ ! -d "./bin" ] && echo "You must execute this command from the repo root directory(where the README.md lives)"

source ~/.bashrc

conda activate HBP

python ./bin/emit_color_fofn.py A

cat emit_color.cmds | parallel -j 1 -k

echo "--------------------- |FIN| ---------------------"

colr "                     ╦ ╦╔╗ ╔═╗                   " "255,0,0" "0,0,255"
colr "                     ╠═╣╠╩╗╠═╝                   " "255,0,0" "0,0,255"
colr "                     ╩ ╩╚═╝╩                     " "255,0,0" "0,0,255"
