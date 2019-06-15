#
# Paths
#
# Show creates paths that slowly fade
# 
# Background is controlled by Touch OSC
# 

import sheep
from random import randint, choice
from color import RGB, HSV
            
# Converts a 0-1536 color into rgb on a wheel by keeping one of the rgb channels off

MaxColor = 1536

def Wheel(color):
	color = color % MaxColor  # just in case color is out of bounds
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

class Path(object):
	def __init__(self, sheep, start_cell):
		self.sheep = sheep
		self.faders = []	# List that holds fader objects
		self.cell = start_cell #choice(sheep.ALL)	# Start of path
		self.prev_cell = None
		self.length = randint(4,6)
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
		       						
class Paths(object):
	def __init__(self, sheep_sides):
		self.name = "Paths"        
		self.sheep = sheep_sides.both
		self.paths = []	# List that holds paths objects
		self.max_paths = 5
		
		self.foreground = randint(0,MaxColor)	# Path color
		self.background  = RGB(0, 0, 0) # Override with Touch OSC
		
		self.speed = 0.2
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'

		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.background.r = rgb255
		elif name == 'colorG':
			self.background.g = rgb255
		elif name == 'colorB':
			self.background.b = rgb255
							
	def next_frame(self):	
					
		while (True):
			
			while len(self.paths) < self.max_paths:
				new_path = Path(self.sheep, choice(sheep.ALL))
				self.paths.append(new_path)
			
			# Set background cells
			
			self.sheep.set_all_cells(self.background)			
			
			# Draw paths
				
			for p in self.paths:
				p.draw_path(Wheel(self.foreground), self.background)
				p.move_path()
			for p in self.paths:
				if p.path_alive() == False:
					self.paths.remove(p)
				
			# Cycle the foreground color
			
			self.foreground += 0.01
			if self.foreground > MaxColor:
				self.foreground -= MaxColor
			
			yield self.speed