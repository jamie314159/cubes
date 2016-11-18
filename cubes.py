#!/bin/ipython3

# Constants ---------------------------------------------------

# Direction deffinitions
CW = 0
CCW = 1

# For easier reading when referenceing coordinates
X = 0
Y = 1

# Map of directions to coorsponding numbers
N 	= 0
NE 	= 1
E 	= 2
SE 	= 3
S 	= 4
SW 	= 5
W 	= 6
NW 	= 7

# Lists of directions for iteration
DA = [N,E,S,W]
DB = [N,NE,E,SE,S,SW,W,NW]
DC = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]

pivotTable = [[W,N],[N,E],[E,S],[S,W]]

squaresList = []
# squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]
squaresCoords = {}

MASTER = 0

# Functions, Procedures, Classes & Methods --------------------------------------------------------

class coordinate(tuple):
	def __add__(self, direction):
		return coordinate((self[X] + DC[direction][X], self[Y] + DC[direction][Y]))


# Returns opposite direction of orientation
def opposite(orientation):
	return((orientation+4)%8)

# Increments orientation in direction num times
def clock(orientation, direction, num = 1):
	d = (1 if direction == CW else -1)
	for n in range(num):
		orientation = (orientation + d) % 8
	return orientation

class Square(object):
	def __init__(self, x = -1, y = -1):
			# self.fill = "grey"
			#self.master = master
			#self.connections = {}
			self.drawings = []
			self.location = (x,y)
			self.orientation = N
			
	
	def rotate(self, direction):
		self.orientation = clock(self.orientation, direction, 2)

	# Pivot self in given direction
	def pivot(self, corner, direction):
		print(pivotTable[corner][direction])
		self.move(pivotTable[corner][direction])
		self.rotate(direction)
	
	def move(self, direction):
		self.location = (self.location[X]+DC[direction][X],self.location[Y]+DC[direction][Y])
			

	


