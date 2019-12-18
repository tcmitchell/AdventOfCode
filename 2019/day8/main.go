package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

// const numCols int = 2
// const numRows int = 2
const numCols int = 25
const numRows int = 6
const layerSize int = numCols * numRows

func loadLayers(filename string) ([]string, error) {
	bytes, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	allLayers := strings.TrimSpace(string(bytes))
	pixels := []rune(allLayers)
	numLayers := len(allLayers) / layerSize
	layers := make([]string, numLayers)
	for i := 0; i < numLayers; i++ {
		layers[i] = string(pixels[i*layerSize : i*layerSize+layerSize])
	}
	return layers, nil
}

func part1(puzzleInput string) error {
	layers, err := loadLayers(puzzleInput)
	if err != nil {
		return err
	}
	numZeroes := layerSize
	answer := 0
	for _, l := range layers {
		zeroes := strings.Count(l, "0")
		if zeroes < numZeroes {
			numZeroes = zeroes
			answer = strings.Count(l, "1") * strings.Count(l, "2")
		}
	}
	fmt.Printf("Part 1: %d\n", answer)
	return nil
}

func pixelAt(layers []string, pos int) string {
	for _, l := range layers {
		switch l[pos] {
		case '0':
			return " "
		case '1':
			return "*"
		}
	}
	// Transparent all the way through the layers
	return "-"
}

func part2(puzzleInput string) error {
	layers, err := loadLayers(puzzleInput)
	if err != nil {
		return err
	}
	image := make([]string, layerSize)
	for i := range image {
		image[i] = pixelAt(layers, i)
	}
	fmt.Printf("Part 2:\n")
	for i := range image {
		if i%numCols == 0 {
			fmt.Println()
		}
		fmt.Print(image[i])
	}
	fmt.Println()
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
	// err := part2("test2.txt")
	// if err != nil {
	// 	panic(err)
	// }
}
