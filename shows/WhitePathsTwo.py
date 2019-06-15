#
# White Paths Two
#
# Show creates paths that slowly fade
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

class Path(object):
	def __init__(self, sheep, start_cell, length, decay):
		self.sheep = sheep
		self.faders = []	# List that holds fader objects
		self.cell = start_cell #choice(sheep.ALL)	# Start of path
		self.prev_cell = None
		self.length = randint(60,100)
		self.decay = 1.0 / self.length
		
		new_fader = Fader(self.sheep, self.cell, self.decay)
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
		if self.length > 0:
			self.length -= 1
			new_cell = self.choose_head(self.cell, self.prev_cell)
			self.prev_cell = self.cell
			self.cell = new_cell
			new_fader = Fader(self.sheep, self.cell, self.decay)
			self.faders.append(new_fader)
			
	def choose_head(self, curr_cell, prev_cell):
		i = 10	# Number of tries to find a new head
		while (i > 0):
			neighbors = sheep.edge_neighbors(curr_cell)
			if len(neighbors) == 0:
				return prev_cell
			elif len(neighbors) == 1:
				return neighbors[0]
			else:
				new_head = choice(neighbors)
				if new_head != prev_cell and new_head <= 43 and new_head > 0:
					return new_head
		return prev_cell
		       						
class WhitePathsTwo(object):
	def __init__(self, sheep_sides):
		self.name = "WhitePathsTwo"        
		self.sheep = sheep_sides.both
		self.paths = []	# List that holds paths objects
		self.max_paths = 2
		self.length = randint(60,100)
		self.decay = 1.0 / self.length
		
		self.foreground = RGB(255,255,255)	# White
		self.background  = RGB(50, 50, 50) # Black
		
		self.speed = 0.2
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'

		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.max_paths = (rgb255 * 3 / 255) + 1
		elif name == 'colorG':
			self.decay = 1.0 / ((rgb255 * 90 / 255) + 10)
		elif name == 'colorB':
			self.length = (rgb255 * 40 / 255) + 60
							
	def next_frame(self):	
					
		while (True):
			
			while len(self.paths) < self.max_paths:
				new_path = Path(self.sheep, choice(sheep.ALL), self.length, self.decay)
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