// Constants ---------------------------------------------------

// Direction deffinitions
var CW = 1;
var CCW = -1;

// For easier reading when referenceing coordinates
var X = 0;
var Y = 1;

// Map of directions to coorsponding numbers
var N 	= 0;
var NE 	= 1;
var E 	= 2;
var SE 	= 3;
var S 	= 4;
var SW 	= 5;
var W 	= 6;
var NW 	= 7;

// Lists of directions for iteration
var DA = [N,E,S,W];
var DB = [N,NE,E,SE,S,SW,W,NW];
var DC = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]];

// Size of window
var SIZE = 512;
// Size of squares
var SCALE = 16;

// Derived info about window and grid
var GSIZE = (SIZE/SCALE)-1;
var GCENTER = (GSIZE/2);
var X_SCALE = SCALE;
var Y_SCALE = SCALE;

var squaresList = new Array();
// squaresCoords = [[0 for i in range(GSIZE)] for j in range(GSIZE)]
var squaresCoords = new Array();

var MASTER = 0;


// Returns opposite direction of orientation
function opposite(orientation) {
	return((orientation+4)%8);
}

// Increments orientation in direction num times
function clock(orientation, direction, num){
	while (num > 0) {
		if (direction == CW) {
			if (orientation == NW) {
				orientation = N;
			} else {
				orientation = orientation+1;
			}
		} else if( direction == CCW) {
			if (orientation == N) {
				orientation = NW;
			} else {
				orientation = orientation-1;
			}
		}
		num -= 1;
	}
	return orientation;
}

function coordAddDir(a, b){
	return [a[X] + DC[b][X], a[Y] + DC[b][Y]];
}



function Square(parent, parentDir, master) { 
	this.fill = "grey";
	this.master = master;
	this.connections = new Array();
	this.orientation = N;
	this.adjNum = 0;

	if (this.master) {
		MASTER = this;
		this.coord = [0, 0];
		squaresList.push(this);
		squaresCoords[this.coord] = this;
		getConnections(this);
		// this.getConnected();
	} else {
		this.coord = coordAddDir(parent.coord, parentDir);
		this.connections[opposite(parentDir)] = parent;
		parent.connections[parentDir] = this;

		getConnections(this);
		// this.getConnected();

		squaresCoords[this.coord] = this;
		squaresList.push(this);
		for (s in this.connections.keys()) {
			alert("test");
			this.connections[s].getConnections();
		}
	}
}

// Pivot self in given direction
Square.prototype.pivot = function(direction) {
	getConnections(this);
	for (var d = 0; d < DB.length; d+= 2) {
		if (this.connections[d]) {
			pivot = d;
		}
	}

	if (this.connections[opposite(pivot)] == null) {
		t = clock(pivot, -direction, 2);
		if (this.connections[t]) {
			pivot = t;
			t = clock(pivot, -direction, 2);
		}
	

		temp = coordAddDir(this.coord, t);

		if (squaresCoords[temp] == null) {
			if (squaresCoords[coordAddDir(temp, pivot)]) {
				if (squaresCoords[coordAddDir(temp, opposite(pivot))] == null) {
					if (move(this, coordAddDir(this.coord, t))){
						this.orientation = clock(this.orientation, direction, 2);
						return 1;
					}
				}
			} else {
				if (squaresCoords[coordAddDir(temp, t)]) {
					if (move(this, coordAddDir(this.coord, t))) {
						this.orientation = clock(this.orientation, direction, 2);
						return 1;
					}
				} else {
					t = clock(pivot, -direction, 1)
					if (squaresCoords[coordAddDir(temp, t)] == null) {
						if (move(this, coordAddDir(this.coord, t))) {
							this.orientation = clock(this.orientation, direction, 4);
							return 1;
						}
					}
				}
			}
		}
	}
	return 0
}

function move(square, newCoord) {
	var fail = 0;
	var oldCoord = square.coord;
	var conns = [];
	if (squaresCoords[newCoord] == null) {
		squaresCoords[square.coord] = null;
		square.coord = newCoord;
		squaresCoords[square.coord] = square;			

		for (var s = 0; s < squaresList.length; s++) {
			getConnections(squaresList[s])
			// squaresList[s].getConnected()
			if (squaresList[s].adjNum == 0) {
				fail = 1;
				break;
			}
		}

		if (fail) {
			squaresCoords[square.coord] == null
			square.coord = oldCoord;
			squaresCoords[square.coord] = square;
			for (var s = 0; s < squaresList.length; s++) {
				getConnections(squaresList[s])
				// squaresList[s].getConnected()
			}
			return 0;
		} else {
			return 1;
		}
	} else {
		return 0;
	}
}


// Gets the direcetions from self which have squares
function getConnections(square) {
	square.connections = new Array();
	square.adjNum = 0;
	for (var d = 0; d < DB.length; d++) {
		c = coordAddDir(square.coord, d);
		if (squaresCoords[c]) {
			square.connections[d] = squaresCoords[c];
			squaresCoords[c].connections[opposite(d)] = square;
			if ((d == 0) || (d == 2) || (d == 4) || (d == 6)) {
				square.adjNum += 1;
			}
		}
	}
}




function test() {
	var a = new Square(0, 0, 1)
	var b = new Square(MASTER, N)
	b.pivot(CW)


}