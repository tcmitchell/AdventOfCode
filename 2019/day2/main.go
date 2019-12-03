package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func execute(intcode []int, pc int) int {
	opcode := intcode[pc]
	switch opcode {
	case 1:
		// Add
		intcode[intcode[pc+3]] = intcode[intcode[pc+1]] + intcode[intcode[pc+2]]
		return 4
	case 2:
		// Multiply
		intcode[intcode[pc+3]] = intcode[intcode[pc+1]] * intcode[intcode[pc+2]]
		return 4
	case 99:
		return opcode
	default:
		panic(fmt.Errorf("Unknown opcode %d", opcode))
	}
}

func loadIntCode(filename string) []int {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	strcode := strings.Split(string(bytes), ",")
	intcode := make([]int, len(strcode))
	for i, s := range strcode {
		intcode[i], err = strconv.Atoi(s)
	}
	return intcode
}

func runProgram(intcode []int) []int {
	pc := 0
	for {
		offset := execute(intcode, pc)
		if offset == 99 {
			break
		}
		pc += offset
	}
	return intcode
}

func initializeProgram(puzzleInput string, noun, verb int) []int {
	intcode := loadIntCode(puzzleInput)
	intcode[1] = noun
	intcode[2] = verb
	intcode = runProgram(intcode)
	// fmt.Printf("%d\n", intcode)
	return intcode
}

func part1(puzzleInput string) {
	intcode := initializeProgram(puzzleInput, 12, 2)
	fmt.Printf("Part1: %d\n", intcode[0])
}

func part2(puzzleInput string) {
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			result := initializeProgram(puzzleInput, noun, verb)
			if result[0] == 19690720 {
				fmt.Printf("Part2: %d (noun = %d; verb = %d)\n",
					100*noun+verb, noun, verb)
			}
		}
	}
}

func main() {
	part1("input.txt")
	part2("input.txt")
}
