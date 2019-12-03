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

func part1(puzzleInput string) {
	intcode := loadIntCode(puzzleInput)
	intcode[1] = 12
	intcode[2] = 2
	intcode = runProgram(intcode)
	fmt.Printf("%d\n", intcode)
}

func main() {
	part1("input.txt")
}
