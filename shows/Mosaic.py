#
# Mosaic
#
# Show fills the sheep with two different colors
# 
# Both colors can be chosen by the Tousch OSC
# 

import sheep
import time
from random import randint, choice
from color import RGB

# Converts a 0-1536 color into rgb on a wheel by keeping one of the rgb channels off

MaxColor = 1536

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

class Mosaic(object):
	def __init__(self, sheep_sides):
		self.name = "Mosaic"
		self.sheep = sheep_sides.both

		self.speed = 1
		self.last_osc = time.time()
		
		self.OSC = False	# Is Touch OSC working?
		self.color1 = randint(0, MaxColor)	# Default color if no Touch OSC
		self.color2 = randint(0, MaxColor)	# Default color if no Touch OSC
		
		self.key_cell = choice(self.sheep.all_cells())
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.color1 = rgb255 * 6
		elif name == 'colorG':
			self.color2 = rgb255 * 6

	def next_frame(self):
		while True:
			
			self.pixel1 = self.get_vertices(self.key_cell)
				
			# Set background to color2
			
			self.sheep.set_all_cells(Wheel(self.color2))
			
			# Set all the mosaic cells to color1
			
			self.sheep.set_cells(self.pixel1, Wheel(self.color1))
			
			# Change vertices generator
			
			self.key_cell = choice(self.sheep.all_cells())
				
			self.color1 += 2
			if self.color1 > MaxColor:
				self.color1 -= MaxColor
			self.color2 -= 20
			if self.color2 < 0:
				self.color2 += MaxColor
				
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

