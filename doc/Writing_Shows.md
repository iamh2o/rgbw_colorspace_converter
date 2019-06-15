# Getting Started

First, make sure you have a working copy of software and simulator before you proceed.  Some rudimentary Python skills are helpful, but not required.  It's easy!

'Shows' are animations that run on Baaahs using the new panel lighting system.  A show may be as short as a few seconds or something that can run for an unlimited amount of time.  Generally, shows are cycled every few minutes over the course of an event to keep things from getting boring.  All shows should be able to run by themselves, but they can accept input to be tuned to the current mood - brighter, faster, different colors are typical things to be tweaked.

*Shows do not (yet!) control the sharpies, only the panel lights.*

# Getting to know the Baaahs

For this year, each panel on the sheep has been individually lit and can display it's own color.  If you've worked on fabricating or installing panels, you're probably already familiar with the numbering scheme.  If you don't know them all by heart, here's a diagram:

[Sheep Panels](https://dl.dropboxusercontent.com/u/387127/SheepSchematic.jpeg)

These are the same panel numbers you're going to use to use when writing a show.

You also have the option of mirroring a show on both sides of the sheep, or treating the two sides individually.  (We're not positive that a show spanning the entire sheep will be interesting since you can only see one side at a time, but it's an option!)  The side of the bus with the DJ booth is referred to as the "party" side, and the side with the generators is the "business" side.

Ok, enough talk!

# Example show

There is an example show in this directory, 'example.py'  Copy it to the 'shows' directory and open it in your favorite editor.

Hopefully, most of the file is self-explanatory.  Each show is defined in it's own class, and there are two main methods that need to be defined on each class:  **next_frame** and **set_param**.  

**next_frame** is the core of the show - this method is called repeatedly to run the animation.  Each call to the method generates the next frame of the show, and then pauses for a predefined amount of time before being called again.  Shows indicate how long they would like to pause by using the **yield** keyword - please do not put an actual pause in your show or it will cause problems!

**set_param** is called to set values from OSC or other external programs.  This method will be called between calls to **next_frame**, so most shows should just remember the values being set and then have **next_frame** take it into account the next time it is called.

There are two main external objects your show will interact with: the **sheep_sides** object (passed in to the show constructor), and the **sheep** module (imported at the top of the example show).

The **sheep_sides** object has three different attributes representing the two sides of the sheep and a "mirrored" mode.  Your show calls any of these objects to set the color of a cell.  The main methods are:

* set_cell(cell_id, color) - Sets a single cell to a color
* set_cells([cell_ids], color) - Sets a list of colors to a single color
* set_all_cells(color) - Sets all cells to a single color
* clear() - Turn off all cells

The color objects are created by calling either the RGB() or HSV() function from the 'color' module.  See the **Color** section below for more details.  An individual panel may be turned off by setting it's color to black - RGB(0,0,0) or HSV(0,0,0).  

*(Note: Panels turned off in the simulator will display as a light grey, not black - somewhat approximating how things will look in real life.  Plus, this way you can still see them against the background
otherwise they vanish against the black background of the simulator)*

The **sheep** module should mainly be used for it's description of the physical geometry of the sheep.  It defines a list of panels in various groupings and functions to determine the which panels touch each other.  The existing groupings are:

* ALL - All panels, mainly useful if you want to choose a panel randomly
* LOW - A horizontal ring of panels closest to the ground 
* MEDIUM - The panels in between the LOW and HIGH rings
* HIGH - A horizontal ring of panels at the top of the sheep
* VSTRIPES - A list of lists defining vertical stripes

And there are two functions that you can call:

* edge_neighbors(panel_id) - Gives the list panel ids that share an edge with a given panel.
* vertex_neighbors(panel_id) - Returns a list of panel ids that share only a vertex with a given panel.

These may be useful depending on what kind of effects you are after, but just use these as suggestions - you are free to create your own groupings in your own show.

Everything is defined in the file sheep.py, so consult that file if you have further questions!

# Color

Color can be specified in either RGB or HSV, whichever you prefer, and are transparently converted as needed between the two.  RGB is probably most familiar color scheme used in computer graphics, but some tasks are simplifed by using HSV, such as fading to white or black or randomly selecting a "bright" color.  If you're not familiar with HSV, [Wikipedia has an explanation and some helpful charts.](http://en.wikipedia.org/wiki/HSL_and_HSV)

The functions 'RGB' and 'HSV' from the color module should be all you need to create the colors needed for your masterpiece.

RGB colors are represented as three integer values ranging from 0-255, representing Red, Green and Blue respectively.  HSV are represented as three floating point values ranging from 0.0 to 1.0 and represent Hue, Saturation and Value (or brightness).

*(Some systems using HSV specify Hue as an integer between 0 and 360, so if you're accustomed to that you should just divide your hue by 360, keeping in mind Python's sometimes surprising division rules)*

In RGB, black is specified as (0,0,0) and white is (255,255,255)

In HSV, black is specified as (*?*,*?*,0) and white is (*?*,0,1)

Regardless of whether you specify a color using RGB or HSV the color object will have both 'r', 'g', 'b' and 'h', 's', 'v' attributes that can be read or adjusted to change the color.

For example, to create a pure Red and fade it to black over 10 steps you can specify the color using RGB but fade to black using the 'v' attribute:

	color = RGB(255,0,0)
	while color.v > 0:
		print color.rgb
		color.v -= 0.1
		
By adjusting the 's' attribute in the same way, you could desaturate the color until it became white.
	
Be careful of making changes to a color object that's used elsewhere in your sketch - there may be unexpected results unless you call copy() on the color and modify the copy.

# Basic Animations

You can call as many set_cell(s) methods as you want during each frame of the animation - they are buffered up and sent only once at the end of the frame.

Each next_frame() function can yield from multiple places if you want to have different parts of an animation that run at different speeds.  For example, this fades a pixel over one second, waits two seconds and then starts again:

	while True:
		color = RGB(255,0,0)
		while color.v > 0:
			cells.set_cell(target, color)
			color.v -= 0.1
			yield 0.1
		
		yield 2.0

# OSC / External Input

TODO
