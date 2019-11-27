package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// Grid represents the cluster computing grid
type Grid map[string]string

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

func infectGrid(grid Grid, x, y int) {
	grid[gridEntry(x, y)] = "#"
}

func cleanGrid(grid Grid, x, y int) {
	delete(grid, gridEntry(x, y))
}

func gridState(grid Grid, x, y int) string {
	if gridInfected(grid, x, y) {
		return "#"
	}
	return "."
}

func gridInfected(grid Grid, x, y int) bool {
	state, ok := grid[gridEntry(x, y)]
	// fmt.Printf("grid[%s]: state=%s; ok=%t\n", gridEntry(x, y), state, ok)
	// A grid node is infected if the entry is present
	// AND the entry is "#"
	return ok && state == "#"
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
			if state == "#" {
				yValue := nRows - y - 1
				infectGrid(grid, x, yValue)
			}
		}
	}
	// for y := nRows; y > 0; y-- {
	// 	for x := 0; x < nRows; x++ {
	// 		fmt.Printf("%s", gridState(grid, x, y-1))
	// 	}
	// 	fmt.Println()
	// }
	midpoint := nRows / 2
	return grid, midpoint, midpoint
}

func moveForward(x, y int, direction Direction) (int, int) {
	return x + direction.x, y + direction.y
}

func carrierBurst(grid Grid, x, y int, direction Direction) (int, int, Direction, bool) {
	// fmt.Printf("carrierBurst(%d, %d, %s)\n", x, y, direction.name)
	infected := false
	if gridInfected(grid, x, y) {
		// fmt.Printf("grid[%d,%d] is infected\n", x, y)
		direction = turnRight(direction)
		cleanGrid(grid, x, y)
	} else {
		direction = turnLeft(direction)
		infectGrid(grid, x, y)
		infected = true
	}
	// fmt.Printf("Moving %s from %d,%d", direction.name, x, y)
	x, y = moveForward(x, y, direction)
	// fmt.Printf(" to %d, %d\n", x, y)
	return x, y, direction, infected
}

func part1(grid Grid, x, y int) {
	infectedCount := 0
	var infected bool
	// fmt.Printf("Initial position [%d, %d]\n", x, y)
	direction := up
	// fmt.Println("Direction:", direction)
	for i := 0; i < 10000; i++ {
		x, y, direction, infected = carrierBurst(grid, x, y, direction)
		if infected {
			infectedCount++
		}
		// fmt.Printf("Carrier at %d, %d, facing %s. State = %s, infected %d\n",
		// 	x, y, direction.name, gridState(grid, x, y), infectedCount)
	}
	fmt.Printf("Infected %d nodes\n", infectedCount)
}

func main() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	grid, x, y := loadGrid(c)
	// fmt.Printf("Centerpoint = %d, %d\n", x, y)
	part1(grid, x, y)
}
