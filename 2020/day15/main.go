package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

func toIntArray(input []string) ([]int, error) {
	result := make([]int, len(input))
	for i, s := range input {
		num, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		result[i] = num
	}
	return result, nil
}

func runGame(input string, limit int) (int, error) {
	numberStrings := strings.Split(input, ",")
	numbers, err := toIntArray(numberStrings)
	if err != nil {
		return 0, err
	}
	// Seed the game
	said := make(map[int]int)
	turn := 1
	lastSaid := 0
	for i := 0; i < len(numbers); i++ {
		said[numbers[i]] = turn
		lastSaid = numbers[i]
		turn++
	}
	lastNew := true
	nextNum := 0
	// Play the game
	for ; turn <= limit; turn++ {
		// Was last number already said?
		lastTurn, ok := said[nextNum]
		lastNew = !ok
		said[nextNum] = turn
		lastSaid = nextNum
		//log.Printf("Turn %d: %v", turn, said)
		if lastNew {
			nextNum = 0
		} else {
			nextNum = turn - lastTurn
		}
	}

	return lastSaid, nil
}

func part1(input string) (int, error) {
	return runGame(input, 2020)
}

func part2(input string) (int, error) {
	return runGame(input, 30000000)
}

func main() {
	fmt.Println("Hello, World!")
	input := "14,8,16,0,1,17"
	p1, err := part1(input)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d\n", p1)
	p2, err := part2(input)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}
