#
# White Cocoon
#
# Show draws a white cocoon
# 
# Cocoon contrast adjusted by Touch OSC
# in an odd way
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

# Interpolates between colors. Fract = 1 is all color 2
def morph_color(color1, color2, fract):
	morph_h = color1.h + ((color2.h - color1.h) * fract)
	morph_v = color1.v + ((color2.v - color1.v) * fract)
	morph_s = color1.s + ((color2.s - color1.s) * fract)
	
	return HSV(morph_h, morph_s, morph_v)
	
class WhiteCocoon(object):
	def __init__(self, sheep_sides):
		self.name = "WhiteCocoon"
		self.sheep = sheep_sides.both
		
		self.last_osc = time.time()

		self.color = RGB(255,255,255)	# White
		
		self.c_contrast = 100	# 0-255 value adjusted by g-channel of Touch OSC
		self.r_contrast = 50	# 0-255 value adjusted by b-channel of Touch OSC
				
		self.speed = 0.5
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.c_contrast = rgb255
		elif name == 'colorG':
			self.r_contrast = rgb255

	def next_frame(self):	
		while (True):
			
			width = len(sheep.VSTRIPES)
			for i in range(width):
			
				# Calculate column contrast level

				c_con_level = (self.c_contrast * 2) - 255	# -255 to 255 value
				if c_con_level > 0:
					c_con_cell = c_con_level * (width - i - 1) / (width - 1)
				else:
					c_con_cell = c_con_level * i / (width - 1)
			
				height = len(sheep.VSTRIPES[i])
				for j in range(height):	

					# Calculate row contrast level

					r_con_level = (self.r_contrast * 2) - 255	# -255 to 255 value
					if r_con_level > 0:
						r_con_cell = r_con_level * (height - j - 1) / (height - 1)
					else:
						r_con_cell = r_con_level * j / (height - 1)
					
					# Double adjusting
					adj_color = fade_color(self.color, r_con_cell)
					adj_color = fade_color(adj_color, c_con_cell)
					
					self.sheep.set_cell(sheep.VSTRIPES[i][j], adj_color)
					
			yield self.speed