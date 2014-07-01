#!/bin/ipython3

from tkinter import *
from tkinter import ttk
import random
import math
import time
import cubes

# Constants ---------------------------------------------------
LINES = -1
DIAGONALS = 0
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

# Make this a dictionary
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


MASTER = 0

# Functions, Procedures, Classes & Methods -----------------------------------------------------

# def randSquare():
# 	if squaresList:
# 		return random.choice(squaresList)
# 	return 0

# def drawPath(event = None, start = 0, goal = 0):
# 	# print(squaresList)
# 	for s in squaresList:
# 		s.fill = FILL
# 		s.draw()
# 	if start == 0:
# 		start = random.choice(squaresList)
# 	if goal == 0:
# 		goal = MASTER
# 	p = shortestPath(start, goal)
# 	for s in p:
# 		if s == start:
# 			s.fill = "green"
# 		elif s == goal:
# 			s.fill = "red"
# 		else:
# 			s.fill = "blue"
# 		s.draw()




# def randPivot(event = None):
# 	n = 0
# 	shuffled = list(squaresList)
# 	random.shuffle(shuffled)
# 	for s in shuffled:
# 		d = random.choice([CW, CCW])
# 		n = s.pivot(d)
# 		if n:
# 			return n
								


# def randNewSquare(event = None):
# 	opens = []
# 	while(len(squaresList) < GSIZE*GSIZE):
# 		for n in (0,1,2,3):
# 			picks = []
# 			shuffled = list(qsuaresList)
# 			random.shuffle(shuffled)
# 			[picks.append(q) for q in shuffled if q.adjNum == n]
# 			if picks:
# 				for s in picks:
# 					opens = []
# 					for d in DA:
# 						if s.connections[d] == 0:
# 							opens.append(d)
# 					random.shuffle(opens)
# 					for d in opens:
# 						d = random.choice(opens)
# 						m = Square(s, d)
# 						if m:
# 							return m


			
			


	




def clicked(event):
	print("test")


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
		canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=DASH, width=DASHWIDTH)
		i += SCALE

# -------------------------------------------------------------



MASTER = cubes.Square(0, 0, master=1, x = 10, y = 10)
n = cubes.Square(MASTER, S)
m = cubes.Square(n, W)

# for i in range(5, GSIZE-10):
# 	n = Square(n, E)

# n = Square(MASTER, E)
# for i in range(5, GSIZE-3):
# 	n = Square(n, E)

while len(squaresList) < 100:
	n = randNewSquare()

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