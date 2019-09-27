from random import random, randint, choice
from math import sqrt

#
# Constants
#

maxColor = 1536
maxDir = 6

#
# Common random functions
#

# Random chance. True if 1 in Number
def oneIn(chance):
	if randint(1,chance) == 1:
		return True
	else:
		return False

# Return either 1 or -1
def plusORminus():
	return (randint(0,1) * 2) - 1

# Increase or Decrease a counter with a range
def upORdown(value, amount, min, max):
	value += (amount * plusORminus())
	return bounds(value, min, max)

# Increase/Decrease a counter within a range
def inc(value, increase, min, max):
	value += increase
	return bounds(value, min, max)

def bounds(value, min, max):
	if value < min:
		value = min
	if value > max:
		value = max
	return value
		
# Get a random direction
def randDir():
	return randint(0,maxDir)

# Return the left direction
def turn_left(dir):
	return (maxDir + dir - 1) % maxDir
	
# Return the right direction
def turn_right(dir):
	return (dir + 1) % maxDir

# Randomly turn left, straight, or right
def turn_left_or_right(dir):
	return (maxDir + dir + randint(-1,1) ) % maxDir

# In Bounds: hack for the Hourglass geometry. Creates a frame.
def in_bounds(coord):
	(x,y) = coord
	return x >= 0 and x <= 46 and y >= 0 and y <= 23

#
# Distance Functions
#
def distance(coord1, coord2):
	(x1,y1) = coord1
	(x2,y2) = coord2
	return sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )

def rect_coord(coord):
	"Return the precise, calculated rectilinear coordinates"
	(x,y) = coord
	return ( (x/2.0)+0.5, (y*0.866)+0.5 )

#
# Color Functions
#
# Pick a random color
def randColor():
	return randint(0,maxColor-1)
	
# Returns a random color around a given color within a particular range
# Function is good for selecting blues, for example
def randColorRange(color, window):
	return (maxColor + color + randint(int(-window),int(window))) % maxColor


# Wrapper for gradient_wheel in which the intensity is 1.0 (full)
def wheel(color):
	return gradient_wheel(color, 1)

# Picks a color in which one rgb channel is off and the other two channels
# revolve around a color wheel
def gradient_wheel(color, intense):
	color = color % maxColor  # just in case color is out of bounds
	channel = color / 256;
	value = color % 256;

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
	return (((float(r)*float(intense))/255.0, (float(g)*float(intense))/255.0, (float(b)*float(intense))/255.0))

#	return (r*intense, g*intense, b*intense)
	
# Picks a color in which one rgb channel is ON and the other two channels
# revolve around a color wheel
def white_wheel(color, intense):
	color = color % maxColor  # just in case color is out of bounds
	channel = color / 256;
	value = color % 256;

	if channel == 0:
		r = 255
		g = value
		b = 255 - value
	elif channel == 1:
		r = 255 - value
		g = 255
		b = value
	elif channel == 2:
		r = value
		g = 255 - value
		b = 255
	elif channel == 3:
		r = 255
		g = value
		b = 255 - value
	elif channel == 4:
		r = 255 - value
		g = 255
		b = value
	else:
		r = value
		g = 255 - value
		b = 255
	
	return ((float(r)*float(intense))/255.0, (float(g)*float(intense))/255.0, (float(b)*float(intense))/255.0)

ROTATE_CLOCK = [
    22,21,23,24,62,61,63,64,94,93,95,96,118,117,119,120,134,133,135,136,142,141,143,
    140,138,137,131,132,122,121,115,116,98,97,91,92,66,65,59,60,26,25,19,20,
    18,17,27,28,58,57,67,68,90,89,99,100,114,113,123,124,130,129,139,
    128,126,125,111,112,102,101,87,88,70,69,55,56,30,29,15,16,
    14,13,31,32,54,53,71,72,86,85,103,104,110,109,127,
    108,106,105,83,84,74,73,51,52,34,33,11,12,
    10,9,35,36,50,49,75,76,82,81,107,
    80,78,77,47,48,38,37,7,8,
    6,5,39,40,46,45,79,
    44,42,41,3,4,
    2,1,43,
    0
]

ROTATE_COUNTER = [
    143,141,140,138,139,129,128,126,127,109,108,106,107,81,80,78,79,45,44,42,43,1,0,
    2,3,41,40,46,47,77,76,82,83,105,104,110,111,125,124,130,131,137,136,142,
    135,133,132,122,123,113,112,102,103,85,84,74,75,49,48,38,39,5,4,
    6,7,37,36,50,51,73,72,86,87,101,100,114,115,121,120,134,
    119,117,116,98,99,89,88,70,71,53,52,34,35,9,8,
    10,11,33,32,54,55,69,68,90,91,97,96,118,
    95,93,92,66,67,57,56,30,31,13,12,
    14,15,29,28,58,59,65,64,94,
    63,61,60,26,27,17,16,
    18,19,25,24,62,
    23,21,20,
    22
]

ROTATE_COORD_CLOCK = { (0,0):(22,0), (1,0):(21,0), (2,0):(21,1), (3,0):(20,1), (4,0):(20,2), (5,0):(19,2),
(6,0):(19,3), (7,0):(18,3), (8,0):(18,4), (9,0):(17,4), (10,0):(17,5), (11,0):(16,5), (12,0):(16,6), (13,0):(15,6),
(14,0):(15,7), (15,0):(14,7), (16,0):(14,8), (17,0):(13,8), (18,0):(13,9), (19,0):(12,9), (20,0):(12,10), (21,0):(11,10),
(22,0):(11,11), (1,1):(20,0), (2,1):(19,0), (3,1):(19,1), (4,1):(18,1), (5,1):(18,2), (6,1):(17,2), (7,1):(17,3),
(8,1):(16,3), (9,1):(16,4), (10,1):(15,4), (11,1):(15,5), (12,1):(14,5), (13,1):(14,6), (14,1):(13,6), (15,1):(13,7),
(16,1):(12,7), (17,1):(12,8), (18,1):(11,8), (19,1):(11,9), (20,1):(10,9), (21,1):(10,10), (2,2):(18,0), (3,2):(17,0),
(4,2):(17,1), (5,2):(16,1), (6,2):(16,2), (7,2):(15,2), (8,2):(15,3), (9,2):(14,3), (10,2):(14,4), (11,2):(13,4),
(12,2):(13,5), (13,2):(12,5), (14,2):(12,6), (15,2):(11,6), (16,2):(11,7), (17,2):(10,7), (18,2):(10,8), (19,2):(9,8),
(20,2):(9,9), (3,3):(16,0), (4,3):(15,0), (5,3):(15,1), (6,3):(14,1), (7,3):(14,2), (8,3):(13,2), (9,3):(13,3), (10,3):(12,3),
(11,3):(12,4), (12,3):(11,4), (13,3):(11,5), (14,3):(10,5), (15,3):(10,6), (16,3):(9,6), (17,3):(9,7), (18,3):(8,7),
(19,3):(8,8), (4,4):(14,0), (5,4):(13,0), (6,4):(13,1), (7,4):(12,1), (8,4):(12,2), (9,4):(11,2), (10,4):(11,3),
(11,4):(10,3), (12,4):(10,4), (13,4):(9,4), (14,4):(9,5), (15,4):(8,5), (16,4):(8,6), (17,4):(7,6), (18,4):(7,7),
(5,5):(12,0), (6,5):(11,0), (7,5):(11,1), (8,5):(10,1), (9,5):(10,2), (10,5):(9,2), (11,5):(9,3), (12,5):(8,3),
(13,5):(8,4), (14,5):(7,4), (15,5):(7,5), (16,5):(6,5), (17,5):(6,6), (6,6):(10,0), (7,6):(9,0), (8,6):(9,1),
(9,6):(8,1), (10,6):(8,2), (11,6):(7,2), (12,6):(7,3), (13,6):(6,3), (14,6):(6,4), (15,6):(5,4), (16,6):(5,5),
(7,7):(8,0), (8,7):(7,0), (9,7):(7,1), (10,7):(6,1), (11,7):(6,2), (12,7):(5,2), (13,7):(5,3), (14,7):(4,3),
(15,7):(4,4), (8,8):(6,0), (9,8):(5,0), (10,8):(5,1), (11,8):(4,1), (12,8):(4,2), (13,8):(3,2), (14,8):(3,3),
(9,9):(4,0), (10,9):(3,0), (11,9):(3,1), (12,9):(2,1), (13,9):(2,2), (10,10):(2,0), (11,10):(1,0),
(12,10):(1,1), (11,11):(0,0) }
