package intcode

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// Program is a series of intcode instructions and parameters
type Program []int

// Execute a single opcode of an Intcode program
func Execute(intcode []int, pc int) int {
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

// Load an intcode program from file
func Load(filename string) []int {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		panic(err)
	}
	strcode := strings.Split(string(bytes), ",")
	program := make([]int, len(strcode))
	for i, s := range strcode {
		program[i], err = strconv.Atoi(s)
	}
	return program
}

// Run executes an intcode program
func Run(program Program) Program {
	pc := 0
	for {
		offset := Execute(program, pc)
		if offset == 99 {
			break
		}
		pc += offset
	}
	return program
}

// Initialize initializes an intcode program for running
func Initialize(puzzleInput string, noun, verb int) []int {
	intcode := Load(puzzleInput)
	intcode[1] = noun
	intcode[2] = verb
	return intcode
}
