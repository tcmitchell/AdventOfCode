package main

import (
	"../aoc"
	"fmt"
	"log"
)

func part1(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	width := len(lines[0])
	trees := 0
	x, y := 0, 0
	for y < len(lines)-1 {
		x += 3
		if x >= width {
			x -= width
		}
		y += 1
		if lines[y][x] == '#' {
			trees++
		}
	}
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
	return len(lines), nil
}
