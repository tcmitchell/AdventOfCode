package main

import (
	"fmt"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func part1(puzzleInput string) error {
	inc := make(chan (int), 1)
	inc <- 1
	close(inc)
	outc := make(chan (int), 30)
	i, err := intcode.NewInterpreter(puzzleInput, inc, outc, "")
	if err != nil {
		return err
	}
	err = i.Run()
	if err != nil {
		return err
	}
	for out := range outc {
		fmt.Println(out)
	}
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
	// err := part1("input.txt")
	// if err != nil {
	// 	panic(err)
	// }
}
