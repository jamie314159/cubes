#!/bin/ipython3

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
	opens = []
	s = random.shuffle(squaresList)
	for s in squaresList:
		opens = []
		for d in DA:
				if s.connections[d] == 0:
					opens.append(d)
		if len(opens) != 3:
			r = s
			
	if len(opens) == 0:a


	d = random.choice(opens)
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
			self.adjacent = [0,0,0,0,0,0,0,0]
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
			self.getConnected()
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
		for i in range(0, 7, 2):
			self.adjacent[i] = self.connections[i]

		self.adjNum = 0
		for s in self.adjacent:
			if s:
				self.adjNum += 1

	def getConnected(self):
		self.connected = 0
		if self.master:
			self.connected = 1
		else:
			for s in self.adjacent:
				if s:
					if s.master or s.connected:
						self.connected = 1


	def getPivot(self, direction):
		connlist = []
		[connlist.append(self.connections[d]) for d in DA if self.connections[d]]
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

			

	def pivot(self, direction):
		oldx = self.x
		oldy = self.y
		conns = []
		[conns.append(s) for s in self.adjacent if s]
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
				pDir = clock(pDir, -direction)
				x = self.x + DC[pDir][X]
				y = self.y + DC[pDir][Y]
				
			pDir = clock(pDir, direction)
			
			self.move(x, y)
			[conns.append(s) for s in self.adjacent if s]

			for s in conns:
				s.getConnected()

			fail = 0

			adj = 0
			for s in self.adjacent:
				if s:
					adj += 1
			if adj > 2:
				fail = 1

			for s in conns:
				if s.connected == 0:
					fail = 1

			if fail:
				self.move(oldx, oldy)
							

		
	def clicked(self, event):
		self.pivot(CW)
		# self.delete()
		# self.erase()
		# print(self.connections)
		# self.move(0,0)

	def rClick(self, event):
		self.pivot(CW)

	def lClick(self, event):
		self.pivot(CCW)

	def move(self, x, y):
		oldCoord = (self.x, self.y)
		conns = []
		[conns.append(s) for s in self.connections if s]

		self.erase()
		squaresCoords[self.y][self.x] = 0

		self.x = x
		self.y = y
		
		squaresCoords[self.y][self.x] = self
		self.getConnections()
		[conns.append(s) for s in self.connections if s]

		self.draw()
		for s in conns:
			if s:
				s.erase()
				s.getConnections()
				s.draw()

	def draw(self):
		self.erase()
		x1 = ((self.x+1)*SCALE)
		y1 = ((self.y+1)*SCALE)
		x2 = ((self.x+1)*SCALE)+SCALE
		y2 = ((self.y+1)*SCALE)+SCALE
		self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline = self.outline, fill = self.fill, width=2)
		canvas.tag_bind(self.drawing, '<Button-3>', self.rClick)
		canvas.tag_bind(self.drawing, '<Button-1>', self.lClick)
		for c in DB:
			if self.connections[c] != 0:
				x1 = SCALE*(self.x+1.5)
				y1 = SCALE*(self.y+1.5)
				x2 = SCALE*((self.x+1.5)+(.5*DC[c][0]))
				y2 = SCALE*((self.y+1.5)+(.5*DC[c][1]))
				self.connLines[c] = canvas.create_line(x1, y1, x2, y2)
				canvas.tag_bind(self.connLines[c], '<Button-3>', self.rClick)
				canvas.tag_bind(self.connLines[c], '<Button-1>', self.lClick)
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
		conns = []
		[conns.append(s) for s in self.connections if s]
		squaresList.remove(self)
		squaresCoords[self.y][self.x] = 0
		self = 0
		for s in conns:
			s.getConnections()
			s.erase()
			s.draw()


if __name__ == "__main__"
# Initialize tkinter ------------------------------------------

root = Tk()
root.minsize(SIZE, SIZE)
root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
canvas.place(relx=.5, rely=.5, anchor=CENTER)
canvas.bind('<B2-Motion>', randSquare)

# Draw Grid ---------------------------------------------------

if(GRID):
	i=SCALE
	while(i <= SIZE):
		canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=DASH, width=DASHWIDTH)
		i += SCALE

# -------------------------------------------------------------



master = Square(0, 0, master=1, x = 10, y = 10)

# n = Square(master, S)
# Square(master, W)
# for i in range(5, GSIZE-10):
# 	n = Square(n, E)

# n = Square(master, E)
# for i in range(5, GSIZE-3):
# 	n = Square(n, E)

while len(squaresList) < 50:
	randSquare(None)
	# s = random.choice(squaresList)
	# d = random.choice(DA)
	# n = Square(s, d)

# [s.draw() for s in squaresList]
# n.pivot(CW)

# n.pivot(1)
# [s.pivot(1) for s in squaresList]

# print(squaresCoords)
root.mainloop()

