package main

import (
	"../aoc"
	"fmt"
	"log"
	"math"
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

func minIntSlice(numbers []int) int {
	min := math.MaxInt64
	for _, num := range numbers {
		if num < min {
			min = num
		}
	}
	return min
}

func maxIntSlice(numbers []int) int {
	max := math.MinInt64
	for _, num := range numbers {
		if num > max {
			max = num
		}
	}
	return max
}

func sumIntSlice(numbers []int) int {
	sum := 0
	for _, num := range numbers {
		sum += num
	}
	return sum
}

func part2(filename string, invalidNumber int) (int, error) {
	numbers, err := aoc.ReadFileOfInts(filename)
	if err != nil {
		return 0, err
	}
	// Find the position of the invalid number
	invalidIndex := -1
	for i, num := range numbers {
		if num == invalidNumber {
			invalidIndex = i
		}
	}
	//log.Printf("Invalid index: %d", invalidIndex)
	// Now find a group of numbers that sums to invalidNumber
	for i := 0; i < invalidIndex; i++ {
		for j := i + 1; j < invalidIndex; j++ {
			numSlice := numbers[i:j]
			if sumIntSlice(numSlice) == invalidNumber {
				//log.Printf("Sum of %v", numSlice)
				return minIntSlice(numSlice) + maxIntSlice(numSlice), nil
			}
		}
	}

	return 0, fmt.Errorf("no set of numbers found")
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
	p2, err := part2(filename, p1)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}
