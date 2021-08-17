#!/usr/bin/env python

import os
import sys

from chromedriver_py import binary_path

print('''This command will fail if you have not run the setup.py script AND "source environment/env.sh" first.\n\n\nIt is installing a headless chrome web browser driver to allow making an image out of the big demo script sessions.  It's not required to run the s/w, but nice to have''')
os.chdir(f"{os.environ['RGBW_CC_ROOT']}/bin/")
cmd = f"cp {binary_path} {os.environ['RGBW_CC_ROOT']}/bin/chrome; chmod a+x ./chrome; ln -s chrome chromium;"
os.system(cmd)
