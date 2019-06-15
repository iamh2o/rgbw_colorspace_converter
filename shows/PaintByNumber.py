#
# PaintByNumber
#
# Show populates every panel with different, random 5-100% intensities
# As the show progresses, each panel gets brighter or darker
# 
# Each section of the sheep gets a different color
#
# Touch OSC controls the three sections
# 

import sheep
import time
from random import randint
from color import RGB

# Converts a 0-MaxColor color into rgb on a wheel by keeping one of the rgb channels off

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

class PaintByNumber(object):
	def __init__(self, sheep_sides):
		self.name = "Paint By Number"
		self.sheep = sheep_sides.both

		self.speed = 0.1
		self.last_osc = time.time()
		
		self.OSC = False	# Is Touch OSC working?
		
		self.wheels = [randint(0,MaxColor), randint(0,MaxColor), randint(0,MaxColor)]
		self.colors = [Wheel(self.wheels[0]), Wheel(self.wheels[1]), Wheel(self.wheels[2])]

		self.panels = []	# List of panels

		for cell in self.sheep.all_cells():
			new_panel = Panel(self.sheep, cell)
			self.panels.append(new_panel)

	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.colors[0] = rgb255 * 6
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorG':
			self.colors[1] = rgb255 * 6
			self.last_osc = time.time()
			self.OSC = True
		elif name == 'colorB':
			self.colors[2] = rgb255 * 6
			self.last_osc = time.time()
			self.OSC = True

	def next_frame(self):
		while True:

			for p in self.panels:
				if self.OSC:	# Which color to use?
					p.draw_panel(self.colors)
				else:
					p.draw_panel([Wheel(self.wheels[0]),
									Wheel(self.wheels[1]),
									Wheel(self.wheels[2])])
				
				p.update_panel()
			
			if time.time() - self.last_osc > 120:	# 2 minutes
				self.OSC == False
				
			if self.OSC == False:
				for i in range(3):
					self.wheels[i] += 5
					if self.wheels[i] > MaxColor:
						self.wheels[i] -= MaxColor

			yield self.speed


class Panel(object):
	def __init__(self, sheep, cell):
		
		self.sheep = sheep
		self.cell = cell
		self.type = self.get_type(cell)
		
		self.intensity = randint(5,100)
		
		# Generate velocities of -2,-1,1, or 2
		self.velocity = randint(1,2)
		if randint(0,1) == 1: self.velocity *= -1

	def get_type(self, cell):
		types = (sheep.SHOULDER + sheep.LEG, sheep.RACK, sheep.LOIN)
		
		for t in range (len(types)):
			for c in types[t]:
				if c == cell:
					return t
		return 0
	
	def draw_panel(self, colors):
		color = colors[self.type].copy()
		color.v = self.intensity / 100.0
		self.sheep.set_cell(self.cell, color)
		
	def update_panel(self):
		self.intensity += self.velocity
		
		if self.intensity > 100:
			self.intensity = 100
			self.velocity *= -1
		elif self.intensity < 5:
			self.intensity = 5
			self.velocity *= -1

