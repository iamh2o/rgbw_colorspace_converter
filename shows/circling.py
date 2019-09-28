from .showbase import ShowBase
from HelperFunctions import*
from triangle import*
from grid.cell import Direction, Position, Coordinate
from color import HSV

class Trail(object):
	def __init__(self, trimodel, color, intense, pos, center):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.intense = intense
		self.center = center
	
	def draw_trail(self):
		self.tri.set(Coordinate(x=self.pos[0],y=self.pos[1]), self.color)
	
	def fade_trail(self):
		self.pos = near_neighbor(self.pos, self.center)
		self.intense -= 0.1
		return self.intense > 0.2


class Planet(object):
	def __init__(self, trimodel, pos, color, dir, center):
		self.tri = trimodel
		self.pos = pos
		self.color = color
		self.rotation = randint(0,1)
		self.dir = dir
		self.arc = randint(3,6)
		self.arc_count = self.arc
		self.size = 2
		self.center = center
		self.trails = []	# List that holds trails
		
	def draw_planet(self):
		
		self.fade_trails()
		
		for i in range(2):
			for c in get_ring(self.pos, i):	
				self.draw_add_trail(self.color, 1 - (0.07 * i), c, self.center)
	
	def move_planet(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		self.arc_count -= 1
		if self.arc_count == 0:
			self.arc_count = self.arc
			self.dir = turn_left(self.dir) if self.rotation == 0 else turn_right(self.dir)
		
	def draw_add_trail(self, color, intense, pos, center):
		if self.tri.cell_exists(Coordinate(pos[0],pos[1])):
			color = HSV(0.5,1.0,1.0)
			self.tri.set(Coordinate(pos[0],pos[1]), color)
			new_trail = Trail(self.tri, color, intense, pos, center)
			self.trails.append(new_trail)
	
	def fade_trails(self):
		for t in self.trails:	 # Plot last-in first
			t.draw_trail()
			if not t.fade_trail():
				self.trails.remove(t)
			
				
class Circling(ShowBase):
	def __init__(self, trimodel, frame_delay=1.1):
		self.tri = trimodel
		self.planets = []	# List that holds Planet objects
		self.speed = frame_delay
		self.dir = 0
		self.color = randColor()
#		from IPython import embed; embed()


	def next_frame(self):
		
		self.tri.clear()

		for strip in range(6):
			for corner in corners(strip):
				new_planet = Planet(self.tri, corner, self.color, self.dir, center(strip))
				self.planets.append(new_planet)
				self.color = (self.color + 40) % maxColor
				self.dir = turn_left(self.dir)

			
		while (True):
			
			self.tri.clear()
			
			for p in self.planets:
				p.draw_planet()
				p.move_planet()
			
			yield self.speed
