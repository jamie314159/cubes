#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import colorsys
#import cubes
import random
import time
import math

# Size of window
SIZE = 320
# Size of squares
SCALE = 32

OFFSET = 10

# Derived info about window and grid
GSIZE = int(SIZE/SCALE)-1
GCENTER = int(GSIZE/2)
X_SCALE = SCALE
Y_SCALE = SCALE

DRAW = 1
# Display grid points
GRID = 0
# Width of grid points
DASHWIDTH = 2

CW = 0
CCW = 1
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

OUTLINE = "#000000"
FILL = "White"
C0 = "Red"
C1 = "Blue"
C2 = "Green"
C3 = "Purple"

drawings = {}
squares = []

pivotTable = [[W,N],[N,E],[E,S],[S,W]]
        
class coordinate(tuple):
	def __add__(self, direction):
		return coordinate((self[X] + DC[direction][X], self[Y] + DC[direction][Y]))
	
class Square(object):
        def __init__(self, x=-1,y=-1):
                self.location = (x,y)
                self.orientation = [C0,C1,C2,C3]

        def rotate(self, direction):
                if direction == CW:
                        y = self.orientation[3]
                        self.orientation[3] = self.orientation[2]
                        self.orientation[2] = self.orientation[1]
                        self.orientation[1] = self.orientation[0]
                        self.orientation[0] = y
                        
                        
                if direction == CCW:
                        y = self.orientation[0]
                        self.orientation[0] = self.orientation[1]
                        self.orientation[1] = self.orientation[2]
                        self.orientation[2] = self.orientation[3]
                        self.orientation[3] = y

        def move(self, direction):
                self.location = (self.location[X]+DC[direction][X],self.location[Y]+DC[direction][Y])
                
        def pivot(self, corner, direction):
                self.move(pivotTable[corner][direction])
                self.rotate(direction)
                
                        
                
                
def drawSquare(square):
	x1 = (square.location[X]*SCALE)+OFFSET
	y1 = (square.location[Y]*SCALE)+OFFSET
	x2 = (square.location[X]+1)*SCALE + OFFSET
	y2 = (square.location[Y]+1)*SCALE + OFFSET
	canvas.create_rectangle(x1, y1, x2, y2,  fill = FILL, outline = OUTLINE, width=1)
	canvas.create_rectangle(x1, y1, x1+SCALE/4, y1+SCALE/4,  fill = square.orientation[0], width = 1)
	canvas.create_rectangle(x2-SCALE/4, y1, x2, y1+SCALE/4,  fill = square.orientation[1], width = 1)
	canvas.create_rectangle(x2-SCALE/4, y2-SCALE/4, x2, y2,  fill = square.orientation[2], width = 1)
	canvas.create_rectangle(x1, y2-SCALE/4, x1+SCALE/4, y2,  fill = square.orientation[3], width = 1)
	
	
	root.update()







# Initialize tkinter ------------------------------------------

if DRAW:
	root = Tk()
	root.minsize(SIZE, SIZE)
	root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))

	canvas = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
	canvas.place(relx=.5, rely=.5, anchor=CENTER)
	#canvas.bind('<Button-2>', mClick)

	# Draw Grid ---------------------------------------------------

	if(GRID):
		i=0
		while(i <= SIZE):
			canvas.create_line(i, SCALE, i, SIZE+DASHWIDTH, dash=(DASHWIDTH, SCALE-DASHWIDTH), width=DASHWIDTH)
			i += SCALE

# -------------------------------------------------------------

a = Square(3,3)
b = Square(3,3)
b.pivot(0,CW)


squares.append(b)
squares.append(a)


if DRAW:	
	for s in squares:
		drawSquare(s)



