package main

import (
	"fmt"
	"strings"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func part1(puzzleInput string) error {
	program, err := intcode.Load(puzzleInput)
	if err != nil {
		return err
	}
	intcode.Input = strings.NewReader("1\n")
	program, err = intcode.Run(program)
	if err != nil {
		return err
	}
	fmt.Printf("Part1: %d\n", program[0])
	return nil
}

func part2(puzzleInput string) error {
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
