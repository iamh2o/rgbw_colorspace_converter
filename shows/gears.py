from .showbase import ShowBase

from color import RGB
from grid.cell import Direction, Position, Coordinate

from HelperFunctions import*
from triangle import*

class Gear():
	def __init__(self, grid, pos):
		self.grid = grid
		self.size = choice([1,2])
		self.dir = 5
		self.turn = self.size % 5
		self.pos = pos
		self.colorchurn = randint(0,6)

	def draw_gear(self, color, clock):
		color += (self.size * 100)
		wc = wheel(color)
		try:
			self.grid.set(Coordinate(x=self.pos[0],y=self.pos[1]), RGB(wc[0],wc[1],wc[2]))  # Draw the center
		except:
			pass
		# Draw the rest of the rings
		for r in range(self.size):
			col = (color + (r * self.colorchurn)) % maxColor
			for coord in get_ring(self.pos,r):
				wh = wheel(col)
				try:
					self.grid.set(Coordinate(coord[0],coord[1]), RGB(wh[0],wh[1], wh[2]))
				except:
					pass
		# Draw the outside gear
		ring_cells = get_ring(self.pos, self.size)
		num_cells = len(ring_cells)
		for i in range(num_cells):
			col = (color + (self.size * self.colorchurn)) % maxColor
			if (i + clock) % 2 == 0:
				wh = wheel(col)
				for c in ring_cells[i]:
					try:
						self.grid.set(Coordinate(c[0],c[1]), RGB(wh[0],wh[1], wh[2]))
					except:
						pass
	
	def move_gear(self):
		self.pos = tri_in_direction(self.pos, self.dir, 2)
		self.dir = turn_right(self.dir) if self.turn == 1 else turn_left(self.dir)

				
class Gears(ShowBase):
	def __init__(self, grid, frame_delay=0.25):
		self.frame_delay = frame_delay
		self.grid = grid
		self.gears = []		# List that holds Gears objects
		self.clock = 10000
		self.color = randColor()

		          
	def next_frame(self):	

		self.gears.extend([Gear(grid=self.grid, pos=coord) for coord in all_corners() + all_centers()])



		while (True):


			for g in self.gears:
				g.draw_gear(self.color, self.clock)
				g.move_gear()
			
			self.clock += 1

			self.color = randColorRange(self.color, 30)

			yield self.frame_delay
			
