"""
Color implements RGBW color values, with the RGB portion able to be modeled
in CIE perceptual color spaces.
"""

#
# a Python port of go-colorful
# Copyright © 2013 Lucas Beyer
# https://github.com/lucasb-eyer/go-colorful
#

from .color import Color, color, white
from .scale import Scale
from .space import RGB, Lab, HCL
