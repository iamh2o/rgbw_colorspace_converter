#!/usr/bin/env python

# --> Original work by ---> from https://gist.github.com/satoruhiga/5736193

"""
DEPENDENCIES:
$ brew install ffmpeg
$ brew install imagemagick
$ python ./mov2gif.py input.mov output.gif 15
"""

import sys
import os
import tempfile
import shutil
import subprocess

print("aaaa")
if len(sys.argv) <= 2:
    print("usage: ", sys.argv[0], "[INPUT_MOV_FILENAME]", "[OUTPUT_GIF_FILENAME]", "[FPS]")

    sys.exit(-1)

assert os.path.exists(sys.argv[1])
INPUT_MOV_FILENAME = sys.argv[1]

OUTPUT_GIF_FILENAME = sys.argv[2]

try:
    FPS = int(sys.argv[3])
except Exception as e:
    del e
    FPS = 10

temp = tempfile.mkdtemp()

cmd = "ffmpeg -loglevel quiet -i %(INPUT_MOV_FILENAME)s -r %(FPS)i %(TEMP)s" % {
    "INPUT_MOV_FILENAME": INPUT_MOV_FILENAME,
    "FPS": FPS,
    "TEMP": os.path.join(temp, "%5d.png"),
}
subprocess.check_call(cmd, shell=True)

cmd = "convert -delay 1x%(FPS)i %(TEMP)s %(OUTPUT_GIF_FILENAME)s" % {
    "FPS": FPS,
    "TEMP": os.path.join(temp, "*.png"),
    "OUTPUT_GIF_FILENAME": OUTPUT_GIF_FILENAME,
}
subprocess.check_call(cmd, shell=True)

shutil.rmtree(temp)

cmd = "open -R %(OUTPUT_GIF_FILENAME)s" % {"OUTPUT_GIF_FILENAME": OUTPUT_GIF_FILENAME}
subprocess.check_call(cmd, shell=True)

print("done")
