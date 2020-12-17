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

type Bus struct {
	Period int64
	Offset int64
}

func p2LoadInput(filename string) ([]Bus, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	result := make([]Bus, 0)
	for i, b := range strings.Split(lines[1], ",") {
		if b == "x" {
			continue
		}
		busTime, err := strconv.Atoi(b)
		if err != nil {
			return nil, err
		}
		// Normalize the offset
		i = i % busTime
		result = append(result, Bus{int64(busTime), int64(i)})
	}
	return result, nil
}

func p2FindSolution(busses []Bus) int64 {
	step := busses[0].Period
	start := busses[0].Offset
	for b := 1; b < len(busses); b++ {
		//log.Printf("Step %d starting at %d", step, start)
		for t := start; t < step*busses[b].Period; t += step {
			if t%busses[b].Period == busses[b].Period-busses[b].Offset {
				step *= busses[b].Period
				start = t
				break
			}
		}
	}
	//log.Printf("Result: %d", start)
	return start
}

func part2(filename string) (int64, error) {
	busses, err := p2LoadInput(filename)
	if err != nil {
		return 0, err
	}
	//for _, b := range busses {
	//	log.Printf("Bus %d at time T+%d", b.Period, b.Offset)
	//}
	answer := p2FindSolution(busses)
	return answer, nil
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
