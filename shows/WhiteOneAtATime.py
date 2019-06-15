#
# White One at a Time
#
# Show lights up one panel at a time with white
# After all panels are lit, sequence starts again with dark gray
#
# No OSC control
# 

import sheep
from random import randint, shuffle
from color import RGB


class WhiteOneAtATime(object):
	def __init__(self, sheep_sides):
		self.name = "White One At A Time"
		self.sheep = sheep_sides.both

		self.speed = 0.1
		self.white = RGB(255,255,255)
		self.black = RGB(0,0,0)
		
		self.color = self.white

		# Blank the sheep to a random background color
		self.sheep.set_all_cells(self.black)

		# Shuffle the panels
		self.shuf_panels = self.sheep.all_cells()
		shuffle(self.shuf_panels)

	def next_frame(self):
		while True:
			for i in range(len(self.shuf_panels)):
				for j in range(i+1):					
					dim = 1.0 - ( (i-j) * (1.0 / len(self.shuf_panels)) )
					adj_color = self.color.copy()
					adj_color.v = dim
					self.sheep.set_cell(self.shuf_panels[j], adj_color)
				yield self.speed
			
			if self.color == self.white:
				self.color = self.black
			else:
				self.color = self.white