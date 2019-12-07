package intcode

import "fmt"

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
	return pc + 4, nil
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
	return pc + 4, nil
}

func doInput(program Program, pc int) (int, error) {
	// Read from Input, and store in the parameter location
	var i int
	_, err := fmt.Fscanf(Input, "%d", &i)
	if err != nil {
		return 0, err
	}
	program[program[pc+1]] = i
	return pc + 2, nil
}

func doOutput(program Program, pc int) (int, error) {
	// Write to stdout
	param, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	fmt.Println(param)
	return pc + 2, nil
}

func doJumpIfTrue(program Program, pc int) (int, error) {
	// Write to stdout
	param, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	if param != 0 {
		newPc, err := getParameter(program, pc, 2)
		if err != nil {
			return 0, err
		}
		return newPc, nil
	}
	return pc + 3, nil
}

func doJumpIfFalse(program Program, pc int) (int, error) {
	// Write to stdout
	param, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	if param == 0 {
		newPc, err := getParameter(program, pc, 2)
		if err != nil {
			return 0, err
		}
		return newPc, nil
	}
	return pc + 3, nil
}

func doLessThan(program Program, pc int) (int, error) {
	a, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(program, pc, 2)
	if err != nil {
		return 0, err
	}
	val := 0
	if a < b {
		val = 1
	}
	program[program[pc+3]] = val
	return pc + 4, nil
}

func doEquals(program Program, pc int) (int, error) {
	a, err := getParameter(program, pc, 1)
	if err != nil {
		return 0, err
	}
	b, err := getParameter(program, pc, 2)
	if err != nil {
		return 0, err
	}
	val := 0
	if a == b {
		val = 1
	}
	program[program[pc+3]] = val
	return pc + 4, nil
}
