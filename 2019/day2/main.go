package main

import (
	"fmt"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func part1(puzzleInput string) {
	program, err := intcode.Initialize(puzzleInput, 12, 2)
	if err != nil {
		panic(err)
	}
	program, err = intcode.Run(program, nil, nil)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Part1: %d\n", program[0])
}

func part2(puzzleInput string) {
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			program, err := intcode.Initialize(puzzleInput, noun, verb)
			if err != nil {
				panic(err)
			}
			result, err := intcode.Run(program, nil, nil)
			if err != nil {
				panic(err)
			}
			if result[0] == 19690720 {
				fmt.Printf("Part2: %d (noun = %d; verb = %d)\n",
					100*noun+verb, noun, verb)
			}
		}
	}
}

func main() {
	part1("input.txt")
	part2("input.txt")
}
