#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import colorsys
import cubes
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
GRID = 1
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
cornerColors = ["Red","Blue","Green","Purple"]

drawings = {}
squares = []

                
def drawSquare(square):
	for drawing in square.drawings:
		canvas.delete(drawing)
	square.drawings = []
	x1 = (square.location[X]*SCALE)
	y1 = (square.location[Y]*SCALE)
	x2 = (square.location[X]+1)*SCALE
	y2 = (square.location[Y]+1)*SCALE
	square.drawings.append(canvas.create_rectangle(x1, y1, x2, y2,  fill = FILL, outline = OUTLINE, width=1))
	
	cx = x1+SCALE/2
	cy = y1+SCALE/2
	
	square.drawings.append(canvas.create_line(cx,cy, cx+(SCALE*DC[square.orientation][X])/2, cy+(SCALE*DC[square.orientation][Y])/2))
	for drawing in square.drawings:
		canvas.tag_bind(drawing, '<Button-3>', lambda event, arg=square: rClick(event, arg))
		canvas.tag_bind(drawing, '<Button-1>', lambda event, arg=square: lClick(event, arg))

	c0 = canvas.create_rectangle(x1, y1, x1+SCALE/4, y1+SCALE/4,   width = 1, fill = cornerColors[int((square.orientation/2-0)%4)])
	c1 = canvas.create_rectangle(x2-SCALE/4, y1, x2, y1+SCALE/4,   width = 1, fill = cornerColors[int((square.orientation/2-1)%4)])
	c2 = canvas.create_rectangle(x2-SCALE/4, y2-SCALE/4, x2, y2,   width = 1, fill = cornerColors[int((square.orientation/2-2)%4)])
	c3 = canvas.create_rectangle(x1, y2-SCALE/4, x1+SCALE/4, y2,   width = 1, fill = cornerColors[int((square.orientation/2-3)%4)])

	square.drawings.append(c0)
	square.drawings.append(c1)
	square.drawings.append(c2)
	square.drawings.append(c3)

	canvas.tag_bind(c0, '<Button-1>', lambda event, args=[square,0]: pivotSquareL(event,args))
	canvas.tag_bind(c0, '<Button-3>', lambda event, args=[square,0]: pivotSquareR(event,args))
	canvas.tag_bind(c1, '<Button-1>', lambda event, args=[square,1]: pivotSquareL(event,args))
	canvas.tag_bind(c1, '<Button-3>', lambda event, args=[square,1]: pivotSquareR(event,args))
	canvas.tag_bind(c2, '<Button-1>', lambda event, args=[square,2]: pivotSquareL(event,args))
	canvas.tag_bind(c2, '<Button-3>', lambda event, args=[square,2]: pivotSquareR(event,args))
	canvas.tag_bind(c3, '<Button-1>', lambda event, args=[square,3]: pivotSquareL(event,args))
	canvas.tag_bind(c3, '<Button-3>', lambda event, args=[square,3]: pivotSquareR(event,args))
	
	
	root.update()

def pivotSquareL(event, args):
	square = args[0]
	corner = args[1]
	square.pivot(corner,CW)
	drawSquare(square)
	root.update()

def pivotSquareR(event, args):
	square = args[0]
	corner = args[1]
	square.pivot(corner,CCW)
	drawSquare(square)
	root.update()


def mClick(event):
	null

def lClick(event, square):
	square.rotate(CW)
	drawSquare(square)
	root.update()

	
def rClick(event, square):
	square.rotate(CCW)
	drawSquare(square)
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
			canvas.create_line(i, 0, i, SIZE,  width=1)
			canvas.create_line(0, i, SIZE, i,  width=1)
			i += SCALE

# -------------------------------------------------------------

a = cubes.Square(0,0)
b = cubes.Square(3,3)
b.pivot(0,CW)


squares.append(b)
squares.append(a)


if DRAW:	
	for s in squares:
		drawSquare(s)




try:
	# root.after(0, rp)
	root.mainloop()
except:
	pass