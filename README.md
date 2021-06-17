# HBR (hex baaahs pyramid) RGBW Color Space Converter From HSL / RGB / HSI / HSV / HEX
## Specifically For LED Based Projects

Non-RGBW LEDs do a poor job of representing the observable color space, generally leaving gaps or complete gradients of pallates missing. This library will convert color space codes to RGBW for use in most new RGBW LEDs.

> We've become accostomed to the limited ability of RGB LEDs to produce truly diverse colors, but with the introduction of RGBW(white) LEDs, the ability of LEDs to replicate a more realistic spectrum of colors is dramatically increased.  The problem however, is decades of systems based on RGB, HEX, HSL do not offer easy transformations to RGBW from each system.  This package does just this, and only this.  If will return you RGBW for given tuples of other spaces, and do so fast enough for interactive LED projects.  There are a few helper functions and whatnot, but it's really as simple as (r,g,b,w) = Color.RGB(255,10,200).  Where 4 channel RGBW LEDs will translate the returned values to represent the richer color specified by the RGB tuple.

### 3 Main Projects Evolved This Library: HEX, BAAAHS and Pyramid Scheme.... hence.... HEXBASPYR ?
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<pre>
 ___  ___      _______       ___    ___  ________      ________      ________       ________     ___    ___  ________            |\  \|\  \    |\  ___ \     |\  \  /  /||\   __  \    |\   __  \    |\   ____\     |\   __  \   |\  \  /  /||\   __  \           \ \  \\\  \   \ \   __/|    \ \  \/  / /\ \  \|\ /_   \ \  \|\  \   \ \  \___|_    \ \  \|\  \  \ \  \/  / /\ \  \|\  \           \ \   __  \   \ \  \_|/__   \ \    / /  \ \   __  \   \ \   __  \   \ \_____  \    \ \   ____\  \ \    / /  \ \   _  _\           \ \  \ \  \   \ \  \_|\ \   /     \/    \ \  \|\  \   \ \  \ \  \   \|____|\  \    \ \  \___|   \/  /  /    \ \  \\  \|           \ \__\ \__\   \ \_______\ /  /\   \     \ \_______\   \ \__\ \__\    ____\_\  \    \ \__\    __/  / /       \ \__\\ _\            \|__|\|__|    \|_______|/__/ /\ __\     \|_______|    \|__|\|__|   |\_________\    \|__|   |\___/ /         \|__|\|__|                                   |__|/ \|__|                                \|_________|            \|___|/                           </pre>



# Right!

## Authors

GrgB wrote the vast majority of the core. JM translated Brian Nettlers theoretical work into code to allow the HS* and RGBW translations, JC added a lot of robustness and filled some algorithmic gaps- and generally made things presentable. This nugget of functionality has been present in projects that now span > 10 years. With multiple artists and show designers also contributing to the s/w (ie: TL, JH, SD, ZB, MF, LN).  This library is a small component of a much more elaborate framework to control custom fabricated LED installations.  Most recentlyly for Pyramid Scheme v-3 [PyramdTriangles](https://github.com/pyramidscheme/pyramidtriangles), which was a fork of the v-1 code [pyramid triangles codebase v1.0](https://github.com/iamh2o/pyramidtriangles), Pyramid Scheme followed several years of running the BAAAHS lighting installation (codebase lost to bitbucket purgatory). And the BAAAHS installation was the first gigantic project of the then baby faced HEX Collective (whom developed the core of this code speficially for a comissioned piece, aptlt dubbed [The Hex's](l;ink)... this repo also sadly lost to time and space.  This color library being an original component, and largely untouched until the need to support RGBW LEDs (and wow, rgbw LEDS are really stunning).

### Roar

It would be remiss of us not to  thank Steve Dudek for his Buffalo soothsaying and accurate measuring of 3 inch increments.

## So, How About Briefly-  What is Your Goal?

To pull this useful library out into a shareable form so that more LED hackers / artists might have a reduced barrier to entry in choosing RGBW chipsets to work with.

# Install

## Requirements

* [Python 3](https://www.python.org)

## Installation

### Add to PYTHONPATH

*  Put HBP_color_spacs_converter/lib in your PYTHONPATH.  Then ```import hbp_color as color``` 

### pip

* pip install hbp_color_space_converter

# Tests

* Simple at the moment, but you may run: ```pytest tests/```

# In The Works

*   * OLA Integration To Allow Testing LED Strips
*   * Example mini project to see for yourself the difference in vividness and saturation of RGBW vs RGB LEDs. You'll need hardware for this fwiw.


# Detailed Docs

<pre>

╦ ╦╔╗ ╔═╗
╠═╣╠╩╗╠═╝
╩ ╩╚═╝╩  

Color

Color class that allows you to initialize a color in any of HSV, HSL, HSI, RGB, Hex color spaces.  Once initialized,
the corresponding RGBW values are calculated and you may modify the object in RGB or HSV color spaces( ie: by re-setting
any component of HSV or RGB (ie, just resetting the R value) and all RGB/HSV/RGBW values will be recalculated.
As of now, you can not work in RGBW directly as we have not written the conversions from RGBW back to one of the
standard color spaces. (annoying, but so it goes).


The main goal of this class is to translate various color spaces into RGBW for use in RGBW pixels.

The color representation is maintained in HSV internally and translated to RGB and RGBW.
Use whichever is more convenient at the time - RGB for familiarity, HSV to fade colors easily.

RGB values range from 0 to 255
HSV values range from 0.0 to 1.0 *Note the H value has been normalized to range between 0-1 in instead of 0-360 to allow
for easier cycling of values.
HSL/HSI values range from 0-360 for H, 0-1 for S/[L|I]

    >>> red = RGB(255, 0 ,0)
    >>> red2 = RGBW(255, 0, 0, 0)
    >>> green = HSV(0.33, 1.0, 1.0)
    >>> green2 = RGBW(5, 254, 0, 0)
    >>> fuchsia = RGB(180, 48, 229)
    >>> fuchsia2 = RGBW(130, 0, 182, 47)

Colors may also be specified as hexadecimal string:

    >>> blue  = Hex('#0000ff')

Both RGB and HSV components are available as attributes
and may be set.

    >>> red.rgb_r
    255

    >>> red.rgb_g = 128
    >>> red.rgb
    (255, 128, 0)

    >>> red.hsv
    (0.08366013071895424, 1.0, 1.0)

These objects are mutable, so you may want to make a
copy before changing a Color that may be shared

    >>> red = RGB(255,0,0)
    >>> purple = red.copy()
    >>> purple.rgb_b = 255
    >>> red.rgb
    (255, 0, 0)
    >>> purple.rgb
    (255, 0, 255)

Brightness can be adjusted by setting the 'v' property, even
when you're working in RGB.

For example: to gradually dim a color
(ranges from 0.0 to 1.0)

    >>> col = RGB(0,255,0)
    >>> while col.v > 0:
    ...   print col.rgb
    ...   col.v -= 0.1
    ...
    (0, 255, 0)
    (0, 229, 0)
    (0, 204, 0)
    (0, 178, 0)
    (0, 153, 0)
    (0, 127, 0)
    (0, 102, 0)
    (0, 76, 0)
    (0, 51, 0)
    (0, 25, 0)

RGBW

To get the (r,g,b,w) tuples back from a Color object, simply call Color.rgbw and you will return the (r,g,b,w) tuple.

</pre>
