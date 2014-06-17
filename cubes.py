# TODO: Make sure pivot doesnt strand another cube

import random
import time
import copy
from tkinter import *
from tkinter import ttk

SIZE = 512
SCALE = 32
GSIZE = int(SIZE/SCALE)-1
X_SCALE = SCALE
Y_SCALE = SCALE
relX_SCALE = 1
relY_SCALE = 1
DELAY = 1

FILL = "tan"

N 	= 0
NE	= 1
E 	= 2
SE 	= 3
S 	= 4
SW  = 5
W 	= 6
NW	= 7

CW = 1
CCW = -1

root = Tk()
root.minsize(SIZE, SIZE)
root.geometry(str(int(SIZE+SCALE)) + 'x' + str(int(SIZE+SCALE)))


b = Canvas(root, width=SIZE+SCALE, height=SIZE+SCALE)
b.place(relx=.5, rely=.5, anchor=CENTER)

possibles = []
class Square:
	def __init__(self, xIn, yIn, color="#000000"):
		self.x = xIn;
		self.y = yIn;
		self.dirs = self.getDirs()
		self.color = color
		self.on = 0
		# self.fill = ""

	def getDirs(self):
		x = self.x;
		y = self.y;
		
		N=(x,y-1)
		NE=(x+1,y-1)
		E=(x+1,y)
		SE=(x+1,y+1)
		S=(x,y+1)
		SW=(x-1,y+1)
		W=(x-1,y)
		NW=(x-1,y-1)

		return([N, NE, E, SE, S, SW, W, NW])

	def draw(self, master=b):
		x1 = (self.x+1)*SCALE
		y1 = (self.y+1)*SCALE
		x2 = (self.x+2)*SCALE
		y2 = (self.y+2)*SCALE
		self.master = master
		self.drawing = master.create_rectangle(x1, y1, x2, y2, outline=self.color, width=2)
		# print(self.drawing)

	def erase(self):
		self.master.delete(self.drawing)

	def move(self, x, y):
		self.x = x
		self.y = y
		self.dirs = self.getDirs()


	def on(self):
		self.on = 1
		self.color = "blue"
		self.draw()
		b.update()

	def off(self):
		self.on = 0
		self.color = "black"
		self.draw()
		b.update()



class Grid:
	def __init__(self):
		self.grange = [(x, y) for x in range(0, GSIZE) for y in range(0, GSIZE)]
		self.grid = [[0 for x in range(0, GSIZE)] for y in range(0, GSIZE)]
		self.squares = []
		self.coords = []
		self.draws = []
		self.adjecent = set([])

	def checkAdjecent(self, exclude=0):
		self.adjecent = set([])
		check = copy.copy(self.squares)
		if(exclude in check):
			check.remove(exclude)
		for s in check:
			if (s.x+1, s.y) not in self.coords:
				self.adjecent.add((s.x+1, s.y)) 
			if (s.x-1, s.y) not in self.coords:
				self.adjecent.add((s.x-1, s.y))
			if (s.x, s.y+1) not in self.coords:
				self.adjecent.add((s.x, s.y+1))
			if (s.x, s.y-1) not in self.coords:
				self.adjecent.add((s.x, s.y-1))

	def checkAdjecentS(self, x, y, s):
		self.adjecent = set([])
		for c in self.squares:
			if(c != s):
				self.adjecent.add((c.x+1, c.y))
				self.adjecent.add((c.x-1, c.y))
				self.adjecent.add((c.x, c.y+1))
				self.adjecent.add((c.x, c.y-1))

	def touching(self, x, y):
		if(len(self.squares) == 0):
			return(1)
		else:
			self.checkAdjecent()
			# print(self.adjecent)
			if((x,y) in self.adjecent):
				return(1)
			else:
				return(0)

	def touchingS(self, x, y, s):
		if(len(self.squares) == 0):
			return(1)
		else:
			self.checkAdjecentS(x, y, s)
			# print(self.adjecent)
			if((x,y) in self.adjecent):
				return(1)
			else:
				return(0)

	def gridCheck(self, x, y):
		b = 1
		if ((x,y) in self.coords):
			b = 0
		elif ((x,y) not in self.grange):
			b = 0
		elif not self.touching(x,y):
			b = 0
		return(b)

	def gridCheckS(self, x, y, s):
		b = 1
		if ((x,y) in self.coords):
			b = 0
		elif ((x,y) not in self.grange):
			b = 0
		elif not self.touchingS(x,y,s):
			b = 0
		return(b)

	def add(self, x , y):
		if(self.gridCheck(x, y)):
			tempSquare = Square(x,y)
			self.coords.append((tempSquare.x, tempSquare.y))
			self.squares.append(tempSquare)
			self.grid[x][y] = tempSquare
			return(tempSquare)
		else:
			return(0)

	def draw(self, master):
		for s in self.squares:
			if(type(s) == Square):
				s.draw(master)

	def move(self, s, x, y):
		s.erase()
		self.grid[x][y] = s
		self.grid[s.x][s.y] = 0
		self.coords.remove((s.x, s.y))
		self.coords.append((x, y))
		s.move(x, y)
		s.draw(s.master)
		s.master.update()

	


	def getPivots(self, s):
		dirs = s.dirs
		pivots = set([])
		self.checkAdjecent(s)

		if(((dirs[N] in self.coords) and (dirs[S] in self.coords)) or ((dirs[E] in self.coords) and (dirs[W] in self.coords))):
			return(0)

		for i in range(0, 8):
			if((dirs[i] not in self.coords) and (dirs[i] in self.adjecent)):
				pivots.add(dirs[i])
		
		if((dirs[N] in self.coords) and (dirs[W] in self.coords) and (dirs[NW] in pivots)):
			pivots.remove(dirs[NW])

		if((dirs[N] in self.coords) and (dirs[E] in self.coords) and (dirs[NE] in pivots)):
			pivots.remove(dirs[NE])

		if((dirs[S] in self.coords) and (dirs[W] in self.coords) and (dirs[SW] in pivots)):
			pivots.remove(dirs[SW])

		if((dirs[S] in self.coords) and (dirs[E] in self.coords) and (dirs[SE] in pivots)):
			pivots.remove(dirs[SE])


		return(pivots)


	# pdir, 1 = cw, -1 = ccw
	def pivot(self, s,  pdir): #vx, vy):
		dirs = s.dirs
		pivots = self.getPivots(s)
		
		
		

		# print(len(order))
		# print((s.x,s.y), order)
		# print(pivots)
		if(pivots != 0):
			order = [x for x in dirs if x in pivots]
		
			if(dirs[N] in self.coords):
				order.reverse()
			# print(order)
			# print(pivots)
			# if(pdir == 0):
						
			# possibles = []
			# for q in order:
			# 	possibles.append(Square(q[0], q[1], "red"))
			# for p in possibles:
			# 	p.draw()

			# b.update()

			# time.sleep(DELAY*.5)
			# [q.draw() for q in self.squares]

			# print(order)
			# CW
			if(pdir == 1):
				if((order[0][0], order[0][1]) in self.grange):
					t = Square(order[0][0], order[0][1], "red")
					t.draw()
					b.update()
					time.sleep(DELAY*.5)
					t.erase()
					self.move(s, order[0][0], order[0][1])
					b.update

			# CCW
			elif(pdir == -1):
				if((order[1][0], order[1][1]) in self.grange):
					t = Square(order[1][0], order[1][1], "red")
					t.draw()
					b.update()
					time.sleep(DELAY*.5)
					t.erase()
					self.move(s, order[1][0], order[1][1])
					b.update

			for p in possibles:
				p.erase()
			return(1)
			# if(self.gridCheckS(s.x+vx, s.y+vy, s)):
			# 	self.move(s, s.x+vx, s.y+vy)
		else:
			return 0


	def random(self):
		return(random.choice(self.squares))


	def clear(self):
		self.squares = []
		self.coords = []



lDashW = int(SCALE/4)
lDashOff = int(lDashW/2)
lDash = (lDashW, SCALE-lDashW)
grid_on = 1
if(grid_on):
	i=SCALE
	while(i <= SIZE):
		b.create_line(i,SCALE,i,SIZE, dash=lDash, dashoff=lDashOff)
		i += SCALE

	i=SCALE
	while(i <= SIZE):
		b.create_line(SCALE,i,SIZE,i, dash=lDash, dashoff=lDashOff)
		i += SCALE

g = Grid()

# [g.add(x, 15) for x in range(3, 22)]
# [g.add(20, y) for y in range(22, 2, -1)]
g.add(3,3)
m = g.add(4,3)
g.add(4,4)

# x = random.randint(0, GSIZE-1)
# y = random.randint(0, GSIZE-1)
# g.add(x,y)

i = 0
r = random.randint(0, GSIZE*(int(GSIZE/8)))
print("r =", r)
# print(g.adjecent)
while(i < r):
	g.checkAdjecent()
	a = random.choice(list(g.adjecent))
	x = a[0]
	y = a[1]
	if(g.add(x, y)):
		i += 1	

# for x in range(5, 25):
# 	for y in range(5, 25):
# 		g.add(x, y)

g.draw(b)

b.update()
try:
	while 1:
		s = g.random()
		# s.on()
		f = g.pivot(s, random.choice([-1,1]))
		# s.off()
		# for s in g.squares:
		# 	g.pivot(s,1)

		root.update_idletasks() # redraw
		root.update() # process events
		time.sleep(DELAY*f)
		
except TclError:
	pass # to avoid errors when the window is closed



