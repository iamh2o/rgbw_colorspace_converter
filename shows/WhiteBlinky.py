#
# White Blinky
#
# Show creates one-cell faders that slowly fade in intensity
# 
# Background is black
# 

import sheep
from random import randint, choice
from color import RGB, HSV
            
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

        						
class WhiteBlinky(object):
	def __init__(self, sheep_sides):
		self.name = "WhiteBlinky"        
		self.sheep = sheep_sides.both
		self.faders = []	# List that holds Fader objects
		self.max_faders = 20
		self.aging = 0.1
		
		self.foreground = RGB(255,255,255)	# Sparkle color = white
		self.background  = RGB(0, 0, 0) # Background = black
		
		self.speed = 0.1
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'

		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.max_faders = (rgb255 * 40 / 255) + 1
		elif name == 'colorG':
			self.aging = ((rgb255 * 5 / 255) + 1) / 20.2
	
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
				new_fader = Fader(self.sheep, self.get_empty_cell(), self.aging)
				self.faders.append(new_fader)
			
			# Set background cells
			
			self.sheep.set_all_cells(self.background)
			
			# Draw the faders
				
			for f in self.faders:
				f.draw_fader(self.foreground, self.background)
			for f in self.faders:
				if f.age_fader() == False:
					self.faders.remove(f)
			
			yield self.speed