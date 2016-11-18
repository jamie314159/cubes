#!/bin/ipython3

# Constants ---------------------------------------------------

# Direction deffinitions
CW = 1
CCW = -1

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
DC = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

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
	for n in range(num):
		orientation = (orientation + direction) % 8
	return orientation

class Square(object):
	def __init__(self, x = -1, y = -1):
			# self.fill = "grey"
			#self.master = master
			self.connections = {}
			self.orientation = N
			self.adjNum = 0
			self.pivots = 0

                         self.coord = parent.coord + parentDir
                        
                        self.connections[opposite(parentDir)] = parent
                        parent.connections[parentDir] = self

                        self.getConnections()

                        squaresCoords[self.coord] = self
                        squaresList.append(self)
                        for s in self.connections.keys():
                                self.connections[s].getConnections()
			
	# Gets the direcetions from self which have squares
	def getConnections(self):
		self.connections = {}
		self.adjNum = 0
		for d in DB:
			c = self.coord + d # (self.coord[X]+DC[d][X], self.coord[Y]+DC[d][Y])
			if c in squaresCoords.keys():
				self.connections[d] = squaresCoords[c]
				squaresCoords[c].connections[opposite(d)] = self
				if d in DA:
					self.adjNum += 1

	# Pivot self in given direction
	def getPivot(self, direction):
		self.getConnections()
		pivot = -1
		# Get "pivot", the diriection from the target square to the adjacent square on which the target square pivots ----------------------
		for d in DA:
			if d in self.connections.keys():
				pivot = d
		if pivot >= 0:
			t = clock(pivot, -direction, 2)
			if t in self.connections.keys():
				pivot = t
				t = clock(pivot, -direction, 2)
			# -----------------------------------------------------------------------------------------

			# Is there a square adjacent to the pivot square
			if opposite(pivot) not in self.connections.keys():
				# Space adjacent to the target square in the direction that it will pivot
				temp = self.coord + t
				if (temp + opposite(pivot)) not in squaresCoords:
					if (temp + pivot) in squaresCoords or (temp + t) in squaresCoords:
						return((self.coord + t, 2))
					else:
						if temp + clock(pivot, -direction) not in squaresCoords:
							return ((self.coord + clock(pivot, -direction), 4))
		return 0


	# Pivot self in given direction
	def pivot(self, direction = 0, p = 0):
		if p == 0:
			p = self.getPivot(direction)
		if p:
			if self.move(p[0]):
				self.orientation = clock(self.orientation, direction, p[1])
				self.pivots += 1
				return 1
			

	# -- Make this private -- #
	# Move self to (x,y)
	# 	Does not allow any squares to become disconnected from group
	# 	Does not allow square to move ontop of another
	def move(self, newCoord):
		fail = 0
		oldCoord = self.coord
		conns = []

		if newCoord not in squaresCoords.keys():
			del squaresCoords[self.coord]
			self.coord = newCoord
			squaresCoords[self.coord] = self
			for s in squaresList:
				s.getConnections()
			return 1
		else:
			return 0
			

	


