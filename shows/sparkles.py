from .showbase import ShowBase
from color import RGB

from HelperClasses import*
import random
from grid import every
import time

class Sparkles(ShowBase):
	def __init__(self, grid, frame_delay=0.1):
#		self.name = "Sparkles"        
		self.grid = grid
		self.faders = Faders(self.grid)
		self.frame_delay = frame_delay
		self.color = randColor()
		self.spark_num = 15


	def set_param(self, name, val):
		if name == 'flash':
			try:
				self.grid.set(every, RGB(255, 0, 0, brightness_override=1.0))
				self.grid.go()
				old_fd = self.frame_delay 
				self.frame_delay = 5
				self.grid.go()
				self.frame_delay = old_fd
			except Exception as e:
				print("Bad Hue flash!", val, e)
				
		if name == 's_num':
			try:
				self.spark_num = int(val)
			except Exception as e:
				print("Bad Speed Value!", val)
		  #Touch OSC Stuff                                                                                                      
		if name == 'speed':
			try:
				self.frame_delay = float(val)
			except Exception as e:
				print("Bad Speed Value!", val)
		          
	def next_frame(self):
		
		for i in range (self.spark_num):
			self.add_new_sparkle()
					
		while (True):

			self.faders.cycle_faders(refresh=True)

			while self.faders.num_faders() < self.spark_num:
				self.add_new_sparkle()
			
			if oneIn(100):
				self.color = randColorRange(self.color, 30)
			
			yield self.frame_delay  	# random time set in init function

	def add_new_sparkle(self):
		cell = random.choices(self.grid.cells)          
		self.faders.add_fader(color=randColorRange(self.color, 30),
							  pos=(cell[0].coordinate.x, cell[0].coordinate.y),
							  change=1.0 / randint(3,10),
							  intense=0,
							  growing=True)
