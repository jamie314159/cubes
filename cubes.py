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

# Size of window
SIZE = 512
# Size of squares
SCALE = 16

# Derived info about window and grid
GSIZE = int(SIZE/SCALE)-1
GCENTER = int(GSIZE/2)
X_SCALE = SCALE
Y_SCALE = SCALE

squaresList = []
# squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]
squaresCoords = {}

MASTER = 0

# Functions, Procedures, Classes & Methods --------------------------------------------------------

class coordinate(tuple):
	def __add__(self, direction):
		return coordinate((self[X] + DC[direction][X], self[Y] + DC[direction][Y]))

# Should this be an object method?
def shortestPath(start, goal):
	def reconstruct_path(navigated, current):
		if current in navigated:
			p = reconstruct_path(navigated, navigated[current])
			return p + [current]
		else:
			return [current]

	def hc_est(start, goal):
		a = abs(start.coord[X] - goal.coord[X])
		b = abs(start.coord[Y] - goal.coord[Y])
		return a+b

	def lowestF(oset):
		lowest = 0
		for s in oset:
			if lowest == 0:
				lowest = s
			elif f_score[s] < f_score[lowest]:
				lowest = s
		return lowest


	closedset = set([])
	openset = set([start])
	navigated = {}

	g_score = {}
	f_score = {}

	g_score[start] = 0
	f_score[start] = g_score[start] + hc_est(start, goal)



	while len(openset) != 0:
		current = lowestF(openset)
		
		if current == goal:
			return reconstruct_path(navigated, goal)
		
		openset.remove(current)
		closedset.add(current)
		for d in DA:
			if d in current.connections.keys():
				neighbor = current.connections[d]
				if neighbor not in closedset:
					tent_g_score = g_score[current] + 1
					if neighbor not in openset or tent_g_score < g_score[neighbor]:
						navigated[neighbor] = current
						g_score[neighbor] = tent_g_score
						f_score[neighbor] = g_score[neighbor] + hc_est(neighbor, goal)
						if neighbor not in openset:
							openset.add(neighbor)
	return 0

# Returns opposite direction of orientation
def opposite(orientation):
	return((orientation+4)%8)

# Increments orientation in direction num times
def clock(orientation, direction, num = 1):
	while num > 0:
		if direction == CW:
			if orientation == NW:
				orientation = N
			else:
				orientation = orientation+1
		elif direction == CCW:
			if orientation == N:
				orientation = NW
			else:
				orientation = orientation-1
		num -= 1
	return orientation


class Square(object):
	def __new__(cls, parent = 0, parentDir = 0, master = 0, x = -1, y = -1):
		if(master):
			return object.__new__(cls)
		elif(parent):
			coord = parent.coord + parentDir #(parent.coord[X] + DC[parentDir][X], parent.coord[Y] + DC[parentDir][Y])
			if coord not in squaresCoords.keys():
				if(master or parentDir not in parent.connections.keys()):
					return object.__new__(cls)
					


	def __init__(self, parent = 0, parentDir = 0, master = 0, x = -1, y = -1):
			self.fill = "grey"
			self.master = master
			self.connections = {}
			self.orientation = N
			self.adjNum = 0

			if self.master:
				global MASTER 
				MASTER = self
				self.coord = coordinate((0, 0))
				squaresList.append(self)
				squaresCoords[self.coord] = self
				self.getConnections()
				self.getConnected()
			else:
				self.coord = parent.coord + parentDir
				
				self.connections[opposite(parentDir)] = parent
				parent.connections[parentDir] = self

				self.getConnections()
				self.getConnected()

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



	
	# Finds if self is connected to the master square
	# 	Important for making sure squares stay connected in one group
	def getConnected(self):
		if self.master:
			self.path = [self]
			self.connected = 1
		else:
			path = shortestPath(self, MASTER)
			if path:
				self.path = path
				self.connected = 1
			else:
				self.path = 0
				self.connected = 0

	
	# Pivot self in given direction
	def pivot(self, direction):
		self.getConnections()

		# Get "pivot", the diriection from the target square to the adjacent square on which the target square pivots ----------------------
		for d in DA:
			if d in self.connections.keys():
				pivot = d

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
					if self.move(self.coord + t):
						self.orientation = clock(self.orientation, direction, 2)
						return 1
				else:
					if temp + clock(pivot, -direction) not in squaresCoords:
						if self.move(self.coord + clock(pivot, -direction)):
							self.orientation = clock(self.orientation, direction, 4)
							return 1
		return 0


	

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
				s.getConnected()
				if s.adjNum == 0:
					fail = 1
					break


			if fail:
				del squaresCoords[self.coord]
				self.coord = oldCoord
				squaresCoords[self.coord] = self
				for s in conns:
					if s:
						self.getConnections()
						s.getConnected()
				return 0
			else:
				return 1
		else:
			return 0
			
	

	# Delete self
	def delete(self):
		squaresList.remove(self)
		del squaresCoords[self.coord]
		conns = list(self.connections.values())
		self = 0
		for s in conns:
			s.getConnections()


	




