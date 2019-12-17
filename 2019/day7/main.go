package main

import (
	"fmt"

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
	inc := make(chan int, 2)
	inc <- phase
	inc <- input
	outc := make(chan int, 1)
	i, err := intcode.NewInterpreter(progFile, inc, outc, "")
	i.Run()
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
		// fmt.Printf("%d: %d\n", p, signal)
		if signal > maxSignal {
			maxSignal = signal
		}
	}
	fmt.Printf("Part 1: %d\n", maxSignal)
	// 9973 is too low

	return nil
}

func runParallelConfig(progFile string, phases []int) (int, error) {
	inc := make([]chan int, len(phases))
	outc := make([]chan int, len(phases))

	for idx := range phases {
		inc[idx] = make(chan int, 2)
	}
	for idx := range phases[1:] {
		// fmt.Printf("outc[%d] = inc[%d]\n", idx, idx+1)
		outc[idx] = inc[idx+1]
	}
	// Output from the last amp goes to the first amp
	fmt.Printf("outc[%d] = inc[%d]\n", len(phases)-1, 0)
	outc[len(phases)-1] = inc[0]

	for idx, phase := range phases[:len(phases)-1] {
		name := fmt.Sprintf("Amp %d:%d", idx, phase)
		i, err := intcode.NewInterpreter(progFile, inc[idx], outc[idx], name)
		if err != nil {
			return 0, err
		}
		inc[idx] <- phase
		fmt.Printf("Starting amplifier %d at phase %d\n", idx, phase)
		go i.Run()
	}
	idx := len(phases) - 1
	name := fmt.Sprintf("Amp %d:%d", idx, phases[idx])
	i, err := intcode.NewInterpreter(progFile, inc[idx], outc[idx], name)
	if err != nil {
		return 0, err
	}
	inc[idx] <- phases[idx]
	// the amplifiers are all constructed and have been seeded
	// with their phases. Now start the process by sending zero
	// to the first amplifier
	inc[0] <- 0
	err = i.Run()
	if err != nil {
		return 0, err
	}
	return <-outc[idx], nil
}

func part2(puzzleInput string) error {
	phases := []int{5, 6, 7, 8, 9}
	maxSignal := 0
	for _, p := range permutation(phases) {
		signal, err := runParallelConfig(puzzleInput, p)
		if err != nil {
			return err
		}
		fmt.Printf("%d: %d\n", p, signal)
		if signal > maxSignal {
			maxSignal = signal
		}
	}
	fmt.Printf("Part 2: %d\n", maxSignal)
	// 9973 is too low

	return nil
}

func main() {
	// err := part1("input.txt")
	// if err != nil {
	// 	panic(err)
	// }
	err := part2("input.txt")
	if err != nil {
		panic(err)
	}
}
