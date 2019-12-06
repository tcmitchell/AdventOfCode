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

// paramMode figures out the paramater mode for the given
// parameter from the instruction.
func paramMode(instruction int, param int) int {
	params := instruction / 100
	for i := param; i > 1; i-- {
		params = params / 10
	}
	return params % 10
}

// opcode gets the opcode from the instruction.
// opcode is the rightmost two digits.
func opcode(instruction int) int {
	return instruction % 100
}

// getParameter gets the given parameter taking into account
// the parameter mode.
func getParameter(program Program, pc int, param int) (int, error) {
	mode := paramMode(program[pc], param)
	switch mode {
	case 0:
		// position mode
		return program[program[pc+param]], nil
	case 1:
		// immediate mode
		return program[pc+param], nil
	default:
		// Should return an error here
		return 0, fmt.Errorf("Illegal parameter mode %d", mode)
	}
}

func doAdd(program Program, pc int) (int, error) {
	a, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(program, pc, 2)
	if err != nil {
		return 0, err
	}
	program[program[pc+3]] = a + b
	return 4, nil
}

func doMultiply(program Program, pc int) (int, error) {
	a, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(program, pc, 2)
	if err != nil {
		return 0, err
	}
	program[program[pc+3]] = a * b
	return 4, nil
}

// Execute a single opcode of an Intcode program
func Execute(program Program, pc int) (int, error) {
	switch opcode(program[pc]) {
	case opcodeAdd:
		return doAdd(program, pc)
	case opcodeMultiply:
		return doMultiply(program, pc)
	case opcodeEnd:
		return EndOfProgram, nil
	default:
		return 0, fmt.Errorf("Unknown opcode %d", opcode(program[pc]))
	}
}

func loadString(prog string) (Program, error) {
	rawCode := strings.TrimSpace(prog)
	strcode := strings.Split(rawCode, ",")
	program := make(Program, len(strcode))
	var err error
	for i, s := range strcode {
		program[i], err = strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
	}
	return program, nil

}

// Load an intcode program from file
func Load(filename string) (Program, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	return loadString(string(bytes))
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
