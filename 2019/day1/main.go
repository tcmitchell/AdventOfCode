package main

import (
	"bufio"
	"fmt"
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

func fuelRequired(mass int) int {
	return mass/3 - 2
}

func fuelRequired2(mass int) int {
	totalFuel := 0
	for {
		// fmt.Printf("Computing more fuel for %d\n", moreFuel)
		mass = fuelRequired(mass)
		// fmt.Printf("moreFuel = %d\n", moreFuel)
		if mass <= 0 {
			break
		}
		totalFuel += mass
	}
	return totalFuel
}

func computeFuel(c chan string) int {
	var totalFuel, mass int
	for line := range c {
		fmt.Sscanln(line, &mass)
		totalFuel += fuelRequired(mass)
	}
	return totalFuel
}

func computeFuel2(c chan string) int {
	var totalFuel, mass int
	for line := range c {
		fmt.Sscanln(line, &mass)
		totalFuel += fuelRequired2(mass)
	}
	return totalFuel
}

func part1(puzzleInput string) {
	c := make(chan string, 1)
	go ReadInputLines(puzzleInput, c)
	totalFuel := computeFuel(c)
	fmt.Printf("Part1: Total fuel = %d\n", totalFuel)
}

func part2(puzzleInput string) {
	c := make(chan string, 1)
	go ReadInputLines(puzzleInput, c)
	totalFuel := computeFuel2(c)
	fmt.Printf("Part2: Total fuel = %d\n", totalFuel)
}

func main() {
	part1("input.txt")
	part2("input.txt")
}
