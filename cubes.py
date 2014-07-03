#!/bin/ipython3
import random
import math
import time

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

# Functions, Procedures, Classes & Methods -----------------------------------------------------

# Should this be an object method?
def shortestPath(start, goal):
	def reconstruct_path(navigated, current):
		if current in navigated:
			p = reconstruct_path(navigated, navigated[current])
			return p + [current]
		else:
			return [current]

	def hc_est(start, goal):
		a = abs(start.x - goal.x)
		b = abs(start.y - goal.y)
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
		for neighbor in current.adjacent:
			if neighbor and neighbor not in closedset:
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
			x = parent.x + DC[parentDir][X]
			y = parent.y + DC[parentDir][Y]
			if (x, y) not in squaresCoords.keys():
				if(master or parentDir not in parent.connections.keys()):
					return object.__new__(cls)
					


	def __init__(self, parent = 0, parentDir = 0, master = 0, x = -1, y = -1):
			self.master = master
			self.connections = {}
			self.adjacent = [0,0,0,0,0,0,0,0]
			self.connLines = [0,0,0,0,0,0,0,0]
			self.orientation = N
			self.adjNum = 0

			if self.master:
				global MASTER 
				MASTER = self
				self.x = 0
				self.y = 0
				squaresList.append(self)
				# squaresCoords[self.x][self.y] = self
				squaresCoords[(self.x, self.y)] = self
				self.getConnections()
				self.getConnected()
			else:
				self.x = parent.x + DC[parentDir][X]
				self.y = parent.y + DC[parentDir][Y]

				self.connections[opposite(parentDir)] = parent
				parent.connections[parentDir] = self

				self.getConnections()
				self.getConnected()

				# squaresCoords[self.x][self.y] = self
				squaresCoords[(self.x, self.y)] = self
				squaresList.append(self)
				for s in self.connections.keys():
					self.connections[s].getConnections()
			
	def getConnections(self):
		self.adjNum = 0
		for d in DB:
			c = (self.x+DC[d][X], self.y+DC[d][Y])
			if c in squaresCoords.keys():
				self.connections[d] = squaresCoords[c]
				squaresCoords[c].connections[opposite(d)] = self
				if d in DA:
					self.adjNum += 1



	

	# Gets the direcetions from self which have squares
	# def getConnections(self):
	# 	self.connections = [0,0,0,0,0,0,0,0]
	# 	for d in DB:
	# 		adjCoord = (self.x+DC[d][X], self.y+DC[d][Y])
	# 		if(adjCoord[X] >= 0 and adjCoord[Y] >= 0 and adjCoord[X] < GSIZE and adjCoord[Y] < GSIZE):
	# 			adjSquare = squaresCoords[adjCoord[X]][adjCoord[Y]]
	# 			if adjSquare:
	# 				self.connections[d] = adjSquare
	# 	for i in range(0, 7, 2):
	# 		self.adjacent[i] = self.connections[i]

	# 	self.adjNum = 0
	# 	for s in self.adjacent:
	# 		if s:
	# 			self.adjNum += 1

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
		for d in DA:
			if self.connections[d]:
				pivot = d

		t = clock(pivot, -direction, 2)
		if self.connections[t]:
			pivot = t
			t = clock(pivot, -direction, 2)

		# if self.connections[opposite(pivot)] or self.connections[clock(opposite(pivot), direction)]:
		# 	return 0
		# else:
		temp = Square(self, t)
		

		if temp:
			if temp.connections[pivot]:
				temp.delete()
				self.orientation = clock(self.orientation, direction, 2)
				if self.move(self.x + DC[t][X], self.y + DC[t][Y]):
					return 1
				else:
					self.orientation = clock(self.orientation, -direction, 2)
			else:
				if temp.connections[t]:
					temp.delete()
					self.orientation = clock(self.orientation, direction, 2)
					if self.move(self.x + DC[t][X], self.y + DC[t][Y]):
						return 1
					else:
						self.orientation = clock(self.orientation, -direction, 2)
				else:
					t = clock(pivot, -direction)
					if not temp.connections[t]:
						temp.delete()
						self.orientation = clock(self.orientation, direction, 4)
						if self.move(self.x + DC[t][X], self.y + DC[t][Y]):
							return 1
						else:
							self.orientation = clock(self.orientation, -direction, 4)
			temp.delete()
		return 0

	# -- Make this private -- #
	# Move self to (x,y)
	# 	Does not allow any squares to become disconnected from group
	# 	Does not allow square to move ontop of another
	def move(self, x, y):
		fail = 0
		oldx = self.x
		oldy = self.y
		conns = []

		if squaresCoords[x][y] == 0:
			
			squaresCoords[self.x][self.y] = 0
			self.x = x
			self.y = y
			squaresCoords[self.x][self.y] = self

			# Gets all potentialy affected squares, hopefully
			[conns.append(s) for s in squaresList if self in s.path]

			for s in squaresList:
				if s:
					s.getConnections()
					s.getConnected()
					if not s.connected:
						fail = 1
						break


			if fail:
				squaresCoords[self.x][self.y] = 0
				self.x = oldx
				self.y = oldy
				squaresCoords[self.x][self.y] = self
				for s in squaresList:
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
		conns = []
		[conns.append(s) for s in self.connections if s]
		squaresList.remove(self)
		squaresCoords[self.x][self.y] = 0
		self = 0
		for s in conns:
			s.getConnections()



	




