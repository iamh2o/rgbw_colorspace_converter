#
# WhiteRandomOneColor
#
# Show populates every panel with different, random 5-100% intensities
# As the show progresses, each panel gets brighter or darker
# 
# Starting color is always white
#
# 

import sheep
import time
from random import randint
from color import RGB

class WhiteRandomOneColor(object):
	def __init__(self, sheep_sides):
		self.name = "White Random One Color"
		self.sheep = sheep_sides.both

		self.speed = 0.1

		self.color = RGB(255,255,255)	# White
		
		self.panel_map = {}	# Dictionary of panels: value is Panel object

		for cell in self.sheep.all_cells():
			newpanel = Panel()
			self.panel_map[cell] = newpanel

	def next_frame(self):
		while True:
			for cell, panel in self.panel_map.iteritems():

				adj_color = self.color.copy()
				adj_color.v = panel.intensity / 100.0
				self.sheep.set_cell(cell, adj_color)

				panel.update_panel()
			
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