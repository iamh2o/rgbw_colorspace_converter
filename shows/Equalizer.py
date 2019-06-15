#
# Equalizer
#
# 3-Horizontal bands pulse
# 
# Touch OSC controls the amount of each band
# 

import sheep
import time
from math import sin
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

class Equalizer(object):
	def __init__(self, sheep_sides):
		self.name = "Equalizer"
		self.sheep = sheep_sides.both		
		self.eq_max = 17
		self.black = RGB(0,0,0)
		self.rate_min = 1
		self.rate_max = 10
		self.rates = [randint(self.rate_min,self.rate_max),
						randint(self.rate_min,self.rate_max),
						randint(self.rate_min,self.rate_max)]
						
		self.eqlizer = [0,0,0]	# Random initial values
		self.eq_colors = (RGB(0,50,0),	#1
							RGB(0,100,0),	#2
							RGB(0,150,0),	#3
							RGB(0,200,0),	#4
							RGB(0,255,0),	#5
							RGB(130,255,0),	#6
							RGB(255,240,0),	#7
							RGB(255,180,0),	#8
							RGB(255,120,0),	#9
							RGB(255,60,0),	#10
							RGB(255,30,0),	#11
							RGB(255,0,0),	#12
							RGB(255,0,0),	#13
							RGB(230,0,0),	#14
							RGB(200,0,0),	#15
							RGB(170,0,0),	#16
							RGB(140,0,0))	#17
							
		self.speed = 0.1
		
		self.cell_map = (sheep.LOW, sheep.MEDIUM, sheep.HIGH)
		self.last_osc = time.time()
		self.OSC = False	# Is Touch OSC working?
		
	def set_param(self, name, val):
		# name will be 'colorR', 'colorG', 'colorB'
		rgb255 = int(val * 0xff)
		if name == 'colorR':
			self.eqlizer[0] = rgb255 * self.eq_max / 255
			self.last_osc = time.time()
			self.OSC = True
		if name == 'colorG':
			self.eqlizer[1] = rgb255 * self.eq_max / 255
			self.last_osc = time.time()
			self.OSC = True
		if name == 'colorB':
			self.eqlizer[2] = rgb255 * self.eq_max / 255
			self.last_osc = time.time()
			self.OSC = True
					
	def next_frame(self):	
		while (True):
			
			self.poll_time()
			self.draw_equalizer()
			
			for y in range (3):
				if randint(0,20) == 1:
					self.rates[y] = randint(self.rate_min, self.rate_max)
					
			yield self.speed
	
	def poll_time(self):
		t = time.time()
		for y in range (3):
			self.eqlizer[y] = ((sin(t * self.rates[y])) + 1) * len(self.cell_map[y]) / 2
			
	def draw_equalizer(self):
		for y in range (3):
			for x in range (len(self.cell_map[y])):
				if x >= self.eqlizer[y]:
					color = self.black
				else:
					color = self.eq_colors[x]
				self.sheep.set_cell(self.cell_map[y][x], color)
					