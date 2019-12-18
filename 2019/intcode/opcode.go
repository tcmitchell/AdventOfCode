package intcode

import (
	"fmt"
	"log"
)

func doAdd(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(i, 2)
	if err != nil {
		return 0, err
	}
	loc, err := paramLoc(i, 3)
	if err != nil {
		return 0, err
	}
	i.program[loc] = a + b
	return i.ip + 4, nil
}

func doMultiply(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(i, 2)
	if err != nil {
		return 0, err
	}
	loc, err := paramLoc(i, 3)
	if err != nil {
		return 0, err
	}
	i.program[loc] = a * b
	return i.ip + 4, nil
}

func doInput(i *Interpreter) (int, error) {
	// Read from the input channel, store in the parameter location
	loc, err := paramLoc(i, 1)
	if err != nil {
		return 0, err
	}
	i.program[loc] = <-i.input
	fmt.Printf("Input: %d\n", i.program[loc])
	return i.ip + 2, nil
}

func doOutput(i *Interpreter) (int, error) {
	// Write to the output channel
	param, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	fmt.Printf("Output: %d\n", param)
	i.output <- param
	return i.ip + 2, nil
}

func doJumpIfTrue(i *Interpreter) (int, error) {
	// Write to stdout
	param, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	if param != 0 {
		newPc, err := getParameter(i, 2)
		if err != nil {
			return 0, err
		}
		return newPc, nil
	}
	return i.ip + 3, nil
}

func doJumpIfFalse(i *Interpreter) (int, error) {
	// Write to stdout
	param, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	if param == 0 {
		newPc, err := getParameter(i, 2)
		if err != nil {
			return 0, err
		}
		return newPc, nil
	}
	return i.ip + 3, nil
}

func doLessThan(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(i, 2)
	if err != nil {
		return 0, err
	}
	val := 0
	if a < b {
		val = 1
	}
	loc, err := paramLoc(i, 3)
	if err != nil {
		return 0, err
	}
	i.program[loc] = val
	return i.ip + 4, nil
}

func doEquals(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(i, 2)
	if err != nil {
		return 0, err
	}
	val := 0
	if a == b {
		val = 1
	}
	loc, err := paramLoc(i, 3)
	if err != nil {
		return 0, err
	}
	i.program[loc] = val
	return i.ip + 4, nil
}

func doAdjustRelativeBase(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	oldBase := i.relBase
	i.relBase += a
	log.Printf("Adjusted relative base from %d to %d\n", oldBase, i.relBase)
	return i.ip + 2, nil
}
