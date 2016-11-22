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

# pivotCheckTable = [[[(x1,y1+1),(x2,y2+1),(x2,y2)],[(x1+1,y1),(x2+1,y2),(x2,y2)]],
# 				   	   [[(x1-1,y1),(x2-1,y2),(x2,y2)],[(x1,y1+1),(x2,y2+1),(x2,y2)]],
# 				   	   [[(x1,y1-1),(x2,y2-1),(x2,y2)],[(x1-1,y1),(x2-1,y2),(x2,y2)]],
# 				   	   [[(x1+1,y1),(x2+1,y2),(x2,y2)],[(x1,y1-1),(x2,y2-1),(x2,y2)]]]

pivotCheckTable = [[[(0,1),(0,1),(0,0)],[(1,0),(1,0),(0,0)]],
			   	   [[(-1,0),(-1,0),(0,0)],[(0,1),(0,1),(0,0)]],
			   	   [[(0,-1),(0,-1),(0,0)],[(-1,0),(-1,0),(0,0)]],
			   	   [[(1,0),(1,0),(0,0)],[(0,-1),(0,-1),(0,0)]]]

squaresList = []


# Functions, Procedures, Classes & Methods --------------------------------------------------------

class coordinate(tuple):
	def __add__(self, direction):
		return coordinate((self[X] + DC[direction][X], self[Y] + DC[direction][Y]))

# Returns opposite direction of orientation
def opposite(orientation):
	return((orientation+4)%8)

# Increments orientation in direction by 45 degrees num times
def clock(orientation, direction, num = 1):
	d = (1 if direction == CW else -1)
	for n in range(num):
		orientation = (orientation + d) % 8
	return orientation

def squareAt(coord):
	r = False
	for square in squaresList:
		if square.location == coord:
			r = True
			continue
	return r


def moveResult(location, direction):
	return (location[X]+DC[direction][X],location[Y]+DC[direction][Y])

def pivotResult(location, corner, direction):
	return moveResult(location, pivotTable[corner][direction])
	

def canPivot(location, corner, direction):
	x1 = location[X]
	y1 = location[Y]
	pivotLocation = pivotResult(location,corner,direction)
	x2 = pivotLocation[X]
	y2 = pivotLocation[Y]
	
	# Get the locations where squares whould interfere with this pivot	# 
	# Get list off ofsets from pre computed table
	cl = pivotCheckTable[corner][direction]
	# Add offsets to coordinates to find list of coordinates to check
	checkList = [(x1+cl[0][0],y1+cl[0][1]),(x2+cl[1][0],y2+cl[1][1]),(x2+cl[2][0],y2+cl[2][1])]
	
	# Check interfering locations
	for coord in checkList:
		if squareAt(coord):
			return False
	
	return True



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
		if canPivot(self.location,corner,direction):
			pivotLocation = pivotResult(self.location, corner, direction)
			adjecentList = [squareAt((pivotLocation[X]+DC[d][X],pivotLocation[Y]+DC[d][Y])) for d in DA if (pivotLocation[X]+DC[d][X],pivotLocation[Y]+DC[d][Y]) != self.location]
			diagonalList = [squareAt((pivotLocation[X]+DC[d+1][X],pivotLocation[Y]+DC[d+1][Y])) for d in DA if (pivotLocation[X]+DC[d+1][X],pivotLocation[Y]+DC[d+1][Y]) != self.location]
			if True not in adjecentList:
				if True in diagonalList:
					# Check if we can pivot 90 degrees further to reach another square
					pCorner = (corner+1)%4 if direction == CW else (corner-1)%4
					if canPivot(pivotLocation, pCorner, direction):
						self.move(pivotTable[corner][direction])
						self.rotate(direction)
						self.move(pivotTable[pCorner][direction])
						self.rotate(direction)
						return
			else:
				self.move(pivotTable[corner][direction])
				self.rotate(direction)


		

	def rotate(self, direction):
		self.orientation = clock(self.orientation, direction, 2)

	
	
	def move(self, direction):
		self.location = (self.location[X]+DC[direction][X],self.location[Y]+DC[direction][Y])
			

	


