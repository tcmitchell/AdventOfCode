package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
)

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

func fuelRequired(mass float64) int {
	return int(math.Floor(mass/3)) - 2
}

func computeFuel(c chan string) int {
	var totalFuel, mass int
	for line := range c {
		fmt.Sscanf(line, "%d", &mass)
		totalFuel += fuelRequired(float64(mass))
	}
	return totalFuel
}

func part1(puzzleInput string) {
	c := make(chan string, 1)
	go ReadInputLines(puzzleInput, c)
	totalFuel := computeFuel(c)
	fmt.Printf("Part1: Total fuel = %d", totalFuel)
}

func main() {
	part1("input.txt")
}
