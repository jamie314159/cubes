#!/bin/ipython3

from tkinter import *
from tkinter import ttk
import random
import math
import time
import colorsys
# Constants ---------------------------------------------------

# Direction deffinitions
CW = 1
CCW = -1

# For easier reading when referenceing coordinates
X = 0
Y = 1

# Make this a dictionary
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

# Size of window
SIZE = 1024
# Size of squares
SCALE = 16

# Derived info about window and grid
GSIZE = int(SIZE/SCALE)-1
GCENTER = int(GSIZE/2)
X_SCALE = SCALE
Y_SCALE = SCALE

# Display grid points
GRID = 0
# Width of grid points
DASHWIDTH = 2





OUTLINE = "black"
FILL = "tan"

# -1: No internal lines; 0: lines pointing in direction of orientation; 1: lines indicating connections
LINES = -1
# Include diagonal connections
DIAGONALS = 0


squaresList = []
squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]

MASTER = 0

# Functions, Procedures, Classes & Methods -----------------------------------------------------

# Find the shortest path between two squares
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
		return math.sqrt(pow(a,2)+pow(b,2))	

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
			# print(navigated)
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


def colorPathDists():
	maxDist = 0
	for s in squaresList:
		s.getConnected()
		if s.distance > maxDist:
			maxDist = s.distance
	for s in squaresList:
		r, g, b = colorsys.hls_to_rgb(s.distance / maxDist, .5, .5)
		s.fill = '#' + '%02x%02x%02x' % (int(r*256%255), int(g*256%255), int(b*256%255))
		s.draw()

def drawPath(event = None, start = 0, goal = 0):
	for s in squaresList:
		s.fill = FILL
		s.draw()
	if start == 0:
		start = random.choice(squaresList)
	if goal == 0:
		goal = MASTER
	p = shortestPath(start, goal)
	l = len(p)
	distance = 0
	for s in p:
		r, g, b = colorsys.hls_to_rgb(distance / l, .5, .5)
		# r, g, b = hex(int(256*r)), hex(int(256*g)), hex(int(256*b))
		s.fill = '#' + '%02x%02x%02x' % (int(r*256%255), int(g*256%255), int(b*256%255))
		# print(s.fill)
		distance += 1
		s.draw()


# Pivot a random square in a random location
def randPivot(event = None):
	n = 0
	shuffled = list(squaresList)
	random.shuffle(shuffled)
	for s in shuffled:
		d = random.choice([CW, CCW])
		n = s.pivot(d)
		if n:
			return n
								
# Create a new square in a random location
# 	Favors spread and long paths
def randNewSquare(event = None):
	opens = []
	picks = {0:[], 1:[], 2:[], 3:[]}
	shuffled = list(squaresList)
	random.shuffle(shuffled)
	for n in (0,1,2,3):
		[picks[n].append(q) for q in shuffled if q.adjNum == n]
	while(len(squaresList) < GSIZE*GSIZE):
		for n in (0,1,2,3):
			if picks[n]:
				for s in picks[n]:
					opens = []
					for d in DA:
						if s.connections[d] == 0:
							opens.append(d)
					random.shuffle(opens)
					for d in opens:
						m = Square(s, d)
						if m:
							return m

# Create a new square in a random location
def randNewSquareFast():
	opens = []
	while len(opens) == 0:
		s = random.choice(squaresList)
		[opens.append(d) for d in DA if s.connections[d] == 0]
		if len(opens) != 0:
			d = random.choice(opens)
			n = Square(s, d)
			if n:
				return n
			else:
				opens.remove(d)
			
			

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
	def __new__(cls, parent, parent_dir, master = 0, x = -1, y = -1, outline = OUTLINE, fill = FILL, temp = 0):
		if(master):
			return object.__new__(cls)
		elif(parent):
			x = parent.x + DC[parent_dir][0]
			y = parent.y + DC[parent_dir][1]
			if(x >= 0 and y >= 0 and x < GSIZE and y < GSIZE):
				if squaresCoords[y][x] == 0:
					if(master or parent.connections[parent_dir] == 0):
						return object.__new__(cls)
					


	def __init__(self, parent, parent_dir, master = 0, x = -1, y = -1, outline = OUTLINE, fill = FILL, temp = 0):
			self.master = master
			self.temp = temp
			self.connections = [0,0,0,0,0,0,0,0]
			self.adjacent = [0,0,0,0,0,0,0,0]
			self.connLines = [0,0,0,0,0,0,0,0]
			self.outline = outline
			self.fill = fill
			self.drawing = None
			self.orientation = N
			self.dirLine = 0

			if(master == 1):
				if(x == -1):
					self.x = GCENTER
				else:
					self.x = x					

				if(y == -1):
					self.y = GCENTER
				else:
					self.y = y
					squaresList.append(self)
					squaresCoords[self.y][self.x] = self
				self.getConnections()
				self.connected = 1
				self.distance = 0
			else:
				self.x = parent.x + DC[parent_dir][0]
				self.y = parent.y + DC[parent_dir][1]
				self.getConnections()
				self.getConnected()
				if not temp:
					squaresCoords[self.y][self.x] = self
					squaresList.append(self)
			
			if not temp:
				if LINES:
					for s in self.connections:
						if s:
							s.getConnections()
							s.draw()

				self.draw()

	# Find shortest path from self to goal square
	def shortestPath(self, goal):
		def reconstruct_path(navigated, current):
			if current in navigated:
				p = reconstruct_path(navigated, navigated[current])
				return p + [current]
			else:
				return [current]

		def hc_est(self, goal):
			a = abs(self.x - goal.x)
			b = abs(self.y - goal.y)
			return math.sqrt(pow(a,2)+pow(b,2))	

		def lowestF(oset):
			lowest = 0
			for s in oset:
				if lowest == 0:
					lowest = s
				elif f_score[s] < f_score[lowest]:
					lowest = s
			return lowest


		closedset = set([])
		openset = set([self])
		navigated = {}

		g_score = {}
		f_score = {}

		g_score[self] = 0
		f_score[self] = g_score[self] + hc_est(self, goal)



		while len(openset) != 0:
			current = lowestF(openset)
			
			if current == goal:
				# print(navigated)
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

	# Gets the direcetions from self which have squares
	def getConnections(self):
		self.connections = [0,0,0,0,0,0,0,0]
		for d in DB:
			adjCoord = (self.x+DC[d][X], self.y+DC[d][Y])
			if(adjCoord[X] >= 0 and adjCoord[Y] >= 0 and adjCoord[X] < GSIZE and adjCoord[Y] < GSIZE):
				adjSquare = squaresCoords[adjCoord[Y]][adjCoord[X]]
				if adjSquare:
					self.connections[d] = adjSquare
		for i in range(0, 7, 2):
			self.adjacent[i] = self.connections[i]

		self.adjNum = 0
		for s in self.adjacent:
			if s:
				self.adjNum += 1

	# Finds if self is connected to the master square
	# 	Important for making sure squares stay connected in one group
	# 	Also gets the distance from self to the master square
	def getConnected(self):
		self.connected = 0
		path = self.shortestPath(MASTER)
		if path:
			self.distance = len(path)
			self.connected = 1
			
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

		if self.connections[opposite(pivot)] or self.connections[clock(opposite(pivot), direction)]:
			return 0
		else:
			temp = Square(self, t, temp = 1)
		

		if temp:
			if temp.connections[pivot]:
				temp.delete()
				self.orientation = clock(self.orientation, direction, 2)
				if self.move(self.x + DC[t][X], self.y + DC[t][Y]):
					return 1
				else:
					self.orientation = clock(self.orientation, -direction, 2)
			else:
				# Dont know if I want this
				#	Allows connection to square in pivot path not connected to pivot square
				if temp.connections[t]:
					pass
					# temp.delete()
					# self.orientation = clock(self.orientation, direction, 2)
					# if self.move(self.x + DC[t][X], self.y + DC[t][Y]):
					# 	return 1
					# else:
					# 	self.orientation = clock(self.orientation, -direction, 2)
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

	# Action for right click		
	def rClick(self, event):
		self.pivot(CW)

	# Action for left click
	def lClick(self, event):
		self.pivot(CCW)

	# Move self to (x,y)
	# 	Does not allow any squares to become disconnected from group
	# 	Does not allow square to move ontop of another
	def move(self, x, y):
		fail = 0
		oldx = self.x
		oldy = self.y
		conns = []
		self.getConnections()
		
		[conns.append(s) for s in self.connections if s]
		squaresCoords[self.y][self.x] = 0
		self.x = x
		self.y = y
		squaresCoords[self.y][self.x] = self
		self.getConnections()
		self.getConnected()
		[conns.append(s) for s in self.connections if s]

		if not self.connected:
			fail = 1

		for s in squaresList:
			if s:
				s.getConnections()
				s.getConnected()
				if not s.connected:
					fail = 1		

		if fail:
			squaresCoords[self.y][self.x] = 0
			self.x = oldx
			self.y = oldy
			squaresCoords[self.y][self.x] = self
			self.getConnections()
			self.getConnected()
			for s in squaresList:
				if s:
					self.getConnections()
					s.getConnected()
			return 0
		else:
			self.draw()
			if LINES:
				for s in conns:
					if s:
						s.draw()
			return 1
			
	# Draw Path from self to master
	def drawPath(self, event):
		drawPath(event, start = self)

	# Draw self
	def draw(self):
		self.erase()
		x1 = ((self.x+1)*SCALE)
		y1 = ((self.y+1)*SCALE)
		x2 = ((self.x+1)*SCALE)+SCALE
		y2 = ((self.y+1)*SCALE)+SCALE
		self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline = self.outline, fill = self.fill, width=2)
		canvas.tag_bind(self.drawing, '<Button-3>', self.rClick)
		canvas.tag_bind(self.drawing, '<Button-1>', self.lClick)
		canvas.tag_bind(self.drawing, '<Button-2>', self.drawPath)
		
		if LINES == 1:
			if DIAGONALS:
				l = DB
			else:
				l = DA
			for c in l:
				if self.connections[c] != 0:
					x1 = SCALE*(self.x+1.5)
					y1 = SCALE*(self.y+1.5)
					x2 = SCALE*((self.x+1.5)+(.5*DC[c][0]))
					y2 = SCALE*((self.y+1.5)+(.5*DC[c][1]))
					self.connLines[c] = canvas.create_line(x1, y1, x2, y2)
					canvas.tag_bind(self.connLines[c], '<Button-3>', self.rClick)
					canvas.tag_bind(self.connLines[c], '<Button-1>', self.lClick)
					canvas.tag_bind(self.connLines[c], '<Button-2>', self.drawPath)
		elif LINES == 0:
			x1 = SCALE*(self.x+1.5)
			y1 = SCALE*(self.y+1.5)
			x2 = SCALE*((self.x+1.5)+(.5*DC[self.orientation][0]))
			y2 = SCALE*((self.y+1.5)+(.5*DC[self.orientation][1]))
			self.dirLine = canvas.create_line(x1, y1, x2, y2)
			canvas.tag_bind(self.dirLine, '<Button-3>', self.rClick)
			canvas.tag_bind(self.dirLine, '<Button-1>', self.lClick)
			canvas.tag_bind(self.dirLine, '<Button-2>', self.drawPath)
		root.update()

	# Erase self
	def erase(self):
		if(self.drawing):
			canvas.delete(self.drawing)
			self.drawing = 0
		if LINES:
			for l in self.connLines:
				canvas.delete(l)
				l = 0
		if(self.dirLine):
			canvas.delete(self.dirLine)
		root.update()

	# Delete self
	def delete(self):
		self.erase()
		conns = []
		[conns.append(s) for s in self.connections if s]
		if not self.temp:
			squaresList.remove(self)
			squaresCoords[self.y][self.x] = 0
		self = 0
		for s in conns:
			s.getConnections()
			s.erase()
			s.draw()


if __name__ == "__main__":
	# Initialize tkinter ------------------------------------------

	root = Tk()
	root.minsize(SIZE, SIZE)
	root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

	canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
	canvas.place(relx=.5, rely=.5, anchor=CENTER)
	# canvas.bind('<Button-2>', randPivot)

	# Draw Grid ---------------------------------------------------

	if(GRID):
		i=SCALE
		while(i <= SIZE):
			canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=(DASHWIDTH, SCALE-DASHWIDTH), width=DASHWIDTH)
			i += SCALE

	# -------------------------------------------------------------



	MASTER = Square(0, 0, master=1, x = GCENTER, y = GCENTER)
	n = Square(MASTER, S)
	m = Square(n, W)

	# for i in range(5, GSIZE-10):
	# 	n = Square(n, E)

	# n = Square(MASTER, E)
	# for i in range(5, GSIZE-3):
	# 	n = Square(n, E)
	while len(squaresList) < 300:
		n = randNewSquare()

	# for i in range(0,100):
	# 	MASTER = Square(0, 0, master=1, x = GCENTER, y = GCENTER)
	# 	while len(squaresList) < 300:
	# 		n = randNewSquare()
		
	# 	colorPathDists()
	# 	while len(squaresList) > 0:
	# 		for s in squaresList:
	# 			s.delete()


	# while(1):
	# # # 	# drawPath()
	# 	randPivot()
	# 	time.sleep(.1)
		# s = random.choice(squaresList)
		# d = random.choice(DA)
		# n = Square(s, d)

	# [s.draw() for s in squaresList]
	# n.pivot(CW)

	# n.pivot(1)
	# [s.pivot(1) for s in squaresList]

	# print(squaresCoords)
	root.mainloop()

