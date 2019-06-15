#
# randomOneColor
#
# Show populates every panel with different, random 5-100% intensities
# As the show progresses, each panel gets brighter or darker
# 
# Starting color is random
#
# Main color can get controlled by Touch OSC
# If OSC is not used, the sheep slowly changes color
# 

import sheep
import time
from random import randint
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

class RandomOneColor(object):
	def __init__(self, sheep_sides):
		self.name = "Random One Color"
		self.sheep = sheep_sides.both

		self.speed = 0.1
		self.last_osc = time.time()
		
		self.OSC = False	# Is Touch OSC working?
		self.noOSCcolor = randint(0,1536)	# Default color if no Touch OSC
		self.OSCcolor = Wheel(self.noOSCcolor)

		self.panel_map = {}	# Dictionary of panels: value is Panel object

		for cell in self.sheep.all_cells():
			newpanel = Panel()
			self.panel_map[cell] = newpanel

	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.OSCcolor.r = rgb255
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorG':
			self.OSCcolor.g = rgb255
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorB':
			self.OSCcolor.b = rgb255
			self.last_osc = time.time()
			self.OSC = True

	def next_frame(self):
		while True:
			for cell, panel in self.panel_map.iteritems():
				if self.OSC:	# Which color to use?
					adj_color = self.OSCcolor.copy()
				else:
					adj_color = Wheel(self.noOSCcolor)
				
				adj_color.v = panel.intensity / 100.0
				self.sheep.set_cell(cell, adj_color)

				panel.update_panel()
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				self.noOSCcolor += 1
				if self.noOSCcolor > 1536:
					self.noOSCcolor -= 1536
			
			yield self.speed


class Panel(object):
	def __init__(self):
		self.intensity = randint(5,100)
		
		# Generate velocities of -2,-1,1, or 2
		self.velocity = randint(1,2)
		if randint(0,1) == 1: self.velocity *= -1

	def update_panel(self):
		self.intensity += self.velocity
		
		if self.intensity > 100:
			self.intensity = 100
			self.velocity *= -1
		elif self.intensity < 5:
			self.intensity = 5
			self.velocity *= -1

