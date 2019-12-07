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
	fmt.Println("----- Begin Part 1 -----")
	program, err = intcode.Run(program)
	if err != nil {
		return err
	}
	fmt.Println("----- End Part 1 -----")
	return nil
}

func part2(puzzleInput string) error {
	program, err := intcode.Load(puzzleInput)
	if err != nil {
		return err
	}
	intcode.Input = strings.NewReader("5\n")
	fmt.Println("----- Begin Part 2 -----")
	program, err = intcode.Run(program)
	if err != nil {
		return err
	}
	fmt.Println("----- End Part 2 -----")
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
