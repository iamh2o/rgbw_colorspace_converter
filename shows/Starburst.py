#
# Starburst
#
# Show creates Starbursts that slowly fade
# 
# Background is controlled by Touch OSC
# 

import sheep
import time
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
	def __init__(self, sheep):
		self.sheep = sheep
		self.faders = []	# List that holds fader objects
		self.heads = []	# coordinate list of growing heads
		self.length = randint(1,5)
		self.decay = 1.0 / randint(3,6)
		self.color = Wheel(randint(0, MaxColor))
		
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
			

class Starburst(object):
	def __init__(self, sheep_sides):
		self.name = "Starburst"        
		self.sheep = sheep_sides.both
		self.starbursts = []	# List that holds Path objects
		self.max_starbursts = 2
		self.speed = 0.2
		
		self.last_osc = time.time()		
		self.OSC = False	# Is Touch OSC working?
		self.noOSCcolor = randint(0,MaxColor)	# Default color if no Touch OSC
		self.OSCcolor = Wheel(self.noOSCcolor)
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.OSCcolor.r = rgb255
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorG':
			self.OSCcolor.g = rgb255
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorB':
			self.OSCcolor.b = rgb255
			self.last_osc = time.time()
			self.OSC = True
							
	def next_frame(self):	
					
		while (True):
			
			if len(self.starbursts) < self.max_starbursts:
				new_path = Path(self.sheep)
				self.starbursts.append(new_path)
			
			# Pick the background color - either random or Touch OSC
			
			if self.OSC:	# Which color to use?
				background = self.OSCcolor.copy()
			else:
				background = Wheel(self.noOSCcolor)
					
			# Draw Starburst
				
			for p in self.starbursts:
				p.draw_path(background)
				p.move_path()
			for p in self.starbursts:
				if p.path_alive() == False:
					self.starbursts.remove(p)
			
			# Change background color
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				self.noOSCcolor += 1
				if self.noOSCcolor > MaxColor:
					self.noOSCcolor -= MaxColor
				
			yield self.speed