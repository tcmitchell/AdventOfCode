package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// The Register holds all the register values
type Register map[string]int

type instructionFunc func(register Register, args []string) int

type instruction struct {
	exe  instructionFunc
	args []string
}

// ReadInputLines reads the input file line by line,
// passing each line to the given channel.
func ReadInputLines(infile string, c chan string) {
	f, err := os.Open(infile)
	if err != nil {
		panic("foo")
	}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		c <- scanner.Text()
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}
	close(c)
}

func getValue(arg string, register Register) int {
	val, err := strconv.Atoi(arg)
	if err != nil {
		return register[arg]
	}
	return val
}

func doSet(register Register, args []string) int {
	x := args[0]
	y := args[1]
	register[x] = getValue(y, register)
	fmt.Printf("set %s %d\n", x, register[x])
	// Go to the next instruction
	return 1
}

func doJnz(register Register, args []string) int {
	x := getValue(args[0], register)
	y := getValue(args[1], register)
	if x != 0 {
		return y
	}
	return 1
}

func doMul(register Register, args []string) int {
	x := args[0]
	y := getValue(args[1], register)
	register[x] = getValue(x, register) * y
	register["mul"]++
	return 1
}

func doSub(register Register, args []string) int {
	x := args[0]
	y := getValue(args[1], register)
	register[x] = getValue(x, register) - y
	return 1
}

func makeInstruction(inputLine string) (instruction, error) {
	parts := strings.Split(inputLine, " ")
	switch parts[0] {
	case "set":
		return instruction{doSet, parts[1:]}, nil
	case "jnz":
		return instruction{doJnz, parts[1:]}, nil
	case "mul":
		return instruction{doMul, parts[1:]}, nil
	case "sub":
		return instruction{doSub, parts[1:]}, nil
	}
	return instruction{}, fmt.Errorf("Unknown instruction %s", parts[0])
}

func loadProgram(c chan string) []instruction {
	result := make([]instruction, 0)
	for line := range c {
		instr, err := makeInstruction(line)
		if err != nil {
			continue
		}
		result = append(result, instr)
	}
	return result
}

func runProgram(program []instruction) {
	register := make(Register)
	pc := 0
	for pc >= 0 && pc < len(program) {
		pc += program[pc].exe(register, program[pc].args)
	}
	fmt.Printf("Executed %d mul instructions.", register["mul"])
}

func main() {
	c := make(chan string, 1)
	go ReadInputLines("input.txt", c)
	program := loadProgram(c)
	fmt.Printf("Program size: %d\n", len(program))
	runProgram(program)
}
