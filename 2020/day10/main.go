package main

import (
	"../aoc"
	"fmt"
	"log"
	"sort"
)

func part1(filename string) (int, error) {
	joltages, err := aoc.ReadFileOfInts(filename)
	if err != nil {
		return 0, err
	}
	sort.Ints(joltages)
	currentJoltage := 0
	countOnes := 0
	countThrees := 0
	for _, j := range joltages {
		diff := j - currentJoltage
		switch diff {
		case 1:
			countOnes++
		case 3:
			countThrees++
		default:
			return 0, fmt.Errorf("wrong difference: %d", diff)
		}
		currentJoltage = j
	}
	// Add the difference of 3 to the device
	countThrees++
	log.Printf("Found %d 1 differences", countOnes)
	log.Printf("Found %d 3 differences", countThrees)
	return countOnes * countThrees, nil
}

func part2(filename string) (int, error) {
	return len(filename), nil
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
