#
# White Starburst
#
# Show creates White Starbursts that slowly fade
# 
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
	def __init__(self, sheep, length, decay):
		self.sheep = sheep
		self.faders = []	# List that holds fader objects
		self.heads = []	# coordinate list of growing heads
		self.length = length
		self.decay = decay
		self.color = RGB(255,255,255)	# Always white
		
		# Plant first head
		new_head = choice(self.sheep.all_cells())
		self.heads.append(new_head)
		new_fader = Fader(self.sheep, new_head, self.decay)
		self.faders.append(new_fader)
	
	def draw_path(self, background):
		for f in self.faders:
			f.draw_fader(self.color, background)
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
			new_heads = []	# temporary list to hold new heads
			
			for h in self.heads:
				for edge in self.sheep.edge_neighbors(h):
					if self.is_empty(edge):
						new_head = edge
						new_heads.append(new_head)
						new_fader = Fader(self.sheep, new_head, self.decay)
						self.faders.append(new_fader)

			for h in new_heads:
				self.heads.append(h)

	def is_empty(self, cell):
		for f in self.faders:
			if f.cell == cell:
				return False
		return True
			

class WhiteStarburst(object):
	def __init__(self, sheep_sides):
		self.name = "White Starburst"        
		self.sheep = sheep_sides.both
		self.starbursts = []	# List that holds Path objects
		self.max_starbursts = 4
		self.decay = 1.0 / 4
		self.length = 3
		self.background = RGB(50,50,50)
		self.speed = 0.2
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'

		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.max_starbursts = (rgb255 * 6 / 255) + 1
		elif name == 'colorG':
			self.decay = 1.0 / ((rgb255 * 4 / 255) + 2)
		elif name == 'colorB':
			self.length = (rgb255 * 4 / 255) + 1
							
	def next_frame(self):	
					
		while (True):
			
			if len(self.starbursts) < self.max_starbursts:
				new_path = Path(self.sheep, self.length, self.decay)
				self.starbursts.append(new_path)
					
			# Draw Starburst
				
			for p in self.starbursts:
				p.draw_path(self.background)
				p.move_path()
			for p in self.starbursts:
				if p.path_alive() == False:
					self.starbursts.remove(p)
			
			yield self.speed