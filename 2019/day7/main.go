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

func runAmplifier(progFile string, phase int, input string) (string, error) {
	program, err := intcode.Load(progFile)
	if err != nil {
		return "", err
	}
	progInput := fmt.Sprintf("%d\n%s", phase, input)
	intcode.Input = strings.NewReader(progInput)
	var output strings.Builder
	intcode.Output = &output
	program, err = intcode.Run(program)
	if err != nil {
		return "", err
	}
	return output.String(), nil
}

func runConfig(progFile string, phases []int) (string, error) {
	input := "0\n"
	for _, phase := range phases {
		output, err := runAmplifier(progFile, phase, input)
		if err != nil {
			return "", err
		}
		input = output
	}
	return input, nil
}

func part1(puzzleInput string) error {
	phases := []int{0, 1, 2, 3, 4}
	signal := 0
	maxSignal := 0
	for _, p := range permutation(phases) {
		result, err := runConfig(puzzleInput, p)
		if err != nil {
			return err
		}
		fmt.Sscanf(result, "%d", &signal)
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
