package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

func part1(puzzleInput string) error {
	bytes, err := ioutil.ReadFile(puzzleInput)
	if err != nil {
		return err
	}
	allLayers := strings.TrimSpace(string(bytes))
	pixels := []rune(allLayers)
	layerSize := 25 * 6
	log.Printf("Loaded %d pixels\n", len(allLayers))
	numLayers := len(allLayers) / layerSize
	log.Printf("There are %d layers\n", numLayers)
	layers := make([]string, numLayers)
	for i := 0; i < numLayers; i++ {
		layers[i] = string(pixels[i*layerSize : i*layerSize+layerSize])
	}
	numZeroes := layerSize
	answer := 0
	for i, l := range layers {
		log.Printf("Layer %d has %d pixels", i, len(l))
		zeroes := strings.Count(l, "0")
		if zeroes < numZeroes {
			log.Printf("Layer %d has %d zeroes", i, zeroes)
			numZeroes = zeroes
			answer = strings.Count(l, "1") * strings.Count(l, "2")
		}
	}
	fmt.Printf("Part 1: %d\n", answer)
	// 2028 is too high
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
	if err != nil {
		panic(err)
	}
}
