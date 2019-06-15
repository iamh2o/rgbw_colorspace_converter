#
# Zebra
#
# Show draws alternating vertical stripes
# 
# Strip colors are controlled by Touch OSC
# in an odd way
# 

import sheep
import time
from random import randint, choice
from color import RGB, HSV
            
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
	
		#adj_color = morph_color(back_color, fore_color, self.life)
		#self.sheep.set_cell(self.cell, adj_color)
	
class Zebra(object):
	def __init__(self, sheep_sides):
		self.name = "Zebra"
		self.sheep = sheep_sides.both
		
		self.last_osc = time.time()
		self.OSC = False	# Is Touch OSC working?

		self.stripe1 = randint(0, MaxColor);		
		self.stripe2 = randint(0, MaxColor);		
		
		self.contrast = 100	# 0 -255 value adjusted by b-channel of Touch OSC
		
		self.speed = 0.5
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.stripe1 = rgb255 * 6
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorG':
			self.stripe2 = rgb255 * 6
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorB':
			self.contrast = rgb255
			self.last_osc = time.time()
			self.OSC = True						
					
	def next_frame(self):	
		while (True):

			for i in range(len(sheep.VSTRIPES)):
				for j in range(len(sheep.VSTRIPES[i])):	
					if i % 2 == 0:
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
					
					adj_color = fade_color(Wheel(color), con_cell)
					self.sheep.set_cell(sheep.VSTRIPES[i][j], adj_color)
					
			# Cycle the colors
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				self.stripe1 += 1
				if self.stripe1 > MaxColor:
					self.stripe1 -= MaxColor
					
				self.stripe2 -= 1
				if self.stripe2 < 0:
					self.stripe2 = MaxColor					
				
			yield self.speed