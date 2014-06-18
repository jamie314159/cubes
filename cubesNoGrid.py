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

N = 0
E = 1
S = 2
W = 3

DA = [N,E,S,W]
DC = [(0,-1), (1,0), (0,1), (-1,0)]

# Functions, Procedures, Classes & Methods -----------------------------------------------------

def opposite(d):
	return((d+2)%4)

def drawSquares(s, x, y, prev=None):
	print(s)
	
	x1 = ((x+1)*SCALE)
	y1 = ((y+1)*SCALE)
	x2 = ((x+1)*SCALE)+SCALE
	y2 = ((y+1)*SCALE)+SCALE

	s.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline=s.color, width=2)

	for i in DA:
		if(s.connections[i] != 0):
			if(opposite(i) != prev):
				drawSquares(s.connections[i], x+DC[i][0], y+DC[i][1], i)


class Square(object):
	def __new__(cls, parent, parent_dir, master = 0):
		if(master):
			return object.__new__(cls)
		elif(parent.connections[opposite(parent_dir)] == 0):
			return object.__new__(cls)

	def __init__(self, parent, parent_dir, master = 0):
			self.master = master
			self.connections = [0,0,0,0]
			self.connections[opposite(parent_dir)] = parent;
			if(master == 1):
				self.x = GCENTER
				self.y = GCENTER
			else:
				self.x = parent.x + DC[parent_dir][0]
				self.y = parent.y + DC[parent_dir][1]
			if(master == 0):
				parent.connections[parent_dir] = self
			self.color = "black";

	def draw(self):
		x1 = ((self.x+1)*SCALE)
		y1 = ((self.y+1)*SCALE)
		x2 = ((self.x+1)*SCALE)+SCALE
		y2 = ((self.y+1)*SCALE)+SCALE
		self.drawing = canvas.create_rectangle(x1, y1, x2, y2, outline=self.color, width=2)


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

squares = []

M = Square(0, 0, master=1)
squares.append(M)

while len(squares) < 10:
	s = random.choice(squares)
	d = random.choice(DA)
	n = Square(s, d)
	if(n != None):
		squares.append(n)

[print(x.connections) for x in squares]


[s.draw() for s in squares]
# drawSquares(M, GCENTER, GCENTER)
	




