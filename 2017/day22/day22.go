package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

// Grid represents the cluster computing grid
type Grid [][]string

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

func loadGrid(c chan string) Grid {
	result := make([][]string, 0)
	for line := range c {
		result = append(result, strings.Split(line, ""))
	}
	// Now reverse the grid. We read it in top to bottom, so
	// so the 0,0 point is the top left. We want it to be the
	// bottom left.
	nRows := len(result)
	grid := make([][]string, nRows)
	for y := range result {
		grid[nRows-y-1] = result[y]
	}
	return grid
}

func printGrid(grid Grid) {
	for i := len(grid); i > 0; i-- {
		fmt.Println(strings.Join(grid[i-1], ""))
	}
}

func initialPosition(grid Grid) (int, int, error) {
	// Assume the grid is always square and odd in size
	center := len(grid)/2 + 1
	return center, center, nil
}

func part1(grid Grid) {
	x, y, _ := initialPosition(grid)
	fmt.Printf("Initial position [%d, %d]\n", x, y)
	direction := up
	fmt.Println("Direction:", direction)
}

func main() {
	c := make(chan string, 1)
	go ReadInputLines("testinput.txt", c)
	grid := loadGrid(c)
	fmt.Printf("Loaded %d x %d grid\n", len(grid[0]), len(grid))
	printGrid(grid)
	part1(grid)
}
