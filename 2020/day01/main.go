package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func strings2ints(input []string) ([]int, error) {
	result := make([]int, len(input))
	for i, item := range input {
		intItem, err := strconv.Atoi(item)
		if err != nil {
			return nil, err
		}
		result[i] = intItem
	}
	return result, nil
}

func part2(filename string) (int, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return 0, err
	}
	input := strings.TrimSpace(string(bytes))
	lines := strings.Split(input, "\n")
	numbers, err := strings2ints(lines)
	if err != nil {
		return 0, err
	}
	for i, n := range numbers {
		for j := i + 1; j < len(numbers); j++ {
			for k := j + 1; k < len(numbers); k++ {
				if n+numbers[j]+numbers[k] == 2020 {
					return n * numbers[j] * numbers[k], nil
				}
			}
		}
	}
	return 0, fmt.Errorf("No numbers summed to 2020")
}

func part1(filename string) (int, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return 0, err
	}
	input := strings.TrimSpace(string(bytes))
	lines := strings.Split(input, "\n")
	numbers, err := strings2ints(lines)
	if err != nil {
		return 0, err
	}
	for i, n := range numbers {
		for j := i + 1; j < len(numbers); j++ {
			if n+numbers[j] == 2020 {
				return n * numbers[j], nil
			}
		}
	}
	return 0, fmt.Errorf("No numbers summed to 2020")
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	p1, err := part1(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part1: %d\n", p1)
	p2, err := part2(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part2: %d\n", p2)
}
