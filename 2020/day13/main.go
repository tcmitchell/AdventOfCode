package main

import (
	"../aoc"
	"fmt"
	"log"
	"math"
	"strconv"
	"strings"
)

func p1LoadInput(filename string) (int, []int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, nil, err
	}
	// line 1 is the departure timestamp
	ts, err := strconv.Atoi(lines[0])
	if err != nil {
		return 0, nil, err
	}
	busses := make([]int, 0)
	for _, b := range strings.Split(lines[1], ",") {
		if b == "x" {
			continue
		}
		busTime, err := strconv.Atoi(b)
		if err != nil {
			return 0, nil, err
		}
		busses = append(busses, busTime)
	}
	return ts, busses, nil
}

func part1(filename string) (int, error) {
	departure, busTimes, err := p1LoadInput(filename)
	if err != nil {
		return 0, err
	}
	//log.Printf("Departure: %d", departure)
	//log.Printf("Bus times: %v", busTimes)

	// min next arrival time for each bus
	nextBus := 0
	nextTime := math.MaxInt64
	for _, bus := range busTimes {
		mod := departure % bus
		if mod == 0 {
			return bus, nil
		}
		next := departure + bus - mod
		if next < nextTime {
			nextBus = bus
			nextTime = next
		}
	}
	return (nextTime - departure) * nextBus, nil
}

func part2(filename string) (int, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return 0, err
	}
	return len(lines), nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	//filename = "test-input2.txt"
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
