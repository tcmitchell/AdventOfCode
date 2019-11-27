package main

// Direction holds the x and y offsets to move
// in a given direction
type Direction struct {
	x int
	y int
}

var up = Direction{0, 1}
var down = Direction{0, -1}
var left = Direction{-1, 0}
var right = Direction{1, 0}

func turnLeft(d Direction) Direction {
	switch d {
	case up:
		return left
	case left:
		return down
	case down:
		return right
	case right:
		return up
	}
	panic("Unknown direction")
}

func turnRight(d Direction) Direction {
	switch d {
	case up:
		return right
	case right:
		return down
	case down:
		return left
	case left:
		return up
	}
	panic("Unknown direction")
}
