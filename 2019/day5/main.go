package main

import (
	"fmt"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func part1(puzzleInput string) error {
	program, err := intcode.Load(puzzleInput)
	if err != nil {
		return err
	}
	inc := make(chan int, 1)
	inc <- 1
	outc := make(chan int, 25)
	fmt.Println("----- Begin Part 1 -----")
	program, err = intcode.Run(program, inc, outc)
	close(inc)
	if err != nil {
		return err
	}
	for out := range outc {
		fmt.Println(out)
	}
	fmt.Println("----- End Part 1 -----")
	return nil
}

func part2(puzzleInput string) error {
	program, err := intcode.Load(puzzleInput)
	if err != nil {
		return err
	}
	inc := make(chan int, 1)
	inc <- 5
	outc := make(chan int, 25)
	program, err = intcode.Run(program, inc, outc)
	close(inc)
	if err != nil {
		return err
	}
	fmt.Printf("Part 2: %d\n", <-outc)
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
