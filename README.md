# HBR (hex baaahs pyramid) RGBW Color Space Converter From HSL / RGB / HSI / HSV / HEX
## Specifically For LED Based Projects

Non-RGBW LEDs do a poor job of representing the observable color space, generally leaving gaps or complete gradients of pallates missing. This library will convert color space codes to RGBW for use in most new RGBW LEDs.

> We've become accostomed to the limited ability of RGB LEDs to produce truly diverse colors, but with the introduction of RGBW(white) LEDs, the ability of LEDs to replicate a more realistic spectrum of colors is dramatically increased.  The problem however, is decades of systems based on RGB, HEX, HSL do not offer easy transformations to RGBW from each system.  This package does just this, and only this.  If will return you RGBW for given tuples of other spaces, and do so fast enough for interactive LED projects.  There are a few helper functions and whatnot, but it's really as simple as (r,g,b,w) = Color.RGB(255,10,200).  Where 4 channel RGBW LEDs will translate the returned values to represent the richer color specified by the RGB tuple.

### 3 Main Projects Evolved This Library: HEX, BAAAHS and Pyramid Scheme.... hence.... HEXBASPYR ?
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<pre>
 ___  ___      _______       ___    ___  ________      ________      ________       ________     ___    ___  ________            
|\  \|\  \    |\  ___ \     |\  \  /  /||\   __  \    |\   __  \    |\   ____\     |\   __  \   |\  \  /  /||\   __  \           
\ \  \\\  \   \ \   __/|    \ \  \/  / /\ \  \|\ /_   \ \  \|\  \   \ \  \___|_    \ \  \|\  \  \ \  \/  / /\ \  \|\  \          
 \ \   __  \   \ \  \_|/__   \ \    / /  \ \   __  \   \ \   __  \   \ \_____  \    \ \   ____\  \ \    / /  \ \   _  _\         
  \ \  \ \  \   \ \  \_|\ \   /     \/    \ \  \|\  \   \ \  \ \  \   \|____|\  \    \ \  \___|   \/  /  /    \ \  \\  \|        
   \ \__\ \__\   \ \_______\ /  /\   \     \ \_______\   \ \__\ \__\    ____\_\  \    \ \__\    __/  / /       \ \__\\ _\        
    \|__|\|__|    \|_______|/__/ /\ __\     \|_______|    \|__|\|__|   |\_________\    \|__|   |\___/ /         \|__|\|__|       
                            |__|/ \|__|                                \|_________|            \|___|/                                                  
</pre>



# Right!

## Authors

GrgB wrote the vast majority of the core. JM translated Brian Nettlers theoretical work into code to allow the translation from RGB/HSV/HSI to RGBW. JC added a lot of robustness and and in latter instances (which you can find in the pyramid triangles repo) filled  in some algorithmic gaps, which I have been unable to test yet, so have not included them yet. This nugget of code has been present in projects that now span > 10 years. With multiple artists and show designers also contributing to the s/w (ie: TL, JH, SD, ZB, MF, LN).  This library is a small component of a much more elaborate framework to control custom fabricated LED installations.  Most recentlyly for Pyramid Scheme v-3 [PyramdTriangles](https://github.com/pyramidscheme/pyramidtriangles), which was a fork of the v-1 code [pyramid triangles codebase v1.0](https://github.com/iamh2o/pyramidtriangles), Pyramid Scheme followed several years of running the BAAAHS lighting installation (codebase lost to bitbucket purgatory). And the BAAAHS installation was the first gigantic project of the then baby faced HEX Collective (whom developed the core of this code speficially for a comissioned piece, aptlt dubbed [The Hex's](l;ink)... this repo also sadly lost to time and space.  This color library being an original component, and largely untouched until the need to support RGBW LEDs (and wow, rgbw LEDS are really stunning).

### Roar

It would be remiss of us not to  thank Steve Dudek for his Buffalo soothsaying and accurate measuring of 3 inch increments.

## So, How About Briefly-  What is Your Goal Again?

To pull this useful library out into a shareable form so that more LED hackers / artists might have a reduced barrier to entry in choosing RGBW chipsets to work with.

# Let's Do It: INSTALL

## Requirements

* [Python 3](https://www.python.org)

## Install Options

### BASIC: Add to PYTHONPATH

*  Put HBP_color_spacs_converter/lib in your PYTHONPATH.  Then

```
from hpb.colorspace_converter.hbp_colorspace_converter import RGB

rgb = RGB(255,10,155)
print(rgb.rgbw)
->(247, 0, 144, 8)
rgb.hsv
-> (0.9013605442176871, 0.9607843137254902, 1.0)
rgb.hex
->'#ff099b'
```

### pip

* pip install hbp_color_space_converter
```
from hbp_colorspace_converter import RGB

rgb = RGB(255,10,155)
print(rgb.rgbw)
->(247, 0, 144, 8)
print(rgb.hsv)
->(0.9013605442176871, 0.9607843137254902, 1.0)
rgb.hex
->'#ff99b'
```

## Contribute

Please do ask questions, discuss new feature requests, file bugs, etc.  You are empowered to add new features, but try to talk it through with the repo admins first-  though if youre really burning to code, we can talk with the code in front of us.  PRs are the way to propose changes.  No commits to main are allowed.  Actions/Tests must all pass as well as review by 2 folks equiped to eval the proposed changes.
Development (less stable)

### Install Dev Env
```
cd environment
./setup.sh #  Read the help text.  To proceed with install:
./setup.sh HBP ~/conda # or wherever your conda is installed or you want it installed
```
* This will install a conda environment you can source with conda activate HBP. If you don't have conda, it is installed where you specify.  Mamba is also installed (read about it. tlds, lightning fast conda) to mane environment creation faster.

* pre-commit checks will be installed to enforce black and flake 8 before any pushes.  Be aware.  Black will auto-fix problems. Flake8, you need to go manually address the issues.


## More Examples

### A Bit More Advanced

Not only does the package allow translation of one color space to another, but it also allows modifications of the color object in real time that re-calculates all of the other color space values at the same time.  This is *EXCEEDINGLY* helpful if you wish to do things like slice through HSV space, and only change the saturation, or the hue. This is simply decrementing the H or S value incremntally, but in RGB space, is a complex juggling of changing all 3 RGB values in non intuitive ways.  The same applies for transversals of HSI or HSL space to RGB.  We often found ourselves writing our shows in HSV/HSL and trnanslating to RGBW for the LED hardware to display b/c the showe were more natural to design in non-RGB.

If you build the developemtn branch, there is a test script in ./bin/ called 'transversals.py', which gives you a crude terminal based idea of what I'm talking about (limited to 256 colors).

What that might look like in code could be:
```
from hbp_colorspace_converter.hbp_colorspace_converter import RGB
rgb = RGB(0,0,255) # BLUE

# HSL value for blue
In [32]: rgb.hsl
Out[32]: (240, 1.0, 0.5)
#HSV value for Blue
In [33]: rgb.hsv
Out[33]: (0.6666666666666666, 1.0, 1.0)
In [34]: rgb.rgbw
Out[34]: (0, 0, 255, 0)

from hbp_colorspace_converter.hbp_colorspace_converter import Color

color = Color(rgb.hsv)

In [40]: color
Out[40]: rgb=(0, 0, 255) hsv=(0.6666666666666666, 1.0, 1.0) rgbw=(0, 0, 255, 0) hsl=(240, 1.0, 0.5)


# Tests

## Command Line
* Simple at the moment, but you may run: 
    * ```pytest --exitfirst --verbose --failed-first --cov=. --cov-report html```

## Github Actions
* Flak8 and Python Black are both tested with github commiut action, as is the pytest above.

# In The Works

    * OLA Integration To Allow Testing LED Strips
    * Example mini project to see for yourself the difference in vividness and saturation of RGBW vs RGB LEDs. You'll need hardware for this fwiw.


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
when you're working in RGB because the native movel is maintained in HSV.

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



                                                                                                              
A more complex example is if you wished to move through HUE space in HSV and display that in RGB (or RGBW)              


from hbp_colorspace_converter.hbp_colorspace_converter import RGB
magenta = RGB(255, 120, 255)
# in HSV it looks like this

magenta.hsv
(0.8333333333333334, 0.5294117647058824, 1.0)

To cycle through hue's in RGB space is incredibly cumbersome. But in HSV space, you simply cycle through 0-1 (and loop back around bc the space is a cylinder!).  So, something like this:

magenta = RGB(255, 120, 255)
In [12]: while ctr < 8:
    ...:     magenta.h = magenta.h - .1
    ...:     print(magenta.hsv, magenta.rgb)
    ...:     ctr = ctr + 1
    ...: 
    ...: 
(0.73333333, 0.5294117647058824, 1.0) (173, 120, 255)
(0.63333333, 0.5294117647058824, 1.0) (120, 147, 255)
(0.53333333, 0.5294117647058824, 1.0) (120, 228, 255)
(0.43333333, 0.5294117647058824, 1.0) (120, 255, 200)
(0.33333333, 0.5294117647058824, 1.0) (120, 255, 120)
(0.23333333, 0.5294117647058824, 1.0) (201, 255, 120)
(0.13333333, 0.5294117647058824, 1.0) (255, 227, 120)
(0.03333333, 0.5294117647058824, 1.0) (255, 146, 120)
(0.0, 0.5294117647058824, 1.0) (255, 120, 120)

! Note how clear the movement through HSV space is, and how unintuituve the RGB transitions are.  This module helps make this usability gap between the more intuitive color spaces and RGB smaller (AND GIVES US RGBW!)

RGBW

To get the (r,g,b,w) tuples back from a Color object, simply call Color.rgbw and you will return the (r,g,b,w) tuple.

</pre>
