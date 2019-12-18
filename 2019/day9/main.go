package main

import (
	"fmt"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func runBoost(filename string, input int) (int, error) {
	inc := make(chan (int), 1)
	inc <- input
	close(inc)
	outc := make(chan (int), 30)
	i, err := intcode.NewInterpreter(filename, inc, outc, "")
	if err != nil {
		return 0, err
	}
	err = i.Run()
	if err != nil {
		return 0, err
	}
	return <-outc, nil
}

func part1(puzzleInput string) error {
	answer, err := runBoost(puzzleInput, 1)
	if err != nil {
		return err
	}
	fmt.Printf("Part 1: %d\n", answer)
	return nil
}

func part2(puzzleInput string) error {
	answer, err := runBoost(puzzleInput, 2)
	if err != nil {
		return err
	}
	fmt.Printf("Part 2: %d\n", answer)
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	err = part2("input.txt")
	if err != nil {
		panic(err)
	}
}
