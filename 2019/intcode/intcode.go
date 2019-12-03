package intcode

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

// Program is a series of intcode instructions and parameters
type Program []int

var opcodeAdd = 1
var opcodeMultiply = 2
var opcodeEnd = 99

// EndOfProgram indicates the program is complete
var EndOfProgram = 99

// Execute a single opcode of an Intcode program
func Execute(intcode []int, pc int) (int, error) {
	opcode := intcode[pc]
	switch opcode {
	case opcodeAdd:
		// Add
		intcode[intcode[pc+3]] = intcode[intcode[pc+1]] + intcode[intcode[pc+2]]
		return 4, nil
	case opcodeMultiply:
		// Multiply
		intcode[intcode[pc+3]] = intcode[intcode[pc+1]] * intcode[intcode[pc+2]]
		return 4, nil
	case opcodeEnd:
		return EndOfProgram, nil
	default:
		return 0, fmt.Errorf("Unknown opcode %d", opcode)
	}
}

// Load an intcode program from file
func Load(filename string) (Program, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	rawCode := strings.TrimSpace(string(bytes))
	strcode := strings.Split(rawCode, ",")
	program := make(Program, len(strcode))
	for i, s := range strcode {
		program[i], err = strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
	}
	return program, nil
}

// Run executes an intcode program
func Run(program Program) (Program, error) {
	pc := 0
	for {
		offset, err := Execute(program, pc)
		if err != nil {
			return nil, err
		}
		if offset == EndOfProgram {
			return program, nil
		}
		pc += offset
	}
}

// Initialize initializes an intcode program for running
func Initialize(puzzleInput string, noun, verb int) ([]int, error) {
	program, err := Load(puzzleInput)
	if err != nil {
		return nil, err
	}
	program[1] = noun
	program[2] = verb
	return program, nil
}
