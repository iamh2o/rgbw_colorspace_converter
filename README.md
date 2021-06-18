# HBP: RGBW Color Space Converter Between HSL / RGB / HSi / HSV / HEX
## Specifically For LED Based Projects
![Farewell]( https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/blob/main/images/bar21.png )

Non-RGBW LEDs do a poor job of representing the observable color space, generally leaving gaps or complete gradients of pallates missing. This library will convert color space codes to RGBW for use in most new RGBW LEDs.

> We've become accostomed to the limited ability of RGB LEDs to produce truly diverse colors, but with the introduction of RGBW(white) LEDs, the ability of LEDs to replicate a more realistic spectrum of colors is dramatically increased.  The problem however, is decades of systems based on RGB, HEX, HSL do not offer easy transformations to RGBW from each system.  This package does just this, and only this.  If will return you RGBW for given tuples of other spaces, and do so fast enough for interactive LED projects.  There are a few helper functions and whatnot, but it's really as simple as (r,g,b,w) = Color.RGB(255,10,200).  Where 4 channel RGBW LEDs will translate the returned values to represent the richer color specified by the RGB tuple.

> Or! Go ahead and use this for non LED projects where you need to convert between color spaces.  Say for controlling old skool DMX lighting rigs.

### 3 Main Projects Evolved This Library: HEX, BAAAHS and Pyramid Scheme.... hence.... HEXBASPYR ?

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  [![Run Color Tests](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/actions/workflows/ci.yml/badge.svg)](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/actions/workflows/ci.yml) [![Lint](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/actions/workflows/black.yaml/badge.svg)](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/actions/workflows/black.yaml) ![LED ART](https://img.shields.io/badge/A--R--T-L.E.D.-white?style=plastic)

.

<pre>
 ___  ___    _______       ___    ___  ________     ________     ________     ________    ___    ___  ________            
\ \  \\\  \ \ \   __/|    \ \  \/  / /\ \  \|\ /_  \ \  \|\  \  \ \  \___|_  \ \  \|\  \ \ \  \/  / /\ \  \|\  \          
 \ \   __  \ \ \  \_|/__   \ \    / /  \ \   __  \  \ \   __  \  \ \_____  \  \ \   ____\ \ \    / /  \ \   _  _\         
  \ \  \ \  \ \ \  \_|\ \   /     \/    \ \  \|\  \  \ \  \ \  \  \|____|\  \  \ \  \___|  \/  /  /    \ \  \\  \|        
   \ \__\ \__\ \ \_______\ /  /\   \     \ \_______\  \ \__\ \__\   ____\_\  \  \ \__\   __/  / /       \ \__\\ _\        
    \|__|\|__|  \|_______|/__/ /\ __\     \|_______|   \|__|\|__|  |\_________\  \|__|  |\___/ /         \|__|\|__|       
                          |__|/ \|__|                             \|_________|        \|___|/                                                  </pre>
![Farewell](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/blob/main/images/bars5.png)

# Right!

## Authors

GrgB wrote the vast majority of the core. JM translated Brian Nettlers theoretical work into code to allow the translation from RGB/HSV/HSI to RGBW. JC added a lot of robustness and and in latter instances (which you can find in the pyramid triangles repo) filled  in some algorithmic gaps, which I have been unable to test yet, so have not included them yet. This nugget of code has been present in projects that now span > 10 years. With multiple artists and show designers also contributing to the s/w (ie: TL, JH, SD, ZB, MF, LN).  This library is a small component of a much more elaborate framework to control custom fabricated LED installations.  Most recentlyly for Pyramid Scheme v-3 [PyramdTriangles](https://github.com/pyramidscheme/pyramidtriangles), which was a fork of the v-1 code [pyramid triangles codebase v1.0](https://github.com/iamh2o/pyramidtriangles), Pyramid Scheme followed several years of running the BAAAHS lighting installation (codebase lost to bitbucket purgatory). And the BAAAHS installation was the first gigantic project of the then baby faced HEX Collective (whom developed the core of this code speficially for a comissioned piece, aptlt dubbed [The Hex's](l;ink)... this repo also sadly lost to time and space.  This color library being an original component, and largely untouched until the need to support RGBW LEDs (and wow, rgbw LEDS are really stunning).

### Roar

It would be remiss of us not to  thank Steve Dudek for his Buffalo soothsaying and accurate measuring of 3 inch increments.

## So, How About Briefly-  What is Your Goal Again?

To pull this useful library out into a shareable form so that more LED hackers / artists might have a reduced barrier to entry in choosing RGBW chipsets to work with.



![Farewell]( https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/blob/main/images/bar20.png)

# Let's Do It: INSTALL



## Requirements

* [Python 3](https://www.python.org)

## Install Options

### BASIC: Add to PYTHONPATH

*  Put color_spacs_converter in your PYTHONPATH.  Then

#### While We're Here, Super Fast Crash Cource
```
from colorspace_converter.colorspace_converter import Color, RGB, HSV

>  The Color class is the top level class, but the RGB and HSV classes inherit from it and do all of the same work. Its intended to be expanded upon at some point, but for now, you can honesly choose any of them.  You can instantiate 'Color(RGB/HSL)' objext only.  Once instantiated, they calculate and maintain the state of the 5 other color spaces these objects manage (HSL, HSi, HEX, RGBW, i guess just 4 others, 6 total.

# Begin Like So:
from colorspace_converter.colorspace_converter import RGB, Color, HSV

rgb = RGB(255,125,22)
rgb.(tab in an interactive shell) and you'll see:
```

>``````
> 
>        rgb...
>               copy()     hsl     hsv_s   rgb     rgb_r    rgbw_b  gbw_w 	      
>               hex        hsv     hsv_t   rgb_b   rgbw_w   rgbw_g         
>               hsi        hsv_h   hsv_v   rgb_g   rgbw     rgbw_r         
>``````

These are the objects and functions available to the Color/HSV and RGB top level objects alike.  There are 3 main classes here.
1) Objects, which when called will give you that color schemes encoding for whatever is currently set by RGB/HSV.  
1b) Note, the core color space used in this module is actually HSV.  The HSV and RGB mappings are tightly coupled.  If you change the RGB.RED value, the HSV values immediately recalculate (as do the values for all of the second order color space objects.
2) The second order color space objects will generallty let you instantiate an object with their values, but you will get back  Color object which will not accept modifications of the second order object properties (again- to make changes you'll need to modify RGB or HSV values. Then there are third order objects which it is not yet possible to instantiate them directly from their native parameters, but we can calculate their values given any first or second order object- this mostly applies to RGBW-- but the problem is small in our exper4ience, nearly all of the use cases for RGBW is getting a realistic transofrmation to RGBW space from these others. We're here to help!
3)Recap:  First order objects: Color, RGB, HSV. Second order (HSL, HSi, HEX. Third order object, but still loved, RGBW.
4) all obect used by name (ie: rgb.hsi ) return a tuple of their values refkectiung the color represented by the RGB and HSV internal values.    The same is tru for .hsv, .hsi, .rgbw....
5) First order objects have the special features of getters and setters.  HSV objects have hsv_v, hsv_s, hsv_h.  Used w/out assignment they reuturn the single value.  Used with assignment, the valiue is updated, and all of the other objects have their values recalculated immediately.  The same goes for RGB, there is rgb_r, rgb_g, rgb_b.  The setters are the encourated way to update the global color of the color objexts.  No save is required.  The hsv_t property is a special internal use tuple of the HSV representation of the current color. Do not muck around with please.  Lastly, there is a function 'copy'.  If you with to spin off a safe Color object to play with, in say, multithreaded envirionments, use copy to deepcopy the Color object you are using.
6) That was longer than I thought, but covers a large part of the basiscs. We are translating between spaces, and allowing programatic use of the obbject to acheive smooth/natural/more intuative control of RGb/RGBW LED hardware ( Ask be about runing huge installations over DMX Sometime )
7) OH!  for the wackadoodle color spaces that like to use one member of the tuple being 0-356degreesm we converted those to 0-1 scales (dividing values by360)
</pre>
So, here is, I really promise, a micro example of how this might work

```
from hbp_colorspace_converter.hbp_colorspace_converter import RGB, Color, HSV

rgb = RGB(126,11,230)

print(rgb)
->rgb=(126, 10, 230) 
->hsv=(0.754185692541857, 0.9521739130434783, 0.9019607843137255) 
->rgbw=(255, 4, 0, 9) hsl=(0.754185692541857, 0.9087136929460582, 0.4725490196078431) 
->hsi=(0.7545454545454545, 0.918031967204918, 0.47842658823529416)  # note- printing the rgb or hsv object will display all the color setting presently active for all obects.

print(rgb.hsi)
(0.7545454545454545, 0.918031967204918, 0.47842658823529416) #returns just the HSI tuple

print(rgb.hsv)
(0.754185692541857, 0.9521739130434783, 0.9019607843137255) #returns the current state of the HSV object which reflects (nearly) the same color as the hsv values)

# But lets change a value, and do it via the hsv object, but reaching through the rgb object!
rgb.hsv_s = 0.0

# Note how all the other objects values have not changed to reflect the new color

print(rgb.hsv) -->(0.754185692541857, 0.0, 0.9019607843137255)

print(rgb.rgb) --> (230, 230, 230)

rgb.hsv --> (0.754185692541857, 0.0, 0.9019607843137255)

```

<b> Putting it all together</a>
* You can set you favorite RGB color (or HSV/HSI/whatever), then use the 0-1 scaled hue/saturation/value(brightness) to more gracefully move through color spaces. A simple example being decrementing just the 'V' part of HSV to dim or brighten the color of choice w/out changing it.  This is non-trivial to do with RGB.</b>
* OK, so many words here. I hope something helps someone save some time :-)


## More On Installation

### Using pip

* pip install hcolor_space_converter


```
from colorspace_converter import RGB

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
* This will install a conda environment you can source with conda activate HBP. If you don't have conda, it is installed where you specify.  Mamba is also installed (read about it. tldr: lightning fast conda, will change your life). The codebase adheres to black style and mostly to flake8.

* Duering the running of setup above, pre-commit checks will be installed to enforce black and flake 8 compliance before any pushes are permitted. Full disclosure.  Black will auto-fix problems when it fails a commit, so you just run again and all is good.  RARELY, you'll have to run 'black' directly on the file. Flake8, you need to go manually address the issues is spits out.  If there are a ton, chip away at a few, then you can use the --skip-verify commit flag- but don't abuse it please.

* Upon commit, flake 8 and black linter checks are run, as well as the pyunit tests for each commit and pull request.  The status of each can be seen in the actions tab and reflected in some of the badges.

### Some Cool Stuff.

* I've worked up a lowtech way to demonstrating cycling through various color spaces programatically using the terminal.  If you've run setup.sh, this should run for you.  Try running ``conda activate CSC; python ./bin/run_color_funthing.sh [rgb-r, rgb-g, rgb-b, hsv-h, hsv-s, hsv-v].   you get a taste for how the spaces cycle differently and what the encoding for each looks like. but really, this is meant to really be helpful in extractin the RGBW signal for use with RGBW LEDs..... something I can't demonstrate withouth hardware.

#### Perhaps a simple hardware how-to should be on the to-do list?


## More Examples

### A Bit More Advanced

Not only does the package allow translation of one color space to another, but it also allows modifications of the color object in real time that re-calculates all of the other color space values at the same time.  This is *EXCEEDINGLY* helpful if you wish to do things like slice through HSV space, and only change the saturation, or the hue. This is simply decrementing the H or S value incremntally, but in RGB space, is a complex juggling of changing all 3 RGB values in non intuitive ways.  The same applies for transversals of HSI or HSL space to RGB.  We often found ourselves writing our shows in HSV/HSL and trnanslating to RGBW for the LED hardware to display b/c the showe were more natural to design in non-RGB.

If you build the developemtn branch, there is a test script in ./bin/ called 'transversals.py', which gives you a crude terminal based idea of what I'm talking about (limited to 256 colors).

What that might look like in code could be:

```
>>> from colorspace_converter.colorspace_converter import RGB
>>> rgb = RGB(0,0,255) # BLUE

# HSL value for blue
>>>rgb.hsl
(240, 1.0, 0.5)

#HSV value for Blue
>>> rgb.hsv
(0.6666666666666666, 1.0, 1.0)

>>> rgb.rgbw
(0, 0, 255, 0)


>>> from colorspace_converter.colorspace_converter import Color

>>> color = Color(rgb.hsv)
>>> color
rgb=(0, 0, 255) hsv=(0.6666666666666666, 1.0, 1.0) rgbw=(0, 0, 255, 0) hsl=(240, 1.0, 0.5)
```


![qq](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/blob/main/images/bar33.png)


# Tests

## Command Line
* Simple at the moment, but you may run: 
    * ```pytest --exitfirst --verbose --failed-first --cov=. --cov-report html```

## Github Actions
* Flak8 and Python Black are both tested with github commiut action, as is the pytest above.

## Fun & Kind Of Weird Tests

* I was going to write a light web UI to output various color space codes and the RGB values, but that kind of defeats the purpose, which is to allow usage of the super awesome RGBW LEDs in projects.  And video screens just can't do real-life RGBW LEDs justice.  So, I wote more of a test toy script that just uses really crude terminal colors :-P.  If you've installed the dev environment, this should do the trick:

```
source ~/.bashrc
python ./bin/run_color_test.sh

# In The Works

    * OLA Integration To Allow Testing LED Strips
    * Example mini project to see for yourself the difference in vividness and saturation of RGBW vs RGB LEDs. You'll need hardware for this fwiw.


# Detailed Docs // Examples

Color

Color class that allows you to initialize a color in any of HSV, HSL, HSI, RGB, Hex color spaces.  Once initialized,
the corresponding RGBW values are calculated and you may modify the object in RGB or HSV color spaces( ie: by re-setting
any component of HSV(_h|_s|_v) or RGB(_r|_g|_b) (ie, just resetting the R value) and all RGB/HSV/RGBW/HSL/HSV/HSI/HEX values will be recalculated. note-  if not setting a value to, say, RGB_r, it will simply return the 0-255 code for 'r'.
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
    >>> green = HSV(0.33, 1.0, 1.0)
    >>> fuchsia = RGB(180, 48, 229)

Colors may also be specified as hexadecimal string:

    >>> blue  = Hex('#0000ff')

Both RGB and HSV components are available as attributes
and may be set.

    >>> red = RGB(255,0,0)
    >>> red.rgb_r
    255

    >>> red.rgb_g = 128
    >>> red.rgb
    (255, 128, 0)

    >>> red.hsv
    (0.08366013071895424, 1.0, 1.0)

    >>> red.hsv_v = 0.5
    >>> red.rgb
    (127, 64, 0)
    >>> red.hsv
    (0.08366013071895424, 1.0, 0.5)
    # Note how as you change the hsv_(h|s|v) or rgb_(r|g|b) properties, the other values are recalculated for the other color types
    
--->>>    # IMPORTANT -- This recalculation after instantiation *only* is allowed for hsv and rgb types.  The HSL/HSV/HSI/RGBW values are all calculated upone instantiation of the Color object **AND** the values for each are updated in real time as the hsv(h|s|v) and rgb(r|g|b) values are modified in the Color object.  But, you can not modify the individual elements of HSL/HSI/RGBW/HEX objects directly after instantiating each.  Put another way. If you create a HSI object, to get a new HSI color value you need to modify r/g/b or h/s/v (or create a new HSI object).

These objects are mutable, so you may want to make a
copy before changing a Color that may be shared

    >>> red = RGB(255,0,0)
    >>> purple = red.copy()
    >>> purple.rgb_b = 255
    >>> red.rgb
    (255, 0, 0)
    >>> purple.rgb
    (255, 0, 255)

Brightness can be adjusted by setting the 'color.hsv_v' property, even
when you're working in RGB because the native movel is maintained in HSV.

For example: to gradually dim a color
(ranges from 0.0 to 1.0)

    >>> col = RGB(0,255,0)
    >>> while col.hsv_v > 0:
    ...   col.hsv_v -= 0.1
    ...   print col.rgb
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
		#  And you could mix and match if you're feeling crazy.  col.hsv_v -=10 ; col_rgb_g = 102; print(col);


                                                                                                              
A more complex example is if you wished to move through HUE space in HSV and display that in RGB (or RGBW)              


from colorspace_converter.colorspace_converter import RGB
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



                -----------------------------------|          |-----------------------------------
                                                     ╦ ╦╔╗ ╔═╗                                  
                                                     ╠═╣╠╩╗╠═╝                                  
                                                     ╩ ╩╚═╝╩

```



![Farewell](https://github.com/iamh2o/HBP-RGBW-Color-Space-Converter/blob/main/images/Screen%20Shot%202021-06-17%20at%205.12.35%20PM.png)
