package intcode

import "fmt"

func doAdd(i *Interpreter) (int, error) {
	a, err := getParameter(i, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(i, 2)
	if err != nil {
		return 0, err
	}
	i.program[i.program[i.ip+3]] = a + b
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
	i.program[i.program[i.ip+3]] = a * b
	return i.ip + 4, nil
}

func doInput(i *Interpreter) (int, error) {
	// Read from the input channel, store in the parameter location
	i.program[i.program[i.ip+1]] = <-i.input
	fmt.Printf("Input: %d\n", i.program[i.program[i.ip+1]])
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
	i.program[i.program[i.ip+3]] = val
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
	i.program[i.program[i.ip+3]] = val
	return i.ip + 4, nil
}
