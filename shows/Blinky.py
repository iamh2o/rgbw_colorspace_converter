#
# Blinky
#
# Show creates one-cell faders that slowly fade in intensity
# 
# Background is controlled by Touch OSC
# 

import sheep
from random import randint, choice
from color import RGB, HSV
            
# Converts a 0-1536 color into rgb on a wheel by keeping one of the rgb channels off

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

# Interpolates between colors. Fract = 1 is all color 2
def morph_color(color1, color2, fract):
	morph_h = color1.h + ((color2.h - color1.h) * fract)
	morph_s = color1.s + ((color2.s - color1.s) * fract)
	morph_v = color1.v + ((color2.v - color1.v) * fract)
	
	return HSV(morph_h, morph_s, morph_v)
	
class Fader(object):
	def __init__(self, sheep, cell, decay):
		self.sheep = sheep
		self.cell = cell
		self.decay = decay
		self.life = 1.0
	
	def draw_fader(self, fore_color, back_color):
		adj_color = morph_color(back_color, fore_color, self.life)
		self.sheep.set_cell(self.cell, adj_color)
	
	def age_fader(self):
		self.life -= self.decay
		if self.life > 0:
			return True	# Still alive
		else:
			return False	# Life less than zero -> Kill

        						
class Blinky(object):
	def __init__(self, sheep_sides):
		self.name = "Blinky"        
		self.sheep = sheep_sides.both
		self.faders = []	# List that holds Fader objects
		self.max_faders = 15
		
		self.foreground = randint(0,255)	# Sparkle color
		self.background  = RGB(0, 255, 0) # Override with Touch OSC
		
		self.speed = 0.1
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'

		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.background.r = rgb255
		elif name == 'colorG':
			self.background.g = rgb255
		elif name == 'colorB':
			self.background.b = rgb255
	
	def get_empty_cell(self):
		while (True):
			new_cell = choice(sheep.ALL)
			if self.is_empty(new_cell):
				return(new_cell)
							
	def is_empty(self, cell):
		for f in self.faders:
			if cell == f.cell:
				return False
		return True 
						
	def next_frame(self):	
					
		while (True):
			
			while len(self.faders) < self.max_faders:
				new_fader = Fader(self.sheep, self.get_empty_cell(), randint(1,5) / 20.0)
				self.faders.append(new_fader)
			
			# Set background cells
			
			self.sheep.set_all_cells(self.background)
			
			# Draw the faders
				
			for f in self.faders:
				f.draw_fader(Wheel(self.foreground), self.background)
			for f in self.faders:
				if f.age_fader() == False:
					self.faders.remove(f)
			
			# Cycle the foreground color
			
			self.foreground += 0.01
			if self.foreground > 1536:
				self.foreground -= 1536
			
			yield self.speed