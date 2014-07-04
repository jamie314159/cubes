#!/usr/local/bin/ipython3

from tkinter import *
from tkinter import ttk
import colorsys
import cubes
import random

# Size of window
SIZE = 512
# Size of squares
SCALE = 16

# Derived info about window and grid
GSIZE = int(SIZE/SCALE)-1
GCENTER = int(GSIZE/2)
X_SCALE = SCALE
Y_SCALE = SCALE

DRAW = 1
# Display grid points
GRID = 1
# Width of grid points
DASHWIDTH = 2

CW = 1
CCW = -1
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

OUTLINE = "black"
FILL = "tan"

# -1: No internal lines; 0: lines pointing in direction of orientation; 1: lines indicating connections
LINES = -1
# Include diagonal connections
DIAGONALS = 0

drawings = {}
changed = []
squares = []
# # Draw self
# def draw(self):
# 	self.erase()
# 	x1 = ((self.x+1)*SCALE)
# 	y1 = ((self.y+1)*SCALE)
# 	x2 = ((self.x+1)*SCALE)+SCALE
# 	y2 = ((self.y+1)*SCALE)+SCALE
# 	self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline = self.outline, fill = self.fill, width=2)
# 	canvas.tag_bind(self.drawing, '<Button-3>', self.rClick)
# 	canvas.tag_bind(self.drawing, '<Button-1>', self.lClick)
# 	canvas.tag_bind(self.drawing, '<Button-2>', self.drawPath)
	
# 	if LINES == 1:
# 		if DIAGONALS:
# 			l = DB
# 		else:
# 			l = DA
# 		for c in l:
# 			if self.connections[c] != 0:
# 				x1 = SCALE*(self.x+1.5)
# 				y1 = SCALE*(self.y+1.5)
# 				x2 = SCALE*((self.x+1.5)+(.5*DC[c][0]))
# 				y2 = SCALE*((self.y+1.5)+(.5*DC[c][1]))
# 				self.connLines[c] = canvas.create_line(x1, y1, x2, y2)
# 				canvas.tag_bind(self.connLines[c], '<Button-3>', self.rClick)
# 				canvas.tag_bind(self.connLines[c], '<Button-1>', self.lClick)
# 				canvas.tag_bind(self.connLines[c], '<Button-2>', self.drawPath)
# 	elif LINES == 0:
# 		x1 = SCALE*(self.x+1.5)
# 		y1 = SCALE*(self.y+1.5)
# 		x2 = SCALE*((self.x+1.5)+(.5*DC[self.orientation][0]))
# 		y2 = SCALE*((self.y+1.5)+(.5*DC[self.orientation][1]))
# 		self.dirLine = canvas.create_line(x1, y1, x2, y2)
# 		canvas.tag_bind(self.dirLine, '<Button-3>', self.rClick)
# 		canvas.tag_bind(self.dirLine, '<Button-1>', self.lClick)
# 		canvas.tag_bind(self.dirLine, '<Button-2>', self.drawPath)
# 	root.update()

# # Erase self
# def erase(self):
# 	if(self.drawing):
# 		canvas.delete(self.drawing)
# 		self.drawing = 0
# 	if LINES:
# 		for l in self.connLines:
# 			canvas.delete(l)
# 			l = 0
# 	if(self.dirLine):
# 		canvas.delete(self.dirLine)
# 	root.update()


# # Find the shortest path between two squares



# def colorPathDists():
# 	maxDist = 0
# 	for s in squaresList:
# 		s.getConnected()
# 		if s.distance > maxDist:
# 			maxDist = s.distance
# 	for s in squaresList:
# 		r, g, b = colorsys.hls_to_rgb(s.distance / maxDist, .5, .5)
# 		s.fill = '#' + '%02x%02x%02x' % (int(r*256%255), int(g*256%255), int(b*256%255))
# 		s.draw()

# def drawPath(event = None, start = 0, goal = 0):
# 	for s in squaresList:
# 		s.fill = FILL
# 		s.draw()
# 	if start == 0:
# 		start = random.choice(squaresList)
# 	if goal == 0:
# 		goal = MASTER
# 	p = shortestPath(start, goal)
# 	l = len(p)
# 	distance = 0
# 	for s in p:
# 		r, g, b = colorsys.hls_to_rgb(distance / l, .5, .5)
# 		# r, g, b = hex(int(256*r)), hex(int(256*g)), hex(int(256*b))
# 		s.fill = '#' + '%02x%02x%02x' % (int(r*256%255), int(g*256%255), int(b*256%255))
# 		# print(s.fill)
# 		distance += 1
# 		s.draw()


# # Pivot a random square in a random location
# def randPivot(event = None):
# 	n = 0
# 	shuffled = list(squaresList)
# 	random.shuffle(shuffled)
# 	for s in shuffled:
# 		d = random.choice([CW, CCW])
# 		n = s.pivot(d)
# 		if n:
# 			return n
								

def randLine():
	m = randNewSquareFast()
	s = 0
	for c in m.connections:
		if c != 0:
			s += 1
	while s > 2:
		m.delete()
		m = randNewSquareFast()
		s = 0
		for c in m.connections:
			if c != 0:
				s += 1
	return m

# Create a new square in a random location
# 	Favors spread and long paths
def randNewSquare(event = None):
	opens = []
	picks = {0:[], 1:[], 2:[], 3:[]}
	shuffled = list(squares)
	random.shuffle(shuffled)
	for n in (0,1,2,3):
		[picks[n].append(q) for q in shuffled if q.adjNum == n]
	while(len(squares) < GSIZE*GSIZE):
		for n in (0,1,2,3):
			if picks[n]:
				for s in picks[n]:
					opens = []
					for d in DA:
						if s.connections[d] == 0:
							opens.append(d)
					random.shuffle(opens)
					for d in opens:
						m = cubes.Square(s, d)
						if m:
							return m

def drawSquare(square):
	drawing = []
	x1 = ((square.coord[X]+GCENTER+1)*SCALE)
	y1 = ((-square.coord[Y]+GCENTER+1)*SCALE)
	x2 = ((square.coord[X]+GCENTER+1)*SCALE)+SCALE
	y2 = ((-square.coord[Y]+GCENTER+1)*SCALE)+SCALE
	drawing.append(canvas.create_rectangle(x1, y1, x2, y2,  fill = FILL, outline = OUTLINE, width=2))
	for d in DA:
		if d in square.connections.keys():
			x1 = SCALE*(square.coord[X]+GCENTER+1.5)
			y1 = SCALE*(-square.coord[Y]+GCENTER+1.5)
			x2 = SCALE*((square.coord[X]+GCENTER+1.5)+(.5*DC[d][0]))
			y2 = SCALE*((-square.coord[Y]+GCENTER+1.5)+(.5*DC[d][1]))
			drawing.append(canvas.create_line(x1, y1, x2, y2))
	for d in drawing:
		canvas.tag_bind(d, '<Button-3>', lambda event, arg=square: rClick(event, arg))
		canvas.tag_bind(d, '<Button-1>', lambda event, arg=square: lClick(event, arg))
	drawings[square] = drawing
	root.update()


		

def printSquares():
	for y in range(GCENTER,-GCENTER, -1):
		for x in range(-GCENTER,GCENTER):
			if (x, y) not in cubes.squaresCoords.keys():
				print('-', end = ' ')
			else:
				s = cubes.squaresCoords[(x, y)]
				n = 0
				for c in DA:
					if c in s.connections.keys():
						n += 1
				if cubes.squaresCoords[(x, y)].master:
					print(n, end = '!')
				else:
					print(n, end = ' ')

				# if n == 1:
				# 	print('- ', end = '')
				# if n == 2:
				# 	print('= ', end = '')
				# if n == 3:
				# 	print('% ', end = '')
				# if n == 4:
				# 	print('+ ', end = '')
		print('')
	print('')

# Create a new square in a random location
def randNewSquareFast():
	shuffledSquares = list(squares)
	random.shuffle(shuffledSquares)
	for s in shuffledSquares:
		if s:
			if s.adjNum < 4:
				parent = s
				break

	shuffledDirs = list(DA)
	random.shuffle(shuffledDirs)
	
	for d in shuffledDirs:
		if d not in parent.connections.keys():
			parentDir = d
			break

	return cubes.Square(parent, parentDir)

def mClick(event):
	new = randNewSquareFast()
	squares.append(new)
	drawSquare(new)
	for s in new.connections.values():
		drawSquare(s)

def lClick(event, square):
	square.pivot(CCW)
	redraw()

def rClick(event, square):
	square.pivot(CW)
	redraw()


def redraw():
	canvas.delete("all")
	for s in squares:
		drawSquare(s)



# Initialize tkinter ------------------------------------------

if DRAW:
	root = Tk()
	root.minsize(SIZE, SIZE)
	root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

	canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
	canvas.place(relx=.5, rely=.5, anchor=CENTER)
	canvas.bind('<Button-2>', mClick)

	# Draw Grid ---------------------------------------------------

	if(GRID):
		i=SCALE
		while(i <= SIZE):
			canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=(DASHWIDTH, SCALE-DASHWIDTH), width=DASHWIDTH)
			i += SCALE

# -------------------------------------------------------------


m = cubes.Square(master = 1)
squares.append(m)

e = cubes.Square(m, E)
squares.append(e)

n = cubes.Square(m, N)
squares.append(n)


# n.delete()

# drawSquare(m)

while len(squares) < 50:
	new = randNewSquareFast()
	squares.append(new)



if DRAW:	
	for s in squares:
		drawSquare(s)
	root.mainloop()