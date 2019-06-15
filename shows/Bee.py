#
# Bee
#
# Show draws alternating yellow and black stripes
# 
# Very little to control by OSC
# If you don't like bees, this is not the show for you
# 

import sheep
import time
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

class Bee(object):
	def __init__(self, sheep_sides):
		self.name = "Bee"
		self.sheep = sheep_sides.both
		
		self.last_osc = time.time()
		self.OSC = False	# Is Touch OSC working?

		self.stripe1 = RGB(255, 240, 0)	# Yellow
		self.stripe2 = RGB(0, 0, 0)	# Black
		
		self.contrast = 150	# 0-255 value adjusted by r-channel of Touch OSC
		
		self.speed = 0.5
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.contrast = rgb255
			self.last_osc = time.time()
			self.OSC = True
					
	def next_frame(self):	
		while (True):

			for i in range(len(sheep.VSTRIPES)):
				for j in range(len(sheep.VSTRIPES[i])):	
					if i % 2 == 1:
						color = self.stripe1
					else:
						color = self.stripe2

					# Calculate contrast level
					height = len(sheep.VSTRIPES[i])
					con_level = (self.contrast * 2) - 255	# -255 to 255 value
					if con_level > 0:
						con_cell = con_level * (height - j - 1) / (height - 1)
					else:
						con_cell = con_level * j / (height - 1)
					
					adj_color = fade_color(color, con_cell)
					self.sheep.set_cell(sheep.VSTRIPES[i][j], adj_color)
					
			# Cycle the colors
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				self.contrast += randint(-2,2)
				if self.contrast > 200:
					self.contrast = 200
				if self.contrast < 50:
					self.contrast = 50
				
			yield self.speed