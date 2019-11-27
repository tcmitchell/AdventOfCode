package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// Grid represents the cluster computing grid
type Grid map[string]string

// A function to perform a burst of activity by the carrier
type burstFunc func(grid Grid, x, y int, direction Direction) (int, int, Direction, bool)

// CLEAN state
const CLEAN = "."

// INFECTED state
const INFECTED = "#"

// FLAGGED state
const FLAGGED = "F"

// WEAKENED state
const WEAKENED = "W"

// ReadInputLines reads the input file line by line,
// passing each line to the given channel.
func ReadInputLines(infile string, c chan string) {
	f, err := os.Open(infile)
	if err != nil {
		panic("foo")
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		c <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	close(c)
}

func gridEntry(x, y int) string {
	return fmt.Sprintf("%d,%d", x, y)
}

func setGrid(grid Grid, x, y int, state string) {
	if state == CLEAN {
		delete(grid, gridEntry(x, y))
	} else {
		grid[gridEntry(x, y)] = state
	}
}

func gridState(grid Grid, x, y int) string {
	state, ok := grid[gridEntry(x, y)]
	if !ok {
		state = CLEAN
	}
	return state
}

func loadGrid(c chan string) (Grid, int, int) {
	result := make([][]string, 0)
	for line := range c {
		result = append(result, strings.Split(line, ""))
	}
	// Now reverse the grid. We read it in top to bottom, so
	// so the 0,0 point is the top left. We want it to be the
	// bottom left.
	nRows := len(result)
	grid := make(map[string]string, nRows)
	for y := range result {
		for x, state := range result[y] {
			yValue := nRows - y - 1
			setGrid(grid, x, yValue, state)
		}
	}
	midpoint := nRows / 2
	return grid, midpoint, midpoint
}

func moveForward(x, y int, direction Direction) (int, int) {
	return x + direction.x, y + direction.y
}

func carrierBurst(grid Grid, x, y int, direction Direction) (int, int, Direction, bool) {
	// fmt.Printf("carrierBurst(%d, %d, %s)\n", x, y, direction.name)
	infected := false
	switch gridState(grid, x, y) {
	case INFECTED:
		direction = turnRight(direction)
		setGrid(grid, x, y, CLEAN)
	case CLEAN:
		direction = turnLeft(direction)
		setGrid(grid, x, y, INFECTED)
		infected = true
	}
	// fmt.Printf("Moving %s from %d,%d", direction.name, x, y)
	x, y = moveForward(x, y, direction)
	// fmt.Printf(" to %d, %d\n", x, y)
	return x, y, direction, infected
}

func runCarrier(grid Grid, x, y int, activityBurst burstFunc, iters int) {
	infectedCount := 0
	var infected bool
	// fmt.Printf("Initial position [%d, %d]\n", x, y)
	direction := up
	// fmt.Println("Direction:", direction)
	for i := 0; i < iters; i++ {
		x, y, direction, infected = activityBurst(grid, x, y, direction)
		if infected {
			infectedCount++
		}
		// fmt.Printf("Carrier at %d, %d, facing %s. State = %s, infected %d\n",
		// 	x, y, direction.name, gridState(grid, x, y), infectedCount)
	}
	fmt.Printf("Infected %d nodes\n", infectedCount)
}

func part1(grid Grid, x, y int) {
	runCarrier(grid, x, y, carrierBurst, 10000)
}

func carrierBurst2(grid Grid, x, y int, direction Direction) (int, int, Direction, bool) {
	// fmt.Printf("carrierBurst2(%d, %d, %s)\n", x, y, direction.name)
	infected := false
	switch gridState(grid, x, y) {
	case CLEAN:
		direction = turnLeft(direction)
		setGrid(grid, x, y, WEAKENED)
	case WEAKENED:
		// Keep current direction
		setGrid(grid, x, y, INFECTED)
		infected = true
	case INFECTED:
		direction = turnRight(direction)
		setGrid(grid, x, y, FLAGGED)
	case FLAGGED:
		direction = reverse(direction)
		setGrid(grid, x, y, CLEAN)
	}
	// fmt.Printf("Moving %s from %d,%d", direction.name, x, y)
	x, y = moveForward(x, y, direction)
	// fmt.Printf(" to %d, %d\n", x, y)
	return x, y, direction, infected
}

func part2(puzzleInput string) {
	c := make(chan string, 1)
	go ReadInputLines(puzzleInput, c)
	grid, x, y := loadGrid(c)
	runCarrier(grid, x, y, carrierBurst2, 10000000)
}

func main() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	grid, x, y := loadGrid(c)
	part1(grid, x, y)
	part2("input.txt")
}
