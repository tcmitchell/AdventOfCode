package main

import (
	"fmt"
	"strings"

	"github.com/tcmitchell/AdventOfCode/2019/intcode"
)

func permutation(xs []int) (permuts [][]int) {
	var rc func([]int, int)
	rc = func(a []int, k int) {
		if k == len(a) {
			permuts = append(permuts, append([]int{}, a...))
		} else {
			for i := k; i < len(xs); i++ {
				a[k], a[i] = a[i], a[k]
				rc(a, k+1)
				a[k], a[i] = a[i], a[k]
			}
		}
	}
	rc(xs, 0)

	return permuts
}

func runAmplifier(progFile string, phase int, input int) (int, error) {
	program, err := intcode.Load(progFile)
	if err != nil {
		return 0, err
	}
	inc := make(chan int, 2)
	inc <- phase
	inc <- input
	outc := make(chan int, 1)
	progInput := fmt.Sprintf("%d\n%s", phase, input)
	intcode.Input = strings.NewReader(progInput)
	var output strings.Builder
	intcode.Output = &output
	program, err = intcode.Run(program, inc, outc)
	close(inc)
	if err != nil {
		return 0, err
	}
	return <-outc, nil
}

func runConfig(progFile string, phases []int) (int, error) {
	input := 0
	for _, phase := range phases {
		output, err := runAmplifier(progFile, phase, input)
		if err != nil {
			return 0, err
		}
		input = output
	}
	return input, nil
}

func part1(puzzleInput string) error {
	phases := []int{0, 1, 2, 3, 4}
	maxSignal := 0
	for _, p := range permutation(phases) {
		signal, err := runConfig(puzzleInput, p)
		if err != nil {
			return err
		}
		fmt.Printf("%d: %d\n", p, signal)
		if signal > maxSignal {
			maxSignal = signal
		}
	}
	fmt.Printf("Part 1: %d\n", maxSignal)
	// 9973 is too low

	return nil
}

func part2(puzzleInput string) error {
	fmt.Printf("Part 2: No answer found\n")
	return nil
}

func main() {
	err := part1("input.txt")
	if err != nil {
		panic(err)
	}
	part2("input.txt")
}
