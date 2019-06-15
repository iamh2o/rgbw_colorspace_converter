#
# White Mosaic
#
# Show fills the sheep with two greys
# 
# No Touch OSC
# 

import sheep
import time
from random import randint, choice
from color import RGB

class WhiteMosaic(object):
	def __init__(self, sheep_sides):
		self.name = "White Mosaic"
		self.sheep = sheep_sides.both

		self.speed = 0.01
		
		self.color = 0
		self.dir = 10	# Either 1 or -1
		
		self.key_cell = choice(self.sheep.all_cells())
		self.pixel1 = self.get_vertices(self.key_cell)
		
	def next_frame(self):
		while True:
				
			# Set background to inverse color
			
			self.sheep.set_all_cells( RGB(255,255,255))
			#self.sheep.set_all_cells( RGB(255 - self.color, 255 - self.color,	255 - self.color))
										  
			# Set all the mosaic cells to color
			
			self.sheep.set_cells(self.pixel1, RGB(self.color, self.color, self.color))
			
			# Change vertices generator
			
			if randint(0,100) == 1:
				self.key_cell = choice(self.sheep.all_cells())
				self.pixel1 = self.get_vertices(self.key_cell)
			
			# Change grey intensity
			self.color += self.dir
			if self.color < 0:
				self.color *= -1
				self.dir *= -1
			if self.color > 255:
				self.color = 255 - (self.color - 255)
				self.dir *= -1
				
			yield self.speed
	
	def get_vertices(self, cell):
		cell_list = []
		cell_list.append(cell)
		
		for c in cell_list:
			cell_list = self.get_near_vertices(c, cell_list)
		
		return cell_list
	
	def get_near_vertices(self, cell, cell_list):
		for c in sheep.vertex_neighbors(cell):
			if c not in cell_list and not self.share_edge(c, cell_list):
				cell_list.append(c)
		return (cell_list)
		
	# Returns true if cell is in cells or shares an edge with any cells
	def share_edge(self, cell, cells):
		if cell in cells:
			return True
		for c in cells:
			if cell in sheep.edge_neighbors(c):
				return True
		return False

