#
# White
#
# Shortest show ever: turn all panels white

import sheep
from color import RGB
            
class White(object):
	def __init__(self, sheep_sides):
		self.name = "White"
		self.sheep = sheep_sides.both
		self.speed = 1
		
	def next_frame(self):	
		while (True):
			
			self.sheep.set_all_cells(RGB(255,255,255))
				
			yield self.speed