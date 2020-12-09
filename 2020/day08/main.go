package main

import (
	"../aoc"
	"fmt"
	"log"
	"strconv"
)

type Instruction struct {
	Type     string
	Offset   int
	Executed bool
}

func (i Instruction) String() string {
	return fmt.Sprintf("%s %d", i.Type, i.Offset)
}

type Program struct {
	Instructions []Instruction
	PC           int
	Accumulator  int
}

func (p Program) Copy() *Program {
	var result Program
	result.Instructions = make([]Instruction, len(p.Instructions))
	copy(result.Instructions, p.Instructions)
	result.Accumulator = p.Accumulator
	result.PC = p.PC
	return &result
}

func loadProgram(filename string) (*Program, error) {
	lines, err := aoc.ReadFileOfStrings(filename)
	if err != nil {
		return nil, err
	}
	var program Program
	program.Instructions = make([]Instruction, len(lines))
	for i, line := range lines {
		program.Instructions[i].Type = line[:3]
		offset, err := strconv.Atoi(line[4:])
		if err != nil {
			return nil, err
		}
		program.Instructions[i].Offset = offset
	}
	return &program, nil
}

func executeInstruction(program *Program, pc int) (int, error) {
	//fmt.Printf("Executing %d: %s with accumulator %d\n", program.PC,
	//	program.Instructions[pc], program.Accumulator)
	//time.Sleep(1 * time.Second)
	switch program.Instructions[pc].Type {
	case "nop":
		program.Instructions[pc].Executed = true
		// Advance the PC by 1
		return 1, nil
	case "jmp":
		program.Instructions[pc].Executed = true
		return program.Instructions[pc].Offset, nil
	case "acc":
		program.Instructions[pc].Executed = true
		program.Accumulator += program.Instructions[pc].Offset
		return 1, nil
	default:
		return 0, fmt.Errorf("unknown instruction %s", program.Instructions[pc].Type)
	}
}

func part1(filename string) (int, error) {
	program, err := loadProgram(filename)
	if err != nil {
		return 0, err
	}
	//for _, i := range program.Instructions {
	//	log.Println(i)
	//}
	for {
		if program.Instructions[program.PC].Executed {
			return program.Accumulator, nil
		}
		offset, err := executeInstruction(program, program.PC)
		if err != nil {
			return 0, err
		}
		program.PC += offset
	}
}

func main() {
	fmt.Println("Hello, World!")
	filename := "input.txt"
	//filename = "test-input1.txt"
	p1, err := part1(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 1: %d\n", p1)
	p2, err := part2(filename)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Part 2: %d\n", p2)
}

func runProgram(program *Program, change int) (int, error) {
	switch program.Instructions[change].Type {
	case "nop":
		program.Instructions[change].Type = "jmp"
	case "jmp":
		program.Instructions[change].Type = "nop"
	default:
		return 0, fmt.Errorf("not changeable")
	}
	for {
		if program.PC >= len(program.Instructions) {
			return program.Accumulator, nil
		}
		if program.Instructions[program.PC].Executed {
			return 0, fmt.Errorf("infinite loop")
		}
		offset, err := executeInstruction(program, program.PC)
		if err != nil {
			return 0, err
		}
		program.PC += offset
	}
}

func part2(filename string) (int, error) {
	program, err := loadProgram(filename)
	if err != nil {
		return 0, err
	}
	//for _, i := range program.Instructions {
	//	log.Println(i)
	//}
	for i := 0; i < len(program.Instructions); i++ {
		acc, err := runProgram(program.Copy(), i)
		if err == nil {
			return acc, err
		}
	}
	return 0, fmt.Errorf("no solution found")
}
