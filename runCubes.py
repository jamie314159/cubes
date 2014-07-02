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

# Display grid points
GRID = 1
# Width of grid points
DASHWIDTH = 2

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
	x1 = ((square.x+1)*SCALE)
	y1 = ((square.y+1)*SCALE)
	x2 = ((square.x+1)*SCALE)+SCALE
	y2 = ((square.y+1)*SCALE)+SCALE
	canvas.create_rectangle(x1, y1, x2, y2,  fill = FILL, outline = OUTLINE, width=2)
	root.update()

# Create a new square in a random location
def randNewSquareFast():
	opens = []
	n = 0
	while not n:
		opens = []
		s = random.choice(squares)
		[opens.append(d) for d in DA if s.connections[d] == 0]
		if len(opens) != 0:
			d = random.choice(opens)
			n = cubes.Square(s, d)
			if n:
				return n
			else:
				opens.remove(d)

def printSquares():
	for y in range(0,GSIZE):
		for x in range(0,GSIZE):
			if cubes.squaresCoords[x][y] == 0:
				print('- ', end = '')
			else:
				if cubes.squaresCoords[x][y].master:
					print('# ', end = '')
				else:
					print('+ ', end = '')
		print('')
	print('')

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

squares = []
m = cubes.Square(master = 1)
squares.append(m)
# squares.append(cubes.Square(m, N))
# squares.append(cubes.Square(m, S))
# squares.append(cubes.Square(m, E))
# squares.append(cubes.Square(m, W))

for s in squares:
	drawSquare(s)

while len(squares) < 200:
	new = randLine()
	squares.append(new)
	drawSquare(new)

printSquares()





root.mainloop()