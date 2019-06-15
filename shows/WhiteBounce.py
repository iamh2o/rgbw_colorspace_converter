#
# White Bounce
#
# Show draws 3 balls that bounce horizontally
# 
# Background is black
#
# Balls are white
#
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
		self.pos = 0	# Where along the sheep
		self.dir = 1	# 1 or -1 for left or right
		self.decay = decay
		self.trajectory = trajectory				
	
	def set_decay(self, decay):
		self.decay = decay
		
	def draw_path(self, foreground, background):
		for f in self.faders:
			f.draw_fader(foreground, background)
		for f in self.faders:
			if f.age_fader() == False:
				self.faders.remove(f)
	
	def move_path(self):
		self.pos += self.dir
		if self.pos <= 0 or self.pos >= len(self.trajectory) - 1:
			self.dir *= -1	# Flip direction: bounce

		new_fader = Fader(self.sheep, self.trajectory[self.pos], self.decay)
		self.faders.append(new_fader)
		
		if randint(1,30) == 1:
			self.decay = 1.0 / randint(2,8)	# Change trail length
		
class WhiteBounce(object):
	def __init__(self, sheep_sides):
		self.name = "WhiteBounce"
		self.sheep = sheep_sides.both
		self.decay = 1.0 / 6
		self.paths = []	# List that holds paths objects
		self.trajectories = (sheep.LOW, sheep.MEDIUM, sheep.HIGH)
		self.background  = RGB(0,0,0) # Always Black
		self.foreground = RGB(255,255,255)	# White
		
		# Set up 3 balls on low, medium, and high levels
		
		for i in range(3):
			new_path = Path(self.sheep, self.trajectories[i], self.decay)
			self.paths.append(new_path)
			
		self.speed = 0.2
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.decay = 1.0 / (((rgb255 * 8) / 255) + 2) 
			for p in self.paths:
				p.set_decay(self.decay)
				
	def next_frame(self):	
					
		while (True):
			
			# Set background cells
			
			self.sheep.set_all_cells(self.background)						
			
			# Draw paths
				
			for p in self.paths:
				p.draw_path(self.foreground, self.background)
				p.move_path()
			
			yield self.speed