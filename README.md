# HBP: RGBW Color Space Converter Between HSL / RGB / HSI / HSV / HEX
## Specifically For LED Based Projects
![HBP]( https://raw.githubusercontent.com/iamh2o/rgbw_colorspace_converter/main/images/bar21.png )
[![wakatime](https://wakatime.com/badge/github/iamh2o/rgbw_colorspace_converter.svg)](https://wakatime.com/badge/github/iamh2o/rgbw_colorspace_converter) [![Run Color Tests 2](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/pytest.yml/badge.svg)](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/pytest.yml)  [![Lint](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/black.yaml/badge.svg)](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/black.yaml) [![bashLint](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/bashLint.yml/badge.svg)](https://github.com/iamh2o/rgbw_colorspace_converter/actions/workflows/bashLint.yml)  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)  ![LED ART](https://img.shields.io/badge/A--R--T-L.E.D.-white?style=plastic)  [![PLACEHOLDER](https://img.shields.io/badge/color-~colorspace~-orange?style=plastic)](http://placeholder.com) [![GitHub version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&r=r&type=6e&v=0.0.11&x2=0)](https://badge.fury.io/gh/iamh2o%2Frgbw_colorspace_converter)


## RGBW ! Why?
* RGBW LEDs allow direct production of much more of the colorspace people are able to observe, as opposed to RGB, which relies on perceptual effects to trick you into seeing a color.  A good example are pastel colors, almost impossible with RGB, very beautiful in RGBW. And just generaly, the experience in real life feel richer with RGBW, probably b/c there is one more layer of data input.
* No more RGB shadows when using white light!!!  Since RGB replicates white light by RGB all on, there is always an offset in the emitters physical location, which ends up leaving RGB shadows on the edges of the white light illuminated area.  This is not a problem with a true W channel.
* And... [we were building this // better res pics and videos here](pyramid_scheme/README.md): <A hrref=pyramid_scheme/README.md ><img src=https://github.com/iamh2o/rgbw_colorspace_converter/blob/27be89226851c1cea834542750ebb4201116b47b/pyramid_scheme/Pyr_ctrim.gif height=150 width=220 ></img>  <img src=pyramid_scheme/pyramid_moody.JPG height=150 width=220></img>

* `if there is a stutter, it's due to the animated gif :-)`

### What is the utility of this module?

<ul>
tldr:  The `color` module within this package will translate various color systems into each other, but most useful is the conversion to RGBW as well. This is a niche use case,. mostly applicable to lighting and LEDs specifically. It is object based, so operating on the object to change properties of the color will automatically translate to all th other color spaces-  this makes it supremely useful in programatic LED applications where you might want to have algorithmic generative art. To see a couple of test examples of using the object, see the ansi art generating scripts, or my novel below.  
</ul>


#### Conceptually, How It Works

<ul>
	
More or less the process is: Instantiate a color object from any of the supported types.  Use the returned object to emit values for all types(including RGBW). Modify the RGB or HSV objects by their r/g/b or h/s/v properties (even interchangibly!  This is killer because, if you want to simply dim a non-saturated color, the rgb path is pretty complicated.  But in HSV you can simply decrement the 'V' in the color.hsv object to dim the color and simultaneously emit the RGB values for the dimmed color (which can be sent to hardware). I tend to operate in HSV space, but send signals in RGB or RGBW space to hardware. But can be used also as a general color manipulator and translator.

> We've become accustomed to the limited ability of RGB LEDs to produce truly diverse colors, but with the introduction of RGBW(white) LEDs, the ability of LEDs to replicate a more realistic spectrum of colors is dramatically increased.  The problem however, is decades of systems based on RGB, HEX, HSL do not offer easy transformations to RGBW from each system.  This package does  this for you.  And further, we believe it makes programatic manipulation of colors for LED/art projects more natural/intuitive.  If will return you RGBW for given tuples of other spaces, and do so fast enough for interactive LED projects.  There are a few helper functions and whatnot, but it's really as simple as (r,g,b,w) = Color.RGB(255,10,200).  Where 4 channel RGBW LEDs will translate the returned values to represent the richer color specified by the RGB tuple.

> Or! Go ahead and use this for non LED projects where you need to convert between color spaces.  Say for controlling old skool DMX lighting rigs.

</ul>

#### Show Me The Math
* We started from first principles, all of the converters mathmatical formulas for converting between color spaces are laid out in the converter module. [This is the formula to move from HSI to RGBW, for example. Much of the math is drawn from other sources, references noted where applicable.](https://github.com/iamh2o/rgbw_colorspace_converter/blob/5dfbf9fd3d519939191d7e7d3213eb173dcce828/src/rgbw_colorspace_converter/colors/converters.py#L242)

### 3 Main Projects Shaped This Module: HEX, BAAAHS and Pyramid Scheme.... hence.... HEXBASPYR ?

<pre>
 ___  ___    _______       ___    ___  ________     ________     ________     ________    ___    ___  ________       
\ \  \\\  \ \ \   __/|    \ \  \/  / /\ \  \|\ /_  \ \  \|\  \  \ \  \___|_  \ \  \|\  \ \ \  \/  / /\ \  \|\  \     
 \ \   __  \ \ \  \_|/__   \ \    / /  \ \   __  \  \ \   __  \  \ \_____  \  \ \   ____\ \ \    / /  \ \   _  _\    
  \ \  \ \  \ \ \  \_|\ \   /     \/    \ \  \|\  \  \ \  \ \  \  \|____|\  \  \ \  \___|  \/  /  /    \ \  \\  \|   
   \ \__\ \__\ \ \_______\ /  /\   \     \ \_______\  \ \__\ \__\   ____\_\  \  \ \__\   __/  / /       \ \__\\ _\   
    \|__|\|__|  \|_______|/__/ /\ __\     \|_______|   \|__|\|__|  |\_________\  \|__|  |\___/ /         \|__|\|__|  
                          |__|/ \|__|                               \|_________|        \|___|/                      
</pre>
![HBP](https://raw.githubusercontent.com/iamh2o/rgbw_colorspace_converter/main/images/bars5.png)


# Let's Do It: INSTALL

## Requirements

* [Python >= 3.7](https://www.python.org) on ubuntu 16?
* Modern MACs seem to require python >= 3.10.8

### Nice to have requirements....

* Chrome or Safari installed. One of the scripts will record a HTML version of what is displayed on the screen, and when exited, renders the page as a png.  This rendering step is not required to run the script, watch it or get the html copy (and ansi output too!)... but if you don't have chrome installed (or safari as an alternate), the image creation won't work.

## Install Options

### PIP From PyPi

```
pip install rgbw_colorspace_converter ;  # v0.4.1 is available in the releases, but not yet pypy

___ MAC Air M2 requires python >= 3.10.8 ___
Try a few of the three test scripts which use the color library for some ansi escape color art :-)  You will need to ctrl-c to exit, and in some cases may need to run the command "reset".

path_between_2_colors.py. #will work with manually installed v0.4.1

run_color_module_RGB_HSV_HEX_demo.py -z -y -g -u 33  
# for more excitement
  run_color_module_RGB_HSV_HEX_demo.py  -b "___|||))--WWWW________///====\__" -z -y -g -u 33 -f
  
run_spectrum_saturation_cycler.py # will work with manually installed v0.4.1

```

* pip install and run test script::: [Example](https://asciinema.org/a/430968)

* The three scripts in the bin dir will work in most any terminal. You may only have 16 colors, but may have more.  I took it as a challenge to write some debugging and teaching tools that would not require a whole pile of LED gear to get going. you can get started in a very simple way with the command line color_printer, which accepts this packages color objects (among other things).  It even manages to make some reasonably interesting art!

### From Github

* Clone repo
* cd into clone dir
* type ```pip install -e .```
* This should instal the main branch active in git (no promises it's stable!)
* `source environment/env.sh`


#### Quick Start Crash Cource


	
  > from rgbw_colorspace_converter.colors.converters import RGB, HSV, HSL, HSI, Hex
  >
  >  The Color class is the top level class, but the RGB and HSV classes inherit from it and do all of the same work. Its intended to be expanded upon at   > some point, but for now, you can honesly choose any of them.  You can instantiate 'Color(RGB/HSL)' objext only.  Once instantiated, they calculate     > and maintain the state of the 5 other color spaces these objects manage (HSL, HSi, HEX, RGBW, i guess just 4 others, 6 total.


	
# Begin Like So:
<ul>
<pre>
from rgbw_colorspace_converter.colors.converters import RGB, HSV, HSL, HSI, Hex

<p valign="middle">rgb = RGB(255,125,22)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff7d16><img src="https://via.placeholder.com/47x20/ff7d16/000000.png?text=+" valign="bottom" ></img></a></p>

rgb.(press tab in an interactive shell) and you'll see:
</pre>
</ul>

>``````
>
>        rgb...
>               copy()     hsl     hsv_s   rgb     rgb_r    rgbw_b  gbw_w 	      
>               hex        hsv     hsv_t   rgb_b   rgbw_w   rgbw_g         
>               hsi        hsv_h   hsv_v   rgb_g   rgbw     rgbw_r         
>``````

These are the objects and functions available to the Color/HSV and RGB top level objects alike.  There are a handful of important types.

> 1)  Objects, which when called will give you that color schemes encoding for whatever is currently set by RGB/HSV.  
> 1b) Note, the core color space used in this module is actually HSV.  The HSV and RGB mappings are tightly coupled.  If you change the RGB.RED value, the HSV values immediately recalculate (as do the values for all of the second order color space objects.
> 2)  The second order color space objects will generallty let you instantiate an object with their values, but you will get back  Color object which will not accept modifications of the second order object properties (again- to make changes you'll need to modify RGB or HSV values. Then there are third order objects which it is not yet possible to instantiate them directly from their native parameters, but we can calculate their values given any first or second order object- this mostly applies to RGBW-- but the problem is small in our exper4ience, nearly all of the use cases for RGBW is getting a realistic transofrmation to RGBW space from these others. We're here to help!
> 3)  Recap:  First order objects: Color, RGB, HSV. Second order (HSL, HSi, HEX. Third order object, but still loved, RGBW.
> 4)  Sll obect used by name (ie: rgb.hsi ) return a tuple of their values refkectiung the color represented by the RGB and HSV internal values. The same is tru for .hsv, .hsi, .rgbw....
> 5) First order objects have the special features of getters and setters.  HSV objects have hsv_v, hsv_s, hsv_h.  Used w/out assignment they reuturn the single value.  Used with assignment, the valiue is updated, and all of the other objects have their values recalculated immediately.  The same goes for RGB, there is rgb_r, rgb_g, rgb_b.  The setters are the encourated way to update the global color of the color objexts.  No save is required.  The hsv_t property is a special internal use tuple of the HSV representation of the current color. Do not muck around with please.  Lastly, there is a function 'copy'.  If you with to spin off a safe Color object to play with, in say, multithreaded envirionments, use copy to deepcopy the Color object you are using.
> 6) oh!  for colorspaces which typically have values that span 0-360 degrees, those have been normalized to a 0-1 scale for easier programatic use.


#### A micro example of how this can work

<pre>
# Instantiate a color object from RGB (you can instantiate from RGB/HSV/HSL/HSi/Hex, and get translations
# to all the others plus rgbw immediately. Further, the RGB and HSV objects are special in that they can
# be manipulated in real time and all the other conversions happen along with the RGB/HSV changes.  Meaning
# you can write programs that operate in RGB/HSV space and control lighting in RGBW space.  Technically
# you can do the same with the HSL/HSI/Hex objects, but way more clunkly.   

# Something to note... is how counter intuitive many RGBW transforms are once you get away from primary colors.

# To start simple- here a color object representing Red as defined by RGB is initialized-- and the translations to all
# the other spaces immediately available.

from rgbw_colorspace_converter.colors.converters import RGB, HSV

color = RGB(255,0,0)
color.rgb
<p valign="middle">(255, 0, 0)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/ff0000.png" valign="bottom" ></img></a></p>

In [34]: color.hsv
<p valign="middle">(0.0, 1.0, 1.0)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/000000.png?text=+" valign="bottom" ></img></a></p>

color.hsl
<p valign="middle">(0.0, 1.0, 0.5)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/000000.png?text=+" valign="bottom" ></img></a></p>

color.hsi
<p valign="middle">(0.0, 1.0, 0.33333)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/000000.png?text=+" valign="bottom" ></img></a></p>

color.hex
<p valign="middle">'#ff0000'<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/000000.png?text=+" valign="bottom" ></img></a></p>

color.rgbw
<p valign="middle">(254, 0, 0, 0)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ff0000><img src="https://via.placeholder.com/47x20/ff0000/000000.png?text=+" valign="bottom" ></img></a></p>

# We can change the red color object to yellow by adding green by directly changing the <code>rgb_g</code> property
# of the color object (which maps all RGB and HSV changes to all other color spaces in real time.

# We add max green
color.rgb_g = 255

color.rgb
<p valign="middle">rgb(255, 255, 0)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ffff00><img src="https://via.placeholder.com/47x20/ffff00/000000.png?text=+" valign="bottom" ></img></a></p>


color.hsv
<p valign="middle">(0.16666666666666666, 1.0, 1.0)<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ffff00><img src="https://via.placeholder.com/47x20/ffff00/000000.png?text=+" valign="bottom" ></img></a></p>
In [17]: color.rgbw
Out[17]: (254, 254, 0, 0)

color.hex
<p valign="middle">'ffff00'<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=ffff00><img src="https://via.placeholder.com/47x20/ffff00/000000.png?text=+" valign="bottom" ></a></img></p>

# and the rest were all translated to represent yellow as well

</pre>

##### A worked use case

* Lets say you wanted to write s/w to control something that emits light- probably using colors. This could be LEDs or other lighting hardware, or even sofware or APIs/services.  Each have their own interfaces with what color codes they accept.  LEDs are primarily RGB or RGBW, but working directly in RGB is a pain. So this module can let you work in the space you grok, and spit out the translations to the thing you are controlling in the protocol it expects (I guess we support DMX too if you want to ask me about that.

* I wrote two simple scripts that achieve all of the above.  I instantiate objects using RGB color codes, I work with the objects in HSV space to move through the color space in various ways (and to show how straight forward it is.  And in a supremely awesome way :-)  I found a way to use a terminal tool called colr to act as my display I'm controlling...... and it only accepted Hex codes.  So I was using 3 spaces actively just for one simple project.  The colored output I produce with these tools also emits the color codes for all of the color spaces represented with each line of color so you can take a peek at how all the different ones represent different things.  RGB and RGBW get really strange when complex mixtures of colors happen.
* So, generally RGB / RGBW and Hex are not the most pleasant to work directly in.... this is a good read if you're curious why [RGB/RGBW/Hex are not the most intuitive ways to think about color](https://www.maketecheasier.com/difference-between-hex-rgb-hsl/). To perform simple organic operations, like fading through saturations of a color, or cycling smoothly through various colors, the manipulation of HSV/HSL/HSI are far more intuitive (and far more amenable to programatic manipulation) than the others.  So, I'll write a toy script (which you can run here using a very low tech display), which I think will demonstrate how this package was intended to be used. There are functional scripts you can run (if you install!)  [here ---](https://github.com/iamh2o/rgbw_colorspace_converter/blob/main/bin/run_spectrum_saturation_cycler.py)  and another named `path_between_2_colors.py`.



![go](https://raw.githubusercontent.com/iamh2o/rgbw_colorspace_converter/main/images/bar20.png)

## Contribute

<ul>
Please do ask questions, discuss new feature requests, file bugs, etc.  You are empowered to add new features, but try to talk it through with the repo admins first-  though if youre really burning to code, we can talk with the code in front of us.  PRs are the way to propose changes.  No commits to main are allowed.  Actions/Tests must all pass as well as review by 2 folks equipped to eval the proposed changes.
Development (less stable)
</ul>

### Install Dev Env

```
cd environment
./setup.sh #  Read the help text.  To proceed with install:
./setup.sh HBP ~/conda # or wherever your conda is installed or you want it installed
source env.sh # which you need to do anytime you wish to run things.
# To Test
./bin/path_between_2_colors.py
./bin/run_spectrum_saturation_cycler.py
./bin/run_color_module_RGB_HSV_HEX_demo.py  -b "___|||))--WWWW________///====\__" -z -y -g -u 33 -f
```
* This will install a conda environment you can source with conda activate HBP. If you don't have conda, it is installed where you specify.  Mamba is also installed (read about it. tldr: lightning fast conda, will change your life). The codebase adheres to black style and mostly to flake8.

* During the running of setup above, pre-commit checks will be installed to enforce black and flake 8 compliance before any pushes are permitted. Full disclosure.  Black will auto-fix problems when it fails a commit, so you just run again and all is good.  RARELY, you'll have to run 'black' directly on the file. Flake8, you need to go manually address the issues is spits out.  If there are a ton, chip away at a few, then you can use the --skip-verify commit flag- but don't abuse it please.

* Upon commit, flake 8 and black linter checks are run, as well as the pyunit tests for each commit and pull request.  The status of each can be seen in the actions tab and reflected in some of the badges.

## A Fun Thing.

* I've worked up a lowtech way to demonstrating cycling through various color spaces programmatically using the terminal.  If you have pip installed or run setup.sh, this should work.  Try running (in dev)```conda activate HBP; python bin/run_color_module_RGB_HSV_HEX_demo.py``` (after pip)```run_color_module_RGB_HSV_HEX_demo.py```.  You get a taste for how the spaces cycle differently and what the encoding for each looks like.

* It the main bin script has a lot of parametyers now.   
** You can easily genrate things like with the test bin files: <a href="https://asciinema.org/a/430968" target="_blank"><img src="https://asciinema.org/a/430968.svg" height=150 wigth=220/></a>

## Quick Note on Our Hardware Setup

* We used OLA + DMXkings to run LEDs via DMX for many BIG projects controlling thousands of LEDS. And this library controlling and mapping colors.

* Other projects used processing as intermediate, among other things.

## More Examples

### A Bit More
<ul>
Not only does the package allow translation of one color space to another, but it also allows modifications of the color object in real time that re-calculates all of the other color space values at the same time.  This is *EXCEEDINGLY* helpful if you wish to do things like slice through HSV space, and only change the saturation, or the hue. This is simply decrementing the H or S value incrementally, but in RGB space, is a complex juggling of changing all 3 RGB values in non intuitive ways.  The same applies for transversals of HSI or HSL space to RGB.  We often found ourselves writing our shows in HSV/HSL and translating to RGBW for the LED hardware to display b/c the show were more natural to design in non-RGB.
</ul>

<pre>
see examples in the ./bin and ./tests directories.

# Moving through the HSV color wheel is simply cycling 0->1.0->0->and so on
# Moving through the color wheel in RGB, is a lot more of a pain in the add.  Here is an example.



# Lets start with a complicated color, crimson: http://www.workwithcolor.com/color-converter-01.htm?cp=D92008
color = RGB(217,32,8) <p valign="middle">rgb 217,32,8<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=D92008><img src="https://via.placeholder.com/47x20/D92008/000000.png?text=+" valign="bottom" ></img></a></p>
color.rgbw
(217,32,8)
color.rgbw
(207, 27, 0, 6)
color.hsv
(0.01913875598086125, 0.9631336405529954, 0.8509803921568627)


# As we swing through the color wheel, we change just the h value, note the changes in RGB/W values are not easily predictable considering it's a pretty simple operation.                                                                                                                    



# Gold:  <p valign="middle">rgb 217,208,7<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=D9C709><img src="https://via.placeholder.com/47x20/D9C709/000000.png?text=+" valign="bottom" ></img></a></p>
# Moving the HSV colorwheel value 'h' only yields these changes
color.hsv_h = 0.16                                                                              
(0.16, 0.9631336405529954, 0.8509803921568627)                                                  
color.rgb                                                                                       
(217, 208, 7)                                                      
color.rgbw                                                                                      
(210, 200, 0, 7)    




# LawnGreen: <p valign="middle">rgb 112,217,7<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=70D907><img src="https://via.placeholder.com/47x20/70D907/000000.png?text=+" valign="bottom" ></img></a></p>
# Moving the HSV colorwheel value 'h' only yields these changes                                 
color.hsv_h = 0.25
(0.25, 0.9631336405529954, 0.8509803921568627)                                                  
color.rgb
(112, 217, 7)
color.rgbw
(104, 209, 0, 7)



# DeepTurquoise:<p valign="middle">rgb7,154,217<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=079AD9 ><img src="https://via.placeholder.com/47x20/709AD9/000000.png?text=+" valign="bottom" ></img></a></p>
# Moving the HSV colorwheel value 'h' only yields these changes    
color.hsv_h = 0.55
color.hsv
(0.55, 0.9631336405529954, 0.8509803921568627)
color.rgb
(7, 154, 217)
color.rgbw
(0, 145, 211, 6)



# DarkViolet: <p valign="middle">rgb 87,7,217<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=5707D9 ><img src="https://via.placeholder.com/47x20/5707D9/000000.png?text=+" valign="bottom" ></img></a></p>
# Moving the HSV colorwheel value 'h' only yields these changes    
color.hsv_h = 0.73
color.hsv
(0.73, 0.9631336405529954, 0.8509803921568627)
color.rgb
(87, 7, 217)
color.rgbw
(81, 0, 208, 7)



# And if we set color.hsv_h = 0.0191, we'd be back to <p valign="middle">crimson<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=D92008><img src="https://via.placeholder.com/47x20/D92008/000000.png?text=+" valign="bottom" ></img></a></p>.



#### This final example demonstrates the counter-intuitive RGB<->RGBW settings when not dealing with fully saturated colors.

from rgbw_colorspace_converter.colors.converters import RGB

color = RGB(20,200,123) # dark orange
print(color.hsv, color.hex)
-> (0.42870370370370364, 0.8999999999999999, 0.7843137254901961), '#14c87a'

ctr = 0
while ctr < 9:
    color.hsv_s -= .1
    color.hsv_h += 0.02
     print(color.hsv, color.rgb, color.rgbw, color.hex)
     ctr += 1

# Outputs
HSV(0.4487037, 0.8, 0.7843137254901961) RGB(39, 200, 150 ) RGBW(0, 162, 109, 39) HEX 27c896
<p valign="middle">--| Light Sea Green<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=27c896><img src="https://via.placeholder.com/47x20/27c896/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.4687037, 0.7, 0.7843137254901961) RGB(60, 200, 173 ) RGBW(0, 141, 111, 59) HEX 3cc8ad
<p valign="middle">--| Medium Aquamarine<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=3cc8ad><img src="https://via.placeholder.com/47x20/3cc8ad/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.4887037, 0.6, 0.7843137254901961) RGB(80, 200, 191 ) RGBW(0, 120, 110, 80) HEX 50c8bf
<p valign="middle">--| Medium Turquoise<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=50c8bf><img src="https://via.placeholder.com/47x20/50c8bf/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.5087037, 0.5, 0.7843137254901961) RGB(100, 194, 200) RGBW(0, 93, 100, 99 ) HEX 64c2c8
<p valign="middle">--| Light Aquamarine<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=64c2c8><img src="https://via.placeholder.com/47x20/64c2c8/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.5287037, 0.4, 0.7843137254901961) RGB(120, 186, 200) RGBW(0, 65, 80, 120 ) HEX 78bac8
<p valign="middle">--| Medium Aquamarine<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=78bac8><img src="https://via.placeholder.com/47x20/78bac8/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.5487037, 0.3, 0.7843137254901961) RGB(139, 182, 200) RGBW(0, 42, 61, 138 ) HEX 8bb6c8
<p valign="middle">--| skyblue<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=8bb6c8><img src="https://via.placeholder.com/47x20/8bb6c8/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.5687037, 0.2, 0.7843137254901961) RGB(160, 183, 200) RGBW(0, 22, 40, 160 ) HEX a0b7c8
<p valign="middle">--| light<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=a0b7c8><img src="https://via.placeholder.com/47x20/a0b7c8/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.5887037, 0.1, 0.7843137254901961) RGB(180, 189, 200) RGBW(0, 9, 19, 180  ) HEX b4bdc8
<p valign="middle">--| silver<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=b4bdc8><img src="https://via.placeholder.com/47x20/b4bdc8/000000.png?text=+" valign="bottom" ></img></a></p>

HSV(0.6087037, 0.0, 0.7843137254901961) RGB(200, 200, 200) RGBW(0, 0, 0, 199   ) HEX c8c8c8
<p valign="middle">--| dark silver<a href=http://www.workwithcolor.com/color-converter-01.htm?cp=c8c8c8><img src="https://via.placeholder.com/47x20/c8c8c8/000000.png?text=+" valign="bottom" ></img></a></p>

</pre>


![qq](https://raw.githubusercontent.com/iamh2o/rgbw_colorspace_converter/main/images/bar33.png)

# Tests

## Command Line
* Simple at the moment, but you may run:
    * ```pytest --exitfirst --verbose --failed-first --cov=. --cov-report html```

## Github Actions
* Pytests, Flake8 and Python Black are all tested with github commit actions.

## Fun & Kind Of Weird Tests

```python ./bin/run_color_module_RGB_HSV_HEX_demo.py``` and ```./bin/run_spectrum_saturation_cycler.py```

* Needs to run on a unix-like terminal. OSX, seems fine. Windows.... I'm not sure.  

# In The Works

    * OLA Integration To Allow Testing LED Strips
    * Example mini project to see for yourself the difference in vividness and saturation of RGBW vs RGB LEDs. You'll need hardware for this fwiw.


# Detailed Docs

<pre>
Color

Color class that allows you to ** initialize ** a color in any of HSL, HSV, RGB, Hex and HSI color spaces.  Once initialized, with one of these specific types, you get a Color object back (or possibly a subclass of the Color object- RGB or HSV- all the same ).  This object will automatically report the color space values for all color spaces based on what you entered.  Notably, it will also translate to RGBW!        


Further, from the returned object, you may modify it in 2 ways-  via the r/g/b properties of the RGB Color object, or via the h/s/v properties of the HSV color object. Any changes in any of the r/g/b or h/s/v properties (even if mixed and matched) will automatically re-calculate the correct values for the other color space representations, which can then be accessed.  You can not modify the other color space object properties and get the same effect (yet).                                                                                                                           
The color representation is maintained in HSV internally and translated to RGB and RGBW and all the others.
Use whichever is more convenient at the time - RGB for familiarity, HSV to fade colors easily.

The main goal of this package is to translate various color spaces into RGBW for use in RGBW LED or DMX/RGB accepting hardware.  There is a strange dearth of translators from ANY color space to RGBW.                                                                                

RGB values range from 0 to 255
HSV values range from 0.0 to 1.0 *Note the H value has been normalized to range between 0-1 in instead of 0-360 to allow
for easier cycling of values.
HSL/HSI values range from 0-360 for H, 0-1 for S/[L|I]
Hex is hex...


# INITIALIZING COLOR OBJECTS -- it is not advised to init Color directly. These below all basically return a valid Color obj # RGBW can not be initialized directly-  it is calculate from the initialized, or modified values of the color objs below    from rgbw_colorspace_converter.colors.converters import RGB, HSV, HSL, HSI, Hex   


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

--->>>    # IMPORTANT -- This recalculation after instantiation *only* is allowed for hsv and rgb types.  The HSL/HSV/HSI/RGBW values are all calculated upon instantiation of the Color object **AND** the values for each are updated in real time as the hsv(h|s|v) and rgb(r|g|b) values are modified in the Color object.  But, you can not modify the individual elements of HSL/HSI/RGBW/HEX objects directly after instantiating each.  Put another way. If you create a HSI object, to get a new HSI color value you need to modify r/g/b or h/s/v (or create a new HSI object).

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


from rgbw_colorspace_converter import RGB
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
<p valign="middle"> <img src="https://via.placeholder.com/43x20/ff0058/000000?text=+" valign="bottom" > <code>#ff0058</code> ... and some more stuff</p>
RGBW

To get the (r,g,b,w) tuples back from a Color object, simply call Color.rgbw and you will return the (r,g,b,w) tuple.



                -----------------------------------|          |-----------------------------------
                                                     ╦ ╦╔╗ ╔═╗                                  
                                                     ╠═╣╠╩╗╠═╝                                  
                                                     ╩ ╩╚═╝╩

</pre>


<b>run_color_module_RGB_HSV_HEX_demo.py</b> generates scrolling patterns by cycling through the various color spaces, this is a screenshot:


![HBP](https://raw.githubusercontent.com/iamh2o/rgbw_colorspace_converter/main/images/Screen%20Shot%202021-06-17%20at%205.12.35%20PM.png)



## Authors

> GrgB wrote the vast majority of the core. JM translated Brian Nettlers theoretical work into code to allow the translation from RGB/HSV/HSI to RGBW. JC added a lot of robustness and and in latter instances (which you can find in the pyramid triangles repo) filled  in some algorithmic gaps, which I have been unable to test yet, so have not included them yet. This nugget of code has been present in projects that now span > 10 years. With multiple artists and show designers also contributing to the s/w (ie: TL, JH, SD, ZB, MF, LN).  This library is a small component of a much more elaborate framework to control custom fabricated LED installations.  Most recentlyly for Pyramid Scheme v-3 [PyramdTriangles](https://github.com/pyramidscheme/pyramidtriangles), which was a fork of the v-1 code [pyramid triangles codebase v1.0](https://github.com/iamh2o/pyramidtriangles), Pyramid Scheme followed several years of running the BAAAHS lighting installation (codebase lost to bitbucket purgatory). And the BAAAHS installation was the first gigantic project of the then baby faced HEX Collective (whom developed the core of this code speficially for a comissioned piece, aptlt dubbed [The Hex's](l;ink)... this repo also sadly lost to time and space.  This color library being an original component, and largely untouched until the need to support RGBW LEDs (and wow, rgbw LEDS are really stunning).

### Roarrrr

It would be remiss of us not to  thank Steve Dudek for his Buffalo soothsaying and accurate measuring of 3 inch increments.

# Credits // References

- [Shield.io](https://shields.io)
- [Placeholder](https://placeholder.com/) for allowing there to be color images in this readme!
- [Colorblind Aware Design](https://davidmathlogic.com/colorblind/)

