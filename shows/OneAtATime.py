#
# One at a Time
#
# Show lights up one panel at a time with a given color
# After all panels are lit, sequence starts again with a new color
#
# Main color can get controlled by Touch OSC
# 

import sheep
from random import randint, shuffle
from color import RGB

# Converts a 0-1536 color into rgb on a wheel by keeping one of the rgb channels off

def Wheel(color):
	color = color % 1536  # just in case color is out of bounds
	channel = color / 255
	value = color % 255
	
	if channel == 0:
		r = 255
		g = value
		b = 0
	elif channel == 1:
		r = 255 - value
		g = 255
		b = 0
	elif channel == 2:
		r = 0
		g = 255
		b = value
	elif channel == 3:
		r = 0
		g = 255 - value
		b = 255
	elif channel == 4:
		r = value
		g = 0
		b = 255
	else:
		r = 255
		g = 0
		b = 255 - value
	
	return RGB(r,g,b)
	
class OneAtATime(object):
	def __init__(self, sheep_sides):
		self.name = "One At A Time"
		self.sheep = sheep_sides.both

		self.speed = 0.1
		self.color = Wheel(randint(0,1536))

		# Blank the sheep to a random background color
		self.sheep.set_all_cells(Wheel(randint(0,1536)))

		# Shuffle the panels
		self.shuf_panels = self.sheep.all_cells()
		shuffle(self.shuf_panels)

	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.color.r = rgb255
		elif name == 'colorG':
			self.color.g = rgb255
		elif name == 'colorB':
			self.color.b = rgb255

	def next_frame(self):
		while True:
			for i in range(len(self.shuf_panels)):
				for j in range(i+1):					
					dim = 1.0 - ( (i-j) * (1.0 / len(self.shuf_panels)) )
					adj_color = self.color.copy()
					adj_color.v = dim
					self.sheep.set_cell(self.shuf_panels[j], adj_color)
				yield self.speed
			self.color = Wheel(randint(0,1536))