#
# Firefly
#
# Show flashes a Firefly
# 
# Blinky, yes, but may be good to bring the flock back into the sheep
# 

import sheep
from random import randint, choice
from color import RGB, HSV            

# Brightens (+255) or Darkens (-255) a color. Range is -255 to 255
def fade_color(color, fade_value):
	# Check limits
	if fade_value < -255: fade_value = -255
	if fade_value > 255: fade_value = 255
			   
	return RGB(bump(color.r, fade_value),
			   bump(color.g, fade_value),
			   bump(color.b, fade_value))
					
# value + bump_amt with 0 <= answer < 256				
def bump(value, bump_amt):
	new_value = value + bump_amt
	if new_value > 255: new_value = 255
	if new_value < 0: new_value = 0
	return new_value

class Firefly(object):
	def __init__(self, sheep_sides):
		self.name = "Firefly"
		self.sheep = sheep_sides.both		
		self.yellow = RGB(255, 250, 0)
		self.black = RGB(0, 0, 0)
		self.contrast = 200
		self.col = 0				
		self.dir = 1
		self.speed = 0.02
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.constrast = rgb255
					
	def next_frame(self):	
		while (True):

			if self.dir == -1:	# Heading back - blackout
				self.sheep.set_cells(sheep.VSTRIPES[self.col], self.black)
			
			else:
				height = len(sheep.VSTRIPES[self.col])
			
				for j in range (height):	

					# Calculate row contrast level

					con_level = (self.contrast * 2) - 255	# -255 to 255 value
					if con_level > 0:
						con_cell = con_level * (height - j - 1) / (height - 1)
					else:
						con_cell = con_level * j / (height - 1)
				
					# Adjust yellow
					adj_color = fade_color(self.yellow, con_cell)
				
					self.sheep.set_cell(sheep.VSTRIPES[self.col][j], adj_color)				
						
			self.col += self.dir
			
			if self.col < 0:
				self.col = 0
				self.dir = 1				
				yield self.speed * 40 * randint(1,10)
			
			if self.col >= len(sheep.VSTRIPES):
				self.col = len(sheep.VSTRIPES) -1
				self.dir = -1
				yield self.speed * 40
						
			yield self.speed