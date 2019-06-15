#
# RandomColors
#
# Show populates every panel with a different random colors
# A color has one full (255) channel, one empty (0) channel,
# and one partial (0-255) channel. This yields saturated colors.
#
# As the show progresses, the partial channel changes
#
# Touch OSC changes the full component of the colors
# Change change color to have Touch OSC change the variable component instead
#

import sheep
from random import randint
from color import RGB

class RandomColors(object):
	def __init__(self, sheep_sides):
		self.name = "Random Colors"
		self.sheep = sheep_sides.both

		self.speed = 0.01
		
		self.panel_map = {}	# Dictionary of panels: value is Panel object

		for cell in self.sheep.all_cells():
			newpanel = Panel()
			self.panel_map[cell] = newpanel

	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)

		if name == 'colorR':
			channel = 0
		elif name == 'colorG':
			channel = 1
		elif name == 'colorB':
			channel = 2

		for cell, panel in self.panel_map.iteritems():
			panel.OSC_update_panel(channel, rgb255)

	def next_frame(self):
		while True:
			for cell, panel in self.panel_map.iteritems():
				self.sheep.set_cell(cell, panel.get_color())
				panel.update_panel()
			
			yield self.speed

class Panel(object):
	def __init__(self):
		self.color_val = [0,0,0]	# r,g,b in list form
		
		full, var, empty = self.pickChannels()
		
		self.color_val[full] = 255
		self.color_val[var] = randint(0,255)
		self.color_val[empty]= 0
		
		self.full_channel = full
		self.moving_channel = var
		
		# Generate velocities of -2,-1,1, or 2
		self.velocity = randint(1,2)
		if randint(0,1) == 1: self.velocity *= -1

	def get_color(self):
		return RGB(self.color_val[0], self.color_val[1], self.color_val[2])
		
	def update_panel(self):
		value = self.color_val[self.moving_channel]
		value += self.velocity
		
		if value > 255:
			value = 255 - (value - 255)
			self.velocity *= -1
		elif value < 0:
			value = 0 - value
			self.velocity *= -1

		self.color_val[self.moving_channel] = value

	def OSC_update_panel(self, channel, value):
		if channel == self.full_channel:
			self.color_val[channel] = value

		# May look better to affect the moving channel instead
		# Try this code replacement:
		#
		#if channel == self.moving_channel:
		#	self.color_val[channel] = value

	def pickChannels(self):
		answers = ((0,1,2), (1,0,2), (0,2,1), (2,0,1), (1,2,0), (2,1,0))
		return answers[randint(0,5)]