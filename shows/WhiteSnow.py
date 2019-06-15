#
# White Snow
#
# Show draws vertically failing trails
# 
# Snow color is always white
# Background is black
# 

import sheep
import time
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

class Path(object):
	def __init__(self, sheep, trajectory, decay):
		self.sheep = sheep
		self.faders = []	# List that holds fader objects
		self.pos = 0
		self.decay = decay
		self.trajectory = trajectory				
		self.length = len(self.trajectory)
		
		new_fader = Fader(self.sheep, self.trajectory[0], self.decay)
		self.faders.append(new_fader)
	
	def draw_path(self, foreground, background):
		for f in self.faders:
			f.draw_fader(foreground, background)
		for f in self.faders:
			if f.age_fader() == False:
				self.faders.remove(f)
	
	def path_alive(self):
		if len(self.faders) > 0:
			return True
		else:
			return False
			
	def move_path(self):
		if self.pos < (self.length - 1):
			self.pos += 1
			new_fader = Fader(self.sheep, self.trajectory[self.pos], self.decay)
			self.faders.append(new_fader)
			
class WhiteSnow(object):
	def __init__(self, sheep_sides):
		self.name = "White Snow"
		self.sheep = sheep_sides.both
		self.paths = []	# List that holds paths objects
		self.max_paths = 6
		self.decay = 1.0 / 3
		self.background  = RGB(0,0,0) # Always Black
		self.foreground = RGB(255,255,255)	# Always White
		
		self.speed = 0.05
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.max_paths = (rgb255 * 8 / 255) + 2
		elif name == 'colorG':
			self.decay = 1.0 / ((rgb255 * 4) + 1)
					
	def next_frame(self):	
		while (True):
			
			if len(self.paths) < self.max_paths:
				stripe_num = randint(0, len(sheep.VSTRIPES) - 1)
				new_path = Path(self.sheep, sheep.VSTRIPES[stripe_num], self.decay)
				self.paths.append(new_path)
			
			# Set background cells

			self.sheep.set_all_cells(self.background)						
			
			# Draw paths
				
			for p in self.paths:
				p.draw_path(self.foreground, self.background)
				p.move_path()
			for p in self.paths:
				if p.path_alive() == False:
					self.paths.remove(p)
				
			yield self.speed