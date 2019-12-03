package main

import (
	"fmt"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func part1(puzzleInput string) {
	program := intcode.Initialize(puzzleInput, 12, 2)
	program = intcode.Run(program)
	fmt.Printf("Part1: %d\n", program[0])
}

func part2(puzzleInput string) {
	for noun := 0; noun < 100; noun++ {
		for verb := 0; verb < 100; verb++ {
			program := intcode.Initialize(puzzleInput, noun, verb)
			result := intcode.Run(program)
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
