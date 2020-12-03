package main

import (
	"../aoc"
	"fmt"
	"log"
)

func checkSlope(lines []string, sx, sy int) int {
	width := len(lines[0])
	trees := 0
	x, y := 0, 0
	for y < len(lines)-1 {
		x += sx
		if x >= width {
			x -= width
		}
		y += sy
		if lines[y][x] == '#' {
			trees++
		}
	}
	return trees
}

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	trees := checkSlope(lines, 3, 1)
	return trees, nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	p1, err := part1(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d\n", p1)
	p2, err := part2(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	trees := 1
	//Right 1, down 1.
	trees *= checkSlope(lines, 1, 1)
	//Right 3, down 1. (This is the slope you already checked.)
	trees *= checkSlope(lines, 3, 1)
	//Right 5, down 1.
	trees *= checkSlope(lines, 5, 1)
	//Right 7, down 1.
	trees *= checkSlope(lines, 7, 1)
	//Right 1, down 2.
	trees *= checkSlope(lines, 1, 2)
	return trees, nil
}
