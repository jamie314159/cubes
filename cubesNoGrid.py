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

N = 0
E = 1
S = 2
W = 3

DA = [N,E,S,W]
DC = [(0,-1), (1,0), (0,1), (-1,0)]

squaresList = []
squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]

# Functions, Procedures, Classes & Methods -----------------------------------------------------

def opposite(d):
	return((d+2)%4)

def clock(d, direction):
	if direction == CW:
		if d == W:
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
				if squaresCoords[x][y] == 0:
					if(master or parent.connections[parent_dir] == 0):
						return object.__new__(cls)
					


	def __init__(self, parent, parent_dir, master = 0, x = -1, y = -1, outline = OUTLINE, fill = FILL):
			self.master = master
			self.connections = [0,0,0,0]
			self.connLines = [0,0,0,0]
			self.connNum = 0

			if(master == 1):
				if(x == -1):
					self.x = GCENTER
				else:
					self.x = x					

				if(y == -1):
					self.y = GCENTER
				else:
					self.y = y
			else:
				self.x = parent.x + DC[parent_dir][0]
				self.y = parent.y + DC[parent_dir][1]
				self.getConnections()

			squaresList.append(self)
			squaresCoords[self.x][self.y] = self

			self.outline = outline
			self.fill = fill
			self.drawing = None

	def getConnections(self):
		for d in DA:
			adjCoord = (self.x+DC[d][X], self.y+DC[d][Y])
			if(adjCoord[X] >= 0 and adjCoord[Y] >= 0 and adjCoord[X] < GSIZE and adjCoord[Y] < GSIZE):
				adjSquare = squaresCoords[adjCoord[X]][adjCoord[Y]]
				if adjSquare != 0:
					self.connections[d] = adjSquare
					self.connNum += 1
					adjSquare.connections[opposite(d)] = self
					adjSquare.connNum += 1

	def pivot(self, direction):
		if(self.connNum < 3):
			if(self.connNum == 1):
				# self.fill = "orange"
				for d in DA:
					if self.connections[d]:
						s = self.connections[d]
			if(self.connNum == 2):
				if(((self.connections[N] and self.connections[S]) == 0) and ((self.connections[E] and self.connections[W]) == 0)):
					# self.fill = "red"
					for d in DA:
						if self.connections[d]:
							if self.connections[clock(d, direction)]:
								s = self.connections[d]
			
			self.draw()

			# s.fill = "blue"
			for d in DA:
				if self.connections[d] == s:
					sd = d
			if s.connections[clock(opposite(sd), direction)] == 0:
				test = Square(s, clock(opposite(sd), direction))
			else:
				s = s.connections[clock(opposite(sd), direction)]
				sd = clock(opposite(sd), direction)
				if s.connections[clock(opposite(sd), direction)] == 0:
					test = Square(s, clock(opposite(sd), direction))
			if test:
				if test.connNum < 3:
					old = self
					self = test
					old.erase()

					self.getConnections()
					for c in self.connections:
						if(c):
							c.getConnections()
							c.draw()

					self.draw()
					for a in self.connections:
						if(a):
							a.draw()
					


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
		self.pivot(1)
		# self.delete()

	def draw(self):
		self.erase()
		x1 = ((self.x+1)*SCALE)
		y1 = ((self.y+1)*SCALE)
		x2 = ((self.x+1)*SCALE)+SCALE
		y2 = ((self.y+1)*SCALE)+SCALE
		self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline = self.outline, fill = self.fill, width=2, )
		canvas.tag_bind(self.drawing, '<ButtonPress>', self.clicked)
		for c in DA:
			if self.connections[c] != 0:
				x1 = SCALE*(self.x+1.5)
				y1 = SCALE*(self.y+1.5)
				x2 = SCALE*((self.x+1.5)+(.5*DC[c][0]))
				y2 = SCALE*((self.y+1.5)+(.5*DC[c][1]))
				self.connLines[c] = canvas.create_line(x1, y1, x2, y2)
				canvas.tag_bind(self.connLines[c], '<ButtonPress>', self.clicked)
		root.update()

	def erase(self):
		# print("abc")
		if(self.drawing):
			canvas.delete(self.drawing)
		for l in self.connLines:
			canvas.delete(l)
		root.update()

	def delete(self):
		self.erase()
		# if self in squaresList:
		squaresList.remove(self)
		# if self in squaresCoords:
		squaresCoords.remove(self)



# Initialize tkinter ------------------------------------------

root = Tk()
root.minsize(SIZE, SIZE)
root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
canvas.place(relx=.5, rely=.5, anchor=CENTER)

# Draw Grid ---------------------------------------------------

if(GRID):
	i=SCALE
	while(i <= SIZE):
		canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=DASH, width=DASHWIDTH)
		i += SCALE

# -------------------------------------------------------------

M = Square(0, 0, master=1, x = 0, y = 10)


n = Square(M, 1)
for i in range(0, GSIZE-3):
	n = Square(n, 1)

while len(squaresList) < 100:
	s = random.choice(squaresList)
	d = random.choice(DA)
	n = Square(s, d)


[s.draw() for s in squaresList]

# n.pivot(1)
# [s.pivot(1) for s in squaresList]




