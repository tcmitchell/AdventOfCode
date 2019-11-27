package main

// Direction holds the x and y offsets to move
// in a given direction
type Direction struct {
	x    int
	y    int
	name string
}

var up = Direction{0, 1, "up"}
var down = Direction{0, -1, "down"}
var left = Direction{-1, 0, "left"}
var right = Direction{1, 0, "right"}

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

func reverse(d Direction) Direction {
	switch d {
	case up:
		return down
	case right:
		return left
	case down:
		return up
	case left:
		return right
	}
	panic("Unknown direction")
}
