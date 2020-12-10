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

func countPathsToDevice(adapters []int, idx int, cache map[int]int) int {
	adapterCount := len(adapters)
	if idx+1 == adapterCount {
		return 1
	}
	count := 0
	//log.Printf("Examining %d", adapters[idx])
	// Look at +1, +2, +3 to see if they are possible candidates
	// If so, add each to the total, and go from there
	current := adapters[idx]
	for i := idx + 1; i < idx+4; i++ {
		if i >= adapterCount {
			break
		}
		diff := adapters[i] - current
		//log.Printf("diff(%d, %d) = %d", joltages[i], current, diff)
		if diff <= 3 {
			value, ok := cache[i]
			if ok {
				count += value
			} else {
				count += countPathsToDevice(adapters, i, cache)
			}
		}
	}
	cache[idx] = count
	return count
}

func part2(filename string) (int, error) {
	joltages, err := aoc.ReadFileOfInts(filename)
	if err != nil {
		return 0, err
	}
	sort.Ints(joltages)
	//log.Printf("%v", joltages)
	adapters := make([]int, len(joltages)+2)
	copy(adapters[1:], joltages)
	// add the first element, a zero
	adapters[0] = 0 // The power port
	// add the last element, the device, 3 + max value
	adapters[len(joltages)+1] = joltages[len(joltages)-1] + 3
	//log.Printf("%v", adapters)
	cache := make(map[int]int)
	total := countPathsToDevice(adapters, 0, cache)
	return total, nil
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
