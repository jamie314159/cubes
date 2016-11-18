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

def moveResult(square, direction):
	return (square.location[X]+DC[direction][X],square.location[Y]+DC[direction][Y])

def pivotResult(square, corner, direction):
	return moveResult(square, pivotTable[corner][direction])
	


def canPivot(square, corner, direction):
	r = 1
	x1 = square.location[X]
	y1 = square.location[Y]
	s = pivotResult(square,corner,direction)
	x2 = s[X]
	y2 = s[Y]
	pivotCheckTable = [[[(x1,y1+1),(x2,y2+1),(x2,y2)],[(x1+1,y1),(x2+1,y2),(x2,y2)]],
				   	   [[(x1-1,y1),(x2-1,y2),(x2,y2)],[(x1,y1+1),(x2,y2+1),(x2,y2)]],
				   	   [[(x1,y1-1),(x2,y2-1),(x2,y2)],[(x1-1,y1),(x2-1,y2),(x2,y2)]],
				   	   [[(x1+1,y1),(x2+1,y2),(x2,y2)],[(x1,y1-1),(x2,y2-1),(x2,y2)]]]
	
	for square in squaresList:
		if square.location in pivotCheckTable[corner][direction]:
			r = 0
			continue
	return r


class Square(object):
	def __init__(self, x = -1, y = -1):
			# self.fill = "grey"
			#self.master = master
			#self.connections = {}
			self.drawings = []
			self.location = (x,y)
			self.orientation = N
			squaresList.append(self)
			
	# Pivot self in given direction about specified corner
	def pivot(self, corner, direction):
		if canPivot(self,corner,direction):
			self.move(pivotTable[corner][direction])
			self.rotate(direction)

		## Finds next 90 pivot
		# newCorner = ((corner+1)%4 if direction == CW else (corner-1)%4)
		# if canPivot(self,newCorner,direction):
		# 	self.move(pivotTable[newCorner][direction])
		# 	self.rotate(direction)

	def rotate(self, direction):
		self.orientation = clock(self.orientation, direction, 2)

	
	
	def move(self, direction):
		self.location = (self.location[X]+DC[direction][X],self.location[Y]+DC[direction][Y])
			

	


