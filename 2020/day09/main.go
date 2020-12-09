package main

import (
	"../aoc"
	"fmt"
	"log"
)

func validSum(sum int, nums []int) bool {
	for i, num := range nums {
		for j := i + 1; j < len(nums); j++ {
			if num+nums[j] == sum {
				return true
			}
		}
	}
	return false
}

func part1(filename string, window int) (int, error) {
	numbers, err := aoc.ReadFileOfInts(filename)
	if err != nil {
		return 0, err
	}
	for i := window; i < len(numbers); i++ {
		if !validSum(numbers[i], numbers[i-window:i]) {
			return numbers[i], nil
		}
	}
	return 0, fmt.Errorf("no invalid sum found")
}

func part2(filename string) (int, error) {
	return len(filename), nil
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	window := 25

	//filename = "test-input1.txt"
	//window = 5

	p1, err := part1(filename, window)
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
