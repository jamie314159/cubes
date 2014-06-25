from tkinter import *
from tkinter import ttk
import random

# Constants ---------------------------------------------------

SIZE = 512
SCALE = 16
GSIZE = int(SIZE/SCALE)-1
GCENTER = int(GSIZE/2)
X_SCALE = SCALE
Y_SCALE = SCALE
relX_SCALE = 1
relY_SCALE = 1
DELAY = 0

GRID = 1
DASHWIDTH = 2
DASH = (DASHWIDTH, SCALE-DASHWIDTH)

OUTLINE = "black"
FILL = "tan"

CW = 1
CCW = -1

X = 0
Y = 1

N 	= 0
NE 	= 1
E 	= 2
SE 	= 3
S 	= 4
SW 	= 5
W 	= 6
NW 	= 7

DA = [N,E,S,W]
DB = [N,NE,E,SE,S,SW,W,NW]
DC = [(0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1)]

squaresList = []
squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]

# Functions, Procedures, Classes & Methods -----------------------------------------------------

def randSquare(event):
	ods = []
	s = random.choice(squaresList)
	while len(ods) == 0:
		s = random.choice(squaresList)
		for d in DA:
			if s.connections[d] == 0:
				ods.append(d)
	d = random.choice(ods)
	n = Square(s, d)

def opposite(d):
	return((d+4)%8)

def clock(d, direction):
	if direction == CW:
		if d == NW:
			return N
		return d+1
	return d-1

def clicked(event):
	print("test")

class Square(object):
	def __new__(cls, parent, parent_dir, master = 0, x = -1, y = -1, outline = OUTLINE, fill = FILL):
		if(master):
			return object.__new__(cls)
		elif(parent):
			x = parent.x + DC[parent_dir][0]
			y = parent.y + DC[parent_dir][1]
			if(x >= 0 and y >= 0 and x < GSIZE and y < GSIZE):
				if squaresCoords[y][x] == 0:
					if(master or parent.connections[parent_dir] == 0):
						return object.__new__(cls)
					


	def __init__(self, parent, parent_dir, master = 0, x = -1, y = -1, outline = OUTLINE, fill = FILL):
			self.master = master
			self.connections = [0,0,0,0,0,0,0,0]
			self.connLines = [0,0,0,0,0,0,0,0]
			# self.connNum = 0

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
			else:
				self.x = parent.x + DC[parent_dir][0]
				self.y = parent.y + DC[parent_dir][1]
				squaresList.append(self)
				squaresCoords[self.y][self.x] = self
			
			self.getConnections()
			for s in self.connections:
				if s:
					s.getConnections()
					s.draw()

			

			self.outline = outline
			self.fill = fill
			self.drawing = None

			self.draw()

	def getConnections(self):
		self.connections = [0,0,0,0,0,0,0,0]
		for d in DB:
			adjCoord = (self.x+DC[d][X], self.y+DC[d][Y])
			if(adjCoord[X] >= 0 and adjCoord[Y] >= 0 and adjCoord[X] < GSIZE and adjCoord[Y] < GSIZE):
				adjSquare = squaresCoords[adjCoord[Y]][adjCoord[X]]
				if adjSquare:
					self.connections[d] = adjSquare
					# self.connNum += 1
					# adjSquare.connections[opposite(d)] = self
					# adjSquare.connNum += 1
		# print(self.connections)

	def getPivot(self, direction):
		connlist = []
		[connlist.append(d) for d in self.connections if d]		
		if len(connlist) == 1:
			return connlist[0]
		elif len(connlist) == 2:
			if self.connections[N] in connlist:
				if self.connections[E] in connlist:
					if direction == CW:
						return self.connections[N]
					if direction == CCW:
						return self.connections[E]
				if self.connections[W] in connlist:
					if direction == CW:
						return self.connections[W]
					if direction == CCW:
						return self.connections[N]
			elif self.connections[S] in connlist:
				if self.connections[E] in connlist:
					if direction == CW:
						return self.connections[E]
					if direction == CCW:
						return self.connections[S]
				if self.connections[W] in connlist:
					if direction == CW:
						return self.connections[S]
					if direction == CCW:
						return self.connections[E]
		return 0

	def move(self, x, y):
		self.erase()
		# self.connNum = 0
		squaresList.remove(self)
		for l in squaresCoords:
			if self in l:
				l.remove(self)
		squaresCoords[y][x] = 0

		self.x = x
		self.y = y
		
		squaresList.append(self)
		squaresCoords[self.y][self.x] = self
		self.getConnections()
		self.draw()
		for s in self.connections:
			if s:
				s.erase()
				s.getConnections()
				s.draw()
		

	def pivot(self, direction = CW):
		pivot = self.getPivot(direction)
		# print(pivot)
		if(pivot):
			for d in DA:
				if self.connections[d] == pivot:
					pDir = d
			# print(pDir)
			# print(self.connections[pDir])
			x = self.x
			y = self.y
			while squaresCoords[y][x]:
				x = x + DC[pDir][X]
				y = y + DC[pDir][Y]
				pDir = clock(pDir, -direction)
			pDir = clock(pDir, direction)
			
			self.move(x, y)
						
			# for d in DA:
			# 	if self.connections[d] == s:
			# 		sd = d
			# if s.connections[clock(opposite(sd), direction)] == 0:
			# 	test = Square(s, clock(opposite(sd), direction))
			# else:
			# 	s = s.connections[clock(opposite(sd), direction)]
			# 	sd = clock(opposite(sd), direction)
			# 	if s.connections[clock(opposite(sd), direction)] == 0:
			# 		test = Square(s, clock(opposite(sd), direction))
			# if test:
			# 	if test.connNum < 3:
			# 		if(((test.connections[N] and test.connections[S]) == 0) and ((test.connections[E] and test.connections[W]) == 0)):
			# 			# old = self
			# 			# self = test
			# 			# old.erase()

			# 			# self.getConnections()
			# 			# self.delete()

			# 			self.erase()
			# 			squaresList.remove(self)
			# 			squaresCoords[self.y].remove(self)
			# 			squaresCoords[self.y][self.x] = 0
			# 			print('\n')
			# 			for s in squaresCoords:
			# 				print(s)

			# 			test.getConnections()
			# 			test.draw()

			# 			for c in self.connections:
			# 				if(c and c != self and c != test):
			# 					c.fill = "blue"
			# 					c.getConnections()
			# 					c.draw()
					
			# 			for c in test.connections:
			# 				if(c and c != self and c != test):
			# 					c.fill = "grey"
			# 					c.getConnections()
			# 					c.draw()
					


					# self.erase()
					# self.x = test.x
					# self.y = test.y

					# self.outline = test.outline
					# self.fill = test.fill
					# squaresCoords.remove(self)
					# self.getConnections()
					# for c in self.connections:
					# 	if(c):
					# 		c.getConnections()
					# 		c.draw()
					# self.draw()


			# test.delete()

		
	def clicked(self, event):
		# self.pivot(CW)
		self.delete()
		# self.erase()
		# print(self.connections)

	def draw(self):
		self.erase()
		x1 = ((self.x+1)*SCALE)
		y1 = ((self.y+1)*SCALE)
		x2 = ((self.x+1)*SCALE)+SCALE
		y2 = ((self.y+1)*SCALE)+SCALE
		self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline = self.outline, fill = self.fill, width=2)
		canvas.tag_bind(self.drawing, '<ButtonPress>', self.clicked)
		for c in DB:
			if self.connections[c] != 0:
				x1 = SCALE*(self.x+1.5)
				y1 = SCALE*(self.y+1.5)
				x2 = SCALE*((self.x+1.5)+(.5*DC[c][0]))
				y2 = SCALE*((self.y+1.5)+(.5*DC[c][1]))
				self.connLines[c] = canvas.create_line(x1, y1, x2, y2)
				canvas.tag_bind(self.connLines[c], '<ButtonPress>', self.clicked)
		root.update()

	def erase(self):
		if(self.drawing):
			canvas.delete(self.drawing)
			self.drawing = 0
		for l in self.connLines:
			canvas.delete(l)
			l = 0
		root.update()

	def delete(self):
		self.erase()
		squaresList.remove(self)
		squaresCoords[self.y].remove(self)
		for s in self.connections:
			if s:
				s.erase()
				s.getConnections()
				s.draw()
		




# Initialize tkinter ------------------------------------------

root = Tk()
root.minsize(SIZE, SIZE)
root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
canvas.place(relx=.5, rely=.5, anchor=CENTER)
# canvas.bind('<ButtonPress>', randSquare)

# Draw Grid ---------------------------------------------------

if(GRID):
	i=SCALE
	while(i <= SIZE):
		canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=DASH, width=DASHWIDTH)
		i += SCALE

# -------------------------------------------------------------



master = Square(0, 0, master=1, x = 10, y = 10)

n = Square(master, S)
Square(master, W)
for i in range(5, GSIZE-10):
	n = Square(n, E)

n = Square(master, E)
for i in range(5, GSIZE-3):
	n = Square(n, E)

# print(master.getPivot(1))
# master.pivot(CW)

while len(squaresList) < 50:
	s = random.choice(squaresList)
	d = random.choice(DA)
	n = Square(s, d)

# [s.draw() for s in squaresList]
# n.pivot(CW)

# n.pivot(1)
# [s.pivot(1) for s in squaresList]

# print(squaresCoords)


