package main

import (
	"bufio"
	"fmt"
	"os"
)

const maxX = uint(1000)
const maxY = uint(1000)

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

func plot(grid [][][]int, x, y, w, h uint, id int) {
	var col, row uint
	for col = x; col < x+w; col++ {
		for row = y; row < y+h; row++ {
			grid[row][col] = append(grid[row][col], id)
		}
	}
}

func main() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	var grid = make([][][]int, maxY)
	for i := range grid {
		grid[i] = make([][]int, maxX)
		for j := range grid[i] {
			grid[i][j] = make([]int, 0)
		}
	}
	for v := range c {
		fmt.Println(v)
		var id int
		var x, y, w, h uint
		fmt.Sscanf(v, "#%d @ %d,%d: %dx%d", &id, &x, &y, &w, &h)
		fmt.Printf("#%d @ %d,%d: %dx%d\n", id, x, y, w, h)
		plot(grid, x, y, w, h, id)
	}
	var multiClaims uint
	for y := range grid {
		for x := range grid[y] {
			if len(grid[y][x]) > 1 {
				// fmt.Printf("%d, %d has multiple claims\n", x, y)
				multiClaims++
			}
		}
	}
	fmt.Println("Multi claims = ", multiClaims)
}
